import os
import nltk

from typemap import type_map
import contextnet_api as cnapi
from logger import print_edges
import words

from cache import set_cache, string_cache, set_global_root
import cache

import secondary_functions
import cache
import loop
from json_socket import make_socket, send_json


ident_dict = {}
socket = None


def init(socket_uri="ws://127.0.0.1:8009"):
    '''
    A initialisztion function for anything requiring a first boot.
    '''

    global socket
    if socket_uri is not None:
        print 'Making secondary_functions socket'
        socket = make_socket(socket_uri)


def apply_to_context(sentence):
    '''given data from the token assess, build clean data for the context
    engine, populating with missing data as required.
    '''

    # success, v = get_cache(filepath)
    thin_structure_words = tokenize_assess_string(sentence, allow_fetch=True)
    # Send to the data cleaner for the next stage of cross referencing.
    updated_words = populate_sub_words(thin_structure_words)

    words = thin_structure_words

    print words.keys()
    print 'tree',  thin_structure_words['tree']
    send_json({ "sentence": sentence })
    res = tuple()

    if 'words' in words:

        for wordset in words['words']:
            word, wtype, ident, dict_ref = wordset
            print "looking at - ", word, wtype
            '''
                (Pdb) pp(ident['meta'][0:2])
                [{'end': {u'@id': u'/c/en/fruit',
                          u'label': u'fruit',
                          u'language': u'en',
                          u'term': u'/c/en/fruit'},
                  'id': u'/a/[/r/RelatedTo/,/c/en/apple/,/c/en/fruit/]',
                  'rel': {u'@id': u'/r/RelatedTo', u'label': u'RelatedTo'},
                  'start': {u'@id': u'/c/en/apple',
                            u'label': u'apple',
                            u'language': u'en',
                            u'term': u'/c/en/apple'},
                  'surfaceText': u'[[apple]] is related to [[fruit]]',
                  'weight': 12.80968383684781},

                 {'end': {u'@id': u'/c/en/red',
                          u'label': u'red',
                          u'language': u'en',
                          u'term': u'/c/en/red'},
                  'id': u'/a/[/r/HasProperty/,/c/en/apple/,/c/en/red/]',
                  'rel': {u'@id': u'/r/HasProperty', u'label': u'HasProperty'},
                  'start': {u'@id': u'/c/en/apple',
                            u'label': u'apple',
                            u'language': u'en',
                            u'term': u'/c/en/apple'},
                  'surfaceText': u'[[apple]] can be [[red]]',
                  'weight': 9.591663046625438}]
            '''
            word_def = clean_for_context(wordset, ident.get('meta', []))
            res += (word_def,)
    else:
        print 'no word information'

    print 'Have {} words'.format(res)
    return res



class Word(object):

    def __init__(self, word, tag_type):
        self.word = word
        self.tag_type = tag_type
        self.relatives = {}
        self._relations = []
        self.meaning = None
        self.antonyms = None
        self.synonyms = None

    def add_relative(self, word, word_type, weight=1, sentence=None, language=None):
        '''Associate a word with this word in relation to the given type'''
        _type = word_type
        self._relations.append({
            'word': word,
            'type': _type,
            'sentence': sentence,
            'weight': weight,
            'language':language,
            })

    def add_relative_type(self, _type):
        if self.relatives.get(_type, None) is None:
            self.relatives[_type] = []

    def __repr__(self):
        s = '<Word("{}" {}) rel: {}~{}>'.format(
            self.word,
            self.tag_type,
            len(self.relatives),
            len(self._relations),
            )
        return s


def clean_for_context(wordset, relations):
    '''Given the entire dataset for a word, generate and return a cleaner API
    word for use within the API
    '''
    langs = ['en']
    ignore = [u'ExternalURL']
    word, wtype, ident, dict_ref = wordset
    wc = Word(word, tag_type=wtype)

    wc.meaning = dict_ref.get('meaning', None)
    wc.antonyms = dict_ref.get('antonym', [])
    wc.synonyms = dict_ref.get('synonym', [])

    if relations is None:
        print 'No relations for {}'.format(wc)
        return wc

    for edge in relations:
        if edge['rel']['label'] in ignore:
            print 'skipping external url relation'
            continue

        try:
            endlang = edge['end']['language']
        except KeyError as e:
            print 'Language key missing'
            print edge
            continue

        # Add the type of edge as a future relationship type.
        wc.add_relative_type(edge['rel']['label'])

        wc.add_relative(
            word=edge['end'],
            word_type=edge['rel']['label'],
            weight=edge['weight'],
            sentence=edge['surfaceText'],
            language=edge['end']['language'],
        )

    return wc



def populate_sub_words(thin_structure_words, allow_fetch=True):
    '''A parent string has been tokenized and filled with the raw
    cache data of the words. Populate the same for any
    sub words, attached synonyms and antonyms
    '''
    words = thin_structure_words
    print 'tree',  thin_structure_words['tree']
    result = []

    if 'words' in words:

        for wordset in words['words']:
            word, wtype, ident, dict_ref = wordset
            # populate similar
            subl = dict_ref['synonym']
            if subl is None:
                continue
            print 'digressing synonyms of', word, len(subl)
            for sub_word in subl:
                print "looking at - ", sub_word
                value = tokenize_assess_string(sub_word.lower(), allow_fetch=allow_fetch)
                result.append({ 'value': sub_word, 'meta': value })
    else:
        print 'no word information'

    return result


