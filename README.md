# TREC 2020 Conversational Assistance

This project focuses on developing methods to retrieve relevant passages from two large datasets. We implement both a baseline method using the BM25 retrieval model and an advanced method using BERT.

## Project Overview

The goal of this project is to enhance the retrieval of relevant passages from extensive datasets. The baseline method leverages the BM25 retrieval model, while the advanced method utilizes BERT for improved accuracy and relevance.

## Indexing Data

To index the MS-MARCO and CAR data collections, we have implemented an indexing module. You need to update the path to your specific data collections. Additionally, ensure that an Elasticsearch server is up and running.

### Elasticsearch

Elasticsearch is used to index the data for the BM25 algorithm. It provides a distributed, RESTful search and analytics engine capable of addressing a growing number of use cases. Ensure that your Elasticsearch server is properly configured and running before indexing the data.

## Requirements

We have listed the package requirements in the [requirements.txt]("./requirements"). Use the following command to install the necessary packages:


```shell
python -m pip install -r requirements.txt
```

## To run the retreival models

Run the baseline method:<br>

```shell
python baseline_method.py
```

Run the advance method:<br>

```shell
python advanced_method.py
```

## Testing the results

You can use the commands in the this section to run test using trec-eval tools:

### Baseline method evaluation

For the manual rewritten queries:<br>

```shell
trec_eval -q data/judgment_file.txt data/results/bm25_man_results.txt > data/benchmark/result_man_bm25.txt -m all_trec
```

For the automatic rewritten queries:<br>

```shell
trec_eval -q data/judgment_file.txt data/results/bm25_auto_results.txt > data/benchmark/result_auto_bm25.txt -m all_trec
```

### Advanced method evaluation

For the manual rewritten queries:<br>

```shell
trec_eval -q data/judgment_file.txt data/results/bert_rerank_manual_results.txt > data/benchmark/result_man_bert.txt -m all_trec
```

For the automatic rewritten queries:<br>

```shell
trec_eval -q data/judgment_file.txt data/results/bert_rerank_auto_results.txt > data/benchmark/result_auto_bert.txt -m all_trec
```
