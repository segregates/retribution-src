from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedDiceGameAI import DistributedDiceGameAI

class DistributedLiarsDiceAI(DistributedDiceGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLiarsDice')

    def __init__(self, air):
        DistributedDiceGameAI.__init__(self, air)

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedDiceGameAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setTableType(2)
        #obj.generatePlayers()
        return obj