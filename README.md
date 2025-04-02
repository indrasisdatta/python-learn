# Python learning guide for beginners

This repository contains information and steps related to installing Python packages and managing dependencies in a Python project, along with basic Python code snippets.

## Pip Install Command

To install a Python package in a specific local directory, use the following command:

```bash
py -m pip install <package-name> --target=<path/to/local/directory>
```

## Generate requirements.txt using this command:

```bash
py -m pip freeze > requirements.txt
```

## Other devs can install the dependencies in requirements.txt

```bash
py -m pip install -r requirements.txt
```

## Create virtual environment

```bash
py -m venv .venv
```

## Activate virtual environment

```bash
.venv\Scripts\activate
```

## Conda commands

```
conda create -p venv1 python=3.10 -y
```

```
conda env list
```

```
conda activate D:\Code\Python\python-learn\conda_example\venv1
```

```
python -m pip install numpy
```

```
py (the Python launcher) ignores your active virtual environment and instead follows its own logic to select a Python version.

python modules.py uses the Python interpreter from the active virtual environment (which is why it works).
```

```
streamlit run app.py
```
