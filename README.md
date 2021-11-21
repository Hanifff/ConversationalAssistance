# TREC 2020 Conversational Assistance - DAT640 project

This is a course project for the Information retrieval and text mining (DAT640) course at the University of Stavanger.<br>
In this project, we develop one baseline and one advanced method to retrieve relevant passages from two large data sets. In the baseline method, we use the BM25 retrieval model and for the advanced method, we use BERT.

## To index data

In order to index the MS-MARCO and CAR data collection, we have implemented an indexing module. However, you need to change the path to your specisifc path of data collections.<br>
In addition you need a elastisc search server up and running.

## Requirements

We have listed are package requirements in the [requirements.txt]("./requirements"). Use the following command to install: <br>

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
