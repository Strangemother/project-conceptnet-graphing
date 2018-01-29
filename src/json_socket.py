import websocket

import json
import collections

class JSONSetEncoder(json.JSONEncoder):
    """Use with json.dumps to allow Python sets to be encoded to JSON

    Example
    -------

    import json

    data = dict(aset=set([1,2,3]))

    encoded = json.dumps(data, cls=JSONSetEncoder)
    decoded = json.loads(encoded, object_hook=json_as_python_set)
    assert data == decoded     # Should assert successfully

    Any object that is matched by isinstance(obj, collections.Set) will
    be encoded, but the decoded value will always be a normal Python set.

    """

    def default(self, obj):
        if isinstance(obj, collections.Set):
            return list(obj)
            # return dict(_set_object=list(obj))
        else:
            return json.JSONEncoder.default(self, obj)

def json_as_python_set(dct):
    """Decode json {'_set_object': [1,2,3]} to set([1,2,3])

    Example
    -------
    decoded = json.loads(encoded, object_hook=json_as_python_set)

    Also see :class:`JSONSetEncoder`

    """
    if '_set_object' in dct:
        return set(dct['_set_object'])
    return dct

class DummySocket(object):
    '''
    Dummy socket for replacement of the real socket, if the socket
    does not exist. All output is sent to print.
    '''
    def send(*a):
        print a

socket = DummySocket()


def send_json(d=None, **data):
    '''
    Send dictionary data through the socket, converting all given arguments
    to a JSON string before send.
    '''
    if isinstance(d, dict) is False:
        d = dict(value=d)

    if len(data) != 0:
        d.update(data)
    socket.send(json.dumps(d, cls=JSONSetEncoder))


def make_socket(uri):
    '''
    Generate and return a new WebSocket client for the given uri.
    '''
    global socket
    socket = websocket.WebSocket()
    socket.connect(uri)
    socket.send('Connected')
    return socket

