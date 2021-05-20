from panda3d.core import CollideMask, CollisionEntry
import sys
import string
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPLocalizer
from otp.chat import ChatManager
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals
from otp.chat import ChatManagerV2
from otp.chat.ChatGlobals import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import ChatPanel
from PChatInputSpeedChat import PChatInputSpeedChat
from PChatInputEmote import PChatInputEmote
from PChatInputWhiteList import PChatInputWhiteList
from pirates.uberdog.UberDogGlobals import InventoryType

class PiratesChatManager(ChatManagerV2.ChatManagerV2):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesChatManager')

    def __init__(self):
        ChatManagerV2.ChatManagerV2.__init__(self)
        self.warningDialog = None
        self.preferredMode = 'All'
        self.lastPreferred = 'All'
        self.whiteListActive = True
        self.active = False
        self.lastWhisper = None
        self.shipPVPChatAllowed = True
        self.crewChatAllowed = True
        self.guildChatAllowed = True
        self.openChatEnabled = True
        self.toggleEnabled = self.openChatEnabled
        self.noChat = not (self.openChatEnabled)
        self.whiteListEntry = PChatInputWhiteList(text_scale = 0.035, frameSize = (-0.006, 3.2, -0.015, 0.036))
        self.whiteListScroller = DirectEntryScroll(entry = self.whiteListEntry, clipSize = (-0.006, 0.684, -0.015, 0.036))
        if self.openChatEnabled:
            self.whiteListEntry.alwaysSubmit = True

        self.speedEntry = PChatInputSpeedChat()
        self.emoteEntry = PChatInputEmote()
        self.chatPanel = ChatPanel.ChatPanel(self, self.whiteListScroller)
        self.whiteListActive = True
        self.whiteListEntry.requestMode(self.preferredMode)

        self.deactivateChat()

    def delete(self):
        self.ignoreAll()
        self.stopFadeTimer()
        self.whiteListEntry.destroy()
        del self.whiteListEntry
        self.speedEntry.delete()
        del self.speedEntry
        self.emoteEntry.delete()
        del self.emoteEntry
        self.chatPanel.destroy()
        del self.chatPanel
        if self.warningDialog:
            self.warningDialog.destroy()
            self.warningDialog = None

        ChatManagerV2.ChatManagerV2.delete(self)

    def enableCrewChat(self):
        self.crewChatAllowed = True
        self.chatPanel.enableCrewChat()

    def disableCrewChat(self):
        self.crewChatAllowed = False
        self.chatPanel.disableCrewChat()

    def enableGuildChat(self):
        self.guildChatAllowed = True
        self.chatPanel.enableGuildChat()

    def disableGuildChat(self):
        self.guildChatAllowed = False
        self.chatPanel.disableGuildChat()

    def enableShipPVPChat(self):
        self.shipPVPChatAllowed = True
        self.chatPanel.enableShipPVPChat()

    def disableShipPVPChat(self):
        self.shipPVPChatAllowed = False
        self.chatPanel.disableShipPVPChat()

    def activateChat(self, preferred = ''):
        if not isinstance(preferred, str):
            if isinstance(preferred, CollisionEntry):
                self.notify.warning("'preferred' is a CollisionEntry")
                self.notify.warning('from mask: %s' % (preferred.getFromNode().getFromCollideMask(),))
                self.notify.warning('into mask: %s' % (preferred.getIntoNode().getIntoCollideMask(),))

            self.notify.warning('Calling PiratesChatManager.activateChat with non-string preferred argument: %s' % (preferred,))
            return None
        messenger.send('openedChat')
        self.stopFadeTimer()
        self.active = True
        if preferred:
            self.preferredMode = preferred
        if hasattr(base, 'localAvatar'):
            base.localAvatar.removeContext(InventoryType.PlayerChat)
        if self.preferredMode == 'All':
            self.chatPanel.activateAllChat()
            self.speedEntry.requestMode('AllChat')
            self.emoteEntry.requestMode('AllChat')
            if self.noChat:
                pass
            elif self.whiteListActive:
                self.whiteListEntry.requestMode('AllChat')
        elif self.preferredMode == 'Crew':
            if localAvatar.getBandId():
                self.chatPanel.activateCrewChat()
                if self.noChat:
                    pass
                if self.whiteListActive:
                    self.whiteListEntry.requestMode('CrewChat')
                self.speedEntry.requestMode('CrewChat')
                self.emoteEntry.requestMode('CrewChat')
            else:
                self.activateChat('All')
        elif self.preferredMode == 'Guild':
            if localAvatar.getGuildId():
                self.chatPanel.activateGuildChat()
                if self.noChat:
                    pass
                if self.whiteListActive:
                    self.whiteListEntry.requestMode('GuildChat')
                self.speedEntry.requestMode('GuildChat')
                self.emoteEntry.requestMode('GuildChat')
            else:
                self.activateChat('All')
        elif self.preferredMode == 'ShipPVP':
            if not hasattr(localAvatar.ship, 'getSiegeTeam'):
                self.activateChat('All')
            elif localAvatar.ship.getSiegeTeam():
                self.chatPanel.activateShipPVPChat()
                if self.noChat:
                    pass
                if self.whiteListActive:
                    self.whiteListEntry.requestMode('ShipPVPChat')
                self.speedEntry.requestMode('ShipPVP')
                self.emoteEntry.requestMode('ShipPVP')
            else:
                self.activateChat('All')
        elif self.preferredMode == 'Whisper' and self.lastWhisper:
            id = self.lastWhisper
            handle = None
            if id:
                handle = base.cr.identifyAvatar(id)
            if handle:
                self.activateWhisperChat(id)
                self.chatPanel.activateWhisperChat(self.lastWhisper)
            else:
                self.activateChat(self.lastPreferred)

    def activateWhisperChat(self, whisperId):
        self.stopFadeTimer()
        if self.preferredMode != 'Whisper':
            self.lastPreferred = self.preferredMode

        self.preferredMode = 'Whisper'
        self.lastWhisper = whisperId
        self.chatPanel.activateWhisperChat(whisperId)
        
        handle = base.cr.identifyAvatar(whisperId)
        
        if handle and handle.isOnline():
            self.speedEntry.requestMode('AvatarWhisper', whisperId)
            self.speedEntry.setWhisperTo(whisperId)
            if self.whiteListActive:
                self.whiteListEntry.requestMode('AvatarWhisper', whisperId)
        else:
            self.activateChat(self.lastPreferred)

    def activateSpeedChat(self):
        messenger.send('openedSpeedChat')
        self.activateChat()
        self.speedEntry.show()
        self.emoteEntry.hide()

    def activateEmoteChat(self):
        self.speedEntry.hide()
        self.emoteEntry.show()

    def toggleWhiteListChat(self):
        if not self.toggleEnabled:
            return None

        if not isinstance(self.preferredMode, str):
            raise TypeError, 'preferredMode was non-string in toggleWhiteListChat'

        self.whiteListActive = True
        if not self.active:
            self.activateChat()

        if self.whiteListActive:
            text = self.whiteListEntry.get(plain = True)
            if 'Whisper' in self.preferredMode:
                self.whiteListEntry.requestMode('AvatarWhisper', self.lastWhisper)
            else:
                self.whiteListEntry.requestMode(self.preferredMode + 'Chat')
            self.whiteListEntry.activate()
            self.whiteListEntry.set(text)
            self.whiteListEntry.setCursorPosition(len(text))
            self.whiteListEntry.applyFilter({ })
            self.chatPanel.enableWhiteListChat()
        else:
            text = self.whiteListEntry.get(plain = True)
            self.whiteListEntry.requestMode('Off')

    def speedChatDone(self, success = True):
        self.deactivateChat(success)

    def deactivateChat(self, fade = False):
        self.active = False
        if fade:
            self.startFadeTimer()
        else:
            self.stopFadeTimer()
            self.chatPanel.deactivateChat()
        self.whiteListEntry.requestMode('Off')
        self.speedEntry.fsm.request('off')
        self.emoteEntry.fsm.request('off')

    def messageSent(self):
        self.deactivateChat(fade = True)

    def whisperCanceled(self):
        self.activateChat(self.lastPreferred)

    def startFadeTimer(self):
        self.stopFadeTimer()
        taskMgr.doMethodLater(3, self.deactivateChat, 'ChatManager-fadeTimer', [])

    def stopFadeTimer(self):
        taskMgr.remove('ChatManager-fadeTimer')

    def enterOpenChatWarning(self):
        self.warningDialog = PDialog.PDialog(text = PLocalizer.ChatManagerNeedParentWarning, style = OTPDialog.Acknowledge, command = self.openChatWarningAck)

    def openChatWarningAck(self, value):
        self.fsm.request('mainMenu')

    def exitOpenChatWarning(self):
        self.warningDialog.destroy()
        self.warningDialog = None

    def enterNoFriendsWarning(self):
        self.warningDialog = PDialog.PDialog(text = PLocalizer.ChatManagerNoFriendsWarning, style = OTPDialog.Acknowledge, command = self.noFriendsWarningAck)

    def noFriendsWarningAck(self, value):
        self.fsm.request('mainMenu')

    def exitNoFriendsWarning(self):
        self.warningDialog.destroy()
        self.warningDialog = None

    def enterNoSecretChatAtAll(self):
        if self.noSecretChatAtAll == None:
            offX = -0.75
            offZ = -0.45
            self.noSecretChatAtAll = GuiPanel.GuiPanel('Secret Codes!!! Arg!!', 1.6, 1.2)
            self.noSecretChatAtAll.setPos(offX, 0, offZ)
            DirectLabel(parent = self.noSecretChatAtAll, relief = None, pos = (-offX, 0, 0.95), text_fg = (0.9, 0.9, 0.9, 1), text = OTPLocalizer.NoSecretChatAtAllTitle, textMayChange = 0, text_scale = 0.08)
            DirectLabel(parent = self.noSecretChatAtAll, relief = None, pos = (-offX, 0, 0.8), text_fg = (0.9, 0.9, 0.9, 1), text = PLocalizer.NoSecretChatAtAll, text_wordwrap = 20, textMayChange = 0, text_scale = 0.07)

            def handleNoSecretChatAtAllOK(value):
                self.fsm.request('mainMenu')

            DirectButton(self.noSecretChatAtAll, relief = None, text_fg = (0.9, 0.9, 0.9, 1), text = OTPLocalizer.NoSecretChatAtAllOK, text_scale = 0.05, text_pos = (0.0, -0.1), textMayChange = 0, pos = (-offX, 0.0, 0.15), command = handleNoSecretChatAtAllOK)

        self.noSecretChatAtAll.show()

    def exitNoSecretChatAtAll(self):
        self.noSecretChatAtAll.hide()

    def enterNoSecretChatWarning(self):
        pass

    def exitNoSecretChatWarning(self):
        pass

    def enterActivateChat(self):
        pass

    def exitActivateChat(self):
        pass

    def enterMainMenu(self):
        pass

    def exitMainMenu(self):
        pass

    def stop(self):
        self.fsm.request('off')
        self.ignoreAll()

    def start(self):
        self.fsm.request('mainMenu')
        self.accept('enter', self.activateChat)

    def enterNoSecretChatWarning(self):
        self.warningDialog = PDialog.PDialog(text = PLocalizer.ChatManagerNoFriendsWarning, style = OTPDialog.Acknowledge, command = self.noSecretChatWarningAck)

    def noSecretChatWarningAck(self, value):
        self.fsm.request('mainMenu')

    def exitNoSecretChatWarning(self):
        self.warningDialog.destroy()
        self.warningDialog = None
