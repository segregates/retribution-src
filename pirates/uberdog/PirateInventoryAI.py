from pirates.reputation import ReputationGlobals
from pirates.inventory import InventoryGlobals
from DistributedInventoryAI import DistributedInventoryAI
from TradableInventoryBase import *
from UberDogGlobals import *
from InventoryInit import *

class PirateInventoryAI(DistributedInventoryAI):
    def announceGenerate(self):
        DistributedInventoryAI.announceGenerate(self)
        av = self.air.doId2do.get(self.ownerId)
        if av:
            av.inventory = self
            av.gotInventory()

        else:
            self.notify.warning('Inventory ownerId %d not found!' % self.ownerId)

    def hasItem(self, item):
        return item == self._locatableItems.get(item[self.ITEM_LOCATION_IDX])

    def moveLocatables(self, item1, item2):
        # Sanity check
        _item1 = self._locatableItems.get(item1[self.ITEM_LOCATION_IDX])
        _item2 = self._locatableItems.get(item2[self.ITEM_LOCATION_IDX])

        swapping = True
        invalid = ''

        if _item1 is not None:
            if _item1 != item1:
                invalid = 'Item 1 does not match'

        elif item1[self.ITEM_CAT_IDX]:
            # If we have nothing in item 1, make sure the player is not trying to add something else than nothing
            invalid = 'Invalid item 1'

        if _item2 is not None:
            if _item2 != item2:
                invalid = 'Item 2 does not match'

        elif item2[self.ITEM_CAT_IDX]:
            # Same as above
            invalid = 'Invalid item 2'

        if invalid:
            self.notify.warning('moveLocatables error: %s' % invalid)
            self.air.writeServerEvent('suspicious', avId=self.ownerId, message=invalid)
            return

        # Swap
        item1 = list(item1)
        item2 = list(item2)

        loc1 = item1[self.ITEM_LOCATION_IDX]
        loc2 = item2[self.ITEM_LOCATION_IDX]

        try:
            del self._locatableItems[loc1]

        except KeyError:
            pass

        try:
            del self._locatableItems[loc2]

        except KeyError:
            pass

        item1[self.ITEM_LOCATION_IDX] = loc2
        item2[self.ITEM_LOCATION_IDX] = loc1

        self._locatableItems[loc1] = InvItem(tuple(item2))
        self._locatableItems[loc2] = InvItem(tuple(item1))

        self.air.writeServerEvent('inventory-item-moved', avId=self.ownerId, item1=item1, item2=item2, swapping=swapping)

        # Update
        self.d_update()

    def d_update(self):
        self.sendUpdate('setLocatables', [prepareSwitchField(self._locatableItems.values())])

    def trashLocatables(self, items):
        deleted = False
        
        for item in items:
            itemObj = InvItem(item)

            if not self.canRemoveLocatable(itemObj):
                continue

            del self._locatableItems[item[self.ITEM_LOCATION_IDX]]
            deleted = True

        if deleted:
            self.d_update()

    def getCategoryLevel(self, category):
        rep = self.getReputation(category)
        return ReputationGlobals.getLevelFromTotalReputation(category, rep)[0]

    def addReputation(self, category, value):
        current = self.getReputation(category)
        current += value
        current = max(current, 0)
        current = min(current, AccumulatorLimits.get(category, 2 ** 32 - 1))

        self.accumulators[category] = current

        if category != InventoryType.OverallRep:
            # Update overall reputation
            total = sum(v for k, v in self.accumulators.items() if InventoryType.begin_Accumulator < k < InventoryType.end_Accumulator)
            self.accumulators[InventoryType.OverallRep] = total

        self.sendUpdate('setAccumulators', [self.accumulators.items()])

    def setStackQuantity(self, item, amount):
        stacks = self.stacks.copy()
        stacks[item] = amount
        self.setStacks(stacks.items())
        self.sendUpdate('setStacks', [self.stacks.items()])

    def addStackItem(self, item, amount=1):
        oldVal = self.getStackQuantity(item)
        val = max(0, oldVal + amount)
        self.setStackQuantity(item, val)

    def addLocatable(self, itemId, slot, amount, inventoryType=InventoryType.ItemTypeWeapon, colorId=0, update=True):
        if not self.locationAvailable(slot):
            return False
        self._locatableItems[slot] = InvItem(tuple([inventoryType, itemId, slot, 0, colorId, amount]))
        if update:
            self.d_update()
        return True
