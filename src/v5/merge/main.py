import requests

from collections import namedtuple, defaultdict
import operator
from pprint import pprint as pp

# Connect to an endpoint for graph pulls.
# This one is the duplex endpoint.
import argparse

ENDPOINT = 'http://127.0.0.1:9005'
parser = argparse.ArgumentParser(description='Edge Weight Analysis')
parser.add_argument('-w', '--words', default=['hello'], nargs='+', help='input word')
args = parser.parse_args()


def main():

    for word in args.words:
        aa = perform_word_weights(word, others=args.words, step_edge_keys=['rev'])
        bb = perform_word_weights(word, others=args.words, step_edge_keys=['edges'])
        import pdb; pdb.set_trace()  # breakpoint 54b72926 //



def perform_word_weights(word, others=None, step_edge_keys=None):
    other = others or []
    upper, lower, dropped = perform(word=word,
                                    step_edge_keys=step_edge_keys,
                                    others=others,
                                    add_self=False)

    # Note "dropped" aren't ignored - they're just not forward edges...
    """
    Contains:
        + The (upper, lower) list of edges for the given word, split by threshold.
        + A first step (forward "edges") of each highest weighted edge.
            (of any word with connected len(edges) > 0)
        + dropped: a list of high weighted primary edges without any decendents
            this may be due to the child edges.weight < threshold.

    cross reference all primary edges, for a forward reference of the root word
    primary primary: Keep cross-referenced and populate the top 50% weighted (above threshold.)
    primary secondary: keep all (without a cross reference) 50% top weighted - for population later.
    lower: anything ignored through the top query

    Once done with the "upper" - perform with the lower.
    then the 'lower lower' in a background process.
    """
    print('Upper:')
    print_group(upper)
    print('---\nLower:')
    print_group(lower)
    print('---\nUpper Dropped:')
    print_group(dropped)

    ubias = cross_reference_first_layer(word, upper, dropped, others)
    lbias = cross_reference_first_layer(word, lower, dropped, others)
    tbias = merge_biases(ubias, lbias, word=word)
    print('lower bias:')
    pp(lbias)
    print('upper bias:')
    pp(ubias)
    print('total bias:')
    pp(tbias)
    biases = (lbias, ubias, tbias,)
    graphs = (upper, lower,)

    return graphs, biases, dropped


def cross_reference_first_layer(word, upper, dropped, others=None):
    """Given a range of grouped edges, return weighted preferences
    by distance through 'word'
    """
    upper_w = count_as_child(word, upper, others=others)
    ## lower_w = count_as_child(word, lower)
    # A reference of all edges (words) of which have a forward edge of the "word."
    # as a hint for a strong connection.
    # (Pdb) uw = {'chicken': 1, 'yolk': 1, ... }
    # (Pdb) lw = {'chicken': 1, ... 'chick': 1}
    #  Get additional weight
    drop_upper_bias = get_biases(dropped, upper, others=others)
    ## drop_lower_bias = get_biases(dropped, lower)
    pp(upper_w)
    pp(drop_upper_bias)
    print('---')
    # Get a list of weight bias
    # to use later during scanning.
    ubias = merge_biases(upper_w, drop_upper_bias, word=word)
    # do the same cross reference for
    # top bias children.
    # Distance calculation defines additional biases.
    return ubias


def merge_biases(*bias_dicts, word=None):
    """
    a bias defines some additional weight to compute
    an edge relation. get_bias returns a dict of counts for a
    given group against another group.

        {'polite/a': 1, 'wax': 1}

    Provide a 'word' for extra context.

        {'buff': 1, 'rub': 1, 'silver': 1}
        {'shine': {'wax': 1},
            'shiny': {'silver': 1}}
        {'buff': {'buff': 1},
         'cleaner': {'cleaner': 1},
         ...
         'shiny': {'clean': 1, 'shiny': 1, 'wax': 1},
         'warsaw': {'poland': 1, 'warsaw': 1}}
    """
    res = defaultdict(int)
    for bias_dict in bias_dicts:
        for word, content in bias_dict.items():
            if isinstance(content, dict):
                # The word is a dictionary,
                # therefore apply a reference weight
                # rather than 1 - a edge base weight
                res[word] += .5
                for key, val in content.items():
                    res[key] += val
            else:
                # standard int
                res[word] += content
    return dict(res)


def get_biases(edge_group, goal_edge_group, others=None):
    # do the same with drops.
    # then also use each drop as a parent word
    # applying as a weighted top for upper and lower.
    dropped_w_u = {}
    for edge, edges in edge_group.values():
        uweights = count_as_child(edge.word, goal_edge_group, others=others)
        if len(uweights) > 0:
            dropped_w_u[edge.word] = uweights

    # {'embryo': {'seed': 1}, 'lays': {'chicken': 1}}
    return dropped_w_u


def find_shared_edges(edge_list_a, edge_list_b):
    """

    + Find any words found within the edges of two graphs.
    + Finding the bridge or "connecting" edge for two lists.
    + given two word lists, find matching word edges

    return the connect words and the assicated edges.

    This is useful for connecting two graphs with an edge word

        alpha       beta
          cake        muffin
          egg         break
          milk        egg
          cheese      cheese

        return egg, cheese
    """


def count_as_child(word, edges_group, weights=None, others=None):
    """Count instances of `word` within the edge list of each key
    within the edges_group.

        word: 'egg'
        edges_group: {
            chicken: [yolk, other, egg]
        }

    return dictionary of counts
        { chicken: 1 }
    """
    weights = weights or defaultdict(int)
    # find primary references
    ## look through upper for first reference of word.
    for primary_edge, primary_edges in edges_group.values():
        pw = primary_edge.word
        #print('Word', pw)
        if word == pw:
            # do nothing with a self reference.
            weights[word] = 1
            continue

        primary_edges = sort_edges(primary_edges)
        for edge in primary_edges:
            #print(f'  {edge.word}')
            if edge.word == word:
                # An edge of the edge (of the root word)
                # matches the root word.
                weights[pw] += 1
                continue

            if edge.word in others:
                # Given additional bias.
                weights[pw] += 1
    return dict(weights)


