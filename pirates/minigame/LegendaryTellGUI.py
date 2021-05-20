from panda3d.core import NodePath, TextNode
# File: L (Python 2.4)

import math
from pirates.piratesgui.GuiButton import GuiButton
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
import FishingGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import PiratesGuiGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import CollectionMap
from pirates.piratesgui import GuiPanel

class LegendaryTellGUI(GuiPanel.GuiPanel):

    def __init__(self, w, h, locationId = LocationIds.PORT_ROYAL_ISLAND):
        GuiPanel.GuiPanel.__init__(self, '', w, h, True)
        self.card = loader.loadModel('models/gui/pir_m_gui_fsh_legendaryScreen')
        self.storyImageCard = loader.loadModel('models/minigames/pir_m_gam_fsh_legendaryGui')
        self.UICompoments = { }
        self.setPos(-1.14, 0.0, -0.598)
        self['geom'] = self.card.find('**/background')
        self['geom_pos'] = (0.576, 0.0, 0.63)
        self['geom_scale'] = (0.946, 0.0, 0.848)
        self.coinImage = OnscreenImage(parent = self, image = self.card.find('**/coin'), scale = 0.9, hpr = (0, 0, 0), pos = (0.848, 0, 0.848))
        self.titleTextNode = TextNode('legendPanelTitle')
        self.titleTextNode.setText(PLocalizer.LegendSelectionGui['panelTitle'])
        self.titleTextNode.setFont(PiratesGlobals.getPirateFont())
        self.titleTextNode.setTextColor(0.87, 0.815, 0.540000, 0.9)
        self.titleTextNodePath = NodePath(self.titleTextNode)
        self.titleTextNodePath.setPos(0.65, 0.0, 1.2)
        self.titleTextNodePath.setScale(0.070)
        self.titleTextNodePath.reparentTo(self)
        self.introTextNode = TextNode('legendaryIntroTextNode')
        self.introTextNode.setText(PLocalizer.LegendSelectionGui['legendIntro'])
        self.introTextNode.setWordwrap(14.0)
        self.introTextNode.setTextColor(0.9, 0.800000, 0.46, 0.9)
        self.introTextNodePath = NodePath(self.introTextNode)
        self.introTextNodePath.setPos(0.598, 0.0, 0.5)
        self.introTextNodePath.setScale(0.042000)
        self.introTextNodePath.reparentTo(self)
        self.buttonRootNode = NodePath('button_RootNode')
        self.buttonRootNode.reparentTo(self)
        self.buttonRootNode.setPos(-0.08, 0.0, 1.14)
        self.iconCard = loader.loadModel('models/gui/treasure_gui')
        self.legendSelectionButtons = { }
        btnGeom = (self.card.find('**/fishButton/idle'), self.card.find('**/fishButton/idle'), self.card.find('**/fishButton/over'))
        for i in xrange(len(FishingGlobals.legendaryFishData)):
            fishName = FishingGlobals.legendaryFishData[i]['name']
            fishId = FishingGlobals.legendaryFishData[i]['id']
            assetsKey = CollectionMap.Assets[fishId]
            pos_x = 0.299
            pos_z = 0.0 - i * 0.25
            button = GuiButton(parent = self.buttonRootNode, text = (fishName, fishName, fishName, fishName), text0_fg = (0.429, 0.288, 0.19, 1.0), text1_fg = (0.429, 0.288, 0.19, 1.0), text2_fg = (0.429, 0.288, 0.19, 1.0), text3_fg = (0.429, 0.288, 0.19, 1.0), text_scale = 0.035000, text_pos = (0.0379, -0.00500), pos = (pos_x, 0, pos_z), hpr = (0, 0, 0), scale = 1.5, image = btnGeom, image_pos = (0, 0, 0), image_scale = 0.696, sortOrder = 2, command = self.buttonClickHandle, extraArgs = [
                fishId,
                assetsKey,
                locationId])
            button.icon = OnscreenImage(parent = button, image = self.iconCard.find('**/%s*' % assetsKey), scale = 0.348, hpr = (0, 0, 0), pos = (-0.123, 0, 0.00500))

        self.legendPanel = GuiPanel.GuiPanel('', 2.60, 1.89, True)
        self.legendPanel.setPos(-1.3, 0.0, -0.946)
        self.legendPanel.background = OnscreenImage(parent = self.legendPanel, scale = (2.39, 0, 1.8), image = self.storyImageCard.find('**/pir_t_gui_fsh_posterBackground'), hpr = (0, 0, 0), pos = (1.3, 0, 0.946))
        self.legendPanel.storyImage = OnscreenImage(parent = self.legendPanel, scale = 1, image = self.card.find('**/coin'), hpr = (0, 0, 0), pos = (1.8, 0, 1))
        self.storyTextNode = TextNode('storyTextNode')
        self.storyTextNode.setText('')
        self.storyTextNode.setWordwrap(19.0)
        self.storyTextNode.setTextColor(0.230, 0.089, 0.0299, 1.0)
        self.storyTextNodePath = NodePath(self.storyTextNode)
        self.storyTextNodePath.setPos(0.33, 0.0, 1.66)
        self.storyTextNodePath.setScale(0.050000)
        self.storyTextNodePath.reparentTo(self.legendPanel)
        self.callBack = None
        self.legendPanel.hide()


    def destroy(self):
        self.legendPanel.destroy()
        GuiPanel.GuiPanel.destroy(self)


    def buttonClickHandle(self, fishId, imgKey, locationId):
        result = imgKey.split('_')
        temp = str(result[1]).capitalize()
        imgName = 'pir_t_gui_fsh_poster%s' % temp
        self.legendPanel.storyImage.setImage(self.storyImageCard.find('**/%s*' % imgName))
        self.storyTextNode.setText(PLocalizer.LegendSelectionGui['shortStory'][fishId][locationId])
        self.legendPanel.show()


    def setCallBack(self, callback):
        self.callBack = callback


    def closePanel(self):
        GuiPanel.GuiPanel.closePanel(self)
        if self.callBack is not None:
            self.callBack()
