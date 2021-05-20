from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleNPCAI import *

class DistributedCreatureAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreatureAI')
    avatarType = AvatarTypes.Creature

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
