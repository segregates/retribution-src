from panda3d.core import TextNode
# File: T (Python 2.4)

from direct.gui.DirectGui import *
from direct.gui.DirectGui import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ListFrame import ListFrame
from pirates.treasuremap.RewardItemGui import RewardItemGui

class TreasureMapCompletePanel(DirectFrame):

    def __init__(self, name, tm, results):
        self.width = PiratesGuiGlobals.TMCompletePanelWidth
        self.height = PiratesGuiGlobals.TMCompletePanelHeight
        DirectFrame.__init__(self, relief = DGG.RIDGE, state = DGG.NORMAL, frameColor = PiratesGuiGlobals.FrameColor, borderWidth = PiratesGuiGlobals.BorderWidth, frameSize = (0, self.width, 0, self.height))
        self.initialiseoptions(TreasureMapCompletePanel)
        self.results = results
        self.continueButton = DirectButton(parent = self, relief = DGG.FLAT, text = PLocalizer.ContinueTreasureButton, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.050000, 0.0448), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, frameColor = PiratesGuiGlobals.ButtonColor1, frameSize = (0, 0.5, 0, 0.100), pos = (1.5, 0, -0.12))
        self.continueButton['state'] = DGG.DISABLED
        self.endButton = DirectButton(parent = self, relief = DGG.FLAT, text = PLocalizer.ExitTreasureButton, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.089, 0.0448), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, frameColor = PiratesGuiGlobals.ButtonColor1, frameSize = (0, 0.5, 0, 0.100), command = tm.requestTreasureMapLeave, pos = (0.418, 0, -0.12))
        self.title = DirectLabel(parent = self, relief = None, text = name, text_align = TextNode.ACenter, text_scale = 0.089, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (1.2, 0, 1.55))
        self.list = ListFrame(PiratesGuiGlobals.TMCompletePageWidth, PiratesGuiGlobals.TMCompletePageHeight, name, self)
        self.list.setup()
        self.list.reparentTo(self)


    def destroy(self):
        self.list.destroy()
        del self.list
        DirectFrame.destroy(self)


    def getItemList(self):
        return self.getResults()


    def getItemChangeMsg(self):
        return self.taskName('tmRewardChanged')


    def createNewItem(self, item, parent, itemType = None, columnWidths = [], color = None):
        return RewardItemGui(item, parent)


    def getResults(self):
        return self.results
