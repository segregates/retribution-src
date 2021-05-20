from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedBandMemberAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBandMemberAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.avatarId = 0
        self.name = "Pirate"
        self.hp = 0
        self.maxHp = 0
        self.bandId = 0
        self.bandManager = 0
        self.bandTempManager = 0
        self.isPvp = 0
        self.isParlor = 0
        self.disconnected = 0
        self.shipInfo = (0, "", 0 , [])
        self.shipHasSpace = False

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def d_setAvatarId(self, avatarId):
        self.sendUpdate("setAvatarId", [avatarId])

    def b_setAvatarId(self, avatarId):
        self.setAvatarId(avatarId)
        self.d_setAvatarId(avatarId)

    def getAvatarId(self):
        return self.avatarId

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate("setName", [avatarId])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate("setHp", [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate("setMaxHp", [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setBandId(self, bandId):
        self.bandId = bandId

    def d_setBandId(self, bandId):
        self.sendUpdate("setBandId", [bandId])

    def b_setBandId(self, bandId):
        self.setBandId(bandId)
        self.d_setBandId(bandId)

    def getBandId(self):
        return self.bandId

    def setIsManager(self, bandManager):
        self.bandManager = bandManager

    def d_setIsManager(self, bandManager):
        self.sendUpdate("setIsManager", [bandManager])

    def b_setIsManager(self, bandManager):
        self.setIsManager(bandManager)
        self.d_setIsManager(bandManager)

    def getIsManager(self):
        return self.bandManager

    def setIsTempManager(self, bandTempManager):
        self.bandTempManager = bandTempManager

    def d_setIsTempManager(self, bandTempManager):
        self.sendUpdate("setIsTempManager", [bandTempManager])

    def b_setIsTempManager(self, bandTempManager):
        self.setIsTempManager(bandTempManager)
        self.d_setIsTempManager(bandTempManager)

    def getIsTempManager(self):
        return self.bandTempManager

    def setPvp(self, pvp):
        self.isPvp = pvp

    def d_setPvp(self, pvp):
        self.sendUpdate("setPvp", [pvp])

    def b_setPvp(self, pvp):
        self.setPvp(pvp)
        self.d_setPvp(pvp)

    def getPvp(self):
        return self.isPvp

    def setParlor(self, parlor):
        self.isParlor = parlor

    def d_setParlor(self, parlor):
        self.sendUpdate("setParlor", [parlor])

    def b_setParlor(self, parlor):
        self.setParlor(parlor)
        self.d_setParlor(parlor)

    def getParlor(self):
        return self.isParlor

    def setDisconnect(self, disconnected):
        self.disconnected = disconnected

    def d_setDisconnect(self, disconnected):
        self.sendUpdate("setDisconnect", [disconnected])

    def b_setDisconnect(self, disconnected):
        self.setDisconnect(disconnected)
        self.d_setDisconnect(disconnected)

    def getDisconnect(self):
        return self.disconnected

    def setShipInfo(self, todo0, todo1, todo2, todo3):
        self.shipInfo = (todo0, todo1, todo2, todo3)

    def d_setShipInfo(self, todo0, todo1, todo2, todo3):
        self.sendUpdate("setShipInfo", [todo0, todo1, todo2, todo3])

    def b_setShipInfo(self, todo0, todo1, todo2, todo3):
        self.setShipInfo(todo0, todo1, todo2, todo3)
        self.d_setShipInfo(todo0, todo1, todo2, todo3)

    def getShipInfo(self):
        return self.shipInfo

    def setShipHasSpace(self, space):
        self.shipHasSpace = space

    def d_setShipHasSpace(self, space):
        self.sendUpdate("setShipHasSpace", [space])

    def b_setShipHasSpace(self, space):
        self.setShipHasSpace(space)
        self.d_setShipHasSpace(space)

    def getShipHasSpace(self):
        return self.shipHasSpace

    #setMessage(uint32, string) broadcast;
    #setShipDeployMessage(uint32, uint32, string, string, uint8) broadcast;
    #removeShipDeployMessage(uint32) broadcast;
    #setCrewHUDUpdate(uint8, HUDIcon) broadcast ram;
    #setChat(string, uint8, uint32) broadcast ownsend;
    #setWLChat(string, uint8, uint32) broadcast ownsend;
    #setSpeedChat(uint32, uint16) broadcast ownsend;
    #requestDisableBandMember(uint32) airecv clsend;
    #responseDisableBandMember(uint32, uint8);
    #setSCQuestChat(uint32, uint16, uint8, uint8) broadcast ownsend;
    #teleportQuery(uint32, uint32, uint32) clsend ownrecv;
    #teleportResponse(uint32, int8, uint32, uint32, uint32) clsend ownrecv;

