.PHONY: all
all: venv/bin/mixtape

venv/bin/python:
	python -m venv ./venv --copies

venv/bin/mixtape: venv/bin/python
	./venv/bin/pip install -e .

.PHONY: clean
clean:
	rm -rf ./venv
	rm -rf ./mixtape.egg-info