def populate_sub_words_recursive(thin_structure_words, depth=6, _current_depth=0, root_value=None):
    print 'populate sub words recursive {}/{}'.format(_current_depth, depth)
    words = populate_sub_words(thin_structure_words, allow_fetch=False)
    if _current_depth >= depth:
        print 'kill depth'
        return words

    for word_result in words:
        if 'words' in word_result['meta']:
            print 'recursive inspection of', len(word_result['meta'])
            _words = populate_sub_words_recursive(
                word_result['meta'],
                depth=depth,
                _current_depth=_current_depth+1,
                root_value=root_value,
                )
            words.extend(_words)

    return words


def ident_object(word, wtype, tokens):
    return dict()


def tokenize_assess_string(sentence, allow_fetch=True):
     # success, v = get_cache(filepath)
    v = cache.get_string_cache(sentence)

    if v is None:
        v = tokenize(sentence)
        cache.set_string_cache(sentence, v)

    return assess_tokens(v, allow_fetch=allow_fetch)


def iter_print(g):
    print '\n'
    for word, typeof in g:
        print "{:<20} {:<4} {}".format(word, typeof, type_map.get(typeof, '[NO TYPE]'))
    return g


def tokenize(s):
    '''
    Tokenize the given string sentence consisting of words split by spaces.
    Returned is a is of tokenized words
    '''
    print 'tokenizing input...', type(s)

    send_json(type='tokenize', input=s, action='start')

    t = nltk.word_tokenize(s)
    g = nltk.pos_tag(t)
    send_json(type='tokenize', input=s, result=g, action='complete')
    return g


def assess_tokens(tokens, allow_fetch=True):
    '''
    Read and analyze a list of tokens. For each discovered work, entire
    word assertions exist.
    returns a tuple of tokens with a word ident object.
    '''
    print 'Assessing:'

    send_json(type='assess', action='start', tokens=tokens)
    tree = nltk.chunk.ne_chunk(tokens)

    res = []
    for word, typeof in tokens:
        item = (word, typeof, type_map.get(typeof, '[NO TYPE]'), )
        res.append(item)

    send_json(type='assess', action='complete', result=res, tokens=tokens)
    iter_print(tokens)

    res = ()

    for word, wtype in tokens:
        # thin_structure_words['words'][3] == tokens
        ident = assess_word_token(word, wtype, tokens, allow_fetch=allow_fetch)
        wdd = words.get_word(word)
        res = res + ( (word, wtype, ident, wdd), )
        send_json(
            type='assess',
            action='word',
            word=wdd,
            word_type=wtype,
            tokens=tokens,
            ident=ident,
            )
        # print_edges(ident)

    return dict(tree=tree, words=res)


def assess_word_token(word, wtype, tokens, allow_fetch=True):
    '''
    Given a Word "cake", its type "NN" and associated sentence tokens, "I like cake"
    identify the word store a cache of identification into the ident_dict.

    returned is the word entry to the ident_dict; an object of 'idents', 'words'
    and 'wtypes'
    '''
    ident = "{}_{}".format(word, wtype)

    # if ident_dict.get(ident, None) is None:
    #     # add to flat
    #     ident_dict[ident] = ident_object(word, wtype, tokens)

    if ident_dict.get(word, None) is None:
        # add to flat
        ident_dict[word] = ident_parent_object(word, wtype, ident, tokens, allow_fetch=allow_fetch)

    ident_dict[word]['idents'].add(ident)
    ident_dict[word]['words'].add(word)
    ident_dict[word]['wtypes'].add(wtype)

    return ident_dict[word]


def ident_parent_object(word, wtype, ident, tokens, allow_fetch=True):
    '''
    Create a single word entry to the identity context, associating any
    _wtype additions

    word:   Literal word given for input: i.e. "cake"
    wtype:  Token type from nltk Penn Treebank tagging: "NN"
    ident:  Literal word token assignment identity: "Cake_NN"
    tokens: Assosciated sentence tokens.

    The meta data within the result will call the to the context API.
    '''
    res = dict(words=set(), wtypes=set(), idents=set())
    res['meta'] = cnapi.api_result(word.lower(), allow_fetch=allow_fetch)
    #    {'end': {u'@id': u'/c/en/greeting',
    #         u'label': u'greeting',
    #         u'language': u'en',
    #         u'term': u'/c/en/greeting'},
    # 'id': u'/a/[/r/IsA/,/c/en/hello/,/c/en/greeting/]',
    # 'rel': {u'@id': u'/r/IsA', u'label': u'IsA'},
    # 'start': {u'@id': u'/c/en/hello',
    #           u'label': u'Hello',
    #           u'language': u'en',
    #           u'term': u'/c/en/hello'},
    # 'surfaceText': u'[[Hello]] is a kind of [[greeting]]',
    # 'weight': 4.47213595499958}
    return res;

