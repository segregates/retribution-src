from panda3d.core import TextProperties, TextPropertiesManager
from direct.fsm import FSM
from otp.otpbase import OTPGlobals
import sys
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals
from otp.otpbase import OTPLocalizer
from direct.task import Task
from otp.nametag.NametagConstants import CFSpeech, CFTimeout, CFThought

class ChatInputWhiteList(FSM.FSM, DirectEntry):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatInputWhiteList')

    def __init__(self, parent = None, **kw):
        FSM.FSM.__init__(self, 'ChatInputWhiteList')
        optiondefs = (('parent', parent, None), ('relief', DGG.SUNKEN, None), ('text_scale', 0.03, None), ('frameSize', (-0.2, 25.3, -0.5, 1.2), None), ('borderWidth', (0.003, 0.003), None), ('frameColor', (0.9, 0.9, 0.85, 0.8), None), ('entryFont', OTPGlobals.getInterfaceFont(), None), ('width', 25, None), ('numLines', 1, None), ('cursorKeys', 1, None), ('backgroundFocus', 0, None), ('suppressKeys', 1, None), ('suppressMouse', 1, None), ('command', self.sendChat, None), ('failedCommand', self.sendFailed, None), ('focus', 0, None), ('text', '', None))
        self.defineoptions(kw, optiondefs)
        DirectEntry.__init__(self, parent = parent)
        self.initialiseoptions(ChatInputWhiteList)
        self.whisperId = None

        self.wantHistory = config.GetBool('want-chat-history', 1)
        self.history = [
            '']
        self.historySize = config.GetInt('chat-history-size', 10)
        self.historyIndex = 0
        self.active = 0
        self.autoOff = 0
        self.alwaysSubmit = False
        self.bind(DirectGuiGlobals.TYPE, self.applyFilter)
        self.bind(DirectGuiGlobals.ERASE, self.applyFilter)
        tpMgr = TextPropertiesManager.getGlobalPtr()
        Red = tpMgr.getProperties('red')
        Red.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLRed', Red)
        del tpMgr
        self.origFrameColor = self['frameColor']
        self.origTextScale = self['text_scale']
        self.origFrameSize = self['frameSize']

    def delete(self):
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')

    def requestMode(self, mode, *args):
        self.request(mode, *args)

    def enterOff(self):
        self.deactivate()

    def exitOff(self):
        self.activate()

    def enterAllChat(self):
        self['focus'] = 1
        self.show()

    def exitAllChat(self):
        pass

    def enterGuildChat(self):
        self['focus'] = 1
        self.show()

    def exitGuildChat(self):
        pass

    def enterCrewChat(self):
        self['focus'] = 1
        self.show()

    def exitCrewChat(self):
        pass

    def enterShipPVPChat(self):
        self['focus'] = 1
        self.show()

    def exitShipPVPChat(self):
        pass

    def enterAvatarWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    def exitAvatarWhisper(self):
        self.set(self.tempText)
        self.whisperId = None

    def activate(self):
        self.set('')
        self['focus'] = 1
        self.show()
        self.active = 1
        self.guiItem.setAcceptEnabled(True)
        self.accept('uber-escape', self.handleEscape)
        if self.wantHistory:
            self.accept('arrow_up-up', self.getPrevHistory)
            self.accept('arrow_down-up', self.getNextHistory)

    def deactivate(self):
        self.ignore('uber-escape')
        self.set('')
        self['focus'] = 0
        self.hide()
        self.active = 0
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')

    def handleEscape(self):
        localAvatar.chatMgr.deactivateChat()

    def isActive(self):
        return self.active

    def _checkShouldFilter(self, text):
        if len(text) > 0 and text[0] in [
            '/']:
            return False
        else:
            return True

    def sendChat(self, text, overflow = False):
        text = self.get(plain = True)
        if text:
            self.set('')
            if text.startswith('/'):
                base.talkAssistant.executeSlashCommand(text)
            else:
                self.sendChatByMode(text)
                if self.wantHistory:
                    self.addToHistory(text)

        else:
            localAvatar.chatMgr.deactivateChat()
        if not overflow:
            self.hide()
            if self.autoOff:
                self.requestMode('Off')

            localAvatar.chatMgr.messageSent()

    def sendChatByMode(self, text):
        state = self.getCurrentOrNextState()
        messenger.send('sentRegularChat')
        if state == 'AvatarWhisper':
            base.talkAssistant.sendWhisperTalk(text, self.whisperId)
        else:
            base.talkAssistant.sendOpenTalk(text)

    def sendFailed(self, text):
        self['frameColor'] = (0.9, 0.0, 0.0, 0.8)

        def resetFrameColor(task = None):
            self['frameColor'] = self.origFrameColor
            return Task.done

        taskMgr.doMethodLater(0.1, resetFrameColor, 'resetFrameColor')
        self.applyFilter(keyArgs = None)
        self.guiItem.setAcceptEnabled(True)

    def chatOverflow(self, overflowText):
        self.sendChat(self.get(plain = True), overflow = True)

    def addToHistory(self, text):
        self.history = [
            text] + self.history[:self.historySize - 1]
        self.historyIndex = 0

    def getPrevHistory(self):
        self.set(self.history[self.historyIndex])
        self.historyIndex += 1
        self.historyIndex %= len(self.history)
        self.setCursorPosition(len(self.get()))

    def getNextHistory(self):
        self.set(self.history[self.historyIndex])
        self.historyIndex -= 1
        self.historyIndex %= len(self.history)
        self.setCursorPosition(len(self.get()))

    def applyFilter(self, keyArgs):
        if base.whiteList:
            self.set(base.whiteList.processThroughAll(self.get(plain=True)))
