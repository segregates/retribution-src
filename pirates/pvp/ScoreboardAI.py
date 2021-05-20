from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class ScoreboardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ScoreboardAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)