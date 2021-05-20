from direct.directnotify import DirectNotifyGlobal
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI

class DistributedPVPInstanceAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPInstanceAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

    def setAvatarReady(self):
        pass

    def requestLeave(self):
        pass


