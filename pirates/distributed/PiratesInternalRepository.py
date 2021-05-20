from panda3d.core import Datagram
from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from otp.distributed.OtpDoGlobals import *
from PiratesNetMessengerAI import PiratesNetMessengerAI
from pirates.ai.AnalyticsManagerAI import AnalyticsManagerAI
from SplunkThreadAI import SplunkThreadAI
from Queue import Queue
import collections, urlparse, traceback, sys

class PiratesInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_PIRATES
    dbId = 1101

    def __init__(self, baseChannel, serverId=None, dcFileNames=None,
                 dcSuffix='AI', connectMethod=None, threadedNet=None):
        if connectMethod is None:
            connectMethod = self.CM_NATIVE
        AstronInternalRepository.__init__(
            self, baseChannel, serverId=serverId, dcFileNames=dcFileNames,
            dcSuffix=dcSuffix, connectMethod=connectMethod, threadedNet=threadedNet)

    def __mongoMissing(self):
        self.notify.warning('The usage of MongoDB is highly recommended. Please switch as soon as possible.')

    def handleConnected(self):
        self.splunkEnabled = config.GetBool('want-splunk', False)
        self.netMessenger = PiratesNetMessengerAI(self)
        self.logQueue = Queue()
        self.analyticsMgr = AnalyticsManagerAI()
        
        try:
            import pymongo
        except:
            self.notify.warning("Couldn't find pymongo package!")
            self.__mongoMissing()
            return

        mongoUrl = config.GetString('mongodb-url', '')
        
        if not mongoUrl:
            self.__mongoMissing()
            return

        db = (urlparse.urlparse(mongoUrl).path or '/porgame')[1:]

        self.dbConn = pymongo.MongoClient(mongoUrl)
        self.database = self.dbConn[db]
        self.dbGlobalCursor = self.database.porGame
        self.dbAstronCursor = self.database.astron
        
        self.logThreads = []
        
        if self.splunkEnabled:
            for i in xrange(4):
                thread = SplunkThreadAI()
                thread.daemon = True
                thread.start()
                self.logThreads.append(thread)

        self.notify.info('Connected to MongoDB.')
    
    def hasMongo(self):
        return hasattr(self, 'database')

    def getAvatarIdFromSender(self):
        return int(self.getMsgSender() & 0xFFFFFFFF)

    def getAccountIdFromSender(self):
        return int((self.getMsgSender() >> 32) & 0xFFFFFFFF)

    def systemMessage(self, message, channel):
        msgDg = PyDatagram()
        msgDg.addUint16(6)
        msgDg.addString(message)

        dg = PyDatagram()
        dg.addServerHeader(channel, self.ourChannel, CLIENTAGENT_SEND_DATAGRAM)
        dg.addString(msgDg.getMessage())
        self.send(dg)

    def systemMsgAll(self, message):
        self.systemMessage(message, 10)

    def getApiKey(self):
        try:
            f = open('../deployment/site/api.key', 'rb')
            key = f.read()
            f.close()

            return key.strip()

        except:
            return 'dev'

    def prepareMessage(self, message, sentArgs=[]):
        return self.netMessenger.prepare(message, sentArgs)

    def sendNetEvent(self, message, sentArgs=[]):
        self.netMessenger.send(message, sentArgs)

    def handleDatagram(self, di):
        msgType = self.getMsgType()

        if msgType == self.netMessenger.msgType:
            self.netMessenger.handle(msgType, di)
            return

        AstronInternalRepository.handleDatagram(self, di)

    def claimOwnership(self, channelId):
        datagram = PyDatagram()
        datagram.addServerHeader(channelId, self.ourChannel,
                                 STATESERVER_OBJECT_SET_AI)
        datagram.addChannel(self.ourChannel)
        self.send(datagram)

    def _isValidPlayerLocation(self, parentId, zoneId):
        parent = self.doId2do.get(parentId)
        if not parent:
            return False

        if hasattr(parent, 'isValidZone'):
            return parent.isValidZone(zoneId)

        return True

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
        except SystemExit, KeyboardInterrupt:
            raise
        except Exception as e:
            if self.getAvatarIdFromSender() > 100000000:
                dg = PyDatagram()
                dg.addServerHeader(self.getMsgSender(), self.ourChannel, CLIENTAGENT_EJECT)
                dg.addUint16(166)
                dg.addString('You were disconnected to prevent a district reset.')
                self.send(dg)

            self.writeServerEvent('INTERNAL-EXCEPTION', avId=self.getAvatarIdFromSender(), accountId=self.getAccountIdFromSender(),
                                  exception=traceback.format_exc())
            self.notify.warning('INTERNAL-EXCEPTION: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
            print traceback.format_exc()
            sys.exc_clear()

        return 1
    
    def writeServerEvent(self, logType, **kwargs):
        if self.splunkEnabled:
            log = collections.OrderedDict()
            log['type'] = logType
            log['sender'] = self.eventLogId
            log.update(kwargs)
            self.logQueue.put(log)
        else:
            AstronInternalRepository.writeServerEvent(self, logType, **kwargs)
    
    def getObjectsOfExactClass(self, objClass):
        return {doId: do for doId, do in self.doId2do.items() if do.__class__ == objClass}
    
    def getObjectsOfClass(self, objClass):
        return {doId: do for doId, do in self.doId2do.items() if isinstance(do, objClass)}