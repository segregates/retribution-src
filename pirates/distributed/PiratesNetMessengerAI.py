from panda3d.core import Datagram
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject
import cPickle, zlib

class PiratesNetMessengerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesNetMessengerAI')

    def __init__(self, air, msgChannel=17800, msgType=42069):
        self.air = air
        self.air.registerForChannel(msgChannel)
        self.msgChannel = msgChannel
        self.msgType = msgType

    def prepare(self, message, sentArgs=[]):
        dg = PyDatagram()
        dg.addServerHeader(self.msgChannel, self.air.ourChannel, self.msgType)
        dg.addString(message)
        dg.addString(zlib.compress(cPickle.dumps(sentArgs)))
        return dg

    def send(self, message, sentArgs=[]):
        self.notify.debug('sendNetEvent: %s %r' % (message, sentArgs))
        dg = self.prepare(message, sentArgs)
        self.air.send(dg)

    def handle(self, msgType, di):
        message = di.getString()
        data = zlib.decompress(di.getString())
        sentArgs = cPickle.loads(data)
        messenger.send(message, sentArgs)
