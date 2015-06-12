from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pymongo import MongoClient

es_client = Elasticsearch(hosts = [{ "host" : "localhost", "port" : 39200 }])

index_name = "enron"

if es_client.indices.exists(index_name):
    print("deleting '%s' index..." % (index_name))
    print(es_client.indices.delete(index = index_name, ignore=[400, 404]))

print("creating '%s' index..." % (index_name))
print(es_client.indices.create(index = index_name))

bulk_data = []

conn = MongoClient('localhost', 41000)
coll = conn['enron_mail']['messages']

cursor = coll.find(timeout=False)

# for iii,doc in enumerate(cursor):
#     del doc['_id']
#     print(doc)
#     if iii>0:
#         break

for iii,doc in enumerate(cursor):
    del doc['_id']
    doc['_id']=iii
    bulk_data.append(doc)

    #print(iii,doc)
    if iii%1000==0:
        #res = es_client.bulk(index=index_name,body=bulk_data,refresh=True)
        print(iii,doc)
        res = helpers.bulk(es_client, bulk_data, index=index_name, doc_type='mail', refresh=True)
        bulk_data.clear()
#res = es_client.bulk(index=index_name,body=bulk_data,refresh=True)
res = helpers.bulk(es_client, bulk_data, index=index_name, doc_type='mail', refresh=True)
bulk_data.clear()

cursor.close()
