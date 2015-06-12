#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from gensim import corpora



def tokenize(doc,stopwords):
    raw=doc.split()
    toks = [w.lower().strip(' ,.\t?"\'\n:') for w in raw]
    toks = [w for w in toks if w not in stopwords]
    return toks

class TwitterCorpus(object):

    def __init__(self,cur,limit=1000000):
        self.limit=limit
        self.cur=cur
        stopwords=open('resources/stoppord_no.txt').readlines()
        stopwords=[s.strip() for s in stopwords]
        stopwords.extend(['rt','…',''])
        #print(stopwords)
        self.stopwords=set(stopwords)


    def __iter__(self):
        for iii,line in enumerate(self.cur):
            if iii<self.limit:
                yield tokenize(line[0],self.stopwords)
            else:
                break

def main():
    conn = sqlite3.connect('../data/tweets.sqlite')
    cur=conn.execute('select text from T')

    tc=TwitterCorpus(cur)

    dic=corpora.dictionary.Dictionary()
    dic.add_documents(tc)
    print(dic)
    dic.filter_extremes(no_below=10, no_above=0.5)
    print(dic)
    # for iii,t in enumerate(tc):
    #     print(iii,t)
    #     if iii>10000:
    #         break
    cur.close()


if __name__ == '__main__' :
  main()
