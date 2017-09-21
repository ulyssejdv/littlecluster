import json
import sys
import requests
from urllib import request


def call_srv(host, port):
    response = requests.get("http://{0}:{1}".format(host, port))
    return response.status_code, response.text

def main(host, port):
    response_code = 404
    content = None
    retries = 0
    while response_code is not 200 and retries <= 5:
        print("try on : {0}:{1}".format(host, port))
        response_code, content = call_srv(host=host, port=port)
        if response_code is not 200:
            json_response = json.loads(content)
            port = json_response['port']
            host = json_response['host']
            retries += 1
    print(content)
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])