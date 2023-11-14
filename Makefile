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

init-solr:
	-docker compose exec solr bin/solr delete -c luis-basic
	-docker compose exec solr bin/solr create_core -c luis-basic
	-curl -T solr/basic.json http://localhost:8983/solr/luis-basic/schema
	-docker compose exec solr bin/solr post -c luis-basic /stories
	-docker compose exec solr bin/solr delete -c luis-advanced
	-docker compose exec solr bin/solr create_core -c luis-advanced
	-curl -T solr/advanced.json http://localhost:8983/solr/luis-advanced/schema
	-docker compose exec solr bin/solr post -c luis-advanced /stories
