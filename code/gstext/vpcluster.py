#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD

from sklearn.pipeline import make_pipeline
from vpcorpus import VPCorpus

from tokenizers import tokenize_nor,get_nor_stopwords


#from tokenizers import tokenize_nor,get_nor_stopwords


def main():
    from tokenizers import tokenize_nor,get_nor_stopwords
    fpath='../docker/vpdata/iconproducts.csv'
    tok=lambda a:tokenize_nor(a,get_nor_stopwords())

    tc=VPCorpus(fpath,do_tok=False)
    cv=CountVectorizer(tokenizer=tok, max_df=0.5,min_df=5)



    # for iii,t in enumerate(tc):
    #     print(iii,t)
    #     if iii>100:
    #         break
    M=cv.fit_transform(tc).as_type(np.float)
    print(type(M))


if __name__ == '__main__' :
  main()
