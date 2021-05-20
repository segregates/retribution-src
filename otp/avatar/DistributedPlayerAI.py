from panda3d.core import Notify
from otp.ai.AIBaseGlobal import *
from otp.avatar import DistributedAvatarAI
from otp.avatar import PlayerBase
from otp.distributed.ClsendTracker import ClsendTracker
from otp.otpbase import OTPGlobals
from otp.ai.MagicWordGlobal import *

class DistributedPlayerAI(DistributedAvatarAI.DistributedAvatarAI, PlayerBase.PlayerBase, ClsendTracker):

    def __init__(self, air):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        PlayerBase.PlayerBase.__init__(self)
        ClsendTracker.__init__(self)
        self.friendsList = []
        self.ignoredPlayers = []
        self.DISLid = 0
        self.adminAccess = 0

    def announceGenerate(self):
        DistributedAvatarAI.DistributedAvatarAI.announceGenerate(self)
        ClsendTracker.announceGenerate(self)
        self._doPlayerEnter()

    def _announceArrival(self):
        self.sendUpdate('arrivedOnDistrict', [self.air.districtId])

    def _announceExit(self):
        self.sendUpdate('arrivedOnDistrict', [0])

    def _sendExitServerEvent(self):
        self.air.writeServerEvent('avatarExit', avId=self.doId)

    def delete(self):
        self._doPlayerExit()
        ClsendTracker.destroy(self)
        DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def isPlayerControlled(self):
        return True

    def setLocation(self, parentId, zoneId):
        DistributedAvatarAI.DistributedAvatarAI.setLocation(self, parentId, zoneId)
        if self.isPlayerControlled():
            if not self.air._isValidPlayerLocation(parentId, zoneId):
                self.notify.info('booting player %s for doing setLocation to (%s, %s)' % (self.doId, parentId, zoneId))
                self.air.writeServerEvent('suspicious', avId=self.doId, messae='invalid setLocation: (%s, %s)' % (parentId, zoneId))
                self.requestDelete()

    def _doPlayerEnter(self):
        self.incrementPopulation()
        self._announceArrival()

    def _doPlayerExit(self):
        self._announceExit()
        self.decrementPopulation()

    def incrementPopulation(self):
        self.air.incrementPopulation(self)

    def decrementPopulation(self):
        simbase.air.decrementPopulation(self)

    def d_setSystemMessage(self, aboutId, chatString):
        self.sendUpdate('setSystemMessage', [aboutId, chatString])

    def d_setCommonChatFlags(self, flags):
        self.sendUpdate('setCommonChatFlags', [flags])

    def setCommonChatFlags(self, flags):
        pass

    def d_friendsNotify(self, avId, status):
        self.sendUpdate('friendsNotify', [avId, status])

    def friendsNotify(self, avId, status):
        pass

    def setAccountName(self, accountName):
        self.accountName = accountName

    def getAccountName(self):
        return self.accountName

    def setDISLid(self, id):
        self.DISLid = id

    def setAdminAccess(self, access):
        self.adminAccess = access

    def getAdminAccess(self):
        return self.adminAccess
    
    def d_setTalk(self, message):
        self.sendUpdate('setTalk', [message])
    
    def d_setTalkFrom(self, avId, channel, message):
        self.sendUpdate('setTalkFrom', [avId, channel, message])

    def d_setFriendsList(self, friendsList):
        self.sendUpdate('setFriendsList', [friendsList])

    def setFriendsList(self, friendsList):
        self.friendsList = friendsList

    def getFriendsList(self):
        return self.friendsList
    
    def isFriend(self, doId):
        return doId in self.friendsList

    def extendFriendsList(self, friendId):
        if friendId in self.friendsList:
            return

        self.friendsList.append(friendId)
        self.d_setFriendsList(self.friendsList)

    def d_setIgnoredPlayers(self, ignoredPlayers):
        self.sendUpdate('setIgnoredPlayers', [ignoredPlayers])
    
    def setIgnoredPlayers(self, ignoredPlayers):
        self.ignoredPlayers = ignoredPlayers
    
    def b_setIgnoredPlayers(self, ignoredPlayers):
        self.setIgnoredPlayers(ignoredPlayers)
        self.d_setIgnoredPlayers(ignoredPlayers)
    
    def getIgnoredPlayers(self):
        return self.ignoredPlayers

@magicWord(CATEGORY_MODERATION)
def accId():
    """Get the accountId from the target player."""
    accountId = spellbook.getTarget().DISLid
    return "%s has the accountId of %d" % (spellbook.getTarget().getName(), accountId)

@magicWord(CATEGORY_GAME_MASTER)
def setName(nameStr):
    spellbook.getTarget().b_setName(nameStr)
    return 'Name set to %s' % nameStr
