from panda3d.core import TextNode, VBase3
# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui.ShipFrame import ShipFrame
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesgui.ShipSnapshot import ShipSnapshot
from pirates.ship import ShipGlobals

class ShipFrameBoard(ShipFrame):

    def __init__(self, parent, **kw):
        gui = loader.loadModel('models/gui/toplevel_gui')
        image = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))
        optiondefs = (('relief', 0, None), ('frameSize', (0.0, 0.9, 0.0, 0.418), None), ('image', image[3], None), ('image_pos', (0.450, 0.0, 0.207), None), ('image_scale', (0.935, 1, 1.10), None), ('image_color', (0.800000, 0.800000, 0.800000, 1), None), ('frameColor', (1, 1, 1, 0.9), None), ('snapShotPos', (-0.0400, 0, -0.08), None), ('shipPos', VBase3(0.200, 0, 0.08), None), ('shipHpr', VBase3(-70, 6, 15), None), ('shipScale', VBase3(0.550000), None), ('time', 0, None), ('command', None, None), ('extraArgs', [], None))
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        self.defineoptions(kw, optiondefs)
        ShipFrame.__init__(self, parent)
        self.initialiseoptions(ShipFrameBoard)


    def destroy(self):
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        ShipFrame.destroy(self)


    def createGui(self):
        ShipFrame.createGui(self)
        self.nameLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(self['shipName'], 2), text_align = TextNode.ALeft, text_scale = 0.050000, text_pos = (0.0598, 0.0149), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, frameColor = PiratesGuiGlobals.ButtonColor1[3], frameSize = (self['frameSize'][0] + 0.0400, self['frameSize'][1] - 0.0299, -0.0, 0.050000), pos = (0, 0, self['frameSize'][3] - 0.089))
        self.classLabel = DirectLabel(parent = self.nameLabel, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(PLocalizer.ShipClassNames.get(self['shipClass']), 1), text_font = PiratesGlobals.getInterfaceFont(), text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_pos = (self.nameLabel['frameSize'][0] + 0.02, -0.0299))
        self.timer = PiratesTimer.PiratesTimer(showMinutes = True, mode = None, titleText = '', titleFg = '', infoText = '', cancelText = '', cancelCallback = None)
        self.timer.setFontColor(PiratesGuiGlobals.TextFG2)
        self.timer.reparentTo(self)
        self.timer.setScale(0.550000)
        self.timer.setPos(0.62, 0, 0.315)
        self.timer.unstash()
        self.timer.countdown(self['time'])
        self.mainText = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.LeadCrew, text_pos = (0.62, 0.200), text_font = PiratesGlobals.getInterfaceFont(), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 10, text_shadow = (0, 0, 0, 1), textMayChange = 1)
        gui = loader.loadModel('models/gui/toplevel_gui')
        geomCheck = gui.find('**/generic_check')
        self.yesButton = DialogButton(parent = self, buttonStyle = DialogButton.YES, pos = (0.5, 0, 0.08), text = PLocalizer.BoardShip, text_scale = PiratesGuiGlobals.TextScaleLarge, text_font = PiratesGlobals.getInterfaceFont(), text_pos = (0.035000, -0.014), geom = (geomCheck,) * 4, geom_pos = (-0.0598, 0, 0), geom_scale = 0.5, geom0_color = PiratesGuiGlobals.ButtonColor6[0], geom1_color = PiratesGuiGlobals.ButtonColor6[1], geom2_color = PiratesGuiGlobals.ButtonColor6[2], geom3_color = PiratesGuiGlobals.ButtonColor6[3], image3_color = (0.800000, 0.800000, 0.800000, 1), helpPos = (0, 0, -0.12), helpDelay = 0.299, command = self['command'], extraArgs = [
            True])
        self.noButton = DialogButton(parent = self, buttonStyle = DialogButton.NO, pos = (0.739, 0, 0.08), text = PLocalizer.ParlayShip, text_scale = PiratesGuiGlobals.TextScaleLarge, text_font = PiratesGlobals.getInterfaceFont(), text_pos = (0.035000, -0.014), helpPos = (0, 0, -0.12), helpDelay = 0.299, command = self['command'], extraArgs = [
            False])
        self.noButton.hide()


    def enableStats(self, shipName = '', shipClass = 0, mastInfo = [], hp = 0, sp = 0, cargo = 0, crew = 0, time = 0):
        pass
