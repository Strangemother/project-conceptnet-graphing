# from database.db import DB
# WRITE_ENV = "E:/conceptnet/_lmdb/"
# db = DB(WRITE_ENV)
# db.open(b'test')

# db.put(b'as', b'weqr')

# print(db.get('as'))

from database.db import AppendableDB
from database.db import *
from database.graph import GraphDB, ObjectDB
# dd=AppendableDB(name='test')
# import pdb; pdb.set_trace()  # breakpoint f5263566 //
# dd.put('tuple', (1,2,3,4,5))

gb = ObjectDB(name='graph_pick')
gb.wipe()
key='Hello'
gb.add(key, 'isa', 'greeting', 3.4, 'hello')
gb.add(key, 'isa', 'word', 3, 'hello')
gb.add(key, 'isa', 'another', 1, 'hello')

gb.add('greeting', 'similarto', 'Hello', 2)
gb.add('greeting', 'similarto', 'hi', 2)
gb.add('greeting', 'isa', 'welcome', 2)
gb.add('hi', 'isa', 'greeting', 3)
gb.add('word', 'isa', 'word', 1)
gb.add('word', 'isa', 'thing', 1)
gb.add('thing', 'etomology', 'law', 2)

r = list(gb.iter())
print(r)

p = gb.pick(key)
p.isa.greeting.similarto.Hello.graph.isa.greeting.value == 'greeting'
p_end = p.isa.greeting.similarto.Hello.isa.word

walk_up = ( p_end
    # hello
    .parent_graph
    # greeting
    .parent_graph
    # Hello
    .parent_graph
    # DB
    .parent_graph )


law_chain =( p
    .isa
        .greeting
    .similarto
        .hi
    .isa
        .greeting
    .similarto
        .Hello
    .isa
        .word
    .isa
        .thing
    .etomology
        .law)
    # .chain()
from pprint import pprint as pp

a = zip(
    law_chain.edgenode_chain(True),
    law_chain.graph_chain(True)
    )
chain=list(a)
chain.reverse()
result = ()
for edge, graph in chain:

    if edge.parent_edgenode is not None:
        nv = edge.parent_edgenode.value
    else:
        nv = edge.parent_graph.key

    result +=( ( nv, edge.edge_type, graph.key, edge.weight),)

expected = (
     ('Hello', 'isa', 'greeting', 3.4),
     ('greeting', 'similarto', 'hi', 2),
     ('hi', 'isa', 'greeting', 3),
     ('greeting', 'similarto', 'Hello', 2),
     ('Hello', 'isa', 'word', 3),
     ('word', 'isa', 'thing', 1),
     ('thing', 'etomology', 'thing', 2)
 )
pp(result)

print('test', gb.create_index(gb._data))
# {'Hello': (1, 1, 1), 'greeting': (2, 2, 2), 'hi': (3,), 'word': (4, 4), 'thing': (5,)}
print('real', gb.index)

# (   <Graph "thing" 1 edges of ('etomology',)>,
#     <Graph "word" 2 edges of ('isa',)>,
#     <Graph "Hello" 3 edges of ('isa',)>,
#     <Graph "greeting" 3 edges of ('isa', 'similarto')>,
#     <Graph "hi" 1 edges of ('isa',)>,
#     <Graph "greeting" 3 edges of ('isa', 'similarto')>,
#     <Graph "Hello" 3 edges of ('isa',)>
# )

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
