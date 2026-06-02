.PHONY: setup daily fetch extract analyse rewrite publish serve clean

PYTHON := python3
PIPELINE := $(PYTHON) -m pipeline

setup:
	cd code && $(PYTHON) -m venv venv && \
	  ./venv/bin/pip install -r requirements.txt && \
	  ./venv/bin/pip install -r ../pipeline/requirements.txt
	@echo "✓ Setup complete. Activate with: source code/venv/bin/activate"

daily:
	$(PIPELINE) fetch
	$(PIPELINE) extract
	$(PIPELINE) analyse

fetch:
	$(PIPELINE) fetch

extract:
	$(PIPELINE) extract

analyse:
	$(PIPELINE) analyse

rewrite:
	$(PIPELINE) rewrite

publish:
	$(PIPELINE) publish

serve:
	cd code && $(PYTHON) -m uvicorn app.main:app --reload --port 8001
