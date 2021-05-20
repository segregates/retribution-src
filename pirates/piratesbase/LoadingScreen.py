from panda3d.core import ConfigVariable, ConfigVariableBool, TextNode, Texture, TransparencyAttrib
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from direct.showbase import DirectObject
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import NO_FADE_SORT_INDEX
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world.LocationConstants import *
from otp.otpbase import OTPGlobals
import random
tutorialShots = [
    'models/gui/loadingScreen_12',
    'models/gui/loadingScreen_16',
    'models/gui/loadingScreen_33',
    'models/gui/loadingScreen_34',
    'models/gui/loadingScreen_35',
    'models/gui/loadingScreen_36',
    'models/gui/loadingScreen_37']
tutorialShots_MoveAim = [
    'models/gui/loadingScreen_33',
    'models/gui/loadingScreen_36']
screenShots = [
    'models/gui/loadingScreen_01',
    'models/gui/loadingScreen_02',
    'models/gui/loadingScreen_05',
    'models/gui/loadingScreen_06',
    'models/gui/loadingScreen_07',
    'models/gui/loadingScreen_08',
    'models/gui/loadingScreen_09',
    'models/gui/loadingScreen_10',
    'models/gui/loadingScreen_11',
    'models/gui/loadingScreen_12',
    'models/gui/loadingScreen_13',
    'models/gui/loadingScreen_14',
    'models/gui/loadingScreen_15',
    'models/gui/loadingScreen_16',
    'models/gui/loadingScreen_17',
    'models/gui/loadingScreen_18',
    'models/gui/loadingScreen_19',
    'models/gui/loadingScreen_20',
    'models/gui/loadingScreen_21',
    'models/gui/loadingScreen_22',
    'models/gui/loadingScreen_24',
    'models/gui/loadingScreen_25',
    'models/gui/loadingScreen_26',
    'models/gui/loadingScreen_27',
    'models/gui/loadingScreen_28',
    'models/gui/loadingScreen_29',
    'models/gui/loadingScreen_30',
    'models/gui/loadingScreen_31',
    'models/gui/loadingScreen_32',
    'models/gui/loadingScreen_34']
screenShots_Jungles = [
    'models/gui/loadingScreen_13']
screenShots_Swamps = [
    'models/gui/loadingScreen_18']
screenShots_Caves = [
    'models/gui/loadingScreen_32',
    'models/gui/loadingScreen_30',
    'models/gui/loadingScreen_31',
    'models/gui/loadingScreen_26',
    'models/gui/loadingScreen_27',
    'models/gui/loadingScreen_29',
    'models/gui/loadingScreen_28',
    'models/gui/loadingScreen_22']
screenShots_WinterHoliday = [
    'models/gui/loadingScreen_38',
    'models/gui/loadingScreen_39',
    'models/gui/loadingScreen_40']
areaType_Jungles = {
    '1161798288.34sdnaik': 0,
    '1164141722.61sdnaik': 1,
    '1169592956.59sdnaik': 2,
    '1165004570.58sdnaik': 3,
    '1165009873.53sdnaik': 4,
    '1165009856.72sdnaik': 5,
    '1167857698.16sdnaik': 6,
    '1172209955.25sdnaik': 7 }
areaType_Swamps = {
    '1169179552.88sdnaik': 0,
    '1161732578.06sdnaik': 1 }
areaType_Caves = {
    '1164952144.06sdnaik': 0,
    '1165001772.05sdnaik': 1,
    '1158121765.09sdnaik': 2,
    '1167862588.52sdnaik': 3,
    '1168057131.73sdnaik': 4,
    '1164929110.98sdnaik': 5,
    '1172208344.92sdnaik': 6,
    '1245949184.0akelts': 7,
    '1235605888.0akelts': 8,
    '1228348366.44akelts': 9,
    '1245948731.45akelts': 10,
    '1245948708.12akelts': 11,
    '1245946851.97akelts': 12,
    '1245946794.3akelts': 13 }
