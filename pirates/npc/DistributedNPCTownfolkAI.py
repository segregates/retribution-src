from direct.directnotify import DirectNotifyGlobal
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals
from pirates.battle.DistributedBattleNPCAI import *
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import *

class DistributedNPCTownfolkAI(DistributedBattleNPCAI, DistributedShopKeeperAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolkAI')

    def __init__(self, spawner):
        DistributedBattleNPCAI.__init__(self, spawner)
        DistributedShopKeeperAI.__init__(self, self.air)
        self.customModel = ''
        self.shopId = 0
        self.helpId = 0
        self.isGhost = 0
        self.ghostColor = 0
        self.isZombie = 0

    def getDNAId(self):
        if self.customModel:
            return self.customModel
        return self.getUniqueId()

    def setShopId(self, shopId):
        self.shopId = shopId

    def getShopId(self):
        return self.shopId

    def setHelpId(self, helpId):
        self.helpId = helpId

    def getHelpId(self):
        return self.helpId

    def setIsGhost(self, isGhost):
        self.isGhost = isGhost

    def getIsGhost(self):
        return self.isGhost

    def setGhostColor(self, ghostColor):
        self.ghostColor = ghostColor

    def getGhostColor(self):
        return self.ghostColor

    def setZombie(self, zombie):
        self.isZombie = zombie

    def d_setZombie(self, zombie):
        self.sendUpdate('setZombie', zombie)

    def b_setZombie(self, zombie):
        self.setZombie(zombie)
        self.d_setZombie(zombie)

    def getZombie(self):
        return self.isZombie

    def isBattleable(self):
        return 0

    # requestMusic(uint32) airecv clsend
    # playMusic(uint32) broadcast
    # levelUpCutlass(uint32) airecv clsend
    # setQuestRewardsEarned(uint32, uint32, uint32 [])
    # setInInvasion(bool) broadcast ram
    # setZombie(bool) broadcast ram
    # setMovie(string, uint32) broadcast ram
    # triggerInteractShow(uint32)
    # offerOptions(int8)
    # startTutorial(uint8)
    # swordTutorialPt1(uint32) airecv clsend
    # pistolTutorialPt1(uint32) airecv clsend
    # shipTutorialPt1(uint32, ItemNameHolder) airecv clsend

    def handleInteract(self, avId, interactType, instant):
        if interactType == PiratesGlobals.INTERACT_TYPE_FRIENDLY:
            return ACCEPT_SEND_UPDATE | ACCEPT

        return DistributedBattleNPCAI.handleInteract(self, avId, interactType, instant)

    def processRespec(self, avId, av, respecId):

        if not config.GetBool('want-respec-option', False):
            self.air.writeServerEvent('suspicious', avId=avId, message="Client bypassed sanity check and used the respec DistributedNPCTownfolkAI option")
            return

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatar: %s" % av)
            return

        IGToITMap = {
            InteractGlobals.RESPEC_CUTLASS: InventoryType.CutlassRep,
            InteractGlobals.RESPEC_PISTOL: InventoryType.PistolRep,
            InteractGlobals.RESPEC_DAGGER: InventoryType.DaggerRep,
            InteractGlobals.RESPEC_DOLL: InventoryType.DollRep,
            InteractGlobals.RESPEC_GRENADE: InventoryType.GrenadeRep,
            InteractGlobals.RESPEC_STAFF: InventoryType.WandRep,
            InteractGlobals.RESPEC_SAILING: InventoryType.SailingRep,
            InteractGlobals.RESPEC_CANNON: InventoryType.CannonRep }

        weaponRep = IGToITMap[respecId]
        numRespecs = inv.getStackQuantity(getNumRespecType(weaponRep))
        cost = EconomyGlobals.getRespecCost(numRespecs)

        if cost > av.getGoldInPocket():
            return

        IGToCSMap = {} #TODO?

        classSkills = IGToCSMap[respecId]
        for skill in classSkills:
            inv.setStackQuantity(skill, 0)

        IGToIRMap = {
            InteractGlobals.RESPEC_CUTLASS: (InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass),
            InteractGlobals.RESPEC_PISTOL: (InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol),
            InteractGlobals.RESPEC_DAGGER: (InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger),
            InteractGlobals.RESPEC_DOLL: (InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll),
            InteractGlobals.RESPEC_GRENADE: (InventoryType.begin_WeaponSkillGrenade, InventoryType.end_WeaponSkillGrenade),
            InteractGlobals.RESPEC_STAFF: (InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand),
            InteractGlobals.RESPEC_SAILING: (InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing),
            InteractGlobals.RESPEC_CANNON: (InventoryType.begin_WeaponSkillCannon, InventoryType.end_WeaponSkillCannon)
        }
        startRange, endRange = IGTOIRMap[respecId]
        amount = 0 
        for invId in range(startRange, endRange):
            amount += inv.getStackQuantity(invId)

        if amount <= 0:
            return

        pointCount = max(min((amount - 1), 30), 0)
        point = av.getUnspentFromRep(IGToITMap[respecId])
        for i in range(0, pointCount):
            inv.addStackItem(point)

        av.takeGold(cost)
        inv.setStackQuantity(getNumRespecType(weaponRep), numRespecs + 1)

    def selectOption(self, option):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        if option == InteractGlobals.HEAL_HP:
            hp = av.hp
            maxHp = av.getMaxHp()
            
            if hp == maxHp:
                return
            
            cost = EconomyGlobals.getAvatarHealHpCost(maxHp - hp)
            
            if cost > av.getGoldInPocket():
                return
            
            av.takeGold(cost)
            av.toonUp(maxHp - hp)
        elif option == InteractGlobals.HEAL_MOJO:
            mojo = av.getMojo()
            maxMojo = av.getMaxMojo()
            
            if mojo == maxMojo:
                return
            
            cost = EconomyGlobals.getAvatarHealMojoCost(maxMojo - mojo)
            
            if cost > av.getGoldInPocket():
                return
            
            av.takeGold(cost)
            av.b_setMojo(maxMojo)

        elif option == InteractGlobals.PLAY_CANNON_DEFENSE:
            pass #TODO implement cannon defense

        elif option in InteractGlobals.RespecOptions:
            self.processRespec(avId, av, option)
        
    
    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, data):
        if cls is None:
            cls = DistributedNPCTownfolkAI
        avType = getattr(AvatarTypes, data['Category'])
        obj = DistributedBattleNPCAI.makeFromObjectKey(cls, spawner, uid, avType, data)

        helpId = data.get('HelpID', 'NONE')
        if helpId and helpId.isdigit():
            obj.setHelpId(int(helpId))

        shopId = data.get('ShopID', 'PORT_ROYAL_DEFAULTS')
        shopId = getattr(PiratesGlobals, shopId, None)
        if shopId is not None:
            obj.setShopId(shopId)
            
        obj.setZombie(data.get('Zombie', False))

        if 'CustomModel' in data and '/' in data['CustomModel']:
            obj.customModel = data['CustomModel']

        return obj
