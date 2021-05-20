import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.fsm.FSM import FSM

class ChatManagerV2(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatManagerV2')

    def __init__(self):
        self.openChatWarning = None
        self.noSecretChatAtAll = None
        self.noSecretChatWarning = None
        self.fsm = ClassicFSM.ClassicFSM('chatManager', [
            State.State('off', self.enterOff, self.exitOff),
            State.State('mainMenu', self.enterMainMenu, self.exitMainMenu),
            State.State('openChatWarning', self.enterOpenChatWarning, self.exitOpenChatWarning),
            State.State('noSecretChatAtAll', self.enterNoSecretChatAtAll, self.exitNoSecretChatAtAll),
            State.State('noSecretChatWarning', self.enterNoSecretChatWarning, self.exitNoSecretChatWarning),
            State.State('noFriendsWarning', self.enterNoFriendsWarning, self.exitNoFriendsWarning),
            State.State('otherDialog', self.enterOtherDialog, self.exitOtherDialog)], 'off', 'off')
        self.fsm.enterInitialState()

    def delete(self):
        self.ignoreAll()
        del self.fsm

    def enterOff(self):
        self.ignoreAll()

    def exitOff(self):
        pass

    def enterOtherDialog(self):
        pass

    def exitOtherDialog(self):
        pass

    def enterNoFriendsWarning(self):
        self.notify.error('called enterNoFriendsWarning() on parent class')

    def exitNoFriendsWarning(self):
        self.notify.error('called exitNoFriendsWarning() on parent class')

    def enterNoSecretChatWarning(self):
        self.notify.error('called enterNoSecretChatWarning() on parent class')

    def exitNoSecretChatWarning(self):
        self.notify.error('called exitNoSecretChatWarning() on parent class')
