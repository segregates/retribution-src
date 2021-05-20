from panda3d.core import NodePath
import random
import math
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from RepairMincroGame import RepairMincroGame
from RepairGridPiece import RepairGridPiece, GOAL_HORIZ_1, GOAL_HORIZ_2, GOAL_VERT_1, GOAL_CROSS_1_1
from RepairGridPiece import TOP, BOTTOM, LEFT, RIGHT
import RepairGlobals
SPACING = 0.149
GRID_SIZE = 4

class RepairBracingGame(RepairMincroGame):
    moveSound = None
    lineCompleteSound = None

    def __init__(self, repairGame):
        self.config = RepairGlobals.Bracing
        RepairMincroGame.__init__(self, repairGame, 'bracing', PLocalizer.Minigame_Repair_Bracing_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.currentGridDimensionAndLineCount = self.config.difficultyLevels[0]
        self.linesComplete = 0

    def _initAudio(self):
        if not self.moveSound:
            RepairBracingGame.moveSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_BRACE_PIECEMOVE)
            RepairBracingGame.lineCompleteSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_BRACE_LINECOMPLETE)

        RepairMincroGame._initAudio(self)

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_bracing_main')
        self.background = self.model.find('**/background')
        self.background.reparentTo(self)
        self.background.setZ(0.174)
        self.gridParent = self.attachNewNode('gridParent')
        self.grid = []
        for xpos in xrange(GRID_SIZE):
            col = []
            for ypos in xrange(GRID_SIZE):
                allWoodSquaresGeom = NodePath('wood_squares')
                for i in xrange(self.model.find('**/wood_squares').getNumChildren()):
                    self.model.find('**/wood_squares').getChild(i).copyTo(allWoodSquaresGeom)

                tempGeom = NodePath('tempGeom')
                self.model.find('**/wood_squares').getChild(0).copyTo(tempGeom)
                selectedOutlineGeom = NodePath('selectedOutlineGeom')
                self.model.find('**/selected').copyTo(selectedOutlineGeom)
                selectedOutlineGeom.setScale(0.9)
                piece = RepairGridPiece(name = 'piece%i' % (xpos * GRID_SIZE + ypos), parent = self.gridParent, allWoodSquaresGeom = allWoodSquaresGeom, selectedOutlineGeom = selectedOutlineGeom, scale = (0.9, 0.9, 0.9), pos = (-0.22 + xpos * SPACING, 0.0, -0.0299 + ypos * SPACING), command = self.onPiecePressed, location = [
                    xpos,
                    ypos], clickSound = None, pressEffect = 0, geom = tempGeom, relief = None)
                col.append(piece)

            self.grid.append(col)

        self.createGoalPieces()

    def reset(self):
        RepairMincroGame.reset(self)
        self.randomizeBoard()
        tutorialIndex = 0
        self.linesComplete = 0
        self.lastLineCompleteTime = globalClock.getRealTime()
        if len(self.currentGridDimensionAndLineCount[1]) > 1:
            tutorialIndex = 1

        self.repairGame.gui.setTutorial(self.name, tutorialIndex)
        self.repairGame.gui.setTitle(self.name)

    def destroy(self):
        RepairMincroGame.destroy(self)

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        difIndex = int(math.floor(percent * (len(self.config.difficultyLevels) - 1)))
        self.currentGridDimensionAndLineCount = self.config.difficultyLevels[difIndex]
    
    def getPieces(self):
        pieces = []
        
        for x in xrange(GRID_SIZE):
            for y in xrange(GRID_SIZE):
                pieces.append(self.grid[x][y])
        
        return pieces

    def randomizeBoard(self):
        for piece in self.getPieces():
            piece.request('Blank')
            piece.unstash()
            piece.setEnabled(False)

        self.removePieces(self.currentGridDimensionAndLineCount[0])
        self.createGoalPieces()

    def getAvailableSpots(self):
        availableSpots = []
        
        for x in xrange(GRID_SIZE):
            for y in xrange(GRID_SIZE):
                if self.grid[x][y].isBlankPiece():
                    availableSpots.append((x, y))
        
        return availableSpots                
    
    def createGoalPieces(self):
        availableSpots = self.getAvailableSpots()
        random.shuffle(availableSpots)

        for pieceType in self.currentGridDimensionAndLineCount[1]:
            goalCount = GRID_SIZE
            if GOAL_VERT_1 in self.currentGridDimensionAndLineCount[1]:
                goalCount -= 1

            for i in xrange(goalCount):
                x, y = availableSpots.pop()
                self.grid[x][y].request('Goal', pieceType)

        if GOAL_VERT_1 in self.currentGridDimensionAndLineCount[1]:
            x, y = availableSpots.pop()
            self.grid[x][y].request('Goal', GOAL_CROSS_1_1)
    
    def removePieces(self, number):
        availableSpots = self.getAvailableSpots()
        
        for i in xrange(number):
            x, y = availableSpots.pop()
            self.grid[x][y].request('Empty')

    def onPiecePressed(self, xpos, ypos, dir = None):
        if self.getCurrentOrNextState() in [
            'Game']:
            dirx = dir[0]
            diry = dir[1]
            if xpos + dirx >= GRID_SIZE or xpos + dirx < 0:
                return False

            if ypos + diry >= GRID_SIZE or ypos + diry < 0:
                return False

            if self.grid[xpos + dirx][ypos + diry].isEmptyPiece():
                self.moveSound.play()
                self.swapPieces(xpos, ypos, xpos + dirx, ypos + diry)
                self.checkWin()
                return True

        return False

    def swapPieces(self, pieceAxpos, pieceAypos, pieceBxpos, pieceBypos):
        pieceA = self.grid[pieceAxpos][pieceAypos]
        pieceB = self.grid[pieceBxpos][pieceBypos]
        posA = pieceA.getPos()
        posB = pieceB.getPos()
        locationA = pieceA.location[:]
        pieceA.setGridLocation(pieceB.location[:], posB)
        pieceB.setGridLocation(locationA, posA)
        self.grid[pieceAxpos][pieceAypos] = pieceB
        self.grid[pieceBxpos][pieceBypos] = pieceA

    def checkWin(self):
        percentages = []
        solved = []

        for type in self.currentGridDimensionAndLineCount[1]:
            solved.append(False)
            percentages.append(0.0)

            if type == GOAL_HORIZ_1 or type == GOAL_HORIZ_2:
                bestGoalCount = 0

                for y in xrange(GRID_SIZE):
                    goalCount = 0

                    for x in xrange(GRID_SIZE):
                        spot = self.grid[x][y]

                        if spot.pieceType in (type, GOAL_CROSS_1_1):
                            goalCount += 1

                    if goalCount > bestGoalCount:
                        bestGoalCount = goalCount

                percent = int(((bestGoalCount - 1.0) / (GRID_SIZE - 1)) * 100)
                percentages[-1] = percent

                if bestGoalCount == GRID_SIZE:
                    solved[-1] = True

            if type == GOAL_VERT_1:
                bestGoalCount = 0

                for x in xrange(GRID_SIZE):
                    goalCount = 0

                    for y in xrange(GRID_SIZE):
                        spot = self.grid[x][y]

                        if spot.pieceType in (type, GOAL_CROSS_1_1):
                            goalCount += 1
                            continue

                    if goalCount > bestGoalCount:
                        bestGoalCount = goalCount

                percent = int(((bestGoalCount - 1.0) / (GRID_SIZE - 1.0)) * 100)
                percentages[-1] = percent

                if bestGoalCount == GRID_SIZE:
                    solved[-1] = True

        linesComplete = len([line for line in solved if line])
        rating = 0

        if linesComplete > self.linesComplete:
            self.lineCompleteSound.play()
            completeTime = globalClock.getRealTime()
            timeToBrace = self.lastLineCompleteTime - completeTime
            rating = math.ceil(max(0, self.config.repairTimeframe - timeToBrace) / self.config.repairTimeframe / 5.0)
            self.lastLineCompleteTime = completeTime

        self.linesComplete = linesComplete
        percent = sum(percentages) / len(percentages)

        self.repairGame.d_reportMincroGameProgress(percent, rating)

        if linesComplete == len(solved):
            self.request('Outro')

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        for piece in self.getPieces():
            if not piece.isEmptyPiece():
                piece.setEnabled(True)
                piece.request('Active')

    def exitGame(self):
        RepairMincroGame.exitGame(self)
        for piece in self.getPieces():
            piece.setEnabled(False)

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)

    def exitOutro(self):
        RepairMincroGame.exitOutro(self)
        for piece in self.getPieces():
            piece.request('Idle')
