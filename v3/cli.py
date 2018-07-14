'''
Some simple functionality to expose the 'assess_string' functionality to the
CLI with.

run `ask_loop` with a callback function. All CLI input is first checked against
a set of internal commands. IF the string is clean the callback is called with
a string sentence.

Command class allows exposure of functionality rather than strings for assessment.
provide "#list" to see all available commands
'''
import os
import contextnet_api as cnapi
# from logger import print_edges
import words
from cache import set_global_root
import cache
# import secondary_functions
#import loop
from json_socket import make_socket

import logging


logging.basicConfig(level=logging.DEBUG)

def log(*a):
    logging.info(' '.join(map(str, a)))

warn = logging.warn


queue = None
loop_data = None


class Command(object):

    def __init__(self):
        log('\n\n---- Command function intervention applied.----\n\n')
        log('\nType #list for actions\n')

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

    def hash_list(self):
        """print a list of available commands"""
        v = [x[5:] for x in dir(self.__class__) if x.startswith('hash_')]
        log('available commands: {}'.format(', '.join(v)))

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
        cnapi.api_fetch(word, allow_cache=False, _force_allow=True, limit=50)


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

    #cache_path = os.path.join(basepath, 'cache')
    #set_global_root(cache_path)
    #loop_data = dict(socket_uri=socket_uri, cache_path=cache_path)
    #ask_loop()
    # queue, procs = loop.init_thread(**loop_data)


def _base_boot(socket_uri="ws://127.0.0.1:8009"):
    basepath = os.path.abspath(os.path.dirname(__file__))
    cache_path = os.path.join(basepath, 'cache')
    #set_global_root(cache_path)


COMMAND_STR = '!#'


def ask_loop(callback):
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
            assess_string(v, callback)
        if kill is True:
            _run = False
            log('Killing processes')
            loop.kill_processes()
    log('Finish askloop')



def assess_string(sentence, success_callback=None):
    '''
    Given an input string, token and assess each token.
    '''
    if sentence[0] in COMMAND_STR:
        return command.command_mode(sentence)
    log('primary_functions assess_string')

    if queue is not None:
        queue.put_nowait(sentence)

    if success_callback is not None:
        success_callback(sentence)
    # return secondary_functions.apply_to_context(sentence)
