from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class PVPGamePirateerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGamePirateerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)