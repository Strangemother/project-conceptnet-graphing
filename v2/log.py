import logging


logging.basicConfig(level=logging.DEBUG)

def log(*a):
    logging.info(' '.join(map(str, a)))

warn = logging.warn
