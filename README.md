# FEUP-PRI

Group project for the PRI course unit at FEUP.

This project focused on building an information retrieval system for a collection of scientific papers. The system includes document processing, indexing, search capabilities, and evaluation metrics.

## Components

- **Collection**: Scripts for collecting and preprocessing scientific papers
- **Processing**: Text processing and feature extraction (tokenization, stemming, etc.)
- **Indexing**: Apache Solr configuration and schema for document indexing
- **Querying**: Search interface and query processing
- **Evaluation**: Information retrieval evaluation metrics and relevance judgments
- **Client**: Web interface for searching the document collection

## Running

The project uses Docker Compose to orchestrate the services:

```bash
docker-compose up
```

This will start:
- Apache Solr instance for document indexing
- Python processing pipeline
- Web client (if available)

## Requirements

- Docker and Docker Compose
- Python 3.x (for local development)
- See `requirements.txt` for Python dependencies

## Unit info

- **Name**: Processamento e Representação de Informação (Information Processing and Representation)
- **Date**: Year 1, Semester 1, 2023/24
- [**More info**](https://sigarra.up.pt/feup/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=518807)

## Disclaimer

This repository (and all others with the name format `feup-*`) are for archival and educational purposes only.

If you don't understand some part of the code or anything else in this repo, feel free to ask (although I may not understand it myself anymore).

Keep in mind that this repo is public. If you copy any code and use it in your school projects you may be flagged for plagiarism by automated tools.
