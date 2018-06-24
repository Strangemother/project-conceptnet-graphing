
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

    # prfs.assess_string('hello')
    prfs.ask_loop()



if __name__ == '__main__':
    main()
