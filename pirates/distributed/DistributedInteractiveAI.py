from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

from pirates.world.DistributedLocatableObjectAI import DistributedLocatableObjectAI

IGNORE = 0
REJECT = 1
ACCEPT = 2
ACCEPT_SET_AV = 4
ACCEPT_SEND_UPDATE = 8

class DistributedInteractiveAI(DistributedLocatableObjectAI, DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractiveAI')

    def __init__(self, air):
        DistributedLocatableObjectAI.__init__(self, air)
        DistributedNodeAI.__init__(self, air)
        self.avIds = []
        self.uniqueId = ''
        self.uid = ''

    def isBattleable(self):
        return 0

    def setUniqueId(self, uid):
        self.uid = uid

    def getUniqueId(self):
        return self.uid
    
    def allowMultipleAvatars(self):
        return False

    def requestInteraction(self, avId, interactType, instant):
        if avId != self.air.getAvatarIdFromSender():
            self.air.writeServerEvent('suspicious', avId=avId, message='tried to requestInteraction as someone else!')
            return

        if avId not in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId=avId, message='tried to requestInteraction but not in shard!')
            return

        if (self.avIds and not self.allowMultipleAvatars()) or avId in self.avIds:
            self.sendUpdateToAvatarId(avId, 'rejectInteraction', [])
            return

        self.notify.debug('%d requested interaction.' % avId)

        result = self.handleInteract(avId, interactType, instant)
        if result & ACCEPT:
            if result & ACCEPT_SET_AV:
                self.addAvatar(avId)

            if result & ACCEPT_SEND_UPDATE:
                self.sendUpdateToAvatarId(avId, 'acceptInteraction', [])

        elif result & REJECT:
            self.sendUpdateToAvatarId(avId, 'rejectInteraction', [])

    def handleInteract(self, avId, interactType, instant):
        ''' Must be overwritten by subclasses '''
        return REJECT

    def d_offerOptions(self, optionsId, statusCodes):
        self.sendUpdateToAvatarId(self.avId, 'offerOptions', [optionIds, statusCodes])

    def addAvatar(self, avId):
        if avId in self.avIds:
            return False

        self.avIds.append(avId)
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.exitAvatar, [avId])
        self.sendUpdate('setUserIds', [self.avIds])
        return True

    def exitAvatar(self, avId):
        if avId not in self.avIds:
            return False
        
        self.avIds.remove(avId)
        self.ignore(self.air.getAvatarExitEvent(avId))
        self.sendUpdate('setUserIds', [self.avIds])
        return True
    
    def hasNoAvatar(self):
        return not self.avIds
    
    def isAvatar(self, avId):
        return avId in self.avIds
    
    def removeAvatars(self):
        for avId in self.avIds:
            self.exitAvatar(avId)
    
    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()

        if avId not in self.avIds:
            self.air.writeServerEvent('suspicious', avId=avId, message='tried to requestExit as someone else!')
            return

        self.exitAvatar(avId)

    def demandExit(self):
        self.requestExit()

    def offerOptions(self, optionIds, statusCodes):
        self.optionIds = optionIds
        self.statusCodes = statusCodes

    def selectOption(self, optionId):
        self.optionId = optionId

    def d_selectOption(self, optionId):
        self.sendUpdate('selectOption', [optionId])

    def b_selectOption(self, optionId):
        self.selectOption(optionId)
        self.d_selectOption(optionId)

    def posControlledByCell(self):
        return True

    @staticmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = cls(air)
        obj.setUniqueId(objKey)
        obj.setPos(data.get('Pos', 0))
        obj.setHpr(data.get('Hpr', 0))
        return obj