screenShot_Dinghy = 'models/gui/loadingScreen_08'
screenShot_Jail = 'models/gui/loadingScreen_12'
screenShot_Weapon = 'models/gui/loadingScreen_35'
screenShot_Cutlass = 'models/gui/loadingScreen_37'
screenShot_EnterGame = 'models/gui/loadingScreen_enter'
screenShot_ExitGame = 'models/gui/loadingScreen_exit'
screenShots_Locations = {
    LocationIds.ANVIL_ISLAND: [
        'models/gui/loadingScreen_01'],
    LocationIds.ISLA_CANGREJOS: [
        'models/gui/loadingScreen_02',
        'models/gui/loadingScreen_10'],
    LocationIds.CUBA_ISLAND: [
        'models/gui/loadingScreen_05'],
    LocationIds.CUTTHROAT_ISLAND: [
        'models/gui/loadingScreen_06'],
    LocationIds.DEL_FUEGO_ISLAND: [
        'models/gui/loadingScreen_07'],
    LocationIds.DRIFTWOOD_ISLAND: [
        'models/gui/loadingScreen_09'],
    LocationIds.ISLA_PERDIDA: [
        'models/gui/loadingScreen_11'],
    LocationIds.KINGSHEAD_ISLAND: [
        'models/gui/loadingScreen_14'],
    LocationIds.OUTCAST_ISLE: [
        'models/gui/loadingScreen_19'],
    LocationIds.PORT_ROYAL_ISLAND: [
        'models/gui/loadingScreen_16'],
    LocationIds.RUMRUNNER_ISLE: [
        'models/gui/loadingScreen_17'],
    LocationIds.ISLA_TORMENTA: [
        'models/gui/loadingScreen_15'],
    LocationIds.TORTUGA_ISLAND: [
        'models/gui/loadingScreen_20'],
    LocationIds.ANVIL_CAVE_BARBOSA: [
        'models/gui/loadingScreen_22'],
    LocationIds.ISLA_AVARICIA: [
        'models/gui/loadingScreen_24'],
    LocationIds.ISLA_DE_PORC: [
        'models/gui/loadingScreen_25'],
    LocationIds.PORT_ROYAL_CAVE_A: [
        'models/gui/loadingScreen_32'],
    LocationIds.PORT_ROYAL_CAVE_B: [
        'models/gui/loadingScreen_30'],
    LocationIds.TORTUGA_CAVE: [
        'models/gui/loadingScreen_31'],
    LocationIds.DEL_FUEGO_CAVE_C: [
        'models/gui/loadingScreen_29'],
    LocationIds.DEL_FUEGO_CAVE_D: [
        'models/gui/loadingScreen_26'],
    LocationIds.DEL_FUEGO_CAVE_E: [
        'models/gui/loadingScreen_27'],
    LocationIds.TORMENTA_CAVE_B: [
        'models/gui/loadingScreen_28'],
    LocationIds.RAVENS_COVE_ISLAND: [
        'models/gui/loadingScreen_46']}
screenShots_WinterHolidayLocations = {
    LocationIds.DEL_FUEGO_ISLAND: [
        'models/gui/loadingScreen_38'],
    LocationIds.PORT_ROYAL_ISLAND: [
        'models/gui/loadingScreen_39'],
    LocationIds.TORTUGA_ISLAND: [
        'models/gui/loadingScreen_40'] }
screenShot_Potions = 'models/gui/loadingScreen_41'
screenShot_BenchRepair = 'models/gui/loadingScreen_42'
screenShot_ShipRepair = 'models/gui/loadingScreen_43'
screenShot_CannonDefense = 'models/gui/loadingScreen_44'
screenShot_Fishing = 'models/gui/loadingScreen_45'

