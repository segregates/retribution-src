from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class TargetManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TargetManagerAI')
