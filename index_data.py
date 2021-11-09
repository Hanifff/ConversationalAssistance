from typing import Dict
from elasticsearch import Elasticsearch


class IndexManagement:
    def __init__(self):
        self.es_cli = Elasticsearch()

    def init_index(self, index_name: str, index_setting: Dict) -> None:
        """ Creates an instance of elastics search.

        Args:
            index_name: Name of index.
            index_setting: Index setting chosen for the elastics search instance.
        """
        if self.es_cli.indices.exists(index_name):
            self.es_cli.indices.delete(index=index_name)

        self.es_cli.indices.create(index=index_name, body=index_setting)

    def index_data(self, index_name: str, doc_id: str, doc: str):
        """ Indexes data into the elastics search instance.

        Args:
            index_name: Name of index.
            doc_id: Id of the document to be indexed.
            doc: Document to be indexed.
        """
        self.es_cli.index(index=index_name,
                          doc_type="_doc", id=doc_id, body={'body': doc})


def index_msmarco(filepath: str):
    """ Initalizes an instance of IndexManagement and defines the index's setting.
        Then, it indexes each line of ms_marco document using the elastiscsearch instance.

    Args:
        filepath: Path of ms_marco document in local disk.
    """
    index_name = 'ms_marco'
    index_mng = IndexManagement()
    index_setting = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        }
    }

    index_mng.init_index(index_name, index_setting)
    f = open(filepath, 'r', encoding='utf-8')
    lines = f.readlines()

    for line in lines:
        line = line.split('\t')
        index_mng.index_data(index_name, line[0], line[1])


if __name__ == "__main__":
    filepath = '../data_collection/collection.tsv'
    index_msmarco(filepath)
