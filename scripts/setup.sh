#!/usr/bin/env bash
set -e

# Determine requested extra ("cpu" or "macos") if any
EXTRA="$1"

PYTHON_VERSION=$(cat .python-version)

# Install Python version if missing
if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
    pyenv install "${PYTHON_VERSION}"
fi


# Use pyenv's Python without altering the user's global configuration
export PYENV_VERSION="${PYTHON_VERSION}"

# Create virtual environment if it doesn't exist
if [ ! -d .venv ]; then
    pyenv exec python -m venv .venv
fi

# Activate venv and install dependencies
source .venv/bin/activate
pip install -U pip

if [[ -n "$EXTRA" ]]; then
    pip install -e ".[$EXTRA]"
else
    pip install -e .
fi

echo "Environment ready. Activate with 'source .venv/bin/activate'."
