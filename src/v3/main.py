'''A set of functions to call into the API - defined as 'primary' as the
first point of access
'''
import os
# import contextnet_api as cnapi
#from logger import print_edges
import words

from cache import set_global_root
import cli
import primary_context as pc
#import loop
import contextnet_api as ca
from json_socket import make_socket
#from log import log

queue = None
loop_data = None


def main():
    init()

SOCKET_ADDRESS = 'ws://127.0.0.1:8009'

def init(socket_uri=SOCKET_ADDRESS):
    '''
    A initialisztion function for anything requiring a first boot.
    '''
    print('init')
    global command
    global loop_data
    global queue
    # global socket
    # if socket_uri is not None:
    #     socket = make_socket(socket_uri)
    #command = Command()
    basepath = os.path.abspath(os.path.dirname(__file__))
    cache_path = os.path.join(basepath, '..', 'cache')
    cache_path = os.path.abspath(cache_path)
    set_global_root(cache_path)
    loop_data = dict(socket_uri=socket_uri, cache_path=cache_path)
    pc.init(socket_uri)
    cli.init(socket_uri)
    cli.ask_loop(assess_string)


def assess_string(string):
    """Run the context functionality on the given string sentence.
    """
    tok = pc.apply_to_context(string)
    print('\n\n', string, '==', tok)

    #queue, procs = loop.init_thread(**loop_data)

"""
Goal preferences

When repeating a sentence in cotext, the importance can be derived from the
repetition itself
when a graphs node is sufficentialy weighted - it's the new
goal or knowledge

Graphing:

    i need my house
    where is my home
    where is my house
    My home now

contextual graphing notes a heavier weight to the 'need', 'my', house', 'home'

"""

if __name__ == '__main__':
    main()
