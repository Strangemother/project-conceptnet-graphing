'''Collect the relations from the CSV.
'''
from conceptnet import parse as P
from conceptnet import relations

P.spread(relations.get_relations, max_count=1000)
P.get_relations(dict(path=P.csv_path, max_count=1000000))

[   ['/r/DerivedFrom', '/r/Causes', '/r/Entails', '/r/CausesDesire',
     '/r/EtymologicallyRelatedTo', '/r/CapableOf', '/r/Antonym',
     '/r/DistinctFrom', '/r/AtLocation', '/r/CreatedBy', '/r/Desires',
     '/r/DefinedAs'],
    ['/r/ExternalURL', None],
    ['/r/ExternalURL', None],
    ['/r/FormOf', '/r/ExternalURL', None],
    ['/r/PartOf', '/r/InstanceOf', '/r/ObstructedBy', '/r/MadeOf',
     '/r/LocatedNear', None, '/r/NotDesires', '/r/MannerOf', '/r/HasSubevent',
     '/r/NotCapableOf', '/r/HasLastSubevent', '/r/HasProperty',
     '/r/ReceivesAction', '/r/HasPrerequisite', '/r/MotivatedByGoal',
     '/r/RelatedTo', '/r/NotUsedFor', '/r/HasContext', '/r/IsA',
     '/r/NotHasProperty', '/r/HasFirstSubevent'],
    ['/r/RelatedTo', None],
    ['/r/RelatedTo', None],
    ['/r/Synonym', None]
]

relations.spread_get_relations(max_count=60000)
expected = ['/r/ExternalURL', '/r/HasLastSubevent', '/r/Antonym', '/r/HasPrerequisite',
'/r/RelatedTo', '/r/HasContext',
'/r/Synonym', '/r/HasFirstSubevent']


from conceptnet import dbstore
dbstore.spread_redis_apply(max_count=100, max_cpu=1)


# populate the database with the given [builtin] csv
from conceptnet import sqlite_db
db = sqlite_db.fill_word_db(dict(max_count=None, byte_end=1000000))


from conceptnet import sqlite_db
from conceptnet import parse
jobs = parse.job_split(path=parse.csv_path)
job = jobs[6]
job.update(dict(max_count=None))
db, res = sqlite_db.fill_word_db(job)

db, res = sqlite_db.fill_word_db(jobs[3])
db, res = sqlite_db.fill_word_db(jobs[3])
db, res = sqlite_db.fill_word_db(jobs[4])


# Use one statement with a handler
from conceptnet import sqlite_db
x = 'C:/Users/jay/Documents/projects/context-api/context/src/cache/sqlites/sql-proc-0.db'
db, c = sqlite_db.open_db(x)
s = 'SELECT * FROM word WHERE start_word = "cat"'
sh = sqlite_db.StatementHandler(db, c)
sh.call(('select', s,))
sh.stmt_select(s)


from conceptnet import sqlite_db
db = sqlite_db.spread_db()
db.get_word('cake')

db.fetch('SELECT * FROM word WHERE start_word = ? ', ('cat', ))
db.fetch('SELECT * FROM word WHERE start_word = "cat"')

from conceptnet import sqlite_db
from conceptnet.parse import spread
db = spread(sqlite_db.fill_word_db, **{})

db = sqlite_db.spread_db()
db.add_line('dog', 'legs', 'has', 1, {})

db._promise._value
