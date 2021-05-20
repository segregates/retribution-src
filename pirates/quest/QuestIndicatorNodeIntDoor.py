from panda3d.core import Light
from pirates.effects.RayOfLight import RayOfLight
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeIntDoor(QuestIndicatorNode):

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'IntDoorIndicator', [
            5], questStep)
        self.nearEffect = None

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None

        QuestIndicatorNode.delete(self)
        if self.nearEffect:
            self.nearEffect.cleanUpEffect()

        self.nearEffect = None

    def placeInWorld(self):

        def stepObjHere(stepObj):
            self.pendingStepObj = None
            self.reparentTo(stepObj)
            self.setPos(0, 0, 0)
            self.setHpr(0, 0, 0)
            self.setScale(render, 1)

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None

        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([
            self.questStep.getStepDoId()], eachCallback = stepObjHere)

    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')

        if level == 1:
            self.request('Near')

    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Near')

        if level == 1:
            self.request('Off')

    def enterOff(self):
        QuestIndicatorNode.enterOff(self)
        self.stopNearEffect()

    def enterNear(self):
        self.startNearEffect()

    def exitNear(self):
        self.stopNearEffect()

    def enterAt(self):
        pass

    def exitAt(self):
        pass

    def showEffect(self):
        QuestIndicatorNode.showEffect(self)
        self.startNearEffect()

    def hideEffect(self):
        QuestIndicatorNode.hideEffect(self)
        self.stopNearEffect()

    def startNearEffect(self):
        if self.muted:
            return None

        if not self.nearEffect:
            self.nearEffect = RayOfLight()
            self.nearEffect.setBottomRayEnabled(self.wantBottomEffect)
            self.nearEffect.reparentTo(self)
            self.nearEffect.startLoop()

    def stopNearEffect(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()
            self.nearEffect = None
