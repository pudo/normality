
all: clean test

install:
	pip install -q '.[dev]'

test: install
	pytest
	mypy --strict normality

clean:
	rm -rf dist build .eggs .mypy_cache .pytest_cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +