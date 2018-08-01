# Database

This part of the project has no name, as it's a custom no-sql db for storing graph and tables.

with LMDB as a platform for local storage.

## Use cases

I've made this for a number of personal tools. But it has enough dimentions to qualify for most casual cases.

+ Sentence Graphing for Sadie
+ Websockets Key Event Horizontal records
+ Distributed state machine storage

# Gettings Started

The absolute basics need no introduction. Using PROJECTNAME as an instant key value needs no setup:

    from database.db import DB

    db = DB(directory='./doc_test')

    // optional
    db.open('first')

    db.put('cake', 'cherry pie')
    True

     db.get('cake')
    'cherry pie'

    db.count()
    1


And that's it! Go ahead and store millions! If you don't supply a `db.open()` database, the library will use a defaulted name.

The entire library works with one handle so you don't need to worry about threads or transactions - it's done for you.


## AppendableDB

The basic key value database is useful for fast tests but pretty boring for functionality. an AppendableDB leverages the raw byte storage to allow updating a single key with _more_ of the same.


    adb = AppendableDB(directory='./doc_play')
    // again - optional.
    adb.open('first')

You'll see we've opened the same database as the first `db.DB` instance. They can both use the same data. We can check that by iterating **all the data**:

    adb.keys()
    list(adb.iter())
    [('cake', b'cherry pie'),]

Scary. Now we'll add a list of names. The `AppendableDB` class help with coversion of a `tuple`:

    adb.put('names', ('eric', 'dave', 'micheal', 'bob'))

    adb.append('names', ('simon',) )
    b"!:A1D!:'eric', 'dave', 'micheal', 'bob'"

When you `append` data, you're adding to an existing row. The appended data type is the same. In this case another `tuple`. The return from `append` was the previously stored value. This will not contain your update.

We can append as much as we want, `get()` a finished product when required:

    adb.append('names', ('simon', 'timmy') )
    adb.get('names')
    ('eric', 'dave', 'micheal', 'bob', 'simon', 'simon', 'timmy')


## Appendable Types and conversion

You can append to any builtin data type such as `list`, `tuple`, `str` or your own. PROJECTNAME doesn't care what you write as the raw data is stored in `bytes`.

You can turn off encoding for advanced routines. This is especially useful when you've broke a key:

    # Apply a 'str' type instead of a tuple.
    adb.append('names', 'another name')
    b"!:A1D!:'eric', 'dave', 'micheal', 'bob','simon','simon', 'timmy'"


Now it's broken; it can't be converted safely:

    adb.get('names')

    _convert_eval() render error: invalid syntax (<string>, line 1) _convert(A1D, 'eric', 'dave', 'micheal', 'bob','simon','simon', 'timmy',another name)
    # ...


Crumbs... Luckily it's only one key that can break.
Let's see the real DB value:

    adb.get('names', convert=False)
    b"!:A1D!:'eric', 'dave', 'micheal', 'bob','simon','simon', 'timmy',another name"


You can delete a value with old standard `.delete()`, or `.replace()`


```py
    from database.db import AppendableDB
    adb = AppendableDB(directory='./doc_test')
    adb.open('first')
    adb.keys()
    adb.get('names', convert=False)

    adb.replace('names', ('bob', 'eric',))

    adb.get('names', convert=False)
    b"!:A1D!:'bob', 'eric'"

    adb.get('names')
    ('bob', 'eric')
    adb.delete('names')
    True

    adb.get('names')
    None
```


Designed to work in any dimension, setting up the database for your personal case is key to how the methods work.

### Vertical Append

Similar to a standard table records apply in a linear order, therefore iteration through rows is possible. Applying a class map for return values can mimic ordered column rows:


```py
    Row = namedtuple('Row', 'a b c d e f')
    db.put(Row(1,2,3,4,5,6))

    for row in db:
        assert isinstance(row, Row)
```


### Horizonal Append

The key input allows an 'append' functionality to reduce the amount of throughput for a given procedure. This will allow the continued extension of basic python types without convertion. for example storing a `list` will allow `db.append('mylist_key', (23,23,45,))`. The same applies for all basic python types.

This example will record typing events per sentence into a single key, storing keystrokes for historical _undo_:

```py
    keystrokes = ('h', 'e', 'l', 'o', '[backspace]', 'l', 'o')
    db.put('my_page_3', keystrokes)
    db.append('my_page_3', ('w', 'o',) )
    db.append('my_page_3', ('r', 'l',) )
    db.append('my_page_3', ('d',) )

    ''.join.(db.get('my_page_3'))
    'helo[backspace]lo world'
```

## GraphDB

A graph database defines connections between _nodes_ (data values) and _edges_ (a connection to values). A node consists of something you'd like to store - such as an object `{ name: 'terry', age: 10}`. an edge connects this node to another, with a special label for the type of connection "terry > friends_with > micheal".
A graph contains lots of edges for each node. In turn they are connected to other nodes and so on.

The `GraphDB` applies a few extra methods through the use of a `GraphWalker`.


# test

    py -mpytest -sv database
    # with coverage:
    py -mpytest database -v --cov --cov-report=term-missing

