from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class LootableAI(DistributedObjectAI):
    notify = directNotify.newCategory('LootableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
     
    def startLooting(self, avId, plunderInfo, timer=0):
        self.sendUpdateToAvatarId(avId, 'startLooting', [plunderInfo, timer])

    def requestItem(self, item):
        pass

    def requestItems(self):
        pass
