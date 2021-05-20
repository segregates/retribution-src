from panda3d.core import Light
from pirates.effects.RayOfLight import RayOfLight
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode
from direct.showbase.PythonUtil import report

class QuestIndicatorNodeQuestProp(QuestIndicatorGridNode):

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'QuestPropIndicator', [
            30,
            150], questStep)

    def delete(self):
        QuestIndicatorGridNode.delete(self)
        if self.nearEffect:
            self.nearEffect.destroy()

        self.nearEffect = None

    def enterOff(self):
        QuestIndicatorGridNode.enterOff(self)

    def enterFar(self):
        QuestIndicatorGridNode.enterFar(self)
        self.requestTargetRefresh()

    def exitFar(self):
        QuestIndicatorGridNode.exitFar(self)
        self.stopTargetRefresh()

    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.startNearEffect()

    def exitNear(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.exitNear(self)

    def enterAt(self):
        QuestIndicatorGridNode.enterAt(self)

    def exitAt(self):
        QuestIndicatorGridNode.exitAt(self)

    def stepObjArrived(self, stepObj):
        QuestIndicatorGridNode.stepObjArrived(self, stepObj)
        if self.getCurrentOrNextState() in ('Near',):
            self.startNearEffect()

    def stepObjLeft(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.stepObjLeft(self)

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
            self.nearEffect.startLoop()

        if self.stepObj:
            self.nearEffect.reparentTo(self.stepObj)

    def stopNearEffect(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()
            self.nearEffect = None
