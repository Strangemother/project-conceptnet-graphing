"""Serve as a first layer connect to the dataset and a word grammer correction"""

# from database.graph import GraphDB
from database.graph import *
import database
from database.db import *

ASSERTIONS_DIR = "E:/conceptnet/_lmdb_assertions/"
BRIDGE_DB_DIR = "E:/conceptnet/_lmdb_server_ui/"

"""The persistent source of original knowledge. held in the shared resource."""
assertions_db = GraphDB(write=False, directory=ASSERTIONS_DIR, name='assertions')
"""Any relative data to store for the internal procedures."""
db = GraphDB(directory=BRIDGE_DB_DIR, name='bridge')

import inflect
"""
methods:
          classical inflect
          plural plural_noun plural_verb plural_adj singular_noun no num a an
          compare compare_nouns compare_verbs compare_adjs
          present_participle
          ordinal
          number_to_words
          join
          defnoun defverb defadj defa defan
    INFLECTIONS:    classical inflect
          plural plural_noun plural_verb plural_adj singular_noun compare
          no num a an present_participle
    PLURALS:   classical inflect
          plural plural_noun plural_verb plural_adj singular_noun no num
          compare compare_nouns compare_verbs compare_adjs
    COMPARISONS:    classical
          compare compare_nouns compare_verbs compare_adjs
    ARTICLES:   classical inflect num a an
    NUMERICAL:      ordinal number_to_words
    USER_DEFINED:   defnoun defverb defadj defa defan

Exceptions:
 UnknownClassicalModeError
 BadNumValueError
 BadChunkingOptionError
 NumOutOfRangeError
 BadUserDefinedPatternError
 BadRcFileError
 BadGenderError
"""
plurals = inflect.engine()


def fetch(word):
    """given a single word, fix plural and singular - returning graph picks"""
    pass


def get_siblings(word):
    """Return a set of assocated words theough noun and plural etc... extraction.
    """

    # func for each word type.
    defs = ('plural',
            'plural_noun',
            'plural_verb',
            'plural_adj',
            'singular_noun',
            'present_participle',)

    _max = max( (len(x) for x in defs) )

    # Once we get a bunch of words, check if they exist as graphs;
    # Delete unknown words, store correctly spelt words, populate with existing
    # words.

    for func in defs:
        val = getattr(plurals, func)(word)
        print("{:>{}} {}".format(func, _max, val))

    # split graph words from unknown words
    # delete error word and store unknown
    # define indefinate article.

    # p.a("cat")        # -> "a cat"

    # p.compare("index","index")      # RETURNS "eq"
    # p.compare("index","indexes")    # RETURNS "s:p"
    # p.compare("index","indices")    # RETURNS "s:p"
    # p.compare("indexes","index")    # RETURNS "p:s"
    # p.compare("indices","index")    # RETURNS "p:s"
    # p.compare("indices","indexes")  # RETURNS "p:p"
    # p.compare("indexes","indices")  # RETURNS "p:p"
    # p.compare("indices","indices")  # RETURNS "eq"
