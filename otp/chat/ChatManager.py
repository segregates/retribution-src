import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
ChatEvent = 'ChatEvent'
NormalChatEvent = 'NormalChatEvent'
SCChatEvent = 'SCChatEvent'
SCCustomChatEvent = 'SCCustomChatEvent'
SCEmoteChatEvent = 'SCEmoteChatEvent'
OnScreen = 0
OffScreen = 1
Thought = 2
ThoughtPrefix = '.'

def isThought(message):
    if len(message) == 0:
        return 0
    elif message.find(ThoughtPrefix, 0, len(ThoughtPrefix)) >= 0:
        return 1
    else:
        return 0


def removeThoughtPrefix(message):
    if isThought(message):
        return message[len(ThoughtPrefix):]
    else:
        return message


class ChatManager(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatManager')

    def __init__(self, cr, localAvatar):
        self.cr = cr
        self.localAvatar = localAvatar
        self.wantBackgroundFocus = 1
        self.__scObscured = 0
        self.__normalObscured = 0
        self.openChatWarning = None
        self.noSecretChatAtAll = None
        self.noSecretChatAtAllAndNoWhitelist = None
        self.noSecretChatWarning = None
        self.fsm = ClassicFSM.ClassicFSM('chatManager', [State.State('off', self.enterOff, self.exitOff),
         State.State('mainMenu', self.enterMainMenu, self.exitMainMenu),
         State.State('speedChat', self.enterSpeedChat, self.exitSpeedChat),
         State.State('normalChat', self.enterNormalChat, self.exitNormalChat),
         State.State('whisper', self.enterWhisper, self.exitWhisper),
         State.State('whisperChat', self.enterWhisperChat, self.exitWhisperChat),
         State.State('whisperSpeedChat', self.enterWhisperSpeedChat, self.exitWhisperSpeedChat),
         State.State('openChatWarning', self.enterOpenChatWarning, self.exitOpenChatWarning),
         State.State('noSecretChatAtAll', self.enterNoSecretChatAtAll, self.exitNoSecretChatAtAll),
         State.State('noSecretChatAtAllAndNoWhitelist', self.enterNoSecretChatAtAllAndNoWhitelist, self.exitNoSecretChatAtAllAndNoWhitelist),
         State.State('noSecretChatWarning', self.enterNoSecretChatWarning, self.exitNoSecretChatWarning),
         State.State('noFriendsWarning', self.enterNoFriendsWarning, self.exitNoFriendsWarning),
         State.State('otherDialog', self.enterOtherDialog, self.exitOtherDialog),
         State.State('whiteListOpenChat', self.enterWhiteListOpenChat, self.exitWhiteListOpenChat),
         State.State('whiteListAvatarChat', self.enterWhiteListAvatarChat, self.exitWhiteListAvatarChat)], 'off', 'off')
        self.fsm.enterInitialState()
        return

    def delete(self):
        self.ignoreAll()
        del self.fsm
        if hasattr(self.chatInputNormal, 'destroy'):
            self.chatInputNormal.destroy()
        self.chatInputNormal.delete()
        del self.chatInputNormal
        self.chatInputSpeedChat.delete()
        del self.chatInputSpeedChat
        if self.openChatWarning:
            self.openChatWarning.destroy()
            self.openChatWarning = None
        if self.noSecretChatAtAll:
            self.noSecretChatAtAll.destroy()
            self.noSecretChatAtAll = None
        if self.noSecretChatAtAllAndNoWhitelist:
            self.noSecretChatAtAllAndNoWhitelist.destroy()
            self.noSecretChatAtAllAndNoWhitelist = None
        if self.noSecretChatWarning:
            self.noSecretChatWarning.destroy()
            self.noSecretChatWarning = None
        del self.localAvatar
        del self.cr

    def obscure(self, normal, sc):
        self.__scObscured = sc
        if self.__scObscured:
            self.scButton.hide()
        self.__normalObscured = normal
        if self.__normalObscured:
            self.normalButton.hide()

    def isObscured(self):
        return (self.__normalObscured, self.__scObscured)

    def stop(self):
        self.fsm.request('off')
        self.ignoreAll()

    def start(self):
        self.fsm.request('mainMenu')

    def sendWhisperString(self, message, whisperAvatarId):
        pass

    def sendSCChatMessage(self, msgIndex):
        base.talkAssistant.sendOpenSpeedChat(1, msgIndex)

    def sendSCWhisperMessage(self, msgIndex, whisperAvatarId):
        base.talkAssistant.sendAvatarWhisperSpeedChat(1, msgIndex, whisperAvatarId)

    def sendSCCustomChatMessage(self, msgIndex):
        base.talkAssistant.sendOpenSpeedChat(3, msgIndex)

    def sendSCCustomWhisperMessage(self, msgIndex, whisperAvatarId):
        base.talkAssistant.sendAvatarWhisperSpeedChat(3, msgIndex, whisperAvatarId)

    def sendSCEmoteChatMessage(self, emoteId):
        base.talkAssistant.sendOpenSpeedChat(2, emoteId)

    def sendSCEmoteWhisperMessage(self, emoteId, whisperAvatarId):
        base.talkAssistant.sendAvatarWhisperSpeedChat(2, emoteId, whisperAvatarId)

    def enterOff(self):
        self.scButton.hide()
        self.normalButton.hide()
        self.ignoreAll()

    def exitOff(self):
        pass

    def enterMainMenu(self):
        self.checkObscurred()
        if self.localAvatar.canChat() or self.cr.wantMagicWords:
            if self.wantBackgroundFocus:
                self.chatInputNormal.chatEntry['backgroundFocus'] = 1
            self.acceptOnce('enterNormalChat', self.fsm.request, ['normalChat'])

    def checkObscurred(self):
        if not self.__scObscured:
            self.scButton.show()
        if not self.__normalObscured:
            self.normalButton.show()

    def exitMainMenu(self):
        self.scButton.hide()
        self.normalButton.hide()
        self.ignore('enterNormalChat')
        if self.wantBackgroundFocus:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 0

    def whisperTo(self, avatarName, avatarId):
        self.fsm.request('whisper', [avatarName, avatarId])

    def noWhisper(self):
        self.fsm.request('mainMenu')

    def handleWhiteListSelect(self):
        self.fsm.request('whiteListOpenChat')

    def enterWhiteListOpenChat(self):
        self.checkObscurred()
        if self.wantBackgroundFocus:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 0
        base.localAvatar.chatMgr.chatInputWhiteList.activateByData()

    def exitWhiteListOpenChat(self):
        pass

    def enterWhiteListAvatarChat(self, receiverId):
        if self.wantBackgroundFocus:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 0
        base.localAvatar.chatMgr.chatInputWhiteList.activateByData(receiverId)

    def exitWhiteListAvatarChat(self):
        pass

    def enterWhisper(self, avatarName, avatarId):
        self.whisperScButton['extraArgs'] = [avatarName, avatarId]
        self.whisperButton['extraArgs'] = [avatarName, avatarId]
        online = 0

        if avatarId in self.cr.doId2do:
            online = 1
        elif self.cr.isFriend(avatarId):
            online = self.cr.isFriendOnline(avatarId)

        avatarUnderstandable = 0
        av = None

        if avatarId:
            av = self.cr.identifyAvatar(avatarId)
        if av != None:
            avatarUnderstandable = av.isUnderstandable()

        normalButtonObscured, scButtonObscured = self.isObscured()

        if avatarUnderstandable and online and not normalButtonObscured:
            self.whisperButton['state'] = 'normal'
            self.enablewhisperButton()
        else:
            self.whisperButton['state'] = 'inactive'
            self.disablewhisperButton()
        if online:
            self.whisperScButton['state'] = 'normal'
            self.changeFrameText(OTPLocalizer.ChatManagerWhisperToName % avatarName)
        else:
            self.whisperScButton['state'] = 'inactive'
            self.changeFrameText(OTPLocalizer.ChatManagerWhisperOffline % avatarName)
        self.whisperFrame.show()
        self.refreshWhisperFrame()

        if avatarUnderstandable and online:
            if self.wantBackgroundFocus:
                self.chatInputNormal.chatEntry['backgroundFocus'] = 1
            self.acceptOnce('enterNormalChat', self.fsm.request, ['whisperChat', [avatarName, avatarId]])

    def disablewhisperButton(self):
        pass

    def enablewhisperButton(self):
        pass

    def refreshWhisperFrame(self):
        pass

    def changeFrameText(self, newText):
        self.whisperFrame['text'] = newText

    def exitWhisper(self):
        self.whisperFrame.hide()
        self.ignore('enterNormalChat')
        self.chatInputNormal.chatEntry['backgroundFocus'] = 0

    def enterWhisperSpeedChat(self, avatarId):
        self.whisperFrame.show()
        if self.wantBackgroundFocus:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 0
        self.chatInputSpeedChat.show(avatarId)

    def exitWhisperSpeedChat(self):
        self.whisperFrame.hide()
        self.chatInputSpeedChat.hide()

    def enterWhisperChat(self, avatarName, avatarId):
        return self.chatInputNormal.activateByData(avatarId)

    def exitWhisperChat(self):
        self.chatInputNormal.deactivate()

    def enterSpeedChat(self):
        messenger.send('enterSpeedChat')
        if not self.__scObscured:
            self.scButton.show()
        if not self.__normalObscured:
            self.normalButton.show()
        if self.wantBackgroundFocus:
            self.chatInputNormal.chatEntry['backgroundFocus'] = 0
        self.chatInputSpeedChat.show()

    def exitSpeedChat(self):
        self.scButton.hide()
        self.normalButton.hide()
        self.chatInputSpeedChat.hide()

    def enterNormalChat(self):
        result = self.chatInputNormal.activateByData()
        return result

    def exitNormalChat(self):
        self.chatInputNormal.deactivate()

    def enterOpenChatWarning(self):
        self.notify.error('called enterOpenChatWarning() on parent class')

    def exitOpenChatWarning(self):
        self.notify.error('called exitOpenChatWarning() on parent class')

    def enterNoSecretChatAtAll(self):
        self.notify.error('called enterNoSecretChatAtAll() on parent class')

    def exitNoSecretChatAtAll(self):
        self.notify.error('called exitNoSecretChatAtAll() on parent class')

    def enterNoSecretChatAtAllAndNoWhitelist(self):
        self.notify.error('called enterNoSecretChatAtAllAndNoWhitelist() on parent class')

    def exitNoSecretChatAtAllAndNoWhitelist(self):
        self.notify.error('called exitNoSecretChatAtAllAndNoWhitelist() on parent class')

    def enterNoSecretChatWarning(self):
        self.notify.error('called enterNoSecretChatWarning() on parent class')

    def exitNoSecretChatWarning(self):
        self.notify.error('called exitNoSecretChatWarning() on parent class')

    def enterNoFriendsWarning(self):
        self.notify.error('called enterNoFriendsWarning() on parent class')

    def exitNoFriendsWarning(self):
        self.notify.error('called exitNoFriendsWarning() on parent class')

    def enterOtherDialog(self):
        pass

    def exitOtherDialog(self):
        pass
