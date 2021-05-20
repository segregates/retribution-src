from DistributedGAInteriorAI import *
from DistributedCellDoorAI import *

import random

class DistributedJailInteriorAI(DistributedGAInteriorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJailInteriorAI')

    def __init__(self, air, extDoor):
        DistributedGAInteriorAI.__init__(self, air, extDoor)
        self.cells = []

    def setUniqueId(self, uid):
        DistributedGAInteriorAI.setUniqueId(self, uid)
        island = self.extDoor.getParentObj()
        island.jail = self

        if island.getName() == 'Port Royal':
            self.air.portRoyalJail = self

    def allocateCell(self, av):
        for cell in self.cells:
            if not cell.hasCaptives():
                self.addToCell(av, cell)
                return
        
        self.addToCell(av, random.choice(self.cells))

    def addToCell(self, av, cell):
        av.jailCell = cell
        cell.addCaptive(av.doId)
        av.sendUpdate('setJailCellIndex', [cell.getCellIndex()])

    def createObject(self, objType, parent, objKey, object):
        genObj = None

        if objType == 'Jail Cell Door':
            genObj = DistributedCellDoorAI.makeFromObjectKey(self.air, objKey, object)
            self.generateChild(genObj)
            self.cells.append(genObj)

        else:
            genObj = DistributedGAInteriorAI.createObject(self, objType, parent, objKey, object)

        return genObj
