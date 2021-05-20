from panda3d.core import NodePath
from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from pirates.world.DistributedIslandAI import DistributedIslandAI
from pirates.battle.DistributedEnemySpawnerAI import DistributedEnemySpawnerAI
from OceanGridBase import OceanGridBase
import WorldGlobals

class DistributedOceanGridAI(DistributedCartesianGridAI, OceanGridBase):
    notify = directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, mainWorld):
        air = mainWorld.air

        startingZone = WorldGlobals.OCEAN_GRID_STARTING_ZONE
        cellWidth = WorldGlobals.OCEAN_CELL_SIZE
        gridSize = WorldGlobals.OCEAN_CELL_SIZE
        gridRadius = WorldGlobals.OCEAN_GRID_RADIUS

        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)
        OceanGridBase.__init__(self)

        self.mainWorld = mainWorld
        self.spawner = DistributedEnemySpawnerAI(self.mainWorld)

        self.islandData = {}
        self.islands = set()

    def registerIslandData(self, data):
        self.islandData = data

    def createIsland(self, uniqueId):
        object = self.islandData.pop(uniqueId)
        name = object.get('Name', 'default')
        modelPath = object['Visual']['Model']
        undockable = object.get('Undockable', False)
        x, y, z = object.get('Pos', (0, 0, 0))
        h, p, r = object.get('Hpr', (0, 0, 0))

        il = DistributedIslandAI(self.mainWorld, modelPath)
        il.setUniqueId(uniqueId)
        il.setName(name)
        il.setUndockable(undockable)
        il.setIslandTransform(x, y, z, h)

        for obj in object['Objects'].values():
            if obj['Type'] == 'LOD Sphere':
                il.setZoneSphereSize(*obj['Radi'])

        self.mainWorld.generateChild(il)

        self.notify.info('Created island %s %s' % (il.getName(), uniqueId))
        self.islands.add(il)
        return il

    def addShipSpawn(self, objKey, object):
        self.spawner.addShipSpawnNode(objKey, object)

    def addShipMovementNode(self, objKey, object):
        nodeName = 'objNode-ShipMovementNode-%s' % objKey
        genObj = NodePath(nodeName)

        if 'Pos' in object:
            genObj.setPos(object['Pos'])

        if 'Hpr' in object:
            genObj.setHpr(object['Hpr'])

        return genObj