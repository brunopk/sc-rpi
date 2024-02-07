# Python virtual environments

## Creating virtual environments

```bash
python3 -m venv <path of the venv>
```

or :

```bash
virtualenv -m <path to the python interpreter> <path of the venv>
```

## Activating the environment

```bash
source <path of the venv>/bin/activate
```

## Installing dependencies

After activating the environment:

```bash
pip install -r requirements.txt
```
