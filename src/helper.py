"""My little boot script."""

from database.graph import *
import database
from database.db import *

from conceptnet import scratch_db

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
handle = Edge(db)
# sorted(handle.my.related_to, reverse=True)[0]

a = EdgeNode('top', 1)
b = EdgeNode('toy', 2)
c = EdgeNode('other', 1)
edges = Edges(items=(a,b,))


db.open('test')
# db.put('banana', False)
# banana_res = db.get('banana')

expected = (False, False, True, True)
db.put('choice', expected)
result = db.get('choice')
print(result, type(result))


def main():
    pass

if __name__ == '__main__':
    main()
