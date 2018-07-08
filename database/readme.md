# Database

This part of the project has no name, as it's a custom no-sql db for storing graph and tables.

with LMDB as a platform for local storage.

## Use cases

I've made this for a number of personal tools. But it has enough dimentions to qualify for most casual cases.

+ Sentence Graphing for Sadie
+ Websockets Key Event Horizontal records
+ Distributed state machine storage


### Vertical Append

Similar to a standard table records apply in a linear order, therefore iteration through rows is possible. Applying a class map for return values can mimic ordered column rows:

    Row = namedtuple('Row', 'a b c d e f')
    db.put(Row(1,2,3,4,5,6))

    for row in db:
        assert isinstance(row, Row)

### Horizonal Append

The key input allows an 'append' functionality to reduce the amount of throughput for a given procedure. This will allow the continued extension of basic python types without convertion. for example storing a `list` will allow `db.append('mylist_key', (23,23,45,))`. The same applies for all basic python types.

A personal usecase will record typing events per sentence into a single key, storing keystrokes for historical _undo_:

    keystrokes = ('h', 'e', 'l', 'o', '[backspace]', 'l', 'o')
    db.put('my_page_3', keystrokes)
    db.append('my_page_3', ('w', 'o',) )
    db.append('my_page_3', ('r', 'l',) )
    db.append('my_page_3', ('d',) )

    ''.join.(db.get('my_page_3'))
    'helo[backspace]lo world'



# test

    py -mpytest -sv database
    # with coverage:
    py -mpytest database -v --cov --cov-report=term-missing

