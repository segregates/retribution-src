from panda3d.core import NodePath, TextNode
# File: F (Python 2.4)

import random
import math
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GuiPanel import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.LureGlow import LureGlow
import FishingGlobals
_glowColors = {
    InventoryType.FishingRodStall: (1.0, 1.0, 0.598, 0.696),
    InventoryType.FishingRodPull: (0.696, 0.696, 1.0, 0.696),
    InventoryType.FishingRodHeal: (0.598, 1.0, 0.598, 0.696),
    InventoryType.FishingRodTug: (1.0, 0.598, 0.598, 0.696),
    InventoryType.FishingRodSink: (1.0, 0.598, 1.0, 0.696),
    InventoryType.FishingRodOceanEye: (1.0, 1.0, 1.0, 0.696) }

class FishLure(NodePath):

    def __init__(self, gameObject, type):
        NodePath.__init__(self, 'FishingLure_%s' % type)
        self.gameObject = gameObject
        self.type = type
        self.initLureModel()
        if FishingGlobals.wantDebugCollisionVisuals:
            self.initCollision()

        self.initLureHelpText()
        self.setLightOff()


    def initLureModel(self):
        self.lureModel = NodePath('lure')
        self.currentLureType = 'regular'
        self.lureAttractRadius = FishingGlobals.lureTypeToAttractRadius[self.currentLureType]
        self.lureModel = loader.loadModel(FishingGlobals.lureTypeToModel[self.currentLureType])
        self.lureModel.setScale(2.0)
        self.lureModel.reparentTo(self)
        self.lureModel.setDepthWrite(False)
        self.lureModel.setDepthTest(True)
        self.lureModel.setBin('ground', 25)
        self.mainGui = loader.loadModel('models/gui/gui_main')


    def initCollision(self):
        self.lureCollisionVisual = loader.loadModel('models/ammunition/cannonball')
        self.lureCollisionVisual.setTransparency(1)
        self.lureCollisionVisual.setColor(0.0, 0.0, 1.0, 0.299)
        self.lureCollisionVisual.setScale(self.lureAttractRadius)
        self.lureCollisionVisual.reparentTo(self)
        self.lureCollisionVisual.hide()


    def initLureHelpText(self):
        self.helpTextNode = TextNode('fishBitingIcon')
        self.helpTextNodePath = NodePath(self.helpTextNode)
        self.helpTextNodePath.setPos(0.0, 0.0, 0.696)
        self.helpTextNode.setText(' ')
        self.helpTextNode.setAlign(TextNode.ACenter)
        self.helpTextNode.setFont(PiratesGlobals.getPirateFont())
        self.helpTextNode.setTextColor(1.0, 1.0, 1.0, 1.0)
        self.helpTextNodePath.reparentTo(self)
        self.helpTextNodePath.setBillboardPointEye()
        self.helpTextNodePath.setBin('fishingGame', 10)
        self.helpTextNodePath.hide()


    def enableLureGlow(self, glowType):
        self.lureGlow = LureGlow.getEffect()
        if self.lureGlow:
            if self.gameObject.fishManager.activeFish is not None:
                self.lureGlow.reparentTo(self.gameObject.fishManager.activeFish.mouthJoint)
            else:
                self.lureGlow.reparentTo(self)
            self.lureGlow.effectColor = _glowColors[glowType]
            self.lureGlow.setShaderOff()
            self.lureGlow.setBin('fishingGame', 5)
            self.lureGlow.play()



    def showHelpText(self, textToShow):
        if not self.gameObject.distributedFishingSpot:
            return
        taskMgr.remove(self.gameObject.distributedFishingSpot.uniqueName('ClearLureText'))
        if textToShow is None:
            textToShow = ' '
        elif self.gameObject.fishManager.activeFish is not None:
            self.helpTextNodePath.setScale(FishingGlobals.fishSizeToHelpTextScale[self.gameObject.fishManager.activeFish.myData['size']])
        else:
            self.helpTextNodePath.setScale(1.0)
        self.helpTextNode.setText(textToShow)
        self.helpTextNodePath.show()
        taskMgr.doMethodLater(FishingGlobals.lureHelpTextDuration, self.showHelpText, name = self.gameObject.distributedFishingSpot.uniqueName('ClearLureText'), extraArgs = [
            None])


    def setLureType(self, type):
        self.currentLureType = type
        if type == None:
            self.lureModel.hide()
            self.gameObject.gui.setTackleBoxPulse(True)
        elif type == 'regular':
            self.gameObject.gui.setTackleBoxPulse(False)
            self.currentLureType = type
            self.lureModel.remove_node()
            self.lureAttractRadius = FishingGlobals.lureTypeToAttractRadius[type]
            self.lureModel = loader.loadModel(FishingGlobals.lureTypeToModel[type])
            self.lureModel.setScale(2.0)
            self.lureModel.reparentTo(self)
            self.lureModel.setDepthWrite(False)
            self.lureModel.setDepthTest(True)
            self.lureModel.setBin('ground', 25)
        elif type == 'legendary':
            self.gameObject.gui.setTackleBoxPulse(False)
            self.currentLureType = type
            self.lureModel.remove_node()
            self.lureAttractRadius = FishingGlobals.lureTypeToAttractRadius[type]
            self.lureModel = loader.loadModel(FishingGlobals.lureTypeToModel[type])
            self.lureModel.setScale(2.0)
            self.lureModel.reparentTo(self)
            self.lureModel.setDepthWrite(False)
            self.lureModel.setDepthTest(True)
            self.lureModel.setBin('ground', 25)



    def showCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.lureCollisionVisual.show()



    def hideCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.lureCollisionVisual.hide()



    def requestPitch(self, fish):
        offset = fish.getPos() - self.getPos()
        if fish.getX() < self.getX():
            return math.degrees(math.atan2(offset.getZ(), -offset.getX()))
        else:
            return math.degrees(math.atan2(-offset.getZ(), offset.getX()))


    def resetLureModel(self):
        self.lureModel.reparentTo(self)
        self.lureModel.show()
        self.lureModel.setPosHpr(0, 0, 0, 0, 0, 0.0)
        if self.currentLureType == None:
            self.lureModel.hide()
            self.gameObject.gui.setTackleBoxPulse(True)
        else:
            self.gameObject.gui.setTackleBoxPulse(False)


    def destroy(self):
        self.lureModel.remove_node()
        self.remove_node()
