from direct.distributed.DistributedObjectAI import DistributedObjectAI
from DistributedRepairGameBase import *
import time

class DistributedCannonDefenseAI(DistributedObjectAI, DistributedCannonDefenseAI):


    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.difficulty = 0
        self.avId2game = {}

    def handleInteract(self, avId, interactType, instant):
        self.notify.debug('interactType: %s' % interactType)
        self.notify.debug('instant: %s' % instant)
        return ACCEPT | ACCEPT_SEND_UPDATE

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

        if self.game:
            self.game.setDifficulty(self.difficulty)

    def getDifficulty(self):
        return self.difficulty

    def generate(self):
        DistributedCannonDefenseAI.generate(self)

    def announceGenerate(self):
        DistributedCannonDefenseAI.announceGenerate(self)
        self.game = DistributedCannonDefenseAI(self.air)
        self.game.setDifficulty(self.difficulty)
        self.getParentObj().generateChild(self.game, self.zoneId)

    def setGameProgress(self, gameIndex, progress):
        self.game2progress[gameIndex] = progress
        self.updateGameProgress()

    def updateGameProgress(self):
        for avId in self.avId2game.keys():
            self.sendUpdateToAvatarId(avId, 'setWaveProgress', [self.game2progress])

