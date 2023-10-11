PYTHON = python3

MAKEFLAGS += --always-make

all: collect process characterize

# This can fail in some linux distributions, be careful 
prepare:
	$(PYTHON) -m pip install -r requirements.txt

collect:
	$(PYTHON) -m collection.collect

process:
	$(PYTHON) -m processing.process

characterize:
	$(PYTHON) -m characterization.characterize
