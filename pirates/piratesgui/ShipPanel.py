from panda3d.core import TextNode
# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrameBottle import ShipFrameBottle
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesTimer

class ShipPanel(DirectFrame):
    Width = PiratesGuiGlobals.ShipPanelWidth
    Height = PiratesGuiGlobals.ShipPanelHeight

    def __init__(self, shipPage, shipId, **kwargs):
        self.shipPage = shipPage
        self.setShipId(shipId)
        self.timer = None
        self.crewDots = []
        self.lBroadsideLimit = 0
        self.rBroadsideLimit = 0
        kwargs.setdefault('relief', None)
        kwargs.setdefault('frameSize', (0, self.Width, 0, self.Height))
        DirectFrame.__init__(self)
        self.initialiseoptions(ShipPanel)
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestIcon = gui.find('**/icon_crate')
        cannonIcon = gui.find('**/topgui_icon_ship_cannon_single')
        broadsideIcon = gui.find('**/topgui_icon_ship_cannon_multiple')
        self.bottleFrame = ShipFrameBottle(parent = self, shipId = shipId, relief = None, state = DGG.DISABLED, pos = (0.074, 0, 0.75), scale = 0.83496)
        ornament = loader.loadModel('models/gui/gui_ship_window')
        ornament.reparentTo(self)
        ornament.setScale(0.299)
        ornament.setPos(0.540000, 0, 0.728)
        ornament.flattenStrong()
        self.nameLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(PLocalizer.EmptyBottle, 2), text_fg = PiratesGuiGlobals.TextFG1, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ACenter, text_shadow = (0, 0, 0, 1), text_wordwrap = 30, textMayChange = 1, text_font = PiratesGlobals.getPirateFont(), pos = (0.550000, 0, 1.22))
        self.classLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(PLocalizer.EmptyBottleDesc, 1), text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), text_wordwrap = 30, textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), pos = (0.550000, 0, 1.17))
        self.timer = PiratesTimer.PiratesTimer(showMinutes = True, mode = None, titleText = '', titleFg = '', infoText = '', cancelText = '', cancelCallback = None)
        self.timer.setFontColor(PiratesGuiGlobals.TextFG2)
        self.timer.reparentTo(self)
        self.timer.setPos(0.450, 0, 0.935)
        self.timer.setScale(0.598)
        self.timer.stash()
        self.hpMeter = DirectWaitBar(parent = self, relief = DGG.RAISED, state = DGG.DISABLED, range = 1, value = 0, frameColor = (0.0, 0.0, 0.0, 0.0), barColor = (0.100, 0.696, 0.100, 1), frameSize = (0, 0.31, 0, 0.018598), text = '', text_align = TextNode.ARight, text_scale = 0.0299, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), text_pos = (0.299, 0.0299), pos = (0.360, 0.0, 0.621), scale = 1.2)
        hpLabel = DirectLabel(parent = self.hpMeter, relief = None, state = DGG.DISABLED, text = PLocalizer.HP, text_scale = 0.0299, text_align = TextNode.ALeft, text_pos = (0.0149, 0.0299), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.speedMeter = DirectWaitBar(parent = self, relief = DGG.RAISED, state = DGG.DISABLED, range = 1, value = 0, frameColor = (0.0, 0.0, 0.0, 0.0), barColor = (0.696, 0.696, 0.100, 1), frameSize = (0, 0.31, 0, 0.018598), text = '', text_align = TextNode.ARight, text_scale = 0.0299, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), text_pos = (0.299, 0.0299), pos = (0.360, 0.0, 0.550000), scale = 1.2)
        speedLabel = DirectLabel(parent = self.speedMeter, relief = None, state = DGG.DISABLED, text = PLocalizer.Speed, text_scale = 0.0299, text_align = TextNode.ALeft, text_pos = (0.0149, 0.0299), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        textPos = (0.0, -0.16)
        self.plunderLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = chestIcon, geom_scale = 0.100, text = '', text_scale = 0.0448, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.200, 0, 0.31))
        plunderLabel = DirectLabel(parent = self.plunderLimit, relief = None, state = DGG.DISABLED, text = PLocalizer.Cargo, text_scale = 0.035, text_align = TextNode.ACenter, text_pos = (0, 0.149), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.cannonLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = cannonIcon, geom_scale = 0.450, text = '', text_scale = 0.0448, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.37, 0, 0.31))
        cannonLabel = DirectLabel(parent = self.cannonLimit, relief = None, state = DGG.DISABLED, text = PLocalizer.Cannon, text_scale = 0.035, text_align = TextNode.ACenter, text_pos = (0, 0.149), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.broadsideLeftLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = broadsideIcon, geom_scale = (-0.450, 0.450, 0.450), text = '', text_scale = 0.0448, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.739, 0, 0.31))
        self.broadsideRightLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = broadsideIcon, geom_scale = 0.450, text = '', text_scale = 0.0448, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.885, 0, 0.31))
        broadsideLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.Broadsides, text_scale = 0.035, text_align = TextNode.ACenter, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), pos = (0.810000, 0, 0.46))
        crewLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.Crew, text_scale = 0.035, text_align = TextNode.ALeft, text_pos = (0.47498, 0.46), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.crewLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = '', text_scale = 0.0448, text_align = TextNode.ACenter, text_pos = (0.560000, 0.149), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont())
        shipOV = base.cr.getOwnerView(self.shipId)
        if shipOV:
            self.setShipName(shipOV.name)
            self.setShipClass(shipOV.shipClass)
            self.setShipHp(shipOV.Hp, shipOV.maxHp)
            self.setShipSp(shipOV.Sp, shipOV.maxSp)
            self.setShipCrew(shipOV.crew, shipOV.maxCrew)
            self.setShipCargo([], shipOV.maxCargo)
            if hasattr(shipOV, 'cannonConfig'):
                self.setShipMaxCannons(shipOV.cannonConfig)
                self.setShipMaxLeftBroadside(shipOV.lBroadsideConfig)
                self.setShipMaxRightBroadside(shipOV.rBroadsideConfig)


        self.accept('setName-%s' % self.shipId, self.setShipName)
        self.accept('setShipClass-%s' % self.shipId, self.setShipClass)
        self.accept('setShipHp-%s' % self.shipId, self.setShipHp)
        self.accept('setShipSp-%s' % self.shipId, self.setShipSp)
        self.accept('setShipCargo-%s' % self.shipId, self.setShipCargo)
        self.accept('setShipCrew-%s' % self.shipId, self.setShipCrew)
        self.accept('setShipTimer-%s' % self.shipId, self.setShipTimer)
        self.accept('setHullCannonConfig-%s' % self.shipId, self.setShipMaxCannons)
        self.accept('setHullLeftBroadsideConfig-%s' % self.shipId, self.setShipMaxLeftBroadside)
        self.accept('setHullRightBroadsideConfig-%s' % self.shipId, self.setShipMaxRightBroadside)
        if config.GetBool('want-deploy-button', 0):
            pass
        1


    def destroy(self):
        self.ignoreAll()
        self.crewDots = []
        self.hullCards = []
        DirectFrame.destroy(self)


    def setShipId(self, shipId):
        self.shipId = shipId


    def getShipId(self):
        return self.shipId


    def setShipName(self, name, team = None):
        self.nameLabel['text'] = PLocalizer.makeHeadingString(name, 2)


    def setShipClass(self, shipClass):
        self.classLabel['text'] = PLocalizer.makeHeadingString(PLocalizer.ShipClassNames.get(shipClass), 1)


    def setShipHp(self, hp, maxHp):
        self.hpMeter['text'] = '%d/%d' % (hp, maxHp)
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp


    def setShipSp(self, sp, maxSp):
        self.speedMeter['text'] = '%d/%d' % (sp, maxSp)
        self.speedMeter['range'] = maxSp
        self.speedMeter['value'] = sp


    def setShipPlunderLimit(self, current, limit):
        self.plunderLimit['text'] = str(limit)


    def setShipCrew(self, crewArray, maxCrewCount):
        if len(self.crewDots) != maxCrewCount:
            for dot in self.crewDots:
                dot.destroy()

            self.crewDots = []

        if not self.crewDots:
            gui = loader.loadModel('models/gui/toplevel_gui')
            crewDotGeom = [
                gui.find('**/topgui_icon_ship_crewdot_off'),
                gui.find('**/topgui_icon_ship_crewdot_on')]
            columns = 2
            for x in xrange(maxCrewCount):
                crewDot = DirectButton(parent = self, relief = None, geom = (crewDotGeom[1], crewDotGeom[1], crewDotGeom[1], crewDotGeom[0]), pos = (0.540000 + 0.0400 * (x % columns), 0, 0.41798 - 0.0400 * (x / columns)), scale = 0.5)
                self.crewDots.append(crewDot)


        crewCount = len(crewArray)
        for x in xrange(maxCrewCount):
            if crewCount > x:
                self.crewDots[x]['state'] = DGG.NORMAL
                continue
            self.crewDots[x]['state'] = DGG.DISABLED

        self.crewLimit['text'] = '%d/%d' % (crewCount, maxCrewCount)


    def setShipCargo(self, cargo, maxCargo):
        self.plunderLimit['text'] = str(maxCargo)


    def setShipTimer(self, timeLeft):
        if timeLeft:
            self.timer.unstash()
            self.timer.countdown(timeLeft)
        else:
            self.timer.timerExpired()
            self.timer.stop()
            self.timer.stash()


    def setShipMaxCannons(self, cannonConfig):
        self.cannonLimit['text'] = str(len(cannonConfig) - cannonConfig.count(0))


    def setShipMaxLeftBroadside(self, broadsideConfig):
        self.lBroadsideLimit = len(broadsideConfig)
        self.broadsideLeftLimit['text'] = '%d' % (self.lBroadsideLimit - broadsideConfig.count(0))


    def setShipMaxRightBroadside(self, broadsideConfig):
        self.rBroadsideLimit = len(broadsideConfig)
        self.broadsideRightLimit['text'] = '%d' % (self.rBroadsideLimit - broadsideConfig.count(0))
