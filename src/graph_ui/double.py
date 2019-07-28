"""Using flask to expose the main entry point as it makes it easier to
expose an input thread.
Individual threads will boot manually or attached through manual setup
"""
# from multiprocessing import Process, Queue
import flask
from flask import Flask, render_template
from flask import jsonify
import requests
import os
import sys

import argparse

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMPORT_PATH =  os.path.normpath(os.path.join(BASE_PATH, '..'))


parser = argparse.ArgumentParser(description='Double call.')
parser.add_argument('-p', '--port', default=9005, help='Server port')
#parser.add_argument('--table', default='assertions', help='Alternative (DB) table name')

cli_args = parser.parse_args()

# sys.path.append(IMPORT_PATH)

# from database import graph
# import database
#from database import db

# gdb = None
# udb = None
app = Flask(__name__)

def main():
    app.run(
        debug=True,
        host='127.0.0.1',
        port=cli_args.port,
    )


# @app.before_first_request
# def initialize():
#     global gdb
#     global udb
    #p = cli_args.path
    #print('Opening Graph.', cli_args.table, p)
    #gdb = graph.GraphDB(directory=p, name=cli_args.table)
    #print('Opening Persistant Local')
    #udb = db.AppendableDB(directory=SERVER_DB_PATH, name='inputs')
    #print('DB Open {} {}'.format(gdb, udb))


@app.route('/word/<word>/')
@app.route('/word/<path:word>/<int:limit>')
def get_word(word, limit=False):

    if limit is False:
        limit = 50
    path = f"word/{word}/{limit}"
    jsons = get_requests(path)
    key = tuple(jsons.values())[0]['key']

    print('merge', len(jsons))
    # merge two.
    result = dict(limit=limit, key=key, word=word)
    for name, _json in jsons.items():
        result[name] = _json['edges']


    return jsonify(result)

# def get_from_db(word):
#     gp = gdb.pick(word)
#     text_edges = gp.edge_text(True)
#     items = sorted(gp.edge_list(), reverse=True)
#     limit_c = None
#     if limit is not False:
#         limit_c = 50
#         if isinstance(limit, int):
#             limit_c = limit

#     if limit_c is not None and limit_c != 0:
#         items = items[:limit_c]
#     else:
#         limit_c = len(items)

#     text_edges = graph.Edges(items=items)._text_list(True)
#     key = gp.key
#     result = dict(limit=limit_c, edges=text_edges, key=key, word=word)
#     return jsonify(result)


ENDPOINTS = [
    ('rev', "http://127.0.0.1:8889",),
    ('edges', "http://127.0.0.1:9000",),
]


def get_requests(url):
    # perform and merge the request for all resources
    items = {}
    for name, part in ENDPOINTS:
        path = f"{part}/{url}"
        print('Fetch', path)
        res = requests.get(path)
        if res.ok:
            items[name] = res.json()
            continue
        print('Error with', path, res)
    return items


@app.route("/")
def index_page():
    return render_template('index.html',)


@app.route("/table")
def table_page():
    return render_template('table.html',)


if __name__ == '__main__':
    main()
