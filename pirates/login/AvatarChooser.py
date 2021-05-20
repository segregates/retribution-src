from panda3d.core import NodePath, Point3, TPHigh, VBase3, TPLow, TextNode, TransparencyAttrib, Vec3, Vec4, invert
import math, time
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.fsm.StateData import StateData
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals, OTPLocalizer
from pirates.piratesbase import PiratesGlobals, PLocalizer, TimeOfDayManager, TODGlobals
from pirates.pirate import Human, HumanDNA, DistributedDynamicHuman, DynamicHuman, Pirate
from pirates.piratesgui.GameOptions import GameOptions
from pirates.piratesgui import PiratesGuiGlobals, PDialog
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.ShardPanel import ShardPanel
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.seapatch.Reflection import Reflection
from pirates.makeapirate import NameGUI
from pirates.audio import SoundGlobals

APPROVED = 1
DENIED = 2

class AvatarChooser(DirectObject, StateData):

    def __init__(self, parentFSM, doneEvent):
        StateData.__init__(self, doneEvent)
        self.choice = 0
        self.gameOptions = None
        self.av = None
        self.deleteConfirmDialog = None
        self.notifications = { }
        self.frame = None
        self.avFrame = None
        self.avButtons = []
        self.handleDialogOnScreen = 0
        self.lastMousePos = (0, 0)
        self.finalizeConfirmDialog = None
        self.deniedConfirmDialog = None
        base.loadingScreen.tick(tickNumber = 150)

    def enter(self):
        taskMgr.setupTaskChain('phasePost', threadPriority = TPHigh)
        if self.isLoaded == 0:
            self.load()

        base.disableMouse()
        self.quitButton.show()
        self.scene.reparentTo(render)
        camera.reparentTo(render)
        camera.setPosHpr(-29.0187, 37.0125, 24.75, 4.09, 1.0, 0.0)
        if self.ship:
            taskMgr.add(self.__shipRockTask, 'avatarChooserShipRockTask')

        base.transitions.fadeScreen(1)
        base.transitions.fadeIn(3)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.cr.loadingScreen.hide()
        globalClock.tick()
        base.graphicsEngine.renderFrame()
        base.playSfx(self.oceanSfx, looping = 1, volume = 0.60)
        base.musicMgr.request(SoundGlobals.MUSIC_AVATAR_CHOOSER, volume = 0.4, priority = -2)
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.accept('mouse3', self._startMouseReadTask)
        self.accept('mouse3-up', self._stopMouseReadTask)
        self.accept('updatedDeletedAvList', self.__updatedDeletedAvs)
        if not self.disableOptions:
            self.accept('f7', self.__handleOptions)

        self.__allPhasesComplete()

    def exit(self):
        if self.isLoaded == 0:
            return

        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_AVATAR_CHOOSER)
        self.oceanSfx.stop()
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
            self.deleteConfirmDialog = None

        self.avatarListFrame.hide()
        self.highlightFrame.hide()
        self.quitFrame.hide()
        self.renameButton.hide()
        self.scene.detachNode()
        if self.ship:
            taskMgr.remove('avatarChooserShipRockTask')

        self.ignore('mouse1')
        self.ignore('mouse1-up')
        self.ignore('mouse3')
        self.ignore('mouse3-up')
        self.ignore('f7')
        self.ignore('updatedDeletedAvList')
        self._stopMouseReadTask()
        self.ignoreAll()
        if hasattr(self, 'fadeInterval'):
            self.fadeInterval.pause()
            del self.fadeInterval

        if hasattr(self, 'fadeFrame'):
            self.fadeFrame.destroy()

        taskMgr.setupTaskChain('phasePost', threadPriority = TPLow)

    def load(self):
        if self.isLoaded == 1:
            return

        self.disableOptions = config.GetBool('disable-pirates-options', False)
        base.musicMgr.load(SoundGlobals.MUSIC_AVATAR_CHOOSER)
        self.model = loader.loadModel('models/gui/avatar_chooser_rope')
        charGui = loader.loadModel('models/gui/char_gui')
        self.oceanSfx = SoundGlobals.loadSfx(SoundGlobals.SFX_FX_OCEAN_LOOP)
        self.exclam = charGui.find('**/chargui_exclamation_mark')
        self.scene = NodePath('AvatarChooserScene')
        self.todManager = TimeOfDayManager.TimeOfDayManager()
        self.todManager.request('EnvironmentTOD')
        
        if config.GetBool('want-spooky-avatarchooser', False):
            self.todManager.switchJollyMoon(True)
            self.todManager.setEnvironment(TODGlobals.ENV_CURSED_NIGHT, { })
        else:
            self.todManager.setEnvironment(TODGlobals.ENV_DEFAULT, {})

        self.todManager.doEndTimeOfDay()
        self.todManager.skyGroup.setSunTrueAngle(Vec3(260, 0, 15))
        self.todManager.skyGroup.setSunLock(1)
        self.todManager.skyGroup.dirLightSun.node().setColor(Vec4(0.9, 0.7, 0.8, 1))

        pier = loader.loadModel('models/islands/pier_port_royal_2deck')
        pier.setPosHpr(-222.23, 360.08, 15.06, 251.57, 0.0, 0.0)
        pier.flattenStrong()
        pier.reparentTo(self.scene)
        pier2 = loader.loadModel('models/islands/pier_port_royal_1deck')
        pier2.setPosHpr(-35.0, 83.27, 19.26, 274.09, 0.0, 0.0)
        pier2.setScale(0.4, 0.3, 0.4)
        pier2.flattenStrong()
        pier2.reparentTo(self.scene)
        self.water = SeaPatch(render, Reflection.getGlobalReflection(), todMgr = None)
        self.water.updateWater(2)
        self.water.enable()
        self.ship = None
        from pirates.ship import ShipGlobals
        
        if config.GetInt('custom-avatarchooser-ship', 0) > 0:
            self.ship = base.shipFactory.getShip(config.GetInt('custom-avatarchooser-ship', 0))
        elif config.GetBool('want-spooky-avatarchooser', False):
            self.ship = base.shipFactory.getShip(ShipGlobals.P_SKEL_PHANTOM)
            self.ship.playStormEffect()
        else:
            self.ship = base.shipFactory.getShip(ShipGlobals.INTERCEPTORL1)

        self.ship.modelRoot.setPosHpr(140.86, 538.97, -3.62, -133.04, 0.0, 0.0)
        self.ship.modelRoot.reparentTo(self.scene)
        self.shipRoot = self.ship.modelRoot
        self.ship.playIdle()
        lodNode = self.ship.lod.node()
        self.ship.lod.node().forceSwitch(0)

        self.avatarListFrame = DirectFrame(parent = base.a2dTopLeft, relief = None)
        self.ropeFrame = DirectFrame(parent = self.avatarListFrame, relief = None, image = self.model.find('**/avatar_c_A_rope'), image_scale = 0.36, pos = (0, 0, -0.015))
        self.frame = BorderFrame(parent = self.avatarListFrame, frameSize = (-0.25, 0.25, -0.04, 0.09), borderScale = 0.2, pos = (0, 0, -0.16), modelName = 'general_frame_f')
        triangleGui = loader.loadModel('models/gui/triangle')
        triangleModel = [triangleGui.find('**/triangle' + name) for name in ('', '_down', '_over')]
        self.label = DirectLabel(parent = self.frame, relief = None, text = '', text_scale = 0.05, text_fg = (1, 0.9, 0.7, 0.9), text_pos = (0, 0.015), textMayChange = 1)

        self.versionLabel = DirectLabel(parent = base.a2dTopRight, relief = None, text_scale = 0.04, text_fg = (1, 1, 1, 0.5), text = '%s\n%s' % (base.cr.getServerVersion(), base.win.getPipe().getInterfaceName()), text_align = TextNode.ARight, pos = (-0.05, 0, -0.05))
        self.highlightFrame = DirectFrame(parent = base.a2dBottomCenter, relief = None, image = self.model.find('**/avatar_c_B_frame'), image_scale = 0.37, pos = (0, 0, 0.25), scale = 0.9)
        self.highlightFrame.hide()

        self.playButton = DirectButton(parent = self.highlightFrame, relief = None, text_scale = 0.05, text_fg = (0.7, 0.7, 0.7, 0.7), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLoading, image = (self.model.find('**/avatar_c_B_bottom'), self.model.find('**/avatar_c_B_bottom'), self.model.find('**/avatar_c_B_bottom_over')), image_scale = 0.37, text_pos = (0, -0.015), pos = (0, 0, -0.08), scale = 1.7, color = (0.7, 0.7, 0.7, 0.7), state = DGG.DISABLED, command = self.__handlePlay)
        self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
        self.playButton.setColor(1, 1, 1, 1)
        self.playButton['text_fg'] = (1.0, 0.9, 0.7, 0.9)
        self.accept('enter', self.__handleEnter)
        self.accept('arrow_up', self.__handleArrowUp)
        self.accept('arrow_down', self.__handleArrowDown)
        self.deleteButton = DirectButton(parent = self.highlightFrame, relief = None, text_scale = 0.045, text_fg = (1, 0.9, 0.7, 0.9), text_shadow = PiratesGuiGlobals.TextShadow, text = ('', '', PLocalizer.AvatarChooserDelete, ''), image = (self.model.find('**/avatar_c_B_delete'), self.model.find('**/avatar_c_B_delete'), self.model.find('**/avatar_c_B_delete_over')), image_scale = 0.37, text_pos = (0, -0.1), pos = (0.51, 0, -0.08), scale = 1.3, command = self.__handleDelete)
        self.quitFrame = DirectFrame(parent = base.a2dBottomRight, relief = None, image = self.model.find('**/avatar_c_C_back'), image_scale = 0.37, pos = (-0.4, 0, 0.21), scale = 0.9)
        self.quitFrameForeground = DirectFrame(parent = self.quitFrame, relief = None, image = self.model.find('**/avatar_c_C_frame'), image_scale = 0.37, pos = (0, 0, 0))
        if self.disableOptions:
            optionsState = DGG.DISABLED
        else:
            optionsState = DGG.NORMAL

        self.optionsButton = DirectButton(parent = self.quitFrame, relief = None, text_scale = 0.05, text_fg = (1, 0.9, 0.7, 0.9), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserOptions, image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.015), pos = (0, 0, 0.075), command = self.__handleOptions, state = optionsState)
        if self.disableOptions:
            self.optionsButton.setColorScale(Vec4(0.7, 0.7, 0.7, 0.7))

        self.quitButton = DirectButton(parent = self.quitFrame, relief = None, text_scale = 0.05, text_fg = (1, 0.9, 0.7, 0.9), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserQuit, image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.015), pos = (0, 0, -0.075), command = self.__handleQuit)
        self.renameButton = DirectButton(parent = base.a2dTopRight, relief = None, text_scale = 0.05, text_fg = (1, 0.9, 0.7, 0.9), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % 'rename', image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.015), pos = (-0.3, 0, -0.2), command = self.__handleRename)

        def shardSelected(shardId):
            base.cr.defaultShard = shardId

        self.shardPanel = ShardPanel(base.a2dBottomLeft, gear = NodePath('gear'), inverted = True, relief = None, scale = 0.85, hpr = Vec3(0, 0, 180), pos = Vec3(0.42, 0, 0.02), uppos = Vec3(0.42, 0, 0.02), downpos = Vec3(0.42, 0, 0.6), shardSelected = shardSelected, buttonFont = PiratesGlobals.getInterfaceFont())
        self.shardPanel.setScissor(self.highlightFrame, Point3(-20, 0, -0.18), Point3(20, 0, 1.0))
        self.shardPanelBottom = loader.loadModel('models/gui/general_frame_bottom')
        self.shardPanelBottom.setPos(0.42, 0, 0.095)
        self.shardPanelBottom.setScale(0.273)
        self.shardPanelBottom.reparentTo(base.a2dBottomLeft)

        self.logo = OnscreenImage(image = 'custom/PORLogo.png', pos = (0, 0, 0.08), scale = (0.4, 0.25, 0.25), parent = self.avatarListFrame)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        
        self.leftButton = DirectButton(self.highlightFrame, relief=None, image=triangleModel, image_scale=-0.18, pos=(-0.55, 0, -0.08), command=self.__increaseDelIndex, extraArgs=[-1])
        self.rightButton = DirectButton(self.highlightFrame, relief=None, image=triangleModel, image_scale=0.18, pos=(0.55, 0, -0.08), command=self.__increaseDelIndex, extraArgs=[1])
        self.leftButton.hide()
        self.rightButton.hide()
        
        self.recoverLabel = DirectLabel(base.a2dBottomLeft, relief = None, text_scale = 0.065, text_fg = (1.0, 0.9, 0.3, 0.9), text_shadow = PiratesGuiGlobals.TextShadow, text = '', pos=(0.415, 0, 0.65), text_wordwrap=9)

        self.updateAvatarList()
        charGui.remove_node()

    def __createAvatarButtons(self):
        if self.avFrame:
            self.avFrame.destroy()

        for button in self.avButtons:
            button.destroy()

        self.avFrame = DirectFrame(self.avatarListFrame, relief=None, pos=(0, 0, -0.3))
        self.avButtons = []
        spacing = -0.1
        
        for slot, av in enumerate(base.cr.avList):
            if slot == 0:
                z = -0.08
                textPos = (0, -0.02)
                image = (self.model.find('**/avatar_c_A_top'), self.model.find('**/avatar_c_A_top'), self.model.find('**/avatar_c_A_top_over'), self.model.find('**/avatar_c_A_top'))
            elif slot == len(base.cr.avList) - 1:
                z = slot * spacing - 0.125
                textPos = (0, 0.033)
                image = (self.model.find('**/avatar_c_A_bottom'), self.model.find('**/avatar_c_A_bottom'), self.model.find('**/avatar_c_A_bottom_over'), self.model.find('**/avatar_c_A_bottom'))
            else:
                z = slot * spacing - 0.08
                textPos = (0, -0.015)
                image = (self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle_over'), self.model.find('**/avatar_c_A_middle'))
            
            if not hasattr(av, 'name'):
                text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreate
            else:
                text = av.name

            self.avButtons.append(DirectButton(relief = None, parent = self.avFrame, state = DGG.NORMAL, text_fg = (1, 0.9, 0.7, 0.9), text_scale = 0.045, text_shadow = PiratesGuiGlobals.TextShadow, text = text, image = image, image_scale = 0.37, text_pos = textPos, pos = (0, 0, z), command = self.__handleHighlight, extraArgs = [slot]))

        self.isLoaded = 1

    def unload(self):
        if self.isLoaded == 0:
            return

        loader.unloadSfx(self.oceanSfx)
        del self.oceanSfx
        loader.unloadModel(self.model)
        self.model.remove_node()
        del self.model
        self.todManager.skyGroup.setSunLock(0)
        self.logo.remove_node()
        if self.av:
            self.av.delete()
            del self.av

        if self.ship:
            self.ship.destroy()
            self.ship = None
            taskMgr.remove('avatarChooserShipRockTask')
            self.shipRoot = None

        self.water.delete()
        del self.water
        self.scene.remove_node()
        del self.scene
        self.todManager.disable()
        self.todManager.delete()
        del self.todManager
        cleanupDialog('globalDialog')

        self.avatarListFrame.destroy()
        self.highlightFrame.destroy()
        self.quitFrame.destroy()
        self.renameButton.destroy()

        if self.gameOptions is not None:
            base.options = self.gameOptions.options
            self.gameOptions.destroy()
            del self.gameOptions

        self.versionLabel.destroy()
        del self.versionLabel
        self.shardPanel.destroy()
        del self.shardPanel
        self.shardPanelBottom.remove_node()
        self.ignoreAll()
        self.isLoaded = 0
        if self.finalizeConfirmDialog:
            self.finalizeConfirmDialog.destroy()
            self.finalizeConfirmDialog = None

        if self.deniedConfirmDialog:
            self.deniedConfirmDialog.destroy()
            self.deniedConfirmDialog = None
        
        self.leftButton.destroy()
        self.leftButton = None
        self.rightButton.destroy()
        self.rightButton = None
        self.recoverLabel.destroy()
        self.recoverLabel = None

    def getChoice(self):
        return self.choice

    def isEmpty(self):
        for av in base.cr.avList:
            if hasattr(av, 'name'):
                return False
        
        return True
    
    def __showHighlightedAvatar(self):
        av = base.cr.avList[self.choice]
        
        if not hasattr(av, 'name'):
            self.showAvatar()
        else:
            self.showAvatar(av.wishState, av.defaultShard, av.name, av.dna)
        
        self.__updatedDeletedAvs()
    
    def showAvatar(self, wishState='CLOSED', name='', defaultShard=0, dna=None):
        if self.av:
            self.av.cleanupHuman()
            self.av.delete()

        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
            self.deleteConfirmDialog = None

        self.av = DistributedDynamicHuman.DistributedDynamicHuman()
        self.av.doId = id(self.av)
        self.av.ghostGeomGenerated = 1
        self.av.setDNAString(dna)

        self.av.loadHuman(self.av.style.gender)
        self.av.setPosHpr(-29.69, 46.35, 22.05, 180.0, 0.0, 0.0)
        self.av.reparentTo(self.scene)
        self.av.loop('idle')
        self.av.useLOD(2000)
        
        if not dna:
            self.av.setGhostColor(1)
            self.av.startGhost(2)
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreatePirate
            self.playButton['command'] = self.__handleCreate
        else:
            if hasattr(base.cr.avList[self.choice], 'name'):
                self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
            else:
                self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserRecover

            self.playButton['command'] = self.__handlePlay

        self.highlightFrame.show()

        self.playButton['state'] = DGG.NORMAL
        self.renameButton.hide()

        if wishState == 'APPROVED':
            self.blockInput()
            self.finalizeConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserNameAccepted, style = OTPDialog.Acknowledge, command = self.__handleFinalize)
        elif wishState == 'DENIED' or wishState == 'OPEN':
            self.blockInput()
            if not self.handleDialogOnScreen:
                self.deniedConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserPleaseRename, style = OTPDialog.Acknowledge, command = self.__handleDenied)

            self.handleDialogOnScreen = 1
            self.renameButton.show()

        self.shardPanel['preferredShard'] = defaultShard

    def __hideHighlightedAvatar(self):
        if self.av:
            self.av.delete()
            self.av = None

        self.highlightFrame.hide()
        self.renameButton.hide()

    def __handleRename(self):
        self.enterNameMode()

    def __handleHighlight(self, slot):
        if self.choice == slot:
            return

        self.choice = slot

        for button in self.avButtons:
            button['text_fg'] = (1, 0.9, 0.7, 0.9)

        self.avButtons[slot]['text_fg'] = (1, 1, 1, 1)
        self.__showHighlightedAvatar()

    def __rotateHighlightedAvatar(self, val):
        if self.av:
            self.av.setH(val)

    def __handleArrowUp(self):
        if self.gameOptions is not None and not self.gameOptions.isHidden():
            return
        if self.isEmpty():
            return

        slot = self.choice

        numButtons = len(self.avButtons)

        if slot == 0:
            slot = numButtons - 1

        while not hasattr(base.cr.avList[slot], 'name'):
            if slot > 0:
                slot -= 1
            else:
                slot = numButtons - 1

        if self.avButtons[slot]['state'] == DGG.NORMAL:
            self.__handleHighlight(slot)

    def __handleArrowDown(self):
        if self.gameOptions is not None and not self.gameOptions.isHidden():
            return
        if self.isEmpty():
            return

        slot = self.choice
        numButtons = len(self.avButtons)

        if slot >= numButtons - 1:
            slot = 0

        while not hasattr(base.cr.avList[slot], 'name'):
            if slot >= numButtons - 1:
                slot = 0
            else:
                slot += 1

        if self.avButtons[slot]['state'] == DGG.NORMAL:
            self.__handleHighlight(slot)

    def __handleCreate(self):
        self.__avatarSlotResponse(self.choice)
        self.blockInput()

    def __avatarSlotResponse(self, slot):
        self.doneStatus = {
            'mode': 'create' }
        base.transitions.fadeOut(finishIval = Func(messenger.send, self.doneEvent, [
            self.doneStatus]))
        base.loadingScreen.showTarget(jail = True)
        base.loadingScreen.show()

    def __handleEnter(self):
        if self.playButton['state'] == DGG.NORMAL:
            self.playButton['command']()

    def __handlePlay(self):
        potAv = self.getChosenAvatar()
        base.emoteGender = potAv.dna.gender

        self.accept('playAvatarResponse', self.__playAvatarResponse)
        winInfo = base.win.getProperties()
        x = winInfo.getXSize()
        y = winInfo.getYSize()
        ratio = float(x) / y
        self.fadeFrame = DirectFrame(parent = aspect2dp, frameSize = (-1.0 * ratio, 1.0 * ratio, -1.0, 1.0))
        self.fadeFrame.setTransparency(1)
        self.fadeInterval = Sequence(Func(self.blockInput), Func(self.fadeFrame.show), LerpColorScaleInterval(self.fadeFrame, 0.3, Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.0, 0.0, 0.0, 0.0), blendType = 'easeInOut'), Func(base.transitions.fadeOut, t = 0), Func(base.cr.loginFSM.request, 'waitForSetAvatarResponse', [potAv, self.choice]))
        self.fadeInterval.start()

    def __playAvatarResponse(self, avatarId):
        slot = self.choice
        self.ignore('playAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.doneStatus = {
            'mode': 'chose' }
        messenger.send(self.doneEvent, [
            self.doneStatus])

    def __activatePlayButton(self):
        self.playButton['state'] = DGG.NORMAL
        self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
        self.playButton.setColor(1, 1, 1, 1)
        self.playButton['text_fg'] = (1.0, 0.9, 0.7, 0.9)

    def __activateCreateButtons(self):
        for i, potAv in enumerate(base.cr.avList):
            if not hasattr(potAv, 'name'):
                button = self.avButtons[i]
                button.setColorScale(1, 1, 1, 1)
                button['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreate
            else:
                button = self.avButtons[i]
                button.setColorScale(1, 1, 1, 1)
                button['text'] = '\x01smallCaps\x01%s\x02' % potAv.name

    def __allPhasesComplete(self):
        self.__activatePlayButton()
        self.__activateCreateButtons()

    def __handleDelete(self):
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()

        slot = self.choice
        potAv = base.cr.avList[slot]
        name = potAv.name
        self.blockInput()
        
        if len(self.deletedAvs) >= 6:
            self.deleteConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserCantDelete % name, style = OTPDialog.Acknowledge, command = self.__destroyDeleteConfirmation)
        else:
            self.deleteConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserConfirmDelete % name, style = OTPDialog.YesNo, command = self.__handleDeleteConfirmation)

    def __destroyDeleteConfirmation(self, value=None):
        self.deleteConfirmDialog.destroy()
        self.deleteConfirmDialog = None
        self.allowInput()

    def __handleDeleteConfirmation(self, value):
        self.__destroyDeleteConfirmation()
        if value == DGG.DIALOG_OK:
            slot = self.choice
            potAv = base.cr.avList[slot]
            self.accept('avDeleted', self.__removeAvatarResponse)
            base.cr.csm.sendDeleteAvatar(potAv.id)
            self.blockInput()

    def __removeAvatarResponse(self, avatarId):
        self.ignore('avDeleted')
        base.cr.cleanupWaitingForDatabase()
        base.cr.loginFSM.request('waitForAvatarList')

    def updateAvatarList(self):
        self.__hideHighlightedAvatar()
        self.__createAvatarButtons()

        self.showSub()
        self.choice = len(self.avButtons) - 1
        
        self.__handleArrowDown()

        if not self.handleDialogOnScreen:
            self.allowInput()

    def __handleOptions(self):
        width = 1.8
        height = 1.6
        x = -width / 2
        y = -height / 2
        self.gameOptions = GameOptions('Game Options', x, y, width, height, base.options, chooser = self)
        self.gameOptions.show()
        self.avatarListFrame.hide()

    def __handleQuit(self):
        from pirates.piratesgui.MainMenuConfirm import MainMenuConfirm
        self.areYouSureMenu = MainMenuConfirm("quit")

    def __shipRockTask(self, task):
        h = self.shipRoot.getH()
        p = 1.5 * math.sin(task.time * 0.9)
        r = 1.5 * math.cos(task.time * 1.1) + 1.5 * math.cos(task.time * 1.8)
        self.shipRoot.setHpr(h, p, r)
        return task.cont

    def blockInput(self):
        color = Vec4(0.7, 0.7, 0.7, 0.7)
        for button in self.avButtons: 
            button['state'] = DGG.DISABLED
            button.setColorScale(color)

        self.renameButton['state'] = DGG.DISABLED
        self.renameButton.setColorScale(color)
        self.quitButton['state'] = DGG.DISABLED
        self.quitButton.setColorScale(color)
        self.playButton['state'] = DGG.DISABLED
        self.playButton.setColorScale(color)
        self.deleteButton['state'] = DGG.DISABLED
        self.deleteButton.setColorScale(color)
        self.optionsButton['state'] = DGG.DISABLED
        self.optionsButton.setColorScale(color)

    def allowInput(self):
        for button in self.avButtons: 
            button['state'] = DGG.NORMAL
            button.clearColorScale()

        self.renameButton['state'] = DGG.NORMAL
        self.renameButton.clearColorScale()
        self.quitButton['state'] = DGG.NORMAL
        self.quitButton.clearColorScale()

        self.playButton['state'] = DGG.NORMAL
        self.playButton.clearColorScale()

        self.deleteButton['state'] = DGG.NORMAL
        self.deleteButton.clearColorScale()
        if not self.disableOptions:
            self.optionsButton['state'] = DGG.NORMAL
            self.optionsButton.clearColorScale()

        potAv = base.cr.avList[self.choice]

        if potAv and hasattr(potAv, 'name'):
            self.deleteButton['state'] = DGG.NORMAL
            self.playButton['state'] = DGG.NORMAL

    def __handleFinalize(self, value):
        slot = self.choice
        self.notifications[slot].remove_node()
        del self.notifications[slot]
        self.finalizeConfirmDialog.destroy()
        self.finalizeConfirmDialog = None
        potAv = base.cr.avList[slot]
        base.cr.csm.sendAcknowledgeName(potAv.id)
        potAv.name = potAv.wishName
        potAv.wishState = 'CLOSED'
        avButton = self.avButtons[slot]
        avButton['text'] = potAv.name
        self.allowInput()

    def __handleDenied(self, value):
        slot = self.choice
        self.notifications[slot].remove_node()
        del self.notifications[slot]
        self.deniedConfirmDialog.destroy()
        self.deniedConfirmDialog = None
        self.handleDialogOnScreen = 0
        potAv = base.cr.avList[slot]
        if potAv.wishState == 'DENIED':
            base.cr.csm.sendAcknowledgeName(potAv.id)
        self.allowInput()

    def enterNameMode(self):
        slot = self.choice
        self.quitFrame.setColorScale(Vec4(1, 1, 1, 0))
        self.highlightFrame.setColorScale(Vec4(1, 1, 1, 0))
        self.avatarListFrame.setColorScale(Vec4(1, 1, 1, 0))
        base.camera.setX(-26)
        self.frame.hide()
        av = base.cr.avList[slot]
        self.accept('q', self.exitNameMode)
        self.accept('NameGUIFinished', self.exitNameMode)
        self.renameButton.hide()
        self.nameGui = NameGUI.NameGUI(main = av, independent = True)
        self.nameGui.enter()

    def exitNameMode(self, value=0, name=None):
        def newList():
            base.cr.loginFSM.request('waitForAvatarList')
            if hasattr(self, 'sendingDialog'):
                self.sendingDialog.destroy()

        if name:
            base.cr.csm.sendNewName(value, name)
            self.sendingDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserNewName)
            self.blockInput()
            self.acceptOnce('newNameResp', newList)

        else:
            newList()
            if hasattr(self, 'renameButton') and self.renameButton:
                self.renameButton.show()
        
        if hasattr(self, 'nameGui'):
            self.nameGui.unload()
            del self.nameGui
        
        self.ignore('q')
        self.ignore('NameGUIFinished')
        
        if hasattr(self, 'quitFrame') and self.quitFrame:
            self.quitFrame.setColorScale(Vec4(1, 1, 1, 1))
            self.highlightFrame.setColorScale(Vec4(1, 1, 1, 1))
            self.avatarListFrame.setColorScale(Vec4(1, 1, 1, 1))
            self.frame.show()

        base.camera.setX(-29)

    def placeNotification(self, slot, pos, style):
        notification = self.exclam.copyTo(self.avatarListFrame)
        self.notifications[slot] = notification
        notification.setPos(pos[0], pos[1], pos[2])
        notification.setScale(0.14)
        notification.setR(25)

    def showSub(self):
        self.label['text'] = '\x01white\x01%s\x02' % base.cr.csm.username

        for i, potAv in enumerate(base.cr.avList):
            if hasattr(potAv, 'name'):
                if potAv.wishState == 'APPROVED':
                    self.placeNotification(i, (0.32, 0, -0.37 - i * 0.095), APPROVED)
                elif potAv.wishState in ('DENIED', 'OPEN'):
                    self.placeNotification(i, (0.32, 0, -0.37 - i * 0.095), DENIED)

        self.avatarListFrame.reparentTo(base.a2dTopLeft)
        self.avatarListFrame.setPosHprScale(0.42, 0, -0.3, 0, 0, 0, 1, 1, 1)

    def _stopMouseReadTask(self):
        taskMgr.remove('AvatarChooser-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'AvatarChooser-MouseRead')

    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            return task.cont
        winSize = (base.win.getXSize(), base.win.getYSize())
        mouseData = base.win.getPointer(0)
        dx = mouseData.getX() - self.lastMousePos[0]
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        if self.av:
            value = self.av.getH()
            value = (value + dx * 0.7) % 360
            self.__rotateHighlightedAvatar(value)

        return task.cont
    
    def __updatedDeletedAvs(self):
        if hasattr(base.cr, 'deletedAvList'):
            self.deletedAvs = base.cr.deletedAvList
        else:
            self.deletedAvs = []

        if not self.av:
            self.__handleHighlight(0)

        self.deletedChoice = -1
        self.decideButtons()
    
    def decideButtons(self):
        if self.deletedChoice == -1:
            self.recoverLabel['text'] = ''

        if hasattr(base.cr.avList[self.choice], 'name'):
            self.leftButton.hide()
            self.rightButton.hide()
            self.deleteButton.show()
            return
        
        if self.deletedChoice <= -1:
            self.leftButton.hide()
        else:
            self.leftButton.show()
        
        if self.deletedChoice >= (len(self.deletedAvs) - 1):
            self.rightButton.hide()
        else:
            self.rightButton.show()
        
        self.deleteButton.hide()
        
        if self.deletedChoice != -1:
            av = self.getChosenAvatar()
            
            if not av:
                return

            secondsLeft = max(0, av.position - int(time.time()))
            
            if not secondsLeft:
                text = PLocalizer.AvatarChooserReady
                self.playButton['state'] = DGG.NORMAL
                self.av.setGhostColor(2)
            else:
                text = PLocalizer.AvatarChooserRemaining % OTPLocalizer.getHumanTime(secondsLeft, 5)
                self.playButton['state'] = DGG.DISABLED
                self.av.setGhostColor(4)
            
            self.av.startGhost(1)
            self.recoverLabel['text'] = '\x01smallCaps\x01%s\n\n%s\x02' % (av.name, text)
    
    def getChosenAvatar(self):
        av = base.cr.avList[self.choice]
        
        if hasattr(av, 'name'):
            return av
        elif self.deletedChoice != -1:
            try:
                return self.deletedAvs[self.deletedChoice]
            except:
                pass
    
    def __increaseDelIndex(self, increment):
        self.deletedChoice += increment
        
        self.leftButton.hide()
        self.rightButton.hide()
        
        if self.deletedChoice == -1:
            self.showAvatar()
        else:
            av = self.getChosenAvatar()
            
            if av:
                self.showAvatar(av.wishState, av.name, av.defaultShard, av.dna)
        
        self.decideButtons()