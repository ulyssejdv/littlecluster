import json
import socket
import sqlite3
from random import randint

import sys
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
        return json.dumps({
            "msg": "hello world",
            "srv": request.host
        })
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
    try:
        selected = rows[randint(0, len(rows)-1)]
        next = {
            "port": selected[1],
            "host": selected[0]
        }
    except:
        next = {
            "port": None,
            "host": None
        }
    return json.dumps(next)

def main(host, port):
    me['host'] = host
    me['port'] = port
    add_srv_properties_to_db(host=me['host'], port=me['port'])
    app.run(port=me['port'])

if __name__ == '__main__':
    me['host'] = sys.argv[1]
    me['port'] = sys.argv[2]

    print(sys.argv[0])
    main(me['host'], me['port'])
