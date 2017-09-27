import json
import sys
from queue import Queue
from random import randint

from flask import Flask
from flask import request

from multicast import Multicast

app = Flask(__name__)
me = {
    "host": "",
    "port": ""
}

server_list = Queue()

@app.route("/")
def hello():
    if randint(0, 1):
        return json.dumps({
            "msg": "hello world",
            "srv": request.host
        })
    else:
        return get_serv_who_is_not_me(), 302

def get_serv_who_is_not_me():
    ele = server_list.get(randint(0, server_list.qsize()))
    server_list.put(ele)
    return ele


def main(args):
    me['host'] = args[0]
    me['port'] = args[1]
    multicast = Multicast(srv_q=server_list)
    multicast.send("{0}:{1}".format(me['host'], me['port']))
    multicast.start()
    app.run(port=me['port'])



if __name__ == '__main__':
    main(sys.argv[1:])
