from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class SiegeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiegeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)