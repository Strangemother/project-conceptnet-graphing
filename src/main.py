
import os
# from autocorrect import spell
from pprint import pprint

from json_socket import make_socket
import primary_functions as prfs
import contextnet_api as cnapi
from typemap import type_map
import cache
import time
# def main():
#     cnapi.read_assertions()
command = None
def main():
    '''
    Open the client websocket and target the ask() loop.
    '''
    prfs.init(socket_uri="ws://127.0.0.1:8009")
    global command
    command = Command()
    # prfs.assess_string('hello')
    ask_loop()


COMMAND_STR = '!#'

def ask_loop():
    loop = True

    while loop is True:
        v = raw_input('\nWhat?: ')
        if v == '':
            print 'Close loop'
            loop = False
        else:
            if v[0] in COMMAND_STR:
                command.command_mode(v)
                continue
            prfs.assess_string(v)


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
        print 'Received command "{}"'.format(mc), name

        if hasattr(self, name):
            return getattr(self, name)(com)

    def com_eval(self, com):
        ret = eval(com)
        print ret
        return ret


    def com_hash(self, com):
        coms = map(str.strip, com.strip().split(' '))

        com0 = coms[0]

        name = "hash_{}".format(com0)

        if hasattr(self, name):
            return getattr(self, name)(*coms[1:])

    def hash_fetch(self, value=None):
        positive = ['true', 'yes', '1', 'on']
        negative = ['no', '0', 'false', 'off']
        lv =None
        if value is not None:
            lv = value.lower()
        switch = True if lv in positive else None
        switch = switch or (False if lv in negative else None)

        if switch is None:
            print 'Fetch is currently:', prfs.allow_external()
            return

        print 'Allow external data fetch: ', switch
        prfs.allow_external(switch)

    def hash_delete(self, word):
        print 'Delete word', word
        print cache.delete_word(word)

    def hash_cache(self, word):
        cnapi.api_fetch(word, allow_cache=False)


    def hash_read(self, data_file):
        '''given the name of a data file within the initial data folder, read each
        line into the ask loop.
        '''
        fn = '{}'.format(data_file)
        fpf = os.path.join(os.path.dirname(__file__), 'data', fn)
        print 'read', fpf

        if os.path.isfile(fpf):
            print 'Slow reading', fpf
            ts = 5
            with open(fpf, 'r') as stream:
                try:
                    for line in stream:
                        word = line.strip()
                        print 'Asking', word
                        prfs.assess_string(word)
                        print 'sleeping', ts
                        time.sleep(ts)
                except KeyboardInterrupt:
                    print 'cancelled slow feed'


if __name__ == '__main__':
    main()
