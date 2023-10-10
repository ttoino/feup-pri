PYTHON = python

MAKEFLAGS += --always-make

prepare:
# This can fail in some linux distributions, be careful 
	$(PYTHON) -m pip install -r requirements.txt

collect:
	$(PYTHON) collection/collect.py

characterize:
	$(PYTHON) characterization/characterize.py