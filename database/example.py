# from database.db import DB
# WRITE_ENV = "E:/conceptnet/_lmdb/"
# db = DB(WRITE_ENV)
# db.open(b'test')

# db.put(b'as', b'weqr')

# print(db.get('as'))

from database.db import AppendableDB
from database.db import *
# dd=AppendableDB(name='test')
# import pdb; pdb.set_trace()  # breakpoint f5263566 //
# dd.put('tuple', (1,2,3,4,5))

gb = GraphDB(name='graph')

key='Hello'
gb.add(key, 'isa', 'greeting', 3.4, 'hello')
gb.add(key, 'isa', 'word', 3, 'hello')
gb.add(key, 'isa', 'another', 1, 'hello')

r = list(gb.iter())
print(r)

p = gb.pick(key)
# gb.add('hey', 'synonym', 'hello', weight=2, root='hello')
# gb.add(start='hi', edge='synonym', end='hello', weight=2, root='hello')

# gb2 = AppendableDB(name='related')

# assoc = ('musta', 1,)
# assoc2 = ('greet', 1,)
# gb2.put('hello', (assoc, assoc2,) ) # weight=1

# # hello related [to] hello > ...
# gb.bind('hello', gb2)

# # returns live Graph
# r = gb.get('hello')
# # Doesn't need to be 'get()', but it's dict friendly.
# if r:
#     result = r.get('related')
#     expected = (
#                  ('musta', 1,),
#                  ('greet', 1,),
#                )
#     print(result == expected)

# """Associate another DB through a name bound
# to the key within the first db.
# """
# # Auto bind hello > related > 'hello'
# # from the DB name, and a like-for-like key name.
# gb.bind('hello', gb2)

# gb.bind(
#     # bind the name of the key within the original DB.
#     key='hello',
#     # the other db to bind to.
#     db=gb2,
#     # The key name to associate against the second db
#     through='more',
#     # The key for the given DB. Default is the given key
#     relation='hello'
#     )
