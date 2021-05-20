from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal


class DistributedMatchMaker(DistributedObjectGlobal):
    notify = directNotify.newCategory('DistributedMatchMaker')

    def requestActivity(self, gameType, gameCategory = -1, options = [], shipIds = []):
        self.sendUpdate('requestActivity', [gameType, gameCategory, options, shipIds])

    def requestJoin(self, matchId):
        self.sendUpdate('requestJoin', [matchId])

    def skipJoin(self, matchId, clearSearch = False):
        self.sendUpdate('skipJoin', [matchId, clearSearch])

    def cancelRequest(self, matchId):
        self.sendUpdate('cancelRequest', [matchId])