def getOceanHint():
    oceans = [
        'Windward_Passage',
        'Brigand_Bay',
        'Bloody_Bayou',
        'Scurvy_Shallows',
        'Blackheart_Strait',
        'Salty_Flats',
        'Mar_de_Plata',
        'Smugglers_Run',
        'The_Hinterseas',
        'Dead_Mans_Trough',
        'Leeward_Passage',
        'Boiling_Bay',
        'Mariners_Reef']
    ocean = random.choice(oceans)
    hints = PLocalizer.HintMap_Locations.get(ocean)
    if hints:
        hint = random.choice(hints)
    else:
        hint = random.choice(PLocalizer.Hints_General)
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


def getGeneralHint():
    return random.choice(PLocalizer.Hints_General)


def getPrivateeringHint():
    hint = random.choice(PLocalizer.Hints_Privateering)
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


def getHint(destId = None, level = None):
    if destId and level:
        type = random.choice([
            0,
            1,
            2])
        if type == 0:
            hints = PLocalizer.HintMap_Locations.get(destId)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        elif type == 1:
            hints = PLocalizer.HintMap_Levels.get(level)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    elif destId and not level:
        type = random.choice([
            0,
            1])
        if type == 0:
            hints = PLocalizer.HintMap_Locations.get(destId)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    elif level and not destId:
        type = random.choice([
            0,
            1])
        if type == 0:
            hints = PLocalizer.HintMap_Levels.get(level)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    else:
        hint = getGeneralHint()
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


