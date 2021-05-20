from panda3d.core import NodePath
from direct.directnotify.DirectNotifyGlobal import directNotify

from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI

from pirates.world.DistributedOceanGridAI import DistributedOceanGridAI
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI

class DistributedPiratesTutorialWorldAI(DistributedInstanceBaseAI, DistributedCartesianGridAI):
    notify = directNotify.newCategory('DistributedPiratesTutorialWorldAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)

        startingZone = 777
        gridSize = gridRadius = cellWidth = 10000
        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)

    def announceGenerate(self):
        DistributedInstanceBaseAI.announceGenerate(self)

        self.oceanGrid = DistributedOceanGridAI(self)
        self.generateChild(self.oceanGrid)

        self.setName("TutorialWorld-%d" % self.doId)

    def getInstanceNodePath(self):
        return self

    def generateChild(self, obj, zoneId=777):
       obj.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId) 
