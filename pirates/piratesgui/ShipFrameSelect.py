from panda3d.core import TextNode, VBase3, VBase4
# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrame import ShipFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.ShipSnapshot import ShipSnapshot

class ShipFrameSelect(ShipFrame):
    STOwn = 0
    STFriend = 1
    STBand = 2
    STGuild = 3
    STPublic = 4

    def __init__(self, parent, **kw):
        gui = loader.loadModel('models/gui/toplevel_gui')
        image = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))
        optiondefs = (('relief', 0, None), ('frameSize', (0.0, 0.9, 0.0, 0.418), None), ('image', image[3], None), ('image_pos', (0.450, 0.0, 0.207), None), ('image_scale', (0.935, 1, 1.10), None), ('image_color', (0.800000, 0.800000, 0.800000, 1), None), ('frameColor', (1, 1, 1, 0.9), None), ('snapShotPos', (-0.0400, 0, -0.08), None), ('shipPos', VBase3(0.760, 0, 0.149), None), ('shipHpr', VBase3(-70, 6, 15), None), ('shipScale', VBase3(0.550000), None), ('shipType', ShipFrameSelect.STOwn, None), ('command', None, None), ('extraArgs', [], None))
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        self.defineoptions(kw, optiondefs)
        ShipFrame.__init__(self, parent)
        self.initialiseoptions(ShipFrameSelect)


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
        self.typeLabel = DirectLabel(parent = self.nameLabel, relief = None, state = DGG.DISABLED, text = '', text_pos = (0.598, -0.0299), text_font = PiratesGlobals.getInterfaceFont(), text_scale = 0.0320, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), textMayChange = 0)
        self.stateLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = '', text_font = PiratesGlobals.getInterfaceFont(), text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), text_pos = (0.19, 0.070), text_scale = PiratesGuiGlobals.TextScaleLarge, textMayChange = 0)
        gui = loader.loadModel('models/gui/toplevel_gui')
        geomCheck = gui.find('**/generic_check')
        self.button = GuiButton(parent = self, pos = (0.739, 0, 0.08), text = PLocalizer.SelectShip, text_scale = PiratesGuiGlobals.TextScaleLarge, text_font = PiratesGlobals.getInterfaceFont(), text_pos = (0.035000, -0.014), geom = (geomCheck,) * 4, geom_pos = (-0.0598, 0, 0), geom_scale = 0.5, geom0_color = PiratesGuiGlobals.ButtonColor6[0], geom1_color = PiratesGuiGlobals.ButtonColor6[1], geom2_color = PiratesGuiGlobals.ButtonColor6[2], geom3_color = PiratesGuiGlobals.ButtonColor6[3], image3_color = (0.800000, 0.800000, 0.800000, 1), helpPos = (-0.4, 0, 0.0299), helpDelay = 0.299, command = self['command'], extraArgs = self['extraArgs'])


    def enableStatsOV(self, shipOV):
        self.snapShot = ShipSnapshot(self, shipOV, pos = self['snapShotPos'])
        typeStr = ''
        if shipOV.Hp <= 0:
            self.button['state'] = DGG.DISABLED
            stateStr = 'Ired%s' % PLocalizer.ShipSunk
            self['shipColorScale'] = VBase4(1, 0.4, 0.4, 1)
        elif shipOV.state in 'Off':
            self.button['state'] = DGG.NORMAL
            stateStr = PLocalizer.ShipInBottle
        else:
            self.button['state'] = DGG.NORMAL
            stateStr = PLocalizer.ShipAtSea
        self.typeLabel['text'] = 'smallCaps(%s)' % typeStr
