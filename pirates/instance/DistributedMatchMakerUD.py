from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD


class DistributedMatchMakerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('DistributedMatchMakerUD')

    def requestActivity(self, gameType, gameCategory, options, shipIds):
        pass

    def requestJoin(self, matchId):
        pass

    def skipJoin(self, matchId, clearSearch):
        pass

    def cancelRequest(self, matchId):
        pass

    def instanceCreated(self, todo0, todo1, todo2):
        pass

    def instanceRemoved(self, todo0, todo1, todo2):
        pass

    def printStatus(self, todo0):
        pass

    def newDistrictOnline(self, todo0):
        pass

    def initiateTeleportResp(self, todo0, todo1):
        pass
