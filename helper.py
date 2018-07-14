"""My little boot script."""

from database.graph import GraphDB, Edge
import database

from conceptnet import scratch_db

ASSERTIONS_DIR = "E:/conceptnet/_lmdb_assertions/"
csv_path = 'E:\\conceptnet\\assertions.csv'

GB_9 = 9e+9



db = GraphDB( directory=ASSERTIONS_DIR, name='assertions')

"""The Edge instance as a handle is a simple wrapper for calling
pick() from the graph. Any calls to edge are piped to the graph_db.

    db.pick('apples')
    # to
    handle.apples
"""
handle = Edge(db)

def main():
    pass

if __name__ == '__main__':
    main()
