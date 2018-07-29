"""My little boot script."""

from database.graph import *
import database
from database.db import *

from conceptnet import scratch_db
from v4.bridge import get_siblings as get
from v4.wordnet import get_word, NOUN, VERB, ADJ, ALL

ASSERTIONS_DIR = "E:/conceptnet/_lmdb_assertions/"
SERVER_ASSERTIONS_DIR = "E:/conceptnet/_lmdb_server_ui/"
csv_path = 'E:\\conceptnet\\assertions.csv'

GB_9 = 9e+9



assertions_db = GraphDB(write=False, directory=ASSERTIONS_DIR, name='assertions')
db = GraphDB(directory=SERVER_ASSERTIONS_DIR, name='server')

"""The Edge instance as a handle is a simple wrapper for calling
pick() from the graph. Any calls to edge are piped to the graph_db.

    db.pick('apples')
    # to
    handle.apples
"""
# handle.my.related_to.belonging.weight
# handle = Edge(db)
# # sorted(handle.my.related_to, reverse=True)[0]

# a = EdgeNode('top', 1)
# b = EdgeNode('toy', 2)
# c = EdgeNode('other', 1)
# edges = Edges(items=(a,b,))


# db.open('test')
# # db.put('banana', False)
# # banana_res = db.get('banana')

# expected = (False, False, True, True)
# db.put('choice', expected)
# result = db.get('choice')
# print(result, type(result))

# e=Edge(assertions_db)
# hi = e.hi
# he = e.hello

# edge = hi.get_edges('greeting')
# res = he & hi
get_word('egg', kws=ALL, to_file='foo1.txt')

# >>> res
# <ChildGraph "hello [&] hi" 2 edges of: (is_a, related_to)>
# >>> res.edges
# {'IsA': <Edges 1 "IsA" ('greeting(3.464) from "hello [&] hi"',)>,
# 'RelatedTo': <Edges 1 "RelatedTo" ('greeting(1.0) from "hello [&] hi"',)>}

# produce a function to flip the associations.
# Relating a word from the child graph 'greeting' to its
# edge type and associated (sum) weight value.
#
# res.flipped_edged:
#   { greeting: ((isa, 3.4), (relatedto, 1))}

# ! the edgenode given to the childgraph looses its main parent.
# This is because the __and__ generates a parent=self tothe child
# Which is collected by the Grow 'child.values' and edge_list()
# spawn.
# >>> res.is_a.greeting.parent_graph
# <ChildGraph "hello [&] hi" 2 edges of: (is_a, related_to)>
# Which should be:
#  he.is_a.greeting.parent_graph
# <Graph "hello" 26 edges of: (a...)>
# because this edge originaled from the 'Hello' graph.
def main():
    pass

if __name__ == '__main__':
    main()
