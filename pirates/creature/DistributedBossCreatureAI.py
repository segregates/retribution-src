from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from pirates.npc.BossAI import BossAI

class DistributedBossCreatureAI(DistributedCreatureAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCreature')

    #def __init__(self, spawner):
    #    DistributedCreatureAI.__init__(self, spawner.air)
    #    BossAI.__init__(self, spawner.air)

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        avType.setBoss(True)
        obj = DistributedCreatureAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['objKey'], avType) #TODO
        return obj