from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedDoorAI import DistributedDoorAI

class DistributedInteriorDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteriorDoorAI')

    def __init__(self, air):
        DistributedDoorAI.__init__(self, air)
        self.interior = None
        self.buildingDoorId = 0

    # setInteriorId(uint32, uint32, uint32) required broadcast ram
    def getInteriorId(self):
        return [self.interior.doId, self.interior.parentId, self.interior.zoneId]

    # setExteriorId(uint32, uint32, uint32) required broadcast ram
    def getExteriorId(self):
        door = self.interior.extDoor
        island = door.getParentObj()
        return [island.doId, island.parentId, island.zoneId]

    # setBuildingDoorId(uint32) is not used, don't bother
    def getBuildingDoorId(self):
        return 0

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data, parentUid):
        parentData = {'key': parentUid, 'Pos': 0}
        obj = DistributedDoorAI.makeFromObjectKey(cls, air, objKey, data, parentData)
        return obj
