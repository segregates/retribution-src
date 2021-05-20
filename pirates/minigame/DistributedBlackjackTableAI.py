from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI

class DistributedBlackjackTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTableAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.pendingStakes = 0
        self.activeStakes = 0
        self.runningStakes = 0
        self.betMultiplier = 1
        self.tableState = (0, 0, [], [], [], [0, 0, 0, 0, 0, 0, 0, 0])

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)

    def delete(self):
        DistributedGameTableAI.delete(self)

    def handleInteract(self, avId, interactType, instant):
        return REJECT # TODO

    def setPendingStakes(self, pending):
        self.pendingStakes = pending

    def getPendingStakes(self):
        return self.pendingStakes

    def setActiveStakes(self, stakes):
        self.activeStakes = stakes

    def getActiveStakes(self):
        return self.activeStakes

    def setTableState(self, round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount):
        self.tableState = (round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount)

    def startRound(self, todo0, todo1, todo2):
        self.sendUpdate("startRound", [todo0, todo1, todo2])

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = multiplier

    def getBetMultiplier(self):
        return self.betMultiplier

    def leftGame(self):
        pass

    def posControlledByCell(self):
        return True

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedGameTableAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setBetMultiplier(int(data.get('BetMultiplier', '1')))
        return obj