class LoadingScreen(DirectObject.DirectObject):

    def __init__(self, parent):
        DirectObject.DirectObject.__init__(self)
        self.parent = parent
        self.state = False
        self.model = None
        self.wheel = None
        self.snapshot = None
        self.snapshotFrame = None
        self.currentTime = 0
        self.lastUpdateTime = globalClock.getRealTime()
        self.locationLabel = None
        self.locationText = None
        self.hintLabel = None
        self.hintText = None
        self.allowLiveFlatten = ConfigVariableBool('allow-live-flatten')
        self.title_art = []
        self.tempVolume = []

    def startLoading(self):
        pass

    def beginStep(self, stageName, amt = 0, percent = 0):
        self.update()

    def endStep(self, stageName):
        self.update()

    def tick(self, tickNumber=1):
        # tickNumber doesn't do squat on
        # the original loading screen
        self.update()

    def destroy(self):
        for part in (self.model, self.snapshot):
            if part is not None:
                tex = part.findTexture('*')
                if tex:
                    tex.releaseAll()

                part.remove_node()
                continue

        self.model = None
        self.snapshot = None
        if self.snapshotFrame:
            self.snapshotFrame.destroy()

        if self.locationLabel:
            self.locationLabel.destroy()

        if self.hintLabel:
            self.hintLabel.destroy()

        taskMgr.remove('updateLoadingScreen')
        self.ignoreAll()

    def showTitleFrame(self):
        if config.GetBool('no-loading-screen', 0):
            return None

        for part in self.title_art:
            part.show()

    def hideTitleFrame(self):
        for part in self.title_art:
            part.hide()

    def show(self, waitForLocation = False, disableSfx = True, expectedLoadScale = 1.0):
        if self.state or config.GetBool('no-loading-screen', 0):
            return None

        self.startLoading()
        render.hide()
        self.state = True
        gsg = base.win.getGsg()
        if gsg:
            gsg.setIncompleteRender(False)

        base.setTaskChainNetNonthreaded()
        self.allowLiveFlatten.setValue(1)
        self.model = loader.loadModel('models/gui/loading_screen')
        self.locationLabel = DirectLabel(parent = aspect2dp, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = PiratesGuiGlobals.TextScaleTitleJumbo * 0.7, text_align = TextNode.ACenter, pos = (0.0, 0.0, -0.52), textMayChange = 1)
        self.hintLabel = DirectLabel(parent = aspect2dp, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = PiratesGuiGlobals.TextScaleTitleJumbo * 0.5, text_align = TextNode.ACenter, pos = (0.0, 0.0, -0.8), text_wordwrap = 30, textMayChange = 1)
        self.wheel = self.model.find('**/red_wheel')
        self.oLogo = self.model.find('**/banner_logo')
        self.oSkull = self.model.find('**/skull')
        self.oLogo.hide()
        self.oSkull.hide()
        title_bg = self.model.find('**/title_bg')
        title_frame = self.model.find('**/title_frame')
        self.title_art.append(title_bg)
        self.title_art.append(title_frame)
        self.hideTitleFrame()
        if not waitForLocation:
            if self.snapshot is None:
                screenshot = random.choice(tutorialShots_MoveAim)
                self.__setLoadingArt(screenshot)

            if self.snapshot:
                self.snapshot.show()

        elif self.snapshot:
            self.snapshot.show()

        self.snapshotFrame = DirectFrame(parent = aspect2dp, relief = DGG.FLAT, frameColor = (0.0, 0.0, 0.0, 1.0), frameSize = (-2.0, 2.0, 2.0, -2.0))
        self.snapshotFrame.setBin('fixed', 0)
        self.model.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.locationLabel.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.hintLabel.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.model.setScale(0.25, 0.25, 0.25)
        self.model.setPos(0.0, 0.0, -0.15)

        if config.GetBool('loading-screenlogo', 0):
            self.logo = OnscreenImage(image = 'custom/PORLogo.png', pos = (-0.12, 0, 3.5), scale = (1.4, 1.25, 1.25), parent = self.model)
            self.logo.setTransparency(TransparencyAttrib.MAlpha)

        if self.locationText and len(self.locationText):
            self.__setLocationText(self.locationText)

        if self.hintText is not None:
            if len(self.hintText):
                self.__setHintText(self.hintText)

        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        taskMgr.add(self.update, 'updateLoadingScreen', priority = -100)
        if base.sfxManagerList and disableSfx:
            index = 0
            while index < len(base.sfxManagerList):
                sfx_manager = base.sfxManagerList[index]
                sfx_manager.setVolume(0.0)
                index += 1

    def showHint(self, destId = None, ocean = False):
        if config.GetBool('no-loading-screen', 0):
            return None

        if ocean:
            hint = getOceanHint()
        elif hasattr(base, 'localAvatar'):
            totalReputation = 0
            level = base.localAvatar.getLevel()
            if totalReputation:
                hint = getHint(destId, level)
            else:
                hint = getHint(destId)
        else:
            hint = getHint()
        shipPVPIslands = [
            '1196970035.53sdnaik',
            '1196970080.56sdnaik']
        if (destId in shipPVPIslands or ocean) and base.localAvatar.getCurrentIsland() in shipPVPIslands:
            hint = getPrivateeringHint()

        if self.parent and base.localAvatar.style.getTutorial() == PiratesGlobals.TUT_MET_JOLLY_ROGER:
            hint = '%s:  %s' % (PLocalizer.LoadingScreen_Hint, PLocalizer.GeneralTip7)

        self.__setHintText(hint)

    def update(self, task = None):
        if not self.state:
            return Task.cont

        realTime = globalClock.getRealTime()
        if realTime - self.lastUpdateTime < 0.1:
            return Task.cont

        self.currentTime += min(10, (realTime - self.lastUpdateTime) * 250)
        self.lastUpdateTime = realTime
        self.wheel.setR(-(self.currentTime))
        base.graphicsEngine.renderFrame()
        return Task.cont

    def hide(self):
        if not self.state:
            return None

        render.show()
        base.graphicsEngine.renderFrame()
        self.state = False
        self.currentTime = 0
        self.locationText = None
        self.hintText = None
        gsg = base.win.getGsg()
        if gsg:
            gsg.setIncompleteRender(True)
            render.prepareScene(gsg)
            render2d.prepareScene(gsg)

        for part in (self.model, self.snapshot):
            if part:
                tex = part.findTexture('*')
                if tex:
                    tex.releaseAll()

                part.remove_node()
                continue

        self.model = None
        self.snapshot = None

        if self.snapshotFrame:
            self.snapshotFrame.destroy()

        if self.locationLabel:
            self.locationLabel.destroy()

        if self.hintLabel:
            self.hintLabel.destroy()

        taskMgr.remove('updateLoadingScreen')
        self.allowLiveFlatten.clearValue()
        base.setTaskChainNetThreaded()
        if base.sfxManagerList:
            index = 0
            while index < len(base.sfxManagerList):
                sfx_manager = base.sfxManagerList[index]
                sfx_manager.setVolume(base.options.sound_volume)
                index += 1

        messenger.send('texture_state_changed')

    def showTarget(self, targetId = None, ocean = False, jail = False, pickapirate = False, exit = False, potionCrafting = False, benchRepair = False, shipRepair = False, cannonDefense = False, fishing = False):
        if config.GetBool('no-loading-screen', 0):
            return None

        if pickapirate:
            screenshot = screenShot_EnterGame
        elif exit:
            screenshot = screenShot_ExitGame
        elif ocean:
            screenshot = screenShot_Dinghy
        elif jail:
            screenshot = screenShot_Jail
        elif potionCrafting:
            screenshot = screenShot_Potions
        elif benchRepair:
            screenshot = screenShot_BenchRepair
        elif shipRepair:
            screenshot = screenShot_ShipRepair
        elif cannonDefense:
            screenshot = screenShot_CannonDefense
        elif fishing:
            screenshot = screenShot_Fishing
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS:
            screenshot = screenShot_Weapon
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER:
            screenshot = screenShot_Cutlass
        elif base.cr.newsManager and base.cr.newsManager.getHoliday(17):
            screenshot = screenShots_WinterHolidayLocations.get(targetId)
            if not screenshot:
                screenshot = screenShots_Locations.get(targetId)

        else:
            screenshot = screenShots_Locations.get(targetId)

        if not screenshot:
            if targetId in areaType_Jungles:
                screenshot = random.choice(screenShots_Jungles)

            elif targetId in areaType_Swamps:
                screenshot = random.choice(screenShots_Swamps)

            elif targetId in areaType_Caves:
                screenshot = random.choice(screenShots_Caves)

            else:
                screenshot = random.choice(tutorialShots_MoveAim)

        if isinstance(screenshot, list):
            screenshot = random.choice(screenshot)

        self.__setLoadingArt(screenshot)
        if pickapirate:
            targetName = PLocalizer.LoadingScreen_PickAPirate
        elif exit:
            targetName = None
        elif ocean:
            targetName = PLocalizer.LoadingScreen_Ocean
        elif jail:
            targetName = PLocalizer.LoadingScreen_Jail
        else:
            targetName = PLocalizer.LocationNames.get(targetId)

        if pickapirate:
            serverVersionText = config.GetString('server-version', 'no_version_set')
            self.__setHintText(serverVersionText)
            
        if targetName is None:
            return None

        if len(targetName):
            self.__setLocationText(targetName)

    def __setLoadingArt(self, screenshot):
        if self.snapshot:
            return None

        if self.parent and hasattr(base, 'localAvatar') and base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER and screenshot not in tutorialShots:
            screenshot = random.choice(tutorialShots)

        try:
            self.snapshot = loader.loadModel(screenshot)
        except:
            self.snapshot = loader.loadModel('models/gui/loadingScreen_enter')
        if self.snapshot:
            self.snapshot.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.snapshot.setScale(2.15, 1, 1.2)
            self.snapshot.setPos(0.0, 0.0, 0.09)
            self.snapshot.setBin('fixed', 1)
            if not self.__isVisible():
                self.snapshot.hide()

    def __setLocationText(self, locationText):
        self.locationText = locationText
        if self.__isVisible():
            self.locationLabel['text'] = locationText
            self.locationLabel.show()
            self.showTitleFrame()

        launcher.setValue('gameLocation', self.locationText)

    def __setHintText(self, hintText):
        self.hintText = hintText
        if self.__isVisible():
            self.hintLabel['text'] = hintText
            self.hintLabel.show()

    def __isVisible(self):
        return self.state

    def scheduleHide(self, function):
        base.cr.queueAllInterestsCompleteEvent()
        self.acceptOnce(function, self.hide)
