from re import split
from typing import Dict
from elasticsearch import Elasticsearch
import cbor2
import json


class IndexManagement:
    def __init__(self, es_cli: Elasticsearch):
        self.es_cli = es_cli
        self.es_cli.info()
        # use default setting
        self.setting = {
            "settings": {
                "number_of_shards": 5,
                "index": {
                    "similarity": {
                        "default": {
                            "type": "BM25",
                            "b": 1.2,
                            "k1": 1.2,
                        }
                    }
                }
            }
        }

    def index_data(self, index_name: str, filepath: str) -> None:
        """ Indexes data into the elastics search instance.
        Args:
            index_name: Name of index.
            doc_id: Id of the document to be indexed.
            doc: Document to be indexed.
        """

        batch_size = 1000
        f = open(filepath, 'r', encoding='utf-8')
        lines = f.readlines()
        for i in range(0, len(lines), batch_size):
            bulk_data = []
            for line in lines[i:i+batch_size]:
                doc = line.split('\t')
                curr_doc = {"doc_id": doc[0], "body": doc[1].strip()}
                json_doc = json.dumps(curr_doc)
                _doc = json.loads(json_doc)
                bulk_data.append(
                    {"index": {"_index": index_name,
                               "_id": _doc.pop("doc_id")}}
                )
                bulk_data.append(_doc)

            self.es_cli.bulk(index=index_name, body=bulk_data, refresh=True)

    def reset_index(self, index_name: str) -> None:
        """ Removes instance of elastics search.
        Args:
            index_name: Name of index.
            index_setting: Index setting chosen for the elastics search instance.
        """
        if self.es_cli.indices.exists(index_name):
            self.es_cli.indices.delete(index=index_name)
        self.es_cli.create(index=index_name, body=self.setting)


if __name__ == "__main__":
    es_cli = Elasticsearch(
        timeout=30, max_retries=5, retry_on_timeout=True)
    filepath = "D:\data_collection/collection.tsv"
    index_name = 'ms_marco'
    index_mng = IndexManagement(es_cli)
    # index_mng.reset_index(index_name)
    index_mng.index_data(index_name, filepath)
