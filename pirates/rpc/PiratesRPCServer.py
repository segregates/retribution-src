from panda3d.core import Connection
from direct.directnotify.DirectNotifyGlobal import *
from PiratesRPCConnection import PiratesRPCConnection
import urlparse
import asyncore
import socket

class PiratesRPCServer(asyncore.dispatcher):
    notify = directNotify.newCategory('PiratesRPCServer')

    def __init__(self, endpoint, handler):
        asyncore.dispatcher.__init__(self)

        self.handler = handler

        url = urlparse.urlparse(endpoint)
        hostname = url.hostname
        port = url.port or 8080

        if hostname is None:
            return

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((hostname, port))
        self.listen(5)

        taskMgr.add(self.task, 'PiratesRPCServer')

    def task(self, task):
        asyncore.loop(timeout=.002, count=5)
        return task.cont

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        sock, addr = pair
        PiratesRPCConnection(sock, self)
