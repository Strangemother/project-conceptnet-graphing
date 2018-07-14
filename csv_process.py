"""Using the recorded CSV assertions, load through 'conceptnet'
parsing tools into the graph 'database'
"""
from database.graph import GraphDB
import database

from conceptnet import scratch_db

ASSERTIONS_DIR = "E:/conceptnet/_lmdb_assertions/"
csv_path = 'E:\\conceptnet\\assertions.csv'

GB_9 = 9e+9



db = GraphDB(
    directory=ASSERTIONS_DIR,
    name='assertions',
    max_bytes=GB_9,
    )


def main():
    # db.wipe()
    store()


def store():
    kw = dict(
        path=csv_path,
        step_function=step_function,
        chunk_size=1000,
        start_index=0,
        max_count=1_000_000_000,
    )

    scratch_db.store_lines(kw)


def step_function(items, line, given_kwargs):

    dd = given_kwargs['current_lineno']
    # print('{} {}'.format(items[-1]['start']['word'], dd))

    c = 0

    for item in items:
        start = item['start']['word']
        edge = item['connection']
        end = item['end']['word']
        weight = item.get('weight', 1)

        c+=1
        db.add(
            start=start,
            edge=edge,
            end=end,
            weight=weight,
            save=False,
        )
    print('At', dd + c)
    db.commit()



if __name__ == '__main__':
    #main()
    pass
