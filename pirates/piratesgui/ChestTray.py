from panda3d.core import ModelNode, Point3, TextNode, VBase4
# File: C (Python 2.4)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import GuiTray, QuestPage
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GuiButton import GuiButton
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class ChestTray(GuiTray.GuiTray):
    WantClothingPage = config.GetBool('want-clothing-page', 0)
    if not config.GetBool('want-land-infamy', 0):
        pass
    WantTitlesPage = config.GetBool('want-sea-infamy', 0)

    def __init__(self, parent, parentMgr, **kw):
        GuiTray.GuiTray.__init__(self, parent, 0.6, 0.12)
        self.initialiseoptions(ChestTray)
        self.setBin('gui-fixed', 1)
        self.state = 0
        self.buttonsParent = self.attachNewNode(ModelNode('ChestTray.buttonsParent'), sort = 1)
        self.stickyButtonsParent = self.attachNewNode(ModelNode('ChestTray.stickyButtonsParent'), sort = 1)
        self.stickyButtonsParent.setPos(0, 0, 0.02)
        self.buttons = { }
        self.buildShowHideButtonsIvals()
        self.openSfx = loadSfx(SoundGlobals.SFX_GUI_OPEN_SEACHEST)
        self.openSfx.setVolume(0.4)
        self.closeSfx = loadSfx(SoundGlobals.SFX_GUI_CLOSE_SEACHEST)
        self.closeSfx.setVolume(0.4)
        gui = loader.loadModel('models/gui/toplevel_gui')
        gui_main = loader.loadModel('models/gui/gui_main')
        helpPos = (-0.26, 0, 0.06)
        helpDelay = 0
        self.buttonImage = gui.find('**/topgui_icon_box')
        self.buttonImageIn = gui.find('**/topgui_icon_box_in')
        self.buttonColors = (VBase4(0.7, 0.7, 0.7, 1), VBase4(0.8, 0.8, 0.8, 1), VBase4(1.0, 1.0, 1.0, 1), VBase4(0.6, 0.6, 0.6, 1))
        self.currentButtonIn = None
        self.highlightButtons = [
            'guiMgrToggleMap',
            'guiMgrToggleInventory',
            'guiMgrToggleWeapons',
            'guiMgrToggleLevels',
            'guiMgrToggleTreasures',
            'guiMgrToggleTitles',
            'guiMgrToggleShips',
            'guiMgrToggleQuest',
            'guiMgrToggleLookout',
            'guiMgrToggleMainMenu']
        buttonOptions = {
            'image': self.buttonImage,
            'geom': None,
            'relief': None,
            'frameSize': (0, 0.12, 0, 0.12),
            'image_scale': 0.47,
            'image_pos': (0.06, 0, 0.06),
            'image0_color': self.buttonColors[0],
            'image1_color': self.buttonColors[1],
            'image2_color': self.buttonColors[2],
            'image3_color': self.buttonColors[3],
            'geom_scale': 0.12,
            'geom_pos': (0.06, 0, 0.06),
            'command': self.togglePanel }
        extraHeight = 0
        if self.WantTitlesPage:
            extraHeight = 0.12

        self.friendButtonLight = gui.find('**/friend_button_over')
        buttonOptions['geom'] = None
        self.socialButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'f',
            'shift-f'], hotkeyLabel = 'F', helpText = PLocalizer.SocialButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleSocial'], pos = (-0.069, 0, 1.525 + extraHeight))
        self.buttons['guiMgrToggleSocial'] = self.socialButton
        self.highlightButton('guiMgrToggleSocial')
        self.friendButtonLightImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.friendButtonLight, scale = 0.135, pos = (-0.069, 0, 1.645))
        self.friendButtonLightImage.sourceImage = self.friendButtonLight

        self.compassSmallButtonLight = gui.find('**/compass_small_button_open_over')
        buttonOptions['geom'] = None
        self.radarButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'c',
            'shift-c'], hotkeyLabel = 'C', helpText = PLocalizer.RadarButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleRadar'], pos = (-0.069, 0, 1.392 + extraHeight))
        self.buttons['guiMgrToggleRadar'] = self.radarButton
        self.highlightButton('guiMgrToggleRadar')
        self.compassSmallButtonLightImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.compassSmallButtonLight, scale = 0.093, pos = (-0.069, 0, 1.510))
        self.compassSmallButtonLightImage.sourceImage = self.compassSmallButtonLight
        buttonPosZ = 0.48
        buttonHeight = 0.12
        if self.WantTitlesPage:
            buttonPosZ += buttonHeight

        self.worldMapButton = gui_main.find('**/world_map_icon')
        buttonOptions['geom'] = None
        self.mapButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'm',
            'shift-m'], hotkeyLabel = 'M', helpText = PLocalizer.MapButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleMap'], pos = (-0.07, 0, 1.325))
        self.buttons['guiMgrToggleMap'] = self.mapButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleMap')
        self.worldMapButtonImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.worldMapButton, scale = 0.107, pos = (-0.069, 0, 1.320))
        self.worldMapButtonImage.sourceImage = self.worldMapButton

        self.chestClosedLight = gui.find('**/treasure_chest_closed_over')
        buttonOptions['geom'] = None
        self.bagButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'i',
            'shift-i'], hotkeyLabel = 'I', helpText = PLocalizer.InventoryButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleInventory'], pos = (-0.07, 0, 1.192))
        self.buttons['guiMgrToggleInventory'] = self.bagButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleInventory')
        self.chestClosedLightImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.chestClosedLight, scale = 0.137, pos = (-0.069, 0, 1.190))
        self.chestClosedLightImage.sourceImage = self.chestClosedLight

        self.weaponIcon = gui.find('**/topgui_icon_weapons')
        buttonOptions['geom'] = None
        self.weaponButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'y',
            'shift-y'], hotkeyLabel = 'Y', helpText = PLocalizer.WeaponButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleWeapons'], pos = (-0.07, 0, 1.059))
        self.buttons['guiMgrToggleWeapons'] = self.weaponButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleWeapons')
        self.weaponIconImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.weaponIcon, scale = 0.140, pos = (-0.069, 0, 1.07))
        self.weaponIconImage.sourceImage = self.weaponIcon

        self.skillIcon = gui.find('**/topgui_icon_skills')
        buttonOptions['geom'] = None
        self.levelButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'k',
            'shift-k'], hotkeyLabel = 'K', helpText = PLocalizer.SkillButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleLevels'], pos = (-0.07, 0, 0.926))
        self.buttons['guiMgrToggleLevels'] = self.levelButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleLevels')
        self.skillIconImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.skillIcon, scale = 0.180, pos = (-0.069, 0, 0.925))
        self.skillIconImage.sourceImage = self.skillIcon

        if self.WantClothingPage:

            self.clothingIcon = gui.find('**/topgui_icon_clothing')
            buttonOptions['geom'] = None
            self.clothingButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeyLabel = '', helpText = PLocalizer.ClothingButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
                'guiMgrToggleClothing'], pos = (-0.07, 0, 0.793))
            self.buttons['guiMgrToggleClothing'] = self.clothingButton
            buttonPosZ -= buttonHeight
            self.highlightButton('guiMgrToggleClothing')
            self.clothingIconImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.clothingIcon, scale = 0.200, pos = (-0.069, 0, 0.790))
            self.clothingIconImage.sourceImage = self.clothingIcon

        if self.WantTitlesPage:
            self.infamyButton = gui.find('**/topgui_infamy_frame')
            buttonOptions['geom'] = None
            self.titlesButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
                'b',
                'shift-b'], hotkeyLabel = 'B', helpText = PLocalizer.TitlesButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
                'guiMgrToggleTitles'], pos = (-0.07, 0, 0.660))
            self.buttons['guiMgrToggleTitles'] = self.titlesButton
            buttonPosZ -= buttonHeight
            self.highlightButton('guiMgrToggleTitles')
            self.infamyButtonImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.infamyButton, scale = 0.190, pos = (-0.069, 0, 0.660))
            self.infamyButtonImage.sourceImage = self.infamyButton

        self.shipButton = gui.find('**/topgui_icon_ship')
        buttonOptions['geom'] = None
        self.shipsButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'h',
            'shift-h'], hotkeyLabel = 'H', helpText = PLocalizer.ShipsButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleShips'], pos = (-0.07, 0, 0.527))
        self.buttons['guiMgrToggleShips'] = self.shipsButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleShips')
        self.shipButtonImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.shipButton, scale = 0.170, pos = (-0.069, 0, 0.530))
        self.shipButtonImage.sourceImage = self.shipButton

        self.journalIcon = gui.find('**/topgui_icon_journal')
        buttonOptions['geom'] = None
        self.questButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'j',
            'shift-j'], hotkeyLabel = 'J', helpText = PLocalizer.QuestButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleQuest'], pos = (-0.07, 0, 0.394))
        self.buttons['guiMgrToggleQuest'] = self.questButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleQuest')
        self.journalIconImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.journalIcon, scale = 0.200, pos = (-0.071, 0, 0.400))
        self.journalIconImage.sourceImage = self.journalIcon

        self.lookoutButtonLight = gui.find('**/telescope_button_over')
        buttonOptions['geom'] = None
        self.lookoutButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'l',
            'shift-l'], hotkeyLabel = 'L', helpText = PLocalizer.LookoutButtonHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleLookout'], pos = (-0.07, 0, 0.261))
        self.buttons['guiMgrToggleLookout'] = self.lookoutButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleLookout')
        self.lookoutButtonLightImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.lookoutButtonLight, scale = 0.350, pos = (-0.069, 0.0, 0.256))
        self.lookoutButtonLightImage.sourceImage = self.lookoutButtonLight

        self.mainMenuIcon = gui.find('**/topgui_icon_main_menu')
        buttonOptions['geom'] = None
        self.mainMenuButton = GuiButton(command = self.togglePanel, parent = self.buttonsParent, hotkeys = [
            'f7',
            'escape'], hotkeyLabel = 'F7', helpText = PLocalizer.MainMenuIconHelp, helpPos = helpPos, helpDelay = helpDelay, extraArgs = [
            'guiMgrToggleMainMenu'], pos = (-0.07, 0, 0.128))
        self.buttons['guiMgrToggleMainMenu'] = self.mainMenuButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleMainMenu')
        self.mainMenuIconImage = OnscreenImage(parent = self.stickyButtonsParent, image = self.mainMenuIcon, scale = 0.170, pos = (-0.069, 0, 0.130))
        self.mainMenuIconImage.sourceImage = self.mainMenuIcon

        self.highlightButton('guiMgrToggleInventory')

        self.chestButtonClosed = (gui.find('**/treasure_chest_closed'), gui.find('**/treasure_chest_closed'), gui.find('**/treasure_chest_closed_over'))
        self.chestButtonOpen = gui.find('**/treasure_chest_open_over')
        self.chestButton = GuiButton(command = self.toggle, parent = self, relief = None, image = self.chestButtonClosed, image_scale = 0.15, image_pos = (0.065, 0, 0.06), scale = 1.2)
        self.chestHotkeyText = DirectLabel(parent = self.chestButton, relief = None, text = 'Tab', text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleSmall, text_pos = (0.125, 0.0), text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateBoldOutlineFont(), textMayChange = 1)
        self.buttonsParent.hide()
        self.socialButton.setScale(2.28)
        self.radarButton.setScale(2.26)
        self.mapButton.setScale(2.3)
        self.bagButton.setScale(2.3)
        self.weaponButton.setScale(2.3)
        self.levelButton.setScale(2.3)
        if self.WantClothingPage:
            self.clothingButton.setScale(2.3)
        self.titlesButton.setScale(2.3)
        self.shipsButton.setScale(2.3)
        self.questButton.setScale(2.3)
        self.lookoutButton.setScale(2.3)
        self.mainMenuButton.setScale(2.3)
        self.buttonsParent.setPos(0.2, 0, 0.14)
        self.chestButton.setPos(-.147, 0, .02)
        self.stickyButtonsParent.hide()
        self.stickyButtonsParent.setPos(0.2, 0, 0.14)
        gui.remove_node()

    def destroy(self):
        self.showButtonsIval.pause()
        del self.showButtonsIval
        self.hideButtonsIval.pause()
        del self.hideButtonsIval
        self.buttonsParent.remove_node()
        del self.buttonsParent
        self.stickyButtonsParent.remove_node()
        del self.stickyButtonsParent
        for button in self.buttons:
            self.buttons[button].destroy()

        del self.buttons
        loader.unloadSfx(self.openSfx)
        loader.unloadSfx(self.closeSfx)
        del self.openSfx
        del self.closeSfx
        GuiTray.GuiTray.destroy(self)

    def highlightButton(self, button):

        def changeButtonImage(button, image):
            button['image'] = image
            button['image0_color'] = self.buttonColors[0]
            button['image1_color'] = self.buttonColors[1]
            button['image2_color'] = self.buttonColors[2]
            button['image3_color'] = self.buttonColors[3]

        if self.currentButtonIn:
            changeButtonImage(self.buttons[self.currentButtonIn], self.buttonImage)

        self.currentButtonIn = button
        changeButtonImage(self.buttons[self.currentButtonIn], self.buttonImageIn)

    def togglePanel(self, message, args = None):
        if localAvatar.getInventory() == None:
            return None

        if message in self.highlightButtons:
            self.highlightButton(message)

        messenger.send(message, [
            args])

    def toggle(self):
        if not self.isHidden():
            messenger.send(PiratesGlobals.SeaChestHotkey)
            if localAvatar.guiMgr.questPage:
                chestPanel = localAvatar.guiMgr.chestPanel
                if chestPanel.currPageIndex:
                    currPage = chestPanel.pages[chestPanel.currPageIndex]

    def isOpen(self):
        return self.state

    def showButtons(self):
        if self.hideButtonsIval.isPlaying():
            self.hideButtonsIval.finish()

        self.showButtonsIval.start()

    def hideButtons(self):
        if self.showButtonsIval.isPlaying():
            self.showButtonsIval.finish()

        for button in self.buttons:
            self.buttons[button].hideDetails()

        self.hideButtonsIval.start()

    def slideOpen(self):
        if not self.state:
            self.openSfx.play()

        self.state = 1
        self.chestButton['image'] = self.chestButtonOpen
        self.showButtons()
        if localAvatar.guiMgr.questPage:
            chestPanel = localAvatar.guiMgr.chestPanel
            if chestPanel.currPageIndex:
                currPage = chestPanel.pages[chestPanel.currPageIndex]

    def slideClose(self):
        if self.state:
            self.closeSfx.play()

        self.state = 0
        self.chestButton['image'] = self.chestButtonClosed
        self.hideButtons()

    def buildShowHideButtonsIvals(self, includeSticky = True):
        showSequence = Sequence(Func(self.buttonsParent.show))
        showParallel = Parallel(LerpPosInterval(self.buttonsParent, 0.2, pos = Point3(0, 0, 0.14), startPos = self.buttonsParent.getPos, blendType = 'easeOut'))
        if includeSticky:
            showSequence.append(Func(self.stickyButtonsParent.show))
            showParallel.append(LerpPosInterval(self.stickyButtonsParent, 0.2, pos = Point3(0, 0, 0.14), startPos = self.stickyButtonsParent.getPos, blendType = 'easeOut'))

        showSequence.append(showParallel)
        self.showButtonsIval = showSequence
        hideParallel = Parallel(LerpPosInterval(self.buttonsParent, 0.2, pos = Point3(0.2, 0, 0.14), startPos = self.buttonsParent.getPos, blendType = 'easeIn'))
        hideSequence = Sequence(hideParallel, Func(self.buttonsParent.hide))
        if includeSticky:
            hideSequence.append(Func(self.stickyButtonsParent.hide))
            hideParallel.append(LerpPosInterval(self.stickyButtonsParent, 0.2, pos = Point3(0.2, 0, 0.14), startPos = self.stickyButtonsParent.getPos, blendType = 'easeIn'))

        hideSequence.append(hideParallel)
        self.hideButtonsIval = hideSequence

    def hideChestButton(self):
        self.chestButton.hide()

    def showChestButton(self):
        self.chestButton.show()
