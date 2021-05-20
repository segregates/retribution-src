from pirates.uberdog.UberDogGlobals import InventoryType
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.ai.MagicWordGlobal import *
import CodeRedemptionGlobals

class CodeRedemptionAI(DistributedObjectAI):
    notify = directNotify.newCategory('CodeRedemptionAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    def checkAlreadyRedeemed(self, av, code):
        used = av.getRedeemedCodes()
        if code in used or config.GetBool('reject-all-redeem-codes', False):
            return True
        return False

    def attemptToRedeemCode(self, code, avId):
        reward = None

        def buildResponse(status, type=-1, uid=0):
            return (status, type, uid)

        holidayList = []
        if config.GetBool('want-holiday-codes', True):
            holidayList = self.air.newsManager.getRawHolidayIdList()

        try:
            reward = CodeRedemptionGlobals.getAwardFromCode(code, holidayList)
        except:
            self.notify.warning("Unexpected error has occured while retreiving award info for code '%s'. Most likely bad award formatting." % code)
            return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

        try:
            if reward is not None:

                av = self.air.doId2do.get(avId)
                if not av:
                    self.notify.warning("Failed to locate Avatar for AvatarId: %s" % avId)
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                if self.checkAlreadyRedeemed(av, code):
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                invType = reward[0]
                invItem = reward[1]
                rewardType = invItem[0] or -1

                itemId = 0
                if rewardType != InventoryType.ItemTypeMoney: 
                    itemId = invItem[1] or 0

                amount = reward[3] or 0

                inv = av.getInventory()
                if not inv:
                    self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                if invType == CodeRedemptionGlobals.NORMAL_INVENTORY:
                    if rewardType == InventoryType.ItemTypeMoney:
                        av.giveGold(amount)
                    else:
                        location = inv.findAvailableLocation(rewardType, itemId=itemId, count=amount, equippable=True)
                        if location != -1:
                            inv.addLocatable(itemId, location, amount, inventoryType=rewardType)
                        else:
                            return buildResponse(CodeRedemptionGlobals.ERROR_ID_OVERFLOW)   
                elif invType == CodeRedemptionGlobals.CLOTHING:
                    femaleReward = invItem[2]
                    isFemale = (av.getGender() == 'f')
                    if femaleReward and isFemale:
                        rewardType = femaleReward

                    location = inv.findAvailableLocation(InventoryType.ItemTypeClothing, itemId=itemId, count=amount, equippable=True)
                    if location != -1:
                        inv.addLocatable(itemId, location, amount, inventoryType=InventoryType.ItemTypeClothing)
                    else:
                        return buildResponse(CodeRedemptionGlobals.ERROR_ID_OVERFLOW)
                elif invType == CodeRedemptionGlobals.JEWELRY:
                    location = inv.findAvailableLocation(InventoryType.ItemTypeJewelry, itemId=itemId, count=amount, equippable=True)
                    if location != -1:
                        inv.addLocatable(itemId, location, amount, inventoryType=InventoryType.ItemTypeJewelry)
                    else:
                        return buildResponse(CodeRedemptionGlobals.ERROR_ID_OVERFLOW)               
                elif invType == CodeRedemptionGlobals.TATTOO:
                    location = inv.findAvailableLocation(InventoryType.ItemTypeTattoo, itemId=itemId, count=amount, equippable=True)
                    if location != -1:
                        inv.addLocatable(itemId, location, amount, inventoryType=InventoryType.ItemTypeTattoo)
                    else:
                        return buildResponse(CodeRedemptionGlobals.ERROR_ID_OVERFLOW)   
                elif invType == CodeRedemptionGlobals.HAIR:
                    self.notify.warning("Unable to process redemption code (%s). Type Hair is not supported yet" % code)
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD) #TODO add hair redemption
                else:
                    self.notify.warning("Unable to process redemption code for inventory type: %s" % invType)
                    return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

                av.addRedeemedCode(code)
                return buildResponse(CodeRedemptionGlobals.ERROR_ID_GOOD, rewardType, itemId) 
            else:
                self.notify.warning("No reward. Code: %s" % code)
                return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)
        except Exception, e:
            self.notify.warning("Unexpected error has occured while processing redemption code '%s' " % code)
            self.notify.warning(str(e))
            return buildResponse(CodeRedemptionGlobals.ERROR_ID_BAD)

    def sendCodeForRedemption(self, code, userName, accountId):
        code = code.lower()
        self.notify.debug("Attempting to redeem code: %s" % code)
        response = (CodeRedemptionGlobals.ERROR_ID_BAD, -1, 0)
        avId = self.air.getAvatarIdFromSender()
        if avId:
            response = self.attemptToRedeemCode(code, avId)
        else:
            self.notify.warning("Failed to find avatarId for code requester. requester username: %s" % userName)
        self.notify.debug("Sending code redemption response: %s" % str(response))
        try:
            self.sendUpdateToAvatarId(avId, 'notifyClientCodeRedeemStatus', [response[0], response[1], response[2]])
        except Exception, e:
            self.notify.warning("Unexpected error has occured while processing redemption code")
            self.notify.warning(str(e))



