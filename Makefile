VENV_PREFIX=.venv/Scripts
PYTHON3=$(VENV_PREFIX)/python
PIP3=$(VENV_PREFIX)/pip3

website:
	export NO_COLOR=true
	$(PYTHON3) app.py

install:
	python -m venv .venv
	$(PIP3) install -r requirements.txt

uninstall:
	rm -rf .venv

.PHONY: website install uninstall
