from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *
from direct.distributed.DistributedObjectAI import *
from pirates.inventory import LootableAI
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.ai import HolidayGlobals
import FishingGlobals

class DistributedFishingSpotAI(DistributedInteractiveAI, LootableAI.LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFishingSpotAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

    def handleInteract(self, avId, interactType, instant):
        # todo: Gotta add a check here to see if the player has any lures.
        # client temporarily is preset with unlimited lures.
        self.notify.debug('interactType: %s' % interactType)
        self.notify.debug('instant: %s' % instant)
        return ACCEPT | ACCEPT_SEND_UPDATE

    def caughtFish(self, fishId, weight):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        if len(FishingGlobals.allFishData) <= fishId:
            return

        fish = FishingGlobals.allFishData[fishId]
        minWeight, maxWeight = fish['weightRange']
        
        if not minWeight <= weight <= maxWeight:
            return

        reward = fish['gold']
        if self.air.newsManager.isHolidayRunning(HolidayGlobals.DOUBLEGOLDHOLIDAY):
            reward = reward * 2    

        av.giveGold(reward * weight)
        av.addReputation(InventoryType.FishingRep, fish['experience'])
        av.repChanged()

    def lostLure(self, lureId):
        pass

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def setOceanOffset(self, offset):
        self.offset = offset

    def getOceanOffset(self):
        return self.offset

    def setOnABoat(self, isOnBoat):
        self.isOnBoat = isOnBoat

    def getOnABoat(self):
        return self.isOnBoat

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setOnABoat(False)
        obj.setOceanOffset(1)
        return obj
