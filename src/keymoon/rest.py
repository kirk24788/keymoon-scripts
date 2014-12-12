# -*- coding: utf-8 -*-
import urllib2
import json

BASE_URL="http://localhost:9000/api/"
ERROR_HEADER = "X-Keymoon-Error"

__OPENER = urllib2.build_opener(urllib2.HTTPHandler)

class KeymoonError(Exception):
    def __init__(self, error):
        super(KeymoonError, self).__init__(error.hdrs.getheader(ERROR_HEADER))

def __without_data(path, method, as_json=False):
    try:
        url = BASE_URL + path.lstrip("/")
        request = urllib2.Request(url)
        request.get_method = lambda: method
        data = __OPENER.open(request).read()
        return json.loads(data) if as_json else data
    except urllib2.HTTPError, error:
        raise KeymoonError(error)

def __with_data(path, method, data=None, json_data=None, as_json=False):
    try:
        url = BASE_URL + path.lstrip("/")
        if json_data:
            request = urllib2.Request(url, data=json.dumps(json_data))
            request.add_header('Content-Type', 'application/json')
        else:
            if data:
                request = urllib2.Request(url, data=data)
                pass
            else:
                request = urllib2.Request(url)
        request.get_method = lambda: method
        recv_data = __OPENER.open(request).read()
        return json.loads(recv_data) if as_json else recv_data
    except urllib2.HTTPError, error:
        raise KeymoonError(error)


def get(path, as_json=False):
    return __without_data(path, "GET", as_json)

def delete(path, as_json=False):
    return __without_data(path, "DELETE", as_json)

def post(path, data=None, json_data=None, as_json=False):
    return __with_data(path, "POST", data, json_data, as_json)

def put(path, data=None, json_data=None, as_json=False):
    return __with_data(path, "PUT", data, json_data, as_json)
