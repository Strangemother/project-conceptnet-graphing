import multiprocessing
import traceback

from .parse import parse_csv, clean_line, spread

def spread_caller_function(**kw):
    return spread(store_lines, **kw)

def writer_function(*a, **kw):
    print(a, kw)

def store_lines(kw):
    process_name = multiprocessing.current_process().name
    db_index = kw.get('job_index', 0)

    options = dict(
        max_count=kw.get('max_count', 1_000_000),
        iter_line=caller_function,
        as_set=True,
        row_index=kw.get('row_index', 0),
        keep_sample=kw.get('sample', False),
        byte_start=kw.get('byte_start', None),
        byte_end=kw.get('byte_end', None),
        path=kw.get('path', None)
    )

    options.update(kw)
    try:
        d, sample = parse_csv(**options)
        print('Finished relations. Count: {}. Writing file'.format(len(d)))
    except Exception as e:
        print('Error on "{}" :'.format(process_name), e)
        print(traceback.format_exc())
        d = []

    # pipe.execute()

    return list(d)

chunk_list = ()

def caller_function(line, **kw):

    l = clean_line(line, **kw)
    k = []

    if l is None:
        return None

    _type, sw, ew, weight, _json = l

    _json.update({
        "connection": _type,
        "weight": weight,
        #"direction": ('start', 'end',)
    })

    chunk_size = kw.get('chunk_size', 1000)
    kw['row_index'] += 1
    if kw['row_index'] % chunk_size == 0:
        global chunk_list
        func = kw.get('step_function', line_print)
        res = func(chunk_list, line, kw)
        chunk_list = ()
    else:
        chunk_list += (_json, )


def line_print(items, line, given_kwargs):

    print('LAST: {start[word]} {connection} {end[word]} {weight}'.format(**items[-1]))


if __name__ == '__main__':
    store_lines({})
