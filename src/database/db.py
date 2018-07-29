import lmdb
import os


WRITE_ENV = "E:/conceptnet/_lmdb/"
DEFAULT_DB_NAME = 'default_db'


UTF8 = 'utf-8'
ASCII = 'ascii'

GB_1 = 1e+9
# 12 gb
GB_12 = 1.2e+10
MAX_BYTES = GB_1
FIRST = '__FIRST_KEY__'
UNDEFINED = '__undefined__'

class DB(object):

    def __init__(self, **kwargs):
        self.start(**kwargs)

    def start(self,
              directory=WRITE_ENV,
              default_name=DEFAULT_DB_NAME,
              write=True,
              name=None,
              allow_duplicate=True,
              auto_commit=True,
              encoding=UTF8,
              auto_open=True,
              get_last=False,
              max_bytes=MAX_BYTES):

        # print('init DB')
        self.env_path = directory
        self.name = name or default_name or DEFAULT_DB_NAME
        self.write = write
        self.auto_commit = auto_commit
        self.encoding = encoding
        self.max_bytes = max_bytes
        # Return the last item of any duplicate keys on get().
        # This is three operations more expensive per transaction.
        self.get_last = get_last
        self.allow_duplicate = allow_duplicate
        # If auto)open is true and a 'name' is, the initial DB will open()
        # with the given name
        self.auto_open = auto_open
        self.is_open = False
        self._cursor = None
        self._auto_open()

    def _auto_open(self):
        if self.auto_open is True and self.name is not None:
            self.open()

    def get_cursor(self):
        if self._cursor is None:
            self._cursor = self.txn.cursor()

        return self._cursor

    cursor = property(get_cursor)

    def _open_args(self, **options):
        """Arguments given to the 'open()' of the internal DB."""
        # https://lmdb.readthedocs.io/en/release/#lmdb.Environment
        # Environment(path,
        #       map_size=10485760,
        #       subdir=True,
        #       readonly=False,
        #       metasync=True,
        #       sync=True,
        #       map_async=False,
        #       mode=493,
        #       create=True,
        #       readahead=True,
        #       writemap=False,
        #       meminit=True,
        #       max_readers=126,
        #       max_dbs=0,
        #       max_spare_txns=1,
        #       lock=True)
        result = dict(
            subdir=True,
            max_dbs=5,
            create=True,
        )

        result.update(options)
        return result

    def wipe(self, destroy=False):
        print('Wiping', self.child_db)
        if destroy:
            print('! --- Destroying database')
        self.txn.drop(self.child_db, delete=destroy)
        if destroy:
            self.txn.commit()
            print('Rebooting')
            self.start()
        else:
            self.commit()

    def open(self, name=None, env_path=None, write=True, max_bytes=MAX_BYTES):
        name = name or self.name
        env_path = env_path or self.env_path
        write = self.write if write is None else write
        max_bytes = max_bytes or self.max_bytes
        print('Open Env', env_path)
        open_args = self._open_args(map_size=max_bytes)

        self.env = lmdb.open(env_path,**open_args)

        """
        open_db(key=None,
        txn=None,
        reverse_key=False,
        dupsort=False,
        create=True,
        integerkey=False,
        integerdup=False,
        dupfixed=False)

        Open a database, returning an opaque handle.
        Repeat Environment.open_db() calls for the same name will
        return the same handle. As a special case, the main database
        is always open.

        Equivalent to mdb_dbi_open()

        Named databases are implemented by storing a special descriptor in
        the main database. All databases in an environment share the same
        file. Because the descriptor is present in the main database,
        attempts to create a named database will fail if a key matching
        the database's name already exists. Furthermore the key is visible
        to lookups and enumerations. If your main database keyspace conflicts
        with the names you use for named databases, then move the contents
        of your main database to another named database.
        """
        self.child_db = self.env.open_db(
            key=self.encode(name),
            dupsort=True,
            # reverse_key=True
            )
        # Open transaction
        self.txn = None
        # self.child_db = self.env.open_db(name)
        self.txn = self.create_transaction(
            # allow writing
            write=self.write,
            # Keep last transaction as parent
            as_child=True,
            )

        self.is_open = True
        self.name = name

    def put(self, key, value, save=True, encode=True, encode_key=True, as_dup=None, **kwargs):
        '''put(key, value, dupdata|as_dup=True, overwrite=True, append=False, db=None)

        Store a record, returning True if it was written, or False to indicate
        the key was already present and overwrite=False. On success, the cursor
        is positioned on the new record.
        Equivalent to mdb_put()

        key:
            Bytestring key to store.
        value:
            Bytestring value to store.
        as_dup:
            If True and database was opened with dupsort=True,
            add pair as a duplicate if the given key already exists.
            Otherwise overwrite any existing matching key.
        overwrite:
            If False, do not overwrite any existing matching key.
        append:
            If True, append the pair to the end of the database without
            comparing its order first. Appending a key that is not
            greater than the highest existing key will cause corruption.
        db:
            Named database to operate on. If unspecified, defaults to
            the database given to the Transaction constructor.
        '''

        key = self.encode(key) if encode_key is True else key
        store_val = self.encode(value) if encode is True else value

        if self.allow_duplicate is True or as_dup is True:
            kwargs['dupdata'] = True
            # kwargs['overwrite'] = False

        try:
            success = self.txn.put(key, store_val, **kwargs)
        except TypeError as e:
            # the user has presented a none bytes type.
            print('key type:', type(key))
            print('value type:', type(store_val))
            raise e

        self.dirty = save is False and success is True
        if save is False:
            return success

        return self._transaction_success(success)

    def encode(self, value):
        """Convert the value to a DB ready storage byte string"""
        if hasattr(value, 'encode') is True and self.encoding is not False:
            return value.encode(self.encoding)
        return self._convert_in(value)

    def decode(self, byte_value):
        """Decode the given value expecting a string like or byte data"""
        if hasattr(byte_value, 'decode'):
            return byte_value.decode(self.encoding)
        return str(byte_value)

    def _convert_in(self, value):
        """Convert the given value to a storable value, noting its type for
        reversal in _convert_out)
        """
        z =  "!:{}!:{}".format(type(value), value)
        return str(z).encode(self.encoding)

    def translate(self, value):
        return self._convert_out(value, render=False)

    def _convert_out(self, value, render=None):
        """Covert a value previously coverted for stage value."""
        render = True if render is None else render
        key = self.encode("!:")
        if value.startswith(key):
            if render:
                return eval(value.split(key)[2])
                # First item is empty due to key split.
            return value.split(key)[1:]
        return self.decode(value)

    def _transaction_success(self, success):
        if success is True and self.auto_commit is True:
            self.commit()

        # Uncommited changes exist.
        return success

    def replace(self, key, value, db=None, commit=None):
        previous = self.txn.replace(key, value, db)

        print('commiting transaction with success:')
        self._transaction_success(True)
        return previous


    def iter(self, keys=True, values=True, start=FIRST, decode=True,
        encode_key=None, dups=None, convert=True, render=None):

        encode_key = encode_key or decode

        if start is not None:
            if start == FIRST:
                self.first()
            else:
                start_key = start
                if encode_key:
                    self.position(start_key)


        cur = self.cursor
        method = cur.iternext
        if dups is not None:
            method = cur.iternext_dup if dups is True else cur.iternext_nodup

        for items in method(keys=keys, values=values):
            if keys and encode_key:
                key = self.decode(items[0])

            if keys and decode:
                value = self._convert_out(items[-1], render=render) if convert else items[-1]
            else:
                value = self._convert_out(items, render=render) if convert else items

            if keys:
                yield key, value
            else:
                yield value

    def collect(self, key, **kwargs):
        """Return a generator of duplicates for the given key
        like a 'filter'
        """
        gen = self.iter(keys=False, start=key, dups=True, **kwargs)
        return tuple(gen)

    def keys(self, **kwargs):
        gen = self.iter(values=False, dups=False, convert=False, **kwargs)
        return tuple(gen)

    def values(self, **kwargs):
        gen = self.iter(keys=False, **kwargs)
        return tuple(gen)

    def position(self, key):
        return self.cursor.set_key(self.encode(key))

    def first(self):
        self.cursor.first()

    def count(self, key=None, restore=False):

        if key is not None:
            self.position(key)

        return self.cursor.count()

    def delete(self, key, value=None, db=None, commit=True):
        '''Delete a key from the database.
        key:
            The key to delete.
        value:
            If the database was opened with dupsort=True and value is not None,
            then delete elements matching only
            this (key, value) pair, otherwise all values for key are deleted.
        '''
        e_val = b''
        if value is not None:
            e_val = self.encode(value)

        success = self.txn.delete(self.encode(key), e_val, db)
        if commit is False:
            return success

        print('commiting transaction')
        return self._transaction_success(success)

    def get(self, key, default=None, db=None, convert=True, last=None):
        ckey = self.encode(key)
        last = self.get_last if last is None else last
        if last is True:
            cursor = self.cursor
            cursor.set_key(ckey)
            cursor.last_dup()
            dbval = cursor.value()
        else:
            dbval = self.txn.get(ckey, default, db)

        if dbval is None:
            return dbval

        if convert is False:
            return dbval

        return self._convert_out(dbval)


    def pop(self, key):
        """Fetch a record's value then delete it. Returns None if no previous
        value existed. This uses the best available mechanism to minimize the
        cost of a delete-and-return-previous operation.

        For databases opened with dupsort=True, the first data element
        ("duplicate") for the key will be popped.
        """
        return self.cursor.pop(self.encode(key))

    def close(self):
        self.env.close()
        self.is_open = False

    def commit(self):
        # print('Commit')
        self.txn.commit()
        self.txn = self.create_transaction()

    def create_transaction(self, write=None, using=None, as_child=True):
        """make a ready transaction for the next put. return the new transactio

        write: boolean
            Open the new transaction with write flag. If None, self.write is used
        using: database
            a child database to use. If none the self.child_db is used.
            If the child db does not exist the main database is applied
        as_child: boolean
            If true, the current transaction (if any) refer as a parent to the new
            transaction.
        """

        write = self.write if write is None else write
        kw = {'write': write}
        kw['db'] = self.child_db
        if using is not None:
            # pick from _None_ or the current child db
            kw['db'] = using

        if as_child is True and self.txn is not None:
            pass
            # kw['parent'] = self.txn

        # print("Creating transaction with", kw)
        self._cursor = None
        return self.env.begin(**kw)

    def __repr__(self):
        s = '<{}.{} "{}">'
        selfc = self.__class__
        return s.format(selfc.__module__, selfc.__name__, self.name)

