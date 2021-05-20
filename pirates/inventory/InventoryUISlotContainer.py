from pirates.inventory.InventoryUIContainer import InventoryUIContainer


class InventoryUISlotContainer(InventoryUIContainer):
    ReferenceSlots = True

    def manageCells(self, slotList):
        self.slotList = slotList
        for index in xrange(len(self.slotList)):
            slot = self.slotList[index]
            cell = self.cellList[index]
            self.manager.assignCellSlot(cell, self.slotList[self.slotCount])
            self.slotCount += 1
