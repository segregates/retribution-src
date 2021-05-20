from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedGhostAI import DistributedGhostAI
from pirates.npc.BossAI import BossAI

class DistributedBossGhostAI(DistributedGhostAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossGhostAI')

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        obj = DistributedGhostAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['objKey'], avType)
        obj.setDNAId(data['objKey'])
        return obj