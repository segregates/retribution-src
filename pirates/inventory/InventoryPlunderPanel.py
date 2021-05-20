from panda3d.core import NodePath, Point3, TextNode
from direct.gui.DirectGui import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals, GuiButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
import InventoryUIPlunderGridContainer

class InventoryPlunderPanel(DirectFrame):

    def __init__(self, manager, plunderList, rating, typeName, timer = 0):
        self.manager = manager
        self.sizeX = 1.0
        self.sizeZ = 0.8
        gui = loader.loadModel('models/gui/toplevel_gui')
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None), ('image', gui.find('**/main_gui_quest_scroll'), None), ('image_pos', (0.5, 0.0, 0.45), None), ('image_scale', (0.5, 1.0, 0.75), None), ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None))
        self.defineoptions({ }, optiondefs)
        DirectFrame.__init__(self, parent = NodePath())
        self.initialiseoptions(InventoryPlunderPanel)
        self.plunderList = plunderList
        self.rating = rating
        self.typeName = typeName
        self.timer = timer
        self.timerUI = None
        self.timerSound = None
        self.setup()


    def destroy(self):
        self.ignoreAll()
        if self.takeAllButton:
            self.takeAllButton.destroy()
            self.takeAllButton = None

        if self.timerUI:
            self.timerUI.destroy()
            self.timerUI = None
            taskMgr.removeTasksMatching(self.taskName('plunderPanelTimeUpdate'))

        DirectFrame.destroy(self)


    def setupPlunder(self, plunderList):
        self.grid.setupPlunder(plunderList)


    def setup(self):
        self.buttonSize = self.manager.standardButtonSize
        self.grid = InventoryUIPlunderGridContainer.InventoryUIPlunderGridContainer(self.manager, self.buttonSize * 7, self.buttonSize * 3.0, 2, 3)
        self.grid.reparentTo(self)
        self.grid.setPos(self.sizeX * 0.5 - self.grid.sizeX * 0.4, 0.0, 0.25)
        self.grid.setScale(0.8)
        Gui = loader.loadModel('models/gui/char_gui')
        buttonImage = (Gui.find('**/chargui_text_block_large'), Gui.find('**/chargui_text_block_large_down'), Gui.find('**/chargui_text_block_large_over'), Gui.find('**/chargui_text_block_large'))
        self.takeAllButton = GuiButton.GuiButton(parent = self, relief = None, image = buttonImage, image_scale = 0.4, text = PLocalizer.InventoryPlunderTakeAll, text_font = PiratesGlobals.getInterfaceOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.8, 0, 0.2), helpText = PLocalizer.InventoryPlunderGiveNothingBack, helpPos = (0.1, 0, -0.07), helpOpaque = 1, helpDelay = 1.0, command = self.takeAllLoot)
        if self.takeAllButton.helpBox:
            self.takeAllButton.helpBox.setPos(0.3, 0, -0.01)

        if self.timer:
            self.timerUI = DirectLabel(parent = self, relief = None, pos = (0.64, 0, 0.21), text = str(self.timer), text_align = TextNode.ACenter, text_font = PiratesGlobals.getInterfaceOutlineFont(), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_pos = (0.0, -0.02))
            self.takeAllButton.setPos(Point3(0.825, 0, 0.2))
            self.timerStart = globalClock.getRealTime()
            taskMgr.add(self._InventoryPlunderPanel__updateTimer, self.taskName('plunderPanelTimeUpdate'))

        maingui = loader.loadModel('models/gui/gui_main')
        box = (maingui.find('**/exit_button'), maingui.find('**/exit_button'), maingui.find('**/exit_button_over'), maingui.find('**/exit_button'))
        x = maingui.find('**/x2')

        self.titleLabel = DirectLabel(parent = self, relief = None, pos = (0.5, 0, 0.68), text = PLocalizer.InventoryPlunderTitle % self.typeName, text_align = TextNode.ACenter, text_font = PiratesGlobals.getInterfaceOutlineFont(), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_pos = (0.0, -0.02), image = maingui.find('**/gui_inv_treasure_loot_bg'), image_scale = (0.3, 0.35, 0.35), image_pos = (0.04, 0, 0))
        self.closeButton = DirectButton(parent = self, relief = None, pos = (self.sizeX + 0.25, 0, self.sizeZ - 1.08), image = box, image_scale = 0.5, geom = x, geom_scale = 0.25, geom_pos = (-0.32, 0, 0.958), command = self.manager.closePlunder)
        self.ratingLabel = DirectLabel(parent = self, relief = None, text = PLocalizer.InventoryPlunderRating, text_align = TextNode.ALeft, text_font = PiratesGlobals.getInterfaceFont(), text_fg = PiratesGuiGlobals.TextFG16, text_scale = PiratesGuiGlobals.TextScaleLarge, pos = (self.sizeX * 0.1, 0, 0.2))
        
        if self.rating < 0:
            self.ratingLabel.hide()
        else:
            toplevelgui = loader.loadModel('models/gui/toplevel_gui')
            rating = self.attachNewNode('rating')
            rating.setPos(self.sizeX * 0.35, 0, 0.21)
            for i in xrange(0, 5):
                skull = rating.attachNewNode('skull%s' % i)
                toplevelgui.find('**/pir_t_gui_gen_goldSkull').copyTo(skull)
                skull.setScale(0.2)
                skull.setX(i * 0.05)
                if i >= self.rating:
                    skull.setColor(0, 0, 0, 0.25)
                    continue

            rating.flattenStrong()
        self.setupPlunder(self.plunderList)
        self.accept('lootsystem-plunderContainer-Empty', self.checkAllContainers)


    def _InventoryPlunderPanel__updateTimer(self, task = None):
        timePassed = globalClock.getRealTime() - self.timerStart
        if timePassed > 15:
            self.timerUI['text'] = '0'
            return task.done
        else:
            newTime = str(int(max(0, 15 - timePassed)))
            if newTime != self.timerUI['text']:
                self.timerUI['text'] = newTime
                if not self.timerSound:
                    self.timerSound = loader.loadSfx('audio/sfx_can_ammochrgremind.ogg')

                self.timerSound.setVolume(1.0 * ((15 - int(newTime)) / 15.0))
                self.timerSound.play()

            return task.cont


    def checkAllContainers(self, event = None):
        numItems = 0
        
        for cell in self.grid.cellList:
            if cell.inventoryItem:
                numItems += 1

        if not numItems:
            self.manager.closePlunder()


    #def giveGold(self, gold):
    # if gold > 0:
    # self.b_setGoldInPocket(min(InventoryGlobals.GOLD_CAP, self.getGoldInPocket() + gold))

    def takeAllLoot(self, playSound = True):
        self.manager.takeAllLoot([self.grid], playSound = playSound)