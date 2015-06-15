


def tokenize_nor(doc,stopwords):
    raw=doc.split()
    toks = [w.lower().strip(' ,.\t?"\'\n:') for w in raw]
    toks = [w for w in toks if w not in stopwords]
    return toks


def get_nor_stopwords():
    with open('resources/stoppord_no.txt') as ff:
        stopwords = ff.readlines()
    stopwords=[s.strip() for s in stopwords]
    stopwords.extend(['rt','…',''])
    return set(stopwords)
