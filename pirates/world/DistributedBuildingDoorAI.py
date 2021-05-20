from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedDoorAI import DistributedDoorAI
from pirates.piratesbase import PLocalizer

class DistributedBuildingDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuildingDoorAI')

    def __init__(self, air):
        DistributedDoorAI.__init__(self, air)
        self.interiorDoId = 0
        self.interiorUid = ''
        self.interiorWorldParentId = 0
        self.interiorWorldZoneId = 0

    # setInteriorId(uint32, string, uint32, uint32) required broadcast ram
    def setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.interiorDoId = interiorDoId
        self.interiorUid = interiorUid
        self.interiorWorldParentId = interiorWorldParentId
        self.interiorWorldZoneId = interiorWorldZoneId

    def d_setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.sendUpdate('setInteriorId', [interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId])

    def b_setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.setInteriorId(interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId)
        self.d_setInteriorId(interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId)

    def getInteriorId(self):
        return [self.interiorDoId, self.interiorUid, self.interiorWorldParentId, self.interiorWorldZoneId]

    def getBuildingName(self):
        return PLocalizer.LocationNames.get(self.interiorUid)

    def requestPrivateInteriorInstance(self):
        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(),
                                  'setPrivateInteriorInstance',
                                  [0, 0, 0, 1])

    def posControlledByCell(self):
        return False

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data, parentData):
        obj = DistributedDoorAI.makeFromObjectKey(cls, air, objKey, data, parentData)
        return obj
