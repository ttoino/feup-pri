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

init-solr-flat:
	-docker compose exec solr bin/solr delete -c luis-basic
	-docker compose exec solr bin/solr create_core -c luis-basic
	-docker compose exec solr bin/post -c luis-basic /stories
	-docker compose exec solr bin/solr delete -c luis-advanced
	-docker compose exec solr bin/solr create_core -c luis-advanced
	-docker compose exec solr cp /data/mapping-FoldToASCII.txt /var/solr/data/luis-advanced/conf/
	-curl --data-binary @solr/advanced.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/schema
	-docker compose exec solr bin/post -c luis-advanced /stories

init-solr-nested:
	-python -m solr.prepare
	-docker compose exec solr bin/solr delete -c luis-basic
	-docker compose exec solr bin/solr create_core -c luis-basic
	-curl -X POST --data-binary @solr/data.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/update
	-docker compose exec solr bin/solr delete -c luis-advanced
	-docker compose exec solr bin/solr create_core -c luis-advanced
	-docker compose exec solr cp /data/mapping-FoldToASCII.txt /var/solr/data/luis-advanced/conf/
	-curl --data-binary @solr/advanced.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/schema
	-curl -X POST --data-binary @solr/data.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/update