class Mappable(object):
    type = None
    mappable = True

    @classmethod
    def convert(cls, *values):
        _type = cls.type or cls
        return _type(values)


DB_TYPE_MAP = {}

def register(cls):
    """Apply the cls to the encoder registry. When a put() occurs for a
    value matching the class pattern, a special encoding method is applied
    for store.
    """
    types = cls.get_type()
    if hasattr(types, '__iter__') is False or isinstance(types, str):
        types = [types]

    print('Registering autotype {} {}'.format(cls, types))
    for _type in types:
        DB_TYPE_MAP[_type] = cls



class AutoRegister:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register(cls)


class Type(str):
    type = None

    @classmethod
    def get_type(cls):
        if isinstance(cls.type, (tuple, list)):
            return tuple(x.__name__ for x in cls.type)
        return cls.type.__name__


class CommaAppend:

    @classmethod
    def append(cls, byte_string):
        """Return an altered version of the converted byte string
        to allow 'append' to the stored byte string.

        Luckily with bytes, simply 'add' the required comma for `convert()` for loop
        """
        print( 'Comma Append', byte_string)
        return b',' + byte_string


class BaseType(Type, AutoRegister, CommaAppend):
    type = str

    @classmethod
    def convert(cls, *values):
        if isinstance(cls.type, (tuple, list)):
            return cls(values)

        return cls.type(values)


