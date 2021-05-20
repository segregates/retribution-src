from panda3d.core import TextNode, Texture, Vec3, Vec4
from direct.gui.DirectGui import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog import UberDogGlobals
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.reputation import ReputationGlobals

class ShipItemGUI(InventoryItemGui.InventoryItemGui):
    shipImageDict = {
        ItemId.INTERCEPTOR_L1: 'Catalog_Light_Sloop',
        ItemId.INTERCEPTOR_L2: 'Catalog_Regular_Sloop',
        ItemId.INTERCEPTOR_L3: 'Catalog_War_Sloop',
        ItemId.MERCHANT_L1: 'Catalog_Light_Galleon',
        ItemId.MERCHANT_L2: 'Catalog_Regular_Galleon',
        ItemId.MERCHANT_L3: 'Catalog_War_Galleon',
        ItemId.WARSHIP_L1: 'Catalog_Light_Frigate',
        ItemId.WARSHIP_L2: 'Catalog_Regular_Frigate',
        ItemId.WARSHIP_L3: 'Catalog_War_Frigate',
        ItemId.BRIG_L1: 'Catalog_Light_Brig',
        ItemId.BRIG_L2: 'Catalog_Regular_Brig',
        ItemId.BRIG_L3: 'Catalog_War_Brig',
        ItemId.CARRACK_L1: 'Catalog_Light_Carrack',
        ItemId.CARRACK_L2: 'Catalog_Regular_Carrack',
        ItemId.CARRACK_L3: 'Catalog_War_Carrack',
        ItemId.CORVETTE_L1: 'Catalog_Light_Brig',
        ItemId.CORVETTE_L2: 'Catalog_Regular_Brig',
        ItemId.CORVETTE_L3: 'Catalog_War_Brig',
        ItemId.SHIP_OF_THE_LINE: 'Catalog_Ship_Of_Line',
        ItemId.EL_PATRONS_SHIP: 'Catalog_War_Carrack',
        ItemId.P_SKEL_PHANTOM: 'Catalog_Phantom',
        ItemId.HUNTER_TALLYHO: 'Catalog_Ship_Of_Line',
        ItemId.QUEEN_ANNES_REVENGE: 'Catalog_Queen_Anne_Revenge', }
    
    def __init__(self, data, trade = 0, buy = 0, sell = 0, use = 0, **kw):
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        InventoryItemGui.InventoryItemGui.__init__(self, data, trade, buy, sell, use, **kw)
        self.initialiseoptions(ShipItemGUI)
        repId = InventoryType.SailingRep
        self.checkLevel(repId, self.minLvl)
        self.flattenStrong()

    def getCardTexture(self, imageName, card):
        tex = None
        try:
            texCard = card.find('**/%s*' % imageName)
            tex = texCard.findAllTextures()[0]
        except:
            tex = loader.loadTexture('maps/%s.jpg' % imageName)
        return tex
    
    def createGui(self):
        (item, quantity) = self.data
        name = PLocalizer.InventoryTypeNames[item]
        self.price = EconomyGlobals.getItemCost(item)
        repId = InventoryType.SailingRep
        itemTypeName = PLocalizer.InventoryTypeNames.get(repId)
        self.itemType = itemTypeName
        if self.sell:
            self.price /= 2
        
        card = loader.loadModel('models/textureCards/shipCatalog')
        renderName = self.shipImageDict.get(item, 'Catalog_War_Brig')
        myTex = self.getCardTexture(renderName, card)
        card.removeNode()
        del card
        self['state'] = DGG.NORMAL
        self.minLvl = EconomyGlobals.getItemMinLevel(item)
        self.miscText = None
        self.picture = DirectFrame(parent = self, relief = None, state = DGG.DISABLED, image = myTex, image_scale = (0.070000000000000007, 1.0, 0.059999999999999998))
        self.picture.setPos(0.10000000000000001, 0, 0.080000000000000002)
        self.picture.setTransparency(1)
        self.nameTag = DirectLabel(parent = self, state = DGG.DISABLED, relief = None, text = name, text_scale = PiratesGuiGlobals.TextScaleMed * PLocalizer.getHeadingScale(2), text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0)
        self.nameTag.setPos(0.20000000000000001, 0, 0.10000000000000001)
        self.costText = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = self.coinImage, geom_scale = 0.12, geom_pos = Vec3(-0.01, 0, 0.01), text = str(self.price), text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, text_pos = (-0.029999999999999999, 0, 0), text_font = PiratesGlobals.getInterfaceFont())
        self.costText.setPos(0.47999999999999998, 0, 0.060000000000000001) #4

    
    def showDetails(self, event):
        pass

    
    def hideDetails(self, event):
        pass

    
    def createHelpbox(self, args = None):
        pass

    
    def checkLevel(self, repId, minLvl):
        inv = localAvatar.getInventory()
        if inv:
            repAmt = inv.getAccumulator(repId)
            if minLvl > ReputationGlobals.getLevelFromTotalReputation(repId, repAmt)[0]:
                if not self.miscText:
                    self.miscText = DirectLabel(parent = self, relief = None, text = '', text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.19, 0, 0.025)) #16
                
                if not base.config.GetBool('ignore-ship-shop-levels', True):
                    self['image_color'] = Vec4(1, 0.5, 0.25, 1)
                    self['state'] = DGG.DISABLED
                    self.miscText['text_fg'] = PiratesGuiGlobals.TextFG8
                    self.miscText['text'] = PLocalizer.LevelRequirement % minLvl