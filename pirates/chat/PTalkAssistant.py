from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.speedchat import SCDecoders
from otp.chat.ChatGlobals import *
from otp.chat.TalkGlobals import *
from otp.speedchat import SpeedChatGlobals
from otp.chat.TalkMessage import TalkMessage
from otp.chat.TalkAssistant import TalkAssistant
from pirates.speedchat import PSCDecoders
from pirates.chat.PiratesTalkGlobals import CANNON_DEFENSE
import random, sys

class PTalkAssistant(TalkAssistant):
    notify = DirectNotifyGlobal.directNotify.newCategory('PTalkAssistant')

    def __init__(self):
        TalkAssistant.__init__(self)
        self.SCDecoder = PSCDecoders

    def clearHistory(self):
        TalkAssistant.clearHistory(self)
        self.historyParty = []
        self.historyPVP = []
        self.labelParty = OTPLocalizer.TalkParty
        self.labelPVP = OTPLocalizer.TalkPVP

    def checkShipPVPTypedChat(self):
        if not hasattr(localAvatar.ship, 'getSiegeTeam'):
            return False

        if localAvatar.ship.getSiegeTeam():
            return True

        return False

    def checkShipPVPSpeedChat(self):
        if not hasattr(localAvatar.ship, 'getSiegeTeam'):
            return False

        if localAvatar.ship.getSiegeTeam():
            return True

        return False

    def checkPartyTypedChat(self):
        if localAvatar.bandMember:
            return True

        return False

    def checkPartySpeedChat(self):
        if localAvatar.bandMember:
            return True

        return False

    def executeSlashCommand(self, text):
        words = text[1:].split(' ')
        comm = words[0].lower()
        argStr = ' '.join(words[1:])

        if comm in ('afk', 'away'):
            localAvatar.toggleAFK()
        elif comm in PLocalizer.EmoteCommands.keys():
            emoteCode = PLocalizer.EmoteCommands[comm]
            if type(emoteCode) == type((0,)):
                emoteCode = random.choice(emoteCode)

            messenger.send(SpeedChatGlobals.SCEmoteMsgEvent, [
                emoteCode])
        elif comm == 'quit':
            sys.exit(0)
        elif comm in ('lfc', 'lfg', 'lookingforcrew'):
            localAvatar.toggleLookingForCrewSign()
        elif comm in ('code', 'redeemcode'):
            localAvatar.submitCodeToServer(argStr)
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeSubmitting % argStr)
        elif comm in ('holiday', 'holidays', 'holidaylist', 'event'):
            base.cr.newsManager.displayHolidayStatus()
        elif comm in ('x2', 'x2bonus'):
            timeRemain = localAvatar.getTempDoubleXPReward()
            if timeRemain:
                timeRemain = int(timeRemain)
                (minutes, seconds) = divmod(timeRemain, 60)
                (hours, minutes) = divmod(minutes, 60)
                base.talkAssistant.receiveGameMessage(PLocalizer.TEMP_DOUBLE_REP_CHAT % (hours, minutes))
            else:
                base.talkAssistant.receiveGameMessage(PLocalizer.NO_TEMP_DOUBLE_REP)
        elif comm == 'crewhud':
            localAvatar.guiMgr.crewHUD.toggleHUD()
        elif comm == 'time':
            messenger.send('requestServerTime')

    def receiveOpenTalk(self, avatarId, avatarName, message, gameMaster):
        if not avatarName and avatarId:
            avatarName = self.findName(avatarId, 0)

        messageType = TALK_GM if gameMaster else TALK_OPEN
        newMessage = TalkMessage(messageType, self.countMessage(), message, avatarId, avatarName)
        self.addToHistory(newMessage)

    def receivePartyTalk(self, fromAv, avatarName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_PARTY, self.countMessage(), message, fromAv, avatarName)
            self.addToHistory(newMessage)

    def receiveOpenSpeedChat(self, msgType, messageIndex, senderId, name, gameMaster):
        messageType = TALK_GM if gameMaster else TALK_OPEN
        message = None

        if msgType == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif msgType == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
            if not message:
                if senderId == localAvatar.doId:
                    message = PLocalizer.EmoteMessagesSelf.get(messageIndex)
                    messageType = INFO_OPEN
                else:
                    message = PLocalizer.EmoteMessagesThirdPerson.get(messageIndex)
                    messageType = INFO_OPEN

        elif msgType == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)

        if message in (None, ''):
            return None

        newMessage = TalkMessage(messageType, self.countMessage(), message, senderId, name)
        self.addToHistory(newMessage)

    def receiveSystemMessage(self, message):
        base.localAvatar.guiMgr.messageStack.addTextMessage(message, seconds = 20, priority = 0, color = (0.5, 0, 0, 1), icon = ('admin', ''))

    def receivePartyMessage(self, senderId, senderName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_PARTY, self.countMessage(), message, senderId, senderName)
            self.addToHistory(newMessage)

    def receiveShipPVPMessage(self, senderId, senderName, teamName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_PVP, self.countMessage(), message, fromAv, avatarName, extraInfo=teamName)
            self.addToHistory(newMessage)

    def sendPartyTalk(self, message):
        if self.checkPartyTypedChat():
            localAvatar.bandMember.sendTalk(0, 0, '', message, 0, 0)

    def sendShipPVPCrewTalk(self, message):
        if self.checkShipPVPTypedChat():
            base.cr.distributedDistrict.siegeManager.sendTalk(message)

    def sendSCQuestChat(self, msgType, questInt, taskNum):
        messenger.send(SCQuestEvent)
        messenger.send('chatUpdateSCQuest', [
            questInt,
            msgType,
            taskNum])

    def sendPartySpeedChat(self, type, msgIndex):
        if self.checkPartySpeedChat():
            localAvatar.bandMember.b_setSpeedChat(msgIndex)

    def sendPartySCQuestChat(self, msgType, questInt, taskNum):
        if self.checkPartySpeedChat():
            localAvatar.bandMember.b_setSCQuestChat(questInt, msgType, taskNum)

    def sendGuildSCQuestChat(self, msgType, questInt, taskNum):
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSCQuest(questInt, msgType, taskNum)

    def sendShipPVPCrewSpeedChat(self, type, msgIndex):
        if self.checkShipPVPSpeedChat():
            base.cr.distributedDistrict.siegeManager.sendSC(msgIndex)

    def sendShipPVPCrewSCQuestChat(self, msgType, questInt, taskNum):
        if self.checkShipPVPSpeedChat():
            base.cr.distributedDistrict.siegeManager.sendSCQuest(msgType, questInt, taskNum)

    def sendAvatarWhisperQuestSpeedChat(self, questInt, msgType, taskNum, receiverId):
        base.localAvatar.whisperSCQuestTo(questInt, msgType, taskNum, receiverId)
        message = PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum)

        if self.logWhispers:
            receiverName = self.findName(receiverId, 0)
            newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, localAvatar.doId, localAvatar.getName(), receiverId, receiverName)
            self.addToHistory(newMessage)

    def receiveCannonDefenseMessage(self, senderId, senderName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(CANNON_DEFENSE, self.countMessage(), message, senderId, senderName, localAvatar.doId, localAvatar.getName())
            self.addToHistory(newMessage)
