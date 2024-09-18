# Makefile

# Variables
PYTHON = python3
PIP = pip
PYLINT = pylint
AUTOPEP8 = autopep8
PYTEST = pytest

# Install dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install pytest==6.2.5
	$(PIP) install pylint==2.10.2
	$(PIP) install autopep8==1.5.7

# Run linting
lint:
	$(PYLINT) app tests

# Run tests
test:
	$(PYTEST) --maxfail=1 --disable-warnings -q

# Format code
format:
	$(AUTOPEP8) --in-place --aggressive --aggressive app tests

# Clean generated files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# Default target
.PHONY: install lint test format clean
