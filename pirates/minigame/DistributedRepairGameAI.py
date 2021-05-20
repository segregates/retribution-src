from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.ai import HolidayGlobals
from DistributedRepairGameBase import *
import time

class DistributedRepairGameAI(DistributedObjectAI, DistributedRepairGameBase):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        DistributedRepairGameBase.__init__(self)
        self.difficulty = 0
        self.avId2game = {}
        self.avId2rewards = {}
        self.game2progress = [-1] * 5
        self.goldBonus = 1.0
        self.startTime = time.time()

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
    
    def getDifficulty(self):
        return self.difficulty
    
    def setLocation(self, location):
        self.location = location
    
    def getLocation(self):
        return self.location
    
    def isCycleComplete(self):
        for progress in self.game2progress:
            if progress != 100:
                return False
        
        return True
    
    def isCycleEmpty(self):
        for progress in self.game2progress:
            if progress != -1:
                return False
        
        return True
    
    def getSpeedMultiplier(self, time):
        if time <= 60:
            return 1.0
        elif time <= 120:
            return 0.6
        else:
            return 0.3
    
    def getDifficultyMultiplier(self):
        if self.difficulty == 0:
            return 6
        elif self.difficulty == 1:
            return 8
        else:
            return 10
    
    def setGameProgress(self, gameIndex, progress):
        self.game2progress[gameIndex] = progress
        self.updateGameProgress()
        
    def updateGameProgress(self):
        for avId in self.avId2game.keys():
            self.sendUpdateToAvatarId(avId, 'setMincroGameProgress', [self.game2progress])
    
    def updateAvatars(self):
        avatars = self.getAvatars()

        for avId in self.avId2game.keys():
            self.sendUpdateToAvatarId(avId, 'setAvatars', [avatars])
    
    def getAvatars(self):
        return [(avId, game) for avId, game in self.avId2game.iteritems() if game != -1]
    
    def joinAvatar(self, avId):
        if avId in self.avId2game:
            return False

        self.avId2game[avId] = -1
        self.avId2rewards[avId] = 0
        self.sendUpdateToAvatarId(avId, 'start', [self.location])
        self.sendUpdateToAvatarId(avId, 'setMincroGameProgress', [self.game2progress])
        self.sendUpdateToAvatarId(avId, 'setAvatars', [self.getAvatars()])
        return True
    
    def exitAvatar(self, avId):
        if avId not in self.avId2game:
            return False
        
        gameIndex = self.avId2game[avId]

        if gameIndex != -1:
            self.setGameProgress(gameIndex, -1)
        
        del self.avId2game[avId]
        self.updateAvatars()
        return True
    
    def requestMincroGame(self, gameIndex):
        if gameIndex >= self.getGameCount() or gameIndex in self.avId2game.values() or self.game2progress[gameIndex] == 100:
            return

        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.avId2game or self.avId2game[avId] != -1:
            return

        if self.isCycleEmpty():
            self.startTime = time.time()

        self.avId2game[avId] = gameIndex
        self.sendUpdateToAvatarId(avId, 'requestMincroGameResponse', [])
        self.setGameProgress(gameIndex, 0)
        self.updateAvatars()

    def reportMincroGameProgress(self, progress):
        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.avId2game:
            return

        gameIndex = self.avId2game[avId]
        
        if gameIndex == -1 or progress <= self.game2progress[gameIndex]:
            return

        self.setGameProgress(gameIndex, progress)
        
        if progress == 100:
            self.avId2game[avId] = -1
            self.avId2rewards[avId] += 1
            self.updateAvatars()
            
            if self.isCycleComplete():
                totalTime = int(time.time() - self.startTime)
                multiplier = self.getDifficultyMultiplier() * self.getSpeedMultiplier(totalTime) * self.goldBonus
                rewards = [(avId, reward * multiplier) for avId, reward in self.avId2rewards.iteritems() if reward]
                
                for avId, reward in rewards:
                    av = self.air.doId2do.get(avId)
                    
                    if av:
                        if self.air.newsManager.isHolidayRunning(HolidayGlobals.DOUBLEGOLDHOLIDAY):
                            reward = reward * 2
                        av.giveGold(reward)

                for avId in self.avId2game.keys():
                    self.sendUpdateToAvatarId(avId, 'cycleComplete', [rewards, totalTime])
                
                self.game2progress = [-1] * 5
                self.avId2rewards = {avId: 0 for avId in self.avId2rewards.keys()}
                self.updateGameProgress()

    def setGoldBonus(self, goldBonus):
        self.goldBonus = goldBonus

    def posControlledByCell(self):
        return False
