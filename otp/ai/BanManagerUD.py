from panda3d.core import Datagram
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from otp.distributed import OtpDoGlobals
from pirates.uberdog.ClientServicesManagerUD import RemoteAccountDB
import time

class RetrieveBannerBase(object):

    def enterRetrieveBanner(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.bannerId, self.handleRetrieveBanner)

    def handleRetrieveBanner(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Banner object was not found in the database!')
            return

        self.bannerName = fields['setName'][0]
        self.banner = '%s (%s)' % (self.bannerName, self.bannerId)
        self.demand('RetrieveAccount')

class BanBase(object):

    def enterRetrieveAccount(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.accountId, self.handleRetrieveAccount)

    def handleRetrieveAccount(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['AccountUD']:
            self.demand('Error', 'Banner object was not found in the database!')
            return
        
        self.targetUsername = fields['ACCOUNT_ID']
        self.demand('Ban')
    
    def enterBan(self):
        self.mgr.air.csm.accountDB.getBannedStatus(self.targetUsername, self.duration, self.handleBannedAccount)
    
    def kickAvatar(self):
        dg = PyDatagram()
        dg.addServerHeader(self.mgr.air.csm.GetPuppetConnectionChannel(self.avId), self.mgr.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(152)
        dg.addString(self.banReason)
        self.mgr.air.send(dg)

class BanFSM(RetrieveBannerBase, BanBase, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanFSM')
    
    def __init__(self, mgr):
        FSM.__init__(self, 'BanFSM')
        self.mgr = mgr
        
    def enterStart(self, bannerId, avId, accountId, duration, banReason):
        self.bannerId = bannerId
        self.avId = avId
        self.accountId = accountId
        self.duration = duration
        self.banReason = banReason
        self.demand('RetrieveBanner')
    
    def handleBannedAccount(self, success, error):
        self.kickAvatar()
        self.mgr.banCallback(self, success, error)
    
    def enterError(self, error):
        self.mgr.banCallback(self, False, error)

class BanAIFSM(BanBase, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanFSM')
    
    def __init__(self, mgr):
        FSM.__init__(self, 'BanFSM')
        self.mgr = mgr
        
    def enterStart(self, avId, accountId, duration, banReason):
        self.avId = avId
        self.accountId = accountId
        self.duration = duration
        self.banReason = banReason
        self.demand('RetrieveAccount')
    
    def handleBannedAccount(self, success, error):
        self.kickAvatar()
        self.mgr.banAICallback(self, success, error)

    def enterError(self, error):
        self.mgr.banAICallback(self, False, error)

class MuteFSM(RetrieveBannerBase, BanBase, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('MuteFSM')
    
    def __init__(self, mgr):
        FSM.__init__(self, 'MuteFSM')
        self.mgr = mgr
        
    def enterStart(self, bannerId, avId, accountId, duration):
        self.bannerId = bannerId
        self.avId = avId
        self.accountId = accountId
        self.duration = duration
        self.demand('RetrieveBanner')

    def enterBan(self):
        if self.duration in xrange(2):
            seconds = self.duration
        else:
            seconds = int(time.time()) + (3600 * self.duration)

        dclassA = self.mgr.air.dclassesByName['AccountUD']
        dclassP = self.mgr.air.dclassesByName['DistributedPlayerPirateUD']
        self.mgr.air.send(dclassA.aiFormatUpdate('MUTED_UNTIL', self.accountId, self.accountId, self.mgr.air.ourChannel, seconds))
        self.mgr.air.send(dclassP.aiFormatUpdate('setMutedUntil', self.avId, self.avId, self.mgr.air.ourChannel, [seconds]))
        self.mgr.muteCallback(self, None)
    
    def enterError(self, error):
        self.mgr.muteCallback(self, error)

class BanManagerUD(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerUD')

    def __init__(self, air):
        self.air = air
        self.accept('BANMGR_ban', self.banUD)
        self.accept('BANMGR_banAI', self.banAI)
        self.accept('BANMGR_mute', self.muteUD)

    def banUD(self, bannerId, avId, accountId, duration, banReason):
        BanFSM(self).demand('Start', bannerId, avId, accountId, duration, banReason)
    
    def banAI(self, avId, accountId, duration, banReason):
        BanAIFSM(self).demand('Start', avId, accountId, duration, banReason)
    
    def muteUD(self, bannerId, avId, accountId, duration):
        MuteFSM(self).demand('Start', bannerId, avId, accountId, duration)
    
    def banCallback(self, fsm, success, error):            
        avId = self.air.csm.GetPuppetConnectionChannel(fsm.bannerId)

        if not success:
            # Better notify the banner
            msg = 'Failed to ban: %s' % error
            self.air.systemMessage(msg, avId)
            self.notify.warning(msg)
            return

        msg = '%s banned %s for %s hours: %s' % (fsm.banner, fsm.targetUsername, fsm.duration, fsm.banReason)
        
        if fsm.duration:
            self.air.systemMessage('You banned %s for %s hours!' % (fsm.targetUsername, fsm.duration), avId)
        else:
            self.air.systemMessage('You terminated %s!' % fsm.targetUsername, avId)

        self.notify.info(msg)
        self.air.writeServerEvent('banned', accountId=fsm.accountId, username=fsm.targetUsername, moreInfo=msg)
    
    def banAICallback(self, fsm, success, error):
        if not success:
            self.notify.warning('Failed to ban with AI: %s' % error)
            return
        
        if fsm.duration:
            msg = 'AI banned %s for %s hours: %s' % (fsm.targetUsername, fsm.duration, fsm.banReason)
        else:
            msg = 'AI terminated %s: %s' % (fsm.targetUsername, fsm.banReason)
        
        self.notify.info(msg)
        self.air.writeServerEvent('banned-ai', accountId=fsm.accountId, username=fsm.targetUsername, moreInfo=msg)
    
    def muteCallback(self, fsm, error):
        avId = self.air.csm.GetPuppetConnectionChannel(fsm.bannerId)
        
        if error:
            msg = 'Failed to mute: %s' % error
            self.air.systemMessage(msg, avId)
            self.notify.warning(msg)
            return
        
        if fsm.duration == 1:
            msg = '%s muted %s for forever' % (fsm.banner, fsm.targetUsername)
            self.air.systemMessage('You muted %s forever!' % fsm.targetUsername, avId)
        elif fsm.duration == 0:
            msg = '%s unmuted %s' % (fsm.banner, fsm.targetUsername)
            self.air.systemMessage('You unmuted %s!' % fsm.targetUsername, avId)
        else:
            msg = '%s muted %s for %s hours' % (fsm.banner, fsm.targetUsername, fsm.duration)
            self.air.systemMessage('You muted %s for %s hours!' % (fsm.targetUsername, fsm.duration), avId)
        
        self.notify.info(msg)
        self.air.writeServerEvent('muted', accountId=fsm.accountId, username=fsm.targetUsername, moreInfo=msg)