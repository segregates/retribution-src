from direct.directnotify import DirectNotifyGlobal

from otp.avatar.DistributedAvatarAI import DistributedAvatarAI

from pirates.distributed.DistributedInteractiveAI import *
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI

class DistributedReputationAvatarAI(DistributedAvatarAI, DistributedMovingObjectAI, DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedReputationAvatarAI')

    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
        DistributedMovingObjectAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)

    def generate(self):
        DistributedAvatarAI.generate(self)
        DistributedMovingObjectAI.generate(self)
        DistributedInteractiveAI.generate(self)

    def delete(self):
        DistributedAvatarAI.delete(self)
        DistributedMovingObjectAI.delete(self)
        DistributedInteractiveAI.delete(self)

    def announceGenerate(self):
        DistributedAvatarAI.announceGenerate(self)
        DistributedMovingObjectAI.announceGenerate(self)
        DistributedInteractiveAI.announceGenerate(self)

    def handleInteract(self, avId, interactType, instant):
        ''' Must be overwritten by subclasses '''
        return IGNORE
