from direct.directnotify import DirectNotifyGlobal
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI

class DistributedInstanceWorldAI(DistributedInstanceBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInstanceWorldAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)
