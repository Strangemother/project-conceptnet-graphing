import time
import os

from json_socket import make_socket, send_json, get_socket
from multiprocessing import Process, Queue
from cache import set_cache, string_cache, set_global_root
from Queue import Empty

session = {}
socket = None

def main():
    init_thread("ws://127.0.0.1:8009")

def init_thread(*args):
    q = Queue()
    proc = Process(target=init, args=(q, ) + args)
    socket_proc = Process(target=socket_init, args=(q, ) + args)
    proc.start()
    socket_proc.start()
    return proc

def socket_init(queue, socket_uri=None, *a):
    global socket
    queue.put_nowait('Init socket')
    socket = make_socket(socket_uri)

    while 1:
        print '?',
        message = socket.recv()
        if message is not None:
            print '!', message
            queue.put_nowait(message)

    queue.put_nowait('Finish socket')
    return socket

def init(queue, socket_uri=None, cache_path=None):
    '''
    A initialization function for anything requiring a first boot.
    '''

    global socket
    if socket_uri is not None:
        socket = make_socket(socket_uri)

    basepath = os.path.abspath(os.path.dirname(__file__))
    set_global_root(cache_path)
    start(queue)


def start(queue):

    run = 1

    while run:
        message = None
        try:
            message = queue.get_nowait()
            print '.',
        except Empty:
            pass
        run = step(message)
        time.sleep(1)



def step(given_data=None):
    '''continuous call by a loop'''
    print '-',
    return 1

if __name__ == '__main__':
    main()
