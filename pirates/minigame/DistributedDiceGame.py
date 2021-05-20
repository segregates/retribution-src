from panda3d.core import Lens
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pirates.piratesbase import PLocalizer
from pirates.minigame import DistributedGameTable
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import DiceGlobals
from pirates.minigame import PlayingCard
from pirates.minigame import DiceGameGUI
from pirates.pirate import HumanDNA
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesbase import PiratesGlobals
from direct.task import Task

class DistributedDiceGame(DistributedGameTable.DistributedGameTable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGame')

    def __init__(self, cr, numdice = 5, public = 1, name = 'dice game'):
        DistributedGameTable.DistributedGameTable.__init__(self, cr)
        self.round = 0
        self.buttonSeat = 0
        self.gameState = DiceGlobals.DSTATE_GETREADY
        self.public = public
        self.numDice = numdice
        self.ante = 10
        self.NumSeats = 7
        self.lastSeat = -1
        self.gameName = name
        self.dicevals = { }

    def generate(self):
        DistributedGameTable.DistributedGameTable.generate(self)
        self.setName(self.uniqueName('DistributedDiceGame'))
        self.reparentTo(render)


    def getInteractText(self):
        return PLocalizer.InteractTableDice


    def getSitDownText(self):
        return PLocalizer.DiceSitDownDice


    def disable(self):
        DistributedGameTable.DistributedGameTable.disable(self)


    def delete(self):
        DistributedGameTable.DistributedGameTable.delete(self)
        if hasattr(self, 'dealer'):
            self.dealer.delete()
            del self.dealer


    def setTableState(self, round, buttonSeat):
        self.buttonSeat = buttonSeat
        if self.isLocalAvatarSeated():
            self.gui.setTableState(round, buttonSeat)


    def guiCallback(self, action):
        self.gui.disableAction()
        if action == 'roll':
            self.gui.rollDice()
        elif action == PlayingCardGlobals.Fold:
            self.d_clientAction(self.round, [
                action,
                0])
        elif action == -1:
            self.requestExit()
        elif self.extraGuiCallback(action):
            pass
        else:
            self.notify.error('guiCallback: unknown action: %s' % action)


    def localAvatarSatDown(self, seatIndex):
        DistributedGameTable.DistributedGameTable.localAvatarSatDown(self, seatIndex)
        self.gui = DiceGameGUI.DiceGameGUI(self, self.numDice, self.public, self.gameName)
        self.extraGuiSetup()
        camera.setPosHpr(self, 0, -10, 20, 0, -65, 0)
        base.camLens.setMinFov(55)
        self.mySeat = seatIndex


    def localAvatarGotUp(self, seatIndex):
        print 'DistributedDiceGame:localAvatarGotUp'
        self.extraGuiDestroy()
        self.gui.destroy()
        del self.gui
        DistributedGameTable.DistributedGameTable.localAvatarGotUp(self, seatIndex)


    def playerIsReady(self):
        if base.localAvatar.getGoldInPocket() < self.ante:
            base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
        else:
            self.sendUpdate('playerIsReady', [])
            self.gui.mainButton['state'] = DGG.DISABLED
            self.gui.mainButton['frameColor'] = (0, 0.4, 0.050000, 1)
            self.gameState = DiceGlobals.DSTATE_DOROLL

    def newRound(self):
        self.gui.mainButton.show()
        self.gui.resetGui()
        self.dicevals.clear()
        self.extraGuiReset()
        self.gui.mainButton['state'] = DGG.DISABLED
        self.gui.mainButton['frameColor'] = (0, 0.299, 0.4, 1)


    def yourTurn(self, activeSeat):
        print 'DistributedDiceGame:yourTurn - activeSeat %d' % activeSeat
        if activeSeat != self.mySeat:
            print 'DistributedDiceGame:yourTurn - not my seat (%d)' % self.mySeat
            return None

        if self.gameState == DiceGlobals.DSTATE_DOROLL:
            if activeSeat == self.mySeat:
                self.gui.timeToRoll()
            else:
                self.gui.mainButton['state'] = DGG.DISABLED

        self.extraYourTurn()


    def rollResults(self, seat, dice):
        self.dicevals[seat] = dice


    def playerHasLost(self, avId):
        pass


    def extraGuiSetup(self):
        pass


    def extraGuiDestroy(self):
        pass


    def extraYourTurn(self):
        pass


    def extraGuiReset(self):
        pass


    def currentTurn(self, state, seat, name):
        if seat != self.mySeat:
            self.lastSeat = seat

        self.gameState = state
        if state == DiceGlobals.DSTATE_PLAY:
            self.gui.updateTurnStatus(name + PLocalizer.DiceText_isTurn)
        elif state == DiceGlobals.DSTATE_DOROLL:
            self.gui.updateTurnStatus(name + PLocalizer.DiceText_Roll)



    def youWin(self, winId, name):
        self.gui.updateTurnStatus(name + PLocalizer.DiceText_Wins)
        avId = base.localAvatar.getDoId()
        if avId == winId:
            pass

        self.gui.mainButton['state'] = DGG.NORMAL
        self.gui.mainButton['text'] = 'READY'
        self.gui.mainButton['command'] = self.playerIsReady
        self.gui.mainButton['frameColor'] = (0, 0.4, 0.100, 1)
        self.gui.mainButton.show()
        self.gui.resetGui()
        self.dicevals.clear()
        self.extraGuiReset()


    def sendChat(self, chatType):
        avId = base.localAvatar.getDoId()
        self.sendUpdate('sendChat', [
            chatType,
            avId])
