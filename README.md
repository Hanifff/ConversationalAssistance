# dat640_project

The aim of this project is to ...

### Baseline Evaluation

`trec_eval -q data/judgment_file.txt data/results/bm25_man_results.txt > data/benchmark/result_man_bm25.txt -m all_trec`
`trec_eval -q data/judgment_file.txt data/results/bm25_auto_results.txt > data/benchmark/result_auto_bm25.txt -m all_trec`

`trec_eval -q data/judgment_file.txt data/results/bert_rerank_manual_results.txt > data/benchmark/result_man_bert.txt -m all_trec`
`trec_eval -q data/judgment_file.txt data/results/bert_rerank_auto_results.txt > data/benchmark/result_auto_bert.txt -m all_trec`
