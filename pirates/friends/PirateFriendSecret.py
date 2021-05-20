global globalFriendSecret
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
globalFriendSecret = None
offX = 0.8
offZ = 0.6

def showFriendSecret():
    global globalFriendSecret
    if not base.cr.allowSecretChat():
        base.localAvatar.chatMgr.fsm.request('noSecretChatAtAll')
    else:
        openFriendSecret()


def openFriendSecret():
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()

    globalFriendSecret = FriendSecret()
    globalFriendSecret.setPos(-0.75, 0, -0.45)
    globalFriendSecret.enter()


def hideFriendSecret():
    if globalFriendSecret != None:
        globalFriendSecret.exit()



def unloadFriendSecret():
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
        globalFriendSecret = None


class FriendSecret(GuiPanel.GuiPanel, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendSecret')

    def __init__(self, secretType):
        GuiPanel.GuiPanel.__init__(self, 'Secret Codes!!! Arg!!', 1.6, 1.2)
        StateData.StateData.__init__(self, 'friend-secret-done')
        self.initialiseoptions(FriendSecret)
        self.prefix = 'POR'
        self.secretType = secretType
        self.notify.debug('### secretType = %s' % self.secretType)
        self.requestedSecretType = secretType
        self.notify.debug('### requestedSecretType = %s' % self.requestedSecretType)


    def unload(self):
        print 'unload'
        if self.isLoaded == 0:
            return None

        self.isLoaded = 0
        self.exit()
        del self.introText
        del self.getSecret
        del self.enterSecretText
        del self.enterSecret
        del self.ok1
        del self.ok2
        del self.cancel
        del self.secretText
        GuiPanel.GuiPanel.destroy(self)


    def load(self):
        print 'load'
        if self.isLoaded == 1:
            return None

        self.isLoaded = 1
        charGui = loader.loadModel('models/gui/char_gui')
        buttonImage = (charGui.find('**/chargui_text_block_large'), charGui.find('**/chargui_text_block_large_down'), charGui.find('**/chargui_text_block_large_over'))
        self.introText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, 0.4 + offZ), scale = 0.05, text = PLocalizer.FriendSecretIntro, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 30)
        self.introText.hide()
        guiButton = loader.loadModel('models/gui/quit_button')
        self.getSecret = DirectButton(parent = self, relief = None, pos = (0 + offX, 0, -0.11 + offZ), image = buttonImage, image_scale = (0.85, 1, 0.4), text = OTPLocalizer.FriendSecretGetSecret, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), command = self._FriendSecret__getSecret)
        self.getSecret.hide()
        self.enterSecretText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, -0.25 + offZ), text = OTPLocalizer.FriendSecretEnterSecret, text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 30)
        self.enterSecretText.hide()
        self.enterSecret = DirectEntry(parent = self, relief = DGG.SUNKEN, scale = 0.06, pos = (-0.6 + offX, 0, -0.38 + offZ), frameColor = (0.8, 0.8, 0.5, 1), borderWidth = (0.1, 0.1), numLines = 1, width = 20, frameSize = (-0.4, 20.4, -0.4, 1.1), command = self._FriendSecret__enterSecret, suppressKeys = 1)
        self.enterSecret.resetFrameSize()
        self.enterSecret.hide()
        self.ok1 = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.85, 1, 0.4), text = OTPLocalizer.FriendSecretEnter, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), pos = (0 + offX, 0, -0.5 + offZ), command = self._FriendSecret__ok1)
        self.ok1.hide()
        self.ok2 = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.4, 1, 0.4), text = OTPLocalizer.FriendSecretOK, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), pos = (0 + offX, 0, -0.5 + offZ), command = self._FriendSecret__ok2)
        self.ok2.hide()
        self.cancel = DirectButton(parent = self, relief = None, text = OTPLocalizer.FriendSecretCancel, image = buttonImage, image_scale = (0.4, 1, 0.4), text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), pos = (0 + offX, 0, -0.5 + offZ), command = self._FriendSecret__cancel)
        self.cancel.hide()
        self.nextText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, 0.3 + offZ), scale = 0.06, text = '', text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 25.5)
        self.nextText.hide()
        self.secretText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, -0.36 + offZ), scale = 0.1, text = '', text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 30)
        self.secretText.hide()
        charGui.remove_node()

    def enter(self):
        print 'enter'
        if self.isEntered == 1:
            return None

        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()

        self.show()
        self.introText.show()
        self.getSecret.show()
        self.enterSecretText.show()
        self.enterSecret.show()
        self.ok1.show()
        self.ok2.hide()
        self.cancel.hide()
        self.nextText.hide()
        self.secretText.hide()
        base.localAvatar.chatMgr.fsm.request('otherDialog')
        self.enterSecret['focus'] = 1
        NametagGlobals.setOnscreenChatForced(1)


    def closePanel(self):
        print 'closePanel'
        self.exit()


    def exit(self):
        print 'exit'
        if self.isEntered == 0:
            return None

        self.isEntered = 0
        NametagGlobals.setOnscreenChatForced(0)
        self._FriendSecret__cleanupFirstPage()
        self.ignoreAll()
        self.hide()

    def _FriendSecret__handleCancel(self):
        self.exit()


    def _FriendSecret__getSecret(self):
        self._FriendSecret__cleanupFirstPage()
        self.nextText['text'] = OTPLocalizer.FriendSecretGettingSecret
        self.nextText.setPos(0 + offX, 0, 0.3 + offZ)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()
        
        if not base.cr.friendManager:
            self.notify.warning('No FriendManager available.')
            self.exit()
            return None

        base.cr.friendManager.up_requestSecret()
        self.accept('requestSecretResponse', self._FriendSecret__gotAvatarSecret)

    def _FriendSecret__gotAvatarSecret(self, result, secret):
        self.ignore('requestSecretResponse')
        if result == 1:
            self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
            self.nextText.setPos(0 + offX, 0, 0.47 + offZ)
            if self.prefix:
                self.secretText['text'] = self.prefix + ' ' + secret
            else:
                self.secretText['text'] = secret
        else:
            self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def _FriendSecret__enterSecret(self, secret):
        self.enterSecret.set('')
        secret = string.strip(secret)
        if not secret:
            self.exit()
            return None

        if not base.cr.friendManager:
            self.notify.warning('No FriendManager available.')
            self.exit()
            return None

        self._FriendSecret__cleanupFirstPage()
        if self.prefix:
            if secret[0:2] == self.prefix:
                secret = secret[3:]
            else:
                self._FriendSecret__enteredSecret(4, 0)
                return None

        base.cr.friendManager.up_submitSecret(secret)
        self.nextText['text'] = OTPLocalizer.FriendSecretTryingSecret
        self.nextText.setPos(0 + offX, 0, 0.3 + offZ)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()
        taskMgr.doMethodLater(10.0, self._FriendSecret__secretTimeout, 'timeoutSecretResponse')


    def _FriendSecret__secretTimeout(self, caller = None):
        self.nextText['text'] = OTPLocalizer.FriendSecretTimeOut
        return None
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()


    def _FriendSecret__secretResponseReject(self, reason):
        print '__secretResponseReject'
        taskMgr.remove('timeoutSecretResponse')
        self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretUnknown
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()


    def _FriendSecret__nowFriends(self, avId):
        self.ignore('friendsMapComplete')
        handle = base.cr.identifyAvatar(avId)
        if handle != None:
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriends % handle.getName()
        else:
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriendsNoName
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()


    def _FriendSecret__ok1(self):
        secret = self.enterSecret.get()
        self._FriendSecret__enterSecret(secret)


    def _FriendSecret__ok2(self):
        self.exit()


    def _FriendSecret__cancel(self):
        self.exit()


    def _FriendSecret__cleanupFirstPage(self):
        self.introText.hide()
        self.getSecret.hide()
        self.enterSecretText.hide()
        self.enterSecret.hide()
        base.localAvatar.chatMgr.fsm.request('mainMenu')
