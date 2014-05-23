"""

Created by: Nathan Starkweather
Created on: 05/23/2014
Created in: PyCharm Community Edition

Dummy server for dumb dumbs do not ever use!
"""
from socket import socket, timeout
from select import select

__author__ = 'Nathan Starkweather'


class _ServerClient():

    """ @type sock: socket"""
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr

    def fileno(self):
        return self.sock.fileno()


def reloadserver():
    import sys
    for m in 'server', 'hello.server':
        try:
            del sys.modules[m]
        except KeyError:
            pass
    g = sys.modules['__main__'].__dict__
    exec("from hello.server import *", g, g)


class Server():
    def __init__(self, host='', port=12345, listen=5, timeout=5):
        sock = socket()
        sock.bind((host, port))
        sock.listen(listen)
        sock.settimeout(timeout)

        self.sock = sock
        self.clients = []
        self.recv_buf = bytearray()

    def accept(self):
        try:
            con, addr = self.sock.accept()
        except timeout:
            print("Got no new connections")
        else:
            print("Got new connection:", con, addr)
            client = _ServerClient(con, addr)
            self.clients.append(client)

    def readall(self):
        readable, writeable, ex = select(self.clients, [], [])
        for s in readable:
            rv = s.recv(4096).decode()
            print("Got message from", s)
            print(rv)

    def recv_msg(self, sock, sentinel):

        buf = self.recv_buf
        spos = endpos = 0
        recv = sock.recv
        slen = len(sentinel)

        while True:
            try:
                chnk = recv(4096)
            except timeout:
                continue

            buf.extend(chnk)
            endpos = buf.find(sentinel, spos)

            if endpos > -1:
                break

            spos = len(buf) - slen - 1
            if spos < 0:
                spos = 0

        msg = buf[:endpos]

        if endpos + slen <= len(buf):
            self.recv_buf = buf[endpos + slen:]
        else:
            self.recv_buf.clear()

        return msg
