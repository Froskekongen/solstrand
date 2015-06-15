#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gensim import corpora
from tokenizers import tokenize_nor,get_nor_stopwords


class VPCorpus(object):

    def __init__(self,txtfile,limit=100000,additional_cols=None,do_tok=True):
        self.limit=limit
        self.txtfile=txtfile
        self.stopwords=get_nor_stopwords()
        self.do_tok=do_tok


    def __iter__(self):
        with open(self.txtfile) as ff:
            for iii,line in enumerate(ff):
                line=line.split(';')

                if iii<self.limit:
                #   ll=list([(iii,dd) for iii,dd in enumerate(line)])
                #    print(ll)
                    if self.do_tok:
                        yield tokenize_nor(line[15]+' '+line[16],self.stopwords)
                    else:
                        yield line[15]+' '+line[16]
                else:
                    break

def main():
    fpath='../docker/vpdata/iconproducts.csv'

    tc=VPCorpus(fpath)

    dic=corpora.dictionary.Dictionary()
    dic.add_documents(tc)
    print(dic)
    dic.filter_extremes(no_below=5, no_above=0.5)
    print(dic)
    # for iii,t in enumerate(tc):
    #     print(iii,t)
    #     if iii>10000:
    #         break


if __name__ == '__main__' :
  main()
