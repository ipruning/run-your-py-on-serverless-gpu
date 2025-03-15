#!/usr/bin/env bash

usage() {
  cat <<EOF
Run a Python script or Marimo notebook in a Modal cloud environment.

Usage:
    $(basename "$0") [options] <script.py>

Options:
    -h, --help     Show this help message

Parameters:
    script.py   - Path to the Python script or Marimo notebook (.py file) to run

Example:
    $(basename "$0") my_script.py

EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
  -h | --help)
    usage
    ;;
  *)
    if [ -f "$1" ] && [[ "$1" =~ \.py$ ]]; then
      script_path=$(realpath "$1")
      echo "Using script: $script_path"

      if grep -q "import marimo" "$script_path"; then
        export MARIMO_NOTEBOOK_PATH="$script_path"
        executor="modal-execute-marimo.py"
      else
        export PY_SCRIPT_PATH="$script_path"
        executor="modal-execute-py.py"
      fi

      shift
    else
      usage
    fi
    ;;
  esac
done

if [ -z "$script_path" ]; then
  usage
fi

$executor
