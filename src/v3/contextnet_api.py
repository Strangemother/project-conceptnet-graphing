import requests
import os, io
import json
import csv
from collections import namedtuple
import traceback

import cache

FETCH_ALLOWED = False

endpoints = ["http://api.conceptnet.io/c/en/",
            "http://conceptnet5.media.mit.edu/c/en/",
            "http://csc.media.mit.edu/c/en/",]
e_counter = 0

def bump_endpoint():
    global e_counter
    e_counter += 1
    if e_counter > len(endpoints) + 1:
        e_counter = 0


def api_fetch(word=None, depth=0, path=None, result_object=None, root_word=None, allow_cache=True, allow_fetch=True, _force_allow=False, limit=50):
    '''
    Fetch the work context from the external API. Returning an object
    '''
    fetch = True
    data = None
    root_word = root_word or word
    print( '.. Root word', root_word)
    filepath = None
    can_fetch = FETCH_ALLOWED
    endpoint = endpoints[e_counter]

    if _force_allow is True:
        print( 'Force override fetch from external')
        can_fetch = True
        allow_fetch = True

    if word is not None:
        fn = 'api_cache_{}.json'.format(word.replace(' ', '_'))
        filepath = cache.resolve_path(fn)
        if allow_cache is True:
            if os.path.isfile(filepath):
                print( 'opening api cache file')
                with io.open(filepath) as stream:
                    content = stream.read()
                    if len(content) > 0:
                        data = json.loads(content)
                        fetch = False

    if fetch is True:
        if can_fetch is False or allow_fetch is False:
            print( 'Fetching not allowed')
        else:
            print( 'Fetching: ', word or path)
            if word is None:
                uri = '{}{}'.format(endpoint, path)

            uri = '{}{}'.format(endpoint, word)
            if path and path.startswith('/'):
                uri = '{}{}'.format(endpoint, os.path.split(path)[1])



            try:
                data = requests.get(uri, params=dict(limit=limit)).json()
            except Exception as e:
                traceback.print_exc()
                bump_endpoint()
                try:
                    data = requests.get(uri, params=dict(limit=limit)).json()
                except Exception as e:
                    print( 'Error fetching context', e)
                    return None

            if 'error' in data:
                print( data['error']['details'])
                return None

            next_path = data.get('view', {}).get('nextPage', None)

            if next_path is not None and depth < 5 and depth != -1:
                print( 'Paging', root_word, depth)
                api_fetch(
                    path=next_path,
                    depth=depth+1,
                    result_object=result_object or data,
                    root_word=root_word,
                    _force_allow=_force_allow,
                    limit=limit,
                    )

            if filepath is None:
                filepath = 'api_cache_{}_{}.json'.format(root_word, depth)

            print( 'writing api cache:', filepath)
            cache.write_json(filepath, data)


    if result_object is not None:
        key = 'index_{}'.format(depth)
        result_object[key] = data
        result_object['index_length'] = max(result_object.get('index_length', -1), depth)
    return data


def api_clean(data):
    '''
    Given an API result, return a clean set of edges
    '''
    result = []

    for edge in data['edges']:
        item = clean_edge(edge)
        result.append(item)

    for index in range(data.get('index_length', 0)):
        key = 'index_{}'.format(index+1)
        sub_data = data[key]
        for edge in sub_data['edges']:
            item = clean_edge(edge)
            result.append(item)

    return result


def clean_edge(edge):

    return dict(
        id=edge['@id'],
        start=edge['start'],
        end=edge['end'],
        rel=edge['rel'],
        weight=edge['weight'],
        surfaceText=edge['surfaceText'],
        )


def api_result(*a, **kw):
    data = api_fetch(*a, **kw)
    if data is None:
        return None
    return api_clean(data)


Line = namedtuple('Line', ['uri', 'relation', 'start', 'end', 'json'])


def read_assertions():
    '''
    + The URI of the whole edge
    + The relation expressed by the edge
    + The node at the start of the edge
    + The node at the end of the edge
    + A JSON structure of additional information about the edge, such as its weight
    '''
    reader = IterCSV(filepath='F:/assertions.csv')
    for line in iter(reader):
        print( line)
    return reader


class IterCSV(object):

    def __init__(self, stream=None, filepath=None):
        if stream is not None:
            self.set_stream(stream)

        if filepath is not None:
            self.set_stream(open(filepath, 'rb'))


    def set_stream(self, stream):
        self.stream = stream
        self.csv = csv.reader(stream, delimiter='\t')

    def next(self):
        return Line(*self.csv.next())

    def __iter__(self):
        return self.next
