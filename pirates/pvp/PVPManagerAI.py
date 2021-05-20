from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class PVPManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)