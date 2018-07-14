#from log import log
import json
import csv
import os

import multiprocessing
from multiprocessing import Pool, cpu_count

csv_path = 'E:\\conceptnet\\assertions.csv'


def job_split(**kw):
    '''
        >>> concepnet.parse.job_split(path=csv_path)
        [{'start': 0L, 'end': 1071224347L},
        {'start': 1071224348L, 'end': 2142448695L},
        {'start': 2142448696L, 'end': 3213673043L},
        {'start': 3213673044L, 'end': 4284897391L},
        {'start': 4284897392L, 'end': 5356121739L},
        {'start': 5356121740L, 'end': 6427346087L},
        {'start': 6427346088L, 'end': 7498570435L},
        {'start': 7498570436L, 'end': 8569794783L}]
    '''

    bytes = os.stat(kw.get('path', csv_path)).st_size
    count = kw.get('cpu_count', cpu_count())
    chunk = bytes / count

    jobs = []

    for i in xrange(count):
        job = dict(
            job_index=i,
            byte_start=chunk * i,
            byte_end=chunk * (i + 1) - 1,
        )
        job.update(kw)
        jobs.append(job)

    return jobs


def spread(func, **kw):
    jobs = job_split(**kw)
    pool = Pool(len(jobs))
    print('Spreading {} jobs to pool {}'.format(len(jobs), pool))
    result = pool.map(func, jobs)
    return result


def parse_csv(path=csv_path, max_count=20000, iter_line=None, as_set=False,
    keep_sample=False, **iter_line_kwargs):
    global skip_stream
    start = iter_line_kwargs.get('byte_start', None)
    end = iter_line_kwargs.get('byte_end', None)

    if os.path.isfile(path) is False:
        raise Exception('Parse CSV is not a file: "{}"'.format(path))

    stream = open(path, 'rt', encoding='utf-8')

    if start is not None:
        stream.seek(start)
        print( next(stream))

    if end is not None:
        print('Seek from {} to {}'.format(start, end))
    count = 0
    pc = 0
    res = () if as_set is not True else set()

    samples = ()

    skip_stream = open('./skips.csv', 'w')
    func = iter_line or clean_line
    print('Reading {} maximum lines'.format(max_count))

    for raw_line in stream:
        line = next(csv.reader((raw_line,), delimiter='\t'))

        if max_count is not None and count > max_count:
            break

        dval = func(line, parser_index=pc, **iter_line_kwargs)
        if dval is None:
            if line[1] == '/r/ExternalURL':
                continue
            s = '/c/en/'
            if line[0][2].startswith(s) is True and line[0][3].startswith(s) is True:
                import pdb; pdb.set_trace()  # breakpoint 1073775b //


        if as_set is True:
            res.add(dval)

            if keep_sample is True and len(res) > len(samples):
                s = '/c/en/'
                if line[2].startswith(s) is True and line[3].startswith(s) is True:
                    samples += (line,)
        else:
            res += (dval,)

        count += 1
        pc += 1
        if end is not None and stream.tell() > end:
            print('Hit limit')
            break

        if pc > 100000:
            pc = 0

    print( 'count', count)
    stream.close()
    skip_stream.close()

    return res, samples


postfix_map = {
    "n": "noun", # /n
    "v": "verb", # /v
    "a": "adjective", # /a
    "s": "adjective satellite", # /s
    "r": "adverb", # /r
}

POSTMAP = postfix_map.keys()

def clean_line(line, **kw):
    '''Return a cleaned CSV line as a tuple
    '''
    try:
        uri, rel, start, end, js = line
    except ValueError as e:
        skip_stream.write('{}\n'.format(line))
        uri, rel, start, end, js = None, None, None,None,None

    if rel == '/r/ExternalURL':
        return None

    if start is None:
        return None

    startl = start[3:5]
    endl = end[3:5]
    startw  = start[6:]
    endw = end[6:]
    sub_rel = rel[3:]
    langs = ['en']
    sl = startw[:-1]
    el = endw[:-1]

    if (startl in langs) is False or (endl in langs) is False:
        return None

    if js is None:
        return None

    _json = json.loads(js)
    weight = _json['weight']


    _json['start'] = dict(lang=startl, word=startw)
    _json['end'] = dict(lang=endl, word=endw)

    if sl in POSTMAP:
        _json['start']['synset'] = postfix_map[sl]

    if el in POSTMAP:
        _json['end']['synset'] = postfix_map[el]

    del _json['sources']

    if 'dataset' in _json:
        del _json['dataset']

    if 'license' in _json:
        del _json['license']


    _json['id'] = uri
    return (sub_rel, startw, endw, weight, _json)

