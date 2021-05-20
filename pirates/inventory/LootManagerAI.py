from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pirates.inventory.DistributedLootContainerAI import DistributedLootContainerAI
from pirates.inventory import DropGlobals, ItemGlobals
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
import random

class LootManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootManagerAI')

    def __init__(self, air):
        self.air = air
        self.containers = {}
        
        self.forceType = config.GetInt('force-loot-chest', 0)

        self.accept('goingOffline', self.__goingOffline)
        self.accept('containerDied', self.deleteContainer)
        taskMgr.doMethodLater(15, self.__removeContainers, 'purgeContainers')

    def spawnLoot(self, npc):
        if not config.GetBool('want-loot', False):
            return

        try:
            enemyLevel = npc.getLevel()
            players = npc.enemySkills.keys()
            enemyGrade = self.getEnemyGradeFromLevels(enemyLevel, players)
            dropRate = DropGlobals.getContainerDropRate(enemyGrade)

            if random.randrange(100) > dropRate and not config.GetBool('always-spawn-loot', True):
                return

            chestType = self.getChestTypeFromEnemyLevel(enemyLevel)
            container = DistributedLootContainerAI.makeFromObjectData(self.air, npc, type=chestType)
            container.setTimeout(config.GetInt('loot-timeout', 120))

            self.containers[container.doId] = container
        except Exception, e:
             self.notify.warning(e)

    def getChestTypeFromEnemyLevel(self, enemyLevel):
        if self.forceType > 0:
            return self.forceType

        sacRate, chestRate, rareRate = DropGlobals.getContainerTypeRate(enemyLevel)
        rareRate = 100 - rareRate
        chestRNG = random.randrange(100)

        if chestRNG < sacRate:
            return PiratesGlobals.ITEM_SAC
        elif chestRNG >= sacRate and chestRNG <= rareRate:
            return PiratesGlobals.TREASURE_CHEST
        elif chestRNG >= rareRate:
            return PiratesGlobals.RARE_CHEST
        else:
            return PiratesGlobals.ITEM_SAC

    def getEnemyGradeFromLevels(self, npcLevel, players):
        return EnemyGlobals.GREEN

    def __removeContainers(self, task):
        garbage = []

        for containerId, container in self.containers.iteritems():
            container.tick(15)
            timeout = container.getTimeout()

            if container.getEmpty() or container.getTimeout() <= 0 or not container.locks:
                garbage.append(containerId)
        
        for containerId in garbage:
            self.deleteContainer(containerId)

        return task.again

    def deleteContainer(self, containerId):
        if containerId not in self.containers:
            return

        container = self.containers[containerId]
        container.deleteContainer()
        del self.containers[containerId]

    def __goingOffline(self, avId):
        for container in [container for container in self.containers.values() if avId in container.getCreditLocks()]:
            container.removePirateFromCreditLock(avId)