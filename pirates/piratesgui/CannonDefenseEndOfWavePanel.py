from panda3d.core import TextNode
# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pirates.piratesgui.CannonDefenseScorePanelBase import CannonDefenseScorePanelBase
from pirates.piratesgui.CannonDefenseScorePanelBase import RoundCompleteFlags
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class CannonDefenseEndOfWavePanel(CannonDefenseScorePanelBase):

    def __init__(self, waveNumber, roundComplete, panelNumber, numOfPanels, **kw):
        CannonDefenseScorePanelBase.__init__(self, panelNumber, numOfPanels)
        self.lblCountDown = None
        self.lblTreasureStolen = None
        self.lblTreasureLeft = None
        self.roundComplete = roundComplete
        self.waveNumber = waveNumber
        self._createPanel()


    def _createPanel(self):
        startX = 0.77
        widthX = 0.390
        self._createHeader(self, self.waveNumber, self.roundComplete)
        self._createTreasureLabels(self, 1.215)
        self._createWaveResultsLabel(self, 0.96)
        self._createPlayerNames(self, self.playerLbls, startX, 0.96, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShipsSunkWave'], self.shipsSunkTotalslbl, startX, 0.815, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['DamageDealtWave'], self.damageTotalslbl, startX, 0.71, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['AccuracyWave'], self.accuracyTotalslbl, startX, 0.62, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShotsFiredWave'], self.shotsFiredTotalslbl, startX, 0.52, widthX)
        self._createGoldAwardedLabel(self, 0.22)
        self._createFooter(self)


    def _createHeader(self, myParent, waveNumber, roundComplete):
        textColor = PiratesGuiGlobals.TextFG1
        if roundComplete == RoundCompleteFlags.GAME_DEFEAT:
            waveCompleteTxt = PLocalizer.CannonDefense['GameOver']
            textColor = PiratesGuiGlobals.TextOV6
        else:
            waveCompleteTxt = PLocalizer.CannonDefense['WaveComplete'] % waveNumber
            if roundComplete == RoundCompleteFlags.GAME_VICTORY:
                textColor = PiratesGuiGlobals.TextFG25

        headingTxtScale = PiratesGuiGlobals.TextScaleLarge * 4
        DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = waveCompleteTxt, text_scale = headingTxtScale, text_align = TextNode.ACenter, text_fg = textColor, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 0, pos = (1.2, 0, 1.35))


    def _createFooter(self, myParent):
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.5
        if self.roundComplete == RoundCompleteFlags.WAVE_COMPLETE:
            nextWaveTxt = PLocalizer.CannonDefense['NextWave'] % '?'
            self.lblCountDown = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = nextWaveTxt, text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 1, pos = (2.25, 0, -0.0598))
            self.lblCountDown.hide()
        else:
            DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '%s/%s' % (self.panelNumber, self.numOfPanels), text_scale = txtScale, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 0, pos = (2.10, 0, 0.0299))
            self.nextButton = GuiButton(parent = self, pos = (2.10, 0, -0.050000), text = PLocalizer.CannonDefense['Next'])


    def _createTreasureLabels(self, myParent, startY):
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.45
        self.lblTreasureStolen = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (0.299, 0, startY))
        self.lblTreasureLeft = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 1, pos = (2.10, 0, startY))


    def _createWaveResultsLabel(self, myParent, startY):
        DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = PLocalizer.CannonDefense['WaveResults'], text_scale = PiratesGuiGlobals.TextScaleLarge * 1.5, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (0.22, 0, startY))


    def _createGoldAwardedLabel(self, myParent, startY):
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.5
        self.lblGoldAwarded = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (2.18, 0, startY - 0.074))
        self.lblTreasureEarned = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (2.18, 0, startY))
        self.lblTreasureEarned.hide()


    def setGoldAwarded(self, gold, goldBonus = 0):
        if goldBonus:
            self.lblGoldAwarded['text'] = PLocalizer.CannonDefense['PayShareBonus'] % (str(gold), str(goldBonus))
        else:
            self.lblGoldAwarded['text'] = PLocalizer.CannonDefense['PayShare'] % str(gold)


    def setTreasureAwarded(self, amount):
        if amount == 0:
            return None

        self.lblTreasureEarned['text'] = PLocalizer.CannonDefense['TreasureEarned'] % amount
        self.lblTreasureEarned.show()


    def updateCountDown(self, timeLeft):
        self.lblCountDown['text'] = PLocalizer.CannonDefense['NextWave'] % timeLeft
        if self.lblCountDown.isHidden():
            self.lblCountDown.show()



    def setTreasureStats(self, treasureStolen, treasureRemaining):
        self.lblTreasureStolen['text'] = '%s %s %s' % (PLocalizer.CannonDefense['TreasureStolen'], treasureStolen, PLocalizer.CannonDefense['Treasure'])
        self.lblTreasureLeft['text'] = '%s %s %s' % (PLocalizer.CannonDefense['TreasureRemaining'], treasureRemaining, PLocalizer.CannonDefense['Treasure'])
