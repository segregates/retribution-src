from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *
from DistributedRepairGameAI import DistributedRepairGameAI
from DistributedRepairGameBase import GAME_OPEN, GAME_ORDER, DIFFICULTY_MAX, ON_LAND

class DistributedRepairBenchAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairBenchAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.difficulty = 0
        self.game = None
    
    def allowMultipleAvatars(self):
        return True

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        
        if self.game:
            self.game.setDifficulty(self.difficulty)

    def getDifficulty(self):
        return self.difficulty

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)
        self.game = DistributedRepairGameAI(self.air)
        self.game.setDifficulty(self.difficulty)
        self.game.setLocation(ON_LAND)
        self.getParentObj().generateChild(self.game, self.zoneId)

    def handleInteract(self, avId, interactType, instant):
        if self.game.joinAvatar(avId):
            return ACCEPT | ACCEPT_SEND_UPDATE | ACCEPT_SET_AV
        else:
            return REJECT
    
    def exitAvatar(self, avId):
        if DistributedInteractiveAI.exitAvatar(self, avId):
            self.game.exitAvatar(avId)

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setDifficulty(int(data.get('difficulty', '0')))
        return obj
