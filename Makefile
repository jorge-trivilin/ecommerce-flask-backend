install:
	pip install --upgrade pip
	pip install pytest==6.2.5
	pip install pylint==2.10.2
	pip install autopep8==1.5.7

lint:
	pylint

test:
	pytest

format:
	autopep8 --in-place --aggressive --aggressive