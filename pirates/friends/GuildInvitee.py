from panda3d.core import NodePath, TextGraphic, TextNode, TextProperties, TextPropertiesManager
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.RequestButton import RequestButton

class GuildInviteeButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(GuildInviteeButton)



class GuildInvitee(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildInvitee')

    def __init__(self, avId, avName, guildId, guildName):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.6, 0, 0.47), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.0275), image_scale = (0.28, 1, 0.28))
        self.initialiseoptions(GuildInvitee)
        self.avId = avId
        self.avName = avName
        self.guildId = guildId
        if base.localAvatar.isIgnored(self.avId):
            self._GuildInvitee__handleNo()
            return None

        self.guildName = guildName
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
        text = OTPLocalizer.GuildInviteeInvitation % (buttonName, self.guildName)
        guiMain = loader.loadModel('models/gui/gui_main')
        self.box = OnscreenImage(parent = self, pos = (0.25, 0, 0.275), image = guiMain.find('**/general_frame_e'), scale = 0.28)
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.GuildInviteeTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.42), image = None, image_scale = 0.25)
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.325), textMayChange = 1)
        self.bOk = GuildInviteeButton(text = OTPLocalizer.GuildInviteeOK, command = self._GuildInvitee__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.15)
        self.bNo = GuildInviteeButton(text = OTPLocalizer.GuildInviteeNo, command = self._GuildInvitee__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.15)
        self.bIgnore = GuildInviteeButton(text = PLocalizer.GuildInviteeIgnore, command = self._GuildInvitee__handleIgnore)
        self.bIgnore.reparentTo(self)
        self.bIgnore['image_scale'] = (0.65, 1, 0.5)
        self.bIgnore.setPos(0.2, 0, 0.05)
        self.bIgnore['text_pos'] = (0.04, 0.04)

        self.accept('declineGuildInvitation', self._GuildInvitee__handleNo)
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            if base.localAvatar.guiMgr.ignoreGuildInvites:
                self._GuildInvitee__handleNo()




    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None

        self.destroyed = 1
        DirectFrame.destroy(self)


    def _GuildInvitee__handleOk(self):
        base.cr.guildManager.sendAcceptInvite()
        self.destroy()


    def _GuildInvitee__handleNo(self):
        base.cr.guildManager.sendDeclineInvite()
        self.destroy()


    def _GuildInvitee__handleIgnore(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleIgnoreGuildInvites()

        self.destroy()

    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)
