from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.creature.DistributedCreatureAI import *

class DistributedRavenAI(DistributedCreatureAI):
    notify = directNotify.newCategory('DistributedRavenAI')
    avatarType = AvatarTypes.Raven

    def isBattleable(self):
        return 0