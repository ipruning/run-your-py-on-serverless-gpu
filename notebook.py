import marimo

__generated_with = "0.11.20"
app = marimo.App()


@app.cell
def _(mo):
    mo.md("""# Hello, from inside Modal!""")
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    subprocess.run(["nvidia-smi"])
    return (subprocess,)


if __name__ == "__main__":
    app.run()
