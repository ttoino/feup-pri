PYTHON = python3

MAKEFLAGS += --always-make


all: collect process add_vector characterize

# This can fail in some linux distributions, be careful 
prepare:
	$(PYTHON) -m pip install -r requirements.txt

collect:
	$(PYTHON) -m collection.collect

process:
	$(PYTHON) -m processing.process

add_vector:
	jq -n '[ inputs ]' data/processed/stories/*.json | $(PYTHON) get_embeddings.py | jq -c . > data/processed/stories_with_vector.json

characterize:
	$(PYTHON) -m characterization.characterize

semantic_query:
	$(PYTHON) query_embedding.py

# init-solr-flat:
init-solr:
	-docker compose up -d solr
	-docker compose exec solr bin/solr delete -c luis-basic
	-docker compose exec solr bin/solr create_core -c luis-basic
	-docker compose exec solr bin/solr post -url http://localhost:8983/solr/luis-basic/update /stories/stories
	-docker compose exec solr bin/solr delete -c luis-advanced
	-docker compose exec solr bin/solr create_core -c luis-advanced
	-docker compose exec solr cp /data/mapping-FoldToASCII.txt /var/solr/data/luis-advanced/conf/
	-docker compose exec solr cp /data/synonyms.txt /var/solr/data/luis-advanced/conf/
	-curl --data-binary @solr/advanced.json -H 'Content-type:application/json' http://localhost:8983/solr/luis-advanced/schema
	-docker compose exec solr bin/solr post -url http://localhost:8983/solr/luis-advanced/update /stories/stories_with_vector.json
	- curl -X POST -H 'Content-type:application/json' \
        --data-binary "{ \
            \"add-requesthandler\" : { \
                \"name\": \"/mlt\", \
                \"class\": \"solr.MoreLikeThisHandler\", \
                \"defaults\": {\"mlt.fl\": \"content, title, author, related_champions.name\"} \
            } \
        }" http://localhost:8983/solr/luis-advanced/config
