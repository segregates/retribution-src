from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.distributed.GridParent import GridParent
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.battle.Teamable import Teamable
from pirates.piratesbase import PiratesGlobals
from pirates.ai import HolidayGlobals
from pirates.minigame.DistributedPotionCraftingTableAI import DistributedPotionCraftingTableAI
from pirates.minigame.DistributedRepairBenchAI import DistributedRepairBenchAI
from pirates.minigame.DistributedFishingSpotAI import DistributedFishingSpotAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.world.LocationConstants import *
from pirates.world import WorldGlobals
import random


class DistributedIslandAI(DistributedCartesianGridAI, DistributedGameAreaAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandAI')

    def __init__(self, mainWorld, islandModel):
        air = mainWorld.air

        cellWidth = WorldGlobals.GAME_AREA_CELL_SIZE
        gridSize = WorldGlobals.LARGE_ISLAND_GRID_SIZE
        gridRadius = WorldGlobals.ISLAND_GRID_RADIUS
        zoneId = WorldGlobals.ISLAND_GRID_STARTING_ZONE

        DistributedCartesianGridAI.__init__(self, air, zoneId, gridSize, gridRadius, cellWidth)
        DistributedGameAreaAI.__init__(self, air, islandModel)
        Teamable.__init__(self)

        self.mainWorld = mainWorld
        self.zoneSphereSize = [0, 0, 0]
        self.zoneSphereCenter = [0, 0]

        self.islandModel = islandModel

        self.undockable = False
        self.portCollisionSpheres = []
        self.feastFireEnabled = False
        self.fireworkShowEnabled = [False, 0]
        self.nextEvent = 0

        self.__fspots = 0
        self.__dinghyIdx = 0

        self.jail = None

    def announceGenerate(self):
        DistributedCartesianGridAI.announceGenerate(self)
        DistributedGameAreaAI.announceGenerate(self)
        self.accept('holidayListChanged', self.__processHolidaysChange)
        if config.GetBool('want-island-events', True):
            self.__runIslandEvents()
            self.runEvents = taskMgr.doMethodLater(15, self.__runIslandEvents, 'runEvents')

    def delete(self):
        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)
        if hasattr(self, 'runEvents'):
            taskMgr.remove(self.runEvents)
        self.ignore('holidayListChanged')

    def __processHolidaysChange(self):
        if not self.air.newsManager:
            return

        islandId = self.getUniqueId()
        if config.GetBool('want-auto-feast', True):
            if islandId == LocationIds.TORTUGA_ISLAND:
                feastHoliday = False
                feastHolidays = [HolidayGlobals.FOUNDERSFEAST, HolidayGlobals.MARDIGRAS, HolidayGlobals.THANKSGIVING]
                for holiday in feastHolidays:
                    if self.air.newsManager.isHolidayRunning(holiday):
                        feastHoliday = True
                if feastHoliday:
                    self.notify.info("Auto starting %s feast..." % self.getName())
                self.b_setFeastFireEnabled(feastHoliday)

        if config.GetBool('want-fireworks', True):
            fireworkIslands = [LocationIds.PORT_ROYAL_ISLAND, LocationIds.TORTUGA_ISLAND, LocationIds.DEL_FUEGO_ISLAND]
            fireworkHolidays = [HolidayGlobals.FOURTHOFJULY, HolidayGlobals.NEWYEARS, HolidayGlobals.MARDIGRAS]
            if islandId in fireworkIslands:
                fireworkTime = False
                showType = 0
                for holiday in fireworkHolidays:
                    if self.air.newsManager.isHolidayRunning(holiday):
                        fireworkTime = True
                        showType = holiday
                if fireworkTime:
                    self.notify.info("Starting Firework shows for '%s' using ShowType %s" % (self.getName(), showType))
                    self.b_setFireworkShowEnabled(True, showType)
                else:
                    self.b_setFireworkShowEnabled(False, 0)

        if config.GetBool('want-invasions', True) and len(self.npcs) > 0:
            invasionLocations = [LocationIds.PORT_ROYAL_ISLAND, LocationIds.TORTUGA_ISLAND, LocationIds.DEL_FUEGO_ISLAND]
            invasionHolidays = {
                LocationIds.PORT_ROYAL_ISLAND: HolidayGlobals.INVASIONPORTROYAL,
                LocationIds.TORTUGA_ISLAND: HolidayGlobals.INVASIONTORTUGA,
                LocationIds.DEL_FUEGO_ISLAND: HolidayGlobals.INVASIONDELFUEGO
            }
            validLocation = islandId in invasionLocations
            if validLocation:
                invasionStatus = invasionHolidays[islandId] in self.air.newsManager.getRawHolidayIdList()
                self.notify.debug("Setting invasion status of npcs on '%s' to '%s'" % (self.getName(), invasionStatus))
                for npcId in self.npcs:
                    npc = self.npcs[npcId]
                    if hasattr(npc, 'b_setInInvasion'):
                        npc.b_setInInvasion(invasionStatus)


    def __runIslandEvents(self, task=None):
        self.nextEvent -= 15
        if self.nextEvent <= 0:
            islandId = self.getUniqueId()
            if islandId == LocationIds.DEL_FUEGO_ISLAND:
                self.makeLavaErupt()
                self.nextEvent = random.randint(5, 10) * 60

        return Task.again


    def setIslandTransform(self, x, y, z, h):
        self.setXYZH(x, y, z, h)

    def d_setIslandTransform(self, x, y, z, h):
        self.sendUpdate('setIslandTransform', [x, y, z, h])

    def b_setIslandTransform(self, x, y, z, h):
        self.setIslandTransform(x, y, z, h)
        self.d_setIslandTransform(x, y, z, h)

    def getIslandTransform(self):
        x, y, z = self.getPos()
        h = self.getH()
        return [x, y, z, h]

    def setZoneSphereSize(self, r0, r1, r2):
        self.zoneSphereSize = [r0, r1, r2]

    def d_setZoneSphereSize(self, r0, r1, r2):
        self.sendUpdate('setZoneSphereSize', [r0, r1, r2])

    def b_setZoneSphereSize(self, r0, r1, r2):
        self.setZoneSphereSize(r0, r1, r2)
        self.d_setZoneSphereSize(r0, r1, r2)

    def getZoneSphereSize(self):
        return self.zoneSphereSize

    def setZoneSphereCenter(self, x, y):
        self.zoneSphereCenter = [x, y]

    def d_setZoneSphereCenter(self, x, y):
        self.sendUpdate('setZoneSphereCenter', [x, y])

    def b_setZoneSphereCenter(self, x, y):
        self.setZoneSphereCenter(x, y)
        self.d_setZoneSphereCenter(x, y)

    def getZoneSphereCenter(self):
        return self.zoneSphereCenter

    def setIslandModel(self, path):
        self.islandModel = path

    def d_setIslandModel(self, path):
        self.sendUpdate('setModelPath', [path])

    def b_setIslandModel(self, path):
        self.setIslandModel(path)
        self.d_setIslandModel(path)

    def getIslandModel(self):
        return self.islandModel

    def setUndockable(self, undockable):
        self.undockable = undockable

    def d_setUndockable(self, undockable):
        self.sendUpdate('setUndockable', [undockable])

    def b_setUndockable(self, undockable):
        self.setUndockable(undockable)
        self.d_setUndockable(undockable)

    def getUndockable(self):
        return self.undockable

    def setPortCollisionSpheres(self, spheres):
        self.portCollisionSpheres = spheres

    def d_setPortCollisionSpheres(self, spheres):
        self.sendUpdate('setPortCollisionSpheres', [spheres])

    def b_setPortCollisionSpheres(self, spheres):
        self.setPortCollisionSpheres(spheres)
        self.d_setPortCollisionSpheres(spheres)

    def getPortCollisionSpheres(self):
        return self.portCollisionSpheres

    def getPortCollisionSpheres(self):
        return self.portCollisionSpheres

    def makeLavaErupt(self):
        self.sendUpdate('makeLavaErupt')

    def setFeastFireEnabled(self, enabled):
        self.feastFireEnabled = enabled

    def d_setFeastFireEnabled(self, enabled):
        self.sendUpdate('setFeastFireEnabled', [enabled])

    def b_setFeastFireEnabled(self, enabled):
        self.setFeastFireEnabled(enabled)
        self.d_setFeastFireEnabled(enabled)

    def getFeastFireEnabled(self):
        return self.feastFireEnabled

    def setFireworkShowEnabled(self, enabled, showType):
        self.fireworkShowEnabled = [enabled, showType]

    def d_setFireworkShowEnabled(self, enabled, showType):
        self.sendUpdate('setFireworkShowEnabled', [enabled, showType])

    def b_setFireworkShowEnabled(self, enabled, showType):
        self.setFireworkShowEnabled(enabled, showType)
        self.d_setFireworkShowEnabled(enabled, showType)

    def getFireworkShowEnabled(self):
        return self.fireworkShowEnabled

    def generateChild(self, obj, zoneId=None, cellParent=False):

        if not hasattr(obj, 'getPos') and zoneId is None:
            self.notify.warning("Failed to spawn '%s'. Object does not have a getPos()" % type(obj).__name__)
            return

        if zoneId is None:
            zoneId = self.getZoneFromXYZ(obj.getPos())

        obj.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId)

        if hasattr(obj, 'posControlledByCell'):
            cellParent = obj.posControlledByCell()

        if cellParent: 
            cell = GridParent.getCellOrigin(self, zoneId)
            pos = obj.getPos()

            obj.reparentTo(cell)
            obj.setPos(self, pos)

            obj.sendUpdate('setPos', obj.getPos())
            obj.sendUpdate('setHpr', obj.getHpr())

    def createObject(self, objType, parent, objKey, object):
        genObj = None

        if objType == 'PotionTable' and config.GetBool('want-potion-game', 0):
            genObj = DistributedPotionCraftingTableAI.makeFromObjectKey(self.air, objKey, object)
            self.generateChild(genObj)

        elif objType == 'Dinghy':
            genObj = DistributedDinghyAI.makeFromObjectKey(self.air, objKey, object)
            genObj.setLocationId(self.__dinghyIdx)
            self.__dinghyIdx += 1
            self.generateChild(genObj)

        elif objType == 'FishingSpot' and config.GetBool('want-fishing-game', 0):
            self.notify.debug('Generated a fishing spot')
            genObj = DistributedFishingSpotAI.makeFromObjectKey(self.air, objKey, object)
            genObj.setIndex(self.__fspots)
            self.__fspots += 1
            self.generateChild(genObj)

        elif objType == 'RepairBench' and config.GetBool('want-repair-game', 0):
            genObj = DistributedRepairBenchAI.makeFromObjectKey(self.air, objKey, object)
            self.generateChild(genObj)
            
        else:
            genObj = DistributedGameAreaAI.createObject(self, objType, parent, objKey, object)

        return genObj

