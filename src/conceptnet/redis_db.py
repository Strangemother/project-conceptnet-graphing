import redis
import multiprocessing
from log import log
import traceback

from conceptnet.parse import parse_csv, clean_line, spread

'''
dbstore.spread_redis_apply(max_count=100, max_cpu=1)

from conceptnet import dbstore
dbstore.store_redis_lines(dict(max_count=100))
'''

def spread_redis_apply(**kw):
    return spread(store_redis_lines, **kw)


def store_redis_lines(kw):
    process_name = multiprocessing.current_process().name
    db_index = kw.get('job_index', 0)
    db = redis.StrictRedis(host='localhost', port=6987, db=db_index)
    pipe = db.pipeline()

    options = dict(
        max_count=kw.get('max_count', 100000),
        iter_line=redis_apply,
        as_set=True,
        pipe=pipe,
        row_index=kw.get('row_index', 1),
        keep_sample=kw.get('sample', False),
        byte_start=kw.get('byte_start', None),
        byte_end=kw.get('byte_end', None),
    )

    try:
        d, sample = parse_csv(**options)
        log('Finished relations. Count: {}. Writing file'.format(len(d)))
    except Exception as e:
        log('Error on "{}" :'.format(process_name), e)
        log(traceback.format_exc())
        d = []

    pipe.execute()

    return list(d)


def redis_apply(line, **kw):
    pipe = kw.get('pipe', None)
    if pipe is None:
        return

    l = clean_line(line, **kw)
    k = []

    if l is None:
        return None

    _type, sw, ew, weight, _json = l

    _json.update({
        "connection": _type,
        "weight": weight,
        "direction": ('start', 'end',)
    })

    pipe.set(sw, str(_json))

    _json["direction"] = ('end', 'start',)
    pipe.set(ew, str(_json))

    if kw['row_index'] % 1000 == 0:
        pipe.execute()
