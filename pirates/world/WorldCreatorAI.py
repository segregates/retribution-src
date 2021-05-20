from direct.directnotify.DirectNotifyGlobal import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from DistributedBuildingDoorAI import DistributedBuildingDoorAI
from DistributedJailInteriorAI import DistributedJailInteriorAI
from DistributedGAInteriorAI import DistributedGAInteriorAI
from DistributedGameAreaAI import DistributedGameAreaAI
from DistributedGATunnelAI import DistributedGATunnelAI
from WorldCreatorBase import WorldCreatorBase
from pirates.world.LocationConstants import LocationIds
import WorldGlobals

class InteriorFlags:
    FORT = 1
    JAIL = 2
    # Next id is 4 (powers of 2)
    # Thought I'd say it since TTR had a similar flag thing
    # and Joey added 3, messing a lot of stuff

class WorldCreatorAI(WorldCreatorBase):
    notify = directNotify.newCategory('WorldCreatorAI')
    _missing = set() #Debug
    _unimplemented = set() #Debug

    def __init__(self, air):
        WorldCreatorBase.__init__(self, air)
        self.air = self.repository
        self.fileDicts = {}

        self.__loadingInterior = False
        self.__loadingIslandArea = False
        self.__currentWorld = None
        self.postponedTunnels = []
    
    def createTunnels(self):
        for postponedTunnel in self.postponedTunnels:
            self.doPostponedTunnel(postponedTunnel)
        
        self.postponedTunnels = []

    def createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj, fileName=fileName)
        if not objType:
            return

        if self.__currentWorld is None:
            return

        if not hasattr(self.__currentWorld, "oceanGrid"):
            self.notify.warning("Failed to generate object. %s has no oceanGrid" % str(self.__currentWorld))
            return

        newObj = None
        genObj = None
        objectCat = ''

        if dynamic:
            objectCat = self.findObjectCategory(objType)

        if self.__loadingInterior or self.__loadingIslandArea:
            actualParentObj = parent.getPythonTag('npTag-gameArea')

        if objType == 'Region':
            self.__currentWorld.oceanGrid.registerIslandData(object['Objects'])

        elif objType == 'Island':
            il = self.__currentWorld.oceanGrid.createIsland(objKey)
            actualParentObj = il

        elif objType == 'Ship Spawn Node' and config.GetBool('want-enemy-ships', False):
            self.__currentWorld.oceanGrid.addShipSpawn(objKey, object)

        elif objType == 'Ship Movement Node' and config.GetBool('want-enemy-ship-movement', False):
            genObj = self.__currentWorld.oceanGrid.addShipMovementNode(objKey, object)

        elif actualParentObj:
            genObj = actualParentObj.createObject(objType, parent, objKey, object)

        if genObj:
            if 'Objects' in object:
                newObj = genObj

        return (newObj, actualParentObj)

    def setCurrentWorld(self, world):
        self.__currentWorld = world

    def createBuilding(self, parent, objKey, object):
        interiorFile = object['File']

        if not (interiorFile and 'Objects' in object):
            return

        flags = 0
        if 'Fort' in interiorFile:
            flags |= InteriorFlags.FORT

        elif 'Jail' in interiorFile:
            flags |= InteriorFlags.JAIL

        extDoor = None

        object['key'] = objKey
        for key, obj in object['Objects'].items():
            if obj['Type'] == 'Door Locator Node':
                extDoor = DistributedBuildingDoorAI.makeFromObjectKey(self.air, key, obj, object)
                break

        else:
            self.notify.warning('%s defines interior, but has no exterior door!' % objKey)
            return

        parent.generateChild(extDoor)
        interior = self.loadInterior(interiorFile, parent.getParentObj(), extDoor, flags)
        extDoor.b_setInteriorId(interior.doId, interior.getUniqueId(), interior.parentId, interior.zoneId)

        if objKey in PLocalizer.LocationNames:
            interior.setName(PLocalizer.LocationNames[objKey])
        else:
            interior.setName(objKey)
        self.notify.debug("Created interior %s %s" % (interior.getName(), objKey))

        return extDoor

    def loadInterior(self, interiorFile, parent, extDoor, flags):
        if flags & InteriorFlags.JAIL:
            interior = DistributedJailInteriorAI(self.air, extDoor)

        else:
            interior = DistributedGAInteriorAI(self.air, extDoor)

        interior.setBuildingInterior(~flags & InteriorFlags.FORT)
        interior.setCaveInterior(False)
        zoneId = PiratesGlobals.InteriorDoorZone << 16 | extDoor.doId & 0xFFFF
        parent.generateChild(interior, zoneId)

        self.__loadingInterior = True
        self.__loadWorldFileAndAdditionalData(interiorFile, interior)
        self.__loadingInterior = False

        if not interior.intDoors:
            self.notify.warning('Interior %s defines no door, forcing generate...' % interiorFile)
            interior.createIntDoor('int%d.fakedoor' % interior.doId, {})

        return interior
    
    def createConnectorTunnel(self, objKey, object):
        self.postponedTunnels.append([objKey, object])
    
    def doPostponedTunnel(self, postponedTunnel):
        objKey, object = postponedTunnel
        parentUid = object['From']
        targetUid = object['To']
        parent = self.air.uid2do[parentUid]
        target = self.air.uid2do[targetUid]
        
        isExterior = False
        links = []
        
        for lObjKey, lObj in object['Objects'].iteritems():
            name = lObj['Name']
            
            if not name.startswith('portal_connector'):
                continue
            
            whichOne = int(name[-1])
            
            if whichOne == 2:
                t = target
                exteriorNode = object['Interior']
            else:
                t = parent
                exteriorNode = object['Exterior']
 
            links.append([name, t.doId, t.getUniqueId(), exteriorNode, t.parentId, t.zoneId])
            isExterior = True

        obj = DistributedGATunnelAI(parent.air)
        obj.setUniqueId(objKey)
        obj.setModelPath(object['Visual']['Model'])
        obj.setLinks(isExterior, links)
        obj.setVisAllowed(object.get('VisAllowed_1', True))
        parent.generateChild(obj, 2709)
        
        obj2 = DistributedGATunnelAI(target.air)
        obj2.setUniqueId(objKey)
        obj2.setModelPath(object['Visual'].get('Model2', obj.getModelPath()))
        obj2.setLinks(isExterior, links)
        obj2.setVisAllowed(object.get('VisAllowed', True))
        target.generateChild(obj2, 2709)

    def loadIslandArea(self, areaKey, areaFile, parent, cave=True):
        area = DistributedGAInteriorAI(self.air, None)
        
        self.air.uid2do[areaKey] = area

        if areaKey in PLocalizer.LocationNames:
            area.setName(PLocalizer.LocationNames[areaKey])
        else:
            area.setName(areaKey)

        area.setBuildingInterior(False)
        area.setCaveInterior(True)
        zoneId = PiratesGlobals.InteriorDoorZone << 16 | (sorted(self.air.doId2do.keys())[-1] + 1) & 0xFFFF
        parent.generateChild(area, zoneId)

        loaded = self.loadObjectsFromFile(areaFile, area, True)
        objects = loaded[0]['Objects']
        objKey = objects.keys()[0]
        obj = objects[objKey]
        
        area.createObject(obj['Type'], area, objKey, obj)

        self.notify.info('Created cave area %s %s' % (PLocalizer.LocationNames[areaKey], areaKey))
        return area

    def __loadWorldFileAndAdditionalData(self, filename, area):
        ret = self.loadObjectsFromFile(filename, area, True)[0]
        additionalData = []
        for obj in ret['Objects'].values():
            additionalData.extend(obj.get('AdditionalData', []))
            
        for additional in additionalData:
            self.__loadWorldFileAndAdditionalData(additional, area)

    @classmethod
    def registerMissing(cls, objType):
        cls._missing.add(objType)

    @classmethod
    def printMissingTypes(cls):
        if not cls._missing:
            return

        cls.notify.warning("Missing object types: ")
        for objType in cls._missing:
            print '   %r' % objType

        del cls._missing

    @classmethod
    def registerUnimplemented(cls, objType):
        cls._unimplemented.add(objType)

    @classmethod
    def printUnimplemented(cls):
        if not cls._unimplemented:
            return

        cls.notify.warning("Unable to spawn the following objects. They are not yet implemented: ")
        for objType in cls._unimplemented:
            print '   %r' % objType

        del cls._unimplemented