from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals
import random

class DistributedGameTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.gameVariation = PiratesGlobals.VILLAGER_TEAM
        self.dealerType = PiratesGlobals.VILLAGER_TEAM
        self.tableType = 1
        self.dealerName = 'Dealer'
        self.aiList = []

    def handleInteraction(self):
        if config.GetBool('want-tables-closed', False):
            msg = 'Client bypassed sanity check and called DistributedGameTableAI'
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), message=msg)
            return REJECT
            
        return ACCEPT

    def setTableType(self, type):
        self.tableType = type

    def getTableType(self):
        return self.tableType

    def setGameVariation(self, variant):
        self.gameVariation = variant

    def getGameVariation(self):
        return self.gameVariation

    def setDealerName(self, name):
        self.dealerName = name

    def getDealerName(self):
        return self.dealerName

    def setDealerType(self, type):
        self.dealerType = type

    def getDealerType(self):
        return self.dealerType

    def setAIList(self, list):
        self.aiList = list

    def getAIList(self):
        return self.aiList

    def requestSeat(self, todo0, todo1):
        self.notify.info("request Seat")

    def requestExit(self):
        self.notify.info("Request exit")

    def generatePlayers(self, seats=7, ai=3, available=[PiratesGlobals.VILLAGER_TEAM]):
        players = [0] * seats

        randomGen = random.Random()
        randomGen.seed(self.getUniqueId()) 

        if (ai > seats):
            self.notify.warning("Cannot have more ai then seats! reducing to 5")
            ai = 5

        for i in range(0, ai):
            aiType = randomGen.choice(available)
            players[i] = aiType

        randomGen.shuffle(players)
        self.setAIList(players)
        
    @staticmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setTableType(1)
        return obj