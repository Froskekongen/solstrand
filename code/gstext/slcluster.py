#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

import json

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

    index_name = "slclusters"

    if es_client.indices.exists(index_name):
        print("deleting '%s' index..." % (index_name))
        print(es_client.indices.delete(index = index_name, ignore=[400, 404]))

    print("creating '%s' index..." % (index_name))
    print(es_client.indices.create(index = index_name))


    import re
    rr=re.compile(r"[\w']+")
    tok=lambda a:rr.findall(a)

    ff1=open('../docker/syslog.csv').readlines()
    aa=[]
    for d in ff1:
        #print(d)
        try:
            aa.append(json.loads(d))
        except:
            continue
    print(len(aa))
    # ff='\n'.join(ff1)
    docs=[]
    other=[]
    # aa=json.loads(ff)
    #print(aa)

    for iii,row in enumerate(aa):
        if len(tok(row['syslog_message']))>3:
            doc={}
            doc['created_at']=datetime.strptime(row["@timestamp"], "%Y-%m-%dT%H:%M:%S.000Z")
            doc['text']=row['syslog_message']
            docs.append(doc['text'])
            other.append( doc['created_at'] )
            print(doc['text'])
            print(tok(doc['text']))
            print()
            if len(docs)>=100000:
                break


    cv=CountVectorizer(tokenizer=tok, max_df=0.5,min_df=5)



    # for iii,t in enumerate(tc):
    #     print(iii,t)
    #     if iii>100:
    #         break
    M=cv.fit_transform(docs).astype(np.float)
    M2=Normalizer(copy=False).fit_transform(M)

    km=KMeans(n_clusters=30, init='k-means++', max_iter=200, n_init=5,\
                verbose=True)

    km.fit_transform(M2)
    clusters=km.labels_

    sortInds=[i[0] for i in sorted(enumerate(clusters), key=lambda x:x[1])]

    nmf=ProjectedGradientNMF(n_components=30)
    M3=nmf.fit_transform(M2)
    print(M3.shape)

    tDict={}
    maxInd=0
    esDocs=[]
    for iii in sortInds:
        dd={}
        dd['message']=docs[iii]
        dd['cluster']=int(clusters[iii])

        c2=tuple(np.argsort(M3[iii,:])[-1:])
        if c2 in tDict:
            cc=tDict[c2]
        else:
            cc=maxInd
            tDict[c2]=maxInd
            maxInd=maxInd+1

        dd['cluster2']=cc
        dd['created_at']=other[iii]
        esDocs.append(dd)
        #print(clusters[iii],other[iii],other[iii])

    res = helpers.bulk(es_client, esDocs, index=index_name, doc_type='syslogmsg', refresh=True)



if __name__ == '__main__' :
  main()
