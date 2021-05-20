from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.GridParent import GridParent
from pirates.distributed.DistributedInteractiveAI import *
from pirates.inventory.LootableAI import LootableAI
from pirates.inventory import DropGlobals, ItemGlobals
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
import random, copy, os

ItemTypes = [InventoryType.ItemTypeWeapon, InventoryType.ItemTypeClothing, InventoryType.ItemTypeClothing, InventoryType.ItemTypeClothing, InventoryType.ItemTypeWeapon, InventoryType.ItemTypeWeapon]
#ItemTypes = [InventoryType.ItemTypeWeapon, InventoryType.ItemTypeConsumable, InventoryType.ItemTypeCharm, InventoryType.ItemTypeClothing, InventoryCategory.CARDS, InventoryCategory.WEAPON_PISTOL_AMMO]

class DistributedLootContainerAI(DistributedInteractiveAI, LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        LootableAI.__init__(self, air)
        self.vizZone = ''
        self.lootType = PiratesGlobals.ITEM_SAC
        self.locks = []
        self.empty = False
        self.timeout = 36000
        self.avatarType = None
        self.avatarLevel = 0
        self.plunder = {}
    
    def delete(self):
        DistributedInteractiveAI.delete(self)
        taskMgr.remove(self.uniqueName('deleteContainer'))

    def setVisZone(self, vizZone):
        self.vizZone = vizZone

    def getVisZone(self):
        return self.vizZone

    def setType(self, type):
        self.lootType = type

    def getType(self):
        return self.lootType

    def setEmpty(self, empty):
        self.empty = empty

    def d_setEmpty(self, empty):
        self.sendUpdate('setEmpty', [empty])

    def b_setEmpty(self, empty):
        self.setEmpty(empty)
        self.d_setEmpty(empty)
    
    def f_setEmpty(self, avId, empty):
        self.sendUpdateToAvatarId(avId, 'setEmpty', [empty])

    def getEmpty(self):
        return self.empty

    def setCreditLocks(self, locks):
        self.locks = locks

    def getCreditLocks(self):
        return self.locks
    
    def deleteContainer(self):
        if not taskMgr.hasTaskNamed(self.uniqueName('deleteContainer')):
            self.b_setEmpty(True)
            taskMgr.doMethodLater(1.5, lambda task: self.requestDelete(), self.uniqueName('deleteContainer'))
    
    def removePirateFromCreditLock(self, avatarId):
        if avatarId in self.plunder:
            del self.plunder[avatarId]
            self.f_setEmpty(avatarId, True)

        if avatarId in self.locks:
            self.locks.remove(avatarId)
            
            if not self.locks:
                messenger.send('containerDied', [self.doId])

    def setTimeout(self, timeout):
        self.timeout = timeout

    def tick(self, amount):
        self.timeout -= amount

    def getTimeout(self):
        return self.timeout
    
    def setAvatarType(self, avatarType):
        self.avatarType = avatarType
    
    def getAvatarType(self):
        return self.avatarType
    
    def setAvatarLevel(self, avatarLevel):
        self.avatarLevel = avatarLevel
    
    def getAvatarLevel(self):
        return self.avatarLevel
    
    def setPlunder(self, plunder):
        self.plunder = plunder
    
    def getPlunder(self):
        return self.plunder
    
    def posControlledByCell(self):
        return False

    def startLooting(self, avId, timer):
        self.sendUpdateToAvatarId(avId, 'startLooting', [self.plunder[avId], timer])
    
    def handleInteract(self, avId, interactType, instant):
        if avId not in self.locks:
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), message='Client bypassed lock check and tried to interact with DistributedLootContainerAI')
            return REJECT

        if avId not in self.plunder or not self.plunder[avId]:
            return REJECT

        self.startLooting(avId, 0)
        return ACCEPT | ACCEPT_SEND_UPDATE
    
    def requestItem(self, item):
        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.locks or avId not in self.plunder:
            return
        
        items = self.plunder[avId]
        
        if item not in items:
            return

        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        del self.plunder[avId][items.index(item)]
        
        if not self.plunder[avId]:
            self.removePirateFromCreditLock(avId)

        self.giveItem(av, item)

    def requestItems(self):
        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.locks or avId not in self.plunder:
            return
        
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        items = self.plunder[avId]
        
        for item in items:
            self.giveItem(av, item)
        
        self.removePirateFromCreditLock(avId)
    
    def giveItem(self, av, item):
        itemClass, itemId, amount = item
        
        if itemClass == InventoryType.ItemTypeMoney:
            av.giveGold(amount)
            return
        
        inv = av.getInventory()
        
        if not inv:
            return

        location = inv.findAvailableLocation(itemClass, itemId=itemId, count=1, equippable=True)
        
        if location != -1:
            inv.addLocatable(itemId, location, 1, inventoryType=itemClass, colorId=amount)
    
    def isGenderAlright(self, av, itemClass, itemId):
        if itemClass != InventoryType.ItemTypeClothing:
            return True
        
        gender = av.style.getGender()
        
        if gender == 'm' and ItemGlobals.getMaleModelId(itemId) == -1:
            return False
        elif gender == 'f' and ItemGlobals.getFemaleModelId(itemId) == -1:
            return False
        
        return True         
    
    def getColor(self, itemId):
        if (not ItemGlobals.canDyeItem(itemId)) or random.random() > 0.05:
            return 0
        else:
            return random.randint(21, 30)

    def getRandomItem(self, av, npc, enemyItems, itemRarities, itemTypes):
        itemRarity = self.chooseFromRate(itemRarities)
        
        if itemRarity > 1 and (av.getLevel() < 30 or npc.getLevel() < 30):
            itemRarity = 1

        itemType = ItemTypes[self.chooseFromRate(itemTypes)]

        random.shuffle(enemyItems)

        for itemId in enemyItems:
            itemClass = ItemGlobals.getClass(itemId)
            
            if itemClass == itemType and ItemGlobals.getRarity(itemId) == itemRarity and PLocalizer.hasItemName(itemId) and self.isGenderAlright(av, itemClass, itemId):
                return (itemType, itemId, self.getColor(itemId))
    
    def chooseFromRate(self, rates):
        rolled = random.uniform(0, 1)
        
        for i, rate in enumerate(rates):
            if rate <= rolled:
                return i
        
        return 0
        
    def getContainerPlunder(self, av, npc):
        enemyItems = DropGlobals.getEnemyDropItemsByType(npc.avatarType, npc.getUniqueId())

        itemRarities = DropGlobals.getItemRarityRate(self.lootType)
        itemTypes = DropGlobals.getItemTypeRate(self.lootType)
        itemRate = self.chooseFromRate(DropGlobals.getNumItemsRate(self.lootType)) + 1
        items = []
        
        if random.random() >= 0.8:
            gold = random.randint(*DropGlobals.getItemGoldRate(self.lootType))
            items.append((InventoryType.ItemTypeMoney, 0, gold))
            itemRate -= 1
        
        for i in xrange(itemRate):
            item = self.getRandomItem(av, npc, enemyItems, itemRarities, itemTypes)
            
            if item:
                items.append(item)
        
        if not items:
            gold = random.randint(*DropGlobals.getItemGoldRate(self.lootType))
            items.append((InventoryType.ItemTypeMoney, 0, gold))

        return items
    
    def setupPlunder(self, npc):
        self.plunder = {}
        
        for avId in self.locks:
            av = self.air.doId2do.get(avId)
            
            if av:
                self.plunder[avId] = self.getContainerPlunder(av, npc)

    @staticmethod
    def makeFromObjectData(air, npc, type=PiratesGlobals.ITEM_SAC):
        obj = DistributedLootContainerAI(air)
        obj.setCreditLocks(npc.enemySkills.keys())
        obj.setAvatarType(npc.avatarType)
        obj.setAvatarLevel(npc.getLevel())
        obj.setType(type)
        obj.setupPlunder(npc)
        
        area = npc.getParentObj()
        cell = GridParent.getCellOrigin(area, npc.zoneId)
        
        obj.setPos(npc.getPos(cell))
        obj.setHpr(npc.getHpr())
        obj.generateWithRequiredAndId(air.allocateChannel(), area.doId, npc.zoneId)
        obj.sendUpdate('setPos', list(obj.getPos()))

        return obj