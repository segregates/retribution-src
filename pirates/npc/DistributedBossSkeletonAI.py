from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.BossAI import BossAI

class DistributedBossSkeletonAI(DistributedNPCSkeletonAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossSkeletonAI')

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        obj = DistributedNPCSkeletonAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['DNA'], avType)
        obj.setDNAId(data['DNA'])
        return obj