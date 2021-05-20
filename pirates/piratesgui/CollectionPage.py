from panda3d.core import TextNode
# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import InventoryItemGui
from pirates.piratesgui import InventoryItemList
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import CollectionMap
from pirates.minigame import FishingGlobals

class CollectionPage(InventoryPage.InventoryPage):

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(CollectionPage)
        self.card = loader.loadModel('models/gui/treasure_gui')
        butcard = loader.loadModel('models/gui/lookout_gui')
        gui = loader.loadModel('models/gui/toplevel_gui')
        ornament = loader.loadModel('models/gui/gui_treasure_window_b')
        ornament.setPos(0.53000, 0, 0.71)
        ornament.setScale(0.315)
        ornament.reparentTo(self)
        ornament.flattenStrong()
        self.setLabel = DirectFrame(parent = self, relief = None, pos = (0.418, 0, 1.04), text = '', text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ALeft, text_scale = 0.050000)
        butImg = butcard.find('**/lookout_forward')
        self.backButton = DirectButton(parent = self, relief = None, image_scale = 0.179, image = butImg, pos = (0.348, 0, 1.0549), command = self.goMainPage, extraArgs = [])
        gui.remove_node()
        self.setPics = { }
        self.setFrames = { }
        self.setNum = { }
        self.setHowMany = { }
        self.currentDisplay = 0


    def goMainPage(self):
        base.localAvatar.guiMgr.showCollectionMain()


    def show(self):
        self.refreshList()
        InventoryPage.InventoryPage.show(self)


    def hide(self):
        InventoryPage.InventoryPage.hide(self)


    def clearList(self):
        for item in self.setFrames:
            self.setFrames[item].destroy()

        for item in self.setPics:
            self.setPics[item].destroy()

        for item in self.setNum:
            self.setNum[item].destroy()

        self.setLabel.destroy()
        self.setPics = { }
        self.setFrames = { }
        self.setNum = { }


    def refreshList(self, setKey = 0):
        if setKey == 0 or setKey == None:
            return None

        if self.currentDisplay != 0:
            oldSize = CollectionMap.Collection_Set_Sizes.get(self.currentDisplay)
            for loopItr in xrange(oldSize):
                curNum = self.currentDisplay + loopItr + 1
                if curNum in self.setPics:
                    self.setPics[curNum].hide()

                self.setFrames[curNum].hide()


        self.currentDisplay = setKey
        self.setLabel['text'] = PLocalizer.Collections[setKey]
        inv = localAvatar.getInventory()
        if not inv:
            return None

        setCount = 0
        heightOffset = 0
        setSize = CollectionMap.Collection_Set_Sizes.get(setKey)
        gui = loader.loadModel('models/gui/toplevel_gui')
        for loopItr in xrange(setSize):
            setItem = setKey + 1 + loopItr
            rowSpot = loopItr % 4
            colSpot = loopItr / 4
            localHeight = PiratesGuiGlobals.InventoryPanelHeight - 0.200
            howMany = inv.getStackQuantity(setItem)

            if howMany > 0:
                if setItem in self.setPics:
                    self.setPics[setItem].show()
                    self.setFrames[setItem].show()
                else:
                    frameImg = gui.find('**/treasure_w_b_slot_full')
                    self.setFrames[setItem] = DirectFrame(parent = self, relief = None, image = frameImg, image_scale = 0.4, image_pos = (0, 0, 0), pos = (0.28000 + 0.179 * rowSpot, 0, localHeight - 0.359 - 0.179 * colSpot))
                    pic_name = CollectionMap.Assets[setItem]
                    tex = self.card.find('**/%s*' % pic_name)
                    use_scale = 0.390
                    self.setPics[setItem] = DirectButton(parent = self, relief = None, image = tex, image_scale = use_scale, image_pos = (0, 0, 0), pos = (0.28000 + 0.179 * rowSpot, 0, localHeight - 0.359 - 0.179 * colSpot), command = self.clickedTreasure, extraArgs = [
                        setItem], text = PLocalizer.Collections[setItem], text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ACenter, text_wordwrap = 6, text_scale = 0.0250, text_pos = (0, -0.085, 0))
                    self.setPics[setItem].setTransparency(1)
                if setItem in CollectionMap.Collection_Needed:
                    howManyINeed = CollectionMap.Collection_Needed[setItem]
                else:
                    howManyINeed = 1
                if setItem in CollectionMap.Collection_SingleNumeric:
                    if howMany > 0:
                        if howMany == 1:
                            weightTxt = 'Lb'
                        else:
                            weightTxt = 'Lbs'
                        if setItem in self.setHowMany:
                            self.setHowMany[setItem]['text'] = '%d %s' % (howMany, weightTxt)
                        else:
                            self.setHowMany[setItem] = DirectLabel(parent = self.setPics[setItem], relief = None, text = '%d %s' % (howMany, weightTxt), text_align = TextNode.ARight, text_scale = 0.0400, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0.08, 0, -0.050000), text_font = PiratesGlobals.getInterfaceOutlineFont())

                elif setItem in self.setHowMany:
                    if howManyINeed < 2:
                        self.setHowMany[setItem].hide()
                    else:
                        self.setHowMany[setItem]['text'] = '%d/%d' % (howMany, howManyINeed)
                        self.setHowMany[setItem].show()
                elif howMany > 1:
                    self.setHowMany[setItem] = DirectLabel(parent = self.setPics[setItem], relief = None, text = '%d/%d' % (howMany, howManyINeed), text_align = TextNode.ARight, text_scale = 0.0400, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0.08, 0, -0.050000), text_font = PiratesGlobals.getInterfaceOutlineFont())

            if setItem in self.setFrames:
                self.setFrames[setItem].show()
                continue
            frameImg = gui.find('**/treasure_w_b_slot_empty')
            self.setFrames[setItem] = DirectFrame(parent = self, relief = None, image = frameImg, image_scale = 0.4, image_pos = (0, 0, 0), pos = (0.28000 + 0.179 * rowSpot, 0, localHeight - 0.359 - 0.179 * colSpot))

        gui.remove_node()


    def destroy(self):
        self.clearList()
        DirectFrame.destroy(self)


    def clickedTreasure(self, value):
        if FishingGlobals.inFishingCollection(value):
            model = FishingGlobals.getModelFromCollection(value)
            inv = localAvatar.getInventory()
            fishWeight = inv.getStackQuantity(value)
            if fishWeight:
                localAvatar.d_requestShowOffFish(value)
