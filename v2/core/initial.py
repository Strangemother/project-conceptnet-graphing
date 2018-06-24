'''The initial layer for all input to apply.
'''
import time
import Queue as Q

from log import log


def run_core(queue, config):
    ''' Run the process '''
    log('run')
    run = 1
    config = config or {}

    # uri = config.get('socket_uri', None)
    # socket = _json_socket(uri)
    # socket.send("run_core")
    # pf.init()

    while run:
        m = None
        try:
            m = queue.get_nowait()
            log('Got message', m)
        except Q.Empty as e:
            pass

        if m == 'kill':
            log('kill run_core')
            run = 0

        if m is None:
            time.sleep(1)
            continue

        # Any message to this point came from websocket(through queue) or
        # queue internal
        log('assess', m)
        assess_string(m)

    log('End run core.')

def assess_string(sentence):
    '''Given an input string, farm to the waiting receivers'''
    log('Read "{}"'.format(sentence))

