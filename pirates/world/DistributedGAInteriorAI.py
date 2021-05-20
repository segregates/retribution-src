from panda3d.core import NodePath
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.distributed.GridParent import GridParent
from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
import WorldGlobals

from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.piratesbase import PiratesGlobals

from DistributedInteriorDoorAI import DistributedInteriorDoorAI
import copy

class DistributedGAInteriorAI(DistributedGameAreaAI, DistributedCartesianGridAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAInteriorAI')

    def __init__(self, air, extDoor):
        DistributedGameAreaAI.__init__(self, air, '')

        cellWidth = WorldGlobals.GAME_AREA_INTERIOR_CELL_SIZE
        gridSize = WorldGlobals.GAME_AREA_INTERIOR_GRID_SIZE
        gridRadius = WorldGlobals.GAME_AREA_INTERIOR_GRID_RADIUS
        zoneId = WorldGlobals.GAME_AREA_INTERIOR_STARTING_ZONE

        DistributedCartesianGridAI.__init__(self, air, zoneId, gridSize, gridRadius, cellWidth)

        self.extDoor = extDoor
        self.intDoors = []

    def announceGenerate(self):
        DistributedGameAreaAI.announceGenerate(self)
        DistributedCartesianGridAI.announceGenerate(self)
    
    def setBuildingInterior(self, buildingInterior):
        self.buildingInterior = buildingInterior

    def getBuildingInterior(self):
        return self.buildingInterior

    def setCaveInterior(self, caveInterior):
        self.caveInterior = caveInterior

    def getCaveInterior(self):
        return self.caveInterior

    def createObject(self, objType, parent, objKey, object):
        genObj = None

        if objType == 'Island Game Area':
            if not self.getUniqueId():
                self.b_setUniqueId(objKey)
                self.b_setVisAllowed(object.get('VisAllowed', True))
                
                if object['Visual']['Model']:
                    self.b_setModelPath(object['Visual']['Model'])
                
                npEmpty = NodePath('npEmpty')

                for objKey2, obj2 in object['Objects'].iteritems():
                    if obj2['Type'] == 'Cave_Pieces':
                        np = NodePath('cavePieces')
                        np.reparentTo(npEmpty)
                        np.setPos(obj2['Pos'])
                        np.setHpr(obj2['Hpr'])

                        for objKey3, obj3 in obj2['Objects'].iteritems():
                            np2 = NodePath('prop')
                            np2.reparentTo(np)
                            np2.setPos(obj3['Pos'])
                            np2.setHpr(obj3['Hpr'])

                            obj4 = copy.copy(obj3)
                            obj4['Pos'] = np2.getPos(npEmpty)
                            obj4['Hpr'] = np2.getHpr(npEmpty)

                            self.createObject(obj3['Type'], self, objKey3, obj4)
                            np2.removeNode()
                        
                        np.removeNode()
                    else:
                        self.createObject(obj2['Type'], self, objKey2, obj2)

                npEmpty.removeNode()
        elif objType == 'Building Interior':
            if not self.getUniqueId():
                self.b_setUniqueId(objKey)
                self.b_setModelPath(object['Visual']['Model'])

        elif objType == 'Door Locator Node':
            genObj = self.createIntDoor(objKey, object)

        else:
            genObj = DistributedGameAreaAI.createObject(self, objType, parent, objKey, object)

        return genObj

    def createIntDoor(self, objKey, object):
        if not self.buildingInterior:
            return

        intDoor = DistributedInteriorDoorAI.makeFromObjectKey(self.air, objKey,
                                         object, self.extDoor.getBuildingUid())
        intDoor.setOtherDoorId(self.extDoor.doId)
        self.generateChild(intDoor)
        self.intDoors.append(intDoor)
        return intDoor
    
    def getZoneFromXYZ(self, *args):
        return 2709

    def generateChild(self, obj, zoneId = None, cellParent = False):
        if not hasattr(obj, 'getPos') and zoneId is None:
            self.notify.warning("Failed to spawn '%s'. Object does not have a getPos()" % type(obj).__name__)
            return

        if zoneId is None:
            zoneId = self.getZoneFromXYZ(obj.getPos())

        if self.buildingInterior:
            obj.interior = self

        obj.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId)

        if hasattr(obj, 'posControlledByCell'):
            cellParent = obj.posControlledByCell()

        if hasattr(obj, 'posControlledByIsland'): #LEGACY.
            self.notify.warning("posControlledByIsland is deprecated. Please switch '%s' to posControlledByCell as soon as possible." % type(obj).__name__)
            cellParent = obj.posControlledByIsland()

        if cellParent and not self.buildingInterior and not self.caveInterior:
            cell = GridParent.getCellOrigin(self, zoneId)
            pos = obj.getPos()

            obj.reparentTo(cell)
            obj.setPos(self, pos)

            obj.sendUpdate('setPos', obj.getPos())
            obj.sendUpdate('setHpr', obj.getHpr())
