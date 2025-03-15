#!/usr/bin/env bash

usage() {
  cat <<EOF
Run a Python script, Marimo notebook, or Jupyter notebook in a Modal cloud environment.

Usage:
    $(basename "$0") [options] <file>

Options:
    -h, --help     Show this help message

Parameters:
    file   - Path to the file to run:
             - Python script (.py)
             - Marimo notebook (.py with marimo imports)
             - Jupyter notebook (.ipynb)

Example:
    $(basename "$0") my_script.py
    $(basename "$0") my_notebook.ipynb
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
  -h | --help)
    usage
    ;;
  *)
    if [ -f "$1" ]; then
      file_path=$(realpath "$1")
      echo "Using file: $file_path"

      if [[ "$1" =~ \.ipynb$ ]]; then
        export IPYNB_PATH="$file_path"
        executor="./modal-execute-ipynb.py"
      elif [[ "$1" =~ \.py$ ]]; then
        if grep -q "import marimo" "$file_path"; then
          export MARIMO_NOTEBOOK_PATH="$file_path"
          executor="./modal-execute-marimo.py"
        else
          export PY_SCRIPT_PATH="$file_path"
          executor="./modal-execute.py"
        fi
      else
        echo "Error: Unsupported file type. Please provide a .py or .ipynb file."
        usage
      fi

      shift
    else
      usage
    fi
    ;;
  esac
done

if [ -z "$file_path" ]; then
  usage
fi

$executor
