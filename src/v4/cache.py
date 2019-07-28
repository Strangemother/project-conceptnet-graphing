import os
import io
import json


root_path = os.path.abspath(os.path.dirname(__file__))

def set_global_root(path):
    global root_path
    root_path = os.path.abspath(path)
    print( 'Set global cache dir', root_path)
    if os.path.exists(root_path) is False:
        print( 'creating', root_path)
        os.makedirs(root_path)


def write_json(relpath, data):
    filepath = resolve_path(relpath)
    with io.open(filepath, 'w') as stream:
        stream.write(unicode(json.dumps(data, indent=4)))


WARNED_STRING_CACHE_DEPRECATION = False

def string_cache(string):
    global WARNED_STRING_CACHE_DEPRECATION
    if WARNED_STRING_CACHE_DEPRECATION is False:
        print( 'string_cache is deprecated. Use "get_string_cache"')
        WARNED_STRING_CACHE_DEPRECATION = True
    string_cache = get_string_cache
    return get_string_cache(string)


def get_string_cache(string):
    filepath = cache_filename(string)
    success, v = get_cache(filepath)
    if success:
        return v
    return None

def set_string_cache(string, value):
    return set_cache(cache_filename(string), value)

def get_cache(relpath):


    # sc = spell(s)
    # if s != sc:
    #     print( 'Corrected Spelling: "{}"'.format(sc))
    #     s = sc
    success = False
    v = ''
    filepath = resolve_path(relpath)

    if os.path.isfile(filepath) is False:
        dirp, fpath = os.path.split(filepath)
        fname, fext = os.path.splitext(fpath)
        cpath = "{}.{}".format(slugify(fpath), fext)
        filepath = os.path.join(dirp, cpath)

    if os.path.isfile(filepath):
        print( 'opening {}'.format(filepath))
        with open(filepath, 'r') as stream:
            v = ''.join(stream.readlines())
        if len(v) > 0:
            v = eval(v)
            success = True

    return success, v


def resolve_path(filepath):

    if os.path.isabs(filepath) is False:
        cpath = os.path.join(root_path, filepath)
    else:
        cpath = filepath

    return cpath


def set_cache(filepath, v):
    cpath = resolve_path(slugify(filepath))
    print( 'writing {}'.format(cpath))

    with open(cpath, 'w') as stream:
        stream.write(str(v))
        return True
    return False


import unicodedata
import re

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    return value
    value = value.encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value

def cache_filename(string):
    return 'cache_{}.txt'.format(string.replace(' ', '_'))


def delete_word(word):
    string_filepath = cache_filename(word)
    cpath = resolve_path(string_filepath)
    if os.path.isfile(cpath):
        print( 'Deleting {}'.format(cpath))
        os.remove(cpath)
        return True

    print( 'Cannot Delete. Is not file "{}"'.format(cpath))
    return False


class LocalData(object):
    '''Collect local data easily.'''

    def __init__(self, path='./data'):
        '''Local Data connection with a given relative path


        Keyword Arguments:
            path {str} -- relative prefix of the data path (default: {'./data'})
        '''
        self.root = resolve_path(path)

    def get_list(self, name):
        '''Return a list from a file.

            >>> c = cache.LocalData()
            >>> l = c.get_list('top-words/3000.txt')
            >>> l[20]
            'account'
        '''
        filepath = os.path.join(self.root, name)

        res = []
        with open(filepath, 'r') as stream:
            for line in stream:
                res.append(line.strip())

        return res
