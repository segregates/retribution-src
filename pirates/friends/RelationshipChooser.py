from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog.RejectCode import RejectCode
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.friends import PirateFriendSecret
from pirates.piratesgui import PirateButtonChain

class RelationshipChooser(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInviter')

    def __init__(self, avId, avName):
        self.avId = avId
        self.avName = avName
        self.avDisableName = 'disable-%s' % avId
        GuiPanel.GuiPanel.__init__(self, PLocalizer.RelationshipChooserTitle % avName, 0.5, 0.25, True, 1)
        self.initialiseoptions(RelationshipChooser)
        self.setPos(0.15, 0, 0.25)
        self.chain = PirateButtonChain.PirateButtonChain(self.width, self)
        self.chain.setPos(0, 0, -0.03)
        self.load()
        self.determineButtonState()


    def load(self):
        self.avFriendButton = self.chain.premakeButton(PLocalizer.RelationshipChooserAvFriendsMake, self._RelationshipChooser__handleAvatarFriend)
        self.secretsButton = self.chain.premakeButton(PLocalizer.RelationshipChooserPlSecrets, self._RelationshipChooser__handleSecrets)
        self.chain.makeButtons()


    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None

        self.destroyed = 1
        self.chain.destroy()
        GuiPanel.GuiPanel.destroy(self)


    def _RelationshipChooser__handleSecrets(self):
        PirateFriendSecret.showFriendSecret()
        self.destroy()


    def _RelationshipChooser__handleAvatarFriend(self):
        base.localAvatar.guiMgr.handleAvatarFriendInvite(self.avId, self.avName)
        self.destroy()


    def determineButtonState(self):
        isAvatarFriend = base.localAvatar.isFriend(self.avId)
        if isAvatarFriend:
            self.avFriendButton['text'] = PLocalizer.RelationshipChooserAvFriendsBreak
        else:
            self.avFriendButton['text'] = PLocalizer.RelationshipChooserAvFriendsMake
        self.avFriendButton['state'] = DGG.DISABLED
        self.secretsButton['state'] = DGG.NORMAL
        if self.avId or self.pId:
            av = base.cr.doId2do.get(self.avId)
            print 'avId %s av %s' % (self.avId, av)
            if av:
                self.avFriendButton['state'] = DGG.NORMAL

            if base.localAvatar.isIgnored(self.avId):
                self.avFriendButton['state'] = DGG.DISABLED
                self.secretsButton['state'] = DGG.DISABLED

            if isAvatarFriend:
                self.avFriendButton['state'] = DGG.NORMAL
