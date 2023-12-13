FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get -y install graphviz graphviz-dev jq

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./characterization ./characterization
COPY ./collection ./collection
COPY ./common ./common
COPY ./processing ./processing
COPY ./Makefile ./Makefile
COPY ./get_embeddings.py ./get_embeddings.py

CMD ["make"]
