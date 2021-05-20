from panda3d.core import Vec4
# File: C (Python 2.4)

from direct.interval.IntervalGlobal import *
from pirates.piratesgui.CannonDefenseHelpPanel import CannonDefenseHelpPanel
from pirates.piratesbase import PLocalizer

class CannonDefenseHelpManager:

    def __init__(self, fadeLength):
        self.ammo = None
        self.mine = None
        self.ammoPanel = None
        self.wave = None
        self.exit = None
        self.help = None
        self._CannonDefenseHelpManager__createPanels()
        self._CannonDefenseHelpManager__createIntervals(fadeLength)


    def _CannonDefenseHelpManager__createPanels(self):
        self.ammo = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['AmmoHeader'], PLocalizer.CannonDefenseHelp['AmmoBody'], 13, 0.609, 0.550000)
        self.ammo.setPos(-0.100, 0, 1)
        self.ammo.arrow.setHpr(0, 0, 90)
        self.ammo.arrow.setPos(0.100, 0, -0.111)
        self.mine = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['MineHeader'], PLocalizer.CannonDefenseHelp['MineBody'], 12, 0.540000, 0.200)
        self.mine.setPos(0.31, 0, -0.25)
        self.mine.arrow.setHpr(0, 0, -90)
        self.mine.arrow.setPos(0.0400, 0, 0.311)
        self.ammoPanel = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['AmmoPanelHeader'], PLocalizer.CannonDefenseHelp['AmmoPanelBody'], 9, 0.450, 0.510)
        self.ammoPanel.setPos(0.200, 0, 0.0598)
        self.ammoPanel.arrow.setHpr(0, 0, -180)
        self.ammoPanel.arrow.setPos(-0.127, 0, 0.25)
        self.wave = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['WaveHeader'], PLocalizer.CannonDefenseHelp['WaveBody'], 13, 0.598, 0.25)
        self.wave.setPos(-1.55, -0.209, -0.299)
        self.wave.arrow.setPos(0.706, 0, 0.19)
        self.exit = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['ExitHeader'], None, 0, 0.44, 0.08)
        self.exit.setPos(-0.450, 0, 0.450)
        self.exit.arrow.setScale(0.598, 1.0, 0.598)
        self.exit.arrow.setHpr(0, 0, 90)
        self.exit.arrow.setPos(0.230, 0, -0.065)
        self.help = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['HelpHeader'], None, 0, 0.510, 0.085)
        self.help.setPos(-0.815, 0, 0.28000)
        self.help.arrow.setScale(0.299, 1.0, 0.299)
        self.help.arrow.setHpr(0, 0, 90)
        self.help.arrow.setPos(0.408, 0, -0.0299)


    def destroy(self):
        if self.mine:
            self.mine.remove_node()
            self.mine = None

        if self.ammoPanel:
            self.ammoPanel.remove_node()
            self.ammoPanel = None

        if self.ammo:
            self.ammo.remove_node()
            self.ammo = None

        if self.wave:
            self.wave.remove_node()
            self.wave = None

        if self.exit:
            self.exit.remove_node()
            self.exit = None

        if self.help:
            self.help.remove_node()
            self.help = None



    def _CannonDefenseHelpManager__createIntervals(self, length):
        opaque = Vec4(1, 1, 1, 1)
        transparent = Vec4(1, 1, 1, 0)
        self.fadeIn = Parallel(self.ammo.colorScaleInterval(length, opaque, transparent), self.mine.colorScaleInterval(length, opaque, transparent), self.ammoPanel.colorScaleInterval(length, opaque, transparent), self.wave.colorScaleInterval(length, opaque, transparent), self.exit.colorScaleInterval(length, opaque, transparent), self.help.colorScaleInterval(length, opaque, transparent))
        self.fadeOut = Parallel(self.ammo.colorScaleInterval(length, transparent), self.mine.colorScaleInterval(length, transparent), self.ammoPanel.colorScaleInterval(length, transparent), self.wave.colorScaleInterval(length, transparent), self.exit.colorScaleInterval(length, transparent), self.help.colorScaleInterval(length, transparent))
