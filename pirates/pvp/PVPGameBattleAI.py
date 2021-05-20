from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class PVPGameBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)