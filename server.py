import socket
import sqlite3
from random import randint

import sys

import signal
from flask import Flask
from flask import request

app = Flask(__name__)
me = {
    "host": "",
    "port": ""
}

@app.route("/")
def hello():
    if randint(0, 1):
        return "Hello World! running on : {}".format(
            request.host
        )
    else:
        return get_serv_who_is_not_me(), 302

def add_srv_properties_to_db(host, port):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute(
        "INSERT INTO servers(host,port) VALUES (?, ?)",
        (host, port)
    )
    conn.commit()
    conn.close()

def get_serv_who_is_not_me():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    rows = c.execute(
        "SELECT * FROM servers WHERE NOT (port = ? AND host = ?)",
        (me['port'], me['host'],)
    ).fetchall()
    conn.close()
    selected = rows[randint(0, len(rows)-1)]
    return str({"port": selected[1], "host": selected[0]})
    
def get_running_properties():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    me['host'] = sock.getsockname()[0]
    me['port'] = sock.getsockname()[1]
    sock.close()

if __name__ == '__main__':
    get_running_properties()
    add_srv_properties_to_db(host=me['host'],port=me['port'])
    app.run(port=me['port'])
