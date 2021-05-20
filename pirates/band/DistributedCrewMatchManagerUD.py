from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedCrewMatchManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchManagerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)

    def requestCrewAdd(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def requestCrewDelete(self):
        pass

    def requestCrewChangeOptions(self, todo0, todo1, todo2):
        pass

    def requestInitialAvatarAdd(self, todo0):
        pass

    def requestInitialAvatarAddResponse(self, todo0, todo1):
        pass

    def requestPutAvatarOnLookoutList(self, todo0):
        pass

    def requestDeleteAvatarFromLookoutList(self):
        pass

    def requestDeleteAvatarFromLookoutListUD(self, todo0):
        pass

    def requestAcceptInvite(self, todo0):
        pass

    def requestCrewOfOneCreation(self):
        pass

    def requestCrewOfOneDelete(self):
        pass

    def requestNewMember(self, todo0, todo1, todo2, todo3):
        pass

    def requestTeleportQuery(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def requestTeleportResponse(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def teleportQuery(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def teleportResponse(self, todo0, todo1, todo2, todo3, todo4):
        pass
