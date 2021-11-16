import json
from baseline_method import BaseLine
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class AdvancedMethod(BaseLine):
    def __init__(self, model_name) -> None:
        super(AdvancedMethod, self).__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def rerank_docs(self, index_name: str, filepath: str) -> None:
        """Ranks passages using the default BM25 in elastisc search module.
            The result is written in a text file with trec_eval format requirements.

        Args:
            index_name: Name of indexing instance.
            query_ids: List of query Ids.
            all_queries: A key value set of all queries.
        """
        data = {}
        Q_0 = str(0)
        with open(file=filepath) as f:
            data = json.load(f)
        f.close()
        bert_rerank_result = open(
            "./data/results/bert_rerank_manual_results.txt", "w")

        for i in range(len(data)):
            TOPICID = str(data[i]["number"])+'_'
            for turn in data[i]['turn']:
                TOPICID_TURNID = TOPICID+str(turn["number"])

                query = turn['manual_rewritten_utterance']
                #query = turn['automatic_rewritten_utterance']

                # First-pass retrieval
                query_terms = self.analyze_query(
                    query, "body", index_name)

                hits = self.es_cli.search(
                    index=index_name, q=" ".join(query_terms), _source=True, size=500
                )["hits"]["hits"]
                docs = [None]*500
                for i in range(len(hits)):
                    docs[i] = hits[i]['_source']['body'].strip()

                # Second-pass reranking - #BERT BASE
                features = self.tokenizer(
                    [" ".join(query_terms)]*500, docs,  padding=True, truncation=True, return_tensors="pt")

                self.model.eval()
                scores = None
                reranks = {}

                with torch.no_grad():
                    scores = self.model(**features).logits

                for i in range(len(hits)):
                    passage_id = ""
                    if len(hits[i]["_id"]) < 12:
                        passage_id = "MARCO_" + hits[i]["_id"]
                    else:
                        passage_id = "CAR_" + hits[i]["_id"]
                    reranks[passage_id] = torch.tensor(scores[i][0]).item()

                # in descending order sort the items based on score
                sorted_reranks = dict(
                    sorted(reranks.items(), key=lambda item: item[1], reverse=True))

                # retrive the first 100 docs from 500 bm25 ranked docs
                sorted_reranks = dict(list(sorted_reranks.items())[:100])
                # put results in trec_eval required format
                rank = 1
                for passage_id, score in sorted_reranks.items():
                    bert_rerank_result.write(TOPICID_TURNID+' '+Q_0 + ' '+passage_id +
                                             ' '+str(rank)+' '+str(round(score, 2))+' '+"Team-011"+'\n')
                    rank += 1

        bert_rerank_result.close()


if __name__ == "__main__":
    index_mng = AdvancedMethod(
        model_name="cross-encoder/ms-marco-MiniLM-L-2-v2")
    index_mng.rerank_docs(
        index_name='ms_marco', filepath='./data/evaluation/2020_manual_evaluation_topics_v1.0.json')
