from re import split
from typing import Dict, Mapping
from elasticsearch import Elasticsearch
import cbor
import json
from trec_car.read_data import *


class IndexManagement:
    def __init__(self):
        self.es_cli = Elasticsearch(
            timeout=200, max_retries=15, retry_on_timeout=True)
        self.es_cli.info()
        # use default setting
        self.setting = {
            "settings": {
                "number_of_shards": 5,
                "index": {
                    "similarity": {
                        "default": {
                            "type": "BM25",
                            "b": 0.75,
                            "k1": 1.2,
                        }
                    }
                }
            }
        }

    def index_text_data(self, index_name: str, filepath: str) -> None:
        """ Indexes data into the elastics search instance.
        Args:
            index_name: Name of index.
            doc_id: Id of the document to be indexed.
            doc: Document to be indexed.
        """

        batch_size = 5000
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

    def index_cbor_data(self, index_name: str, filepath: str) -> None:
        """[summary]

        Args:
            index_name (str): [description]
            filepath (str): [description]
        """
        batch_size = 5000
        bulk_data = []
        with open(filepath, 'rb') as fp:
            for i, para in enumerate(iter_paragraphs(fp)):
                para_id = para.para_id
                body = [elem.text if isinstance(elem, ParaText)
                        else elem.anchor_text
                        for elem in para.bodies]
                body = ' '.join(body)

                elem = {"doc_id": para_id, "body": body.strip()}
                json_elem = json.dumps(elem)
                _elem = json.loads(json_elem)
                bulk_data.append(
                    {"index": {"_index": index_name,
                               "_id": _elem.pop("doc_id")}}
                )
                bulk_data.append(_elem)
                if (i+1) % batch_size == 0:
                    self.es_cli.bulk(index=index_name,
                                     body=bulk_data, refresh=True)
                    bulk_data = []

            if len(bulk_data) > 0:
                self.es_cli.bulk(index=index_name,
                                 body=bulk_data, refresh=True)

    def reset_index(self, index_name: str) -> None:
        """ Removes instance of elastics search.
        Args:
            index_name: Name of index.
            index_setting: Index setting chosen for the elastics search instance.
        """
        if self.es_cli.indices.exists(index_name):
            self.es_cli.indices.delete(index=index_name)
        # self.es_cli.create(index=index_name)


if __name__ == "__main__":
    """ filepath_marco = "D:\data_collection/collection.tsv"
    filepath_car = "../data_collection/dedup.articles-paragraphs.cbor"
    index_name = 'ms_marco'
    index_mng = IndexManagement()
    index_mng.reset_index(index_name)
    index_mng.index_text_data(index_name, filepath_marco)
    index_mng.index_cbor_data(index_name, filepath_car) """

    es = Elasticsearch()
    print(es.count(index="ms_marco"))
