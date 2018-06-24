import traceback
import sys
import multiprocessing

from log import log
from conceptnet.parse import parse_csv, spread


def generate_negatives():
    """Relations can be prefixed with "Not" to express a negative assertion,
    such as `/r/NotIsA` `/c/en/mammal` `/c/en/plant`. The negative relations
    that we have data for are NotDesires, NotUsedFor, NotCapableOf, and
    NotHasProperty."""
    global map_tuple
    not_desc = '[Negative relation of]'
    res = ()
    for item in map_tuple:
        rel = item[0].replace('/r/', '/r/Not')
        desc = "{} {}".format(not_desc, item[1])
        ires = (rel, desc, ) + item[2:]

        res +=  (ires,)
    map_tuple += res

'''Tuple of tuples for the expected relation types. additional 'not'
statements generate and append upon module import
'''
map_tuple =(
    (
        "/r/RelatedTo",
        """The most general relation. There is some positive relationship
        between A and B, but ConceptNet can't determine what that relationship
        is based on the data. This was called "ConceptuallyRelatedTo" in
        ConceptNet 2 through 4. Symmetric. """,
        """learn <=> erudition""",
    ),
    (
        "/r/ExternalURL",
        """Points to a URL outside of ConceptNet, where further Linked Data
        about this term can be found. Similar to RDF's `seeAlso` relation. """,
        """knowledge => http://dbpedia.org/page/Knowledge""",
    ),
    (
        "/r/FormOf",
        """A is an inflected form of B; B is the root word of A. """,
        """slept => sleep""",
    ),
    (
        "/r/IsA",
        """A is a subtype or a specific instance of B; every A is a B. This
        can include specific instances; the distinction between subtypes and
        instances is often blurry in language. This is the *hyponym* relation
        in WordNet. """,
        """car => vehicle; Chicago => city""",
    ),
    (
        "/r/PartOf",
        """A is a part of B. This is the *part meronym* relation in WordNet. """,
        """gearshift => car""",
    ),
    (
        "/r/HasA",
        """B belongs to A, either as an inherent part or due to a social
        construct of possession. HasA is often the reverse of PartOf. """,
        """bird => wing; pen => ink""",
    ),
    (
        "/r/UsedFor",
        """A is used for B; the purpose of A is B. """,
        """bridge => cross water""",
    ),
    (
        "/r/CapableOf",
        """Something that A can typically do is B. """,
        """knife => cut""",
    ),
    (
        "/r/AtLocation",
        """A is a typical location for B, or A is the inherent location of B.
        Some instances of this would be considered meronyms in WordNet. """,
        """butter => refrigerator; Boston => Massachusetts""",
    ),
    (
        "/r/Causes",
        """A and B are events, and it is typical for A to cause B. """,
        """exercise => sweat""",
    ),
    (
        "/r/HasSubevent",
        """A and B are events, and B happens as a subevent of A. """,
        """eating => chewing""",
    ),
    (
        "/r/HasFirstSubevent",
        """A is an event that begins with subevent B. """,
        """sleep => close eyes""",
    ),
    (
        "/r/HasLastSubevent",
        """A is an event that concludes with subevent B. """,
        """cook => clean up kitchen""",
    ),
    (
        "/r/HasPrerequisite",
        """In order for A to happen, B needs to happen; B is a dependency of A. """,
        """dream => sleep""",
    ),
    (
        "/r/HasProperty",
        """A has B as a property; A can be described as B. """,
        """ice => cold""",
    ),
    (
        "/r/MotivatedByGoal",
        """Someone does A because they want result B; A is a step toward
        accomplishing the goal B. """,
        """compete => win""",
    ),
    (
        "/r/ObstructedBy",
        """A is a goal that can be prevented by B; B is an obstacle in the way of A. """,
        """sleep => noise""",
    ),
    (
        "/r/Desires",
        """A is a conscious entity that typically wants B. Many assertions of
        this type use the appropriate language's word for "person" as A. """,
        """person => love""",
    ),
    (
        "/r/CreatedBy",
        """B is a process or agent that creates A. """,
        """cake => bake""",
    ),
    (
        "/r/Synonym",
        """A and B have very similar meanings. They may be translations of each
        other in different languages. This is the *synonym* relation in WordNet
        as well. Symmetric. """,
        """sunlight <=> sunshine """,
    ),
    (
        "/r/Antonym",
        """A and B are opposites in some relevant way, such as being
        opposite ends of a scale, or fundamentally similar things with a key
        difference between them. Counterintuitively, two concepts must be quite
        similar before people consider them antonyms. This is the *antonym*
        relation in WordNet as well. Symmetric. """,
        """black <=> white; hot <=> cold""",
    ),
    (
        "/r/DerivedFrom",
        """A is a word or phrase that appears within B and contributes to B's
        meaning. """,
        """pocketbook => book""",
    ),
    (
        "/r/SymbolOf",
        """A symbolically represents B. """,
        """red => fervor""",
    ),
    (
        "/r/DefinedAs",
        """A and B overlap considerably in meaning, and B is a more
        explanatory version of A. """,
        """peace => absence of war""",
    ),
    (
        "/r/Entails",
        """If A is happening, B is also happening. (This may be merged with
        HasPrerequisite in a later version.) | run => move""",
    ),
    (
        "/r/MannerOf",
        """A is a specific way to do B. Similar to "IsA", but for verbs. """,
        """auction => sale""",
    ),
    (
        "/r/LocatedNear",
        """A and B are typically found near each other. Symmetric. """,
        """chair <=> table""",
    ),
    (
        "/r/HasContext",
        """A is a word used in the context of B, which could be a topic area,
        technical field, or regional dialect. """,
        """astern => ship; arvo => Australia""",
    ),
    (
        "/r/dbpedia",
        """Some relations have been provisionally imported from DBPedia, and
        don't correspond to any of the existing relations. For now, these are
        in the `/r/dbpedia/...` namespace, such as `/r/dbpedia/genre`. The
        DBPedia relations represented this way are `genre`, `influencedBy`,
        `knownFor`, `occupation`, `language`, `field`, `product`, `capital`,
        and `leader`.""",
    ),
)


