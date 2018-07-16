"""Using flask to expose the main entry point as it makes it easier to
expose an input thread.
Individual threads will boot manually or attached through manual setup
"""
# from multiprocessing import Process, Queue
import flask
from flask import Flask, render_template
from flask import jsonify
import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMPORT_PATH =  os.path.normpath(os.path.join(BASE_PATH, '..'))
DB_PATH = "E:/conceptnet/_lmdb_assertions/"
SERVER_DB_PATH = "E:/conceptnet/_lmdb_server_ui/"


sys.path.append(IMPORT_PATH)

from database import graph
import database
from database import db

gdb = None
udb = None
app = Flask(__name__)


@app.before_first_request
def initialize():
    global gdb
    global udb
    print('Opening Graph.')
    gdb = graph.GraphDB( directory=DB_PATH, name='assertions')
    print('Opening Persistant Local')
    udb = db.AppendableDB(directory=SERVER_DB_PATH, name='inputs')
    print('DB Open {} {}'.format(gdb, udb))

def main():
    app.run(
        debug=True,
        host='127.0.0.1',
        port=9000,
    )


@app.route('/word/<word>/')
@app.route('/word/<path:word>/<int:limit>')
def get_word(word, limit=False):
    gp = gdb.pick(word)
    text_edges = gp.edge_text(True)
    items = sorted(gp.edge_list(), reverse=True)
    limit_c = None
    if limit is not False:
        limit_c = 50
        if isinstance(limit, int):
            limit_c = limit

    if limit_c is not None and limit_c != 0:
        items = items[:limit_c]
    else:
        limit_c = len(items)

    text_edges = graph.Edges(items=items)._text_list(True)
    key = gp.key
    result = dict(limit=limit_c, edges=text_edges, key=key, word=word)
    return jsonify(result)


@app.route("/")
def index_page():

    return render_template('index.html',)


if __name__ == '__main__':
    main()
