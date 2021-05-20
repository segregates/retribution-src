from panda3d.core import Light, Point3
from pirates.piratesgui.RadarGui import *
from pirates.effects.RayOfLight import RayOfLight
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode
from direct.showbase.PythonUtil import report

class QuestIndicatorNodeExtDoor(QuestIndicatorGridNode):

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'ExtDoorIndicator', [
            10,
            150], questStep)

    def delete(self):
        QuestIndicatorGridNode.delete(self)
        if self.nearEffect:
            self.nearEffect.cleanUpEffect()

        self.nearEffect = None

    def enterOff(self):
        QuestIndicatorGridNode.enterOff(self)
        self.stopNearEffect()

    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.startNearEffect()

    def exitNear(self):
        QuestIndicatorGridNode.exitNear(self)
        self.stopNearEffect()

    def stepObjArrived(self, stepObj):
        QuestIndicatorGridNode.stepObjArrived(self, stepObj)
        if self.getCurrentOrNextState() in ('Near',):
            self.startNearEffect()

    def stepObjLeft(self):
        QuestIndicatorGridNode.stepObjLeft(self)
        self.stopNearEffect()

    def showEffect(self):
        QuestIndicatorGridNode.showEffect(self)
        self.startNearEffect()

    def hideEffect(self):
        QuestIndicatorGridNode.hideEffect(self)
        self.stopNearEffect()

    def startNearEffect(self):
        if self.muted:
            return None

        if not self.nearEffect:
            self.nearEffect = RayOfLight()
            self.nearEffect.setBottomRayEnabled(self.wantBottomEffect)
            self.nearEffect.setPos(Point3(0, 5, 0))
            self.nearEffect.startLoop()

        if self.stepObj:
            self.nearEffect.reparentTo(self.stepObj)

    def stopNearEffect(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()
            self.nearEffect = None