class ATuple(BaseType):
    type = tuple

class A1D(Type, AutoRegister, CommaAppend):
    type = tuple, list

    @classmethod
    def convert_in(cls, value, map_type):
        return value, map_type

    @classmethod
    def convert_out(cls, type_cls, value):
        return type_cls(value)



class ADict(BaseType, CommaAppend):
    type = dict

    @classmethod
    def convert(cls, *values):
        res = {}
        for inner_dict in values:
            res.update(inner_dict)
        return res


class AList(ATuple):
    type = list


class ABool(BaseType):
    type = bool

    @classmethod
    def convert(cls, value):
        return value

class ANumber(BaseType):
    type = int, float, complex

class AString(BaseType):
    type = str

class OrderedDB(DB):

    def next(self):
        """return the next key of the (cursor current position index)+1
        and set the cursor position for the next relative steo.
        """

        success = self.cursor.next()

        if success is False:
            raise StopIteration
        key, value = self._get_cursor_row()
        return key, value

    def _get_cursor_row(self):
        """Return the key, value of the cursors current position."""
        return self.cursor.key(), self.cursor.value()


class AppendableDB(OrderedDB):

    def append(self, key, value, safe=False):

        val, ConvertClass = self._convert_in(value, False, with_class=True)

        if hasattr(ConvertClass, 'append'):
            val = ConvertClass.append(val)

        try:
            result = self.get(key, convert=False)
            result += val
        except TypeError as e: #Unsupport Operand on None.
            if self.auto_commit and (safe is True):
                return self.put(key, value)
            raise TypeError("Cannot append to missing key: {}".format(key))

        return self.replace(self.encode(key), result)#, encode=False, overwrite=True)

    def _convert_in(self, value, prefix=True, with_class=False):
        """Convert the given value to a storable value, noting its type for
        reversal in _convert_out)
        """

        # Used for the internal 'appendable' unit type map.
        # It can be anything really =
        type_id = type(value).__name__

        lmap = {
            # 'list': AList,
            # 'tuple': ATuple,
            # 'dict': ADict,
            # 'bool': ABool,
        }

        convert_class = lmap.get(type_id, DB_TYPE_MAP.get(type_id))

        if hasattr(value, 'mappable') and value.mappable is True:
            convert_class = value.__class__

        if convert_class is None:
            convert_class = BaseType
            print('No value convertion for {} - defaulting to {}'.format(type_id, convert_class))

        map_type = convert_class.__name__

        # If no prefix, these elements are removed
        stamp = "!:" if prefix is True else ''
        map_type_prefix = map_type if prefix is True else ''

        if hasattr(convert_class, 'convert_in'):
            value, map_type_prefix = convert_class.convert_in(value, map_type_prefix)

        if isinstance(value, (list, tuple)):
            # Call into mappable, for later type conversion
            cut = str(value)[1:-1]

            if cut.endswith(','):
                cut = cut[:-1]
            value = convert_class(cut)#"{}, ".format(cut))

        z =  "{}{}{}{}".format(stamp, map_type_prefix, stamp, value)

        result = str(z).encode(self.encoding)

        if with_class:
            return result, convert_class
        return result

    def _convert_out(self, value, render=True, transpose=None):
        """
        Convert the given value from the database and return
        an item ready to digest by the application. The given 'value' is expected
        to be a byte string or something acting similar.
        The discovered database value is evaluted and converted to python
        literals.

            render {bool}: execute the found value to produce python objects
            transpose {bool}: convert the found data value when rendering.
                This is only usesful to 'render=False' and transpose=True
                for an execution of data without the execution sandbox.
        """
        render = True if render is None else render
        transpose = render if transpose is None else transpose
        """Covert a value previously coverted for stage value."""
        key = "!:"
        ekey = self.encode(key)
        result = value
        if hasattr(value, 'startswith') and value.startswith(ekey):
            splits = value.decode().split(key)
            result = self._convert_eval(splits, render, transpose)
        else:
            return result

        return result

    def _convert_eval(self, splits, render, transpose):
        # print('Converting', value)
        # print('  -- as', splits)
        # print('  -- to', render, ev)
        _eval = eval# literal_eval
        def _convert(cls_jumper, *values):

            if hasattr(cls_jumper, 'convert'):
                # print('_convert', cls_jumper, values)
                return cls_jumper.convert(*values)

            if isinstance(cls_jumper, tuple):
                eval_string = "{}.convert_out({}, {})".format(cls_jumper[0], cls_jumper[1], values)
                return _eval(eval_string)

            return values

        if render:
            eval_string = "_convert({0[1]}, {0[2]})".format(splits)
            try:
                return _eval(eval_string)
            except Exception as e:
                print("_convert_eval() render error: {}".format(e), eval_string)

        # Don't perform full rendering; extract the wanted value and
        # eval only.
        result = splits[2]
        if transpose:
            result = _eval(result)
        return result


from ast import literal_eval

class GRow(Mappable):
    # type = tuple
    cut = True

    @classmethod
    def convert(cls, *values):
        _type = cls.type or cls
        # print("GRow convert {} using {}".format(values, _type))
        return _type(*values)

    def __init__(self, *a):
        self._a = a

    def __str__(self):
        result = str(self._a)
        return result[1:-1] if self.cut else result

    def __repr__(self):
        return '<GRow {}>'.format(self._a)

    def __getitem__(self, key):
        return self._a[key]

    def __len__(self):
        return len(self._a)
