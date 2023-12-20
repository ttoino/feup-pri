FROM python:3.11-slim as data

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y make git gcc g++ graphviz graphviz-dev jq musl-dev python3-dev libffi-dev
RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./characterization ./characterization
COPY ./collection ./collection
COPY ./common ./common
COPY ./processing ./processing
COPY ./Makefile ./Makefile

CMD ["make"]

FROM data as data-static

RUN make

FROM solr:9.4-slim as solr

COPY ./solr/advanced.json ./schema.json
COPY ./solr/config.json ./config.json
COPY ./solr/mapping-FoldToASCII.txt ./mapping-FoldToASCII.txt
COPY ./solr/synonyms.txt ./synonyms.txt

COPY --from=data-static /app/data/processed/stories ./stories

RUN init-var-solr && \
    start-local-solr && \
    ./bin/solr create_core -c luis && \
    cp ./mapping-FoldToASCII.txt /var/solr/data/luis/conf/mapping-FoldToASCII.txt && \
    cp ./synonyms.txt /var/solr/data/luis/conf/synonyms.txt && \
    curl --data-binary @./schema.json -H 'Content-type:application/json' http://localhost:8983/solr/luis/schema && \
    ./bin/solr post -url http://localhost:8983/solr/luis/update ./stories && \
    curl --data-binary @./config.json -H 'Content-type:application/json' http://localhost:8983/solr/luis/config && \
    mv /var/solr/data/luis /tmp/luis

USER root

RUN echo "mv /tmp/luis /var/solr/data/luis" >> /docker-entrypoint-initdb.d/99-luis.sh

USER $SOLR_UID
