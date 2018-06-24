'''A set of functions to call into the API - defined as 'primary' as the
first point of access
'''
import os
import contextnet_api as cnapi
from logger import print_edges
import words
from cache import set_global_root
# import secondary_functions
import loop
from json_socket import make_socket
from log import log

queue = None
loop_data = None


def allow_external(bool=None):
    if bool is not None:
        cnapi.FETCH_ALLOWED = bool
    return cnapi.FETCH_ALLOWED


def init(socket_uri="ws://127.0.0.1:8009"):
    '''
    A initialisztion function for anything requiring a first boot.
    '''
    global command
    global loop_data
    global queue
    # global socket
    # if socket_uri is not None:
    #     socket = make_socket(socket_uri)
    command = Command()
    basepath = os.path.abspath(os.path.dirname(__file__))
    cache_path = os.path.join(basepath, 'cache')
    set_global_root(cache_path)
    loop_data = dict(socket_uri=socket_uri, cache_path=cache_path)

    queue, procs = loop.init_thread(**loop_data)


def _base_boot(socket_uri="ws://127.0.0.1:8009"):
    basepath = os.path.abspath(os.path.dirname(__file__))
    cache_path = os.path.join(basepath, 'cache')
    set_global_root(cache_path)


COMMAND_STR = '!#'


def ask_loop():
    _run = True
    kill = False

    while _run is True:
        v = raw_input('\nWhat?: ')
        if v == '':
            log('Close _run')
            _run = False
        else:
            if v == 'kill':
                log('Loop kill in process')
                kill = True
            assess_string(v)
        if kill is True:
            _run = False
            log('Killing processes')
            loop.kill_processes()
    log('Finish askloop')



def assess_string(sentence):
    '''
    Given an input string, token and assess each token.
    '''
    if sentence[0] in COMMAND_STR:
        return command.command_mode(sentence)
    log('primary_functions assess_string')
    if queue is not None:
        queue.put_nowait(sentence)
    # return secondary_functions.apply_to_context(sentence)


class Command(object):

    def command_mode(self, command):
        _map = {
            "!": 'eval',
            "#": "hash",
        }

        comt = command[0]
        com = command[1:]
        mc = _map[comt]
        name = "com_{}".format(mc)
        log('Received command "{}"'.format(mc), name)

        if hasattr(self, name):
            return getattr(self, name)(com)

    def com_eval(self, com):
        ret = eval(com)
        log(ret)
        return ret


    def com_hash(self, com):
        coms = map(str.strip, com.strip().split(' '))
        com0 = coms[0]
        name = "hash_{}".format(com0)

        if hasattr(self, name):
            return getattr(self, name)(*coms[1:])

    def hash_die(self):
        '''Send a kill message'''
        log('Killing...')
        assess_string('kill')
        loop.kill_processes()
        log('Death complete.')

    def hash_start(self):
        log('Start Procs')
        loop.start_procs(queue, **loop_data)

    def hash_fetch(self, value=None):
        positive = ['true', 'yes', '1', 'on']
        negative = ['no', '0', 'false', 'off']
        lv =None
        if value is not None:
            lv = value.lower()
        switch = True if lv in positive else None
        switch = switch or (False if lv in negative else None)

        if switch is None:
            log('Fetch is currently:', allow_external())
            return

        log('Allow external data fetch: ', switch)
        allow_external(switch)

    def hash_delete(self, word):
        log('Delete word', word)
        log(cache.delete_word(word))

    def hash_cache(self, word):
        cnapi.api_fetch(word, allow_cache=False, _force_allow=True)


    def hash_read(self, data_file):
        '''given the name of a data file within the initial data folder, read each
        line into the ask loop.
        '''
        fn = '{}'.format(data_file)
        fpf = os.path.join(os.path.dirname(__file__), 'data', fn)
        log('read', fpf)

        if os.path.isfile(fpf):
            log('Slow reading', fpf)
            ts = 5
            with open(fpf, 'r') as stream:
                try:
                    for line in stream:
                        word = line.strip()
                        log('Asking', word)
                        assess_string(word)
                        log('sleeping', ts)
                        time.sleep(ts)
                except KeyboardInterrupt:
                    log('cancelled slow feed')
