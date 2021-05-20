from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleNPCAI import *
from pirates.npc.BossAI import BossAI

class DistributedDavyJonesAI(DistributedBattleNPCAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDavyJonesAI')

    def getNameText(self):
        return 'Davy Jones'
    
    def isBattleable(self):
        return 1

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        obj = DistributedBattleNPCAI.makeFromObjectKey(cls, spawner, uid, avType, data)
        obj._setupBossValues(data['DNA'], avType)
        return obj
