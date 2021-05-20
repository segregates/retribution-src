from panda3d.core import NodePath
from direct.directnotify.DirectNotifyGlobal import directNotify

from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI

from pirates.world.DistributedOceanGridAI import DistributedOceanGridAI
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.piratesbase import PiratesGlobals

class DistributedMainWorldAI(DistributedInstanceBaseAI, DistributedCartesianGridAI):
    notify = directNotify.newCategory('DistributedMainWorldAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)

        startingZone = 777
        gridSize = gridRadius = cellWidth = 10000
        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)

    def announceGenerate(self):
        DistributedInstanceBaseAI.announceGenerate(self)

        self.oceanGrid = DistributedOceanGridAI(self)
        self.generateChild(self.oceanGrid)

        self.setName('MainWorld-%d' % self.doId)

    def getInstanceNodePath(self):
        return self

    def generateChild(self, obj, zoneId=777):
        obj.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId)