### autocall the Negative relations
generate_negatives()




# + The URI of the whole edge
# + The relation expressed by the edge
# + The node at the start of the edge
# + The node at the end of the edge
# + A JSON structure of additional information about the edge, such as its weight
def get_relations(kw):
    '''Parse the given dictionary through parse_csv.
    returns a list of relations from the CSV

        path            path of the csv to parse
        cpu_count       allowed number of threads in spread mode
        byte_start      [auto] Byte chunk for the parse csv - autmatically applied
                        when spread() with job split.
        byte_end        [auto] Byte chunk for the parse csv - autmatically applied
                        when spread() with job split.
        sample          return a sample of each relation found.
        row_index       Which index within a given row to collect for the return
                        store value. This isposition indexed for the input CSV
                        (default 1)
        max_count       max lines per thread to iterate from the CSV provide None
                        to disable
    '''
    process_name = multiprocessing.current_process().name
    try:
        d, sample = parse_csv(
            max_count=kw.get('max_count', 100000),
            iter_line=get_value,
            as_set=True,
            row_index=kw.get('row_index', 1),
            keep_sample=kw.get('sample', False),
            byte_start=kw.get('byte_start', None),
            byte_end=kw.get('byte_end', None),
            )
        log('Finished relations. Count: {}. Writing file'.format(len(d)))
    except Exception as e:
        log('Error on "{}" :'.format(process_name), e)
        log(traceback.format_exc())
        d = []

    with open('relations-{}.txt'.format(process_name), 'w') as stream:
        for item in d:
            stream.write('{}\n'.format(item))

    return list(d)


def spread_get_relations(**kw):
    '''Similar to:

        from conceptnet import parse
        from conceptnet import relations
        parse.spread(relations.get_relations, max_count=1000)
    '''
    result = spread(get_relations, **kw)

    merged = set()
    for thread_result in result:
        for rel_list in thread_result:
            merged.add(rel_list)

    return filter(None, list(merged))


def get_value(line, **kw):
    '''return the sub value using row_index with the given tuple _line_ from
    the CSV'''
    index = kw.get('row_index', 0)
    v = None
    try:
        v = line[index]
    except Exception as e:
        log('get_value error', e)
    finally:
        return v
