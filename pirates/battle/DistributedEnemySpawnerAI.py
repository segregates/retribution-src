from direct.directnotify import DirectNotifyGlobal

from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
from pirates.npc.DistributedKillerGhostAI import DistributedKillerGhostAI
from pirates.npc.DistributedBountyHunterAI import DistributedBountyHunterAI
from pirates.npc.DistributedVoodooZombieAI import DistributedVoodooZombieAI
from pirates.npc.DistributedGhostAI import DistributedGhostAI
from pirates.npc.DistributedJollyRogerAI import DistributedJollyRogerAI
from pirates.npc.DistributedDavyJonesAI import DistributedDavyJonesAI
from pirates.npc.DistributedBossSkeletonAI import DistributedBossSkeletonAI
from pirates.npc.DistributedBossNavySailorAI import DistributedBossNavySailorAI
from pirates.npc.DistributedBossGhostAI import DistributedBossGhostAI
from pirates.npc.DistributedBossTownfolkAI import DistributedBossTownfolkAI
from pirates.npc import BossNPCList

from pirates.battle.DistributedBattleNPCAI import *
from pirates.creature.DistributedCreatureAI import *
from pirates.creature.DistributedAnimalAI import *
from pirates.creature.DistributedRavenAI import *
from pirates.creature.DistributedBossCreatureAI import DistributedBossCreatureAI

from pirates.ship import ShipGlobals
from pirates.ship.DistributedNPCSimpleShipAI import DistributedNPCSimpleShipAI
from pirates.ship.DistributedPlayerSeizeableShipAI import DistributedPlayerSeizeableShipAI

from pirates.piratesbase import PLocalizer
import random, os

NPC_CACHE = {}
ANIMAL_CACHE = {}
SHIP_CACHE = {}

class EnemySpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('EnemySpawnNode')

    def __init__(self, spawner, data):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'EnemySpawnNode-%d' % self.air.allocateChannel()
        self.npcs = {}

        self.data = data
        if 'Spawnables' not in data:
            return

        self.spawnable = self.data['Spawnables']
        if self.spawnable not in AvatarTypes.NPC_SPAWNABLES:
            return

        self.avType = AvatarTypes.NPC_SPAWNABLES[self.spawnable][0]()
        self.avClass = self.getClassFromAvatarType(self.avType)
        if self.avClass == None:
            self.notify.warning("Unknown avatar class: %s" % self.spawnable)
            DistributedEnemySpawnerAI.missingAvatarClass(self.avType)
            return

        self.desiredNumAvatars = self.data['Min Population'] or 1
        self.acceptOnce('startShardActivity', self.died)

    def getClassFromAvatarType(self, avatar):
        avatarClass = None

        if avatar in NPC_CACHE:
            return NPC_CACHE[avatar]

        if avatar.isA(AvatarTypes.Animal):
            avatarClass = DistributedAnimalAI
        elif avatar.isA(AvatarTypes.SeaMonster):
            pass
        elif avatar.isA(AvatarTypes.DavyJones):
            avatarClass = DistributedDavyJonesAI
        elif avatar.isA(AvatarTypes.JollyRoger):
            avatarClass = DistributedJollyRogerAI
        elif avatar.isA(AvatarTypes.Undead):
            avatarClass = DistributedNPCSkeletonAI
        elif avatar.isA(AvatarTypes.Navy):
            avatarClass = DistributedNPCNavySailorAI
        elif avatar.isA(AvatarTypes.GhostPirate):
            avatarClass = DistributedGhostAI
        elif avatar.isA(AvatarTypes.KillerGhost):
            avatarClass = DistributedKillerGhostAI
        elif avatar.isA(AvatarTypes.BountyHunter):
            avatarClass = DistributedBountyHunterAI
        elif avatar.isA(AvatarTypes.TradingCo):
            avatarClass = DistributedNPCNavySailorAI
        elif avatar.isA(AvatarTypes.VoodooZombie):
            avatarClass = DistributedVoodooZombieAI
        elif avatar.isA(AvatarTypes.LandCreature):
            avatarClass = DistributedCreatureAI
        elif avatar.isA(AvatarTypes.AirCreature):
            avatarClass = DistributedCreatureAI

        if avatar not in NPC_CACHE and avatarClass != None:
            NPC_CACHE[avatar] = avatarClass

        return avatarClass

    def getBossRandomFromAvatarType(self, avatar):
        bossRandomTypes = [
            #AvatarTypes.Clod,
            AvatarTypes.CorpseCutlass, 
            AvatarTypes.Sludge,
            AvatarTypes.Mire,
            AvatarTypes.Muck,
            AvatarTypes.Corpse,
            AvatarTypes.Carrion,
            AvatarTypes.CaptMudmoss,
            AvatarTypes.Mossman,
            AvatarTypes.AngryWasp,
            AvatarTypes.Wasp,
            AvatarTypes.VampireBat,
            AvatarTypes.Bat,
            AvatarTypes.BigGator,
            AvatarTypes.Alligator,
            AvatarTypes.DreadScorpion,
            AvatarTypes.Scorpion,
            AvatarTypes.FlyTrap,
            AvatarTypes.Stump,
            AvatarTypes.GiantCrab,
            AvatarTypes.RockCrab,
            AvatarTypes.Crab,
            AvatarTypes.Cadet,
            AvatarTypes.Guard,
            AvatarTypes.Sergeant,
            AvatarTypes.Veteran,
            AvatarTypes.Officer,
            AvatarTypes.Grunt,
            AvatarTypes.Thug,
            AvatarTypes.Hiredgun,
            AvatarTypes.Mercenary,
            AvatarTypes.Assassin]

        bossType = None
        for type in bossRandomTypes:
            if avatar.isA(type):
                bossType = type.getRandomBossType()
                break
        return bossType

    def died(self):
        taskMgr.doMethodLater(random.random() * 10, self.__checkCreatures, self.uniqueName('checkCreatures'))

    def __checkCreatures(self, task):
        deadNpcs = []
        for doId, npc in self.npcs.items():
            if npc.isDeleted():
                deadNpcs.append(doId)

        for doId in deadNpcs:
            avType = self.npcs[doId].getRawAvatarType()
            if avType.boss:
                self.notify.info("Random boss '%s' has died. " % avType.getName())
                DistributedEnemySpawnerAI.removeRandomBoss(avType)
            del avType
            del self.npcs[doId]

        # Upkeep population
        numNpcs = len(self.npcs)
        spawnedType = self.avType
        if numNpcs < self.desiredNumAvatars:

            bossType = self.getBossRandomFromAvatarType(self.avType)
            if bossType != None and config.GetBool('want-random-bosses', True):
                if bossType.boss:
                    bossDice = (random.randint(0, 100) <= config.GetInt("random-boss-spawn-rate", 5)) or config.GetBool('force-random-bosses', False)
                    bossSpawned = DistributedEnemySpawnerAI.isRandomBossSpawned(bossType)

                    if bossSpawned:
                        self.notify.debug("'%s' already is spawned. Returned to regular enemy" % bossType)

                    if bossDice and not bossSpawned:
                        spawnedType = bossType
                        DistributedEnemySpawnerAI.addRandomBoss(bossType)
                        if self.avType != bossType:
                            self.notify.info("Spawning random boss '%s' instead of '%s' at %s" % (bossType.getName(), self.avType.getName(), self.spawner.gameArea.getName()))

            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            npc = self.avClass.makeFromObjectKey(self.avClass, self, uid,
                                                 spawnedType, self.data)
            self.spawner.spawn(npc)
            self.npcs[npc.doId] = npc

        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class BossSpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossSpawnNode')

    def __init__(self, spawner, type, data, objKey):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'BossSpawnNode-%d' % self.air.allocateChannel()
        self.npcs = {}
        self.objKey = objKey

        self.data = data
        if 'Boss' not in data:
            self.notify.warning("Attempted add spawn node for invalid boss. No boss flag found")
            return

        if not data['Boss']:
            self.notify.warning("Attmempted to add spawn node for inactive boss. Boss flag is False")
            return

        self.bossData = []
        self.dnaId = None
        if 'DNA' in self.data:
            self.dnaId = self.data['DNA']
        else:
            self.dnaId = objKey

        if self.dnaId not in BossNPCList.BOSS_NPC_LIST:
            self.notify.warning("Attempted to add spawn node for invalid boss. No boss data found in BossNPCList")
            DistributedEnemySpawnerAI.badBossData(self.getBossName(), self.dnaId)
            return
        self.bossData = BossNPCList.BOSS_NPC_LIST[self.dnaId]

        self.avType = self.getAvTypeFromType(type)
        if self.avType is None and type != 'Townsperson':
            self.notify.warning("Attempted to add spawn node for invalid boss. Boss %s (%s) has no AvatarType" % (self.getBossName(), self.dnaId))
            DistributedEnemySpawnerAI.badBossData(self.getBossName(), self.dnaId)
            return

        self.avClass = self.getBossClassFromType(type)
        if self.avClass is None:
            self.notify.warning("Attempted add spawn node for invalid boss. No boss class found for type %s" % type)
            DistributedEnemySpawnerAI.missingBossClass(type)
            return

        self.desiredNumAvatars = 1
        self.acceptOnce('startShardActivity', self.died)

    def died(self):
        if 'Respawns' in self.data:
            if not self.data['Respawns']:
                self.notify.info("Ending Boss Spawn. Respawn is disabled")
                return

        taskMgr.doMethodLater(random.random() * 5, self.__checkBosses, self.uniqueName('checkBosses'))

    def getDefaultValue(self, key):
        return BossNPCList.BOSS_NPC_LIST[''][key]

    def getBossValue(self, key):
        if key in self.bossData:
            return self.bossData[key]
        else:
            return self.getDefaultValue(key)

    def getBossName(self):
        bossName = '%s %s' % (PLocalizer.Unknown, PLocalizer.Boss)

        if self.dnaId != None:
            bossName = PLocalizer.BossNPCNames[self.dnaId]
        else:
            pass

        return bossName

    def getAvTypeFromType(self, type):

        def findFromBossData(bossData=self.bossData):
            if 'AvatarType' in bossData:
                return bossData['AvatarType']
            return None

        dataType = findFromBossData()
        if dataType != None:
            return dataType

        if 'Species' in self.data:
            self.spawnable = self.data['Species']
            if self.spawnable not in AvatarTypes.NPC_SPAWNABLES:
                self.notify.warning("Unknown Boss species: %s" % self.spawnable)
                return

            avType = AvatarTypes.NPC_SPAWNABLES[self.spawnable][0]()
            return avType.getBossType()

        if type == 'Ghost':
            return AvatarTypes.RageGhost
        elif type == 'DavyJones':
            return AvatarTypes.DavyJones

        return None


    def getBossClassFromType(self, type):
        bossClass = None
        if 'Davy' in self.avType.getName():
            bossClass = DistributedDavyJonesAI
        elif type == 'Skeleton':
            bossClass = DistributedBossSkeletonAI
        elif type == 'Creature':
            bossClass = DistributedBossCreatureAI
        elif type == 'NavySailor':
            bossClass = DistributedBossNavySailorAI
        elif type == 'Ghost':
            bossClass = DistributedBossGhostAI
        elif type == 'Townsperson':
            bossClass = DistributedBossTownfolkAI
        else:
            self.notify.warning("Unknown boss creature class: %s" % type)

        return bossClass

    def __checkBosses(self, task):
        deadNpcs = []
        for doId, npc in self.npcs.items():
            if npc.isDeleted():
                deadNpcs.append(doId)

        for doId in deadNpcs:
            del self.npcs[doId]

        # Upkeep population
        numNpcs = len(self.npcs)
        if numNpcs < self.desiredNumAvatars:
            self.avType.setBoss(True)
            self.data['objKey'] = self.objKey
            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            npc = self.avClass.makeFromObjectKey(self.avClass, self, uid,
                                                 self.avType, self.data)
            npc.setUniqueId(self.objKey)
            self.notify.info("Spawning Boss '%s' on %s" % (npc.getNameText(), self.spawner.gameArea.getName()))
            self.spawner.spawn(npc, forceLevel = npc._getBossLevel())
            self.npcs[npc.doId] = npc
        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class AnimalSpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('AnimalSpawnNode')

    def __init__(self, spawner, data):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'AnimalSpawnNode-%d' % self.air.allocateChannel()
        self.npcs = {}

        self.data = data
        if 'Species' not in data:
            return

        self.spawnable = self.data['Species']
        if self.spawnable not in AvatarTypes.NPC_SPAWNABLES:
            self.notify.warning("Unknown animal species: %s" % self.spawnable)
            return

        self.avType = AvatarTypes.NPC_SPAWNABLES[self.spawnable][0]()

        self.avClass = self.getClassFromAnimalType(self.spawnable)
        if self.avClass == None:
            self.notify.warning("Unknown animal class: %s" % self.spawnable)
            DistributedEnemySpawnerAI.missingAnimalClass(self.spawnable)
            return            

        self.desiredNumAvatars = 1
        self.acceptOnce('startShardActivity', self.died)

    def getClassFromAnimalType(self, animal): #Done like this for potential future expansion
        avatarClass = None
        if animal in ANIMAL_CACHE:
            return ANIMAL_CACHE[animal]

        if animal == "Raven":
            avatarClass = DistributedRavenAI
        elif animal == "Seagull":
            avatarClass = None #TODO
        else:
            avatarClass = DistributedAnimalAI

        if avatarClass != None and animal not in ANIMAL_CACHE:
            ANIMAL_CACHE[animal] = avatarClass

        return avatarClass

    def died(self):
        taskMgr.doMethodLater(random.random() * 7, self.__checkCreatures, self.uniqueName('checkCreatures'))

    def __checkCreatures(self, task):
        deadNpcs = []
        for doId, npc in self.npcs.items():
            if npc.isDeleted():
                deadNpcs.append(doId)

        for doId in deadNpcs:
            del self.npcs[doId]

        # Upkeep population
        numNpcs = len(self.npcs)
        if numNpcs < self.desiredNumAvatars:
            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            npc = self.avClass.makeFromObjectKey(self.avClass, self, uid,
                                                 self.avType, self.data)
            self.spawner.spawn(npc)
            self.npcs[npc.doId] = npc

        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class ShipSpawnNode(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipSpawnNode')

    def __init__(self, spawner, data):
        self.spawner = spawner
        self.air = self.spawner.air
        self.uid = 'ShipSpawnNode-%d' % self.air.allocateChannel()
        self.ships = {}

        self.data = data
        if 'Spawnables' not in data:
            return

        self.spawnable = self.data['Spawnables']
        self.flagship = self.data['Flagship'] or False

        if self.spawnable not in ShipGlobals.SHIP_CLASS_LIST:
            self.notify.warning("Unknown ship class: %s" % self.spawnable)
            DistributedEnemySpawnerAI.missingShipClass(self.spawnable)
            return


        self.shipClass = DistributedNPCSimpleShipAI

        self.desiredNumShips = 1
        self.acceptOnce('startShardActivity', self.died)

    def died(self):
        taskMgr.doMethodLater(random.random() * 7, self.__checkShips, self.uniqueName('checkShips'))

    def __checkShips(self, task):
        deadShips = []
        for doId, ship in self.ships.items():
            if ship.isDeleted():
                deadShips.append(doId)

        for doId in deadShips:
            del self.ships[doId]

        # Upkeep population
        numShips = len(self.ships)
        if numShips < self.desiredNumShips:
            self.notify.info("Spawning Ship: %s" % self.spawnable)
            uid = self.uniqueName('spawned-%s' % os.urandom(4).encode('hex'))
            ship = self.shipClass.makeFromObjectKey(self.shipClass, self, uid, self.data)
            self.spawner.spawn(ship)
            self.ships[ship.doId] = ship

        if task:
            return task.done

    def uniqueName(self, name):
        return '%s-%s' % (self.uid, name)

class DistributedEnemySpawnerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawnerAI')
    _avatarMissing = set() # Debug
    _shipMissing = set() # Debug
    _animalMissing = set() #Debug
    _bossMissing = set() #Debug
    _badBosses = set() #Debug
    _randomBosses = []


    def __init__(self, gameArea):
        self.gameArea = gameArea
        self.air = self.gameArea.air

        self.spawnNodes = {}

    def addEnemySpawnNode(self, objType, objKey, data):
        regularSpawns = ['Spawn Node', 'Dormant NPC Spawn Node', 'Invasion NPC Spawn Node']
        if objType in regularSpawns:
            self.spawnNodes[objKey] = EnemySpawnNode(self, data)
        else:
            self.spawnNodes[objKey] = BossSpawnNode(self, objType, data, objKey)

    def addAnimalSpawnNode(self, objKey, data):
        self.spawnNodes[objKey] = AnimalSpawnNode(self, data)

    def addShipSpawnNode(self, objKey, data):
        self.spawnNodes[objKey] = ShipSpawnNode(self, data)

    def spawnNavy(self, objKey, data):
        npc = DistributedNPCPirateAI.makeFromObjectKey(None, self, objKey, data)
        self.spawn(npc, False)
        return npc

    def spawnMarine(self, objKey, data):
        npc = DistributedNPCNavySailorAI.makeFromObjectKey(None, self, objKey, data)
        self.spawn(npc, False)
        return npc

    def spawnNPC(self, objKey, data):
        npc = DistributedNPCTownfolkAI.makeFromObjectKey(None, self, objKey, data)
        self.spawn(npc, False)
        return npc

    def spawn(self, npc, setLevel=True, forceLevel=0):
        if not npc.getLevel():
            if setLevel:
                npc.setLevel(0) # Random

        if forceLevel != 0:
            npc.setLevel(forceLevel)

        npc.regularZone = self.gameArea.getZoneFromXYZ(npc.getPos())
        self.gameArea.generateChild(npc, 2709)

    @classmethod
    def missingAvatarClass(cls, avType):
        cls._avatarMissing.add(avType)

    @classmethod
    def printMissingAvatarTypes(cls):
        if not cls._avatarMissing:
            return

        cls.notify.warning('Missing avatar types:')
        for avType in cls._avatarMissing:
            print '   %r' % avType

        del cls._avatarMissing

    @classmethod
    def missingShipClass(cls, shipType):
        cls._shipMissing.add(shipType)

    @classmethod
    def printMissingShipTypes(cls):
        if not cls._shipMissing:
            return

        cls.notify.warning('Missing ship types:')
        for shipType in cls._shipMissing:
            print '   %r' % shipType

        del cls._shipMissing   

    @classmethod
    def missingAnimalClass(cls, avType):
        cls._animalMissing.add(avType)

    @classmethod
    def printMissingAnimalTypes(cls):
        if not cls._animalMissing:
            return

        cls.notify.warning('Missing animal types:')
        for avType in cls._animalMissing:
            print '   %r' % avType

        del cls._animalMissing 

    @classmethod
    def missingBossClass(cls, type):
        cls._bossMissing.add(type)

    @classmethod
    def printMissingBossTypes(cls):
        if not cls._bossMissing:
            return

        cls.notify.warning('Missing boss types:')
        for avType in cls._bossMissing:
            print '   %r' % avType

        del cls._bossMissing     

    @classmethod
    def badBossData(cls, name, dnaId):
        cls._badBosses.add("%s (%s)" % (name, dnaId)) 

    @classmethod
    def printBadBossTypes(cls):
        if not cls._badBosses:
            return

        cls.notify.warning('Failed to add the following bosses:')
        for avType in cls._badBosses:
            print '   %r' % avType

        del cls._badBosses            

    @classmethod
    def addRandomBoss(cls, avatarType):
        if avatarType in cls._randomBosses:
            return

        cls._randomBosses.append(avatarType)

    @classmethod
    def isRandomBossSpawned(cls, avatarType):
        return avatarType in cls._randomBosses

    @classmethod
    def removeRandomBoss(cls, avatarType):
        if avatarType not in cls._randomBosses:
            return

        cls._randomBosses.remove(avatarType)