def sort_edges(edges, key='weight', decending=False):
    name = 'itemgetter'
    if isinstance(key, str):
        name = 'attrgetter'
    getter = getattr(operator, name)(key)
    return sorted(edges, key=getter, reverse=not decending)


def perform(word, edge_keys=None, step_edge_keys=None, add_self=False, others=None, threshold=1):
    # Read edges, anaylse topolgies, brdge and call more words
    print('Analyse word', word)
    group_upper = {}
    group_lower = {}

    upper, lower = get_word_split_edges(word, edge_keys)
    if add_self:
        # Append the existing word to the work stacks.
        group_upper[word] = (None, upper)
        group_lower[word] = (None, lower)

    # populate all relations for each primary edge.
    # But onky the forward policy.
    step_edge_keys = step_edge_keys or ['edges']
    upper_forward_groups = get_edges_words(upper, edge_keys=step_edge_keys) # not rev
    gu, gl, dropped = remove_edgeless(upper_forward_groups, group_upper, group_lower, threshold=threshold)

    return gu, gl, dropped


def remove_edgeless(groups, upper=None, lower=None, threshold=1):
    group_upper = upper or {}
    group_lower = lower or {}
    dropped = {}

    for key_word, (edge, (upper, lower,), ) in groups.items():
        """
        Upper:
          cook                 2.0    (39) - measure_flour, prepare_meal, ...
          measure_flour        4.899  (0)  - ...
          prepare_meal         4.899  (0)  - ...
        """
        #key = key_word# f"{word}-{key_word}"
        # remove any group without an edge list
        if len(upper) > 0:
            group_upper[key_word] = (edge, upper, )
        else:
            if edge.weight > threshold:
                # Although highly weighted, the given edge yeilds no forward
                #  edges...
                dropped[key_word] = (edge, lower,)

        if len(lower) > 0:
            group_lower[key_word] = (edge, lower, )

    return group_upper, group_lower, dropped


def print_group(gu):
    _max = 8
    key = 'word'
    edge_val ='weight'
    le = 'len'
    el = 'items'
    ext = ''
    rel = 'relation'

    s = f"  {rel:<12} {key:<20} {edge_val:<6} {le:<5} {el}{ext}"
    print(s)
    print('-' * len(s))
    for key, (edge, edges,) in gu.items():
        el = ", ".join([x.word for x in edges[0:_max]])
        # edge_val is none if the given item entry was the root word.
        # therefore has no edge.
        edge_val = '-' if edge is None else edge.weight
        le = f"{len(edges)}"
        rel = '-' if edge is None else edge.rel
        ext = ' ...' if len(edges) > _max else ''
        s = f"  {rel:<12} {key:<20} {edge_val:<6} {le:<5} {el}{ext}"
        print(s)


def print_edges(edges):
    for edge in edges:
        le = len(edge)
        s = f"  {edge.rel:<12} {edge.word:<20} {edge.weight:<6} {le:<5}"
        print(s)


def get_word_split_edges(word, edge_keys=None):
    data = get_word(word)
    # produce flat, sort by weight.
    # (upper, lower)
    return split_multi_edges(data, edge_keys=edge_keys)


def get_edges_words(edges, edge_keys=None):
    """ read the given edges iterable and call each word
    """
    result = {}
    for edge in edges:
        result[edge.word] = (edge, get_word_split_edges(edge.word, edge_keys=edge_keys))
    return result


def split_multi_edges(data, threshold=1, edge_keys=None):
    """split the json raw data into an upper and lower edges stack

        'edges': [
            ['IsA', 'greeting', 3.464],
            ...
            ['EtymologicallyRelatedTo', 'hollo', 0.25]
        ],
        'key': 'hello',
        'limit': 0,
        'rev': [
            ['RelatedTo', 'rehi', 2.0],
            ...
        ],
        'word': 'hello'
    """
    # Applicable iterables.
    edge_keys = edge_keys or ['edges', 'rev']
    _upper = []
    _lower = []
    for ek in edge_keys:
        # produce a higher and lower range.
        e_upper, e_lower = split_edges(data[ek], ek, threshold=1)
        _upper.extend(e_upper)
        _lower.extend(e_lower)
    return _upper, _lower


Edge = namedtuple('Edge', ["type", "rel", "word", "weight"])

def split_edges(edges, key_type, threshold=1):
    # Split the stack based upon a simple threshold.
    _upper = []
    _lower = []
    for edge_line in edges:
        _edge = Edge(key_type, *edge_line)
        #print(f"edge {_edge.word}, {_edge.weight}")
        stack = _lower if _edge.weight <= threshold else _upper
        stack.append(_edge, )
    return sort_edges(_upper), sort_edges(_lower)


def get_word(word, limit=0):
    p = f'word/{word}/{limit}'
    edge_d = get_request(p)
    return edge_d


request_cache = {}

def get_request(url, use_cache=True):
    # perform and merge the request for all resources
    if (url in request_cache) and use_cache is True:
        return request_cache[url]

    path = f"{ENDPOINT}/{url}"
    print('Fetch', path)
    res = requests.get(path)
    if res.ok:
        res = res.json()
        request_cache[url] = res
        return res

    print('Error with', path, res)
    return res


if __name__ == '__main__':
    main()
