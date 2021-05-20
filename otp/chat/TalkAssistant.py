from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.speedchat import SCDecoders
from otp.chat.TalkMessage import TalkMessage
from otp.chat.TalkGlobals import *
from otp.chat.ChatGlobals import *
from otp.nametag.NametagConstants import CFSpeech, CFTimeout, CFThought
ThoughtPrefix = '.'

class TalkAssistant(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TalkAssistant')

    def __init__(self):
        self.logWhispers = 1
        self.clearHistory()
        self.lastWhisper = None
        self.SCDecoder = SCDecoders
        self.accept('friendOnline', self.__friendOnline)
        self.accept('friendOffline', self.__friendOffline)

    def clearHistory(self):
        self.historyComplete = []
        self.messageCount = 0

    def delete(self):
        self.ignoreAll()
        self.clearHistory()

    def start(self):
        pass

    def stop(self):
        pass

    def countMessage(self):
        self.messageCount += 1
        return self.messageCount - 1

    def getCompleteText(self, numLines, startPoint = 0):
        return self.historyComplete[startPoint:startPoint + numLines]

    def getCompleteTextFromRecent(self, numLines, startPoint = 0):
        start = len(self.historyComplete) - startPoint
        if start < 0:
            start = 0
        backStart = max(start - numLines, 0)
        text = self.historyComplete[backStart:start]
        text.reverse()
        return text

    def getAllCompleteText(self):
        return self.historyComplete

    def getSizeCompleteText(self):
        return len(self.historyComplete)

    def addToHistory(self, message, doId=None):
        if message.getTalkType() == TALK_WHISPER and doId != localAvatar.doId:
            self.lastWhisper = doId
        
        self.historyComplete.append(message)
        messenger.send('NewOpenMessage', [message])

    def findName(self, id, isPlayer = 0):
        return self.findAvatarName(id)

    def findAvatarName(self, id):
        info = base.cr.identifyAvatar(id)
        if info:
            return info.getName()
        else:
            return ''

    def executeSlashCommand(self, text):
        pass

    def isThought(self, message):
        if not message:
            return 0
        elif len(message) == 0:
            return 0
        elif message.find(ThoughtPrefix, 0, len(ThoughtPrefix)) >= 0:
            return 1
        else:
            return 0

    def removeThoughtPrefix(self, message):
        if self.isThought(message):
            return message[len(ThoughtPrefix):]
        else:
            return message

    def checkOpenSpeedChat(self):
        return True

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def checkGuildTypedChat(self):
        if localAvatar.guildId:
            return True
        return False

    def checkGuildSpeedChat(self):
        if localAvatar.guildId:
            return True
        return False

    def receiveWhisperTalk(self, avatarId, avatarName, message):
        if not avatarName and avatarId:
            avatarName = self.findAvatarName(avatarId)

        newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, avatarId, avatarName)
 
        if avatarId:
            self.addToHistory(newMessage, avatarId)

    def receiveGuildTalk(self, senderAvId, avatarName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_GUILD, self.countMessage(), message, senderAvId, avatarName)
            self.addToHistory(newMessage, senderAvId)

    def receiveThought(self, avatarId, avatarName, message):
        if not avatarName and avatarId:
            avatarName = self.findAvatarName(avatarId)

        newMessage = TalkMessage(AVATAR_THOUGHT, self.countMessage(), message, avatarId, avatarName)
        self.addToHistory(newMessage, avatarId)

    def receiveGameMessage(self, message):
        if not self.isThought(message):
            newMessage = TalkMessage(INFO_GAME, self.countMessage(), message, receiverAvatarId=localAvatar.doId, receiverAvatarName=localAvatar.getName())
            self.addToHistory(newMessage)

    def addSystemMessage(self, message):
        if not self.isThought(message):
            newMessage = TalkMessage(INFO_SYSTEM, self.countMessage(), message, receiverAvatarId=localAvatar.doId, receiverAvatarName=localAvatar.getName())
            self.addToHistory(newMessage)

    def receiveGuildMessage(self, senderId, senderName, message):
        if not self.isThought(message):
            newMessage = TalkMessage(TALK_GUILD, self.countMessage(), message, senderId, senderName)
            self.addToHistory(newMessage)

    def receiveGuildUpdateMessage(self, message, senderId, senderName, receiverId, receiverName, extraInfo = None):
        if not self.isThought(message):
            newMessage = TalkMessage(INFO_GUILD, self.countMessage(), message, senderId, senderName, receiverId, receiverName, extraInfo)
            self.addToHistory(newMessage)

    def receiveFriendUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline
        else:
            onlineMessage = OTPLocalizer.FriendOffline
        newMessage = TalkMessage(UPDATE_FRIEND, self.countMessage(), onlineMessage, friendId, friendName, localAvatar.doId, localAvatar.getName())
        self.addToHistory(newMessage)

    def receiveGuildUpdate(self, memberId, memberName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.GuildMemberOnline
        else:
            onlineMessage = OTPLocalizer.GuildMemberOffline
        newMessage = TalkMessage(UPDATE_GUILD, self.countMessage(), onlineMessage, memberId, memberName)
        self.addToHistory(newMessage)

    def receiveAvatarWhisperSpeedChat(self, type, messageIndex, senderAvId, name = None):
        if not name and senderAvId:
            name = self.findName(senderAvId, 0)

        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)

        newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, senderAvId, name, localAvatar.doId, localAvatar.getName())
        self.addToHistory(newMessage, senderAvId)

    def sendOpenTalk(self, message):
        try:
            message.encode('ascii')
        except UnicodeEncodeError:
            base.talkAssistant.receiveGameMessage("Non-ASCII messages are not permitted.")
            return

        if base.cr.wantMagicWords and len(message) > 0 and message[0] == '~':
            messenger.send('magicWord', [message])
        else:
            base.cr.chatAgent.sendChatMessage(message)

    def sendWhisperTalk(self, message, receiverAvId, history=True):
        # This is Pirates specific... which goes against all things OTP. But oh well.
        # Route through the PFMUD.
        if base.localAvatar.isMuted():
            base.localAvatar.sendMuteWarning()
        else:
            if history:
                self.addWhisperToHistory(receiverAvId, message)

            base.cr.piratesFriendsManager.sendUpdate('sendTalkWhisper', [receiverAvId, message])

    def sendGuildTalk(self, message):
        if self.checkGuildTypedChat():
            if base.localAvatar.isMuted():
                base.localAvatar.sendMuteWarning()
            else:
                base.cr.guildManager.sendTalk(message)

    def sendOpenSpeedChat(self, type, messageIndex):
        if type == SPEEDCHAT_NORMAL:
            messenger.send(SCChatEvent)
            messenger.send('chatUpdateSC', [messageIndex])
            base.localAvatar.b_setSC(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            messenger.send('chatUpdateSCEmote', [messageIndex])
            messenger.send(SCEmoteChatEvent)
            base.localAvatar.b_setSCEmote(messageIndex)
        elif type == SPEEDCHAT_CUSTOM:
            messenger.send('chatUpdateSCCustom', [messageIndex])
            messenger.send(SCCustomChatEvent)
            base.localAvatar.b_setSCCustom(messageIndex)

    def addWhisperToHistory(self, receiverId, message):
        if not self.logWhispers:
            return
        
        avatarName = ''
        avatar = base.cr.identifyAvatar(receiverId)
        if avatar:
            avatarName = avatar.getName()
        newMessage = TalkMessage(TALK_WHISPER, self.countMessage(), message, localAvatar.doId, localAvatar.getName(), receiverId, avatarName)
        self.addToHistory(newMessage)
    
    def sendAvatarWhisperSpeedChat(self, type, messageIndex, receiverId):
        if type == SPEEDCHAT_NORMAL:
            base.localAvatar.whisperSCTo(messageIndex, receiverId)
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            base.localAvatar.whisperSCEmoteTo(messageIndex, receiverId)
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, localAvatar.getName())
        elif type == SPEEDCHAT_CUSTOM:
            base.localAvatar.whisperSCCustomTo(messageIndex, receiverId)
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)

        self.addWhisperToHistory(receiverId, message)

    def sendGuildSpeedChat(self, type, msgIndex):
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSC(msgIndex)

    def getWhisperReplyId(self):
        if self.lastWhisper:
            return self.lastWhisper

        return 0
    
    def __friendOnline(self, doId, name):
        self.receiveFriendUpdate(doId, name, True)
    
    def __friendOffline(self, doId, name):
        self.receiveFriendUpdate(doId, name, False)
