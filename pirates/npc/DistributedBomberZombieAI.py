from direct.directnotify import DirectNotifyGlobal
from DistributedNPCSkeletonAI import *

class DistributedBomberZombieAI(DistributedNPCSkeletonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBomberZombieAI')
