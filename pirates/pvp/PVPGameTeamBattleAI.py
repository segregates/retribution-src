from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class PVPGameTeamBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameTeamBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)