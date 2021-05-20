from panda3d.core import Notify
from otp.margins.WhisperPopup import WhisperPopup
from otp.nametag.NametagConstants import CFQuicktalker, CFPageButton, CFQuitButton, CFSpeech, CFThought, CFTimeout
from otp.chat import ChatGarbler
import string
from direct.task import Task
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from direct.showbase import PythonUtil
from otp.avatar import DistributedAvatar
import time
from otp.avatar import Avatar, PlayerBase
from otp.chat import TalkAssistant
from otp.otpbase import OTPGlobals
from otp.avatar.Avatar import teleportNotify
from otp.distributed.TelemetryLimited import TelemetryLimited
from otp.ai.MagicWordGlobal import *
from otp.chat.ChatGarbler import ChatGarbler

class DistributedPlayer(DistributedAvatar.DistributedAvatar, PlayerBase.PlayerBase, TelemetryLimited, ChatGarbler):
    TeleportFailureTimeout = 60.0

    def __init__(self, cr):
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        PlayerBase.PlayerBase.__init__(self)
        TelemetryLimited.__init__(self)
        self.__teleportAvailable = 0
        self.inventory = None
        self.experience = None
        self.friendsList = []
        self.ignoredPlayers = []
        self.oldFriendsList = None
        self.timeFriendsListChanged = None
        self.lastFailedTeleportMessage = {}
        self._districtWeAreGeneratedOn = None
        self.DISLid = 0
        self.adminAccess = 0
        self.autoRun = 0
        self.isConfused = False
        self.online = True

    @staticmethod
    def GetPlayerGenerateEvent():
        return 'DistributedPlayerGenerateEvent'

    @staticmethod
    def GetPlayerNetworkDeleteEvent():
        return 'DistributedPlayerNetworkDeleteEvent'

    @staticmethod
    def GetPlayerDeleteEvent():
        return 'DistributedPlayerDeleteEvent'

    def networkDelete(self):
        DistributedAvatar.DistributedAvatar.networkDelete(self)
        messenger.send(self.GetPlayerNetworkDeleteEvent(), [self])

    def disable(self):
        DistributedAvatar.DistributedAvatar.disable(self)
        messenger.send(self.GetPlayerDeleteEvent(), [self])

    def delete(self):
        try:
            self.DistributedPlayer_deleted
        except:
            self.DistributedPlayer_deleted = 1
            del self.experience
            if self.inventory:
                self.inventory.unload()
            del self.inventory
            DistributedAvatar.DistributedAvatar.delete(self)

    def generate(self):
        DistributedAvatar.DistributedAvatar.generate(self)

    def announceGenerate(self):
        DistributedAvatar.DistributedAvatar.announceGenerate(self)
        messenger.lock.release()
        messenger.send(self.GetPlayerGenerateEvent(), [self])

    def setLocation(self, parentId, zoneId):
        DistributedAvatar.DistributedAvatar.setLocation(self, parentId, zoneId)

    def isGeneratedOnDistrict(self, districtId = None):
        if districtId is None:
            return self._districtWeAreGeneratedOn is not None
        else:
            return self._districtWeAreGeneratedOn == districtId
        return

    def getArrivedOnDistrictEvent(self, districtId = None):
        if districtId is None:
            return 'arrivedOnDistrict'
        else:
            return 'arrivedOnDistrict-%s' % districtId
        return

    def arrivedOnDistrict(self, districtId):
        curFrameTime = globalClock.getFrameTime()
        if hasattr(self, 'frameTimeWeArrivedOnDistrict') and curFrameTime == self.frameTimeWeArrivedOnDistrict:
            if districtId == 0 and self._districtWeAreGeneratedOn:
                self.notify.warning('ignoring arrivedOnDistrict 0, since arrivedOnDistrict %d occured on the same frame' % self._districtWeAreGeneratedOn)
                return
        self._districtWeAreGeneratedOn = districtId
        self.frameTimeWeArrivedOnDistrict = globalClock.getFrameTime()
        messenger.send(self.getArrivedOnDistrictEvent(districtId))
        messenger.send(self.getArrivedOnDistrictEvent())

    def setLeftDistrict(self):
        self._districtWeAreGeneratedOn = None
    
    def isOnline(self):
        return True

    def hasParentingRules(self):
        if self is localAvatar:
            return True

    def setAccountName(self, accountName):
        self.accountName = accountName

    def setSystemMessage(self, aboutId, chatString):
        base.talkAssistant.receiveSystemMessage(chatString)

       
    def displayWhisper(self, fromId, chatString, whisperType):
        print 'Whisper type %s from %s: %s' % (whisperType, fromId, chatString)

    def whisperSCTo(self, msgIndex, sendToId):
        if sendToId not in base.cr.doId2do:
            messenger.send('wakeup')
            base.cr.piratesFriendsManager.d_whisperSCTo(sendToId, msgIndex)
        else:
            messenger.send('wakeup')
            self.sendUpdate('setWhisperSCFrom', [self.doId, msgIndex], sendToId)

    def setWhisperSCFrom(self, fromId, msgIndex):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.localAvatar.isIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, fromId)
        return

    def whisperSCCustomTo(self, msgIndex, sendToId):
        if sendToId not in base.cr.doId2do:
            messenger.send('wakeup')
            base.cr.piratesFriendsManager.d_whisperSCCustomTo(sendToId, msgIndex)
            return
        messenger.send('wakeup')
        self.sendUpdate('setWhisperSCCustomFrom', [self.doId, msgIndex], sendToId)

    def _isValidWhisperSource(self, source):
        return True

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if not self._isValidWhisperSource(handle):
            self.notify.warning('displayWhisper from non-toon %s' % fromId)
            return
        if base.localAvatar.isIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_CUSTOM, msgIndex, fromId)

    def whisperSCEmoteTo(self, emoteId, sendToId):
        if sendToId not in base.cr.doId2do:
            messenger.send('wakeup')
            base.cr.piratesFriendsManager.d_whisperSCEmoteTo(sendToId, emoteId)
            return
        messenger.send('wakeup')
        self.sendUpdate('setWhisperSCEmoteFrom', [self.doId, emoteId], sendToId)

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.localAvatar.isIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCEmoteWhisperMsg(emoteId, handle.getName())
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTEmote)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_EMOTE, emoteId, fromId)

    def d_setWhisperIgnored(self, sendToId):
        base.talkAssistant.sendWhisperTalk(OTPLocalizer.WhisperIgnored, sendToId, False)

    def setChatAbsolute(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        DistributedAvatar.DistributedAvatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)

    def setTalk(self, chat):
        if not base.cr.chatAgent.verifyMessage(chat):
            return
        if base.localAvatar.isIgnored(self.doId):
            return
        if not self.understandable:
            chat = self.garble(len(chat.split(' ')))
        elif base.whiteList and self.understandable < 2:
            chat = base.whiteList.processThroughAll(chat, self)

        self.displayTalk(chat)
        
        if base.talkAssistant.isThought(chat):
            chat = base.talkAssistant.removeThoughtPrefix(chat)
            base.talkAssistant.receiveThought(self.doId, self.getName(), chat)
        else:
            base.talkAssistant.receiveOpenTalk(self.doId, self.getName(), chat, self.hasGMChat())
    
    def setTalkFrom(self, avId, channel, chat):
        av = self.cr.doId2do.get(avId)
        
        if (not av) or not hasattr(av, 'nametag'):
            return

        av.nametag.setSpecialColor(OTPGlobals.CHAT_CHANNEL_COLORS[channel])
        av.setTalk(chat)
        av.nametag.setSpecialColor(None)

    def setTalkWhisper(self, fromAV, avatarName, chat):
        if base.whiteList:
            chat = base.whiteList.processThroughAll(chat, base.chatGarbler)

        self.displayTalkWhisper(fromAV, avatarName, chat)

    def displayTalkWhisper(self, fromId, avatarName, chatString):
        print 'TalkWhisper from %s: %s' % (fromId, chatString)

    def hasGMChat(self):
        return False
    
    def b_setSC(self, msgIndex):
        self.setSC(msgIndex)
        self.d_setSC(msgIndex)

    def d_setSC(self, msgIndex):
        messenger.send('wakeup')
        self.sendUpdate('setSC', [msgIndex])

    def setSC(self, msgIndex):
        if base.localAvatar.isIgnored(self.doId):
            return
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout, quiet=1)
        base.talkAssistant.receiveOpenSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, self.doId, self.getName(), self.hasGMChat())

    def b_setSCCustom(self, msgIndex):
        self.setSCCustom(msgIndex)
        self.d_setSCCustom(msgIndex)

    def d_setSCCustom(self, msgIndex):
        messenger.send('wakeup')
        self.sendUpdate('setSCCustom', [msgIndex])

    def setSCCustom(self, msgIndex):
        if base.localAvatar.isIgnored(self.doId):
            return
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)
        base.talkAssistant.receiveOpenSpeedChat(TalkAssistant.SPEEDCHAT_CUSTOM, msgIndex, self.doId, self.getName(), self.hasGMChat())

    def b_setSCEmote(self, emoteId):
        self.b_setEmoteState(emoteId, animMultiplier=self.animMultiplier)

    def d_friendsNotify(self, avId, status):
        self.sendUpdate('friendsNotify', [avId, status])

    def friendsNotify(self, avId, status):
        avatar = base.cr.identifyFriend(avId)
        if avatar != None:
            if status == 1:
                self.setSystemMessage(avId, OTPLocalizer.WhisperNoLongerFriend % avatar.getName())
            elif status == 2:
                self.setSystemMessage(avId, OTPLocalizer.WhisperNowSpecialFriend % avatar.getName())
        return

    def d_teleportQuery(self, requesterId, sendToId = None):
        if sendToId in base.cr.doId2do:
            teleportNotify.debug('sending teleportQuery%s' % ((requesterId, sendToId),))
            self.sendUpdate('teleportQuery', [requesterId], sendToId)
        else:
            teleportNotify.debug('sending TTRFM teleportQuery%s' % ((requesterId, sendToId),))
            base.cr.piratesFriendsManager.d_teleportQuery(sendToId)

    def teleportQuery(self, requesterId):
        teleportNotify.debug('receieved teleportQuery(%s)' % requesterId)
        avatar = base.cr.identifyFriend(requesterId)
        if avatar != None:
            teleportNotify.debug('avatar is not None')
            if base.localAvatar.isIgnored(requesterId):
                teleportNotify.debug('avatar ignored')
                self.d_teleportResponse(self.doId, 2, 0, 0, 0, sendToId=requesterId)
                return
            if hasattr(base, 'distributedParty'):
                if base.distributedParty.partyInfo.isPrivate:
                    if requesterId not in base.distributedParty.inviteeIds:
                        teleportNotify.debug('avatar not in inviteeIds')
                        self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId=requesterId)
                        return
                if base.distributedParty.isPartyEnding:
                    teleportNotify.debug('party is ending')
                    self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId=requesterId)
                    return
            if self.__teleportAvailable and not self.ghostMode and config.GetBool('can-be-teleported-to', 1):
                teleportNotify.debug('teleport initiation successful')
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperComingToVisit % avatar.getName())
                messenger.send('teleportQuery', [avatar, self])
                return
            teleportNotify.debug('teleport initiation failed')
            if self.failedTeleportMessageOk(requesterId):
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperFailedVisit % avatar.getName())
        teleportNotify.debug('sending try-again-later message')
        self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId=requesterId)
        return

    def failedTeleportMessageOk(self, fromId):
        now = globalClock.getFrameTime()
        lastTime = self.lastFailedTeleportMessage.get(fromId, None)
        if lastTime != None:
            elapsed = now - lastTime
            if elapsed < self.TeleportFailureTimeout:
                return 0
        self.lastFailedTeleportMessage[fromId] = now
        return 1

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId, sendToId = None):
        teleportNotify.debug('sending teleportResponse%s' % ((avId,
          available,
          shardId,
          hoodId,
          zoneId,
          sendToId),))
        self.sendUpdate('teleportResponse', [avId,
         available,
         shardId,
         hoodId,
         zoneId], sendToId)

    def teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        teleportNotify.debug('received teleportResponse%s' % ((avId,
          available,
          shardId,
          hoodId,
          zoneId),))
        messenger.send('teleportResponse', [avId,
         available,
         shardId,
         hoodId,
         zoneId])

    def d_teleportGiveup(self, requesterId, sendToId = None):
        teleportNotify.debug('sending teleportGiveup(%s) to %s' % (requesterId, sendToId))
        self.sendUpdate('teleportGiveup', [requesterId], sendToId)

    def teleportGiveup(self, requesterId):
        teleportNotify.debug('received teleportGiveup(%s)' % (requesterId,))
        avatar = base.cr.identifyAvatar(requesterId)
        if not self._isValidWhisperSource(avatar):
            self.notify.warning('teleportGiveup from non-toon %s' % requesterId)
            return
        if avatar != None:
            self.setSystemMessage(requesterId, OTPLocalizer.WhisperGiveupVisit % avatar.getName())
        return

    def b_teleportGreeting(self, avId):
        self.d_teleportGreeting(avId)
        self.teleportGreeting(avId)

    def d_teleportGreeting(self, avId):
        self.sendUpdate('teleportGreeting', [avId])

    def teleportGreeting(self, avId):
        avatar = base.cr.getDo(avId)
        if isinstance(avatar, Avatar.Avatar):
            self.setChatAbsolute(OTPLocalizer.TeleportGreeting % avatar.getName(), CFSpeech | CFTimeout)
        elif avatar is not None:
            self.notify.warning('got teleportGreeting from %s referencing non-toon %s' % (self.doId, avId))
        return

    def setTeleportAvailable(self, available):
        self.__teleportAvailable = available

    def getTeleportAvailable(self):
        return self.__teleportAvailable

    def getFriendsList(self):
        return self.friendsList

    def setFriendsList(self, friendsList):
        self.oldFriendsList = self.friendsList
        self.friendsList = friendsList
        self.timeFriendsListChanged = globalClock.getFrameTime()
        messenger.send('friendsListChanged')
        Avatar.reconsiderAllUnderstandable()
    
    def isFriend(self, doId):
        return doId in self.friendsList

    def setDISLid(self, id):
        self.DISLid = id

    def setAdminAccess(self, access):
        self.adminAccess = access
        if self.isLocal():
            self.cr.wantMagicWords = self.adminAccess >= MINIMUM_MAGICWORD_ACCESS

    def getAdminAccess(self):
        return self.adminAccess

    def setAutoRun(self, value):
        self.autoRun = value

    def getAutoRun(self):
        return self.autoRun
    
    def d_setIgnoredPlayers(self, ignoredPlayers):
        self.sendUpdate('setIgnoredPlayers', [ignoredPlayers])
    
    def setIgnoredPlayers(self, ignoredPlayers):
        self.ignoredPlayers = ignoredPlayers
    
    def b_setIgnoredPlayers(self, ignoredPlayers):
        self.setIgnoredPlayers(ignoredPlayers)
        self.d_setIgnoredPlayers(ignoredPlayers)
    
    def getIgnoredPlayers(self):
        return self.ignoredPlayers
    
    def isIgnored(self, doId):
        return doId in self.ignoredPlayers
    
    def addIgnore(self, doId):
        if doId in self.ignoredPlayers:
            return
        
        self.ignoredPlayers.append(doId)
        self.d_setIgnoredPlayers(self.ignoredPlayers)
        messenger.send('AvatarIgnoreChange')   
    
    def removeIgnore(self, doId):
        if doId not in self.ignoredPlayers:
            return
        
        self.ignoredPlayers.remove(doId)
        self.d_setIgnoredPlayers(self.ignoredPlayers)
        messenger.send('AvatarIgnoreChange')   
