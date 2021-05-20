from panda3d.core import NodePath, TextGraphic, TextNode, TextProperties, TextPropertiesManager
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.RequestButton import RequestButton

class FriendInviteeButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FriendInviteeButton)



class FriendInvitee(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInvitee')

    def __init__(self, avId, avName, context):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.6, 0, 0.47), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.275), image_scale = 0.25)
        self.initialiseoptions(FriendInvitee)
        self.avId = avId
        self.avName = avName
        self.context = context
        if base.localAvatar.isIgnored(self.avId):
            self._FriendInvitee__handleNo()
            return None

        nameArray = ('\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeOVER\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02')
        nameButton = DirectButton(parent = NodePath(), relief = None, text = nameArray, text_align = TextNode.ALeft, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, command = self.handleAvatarPress, extraArgs = [
            avId,
            avName])
        (left, right, bottom, top) = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '' + self.avName + ''
        buttonText = PLocalizer.CrewInviteeInvitation % buttonName
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setGraphic(self.avName, nameGFX)
        del tpMgr
        text = OTPLocalizer.FriendInviteeInvitation % buttonName
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.FriendInviteeTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), text_pos = (0, 0), pos = (0.25, 0, 0.42), image = None, image_scale = 0.25)
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.325), textMayChange = 1)
        self.bOk = FriendInviteeButton(text = OTPLocalizer.FriendInviteeOK, command = self._FriendInvitee__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = FriendInviteeButton(text = OTPLocalizer.FriendInviteeNo, command = self._FriendInvitee__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('cancelFriendInvitation', self._FriendInvitee__handleCancelFromAbove)


    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None

        if self.context:
            base.cr.friendManager.up_inviteeFriendResponse(2, self.context)
            self.context = None

        self.destroyed = 1
        self.ignore('cancelFriendInvitation')
        DirectFrame.destroy(self)


    def _FriendInvitee__handleOk(self):
        base.cr.friendManager.up_inviteeFriendResponse(1, self.context)
        self.context = None
        self.destroy()


    def _FriendInvitee__handleNo(self):
        base.cr.friendManager.up_inviteeFriendResponse(0, self.context)
        self.context = None
        self.destroy()


    def _FriendInvitee__handleCancelFromAbove(self):
        self.destroy()


    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)
