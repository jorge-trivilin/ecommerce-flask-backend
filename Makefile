# Makefile

# Variables
PYTHON = python3
PIP = pip
PYLINT = pylint
AUTOPEP8 = autopep8
PYTEST = pytest

# Install all dependencies
install: install-prod install-dev

# Install production dependencies
install-prod:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Install development dependencies
install-dev:
	$(PIP) install -r dev-requirements.txt

# Run linting
lint:
	$(PYLINT) app tests

# Run tests
test:
	$(PYTEST) --maxfail=1 --disable-warnings -q

# Format code
format:
    find app tests -name '*.py' -exec $(AUTOPEP8) --in-place --aggressive --aggressive {} +
    git config --global user.email "jorge.trivilin@gmail.com"
    git config --global user.name "Jorge Trivilin"
    git diff --exit-code || (git add . && git commit -m "Auto-format code" && echo "Changes committed")

# Clean generated files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# Default target
.PHONY: install install-prod install-dev lint test format clean