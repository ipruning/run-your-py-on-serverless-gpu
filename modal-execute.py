#!/usr/bin/env uvx modal run
import os
import subprocess
import time
from pathlib import Path

import modal

PY_SCRIPT_PATH = Path(os.getenv("PY_SCRIPT_PATH", ""))

if not PY_SCRIPT_PATH.exists():
    raise ValueError("PY_SCRIPT_PATH IS NOT SET / DOES NOT EXIST")

app = modal.App(
    image=modal.Image.debian_slim()
    .pip_install("uv")
    .add_local_file(
        PY_SCRIPT_PATH,
        remote_path="/root/main.py",
    )
)


@app.function(max_containers=1, timeout=1_500, gpu="H100")  # L40S
def run_py(timeout: int):
    py_process = subprocess.Popen(
        [
            "uv",
            "run",
            "/root/main.py",
        ],
    )

    try:
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(5)
        print(f"Reached end of {timeout} second timeout period. Exiting...")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        py_process.kill()


@app.local_entrypoint()
def main():
    run_py.remote(1000)
