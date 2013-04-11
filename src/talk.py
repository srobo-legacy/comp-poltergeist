
import socket
import sys
import yaml

import config

_soc = None

def _get_connection():
    global _soc
    if _soc is None:
        _soc = socket.socket()
        _soc.connect(('localhost', config.control_port))
        back = _soc.recv(7)
        assert back == "Hello!\n", "Failed to establish connection (got '{0}')".format(back)
    return _soc

def command(cmd):
    soc = _get_connection()
    if cmd[-1] != "\n": cmd += "\n"
    soc.send(cmd)
    data = ''
    while True:
        back = soc.recv(256)
        data += back
        if len(back) < 256:
            break
    return data

def command_yaml(cmd):
    cmd += ' --yaml'
    raw_data = command(cmd)
    data = yaml.load(raw_data)
    return data
