from panda3d.core import NodePath, Point3, VBase4

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class AmmoPanelMessageManager:

    def __init__(self):
        self.levelUpCannonDefenseIval = None
        self.noAmmoSlotIval = None
        self.notEnoughBankNotesIval = None


    def createDefenseCannonSkillsText(self):
        if self.levelUpCannonDefenseIval:
            return None

        self.levelUpCannonDefenseText = NodePath('levelUpCannonDefenseText')
        self.levelUpCannonDefenseLabel = DirectLabel(parent = self.levelUpCannonDefenseText, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = (1.0, 1.0, 1.0, 1.0), scale = 0.074, pos = (0, 0, -0.25))
        self.levelUpCannonDefenseIval = Sequence(Func(self.levelUpCannonDefenseText.reparentTo, aspect2d), Parallel(LerpPosInterval(self.levelUpCannonDefenseText, 5, pos = Point3(0, 0, 0.299), startPos = Point3(0, 0, -0.299)), Sequence(LerpColorScaleInterval(self.levelUpCannonDefenseText, 0.5, colorScale = VBase4(1, 1, 1, 1), startColorScale = VBase4(1, 1, 1, 0)), Wait(4), LerpColorScaleInterval(self.levelUpCannonDefenseText, 0.5, colorScale = VBase4(1, 1, 1, 0), startColorScale = VBase4(1, 1, 1, 1)))), Func(self.levelUpCannonDefenseText.detachNode))


    def createNoAmmoSlotText(self):
        if self.noAmmoSlotIval:
            return None

        self.noAmmoSlotText = NodePath('noAmmoSlotText')
        self.noAmmoSlotLabel = DirectLabel(parent = self.noAmmoSlotText, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = (0.100, 0.696, 0.100, 1), scale = 0.074, pos = (0, 0, -0.25))
        self.noAmmoSlotIval = Sequence(Func(self.noAmmoSlotText.reparentTo, aspect2d), Parallel(LerpPosInterval(self.noAmmoSlotText, 5, pos = Point3(0, 0, 0.299), startPos = Point3(0, 0, -0.299)), Sequence(LerpColorScaleInterval(self.noAmmoSlotText, 0.5, colorScale = VBase4(1, 1, 1, 1), startColorScale = VBase4(1, 1, 1, 0)), Wait(1), LerpColorScaleInterval(self.noAmmoSlotText, 0.5, colorScale = VBase4(1, 1, 1, 0), startColorScale = VBase4(1, 1, 1, 1)))), Func(self.noAmmoSlotText.detachNode))


    def createNotEnoughBankNotesText(self):
        if self.notEnoughBankNotesIval:
            return None

        self.notEnoughBankNotesText = NodePath('notEnoughBankNotesText')
        self.notEnoughBankNotesLabel = DirectLabel(parent = self.notEnoughBankNotesText, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = (0.100, 0.696, 0.100, 1), scale = 0.074, pos = (0, 0, -0.25))
        self.notEnoughBankNotesIval = Sequence(Func(self.notEnoughBankNotesText.reparentTo, aspect2d), Parallel(LerpPosInterval(self.notEnoughBankNotesText, 5, pos = Point3(0, 0, 0.299), startPos = Point3(0, 0, -0.299)), Sequence(LerpColorScaleInterval(self.notEnoughBankNotesText, 0.5, colorScale = VBase4(1, 1, 1, 1), startColorScale = VBase4(1, 1, 1, 0)), Wait(1), LerpColorScaleInterval(self.notEnoughBankNotesText, 0.5, colorScale = VBase4(1, 1, 1, 0), startColorScale = VBase4(1, 1, 1, 1)))), Func(self.notEnoughBankNotesText.detachNode))


    def showDefenseCannonSkillsUnlocked(self, message):
        self.createDefenseCannonSkillsText()
        self.levelUpCannonDefenseLabel['text'] = message
        self.levelUpCannonDefenseLabel['text_fg'] = (1.0, 1.0, 1.0, 1.0)
        self.levelUpCannonDefenseIval.pause()
        self.levelUpCannonDefenseIval.start()


    def showNoAmmoSlot(self):
        self.createNoAmmoSlotText()
        self.noAmmoSlotLabel['text'] = PLocalizer.NoAmmoSlot
        self.noAmmoSlotLabel['text_fg'] = (1.0, 0.200, 0.200, 1)
        self.noAmmoSlotIval.pause()
        self.noAmmoSlotIval.start()


    def showNotEnoughBankNotes(self):
        self.createNotEnoughBankNotesText()
        self.notEnoughBankNotesLabel['text'] = PLocalizer.NotEnoughBankNotes
        self.notEnoughBankNotesLabel['text_fg'] = (1.0, 0.200, 0.200, 1)
        self.notEnoughBankNotesIval.pause()
        self.notEnoughBankNotesIval.start()


    def deleteLevelUpCannonDefenseText(self):
        if not self.levelUpCannonDefenseIval:
            return None

        self.levelUpCannonDefenseIval.pause()
        self.levelUpCannonDefenseIval = None
        self.levelUpCannonDefenseLabel.destroy()
        self.levelUpCannonDefenseText.remove_node()


    def deleteNoAmmoSlotText(self):
        if not self.noAmmoSlotIval:
            return None

        self.noAmmoSlotIval.pause()
        self.noAmmoSlotIval = None
        self.noAmmoSlotLabel.destroy()
        self.noAmmoSlotText.remove_node()


    def deleteNotEnoughBankNotesText(self):
        if not self.notEnoughBankNotesIval:
            return None

        self.notEnoughBankNotesIval.pause()
        self.notEnoughBankNotesIval = None
        self.notEnoughBankNotesLabel.destroy()
        self.notEnoughBankNotesText.remove_node()


    def destroy(self):
        self.deleteLevelUpCannonDefenseText()
        self.deleteNoAmmoSlotText()
        self.deleteNotEnoughBankNotesText()
