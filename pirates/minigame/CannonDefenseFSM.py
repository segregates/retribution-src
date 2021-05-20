from panda3d.core import TextNode
# File: C (Python 2.4)

from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.CannonDefenseScorePanelBase import RoundCompleteFlags
from pirates.piratesgui.CannonDefenseScoreBoard import CannonDefenseScoreBoard
from pirates.piratesgui.CannonDefenseCountdownUI import CannonDefenseCountdownUI
from pirates.minigame import CannonDefenseGlobals
import pirates.minigame.AmmoPanel as pirates

class CannonDefenseFSM(FSM):

    def __init__(self, gameDO):
        FSM.__init__(self, 'CannonDefenseFSM')
        self._resultScreen = None
        self._gameOverScreen = None
        self._victoryScreen = None
        self._countDownUI = None
        self._gameDO = gameDO
        self._CannonDefenseFSM__lblwaitingFor = None
        self.defaultTransitions = {
            'WaitingForPlayers': [
                'Tutorial'],
            'Tutorial': [
                'WaitingForPlayers',
                'Wave'],
            'Wave': [
                'ResultScreen',
                'WaitingForPlayers',
                'Defeat',
                'Victory'],
            'ResultScreen': [
                'WaitingForPlayers',
                'Wave'],
            'Defeat': [
                'WaitingForPlayers',
                'Wave'],
            'Victory': [
                'WaitingForPlayers',
                'Wave'] }


    def enterWaitingForPlayers(self):
        self._CannonDefenseFSM__createWaitingPlayersLabel()
        self._gameDO.disableCannonInput()



    def exitWaitingForPlayers(self):
        self._CannonDefenseFSM__destroyWaitingPlayersLabel()
        self._gameDO.enableCannonFire()


    def enterTutorial(self):
        self._gameDO.disableCannonFire()
        if localAvatar.cannon and hasattr(localAvatar.cannon.cgui, 'flashHelpButton'):
            localAvatar.cannon.cgui.flashHelpButton(0.200, 10)
            if localAvatar.cannon.ammoPanel.state == pirates.minigame.AmmoPanel.CLOSED:
                localAvatar.cannon.ammoPanel.onTabClick()


        self._countDownUI = CannonDefenseCountdownUI()
        self._countDownUI.reparentTo(base.a2dTopCenter)
        self._countDownUI.setPos(0.0, 0, -0.230)


    def exitTutorial(self):
        self._gameDO.enableCannonFire()
        if self._countDownUI:
            self._countDownUI.remove_node()
            self._countDownUI = None



    def enterWave(self):
        pass


    def exitWave(self):
        localAvatar.setPirateDazed(False)


    def enterResultScreen(self):
        self._CannonDefenseFSM__destroyVictoryScreen()
        self._gameDO.disableCannonInput()
        self._resultScreen = CannonDefenseScoreBoard(self._gameDO.getWaveNumber() + 1, self._gameDO.getBonusSet(), self._gameDO.getNumWaves(), RoundCompleteFlags.WAVE_COMPLETE)
        self._resultScreen.setupPanel1(self._gameDO.endOfWaveData)
        self._resultScreen.setScale(0.848)
        self._resultScreen.reparentTo(base.a2dRightCenter)
        self._resultScreen.setX(-2.28)
        self._resultScreen.setZ(-0.598)
        if localAvatar.cannon and hasattr(localAvatar.cannon, 'ammoPanel'):
            if localAvatar.cannon.ammoPanel.state == pirates.minigame.AmmoPanel.CLOSED:
                localAvatar.cannon.ammoPanel.onTabClick()


        messenger.send('flashHandleStart')


    def exitResultScreen(self):
        self._gameDO.enableCannonInput()
        self._CannonDefenseFSM__destroyResultScreen()
        if localAvatar.cannon and hasattr(localAvatar.cannon, 'ammoPanel'):
            if localAvatar.cannon.ammoPanel.state == pirates.minigame.AmmoPanel.OPENED:
                localAvatar.cannon.ammoPanel.onTabClick()


        messenger.send('flashHandleStop')


    def enterVictory(self):
        self._gameDO.disableCannonInput()
        self._victoryScreen = CannonDefenseScoreBoard(self._gameDO.getWaveNumber() + 1, self._gameDO.getBonusSet(), self._gameDO.getNumWaves(), RoundCompleteFlags.GAME_VICTORY)
        self._victoryScreen.setupPanel1(self._gameDO.endOfWaveData)
        self._victoryScreen.setupPanel3(self._gameDO.endOfWaveData)
        self._victoryScreen.panel3.nextButton['command'] = self._CannonDefenseFSM__continueGame
        self._CannonDefenseFSM__createWaitingLabel()


    def exitVictory(self):
        self._gameDO.enableCannonInput()
        self._CannonDefenseFSM__destroyVictoryScreen()
        self._CannonDefenseFSM__destroyWaitingLabel()


    def enterDefeat(self):
        self._gameDO.disableCannonInput()
        self._resultScreen = CannonDefenseScoreBoard(self._gameDO.getWaveNumber() + 1, self._gameDO.getBonusSet(), self._gameDO.getNumWaves(), RoundCompleteFlags.GAME_DEFEAT)
        self._resultScreen.setupPanel1(self._gameDO.endOfWaveData)
        self._resultScreen.setupPanel3(self._gameDO.endOfWaveData)
        self._resultScreen.panel3.nextButton['command'] = self._gameDO.exitMiniGame


    def exitDefeat(self):
        self._gameDO.enableCannonInput()
        self._CannonDefenseFSM__destroyResultScreen()


    def enterOff(self):
        self._CannonDefenseFSM__destroyVictoryScreen()


    def exitOff(self):
        pass


    def updateCountDown(self, timeLeft):
        if self._resultScreen:
            self._resultScreen.panel1.updateCountDown(timeLeft)

        if self._countDownUI:
            self._countDownUI.setTime(timeLeft - 1)
            if timeLeft <= 2:
                if localAvatar.cannon and hasattr(localAvatar.cannon, 'ammoPanel'):
                    if localAvatar.cannon.ammoPanel.state == pirates.minigame.AmmoPanel.OPENED:
                        localAvatar.cannon.ammoPanel.onTabClick()






    def _CannonDefenseFSM__continueGame(self):
        if self._victoryScreen:
            self._victoryScreen.panel3.nextButton['state'] = DGG.DISABLED

        self._gameDO.requestStartBonusRound()


    def _CannonDefenseFSM__destroyResultScreen(self):
        if self._resultScreen != None:
            self._resultScreen.destroy()
            self._resultScreen = None



    def _CannonDefenseFSM__destroyVictoryScreen(self):
        if self._victoryScreen != None:
            self._victoryScreen.destroy()
            self._victoryScreen = None



    def _CannonDefenseFSM__createWaitingLabel(self):
        self._CannonDefenseFSM__destroyWaitingLabel()
        self._CannonDefenseFSM__lblwaitingFor = OnscreenText(parent = base.a2dTopCenter, pos = (0.0, -0.13), text = PLocalizer.CannonDefense['Waiting'], font = PiratesGlobals.getPirateOutlineFont(), scale = 0.089, align = TextNode.ACenter, shadow = PiratesGuiGlobals.TextShadow, fg = PiratesGuiGlobals.TextFG1)


    def _CannonDefenseFSM__createWaitingPlayersLabel(self):
        self._CannonDefenseFSM__destroyWaitingLabel()
        self._CannonDefenseFSM__lblwaitingForPlayers = OnscreenText(parent = base.a2dTopCenter, pos = (0.0, -0.13), text = PLocalizer.CannonDefenseWaitingForPlayers, font = PiratesGlobals.getPirateOutlineFont(), scale = 0.089, align = TextNode.ACenter, shadow = PiratesGuiGlobals.TextShadow, fg = PiratesGuiGlobals.TextFG1)


    def _CannonDefenseFSM__destroyWaitingLabel(self):
        if self._CannonDefenseFSM__lblwaitingFor:
            self._CannonDefenseFSM__lblwaitingFor.destroy()
            self._CannonDefenseFSM__lblwaitingFor = None

    def _CannonDefenseFSM__destroyWaitingPlayersLabel(self):
        if self._CannonDefenseFSM__lblwaitingForPlayers:
            self._CannonDefenseFSM__lblwaitingForPlayers.destroy()
            self._CannonDefenseFSM__lblwaitingForPlayers = None
