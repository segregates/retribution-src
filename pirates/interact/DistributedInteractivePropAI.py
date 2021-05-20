from panda3d.core import getModelPath
from direct.distributed import DistributedObjectAI
from pirates.distributed.DistributedInteractiveAI import *
from pirates.distributed.DistributedTargetableObjectAI import *

class DistributedInteractivePropAI(DistributedInteractiveAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractivePropAI')

    def ___init___(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedTargetableObjectAI.__init__(self, air)

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def getModelPath(self):
        return self.modelPath

    def setInteractAble(self, able):
        self.able = able

    def getInteractAble(self):
        return self.able

    def setInteractType(self, type):
        self.interactType = type

    def getInteractType(self):
        return self.interactType

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setModelPath(data['Visual']['Model'])
        obj.setInteractAble(data.get('interactAble', 'npc'))
        obj.setInteractType(data.get('interactType', 'hit'))
        return obj
