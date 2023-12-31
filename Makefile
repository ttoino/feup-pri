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

semantic_query:
	$(PYTHON) query_embedding.py

# init-solr-flat:
init-solr:
	-docker compose up -d solr
	-docker compose exec solr bin/solr delete -c luis-basic
	-docker compose exec solr bin/solr create_core -c luis-basic
	-curl --data-binary @solr/basic.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-basic/schema
	-docker compose exec solr bin/solr post -url http://localhost:8983/solr/luis-basic/update /stories/stories
	-docker compose exec solr bin/solr delete -c luis-advanced
	-docker compose exec solr bin/solr create_core -c luis-advanced
	-docker compose exec solr cp /data/mapping-FoldToASCII.txt /var/solr/data/luis-advanced/conf/
	-docker compose exec solr cp /data/synonyms.txt /var/solr/data/luis-advanced/conf/
	-curl --data-binary @solr/advanced.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/schema
	-docker compose exec solr bin/solr post -url http://localhost:8983/solr/luis-advanced/update /stories/stories
	-curl --data-binary @solr/config.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/config
