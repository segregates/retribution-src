from direct.gui.DirectGui import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory.InventoryGlobals import *
from pirates.inventory import InventoryUIStackItem

class InventoryUIGoldItem(InventoryUIStackItem.InventoryUIStackItem):

    def __init__(self, manager, itemTuple, imageScaleFactor = 1.0, update = False):
        InventoryUIStackItem.InventoryUIStackItem.__init__(self, manager, itemTuple, imageScaleFactor = imageScaleFactor, showMax = 0, update = False)
        self.initialiseoptions(InventoryUIGoldItem)
        gui = loader.loadModel('models/gui/toplevel_gui')
        self['image'] = gui.find('**/treasure_w_coin*')
        self['image_scale'] = 0.1 * imageScaleFactor
        self.imageScale = 3.0
        self.textScale = 1.1
        if update:
            self.accept('goldInPocketChanged', self.updateAmount)
            self.updateAmount()



    def destroy(self):
        self.ignoreAll()
        InventoryUIStackItem.InventoryUIStackItem.destroy(self)


    def getName(self):
        return PLocalizer.GoldName


    def updateAmount(self, caller = None):
        self.amount = localAvatar.getGoldInPocket()
        self.updateAmountText()
