import multiprocessing
import traceback

from parse import parse_csv, clean_line, spread

def spread_caller_function(**kw):
    return spread(store_lines, **kw)

def writer_function(*a, **kw):
    print(a, kw)

def store_lines(kw):
    process_name = multiprocessing.current_process().name
    db_index = kw.get('job_index', 0)
    pipe = writer_function

    options = dict(
        max_count=kw.get('max_count', 100000),
        iter_line=caller_function,
        as_set=True,
        pipe=pipe,
        row_index=kw.get('row_index', 1),
        keep_sample=kw.get('sample', False),
        byte_start=kw.get('byte_start', None),
        byte_end=kw.get('byte_end', None),
    )

    try:
        d, sample = parse_csv(**options)
        print('Finished relations. Count: {}. Writing file'.format(len(d)))
    except Exception as e:
        print('Error on "{}" :'.format(process_name), e)
        print(traceback.format_exc())
        d = []

    # pipe.execute()

    return list(d)


def caller_function(line, **kw):
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
        #"direction": ('start', 'end',)
    })

    print('{start[word]} {connection} {end[word]} {weight}'.format(**_json))
    if kw['row_index'] % 1000 == 0:
        pass
        # pipe.execute()


if __name__ == '__main__':
    store_lines({})
