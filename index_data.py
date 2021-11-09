from elasticsearch import Elasticsearch
import csv

def index_data(es, file):
    
    es.indices.create(index='ms_marco')
    with open(file) as f:
        tsv_file = csv.reader(f, delimiter="\t")
        i = 0
        for line in tsv_file:
            es.index(index='ms_marco', id=line[0], body=line[1])


index_data(Elasticsearch, 'data/collection.tsv')
