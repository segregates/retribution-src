from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import *

class DistributedBuriedTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.startingDepth = 0
        self.curDepth = 0
        self.visZone = ''

    def handleInteract(self, avId, interactType, instant):
        # TO DO: If av has a quest to dig, allow them
        return REJECT

    def setStartingDepth(self, depth):
        self.startingDepth = depth

    def getStartingDepth(self):
        return self.startingDepth

    def setCurrentDepth(self, depth):
        self.curDepth = depth

    def d_setCurrentDepth(self, depth):
        self.sendUpdate('setCurrentDepth', [depth])

    def b_setCurrentDepth(self, depth):
        self.setCurrentDepth(depth)
        self.d_setCurrentDepth(depth)

    def getCurrentDepth(self):
        return self.curDepth

    def setVisZone(self, visZone):
        self.visZone = visZone

    def getVisZone(self):
        return self.visZone

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)

        depth = int(data['startingDepth'])
        obj.setCurrentDepth(depth)
        obj.setStartingDepth(depth)
        obj.setVisZone(data.get('VisZone', ''))

        return obj
