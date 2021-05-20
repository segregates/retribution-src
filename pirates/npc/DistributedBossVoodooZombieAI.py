from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedVoodooZombieAI import *

class DistributedBossVoodooZombieAI(DistributedVoodooZombieAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossVoodooZombieAI')

    def isBattleable(self):
        return 1