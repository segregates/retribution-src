from panda3d.core import Texture
from direct.gui.DirectGui import *
from otp.otpgui import OTPDialog
from pirates.piratesgui import BorderFrame, GUIUtils, PiratesGuiGlobals, PDialog
from pirates.piratesbase import PiratesGlobals, PLocalizer

class FactionChooser(DirectFrame):
    
    def __init__(self, callback, *args, **kwargs):
        frame = BorderFrame.BorderFrame(borderScale=0.5)
        kwargs['image'] = frame
        kwargs['image_scale'] = (0.8, 1, 0.5)

        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(FactionChooser)
        frame.destroy()
        
        self.callback = callback
        
        self.text = DirectLabel(self, relief=None, text=PLocalizer.MakeAPirateFactionChoose, text_wordwrap=15, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=PiratesGuiGlobals.TextScaleLarge, pos=(0, 0, 0.1))
        self.buttons = []

        for i, x in enumerate([-0.15, 0, 0.15]):
            if i == 0:
                flag = GUIUtils.loadTextureModel(loader.loadTexture('phase_2/maps/pir_t_gui_shp_skull.jpg', 'phase_2/maps/pir_t_gui_shp_skull_a.rgb'))
            else:
                flags = loader.loadModel('models/textureCards/sailLogo')
                flag = flags.find('**/' + PiratesGlobals.ALLEGIANCE_FLAGS[i])
                flags.removeNode()

            self.buttons.append(DirectButton(self, relief=None, geom=flag, geom_scale=(0.04 if i == 0 else 0.074), pos=(x, 0, -0.05), command=self.__choose, extraArgs=[i]))
            self.buttons.append(DirectButton(self, relief=None, text=PLocalizer.FactionNames[i], pos=(x, 0, -0.15), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=PiratesGuiGlobals.TextScaleLarge, command=self.__choose, extraArgs=[i]))
        
        for i, button in enumerate(self.buttons):
            button.bind(DGG.ENTER, self.__enterButton, extraArgs=[i])
            button.bind(DGG.EXIT, self.__exitButton, extraArgs=[i])
    
    def removeNode(self):
        self.destroy()
    
    def destroy(self):
        DirectFrame.destroy(self)
        
        if hasattr(self, 'buttons') and self.buttons:
            for button in self.buttons:
                button.destroy()
            
            del self.buttons
    
    def destroyDialog(self):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.destroy()
            del self.dialog
    
    def getButtons(self, i):
        i = i // 2 * 2
        return [self.buttons[i], self.buttons[i + 1]]
    
    def __enterButton(self, i, event=None):
        for button in self.getButtons(i):
            button.setScale(1.25)
    
    def __exitButton(self, i, event=None):
        for button in self.getButtons(i):
            button.setScale(1)
    
    def __choose(self, i):
        self.destroyDialog()
        self.hide()
        
        self.chosen = i
        self.dialog = PDialog.PDialog(parent=aspect2dp, text=PLocalizer.MakeAPirateFactionConfirm % PLocalizer.FactionArticulatedNames[i], style=OTPDialog.YesNo, command=self.__confirm)
        self.dialog.setBin('gui-popup', 5)

    def __confirm(self, done):
        self.destroyDialog()

        if done == DGG.DIALOG_CANCEL:
            self.show()
            base.transitions.fadeScreen(0.25)
            return
        
        self.callback(self.chosen)