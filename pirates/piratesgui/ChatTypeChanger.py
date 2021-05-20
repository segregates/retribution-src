from panda3d.core import TextNode, VBase4
from direct.gui.DirectGui import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog

class ChatTypeChanger(BorderFrame):

    def __init__(self, **kw):
        self.sizeX = 0.8
        self.sizeZ = 1
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        optiondefs = (
            ('parent', aspect2d, None),
            ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None),
            ('text', PLocalizer.MainMenuChatSettings, None),
            ('text_align', TextNode.ACenter, None),
            ('text_font', PiratesGlobals.getPirateBoldOutlineFont(), None),
            ('text_fg', (1, 1, 1, 1), None),
            ('text_shadow', PiratesGuiGlobals.TextShadow, None),
            ('textMayChange', 1, None),
            ('text_scale', textScale, None),
            ('text_pos', (self.sizeX * 0.5, self.sizeZ * 0.968 - textScale), None)
        )

        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self)
        self.initialiseoptions(ChatTypeChanger)

        self.confirmDialog = None
        self.setup()


    def destroy(self, _=None):
        self.ignoreAll()
        BorderFrame.destroy(self)
        self.destroyConfirmDialog()

    def destroyConfirmDialog(self):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None

    def setup(self):
        self.setBin('gui-popup', 0)
        self.messageLabel = DirectLabel(parent = self, relief = None, text = PLocalizer.ChatTypeWarning, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 18, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.050000, 0.0, self.sizeZ * 0.825))
        
        gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))

        self.cancelButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.418, 1.0, 0.22), image0_color = VBase4(0.65, 0.65, 0.65, 1), image1_color = VBase4(0.4, 0.4, 0.4, 1), image2_color = VBase4(0.9, 0.9, 0.9, 1), image3_color = VBase4(0.408, 0.4, 0.4, 1), text = PLocalizer.ChatTypeLater, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.5, 0, 0.070), command = self.destroy)
        
        main_gui = loader.loadModel('models/gui/gui_main')
        generic_x = main_gui.find('**/x2')
        generic_box = main_gui.find('**/exit_button')
        generic_box_over = main_gui.find('**/exit_button_over')
        main_gui.remove_node()
        
        closeButton = GuiButton.GuiButton(parent = self, relief = None, pos = (1.0, 0, 0.1598), image = (generic_box, generic_box, generic_box_over, generic_box), image_scale = 0.4, command = self.destroy)
        xButton = OnscreenImage(parent = closeButton, image = generic_x, scale = 0.200, pos = (-0.256, 0, 0.766))

        for i, choice in enumerate(PLocalizer.ChatTypeNames):
            choiceButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.418, 1.0, 0.22), image0_color = VBase4(0.65, 0.65, 0.65, 1), image1_color = VBase4(0.4, 0.4, 0.4, 1), image2_color = VBase4(0.9, 0.9, 0.9, 1), image3_color = VBase4(0.408, 0.4, 0.4, 1), text = choice, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.5, 0, 0.37 - 0.1 * i), command = self.confirmChatType, extraArgs = [i])

    def confirmChatType(self, choice):
        self.hide()

        if choice != 0:
            self.confirmDialog = PDialog.PDialog(text = PLocalizer.ChatTypeWarnings[choice], text_wordwrap = 20, style = OTPDialog.YesNo, command = self.doConfirmChatType, extraArgs = [choice])
            self.confirmDialog.show()
        else:
            self.doConfirmChatType(1, choice)

    def doConfirmChatType(self, choice, chatType):
        self.destroyConfirmDialog()

        if choice > 0:
            base.localAvatar.d_requestChatType(chatType)
            self.confirmDialog = PDialog.PDialog(text = PLocalizer.ChatTypeUpdated, style = OTPDialog.Acknowledge, command = self.destroy)
            self.confirmDialog.show()
        else:
            self.show()