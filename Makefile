.PHONY: all
all: venv/bin/python

venv/bin/python: setup.py
	rm -rf ./venv
	python -m venv --copies ./venv
	./venv/bin/pip install --upgrade --quiet pip
	./venv/bin/pip install -e .

.PHONY: dev
dev: venv/bin/python
	./venv/bin/pip install -e .[dev]

.PHONY: test
test: venv/bin/python
	./venv/bin/python -m unittest

.PHONY: clean
clean:
	rm -rf ./venv
	rm -rf ./mixtape.egg-info
