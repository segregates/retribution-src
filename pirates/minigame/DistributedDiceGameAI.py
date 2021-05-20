from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI

class DistributedDiceGameAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGameAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)