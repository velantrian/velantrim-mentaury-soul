PYTHON ?= python3

.PHONY: check validate test coverage

check: validate test

validate:
	$(PYTHON) scripts/validate.py

test:
	PYTHONPATH=src $(PYTHON) -m pytest

coverage:
	PYTHONPATH=src $(PYTHON) -m pytest --cov=mentaury --cov-report=term-missing
