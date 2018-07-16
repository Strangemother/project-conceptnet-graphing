'''
from conceptnet import dbstore
dbstore.spread_redis_apply(max_count=100, max_cpu=1)


# populate the database with the given [builtin] csv
from conceptnet import sqlite_db
db = sqlite_db.fill_word_db({})

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
'''

import sqlite3
import multiprocessing
from log import log
import traceback

from conceptnet.parse import parse_csv, clean_line, spread
'''
from conceptnet import sqlite_db
sqlite_db.store_sqlite_lines(dict(max_count=20000))
'''
import json
from sqlite3 import OperationalError, ProgrammingError
from multiprocessing import Queue, cpu_count

import os
from parse import job_split
from multiprocessing import Pool, Process
import atexit
import multiprocessing
from Queue import Empty

import string
import random
import re

UNDEFINED = 'undefined'
INSERT = 'insert'
COMMIT = 'commit'
CLOSE = 'close'
SELECT = 'select'


def open_db(name):
    if os.path.isfile(name) is False:
        stream = open(name, 'wb')
        stream.close()

    conn = sqlite3.connect(name)
    return conn, conn.cursor()


def create(cursor):

    word_table = '''CREATE TABLE word (
        start_word STRING,
        end_word   STRING,
        relation   STRING,
        weight     REAL,
        json       TEXT
    );
    '''

    table_index = '''
    CREATE INDEX value ON word (
        start_word,
        end_word
    );
    '''
    if cursor:
        cursor.execute(word_table)
        cursor.execute(table_index)

        cursor.commit()


def table_exists(name='word', db=None):
    word = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}';"
    ex_str = word.format(name)

    count = db.execute(ex_str).fetchall()[0][0]
    return count > 0


def store_sqlite_lines(kw):
    process_name = multiprocessing.current_process().name
    db_index = kw.get('job_index', 0)

    db, conn = open_db("sql-{}.db".format(process_name))
    if table_exists('word', db) is False:
        create(db)

    options = dict(
        max_count=kw.get('max_count', 100000),
        iter_line=sqlite_apply,
        as_set=True,
        db=db,
        cursor=conn,
        keep_sample=kw.get('sample', False),
        byte_start=kw.get('byte_start', None),
        byte_end=kw.get('byte_end', None),
    )

    try:
        d, sample = parse_csv(**options)
    except Exception as e:
        log('Error on "{}" :'.format(process_name), e)
        log(traceback.format_exc())
        d = []

    db.commit()
    db.close()
    return list(d)


def sqlite_apply(line, **kw):
    cursor = kw.get('cursor', None)
    if cursor is None:
        return

    l = clean_line(line, **kw)
    k = []

    if l is None:
        return None

    _type, sw, ew, weight, _json = l

    _json.update({
        "relation": _type,
        "weight": weight,
    })

    values = (sw, ew, _type, weight, json.dumps(_json))
    insert_str = '''INSERT INTO word VALUES {}'''.format(values)
    try:
        cursor.execute(insert_str)
    except OperationalError as e:
        raise e

    if kw.get('row_index', 0) % 100 == 0:
        kw.get('db').commit()



def fill_apply(line, **kw):

    l = clean_line(line, **kw)
    k = []
    db = kw.get('db')

    if l is None:
        return None

    _type, sw, ew, weight, _json = l

    _json.update({
        "relation": _type,
        "weight": weight,
    })

    values = (sw, ew, _type, weight, _json)

    db.add_line(*values)

    if kw.get('row_index', 0) % 100 == 0:
        db.commit()


def fill_word_db(kw):

    db = spread_db(**kw)

    options = dict(
        max_count=kw.get('max_count', 100000),
        iter_line=fill_apply,
        as_set=True,
        db=db,
        keep_sample=kw.get('sample', False),
        byte_start=kw.get('byte_start', None),
        byte_end=kw.get('byte_end', None),
    )

    try:
        d, sample = parse_csv(**options)
    except Exception as e:
        log('Error:', e)
        log(traceback.format_exc())
        d = []

    db.commit()
    db.close()
    return db, list(d)


