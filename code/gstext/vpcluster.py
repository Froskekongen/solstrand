#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD

from sklearn.pipeline import make_pipeline

from tokenizers import tokenize_nor,get_nor_stopwords



from sklearn.cluster import KMeans, MiniBatchKMeans

from elasticsearch import Elasticsearch
from elasticsearch import helpers


#from tokenizers import tokenize_nor,get_nor_stopwords


def main():

    es_client = Elasticsearch(hosts = [{ "host" : "localhost", "port" : 9200 }])

    index_name = "vpclusters"

    if es_client.indices.exists(index_name):
        print("deleting '%s' index..." % (index_name))
        print(es_client.indices.delete(index = index_name, ignore=[400, 404]))

    print("creating '%s' index..." % (index_name))
    print(es_client.indices.create(index = index_name))


    from tokenizers import tokenize_nor,get_nor_stopwords
    fpath='../docker/vpdata/iconproducts.csv'

    docs=[]
    typeLand=[]
    with open(fpath) as ff:
        for iii,line in enumerate(ff):
            line=line.split(';')
            if iii==0:
                dl=[(iii,tt) for iii,tt in enumerate(line)]
                print(dl)
            if line[15] or line[16]:
                docs.append(line[15]+' '+line[16])
                typeLand.append([line[6],line[20]])


    tok=lambda a:tokenize_nor(a,get_nor_stopwords())

    cv=CountVectorizer(tokenizer=tok, max_df=0.5,min_df=5)



    # for iii,t in enumerate(tc):
    #     print(iii,t)
    #     if iii>100:
    #         break
    M=cv.fit_transform(docs).astype(np.float)
    M2=Normalizer(copy=False).fit_transform(M)

    km=KMeans(n_clusters=8, init='k-means++', max_iter=100, n_init=1,\
                verbose=True)

    km.fit_transform(M2)
    clusters=km.labels_

    sortInds=[i[0] for i in sorted(enumerate(clusters), key=lambda x:x[1])]

    esDocs=[]
    for iii in sortInds:
        dd={}
        dd['Beskrivelse']=docs[iii]
        dd['cluster']=int(clusters[iii])
        dd['Land']=typeLand[iii][1]
        dd['Type']=typeLand[iii][0]
        esDocs.append(dd)
        print(clusters[iii],typeLand[iii],docs[iii])

    res = helpers.bulk(es_client, esDocs, index=index_name, doc_type='beskriv', refresh=True)



if __name__ == '__main__' :
  main()
