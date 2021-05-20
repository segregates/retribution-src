from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.economy import EconomyGlobals
from pirates.inventory import ItemGlobals
from pirates.audio import SoundGlobals
from pirates.makeapirate import BarberGlobals
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.uberdog.UberDogGlobals import *
from pirates.ai import HolidayGlobals
from otp.uberdog.RejectCode import RejectCode

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
    
    
    def requestMusic(self, music):
        if not SoundGlobals.isSongId(music):
            return

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        
        if not av:
            return
        
        requiredGold = EconomyGlobals.PLAY_MUSIC_COST
        if requiredGold > av.getGoldInPocket():
            return
        
        av.takeGold(requiredGold)
        self.sendUpdate('playMusic', [music])

    def requestPurchaseRepair(self, shipId):
        pass

    def requestPurchaseOverhaul(self, todo0):
        pass

    def requestSellShip(self, shipId):
        pass

    def requestMakeShipSale(self, buying, selling, names):
        self.notify.info("requestMakeShipSale: ({0}) ({1}) ({2})".format(buying, selling, names))

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        def sendResponse(resultCode, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode]) 

        if not len(buying) > 0:
            self.notify.warning("Unable to process ship sale. Received malformed 'requestMakeShipSale' packet")
            sendResponse(RejectCode.TIMEOUT)
            return  

        itemData = buying[0]
        if not itemData:
            self.notify.warning("Unable to process ship sale. Invalid itemData received")
            sendResponse(RejectCode.TIMEOUT)
            return

        shipId = itemData[0]
        requiredGold = EconomyGlobals.getItemCost(shipId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for shipId: %s" % shipId)
            sendResponse(RejectCode.TIMEOUT)
            return   

        requiredGold = requiredGold
        if requiredGold > av.getGoldInPocket():
            sendResponse(0)
            return         

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            sendResponse(RejectCode.TIMEOUT)
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.NewShipToken, itemId=shipId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(shipId, availableSlot, 1)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2
        sendResponse(resultCode) 

    def requestSellItem(self, todo0, todo1, todo2, todo3):
        self.notify.info("requestSellItem: ({0}) ({1}) ({2}) ({3})".format(todo0, todo1, todo2, todo3))

    def requestWeapon(self, buying, selling):

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        def sendResponse(resultCode, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode]) 

        if not len(buying) > 0:
            self.notify.warning("Unable to process weapon sale. Received malformed 'requestWeapon' packet")
            sendResponse(RejectCode.TIMEOUT)
            return

        itemId, amount = buying[0]
        amount = max(1, amount)

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for itemId: %s" % itemId)
            sendResponse(RejectCode.TIMEOUT)
            return

        requiredGold = requiredGold * amount
        if requiredGold > av.getGoldInPocket():
            sendResponse(0)
            return

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            sendResponse(RejectCode.TIMEOUT)
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeWeapon, itemId=itemId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, amount)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2
        sendResponse(resultCode)

    def requestAccessories(self, buying, selling):

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        def sendResponse(resultCode, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode]) 

        if not len(buying) > 0:
            self.notify.warning("Unable to process accessories sale. Received malformed 'requestAccessories' packet")
            sendResponse(RejectCode.TIMEOUT)
            return

        itemId, colorId, todo0, todo1 = buying[0] #TODO: figure out what todo0 and todo1 are

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for itemId: %s" % itemId)
            sendResponse(RejectCode.TIMEOUT)
            return

        if self.air.newsManager.isHolidayRunning(HolidayGlobals.HALFOFFCUSTOMIZATION) and requiredGold > 0:
            requiredGold = requiredGold / 2

        if requiredGold > av.getGoldInPocket():
            sendResponse(0)
            return

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            sendResponse(RejectCode.TIMEOUT)
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeClothing, itemId=itemId, count=1, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, 1, inventoryType=InventoryType.ItemTypeClothing, colorId=colorId)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2

        sendResponse(resultCode)

    def requestJewelry(self, buying, selling):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        def sendResponse(resultCode, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode])

        if not len(buying) > 0:
            self.notify.warning("Unable to process jewelry sale. Received malformed 'requestJewelry' packet")
            sendResponse(RejectCode.TIMEOUT)
            return

        itemId, amount = buying[0]
        amount = max(1, amount)

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for itemId: %s" % itemId)
            sendResponse(RejectCode.TIMEOUT)
            return

        requiredGold = requiredGold * amount
        if self.air.newsManager.isHolidayRunning(HolidayGlobals.HALFOFFCUSTOMIZATION):
            requiredGold = requiredGold / 2

        if requiredGold > av.getGoldInPocket():
            sendResponse(0)
            return

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            sendResponse(RejectCode.TIMEOUT)
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeJewelry, itemId=itemId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, amount, inventoryType=InventoryType.ItemTypeJewelry)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2

        sendResponse(resultCode)

    def requestTattoo(self, buying, selling):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if not len(buying) > 0:
            self.notify.warning("Unable to process Tattoo sale. Received malformed 'requestTattoo' packet")
            self.sendUpdateToAvatarId(avId, 'makeTattooResponse', [0, 0, False])
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        itemId, amount = buying[0]
        zone = ItemGlobals.getType(itemId)

        def sendResponse(resultCode, success, itemId=itemId, zone=zone, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeTattooResponse', [itemId, zone, success])
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode])

        requiredGold = ItemGlobals.getGoldCost(itemId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for itemId: %s" % itemId)
            sendResponse(RejectCode.TIMEOUT, False)
            return

        requiredGold = requiredGold * amount
        if self.air.newsManager.isHolidayRunning(HolidayGlobals.HALFOFFCUSTOMIZATION):
            requiredGold = requiredGold / 2

        if requiredGold > av.getGoldInPocket():
            sendResponse(0, False)
            return
        
        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            sendResponse(RejectCode.TIMEOUT, False)
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.ItemTypeTattoo, itemId=itemId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(itemId, availableSlot, amount, inventoryType=InventoryType.ItemTypeTattoo)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2

        sendResponse(resultCode, True)

    def requestBarber(self, hairId, colorId):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        def sendResponse(resultCode, success, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode])

        itemData = BarberGlobals.barber_id.get(hairId)
        if not itemData:
            self.notify.warning("Unable to locate itemData for hairId: %s" % hairId)
            sendResponse(RejectCode.TIMEOUT, False)
            return

        hairDnaId, hairType, _, _, requiredGold, _ = itemData

        if len(BarberGlobals.barberFunctions) <= hairType:
            self.notify.warning('Invalid hair type for hairId: %s' % hairId)
            sendResponse(RejectCode.TIMEOUT, False)
            return

        if not requiredGold:
            self.notify.warning("Unable to locate price for hairId: %s" % hairId)
            sendResponse(RejectCode.TIMEOUT, False)
            return

        if requiredGold > av.getGoldInPocket():
            sendResponse(0, False)
            return

        self.notify.info("requestBarber: cost(%s)" % requiredGold)
        av.takeGold(requiredGold)

        av.style.setHairColor(colorId)
        getattr(av.style, BarberGlobals.barberFunctions[hairType])(hairDnaId)
        av.d_setDNAString(av.style.makeNetString())
        av.d_doRegeneration()
        sendResponse(2, True)

    # requestAccessoriesList(uint32) airecv clsend
    # requestJewelryList(uint32) airecv clsend
    # requestTattooList(uint32) airecv clsend
    # requestAccessoryEquip(Accessory []) airecv clsend
    # requestJewelryEquip(Jewelry []) airecv clsend
    # requestTattooEquip(Tattoo []) airecv clsend
    # requestTattoo(TattooInfo [], TattooInfo []) airecv clsend

    def requestStowaway(self, locationId):
        if not locationId in EconomyGlobals.StowawayCost:
            self.notify.warning("Unknown stowaway locationId: %s" % locationId)
            return

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        requiredGold = EconomyGlobals.StowawayCost[locationId]
        if requiredGold > av.getGoldInPocket():
            return

        #av.takeGold(requiredGold)

        #tpMgr = self.air.tpMgr
        #tpMgr.initiateStowawayTeleport(locationId)
    
    # responseShipRepair(uint32) ownrecv
    # responseClothingList(uint32, uint32 [][]) ownrecv
    # responseTattooList(uint32, TattooInfo []) ownrecv
    # responseJewelryList(uint32, JewelryInfo []) ownrecv

