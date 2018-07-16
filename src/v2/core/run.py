'''Core run service with the initial 'run_core' function to boot a main
queue thread and waiting socket.
'''
from multiprocessing import Process, Queue


import json_socket
from log import log
from initial import run_core


standard_config = dict(
    socket_uri="ws://127.0.0.1:8009",
)

queue_prc = None
socket_prc = None


def _json_socket(uri):
    socket = json_socket.get_socket()
    if uri is not None:
        socket = json_socket.get_or_create(uri)
    return socket


def socket_receiver(queue, config=None):
    config = config or {}
    uri = config.get('socket_uri', None)
    socket = _json_socket(uri)
    if socket is None:
        # no worker to run.
        return False

    run = 1
    while run:
        m = socket.recv()
        if m == 'kill':
            run = 0
        queue.put(m)

    log('finished socket_receiver')


def thread_run(queue=None, config=None):
    global queue_prc
    global socket_prc

    conf = config or {}
    settings = standard_config.copy()
    settings.update(conf)


    q = queue or Queue()

    socket_prc = Process(target=socket_receiver, args=(q, settings))
    socket_prc.start()

    global_prc = Process(target=run_core, args=(q, settings))
    global_prc.start()

    return global_prc, q
