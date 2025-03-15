#!/usr/bin/env uvx modal run
import os
import secrets
import subprocess
import time
from pathlib import Path

import modal

IPYNB_PATH = Path(os.getenv("IPYNB_PATH", ""))

if not IPYNB_PATH.exists():
    raise ValueError("IPYNB_PATH IS NOT SET / DOES NOT EXIST")

app = modal.App(
    image=modal.Image.debian_slim()
    .pip_install("jupyterlab")
    .add_local_file(IPYNB_PATH, remote_path="/root/notebook.ipynb")
)

TOKEN = secrets.token_urlsafe(16)
PORT = 8888


@app.function(max_containers=1, timeout=1_500, gpu="H100")  # L40S
def run_jupyter(timeout: int):
    with modal.forward(PORT) as tunnel:
        jupyter_process = subprocess.Popen(
            [
                "jupyter",
                "lab",
                "--ip=0.0.0.0",
                f"--port={PORT}",
                f"--NotebookApp.token='{TOKEN}'",
                "--no-browser",
                "--allow-root",
                "--notebook-dir=/root",
            ],
        )

        print(f"Jupyter Lab available at => {tunnel.url}?token={TOKEN}")
        print("Your notebook is at: /root/notebook.ipynb")

        try:
            end_time = time.time() + timeout
            while time.time() < end_time:
                time.sleep(5)
            print(f"Reached end of {timeout} second timeout period. Exiting...")
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            jupyter_process.kill()


@app.local_entrypoint()
def main():
    run_jupyter.remote(1000)
