class FriendHandle:

    def __init__(self, doId, name, hp, maxHp, online):
        self.doId = doId
        self.name = name
        self.hp = hp
        self.maxHp = maxHp
        self.online = online
    
    def isAdmin(self):
        return False

    def getDoId(self):
        return self.doId

    def getName(self):
        return self.name
    
    def isUnderstandable(self):
        return True
    
    def getHp(self):
        return self.hp
    
    def getMaxHp(self):
        return self.maxHp
    
    def isOnline(self):
        return self.online

    def uniqueName(self, idString):
        return idString + '-' + str(self.getDoId())
    
    def getBandId(self):
        # TODO: Bands
        return 0

    def d_teleportQuery(self, requesterId):
        base.cr.piratesFriendsManager.d_teleportQuery(self.doId)

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        base.cr.piratesFriendsManager.d_teleportResponse(self.doId, available,
            shardId, hoodId, zoneId
        )

    def d_teleportGiveup(self, requesterId):
        base.cr.piratesFriendsManager.d_teleportGiveup(self.doId)
