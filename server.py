import socket
from random import randint

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    # random error response
    if randint(0, 1):
        return "Hello World! running on : {}".format(
            request.host
        )
    else:
        return "302"


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    # Permet de lancer l'app flask sur un port libre au pif
    app.run(port=port)