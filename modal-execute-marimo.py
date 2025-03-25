#!/usr/bin/env uvx modal run
import os
import secrets
import subprocess
import time
from pathlib import Path

import modal

MARIMO_NOTEBOOK_PATH = Path(os.getenv("MARIMO_NOTEBOOK_PATH", ""))

if not MARIMO_NOTEBOOK_PATH.exists():
    raise ValueError("MARIMO_NOTEBOOK_PATH IS NOT SET / DOES NOT EXIST")

app = modal.App(
    image=modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install("uv")
    .add_local_file(MARIMO_NOTEBOOK_PATH, remote_path="/root/main.py")
)

TOKEN = secrets.token_urlsafe(16)
PORT = 2718


@app.function(max_containers=1, timeout=1_500, gpu="H100")  # L40S
def run_marimo(timeout: int):
    with modal.forward(PORT) as tunnel:
        print("modal: Starting sshx...")
        sshx_process = subprocess.Popen(
            ["sh", "-c", "curl -sSf https://sshx.io/get | sh -s run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        def monitor_sshx_output():
            if sshx_process.stdout is None:
                print("sshx: [Error] sshx stdout is None")
                return

            for line in iter(sshx_process.stdout.readline, ""):
                print(f"sshx: {line.strip()}")

        import threading

        sshx_thread = threading.Thread(target=monitor_sshx_output, daemon=True)
        sshx_thread.start()

        marimo_process = subprocess.Popen(
            [
                "uvx",
                "marimo",
                "edit",
                "--headless",
                "--host",
                "0.0.0.0",
                "--port",
                str(PORT),
                "--token-password",
                TOKEN,
                "/root/main.py",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        def monitor_marimo_output():
            if marimo_process.stdout is None:
                print("marimo: [Error] marimo stdout is None")
                return

            for line in iter(marimo_process.stdout.readline, ""):
                print(f"marimo: {line.strip()}")

        marimo_thread = threading.Thread(target=monitor_marimo_output, daemon=True)
        marimo_thread.start()

        print(f"modal: Marimo available at => {tunnel.url}?access_token={TOKEN}")

        try:
            end_time = time.time() + timeout
            while time.time() < end_time:
                time.sleep(5)
            print(f"modal: Reached end of {timeout} second timeout period. Exiting...")
        except KeyboardInterrupt:
            print("modal: Exiting...")
        finally:
            sshx_process.kill()
            marimo_process.kill()


@app.local_entrypoint()
def main():
    run_marimo.remote(1000)
