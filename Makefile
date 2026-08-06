PYTHON ?= python3

.PHONY: check validate doc-freshness test coverage

check: validate doc-freshness test

validate:
	$(PYTHON) scripts/validate.py

doc-freshness:
	$(PYTHON) scripts/check_doc_freshness.py

test:
	PYTHONPATH=src $(PYTHON) -m pytest

coverage:
	PYTHONPATH=src $(PYTHON) -m pytest --cov=mentaury --cov-report=term-missing
