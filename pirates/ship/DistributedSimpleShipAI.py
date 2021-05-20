from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.battle.Teamable import Teamable
from pirates.ship.DistributedFlagshipAI import DistributedFlagshipAI
from pirates.ship import ShipGlobals

class DistributedSimpleShipAI(DistributedMovingObjectAI, Teamable, DistributedFlagshipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSimpleShipAI')

    def __init__(self, air):
        DistributedMovingObjectAI.__init__(self, air)
        Teamable.__init__(self)
        self.uniqueId = ""
        self.level = 0
        self.pos = (0,0,0)
        self.hpr = (0,0,0)
        self.name = "Mysterious Ship"
        self.gameState = ("", 0, 0)
        self.classId = ShipGlobals.INTERCEPTORL1
        self.styleOverride = 0
        self.logoOverride = 0
        self.armorStates = (100, 100, 100)
        self.mastStates = (0, 0, 0, 0, 0)
        self.healthState = 0
        self.crew = []
        self.owner = 0
        self.boardable = 0
        self.exitable = 0
        self.flagship = 0
        self.inBoardingPosition = 0
        self.wishName = ""
        self.wishNameState = "OPEN"
        self.cargo = []
        self.badge = (0, 0)
        self.sailState = False

    def setUniqueId(self, id):
        self.uniqueId = id

    def getUniqueId(self):
        return self.uniqueId

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def setHpr(self, hpr):
        self.hpr = hpr

    def getHpr(self):
        return self.hpr

    def setGameState(self, statename, avId, timeStamp):
        self.gameState = (statename, avId, timeStamp)

    def getGameState(self):
        return self.gameState

    def setShipClass(self, classId):
        self.classId = classId

    def getShipClass(self):
        return self.classId

    def setStyleOverride(self, style):
        self.styleOverride = style

    def getStyleOverride(self):
        return self.styleOverride

    def setLogoOverride(self, logo):
        self.logoOverride = logo

    def getLogoOverride(self):
        return self.logoOverride

    def setArmorStates(self, todo0, todo1, todo2):
        self.armorStates = (todo0, todo1, todo2)

    def getArmorStates(self):
        return self.armorStates

    def setMastStates(self, todo0, todo1, todo2, todo3, todo4):
        self.mastStates = (todo0, todo1, todo2, todo3, todo4)

    def getMastStates(self):
        return self.mastStates

    def setHealthState(self, health):
        self.healthState = health

    def getHealthState(self):
        return self.healthState

    def setCrew(self, crew):
        self.crew = crew

    def getCrew(self):
        return self.crew

    #setBandId(uint32, uint32) broadcast ram;

    def setOwnerId(self, ownerId):
        self.owner = ownerId

    def getOwnerId(self):
        return self.owner

    #setCannons(uint32 [], uint32) broadcast ram;
     #setSkillEffects(BuffList) broadcast ram;

    def setIsBoardable(self, boardable):
        self.boardable = boardable

    def getIsBoardable(self):
        return self.boardable

    def setIsExitable(self, exitable):
        self.exitable = exitable

    def getIsExitable(self):
        return self.exitable

    def setIsFlagship(self, flagship):
        self.flagship = flagship

    def getIsFlagship(self):
        return self.flagship

    #setBoardableShipId(uint32) broadcast ram;

    def setIsInBoardingPosition(self, inBoardingPosition):
        self.inBoardingPosition = inBoardingPosition

    def getIsInBoardingPosition(self):
        return self.inBoardingPosition

    #requestBoard(uint32) airecv clsend;
    #setMovie(uint8, uint32, uint32, bool, int16) broadcast;
    #shipBoarded() clsend airecv;
    #leave(uint32) airecv clsend;
    #setDeploy(uint8, int16) broadcast ram;
    #requestBoardFlagship(uint32) clsend airecv;
    #boardShip(uint8) broadcast;
    #swingToShip(uint8) broadcast;

    def setWishName(self, wishName):
        self.wishName = wishName

    def getWishName(self):
        return self.wishName

    def setWishNameState(self, state):
        self.wishNameState = state

    def getWishNameState(self):
        return self.wishNameState

    def setCargo(self, cargo):
        self.cargo = cargo

    def getCargo(self):
        return self.cargo

    #notifyReceivedLoot(uint8[]) broadcast;
    #setCaptainId(DoId) broadcast ram;

    def setBadge(self, todo0, todo1):
        self.badge = (todo0, todo1)

    def getBadge(self):
        return self.badge

    #setRespectDeployBarriers(bool, uint32) broadcast ram;
    #setGuildId(uint32) broadcast ram;
    #setClientController(uint32) broadcast ram;
    #sendCrewToIsland(uint32, PosH);
    #dropAnchor(uint32) airecv clsend;
    #requestSkillEvent(uint32, uint32) airecv clsend;
    #recordSkillEvent(uint32, uint32) broadcast;
    #sendShipDefeated() broadcast;
    #setLandedGrapples(LandedGrappleList) broadcast ram;
    #setRespawnLocation(uint32, uint32);
    #setRepairCount(uint8) broadcast ram;

    def setSailsDown(self, sailState):
        self.sailState = sailState

    def getSailsDown(self):
        return self.sailState

    #requestClientAggro() airecv clsend;
    #requestShipRam(DoId, Pos, uint32) clsend airecv;
    #useShipRam(Pos) broadcast;
    #relayTeleportInfo() airecv;
    #sendTeleportInfo(uint32, uint32) ownrecv;
    #teleportAvatarAboard(DoId) airecv;

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, data):
        if cls is None:
            cls = DistributedSimpleShipAI

        obj = cls(spawner.air)

        x, y, z = data.get('Pos', (0, 0, 0))
        h, p, r = data.get('Hpr', (0, 0, 0))
        pos = (x, y, z)
        hpr = (h, p, r)

        obj.setPos(pos)
        obj.setHpr(hpr)
        obj.setUniqueId(uid)

        obj.setIsFlagship(data.get('Flagship', False))
        obj.setLevel(int(data.get('Level', '1')))
        obj.setShipClass(ShipGlobals.SHIP_CLASS_LIST.index(data.get('Spawnables', 'INTERCEPTORL1')))
        obj.setTeam(ShipGlobals.getShipTeam(obj.getShipClass()))

        return obj
