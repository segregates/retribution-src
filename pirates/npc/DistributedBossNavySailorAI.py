from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
from pirates.npc.BossAI import BossAI

class DistributedBossNavySailorAI(DistributedNPCNavySailorAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCNavySailorAI')

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        obj = DistributedNPCNavySailorAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['objKey'], avType)
        if 'DNA' in data:
            obj.setDNAId(data['DNA'])
        return obj