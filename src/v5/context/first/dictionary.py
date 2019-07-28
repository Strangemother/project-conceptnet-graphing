"""
from v4 import dictionary
CACHE_PATH = "C:/Users/jay/Documents/projects/context-api/context/src/cache"
set_global_root(CACHE_PATH)
# Set global cache dir C:/Users/jay/Documents/projects/context-api/context/src/cache

from v4 import dictionary as D
D.get_word('apples')
"""
from PyDictionary import PyDictionary
from .cache import get_cache, set_cache, set_global_root

dictionary = None

CACHE_PATH = "C:/Users/jay/Documents/projects/context-api/context/src/cache"

set_global_root(CACHE_PATH)

def make_dictionary():
    global dictionary
    dictionary = PyDictionary()
    return dictionary

def get_dictionary():
    global dictionary
    if dictionary is None:
        dictionary = make_dictionary()
    return dictionary


def get_word(value):
    '''Return the entire feed of a word from cache or API.'''
    wd = get_dictionary()

    filename = 'dictionary_word_{}.pyf'.format(value)
    success, val = get_cache(filename)
    if success is True:
        print('returning cache word')
        return val

    val = dict(
        value=value,
        meaning=wd.meaning(value),
        synonym=wd.synonym(value),
        antonym=wd.antonym(value),
    )

    set_cache(filename, val)
    return val