def spread_db(**kw):
    '''Open many processes with a DB for each.
    return a unified value of all db's on request.
    '''

    db = WordDB()
    db.create(open_wait, **kw)
    db.start()
    return db


class SpreadDBHandle(object):
    '''A Simple multiprocess gateway to multiple sqlite dbs, each containing
    the same table structure but maintaining single copies of a record
    across any thread.

    '''
    def __init__(self, queues=None, pool=None):
        self.queues = queues
        self._pool = pool
        self._step_next = 0
        self._dead = False
        self._q_ordered = None
        atexit.register(self.terminate)
        self.quit = self.terminate

    def create(self, func, count=None, **kw):
        count = count or cpu_count()
        m = multiprocessing.Manager()
        self.queues = [(i, m.Queue(),) for i in range(count)]
        self._q_ordered = dict(self.queues).values()
        self.response_queue = m.Queue()
        _kw = dict(
            cpu_count=count,
            # path=None, # auto
            queues=self.queues,
            response_queue=self.response_queue,
        )
        kw.update(_kw)

        self._pool = self.async_spread(func, **kw)
        self._dead = False

    def async_spread(self, func, **kw):
        '''
        Generate the jobs and process pool. return a list of Process
        '''
        jobs = job_split(**kw)
        pool = []
        counter = 0
        for job in jobs:
            name = self.process_name(counter)
            counter += 1
            proc = Process(target=func, name=name, args=(job,))
            pool.append(proc)

        log('Spreading {} jobs to pool'.format(len(jobs)))
        return pool

    def process_name(self, counter):
        return "proc-{}".format(counter)

    def start(self):
        '''
        start a waiting 'create()' _pool.
        '''
        if self._dead is True:
            log('Previously dead threads must be recreated, SpreadDB.create()')
            return False

        for proc in self._pool:
            proc.start()
        return True

    def send_all(self, *a):
        '''Send one message copied to every process queue
        '''
        for q in self.queues:
            q[1].put_nowait(*a)

    def send_next(self, msg):
        res = self.send_to(self._step_next, msg)

        self._step_next += 1
        if self._step_next >= len(self.queues):
            self._step_next = 0

        return res

    def send_to(self, index, msg, wait=False):
        mname = 'put_nowait' if wait is False else 'put'
        # log('send to', index)
        return getattr(self._q_ordered[index], mname)(msg)

    def fetch(self, select_str, args=None):
        _id = rand_str()
        v = self.send_all((SELECT, (select_str, args, ), None, _id))
        log('Wait on', _id)
        result = self.loop_wait(len(self._pool), _id)
        log('\nResult', len(result))
        return result

    def loop_wait(self, count, _id):

        keep = ()
        snooze = ()
        q = self.response_queue
        while 1:
            try:
                value = q.get_nowait()
                # log(index, 'Got message', msg)
                if value[1] == _id:
                    log('Recv a value from', value[0], 'expecting', count, 'got', len(keep))
                    keep += (value,)
                else:
                    snooze += (value,)
            except Empty:
                pass

            if len(keep) >= count:
                break

        log('Done. Reapplying {}'.format(len(snooze)))

        for value in snooze:
            q.put_nowait(value)

        result = ()
        for index, p_id, results in keep:
            for row in results:
                result += (row,)
        return result

    def commit(self):
        self.send_all(COMMIT)

    def close(self):
        self.send_all(CLOSE)

    def terminate(self):
        '''Hard kill of the threads. '''
        for proc in self._pool:
            proc.terminate()
        self._dead = True

    def shutdown(self):
        '''Clean close of the threads. Sending a kill message and waiting for
        join'''
        log('shutdown', self)
        self.send_all('kill')
        for proc in self._pool:
            proc.join()
        self._dead = True


