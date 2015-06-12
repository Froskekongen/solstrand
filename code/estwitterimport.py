from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sqlite3
from datetime import datetime
import re as regex

es_client = Elasticsearch(hosts = [{ "host" : "localhost", "port" : 39200 }])

index_name = "twitter"

#hashtagre=regex.compile(r'(^|[^0-9A-Z&/]+)(#|\uFF03)([0-9A-Z_]*[A-Z_]+[a-z0-9_\\u00c0-\\u00d6\\u00d8-\\u00f6\\u00f8-\\u00ff]*)')
retweetre = regex.compile(r'(RT|retweet|from|via)(?:\b\W*@(\w+))+',flags=regex.IGNORECASE)
mentionre = regex.compile(r'^(?!RT|retweet|from|via)(?:\b\W*@(\w+))+',flags=regex.IGNORECASE)
hashtagre=regex.compile('(?:#|\uFF03)(?:[0-9a-zæøå\\u00c0-\\u00d6\\u00d8-\\u00f6\\u00f8-\\u00ff_]+)',flags=regex.IGNORECASE)
atre=regex.compile('@[\w0-9_]+',flags=regex.IGNORECASE)


if es_client.indices.exists(index_name):
    print("deleting '%s' index..." % (index_name))
    print(es_client.indices.delete(index = index_name, ignore=[400, 404]))

print("creating '%s' index..." % (index_name))
print(es_client.indices.create(index = index_name))

bulk_data = []

conn=sqlite3.connect('data/tweets.sqlite')


cursor = conn.execute('select * from T')
colnames=[]
for cn in cursor.description:
    colnames.append(cn[0])

print(colnames)

# for iii,doc in enumerate(cursor):
#     del doc['_id']
#     print(doc)
#     if iii>0:
#         break

for iii,row in enumerate(cursor):
    doc={}
    doc['_id']=row[3]
    doc['created_at']=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
    doc['author_id']=row[1]
    doc['retweet_count']=row[2]
    doc['text']=row[4]
    doc['language']=row[5]
    doc['hashtags']=hashtagre.findall(doc['text'])
    doc['ats']=atre.findall(doc['text'])

    bulk_data.append(doc)

    #print(iii,doc)
    if iii%10000==0:
        #res = es_client.bulk(index=index_name,body=bulk_data,refresh=True)
        print(doc['text'])
        print(doc['ats'])
        print()
        res = helpers.bulk(es_client, bulk_data, index=index_name, doc_type='mail', refresh=True)
        bulk_data.clear()
    # if iii>10000:
    #     break
#res = es_client.bulk(index=index_name,body=bulk_data,refresh=True)
res = helpers.bulk(es_client, bulk_data, index=index_name, doc_type='tweet', refresh=True)
bulk_data.clear()

cursor.close()
