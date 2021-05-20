from panda3d.core import Connection, NodePath, TextNode, Texture, TextureAttrib, TextureStage
# File: P (Python 2.4)

from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from PotionRecipeData import PotionColorSets
from pirates.battle.WeaponConstants import *
import random
import PotionGlobals
LowLevelRecipes = [
    C_PISTOL_DAMAGE_LVL1,
    C_CUTLASS_DAMAGE_LVL1,
    C_DOLL_DAMAGE_LVL1,
    C_HASTEN_LVL1,
    C_CANNON_DAMAGE_LVL1]

class PotionBoardPiece(NodePath):
    colorTable = [
        (1.0, 0, 0, 1.0),
        (0, 0, 1.0, 1.0),
        (0, 1.0, 0, 1.0),
        (0.800000, 0.598, 0, 1.0),
        (0.299, 0.299, 0.299, 1.0),
        (0.800000, 0, 1.0, 1.0)]
    colorTableIncomplete = [
        (0.5, 0.25, 0.25, 1.0),
        (0.25, 0.5, 0.25, 1.0),
        (0.25, 0.25, 0.5, 1.0),
        (0.598, 0.4, 0.200, 1.0),
        (0.800000, 0.800000, 0.800000, 1.0),
        (0.598, 0.5, 0.75, 1.0)]
    secretColor = (0.5, 0.5, 0.5, 1.0)

    def __init__(self, parentFrame, color = 0, level = 0, colorSet = 0, recipe = None):
        self.Xpos = 0
        self.Ypos = 0
        self.column = 0
        self.row = 0
        self.completed = True
        if level == 0:
            if recipe.potionID in LowLevelRecipes:
                self.colorIndex = random.choice(PotionColorSets[0])
            else:
                self.colorIndex = random.choice(PotionColorSets[colorSet])
            self.level = 1
        else:
            self.colorIndex = color
            self.level = level

        self.moveFast = False
        self.moveSlow = False
        self.moveVerySlow = False
        self.connections = []
        self.potentialConnections = []
        self.pendingConnections = []
        self.connectionsRemoved = 0
        NodePath.__init__(self, 'peice')
        self.reparentTo(parentFrame.background)
        self.parentFrame = parentFrame
        self.enabled = True
        self.pendingMatch = False
        self.nameLabel = None
        self.nameCheck = None
        self.setupScene()
        self.hiddenColor = 0
        self.hiddenLevel = 0


    def __cmp__(self, other):
        myConnections = len(self.connections)
        thierConnections = len(other.connections)
        if myConnections != thierConnections:
            return cmp(thierConnections, myConnections)
        elif self.Ypos == other.Ypos:
            return cmp(self.Xpos, other.Xpos)
        else:
            return cmp(self.Ypos, other.Ypos)


    def showName(self, show = True):
        if self.colorIndex >= 0 and self.colorIndex < 6 and self.level > 0 and self.level <= 6:
            nameText = PLocalizer.PotionIngredients[self.colorIndex][self.level - 1]
        else:
            self.completed = False
            nameText = PLocalizer.PotionGui['UnknownIngredient']
        topGui = loader.loadModel('models/gui/toplevel_gui')
        self.nameCheck = topGui.find('**/generic_check')
        textureCard = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
        self.checkBox = textureCard.find('**/pir_t_gui_pot_checkbox')
        self.nameLabel = DirectLabel(relief = None, text = nameText, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ALeft, text_fg = PotionGlobals.TextColor, text_wordwrap = 37, pos = (0.22, 0, -0.0400), textMayChange = 0)
        self.nameLabel.reparentTo(self)
        self.nameCheck.setPos(0.16, 0, -0.0299)
        self.nameCheck.setScale(0.75, 0.75, 0.75)
        self.nameCheck.reparentTo(self.background)
        self.checkBox.setPos(0.149, 0, -0.070)
        self.checkBox.setScale(0.200, 0.200, 0.200)
        self.checkBox.reparentTo(self.background)
        if not self.completed:
            self.nameCheck.stash()

        topGui.remove_node()
        textureCard.remove_node()


    def setHiddenInfo(self, color, level):
        self.hiddenColor = color
        self.hiddenLevel = level


    def findConnections(self, gameBoard):
        self.connections = []
        self.potentialConnections = []
        self.connectionsRemoved = 0
        self.testConnection(gameBoard, self.column, self.row - 1)
        self.testConnection(gameBoard, self.column, self.row + 1)
        self.testConnection(gameBoard, self.column + 1, self.row)
        self.testConnection(gameBoard, self.column - 1, self.row)
        if self.column % 2 == 0:
            self.testConnection(gameBoard, self.column - 1, self.row + 1)
            self.testConnection(gameBoard, self.column + 1, self.row + 1)
        else:
            self.testConnection(gameBoard, self.column - 1, self.row - 1)
            self.testConnection(gameBoard, self.column + 1, self.row - 1)


    def previewConnections(self, gameBoard):
        self.pendingConnections = []
        self.testPreviewConnection(gameBoard, self.column, self.row - 1)
        self.testPreviewConnection(gameBoard, self.column, self.row + 1)
        self.testPreviewConnection(gameBoard, self.column + 1, self.row)
        self.testPreviewConnection(gameBoard, self.column - 1, self.row)
        if self.column % 2 == 0:
            self.testPreviewConnection(gameBoard, self.column - 1, self.row + 1)
            self.testPreviewConnection(gameBoard, self.column + 1, self.row + 1)
        else:
            self.testPreviewConnection(gameBoard, self.column - 1, self.row - 1)
            self.testPreviewConnection(gameBoard, self.column + 1, self.row - 1)


    def testConnection(self, gameBoard, col, row):
        intcol = int(col)
        introw = int(row)
        if intcol >= 0 and intcol < gameBoard.numColumns and introw >= 0 and introw < gameBoard.numRows:
            if gameBoard.boardPieces[intcol][introw] is not None:
                if gameBoard.boardPieces[intcol][introw].colorIndex == self.colorIndex:
                    if gameBoard.boardPieces[intcol][introw].level == self.level:
                        self.connections.append(gameBoard.boardPieces[intcol][introw])
                    else:
                        self.potentialConnections.append(gameBoard.boardPieces[intcol][introw])





    def testPreviewConnection(self, gameBoard, col, row):
        intcol = int(col)
        introw = int(row)
        if intcol >= 0 and intcol < gameBoard.numColumns and introw >= 0 and introw < gameBoard.numRows:
            if gameBoard.boardPieces[intcol][introw] is not None:
                if gameBoard.boardPieces[intcol][introw].colorIndex == self.colorIndex:
                    if self not in gameBoard.removeList and gameBoard.boardPieces[intcol][introw] not in gameBoard.removeList:
                        ownLevel = self.level
                        if self in gameBoard.upgradeList:
                            self.upgrade()

                        otherLevel = gameBoard.boardPieces[intcol][introw].level
                        if gameBoard.boardPieces[intcol][introw] in gameBoard.upgradeList:
                            otherLevel += 1

                        if ownLevel == otherLevel:
                            self.pendingConnections.append(gameBoard.boardPieces[intcol][introw])







    def updateDisplay(self):
        if self.colorIndex >= 0 and self.colorIndex <= 5 and self.level > 0 and self.level <= 6:
            if self.colorIndex == 0:
                texName = 'pir_t_gui_pot_tok_red_%i' % self.level
            elif self.colorIndex == 1:
                texName = 'pir_t_gui_pot_tok_blu_%i' % self.level
            elif self.colorIndex == 2:
                texName = 'pir_t_gui_pot_tok_gre_%i' % self.level
            elif self.colorIndex == 3:
                texName = 'pir_t_gui_pot_tok_ora_%i' % self.level
            elif self.colorIndex == 4:
                texName = 'pir_t_gui_pot_tok_bla_%i' % self.level
            elif self.colorIndex == 5:
                texName = 'pir_t_gui_pot_tok_pur_%i' % self.level

            if not self.completed:
                texName += '_empty'
                if self.nameCheck is not None:
                    self.nameCheck.stash()

            elif self.nameCheck is not None:
                self.nameCheck.unstash()

            textureCard = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
            self.bgTexture = textureCard.findTexture(texName)
            geom = self.bgModel.find('**/+GeomNode').node()
            renderState = geom.getGeomState(0)
            texAttrib = renderState.getAttrib(TextureAttrib.getClassType())
            texAttrib = texAttrib.addOnStage(TextureStage.getDefault(), self.bgTexture)
            renderState = renderState.addAttrib(texAttrib)
            geom.setGeomState(0, renderState)
            textureCard.remove_node()
        else:
            textureCard = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
            self.bgTexture = textureCard.findTexture('pir_t_gui_pot_tok_red_1_empty')
            geom = self.bgModel.find('**/+GeomNode').node()
            renderState = geom.getGeomState(0)
            texAttrib = renderState.getAttrib(TextureAttrib.getClassType())
            texAttrib = texAttrib.addOnStage(TextureStage.getDefault(), self.bgTexture)
            renderState = renderState.addAttrib(texAttrib)
            geom.setGeomState(0, renderState)
            textureCard.remove_node()


    def upgrade(self):
        self.level += 1
        self.updateDisplay()


    def setCompleted(self, completed):
        self.completed = completed
        self.updateDisplay()


    def setColor(self, color, level):
        self.colorIndex = color
        self.level = level
        self.updateDisplay()


    def moveLeft(self):
        self.moveFast = True
        self.column -= 1
        return self.moveToBoard(self.column, self.row)


    def moveRight(self):
        self.moveFast = True
        self.column += 1
        return self.moveToBoard(self.column, self.row)


    def moveUp(self):
        self.moveFast = True
        self.row += 1
        return self.moveToBoard(self.column, self.row)


    def moveDown(self):
        self.moveFast = True
        self.row -= 1
        return self.moveToBoard(self.column, self.row)


    def setupScene(self):
        base.disableMouse()
        self._initGUI()


    def _initGUI(self):
        self.background = NodePath('background')
        self.background.reparentTo(self)
        self.bgModel = loader.loadModel('models/minigames/pir_m_gui_pot_tok_blank')
        self.bgModel.flattenStrong()
        self.bgModel.setScale(0.35198, 0.35198, 0.35198)
        self.bgModel.reparentTo(self.background)
        self.background.reparentTo(self)
        self.bgModel.setTransparency(True)
        self.background.setColor(1, 1, 1, 1)
        self.background.setDepthWrite(True)
        self.background.setDepthTest(True)
        self.updateDisplay()


    def setPiecePosition(self, destX, destY):
        self.setPos(destX, self.getY(), destY)
        self.Xpos = destX
        self.Ypos = destY


    def setBoardPos(self, destX, destY):
        self.column = destX
        self.row = destY
        if self.column % 2 == 0:
            self.setPiecePosition(self.column * 0.13919, self.row * 0.16159 + 0.0807)
        else:
            self.setPiecePosition(self.column * 0.13919, self.row * 0.16159)


    def moveTo(self, destX, destY):
        prevPosX = self.Xpos
        prevPosY = self.Ypos
        self.Xpos = destX
        self.Ypos = destY
        if self.moveVerySlow:
            speed = 0.598
        elif self.moveSlow:
            speed = 0.4
        elif self.moveFast:
            speed = 0.149
        else:
            speed = 0.299
        self.moveFast = False
        self.moveSlow = False
        self.moveVerySlow = False
        if self.is_empty() == False:
            return LerpPosInterval(self, duration = speed, pos = (self.Xpos, self.getY(), self.Ypos), blendType = 'easeIn')


    def moveToBoardSlow(self, destX, destY):
        self.moveSlow = True
        return self.moveToBoard(destX, destY)


    def moveToBoardVerySlow(self, destX, destY):
        self.moveVerySlow = True
        return self.moveToBoard(destX, destY)


    def moveToBoard(self, destX, destY):
        self.column = destX
        self.row = destY
        if self.column % 2 == 0:
            return self.moveTo(self.column * 0.13919, self.row * 0.16159 + 0.0807)
        else:
            return self.moveTo(self.column * 0.13919, self.row * 0.16159)


    def destroy(self):
        self.remove_node()

    def setY(self, *args):
        if self:
            NodePath.setY(self, *args)

        else:
            info = (self, self.level, self.colorIndex, args)
            print ':PotionBoardPiece(warning): called setY on removed piece:', info
