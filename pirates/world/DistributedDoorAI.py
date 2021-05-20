from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from pirates.distributed.DistributedInteractiveAI import *
from pirates.piratesbase import PiratesGlobals

class DistributedDoorAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoorAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.doorIndex = 0

        self.buildingUid = ''
        self.locked = 0
        self.otherDoorId = 0
        self.questNeeded = ''

    # setDoorIndex(uint8) required broadcast ram
    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex

    def d_setDoorIndex(self, doorIndex):
        self.sendUpdate('setDoorIndex', [doorIndex])

    def b_setDoorIndex(self, doorIndex):
        self.setDoorIndex(doorIndex)
        self.d_setDoorIndex(doorIndex)

    def getDoorIndex(self):
        return self.doorIndex

    # setBuildingUid(string) required broadcast ram
    def setBuildingUid(self, buildingUid):
        self.buildingUid = buildingUid

    def d_setBuildingUid(self, buildingUid):
        self.sendUpdate('setBuildingUid', [buildingUid])

    def b_setBuildingUid(self, buildingUid):
        self.setBuildingUid(buildingUid)
        self.d_setBuildingUid(buildingUid)

    def getBuildingUid(self):
        return self.buildingUid

    # setMovie(uint8, uint32, int16) broadcast

    # setLocked(uint8) required broadcast ram
    def setLocked(self, locked):
        self.locked = locked

    def d_setLocked(self, locked):
        self.sendUpdate('setLocked', [locked])

    def b_setLocked(self, locked):
        self.setLocked(locked)
        self.d_setLocked(locked)

    def getLocked(self):
        return self.locked

    # requestArea() airecv clsend

    # setArea(Locations, uint32, bool)

    # setOtherDoorId(uint32) required broadcast ram
    def setOtherDoorId(self, otherDoorId):
        self.otherDoorId = otherDoorId

    def d_setOtherDoorId(self, otherDoorId):
        self.sendUpdate('setOtherDoorId', [otherDoorId])

    def b_setOtherDoorId(self, otherDoorId):
        self.setOtherDoorId(otherDoorId)
        self.d_setOtherDoorId(otherDoorId)

    def getOtherDoorId(self):
        return self.otherDoorId

    # setQuestNeeded(string) required broadcast ram
    def setQuestNeeded(self, questNeeded):
        self.questNeeded = questNeeded

    def d_setQuestNeeded(self, questNeeded):
        self.sendUpdate('setQuestNeeded', [questNeeded])

    def b_setQuestNeeded(self, questNeeded):
        self.setQuestNeeded(questNeeded)
        self.d_setQuestNeeded(questNeeded)

    def getQuestNeeded(self):
        return self.questNeeded

    def handleInteract(self, avId, interactType, instant):
        self.d_open(avId)
        return ACCEPT

    def d_open(self, avId):
        self.sendUpdate('setMovie', [PiratesGlobals.DOOR_OPEN, avId,
                                     globalClockDelta.getRealNetworkTime()])

    @staticmethod
    def makeFromObjectKey(cls, air, objKey, data, parentData):
        obj = cls(air)
        obj.setUniqueId(objKey)

        obj.setPos(parentData.get('Pos', 0))
        obj.setHpr(parentData.get('Hpr', 0))
        obj.setPos(obj, data.get('Pos', 0))

        obj.setBuildingUid(parentData['key'])

        return obj
