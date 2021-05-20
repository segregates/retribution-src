from panda3d.core import Light
from pirates.effects.RayOfLight import RayOfLight
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode

class QuestIndicatorNodeShip(QuestIndicatorGridNode):

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'ShipIndicator', [
            300,
            1500], questStep)
        self._selfRefreshTask = None
        self._refreshTargetLoc = None

    def delete(self):
        QuestIndicatorGridNode.delete(self)
        if self.nearEffect:
            self.nearEffect.cleanUpEffect()

        self.nearEffect = None
        self.stopTargetRefresh()

    def enterOff(self):
        QuestIndicatorGridNode.enterOff(self)
        self.stopNearEffect()

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
