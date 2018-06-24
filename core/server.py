"""Using flask to expose the main entry point as it makes it easier to
expose an input thread.
Individual threads will boot manually or attached through manual setup
"""
from multiprocessing import Process, Queue
import flask
from flask import Flask

from core.run import run_core, thread_run
from log import log

app = Flask(__name__)
global_prc = None
proc_q = None


def main():
    app.run(
        debug=True,
        host='127.0.0.1',
        port=9000,
    )


def proc_start():
    global global_prc
    global proc_q

    if global_prc is not None:
        return global_prc

    options = {}

    global_prc, proc_q = thread_run(proc_q, options)

    return global_prc


def proc_stop():
    global global_prc
    if global_prc is None:
        return True
    proc_q.put_nowait('kill')
    log('sent kill command, waiting for death.')
    global_prc.join()
    log('Stop complete')
    global_prc = None
    return True


@app.route("/start")
def start():
    proc_start()
    return "Run main thread!"


@app.route("/")
def index_page():
    proc_start()
    return "first page. Welcome."


@app.route('/put/<sentence>')
def put_string(sentence):
    proc_q.put(sentence)
    return sentence


@app.route("/stop")
def stop():
    proc_stop()
    return "kill thread"

if __name__ == '__main__':
    main()
