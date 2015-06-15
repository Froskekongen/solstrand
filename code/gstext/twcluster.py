#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

import sqlite3

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import ProjectedGradientNMF

from sklearn.pipeline import make_pipeline

from tokenizers import tokenize_nor,get_nor_stopwords
from datetime import datetime



from sklearn.cluster import KMeans, MiniBatchKMeans

from elasticsearch import Elasticsearch
from elasticsearch import helpers


#from tokenizers import tokenize_nor,get_nor_stopwords


def main():

    es_client = Elasticsearch(hosts = [{ "host" : "localhost", "port" : 9200 }])

    index_name = "twclusters"

    if es_client.indices.exists(index_name):
        print("deleting '%s' index..." % (index_name))
        print(es_client.indices.delete(index = index_name, ignore=[400, 404]))

    print("creating '%s' index..." % (index_name))
    print(es_client.indices.create(index = index_name))


    from tokenizers import tokenize_nor,get_nor_stopwords
    tok=lambda a:tokenize_nor(a,get_nor_stopwords())

    docs=[]
    other=[]
    conn=sqlite3.connect('../data/tweets.sqlite')
    cur=conn.execute('select * from T')
    for iii,row in enumerate(cur):
        doc={}
        doc['_id']=row[3]
        doc['created_at']=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        doc['author_id']=row[1]
        doc['text']=row[4]
        doc['language']=row[5]
        if len(tok(doc['text']))>2:
            docs.append(doc['text'])
            other.append( (doc['created_at'],doc['author_id']) )
        if len(docs)>=100000:
            break

    cur.close()


    cv=CountVectorizer(tokenizer=tok, max_df=0.5,min_df=5)



    # for iii,t in enumerate(tc):
    #     print(iii,t)
    #     if iii>100:
    #         break
    M=cv.fit_transform(docs).astype(np.float)
    M2=Normalizer(copy=False).fit_transform(M)

    km=KMeans(n_clusters=20, init='k-means++', max_iter=200, n_init=5,\
                verbose=True)

    km.fit_transform(M2)
    clusters=km.labels_

    sortInds=[i[0] for i in sorted(enumerate(clusters), key=lambda x:x[1])]

    nmf=ProjectedGradientNMF(n_components=10)
    M3=nmf.fit_transform(M2)
    print(M3.shape)

    tDict={}
    maxInd=0
    esDocs=[]
    for iii in sortInds:
        dd={}
        dd['tweet']=docs[iii]
        dd['cluster']=int(clusters[iii])

        c2=tuple(np.argsort(M3[iii,:])[-2:])
        if c2 in tDict:
            cc=tDict[c2]
        else:
            cc=maxInd
            tDict[c2]=maxInd
            maxInd=maxInd+2

        dd['cluster2']=cc
        dd['created_at']=other[iii][1]
        dd['author_id']=other[iii][0]
        esDocs.append(dd)
        #print(clusters[iii],other[iii],other[iii])

    res = helpers.bulk(es_client, esDocs, index=index_name, doc_type='tweet', refresh=True)



if __name__ == '__main__' :
  main()
