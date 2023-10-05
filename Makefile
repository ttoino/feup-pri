PYTHON = python

MAKEFLAGS += --always-make

collect:
	$(PYTHON) collection/collect.py
