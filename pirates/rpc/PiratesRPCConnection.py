from panda3d.core import Connection
from direct.directnotify.DirectNotifyGlobal import *
from direct.fsm.FSM import *


import asynchat
import httplib
import time
import json
import sys

class PiratesRPCConnection(asynchat.async_chat, FSM):
    notify = directNotify.newCategory('PiratesRPCConnection')

    def __init__(self, sock, server):
        asynchat.async_chat.__init__(self, sock=sock)
        FSM.__init__(self, 'RPCConnection')

        self.server = server
        self.air = self.server.handler.air

        self.data = ''
        self.found_terminator = lambda: None

        self.path = ''
        self.headers = {}
        self.id = None
        self.timeout = None
        self.__gotResp = False
        self.__method = ''
        self.__params = ''

        self.demand('ReadHeaders')

    def collect_incoming_data(self, data):
        self.data += data

    def handle_close(self):
        self.demand('Off')
        asynchat.async_chat.handle_close(self)

    def enterReadHeaders(self):
        self.data = ''
        self.set_terminator('\r\n\r\n')
        self.found_terminator = self.__got_headers

    def __got_headers(self):
        self.set_terminator(None)

        for i, line in enumerate(self.data.split('\n')):
            line = line.rstrip('\r')

            if i == 0:
                request = line.split(' ')
                if len(request) != 3:
                    return self.demand('HTTPError', 400)

                method, _, version = tuple(request)

                if method != 'POST':
                    return self.demand('HTTPError', 501)

                if version not in ('HTTP/1.0', 'HTTP/1.1'):
                    return self.demand('HTTPError', 505)

            else:
                header = line.split(': ')
                if len(header) != 2:
                    return self.demand('HTTPError', 400)

                key, value = tuple(header)
                self.headers[key.lower()] = value

        self.demand('ReceiveData')

    def enterReceiveData(self):
        length = self.headers.get('content-length', '')
        if not length or not length.isdigit():
            return self.demand('HTTPError', 400)

        length = int(length)

        self.data = ''
        self.set_terminator(length)
        self.found_terminator = self.__got_post
        self.setTimeout(None)

    def __got_post(self):
        self.set_terminator(None)

        try:
            request = json.loads(self.data)

        except ValueError:
            return self.demand('JSONError', -32700, 'Parse error')

        if 'method' not in request or 'params' not in request:
            return self.demand('JSONError', -32600, 'Invalid Request')

        self.id = request.get('id')

        if not isinstance(request['method'], basestring) or \
           not isinstance(request['params'], (tuple, list, dict)):
            return self.demand('JSONError', -32600, 'Invalid Request')

        if request['method'] == 'listCommands':
            method = self.server.handler.listCommands
            params = {}

        else:
            method = getattr(self.server.handler, 'rpc_' + str(request['method']), None)
            params = request['params']
            if not method:
                return self.demand('JSONError', -32601, 'Method not found')

            token = None
            if isinstance(request['params'], dict):
                token = request['params'].pop('token', None)

            elif len(request['params']) > 0:
                token = request['params'].pop(0)

            if not isinstance(token, basestring):
                token = None

            error = self.server.handler.authenticate(token, method)
            if error is not None:
                self.demand('JSONError', *error)
                return

        self.__method = method.func_name
        self.__params = json.dumps(params)

        try:
            if isinstance(params, dict):
                method(self.__callback, **params)

            else:
                method(self.__callback, *params)

        except:
            self.demand('JSONError', -1, describeException())

        if not self.__gotResp:
            self.setTimeout(20)

    def __callback(self, result):
        if self.__gotResp:
            return

        if self.state == 'Off':
            return

        self.__gotResp = True
        self.air.writeServerEvent('rpc_result', method=self.__method, params=self.__params, result=json.dumps(result))
        self.sendJSON({'jsonrpc': '2.0', 'result': result, 'id': self.id})
        self.demand('Off')

    def enterOff(self):
        self.setTimeout(None)
        self.close_when_done()

    def setTimeout(self, timeout):
        if self.timeout is not None:
            self.timeout.remove()

        if timeout is not None:
            self.timeout = taskMgr.doMethodLater(timeout, self.demand,
                                                 'RPCConnection-timeout-%d' % id(self),
                                                 extraArgs=['Off'])

    def sendResponse(self, body, contentType=None, code=200):
        description = httplib.responses.get(code, 'Code %d' % code)

        response =  'HTTP/1.1 %d %s\r\n' % (code, description)
        response += 'Date: %s\r\n' % time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        response += 'Server: Pirates-RPCServer/1.0\r\n'
        response += 'Content-Length: %d\r\n' % len(body)
        if contentType:
            response += 'Content-Type: %s\r\n' % contentType

        response += 'Connection: close\r\n'
        response += '\r\n' + body
        self.push(response)

        self.demand('Off')

    def sendJSON(self, data):
        body = json.dumps(data) + '\n'
        self.sendResponse(body, 'application/json', 200)

    def enterHTTPError(self, code):
        self.air.writeServerEvent('rpc_http_error', code=code)
        description = httplib.responses.get(code, 'Code %d' % code)
        self.sendResponse('%d %s\n' % (code, description),
                          'text/plain', code)

    def enterJSONError(self, code, message):
        self.air.writeServerEvent('rpc_json_error', code=code)

        response = {'jsonrpc': '2.0',
                    'error': {'code': code,
                              'message': message},
                    'id': self.id}

        self.sendJSON(response)
