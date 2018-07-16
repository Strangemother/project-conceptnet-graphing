'''A Plugin is a python module as a standalone thread or a multiprocess
Process connected through websockets.
'''
import threading
import sys
from log import log

import json_socket


class SocketWorker(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        self.target = target
        return

    def _connect(self, uri):
        socket = json_socket.get_socket()
        if uri is not None:
            socket = json_socket.get_or_create(uri)
        return socket

    def die(self):
        self.socket.send('kill')


    def run(self):
        self.socket = self._connect(self.args[0])
        self.lock = self.args[1]
        self.socket.send('SocketWorker connected "{}"'.format(self.name))
        log('running with {} and {}'.format(self.args, self.kwargs))
        run = 1

        plugin = self.kwargs.get('plugin', None)

        while run:
            m = self.socket.recv()
            if m == 'kill':
                run = 0
                break

            if plugin is not None:
                log('Returning message')
                self.lock.acquire()
                try:
                    run = self.target(m)
                except Exception as e:
                    _t, _v, _tr = sys.exc_info()
                    log('Worker error:', e)
                    log(_tr)
                self.lock.release()

        log('SocketWorker death "{}"'.format(self.name))

        return


class Plugin(object):
    '''A Plugin class wraps up a mounting strategy with an automatic JSON
    socket.'''
    mount_type = None
    _recv_thread = True

    def _init(self, config=None):
        '''
        >>> pp=plugin.Plugin()
        >>> pp._init(dict(socket_uri="ws://127.0.0.1:8009"))
        >>> pp.socket.send('cake')
        10
        '''
        self.msgs = []
        config = config or self.config or {}
        self._mount(config)


    def _connect(self, uri):
        '''
        >>> pp=plugin.Plugin()
        >>> pp._connect("ws://127.0.0.1:8009")
        >>> pp.socket
        <websocket._core.WebSocket object at 0x0000000002E2E940>
        '''
        socket = json_socket.get_socket()
        if uri is not None:
            socket = json_socket.get_or_create(uri)
            log('Connected new socket')
        return socket

    def _mount(self, config):
        log('Mounting')
        config = config or self.config or {}
        self.uri = config.get('socket_uri', None)
        self.socket = self._connect(self.uri)
        v = config.get('recv_thread', self._recv_thread)
        log("Mounting thread:", v)
        if v is True:
            self.recv_thread()

    def recv_thread(self):
        self.lock = threading.Lock()
        self.thread = SocketWorker(
            name='plugin_worker',
            target=self._worker_message,
            args=(self.uri, self.lock,),
            kwargs=dict(plugin=self),
            )

        self.thread.start()

    def _worker_message(self, msg):
        log('Plugin class received msg from worker', msg)
        wait_request = self._recv(msg)
        return 1

    def _announce(self):
        _type = self._type or self.mount_type
        self.socket.send(dict(type=_type, msg='_announce'))

    def _recv(self, msg):
        '''received an incoming msg from the connected client'''
        self.msgs.append(msg)

