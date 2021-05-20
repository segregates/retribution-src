from panda3d.core import VBase4
# File: S (Python 2.4)

from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ScoreFrame import ScoreFrame
from direct.gui.DirectGui import *
from pirates.piratesgui import BorderFrame
from direct.showbase.DirectObject import DirectObject

class SiegeBoard(DirectObject):

    def __init__(self, holder):
        pvpIcons = loader.loadModel('models/textureCards/pvp_arrow')
        self.holder = holder
        self.borderOne = BorderFrame.BorderFrame(relief = None, frameSize = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200, PiratesGuiGlobals.ScorePanelHeight * 0.5), modelName = 'pir_m_gui_frm_subframe', imageColorScale = VBase4(0.75, 0.75, 0.9, 0.75))
        self.borderOneSecondLayer = BorderFrame.BorderFrame(parent = self.borderOne, relief = None, frameSize = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200, PiratesGuiGlobals.ScorePanelHeight * 0.5), modelName = 'pir_m_gui_frm_subframe', imageColorScale = VBase4(0.75, 0.75, 0.9, 0.75))
        iconOne = DirectFrame(parent = self.borderOne, relief = None, image = pvpIcons.find('**/pir_t_gui_frm_pvpFrench'), image_scale = 0.200, image_pos = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.348, 0, PiratesGuiGlobals.ScorePanelHeight * 0.450))
        self.one = ScoreFrame(PiratesGuiGlobals.ScorePanelWidth - 0.200, PiratesGuiGlobals.ScorePanelHeight, holder, 1, sortOrder = 2)
        self.borderOne.setPos(-0.625, 0, -0.299)
        self.one.setPos(-1.05, 0, -1.10)
        self.borderOne.hide()
        self.one.hide()
        self.borderTwo = BorderFrame.BorderFrame(relief = None, frameSize = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200, PiratesGuiGlobals.ScorePanelHeight * 0.5), modelName = 'pir_m_gui_frm_subframe', imageColorScale = VBase4(0.75, 0.75, 0.9, 0.75))
        self.borderTwoSecondLayer = BorderFrame.BorderFrame(parent = self.borderTwo, relief = None, frameSize = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200, PiratesGuiGlobals.ScorePanelHeight * 0.5), modelName = 'pir_m_gui_frm_subframe', imageColorScale = VBase4(0.75, 0.75, 0.9, 0.75))
        self.borderTwo.setPos(-0.625 + PiratesGuiGlobals.ScorePanelWidth + 0.01, 0, -0.299)
        iconTwo = DirectFrame(parent = self.borderTwo, relief = None, image = pvpIcons.find('**/pir_t_gui_frm_pvpSpanish'), image_scale = 0.200, image_pos = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.348, 0, PiratesGuiGlobals.ScorePanelHeight * 0.450))
        self.two = ScoreFrame(PiratesGuiGlobals.ScorePanelWidth - 0.200, PiratesGuiGlobals.ScorePanelHeight, holder, 2, sortOrder = 2)
        self.two.setPos(-1.05 + PiratesGuiGlobals.ScorePanelWidth + 0.01, 0, -1.10)
        self.borderTwo.hide()
        self.two.hide()
        self.accept(self.holder.getItemChangeMsg(), self._updateBorders)


    def hide(self):
        self.borderOne.hide()
        self.one.hide()
        self.borderTwo.hide()
        self.two.hide()


    def show(self):
        self.borderOne.show()
        self.one.show()
        self.borderTwo.show()
        self.two.show()


    def destroy(self):
        self.ignore(self.holder.getItemChangeMsg())
        self.holder = None
        self.borderOne.hide()
        self.one.hide()
        self.borderTwo.hide()
        self.two.hide()
        self.borderOne.destroy()
        self.borderOne = None
        self.borderOneSecondLayer.destroy()
        self.borderOneSecondLayer = None
        self.one.destroy()
        self.one = None
        self.borderTwo.destroy()
        self.borderTwo = None
        self.borderTwoSecondLayer.destroy()
        self.borderTwoSecondLayer = None
        self.two.destroy()
        self.two = None


    def _updateBorders(self):
        self.borderOne['frameSize'] = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200 - (len(self.holder.getItemList(1)) - 1) * 0.100, PiratesGuiGlobals.ScorePanelHeight * 0.5)
        self.borderOneSecondLayer['frameSize'] = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200 - (len(self.holder.getItemList(1)) - 1) * 0.100, PiratesGuiGlobals.ScorePanelHeight * 0.5)
        self.borderTwo['frameSize'] = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200 - (len(self.holder.getItemList(2)) - 1) * 0.100, PiratesGuiGlobals.ScorePanelHeight * 0.5)
        self.borderTwoSecondLayer['frameSize'] = (-(PiratesGuiGlobals.ScorePanelWidth) * 0.4, PiratesGuiGlobals.ScorePanelWidth * 0.5, PiratesGuiGlobals.ScorePanelHeight * 0.5 - 0.200 - (len(self.holder.getItemList(2)) - 1) * 0.100, PiratesGuiGlobals.ScorePanelHeight * 0.5)
