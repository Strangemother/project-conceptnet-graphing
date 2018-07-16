import time
import os

from multiprocessing import Process, Queue
from cache import set_cache, string_cache, set_global_root
from Queue import Empty

import secondary_functions
from json_socket import make_socket, send_json, get_socket

session = {}
socket = None
procs = None

def main():
    init_thread()


def init_thread(*args, **kw):
    q = Queue()
    procs = start_procs(q, *args, **kw)
    return (q, procs,)


def start_procs(q, *args, **kw):
    global procs
    procs = create_procs(q, *args, **kw)
    proc, socket_proc = procs
    print 'starting procs'
    proc.start()
    socket_proc.start()
    return procs


def create_procs(q, *args, **kw):

    proc = Process(target=init, args=(q, ) + args, kwargs=kw)
    socket_proc = Process(target=socket_init, args=(q, ) + args, kwargs=kw)
    return (proc, socket_proc,)


def kill_processes():
    for proc in procs:
        print 'Joining', proc
        proc.join()


def socket_init(queue, *a, **kw):
    global socket
    print 'socket_init', kw['socket_uri']
    socket_uri = kw.get('socket_uri', None)

    print 'init socket'
    socket = make_socket(socket_uri)
    run = 1
    while run:
        print '?',
        message = socket.recv()
        if message is not None:
            print '!', len(message)
        if message == 'kill':
            print 'socket kill pill'
            queue.put_nowait(message)
            run = 0
            continue
    print 'Finish socket'
    return socket


def init(queue, **kw):
    '''
    A initialization function for anything requiring a first boot.
    '''
    socket_uri = kw.get('socket_uri', None)
    cache_path = kw.get('cache_path', None)

    # global socket
    # if socket_uri is not None:
    #     print 'Making loop socket'
    #     socket = make_socket(socket_uri)
    print 'Init main loop'
    basepath = os.path.abspath(os.path.dirname(__file__))
    set_global_root(cache_path)
    secondary_functions.init(socket_uri=socket_uri)
    start(queue, socket_uri=socket_uri)


def start(queue, socket_uri=None):

    run = 1

    while run:
        message = None
        try:
            message = queue.get_nowait()
            print '.',
        except Empty:
            time.sleep(.2)

        if message == 'kill':
            run = 0
            if socket_uri is not None:
                 socket = make_socket(socket_uri)
                 socket.send('kill')
            continue
        run = step(message)

    print 'End Stepper'


def step(given_data=None):
    '''continuous call by a loop'''

    if given_data is not None:
        print 'Loop react', given_data
        secondary_functions.apply_to_context(given_data)
    return 1

if __name__ == '__main__':
    main()
