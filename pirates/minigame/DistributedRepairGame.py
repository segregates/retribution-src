from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from DistributedRepairGameBase import DistributedRepairGameBase
from DistributedRepairGameBase import GAME_OPEN, GAME_ORDER, DIFFICULTY_MAX, ON_LAND
from RepairClock import RepairClock
from RepairGameGUI import RepairGameGUI
from RepairGameFSM import RepairGameFSM
from RepairMousePicker import RepairMousePicker
import RepairGlobals
from pirates.audio import SoundGlobals
import time

class DistributedRepairGame(DistributedRepairGameBase, DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairGame')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        DistributedRepairGameBase.__init__(self)
        self.accept('onCodeReload', self.codeReload)
        self.gameFSM = None
        self.goldBonus = 0
        self.difficulty = 0

    def codeReload(self):
        reload(RepairGlobals)

    def setGoldBonus(self, goldBonusAmount):
        self.goldBonus = goldBonusAmount

    def getGoldBonus(self):
        return self.goldBonus
    
    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def start(self, location):
        if self.gameFSM:
            self.gameFSM.request('Off')

        self.location = location

        if location == ON_LAND:
            base.loadingScreen.showTarget(benchRepair = True)
        else:
            base.loadingScreen.showTarget(shipRepair = True)
        base.cr.loadingScreen.show()
        self.gameIndexRequested = -1
        self.gameProgress = [
            GAME_OPEN] * self.getGameCount()
        self.gameFSM = RepairGameFSM(self)
        self.gameFSM.request('Init')
        self.difficultyMax = DIFFICULTY_MAX + 0.0
        self.doIds2Rewards = { }
        self.cycleCompleteTime = 0
        self.currentGame = None
        self.gui = RepairGameGUI(self)
        base.loadingScreen.beginStep('left')
        self.repairClock = RepairClock(self)
        self.mousePicker = RepairMousePicker()
        self.games = []
        base.loadingScreen.endStep('left')
        base.loadingScreen.beginStep('games', 1, 48)
        for gameClass in GAME_ORDER[self.location]:
            self.games.append(gameClass(self))

        base.loadingScreen.endStep('games')
        self.gui.setGames(self.games)
        base.loadingScreen.beginStep('Intro')
        self.gameFSM.request('Intro')
        base.loadingScreen.endStep('Intro')
        base.loadingScreen.hide()
        self.time = time.time()

    def stop(self):
        # This is not perfect.
        if not self.gameFSM:
            return None

        self.notify.debug('stop')
        if self.gameFSM.getCurrentOrNextState() in [
            'Idle',
            'MincroGame',
            'CycleComplete']:
            self.gameFSM.request('Outro')
        else:
            self.cleanup()

    def cleanup(self):
        # This is not perfect.
        if not self.gameFSM:
            return None

        if self.gameFSM.getCurrentOrNextState() != 'Off':
            self.gameFSM.request('Off')
            if not self.gameFSM:
                return None

        self.gameIndexRequested = None
        del self.gameProgress[:]
        del self.gameProgress
        self.gameFSM.destroy()
        self.gameFSM = None
        self.mousePicker.destroy()
        self.mousePicker = None
        if hasattr(self, 'gui'):
            self.gui.destroy()
            self.gui = None

        if hasattr(self, 'repairClock'):
            self.repairClock.destroy()
            self.repairClock = None

        if hasattr(self, 'games'):
            for game in self.games:
                game.destroy()

            del self.games[:]
            del self.games

        shipRepairMusic = [
            SoundGlobals.MUSIC_PERFORMERS_02,
            SoundGlobals.MUSIC_PERFORMERS_07,
            SoundGlobals.MUSIC_PERFORMERS_09]
        for song in shipRepairMusic:
            base.musicMgr.stop(song)

    def isCycleComplete(self):
        for progress in self.gameProgress:
            if progress != 100:
                return False

        return True

    def isThereAnOpenGame(self):
        for progress in self.gameProgress:
            if progress == -1:
                return True

        return False

    def d_requestMincroGame(self, gameIndex):
        if self.gameFSM.state in [
            'Idle',
            'MincroGame']:
            self.gameIndexRequested = gameIndex
            self.sendUpdate('requestMincroGame', [
                gameIndex])

    def requestMincroGameResponse(self):
        self.gui.setDifficulty(self.difficulty)
        self.gameFSM.request('MincroGame', self.gameIndexRequested, self.difficulty)

    def d_reportMincroGameProgress(self, progress, rating = 0):
        self.sendUpdate('reportMincroGameProgress', [progress])

    def setMincroGameProgress(self, progress):
        for game, gameProgress in enumerate(progress):
            self.setGameProgress(game, gameProgress)
    
    def setGameProgress(self, gameIndex, progress):
        if hasattr(self, 'gui') and self.gui:
            self.gui.setProgress(gameIndex, progress)

        if hasattr(self, 'gameProgress'):
            self.gameProgress[gameIndex] = progress

        if hasattr(self, 'currentGame') and self.currentGame:
            self.currentGame.updatePostWinLabel()

    def setAvatars(self, avatars):
        if hasattr(self, 'gui') and self.gui:
            self.gui.updatePirateNamesPerMincrogame(avatars)

    def cycleComplete(self, rewards, totalTime):
        if self.gameFSM == None:
            return None

        if self.gameFSM.state == 'Intro':
            return None

        self.setRewards(rewards)
        self.setCycleCompleteTime(totalTime)
        self.gameFSM.request('CycleComplete')

    def setRewards(self, rewards):
        self.doIds2Rewards = {doId: reward for doId, reward in rewards}

    def getReward(self, doId):
        if doId in self.doIds2Rewards:
            return self.doIds2Rewards[doId]
        else:
            return 0

    def setCycleCompleteTime(self, totalTime):
        self.cycleCompleteTime = totalTime

    def getCycleCompleteTime(self):
        return self.cycleCompleteTime

    def shipDamaged(self, wasGrapeshot = False, difficulty = 0):
        if hasattr(self, 'gui') and self.gui:
            self.gui.onShipDamaged(wasGrapeshot)
            self.gui.setDifficulty(difficulty)

    def delete(self):
        DistributedObject.delete(self)
        self.ignore('onCodeReload')
        if hasattr(self, 'gameFSM'):
            self.cleanup()

    def handleArrivedOnShip(self, ship):
        pass

    def handleLeftShip(self, ship):
        pass
