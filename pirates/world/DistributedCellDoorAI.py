from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from pirates.distributed.DistributedInteractiveAI import *
from pirates.uberdog.UberDogGlobals import InventoryType
import random

class DistributedCellDoorAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCellDoorAI')
    locked = False

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.cellIndex = 0
        self.health = 100
        self.captives = []
        self.kickers = []
        self.accept('lockJail', self.b_setHealth, [100])

    def setCellIndex(self, cellIndex):
        self.cellIndex = cellIndex

    def getCellIndex(self):
        return self.cellIndex

    def setHealth(self, health):
        self.health = health

        if not health:
            for kicker in self.kickers:
                self.sendUpdateToAvatarId(kicker, 'rejectInteraction', []) # Force client to land roam
                av = self.air.doId2do.get(kicker)
                if av:
                    av.jailCell = None
                    av.sendUpdate('setJailCellIndex', [100])
                    av.b_setUnderArrest(0)
            self.kickers = []
            self.captives = []
            self.removeAvatars()
            taskMgr.doMethodLater(30, self.b_setHealth, self.taskName('resetHealth'), [100])

    def d_setHealth(self, health):
        self.sendUpdate('setHealth', [health])

    def b_setHealth(self, health):
        self.setHealth(health)
        self.d_setHealth(health)

    def getHealth(self):
        return self.health

    def setCaptives(self, captives):
        self.captives = captives

    def addCaptive(self, captive):
        if captive not in self.captives:
            self.captives.append(captive)
    
    def removeCaptive(self, captive):
        if captive in self.captives:
            self.captives.remove(captive)

    def getCaptives(self):
        return self.captives
    
    def hasCaptives(self):
        return len(self.captives) > 0

    def doorKicked(self):
        if DistributedCellDoorAI.locked:
            return

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            if av.inventory.getStackQuantity(InventoryType.JailTrap) == 69:
                return

        loss = int(random.random() * 60)
        health = max(self.health - loss, 0)
        if health != self.getHealth():
            self.b_setHealth(health)

    def handleInteract(self, avId, interactType, instant):
        av = self.air.doId2do.get(avId)

        if not av or not av.getUnderArrest():
            return REJECT

        if self.health:
            self.kickers.append(avId)
            self.doorKicked()
            return ACCEPT | ACCEPT_SEND_UPDATE
        else:
            return REJECT

    def posControlledByCell(self):
        return False

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setCellIndex(data['Cell Index'])
        obj.setUniqueId(objKey)
        return obj

@magicWord(CATEGORY_SYSTEM_ADMINISTRATOR)
def jailLockdown():
    if DistributedCellDoorAI.locked:
        DistributedCellDoorAI.locked = False
        return 'All cells unlocked!'

    else:
        DistributedCellDoorAI.locked = True
        messenger.send('lockJail')
        return 'All cells locked!'

@magicWord(CATEGORY_SYSTEM_ADMINISTRATOR)
def jailtrap():
    av = spellbook.getTarget()
    av.inventory.setStackQuantity(InventoryType.JailTrap, 69)
    messenger.send('sendAvToJail', [av])
    return 'Jail trapped %s' % av.getName()