class WordDB(SpreadDBHandle):

    def __init__(self, queues=None, pool=None):
        super(WordDB, self).__init__(queues, pool)

    def add_line(self, start_word, end_word, relation, weight=1, meta=None, commit=True):
        values = (start_word, end_word, relation, weight, json.dumps(meta or {}))
        #es_start_word = re.escape(start_word)
        #es_end_word = re.escape(end_word)
        insert_str = '''INSERT INTO word VALUES (?, ?, ?, ?, ?)'''.format(values)

        # # Line one calls the StatementHandler with inline arguments (or None)
        # line = (INSERT, insert_str, )

        # Apply args, kwargs
        _id = rand_str()
        line = (INSERT, (insert_str, ) , dict(params=values, commit=commit), _id)

        return self.send_next(line)

    def get_word(self, start_word):
        stmt = 'SELECT * FROM word WHERE start_word = ?'
        return self.fetch(stmt, (start_word, ))


def rand_str(length=10):
    chars = string.ascii_letters
    return ''.join([chars[random.randrange(len(chars))] for x in range(length)])


def get_or_create_db(**kw):
    process_name = multiprocessing.current_process().name
    cp = os.path.join(os.path.dirname(__file__), '..', 'cache', 'sqlites')
    bp = kw.get('root_path', cp)
    fp = os.path.abspath(os.path.join(bp, "sql-{}.db".format(process_name)))
    log('filepath', fp)
    db, conn = open_db(fp)

    if table_exists('word', db) is False:
        log('Thread {} - creating new table'.format(process_name))
        create(db)

    return db, conn


def open_wait(kw):
    log('Running thread'. index)
    queues = kw.get('queues', {})
    index = kw.get('job_index')

    queue = dict(queues)[index]
    db_index = kw.get('job_index', 0)

    db, conn = get_or_create_db()
    rq = kw.get('response_queue', None)

    run = 1
    while run:
        try:
            msg = queue.get()
            # log(index, 'Got message', msg)
        except Empty:
            pass

        if msg == 'kill':
            run = 0
            continue

        result,_id = process_queue_message(msg, db, conn, kw)
        if (result in [UNDEFINED, None]) is False:
            if (_id is not None) and (rq is not None):

                # log('Sending Response from', index, '\n', len(result))
                rq.put_nowait((index, _id, result,))
            #else:
            #    log('Going nowhere')


def process_queue_message(msg, db, cursor, kw):
    # log('process_queue_message', kw.get('job_index'))
    # log(kw)
    result = StatementHandler(db, cursor).call(msg)
    return result


class StatementHandler(object):

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def call(self, msg):

        com = msg
        args = (msg,)
        kw = {}
        lm = len(msg)
        result = UNDEFINED
        with_kw = True
        _id = None

        if lm == 1:
            # A single statement, such as 'commit'
            name = "stmt_{}".format(msg[0])
            result = getattr(self, name)()

        if lm == 2:
            # a type and string.
            # convert the string into args
            com = msg[0]
            args = (msg[1], )
            name = "stmt_{}".format(com)
            with_kw = False

        if lm == 3:
            com, args, kw = msg

        if lm == 4:
            com, args, kw, _id = msg

        name = "stmt_{}".format(com)

        if with_kw is False or (kw is None):
            result = getattr(self, name)(*args)
        else:
            result = getattr(self, name)(*args, **kw)

        return result, _id


    def stmt_commit(self, *a):
        return self.db.commit()

    def stmt_close(self, *a):
        return self.db.close()

    def stmt_select(self, line, params=None, commit=True, fetchall=True):
        # log('Select statement', line, params)
        return self.execute(line, params, fetchall=fetchall)

    def stmt_insert(self, line, params=None, commit=True):
        return self.execute(line, params=params, commit=commit)

    def executemany(self, line, params=None, fetchall=True):
        if params is None:
            params = ()

        return self.execute(line, params, commit=False, func='executemany')

    def execute(self, line, params=None, commit=True, func='execute', fetchall=False):
        # log('Execute', line)

        try:
            if params is not None:
                # log(func, line)
                getattr(self.cursor, func)(line, params)
            else:
                # log(func, line)
                getattr(self.cursor, func)(line)

        except OperationalError as e:
            log('OP ERROR', traceback.format_exc())
            log('Line: {}'.format(line))
            raise e
        except ProgrammingError:
            log('Skipped "{}"'.format(params))

        if commit is True:
            self.db.commit()

        if fetchall is True:
            log('fetch')
            return self.cursor.fetchall()

        return self.cursor.lastrowid
