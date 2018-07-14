"""A prototype of the graphing data core, to allow weighted data from
rows
"""

from conceptnet import sqlite_db
db = sqlite_db.spread_db()


class Connection(object):

    def __init__(self, start, end, rel,weight):
        self.start = start
        self.end = end
        self.rel = rel
        self.weight = weight

words = {}

word_dic = {}
word_dic_counter = 0

def dic(word):
    global word_dic_counter
    index = word_dic_counter
    word_dic_counter += 1
    if index in word_dic:
        return word_dic[index]

    word_dic[index] = word
    return index

REVERSE = 'reverse'

class Weighted(object):
    def __init__(self, word, weight, reverse=False):
        self.word = word
        self.weight = weight
        self.reverse = reverse

    def __repr__(self):
        s = '<Weight {} {}>'.format(self.word, self.weight)
        return s

def weighted(*a):
    return Weighted(*a)


def back_weighted(relation_word, value):
    return weighted(relation_word, value)

def graph_word(word, words=None, reverse=True):
    words = words or {}
    lines = db.get_word(word)

    for start, end, rel, weight, _json in lines:
        d_start = str(start)
        d_end = str(end)
        d_rel = dic(str(rel))

        if d_start not in words:
            words[d_start] = {}

        if rel not in words[d_start]:
            words[d_start][rel] = ()

        # words[d_start][rel] += ( (d_end, weighted(rel, weight),), )
        words[d_start][rel] += ( (d_end, weight,), )

        if reverse is True:
            if d_end not in words:
                words[d_end] = ()
            #words[d_end] += ( (d_start, weighted(rel, weight, True),), )
            words[d_end] += ( (d_start, (weight, True,),), )

    return words
