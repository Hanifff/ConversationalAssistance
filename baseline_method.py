import json
from typing import List, Dict

from elasticsearch.client import Elasticsearch
from index_data import IndexManagement


class BaseLine(IndexManagement):
    def __init__(self, es_cli: Elasticsearch, collection_name: str = "MARCO_") -> None:
        super(BaseLine, self).__init__(es_cli)
        self.collection_name = collection_name

    def analyze_query(self, query: str, field: str, index_name: str) -> List[str]:
        """Analyzes a query with respect to the relevant index.

        Args:
            es: Elasticsearch object instance.
            query: String of query terms.
            field: The field with respect to which the query is analyzed.
            index: Name of the index with respect to which the query is analyzed.

        Returns:
            A list of query terms that exist in the specified field among the
            documents in the index.
        """
        tokens = self.es_cli.indices.analyze(
            index=index_name, body={"text": query})["tokens"]
        query_terms = []
        for t in sorted(tokens, key=lambda x: x["position"]):
            # Use a boolean query to find at least one document that contains the
            # term.
            hits = (
                self.es_cli.search(
                    index=index_name,
                    query={"match": {field: t["token"]}},
                    _source=False,
                    size=1,
                )
                .get("hits", {})
                .get("hits", {})
            )
            doc_id = hits[0]["_id"] if len(hits) > 0 else None
            if doc_id is None:
                continue
            query_terms.append(t["token"])
        return query_terms

    def score_term(self, index_name: str, filepath: str) -> Dict[str, List[str]]:
        """We rank queries using the default BM25 in elastisc search module.
            , query_ids: List[str], all_queries: Dict[str, str], 

        Args:
            index_name: Name of indexing instance.
            query_ids: List of query Ids.
            all_queries: A key value set of all queries.

        Returns:
            A set of ranked queries.
        """
        rankings = {}
        data = {}
        Q_0 = 0
        with open(file=filepath) as f:
            data = json.load(f)
        for i in range(len(data)):
            print(data[i]["turn"])

        """ for hit in hits:
            TOPICID_TURNID = hit["number"]+"_"+hit["number"]["number"]
            # Q_O
            passage_identifier = self.collection_name+query_id
            # rank
            # score

        for i, query_id in enumerate(query_ids):
            print(
                "Processing query {}/{} ID {}".format(
                    i + 1, len(query_ids), query_id
                )
            )
            # First-pass retrieval
            query_terms = self.analyze_query(
                self.es_cli, all_queries[query_id], "body", index=index_name
            )

            hits = self.es_cli.search(
                index=index_name, q=" ".join(query_terms), _source=True, size=1
            )["hits"]["hits"]
            rankings[query_id] = [hit["_id"] for hit in hits]
        return rankings """


if __name__ == "__main__":
    es_cli = Elasticsearch(
        timeout=30, max_retries=5, retry_on_timeout=True)
    filepath = "./data/evaluation/2020_manual_evaluation_topics_v1.0.json"
    index_name = 'ms_marco'
    index_mng = BaseLine(es_cli, 'MARCO_')
    index_mng.score_term(index_name, filepath)
