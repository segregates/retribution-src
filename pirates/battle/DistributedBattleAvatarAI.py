from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.reputation.DistributedReputationAvatarAI import *
from pirates.pirate.AvatarType import AvatarType
from pirates.pirate import AvatarTypes
from pirates.inventory import ItemGlobals

from WeaponBaseAI import WeaponBaseAI
from BattleRandom import BattleRandom
from Teamable import Teamable

import WeaponGlobals

class DistributedBattleAvatarAI(Teamable, DistributedReputationAvatarAI, WeaponBaseAI):
    notify = directNotify.newCategory('DistributedBattleAvatarAI')
    avatarType = AvatarTypes.AnyAvatar
    isNpc = False
    zombie = False

    def __init__(self, air):
        DistributedReputationAvatarAI.__init__(self, air)
        WeaponBaseAI.__init__(self, air)
        Teamable.__init__(self)
        self.level = 0
        self.mojo = 0
        self.maxMojo = 0
        self.currentWeaponId = 0
        self.isWeaponDrawn = 0
        self.currentAmmo = 0
        self.currentCharm = 0
        self.shipId = 0
        self.inInvasion = False
        self.skillEffects = []
        self.isGhost = 0
        self.ghostColor = 0
        self.luck = 0
        self.maxluck = 0
        self.swiftness = 0
        self.maxSwiftness = 0
        self.power = 0
        self.maxPower = 0
        self.ensnaredTargetId = 0
        self.enemySkills = {}

    def announceGenerate(self):
        DistributedReputationAvatarAI.announceGenerate(self)
        self.battleRandom = BattleRandom(self.doId)

    def getHp(self):
        return [self.hp, 1]

    def setLevel(self, level):
        self.level = level

    def d_setLevel(self, level):
        self.sendUpdate('setLevel', [level])

    def b_setLevel(self, level):
        self.setLevel(level)
        self.d_setLevel(level)

    def getLevel(self):
        return self.level

    def setHp(self, hp, quietly=0):
        DistributedAvatarAI.setHp(self, hp)

    def d_setHp(self, hp, quietly=0):
        self.sendUpdate('setHp', [hp, quietly])

    def b_setHp(self, hp, quietly=0):
        self.setHp(hp) # This might be modified by DPPAI (groggy)
        self.d_setHp(self.hp, quietly)

    def setIsGhost(self, isGhost):
        self.isGhost = isGhost

    def d_setIsGhost(self, isGhost):
        self.sendUpdate('setIsGhost', [isGhost])

    def b_setIsGhost(self, isGhost, evil=None):
        self.setIsGhost(isGhost)
        self.d_setIsGhost(isGhost)
        if evil is not None:
            self.setIsGhost(evil)
            self.d_setIsGhost(evil)

    def getIsGhost(self):
        return self.isGhost

    def setGhostColor(self, ghostColor):
        self.ghostColor = ghostColor

    def d_setGhostColor(self, ghostColor):
        self.sendUpdate("setGhostColor", [ghostColor])

    def b_setGhostColor(self, ghostColor):
        self.setGhostColor(ghostColor)
        self.d_setGhostColor(ghostColor)

    def getGhostColor(self):
        return self.ghostColor

    def setMojo(self, mojo):
        self.mojo = mojo

    def d_setMojo(self, mojo):
        self.sendUpdate('setMojo', [mojo])

    def b_setMojo(self, mojo):
        self.setMojo(mojo) # This might be modified by DPPAI (groggy)
        self.d_setMojo(self.mojo)

    def getMojo(self):
        return self.mojo

    def setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo

    def d_setMaxMojo(self, maxMojo):
        self.sendUpdate('setMaxMojo', [maxMojo])

    def b_setMaxMojo(self, maxMojo):
        self.setMaxMojo(maxMojo)
        self.d_setMaxMojo(maxMojo)

    def getMaxMojo(self):
        return self.maxMojo

    def setPower(self, power):
        self.power = power

    def d_setPower(self, power):
        self.sendUpdate('setPower', [power])

    def b_setPower(self, power):
        self.setPower(power)
        self.d_setPower(power)

    def getPower(self):
        return self.power

    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def d_setMaxPower(self, maxPower):
        self.sendUpdate('setMaxPower', [maxPower])

    def b_setMaxPower(self, maxPower):
        self.setMaxPower(maxPower)
        self.d_setMaxPower(maxPower)

    def getMaxPower(self):
        return self.maxPower

    def setAvatarType(self, avatarType):
        self.avatarType = AvatarType.fromTuple(avatarType)

    def getAvatarType(self):
        return self.avatarType.asTuple()

    def getRawAvatarType(self):
        return self.avatarType

    def isBoss(self):
        return self.avatarType.isA(AvatarTypes.BossType)

    def setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        self.currentWeaponId = currentWeapon
        self.isWeaponDrawn = isWeaponDrawn

    def d_setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        self.sendUpdate('setCurrentWeapon', [currentWeapon, isWeaponDrawn])

    def b_setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        self.setCurrentWeapon(currentWeapon, isWeaponDrawn)
        self.d_setCurrentWeapon(currentWeapon, isWeaponDrawn)

    def getCurrentWeapon(self):
        return [self.currentWeaponId, self.isWeaponDrawn]

    def setCurrentAmmo(self, currentAmmo):
        self.currentAmmo = currentAmmo

    def d_setCurrentAmmo(self, currentAmmo):
        self.sendUpdate('setCurrentAmmo', [currentAmmo])

    def b_setCurrentAmmo(self, currentAmmo):
        self.setCurrentAmmo(currentAmmo)
        self.d_setCurrentAmmo(currentAmmo)

    def getCurrentAmmo(self):
        return self.currentAmmo

    def setCurrentCharm(self, currentCharm):
        self.currentCharm = currentCharm

    def d_setCurrentCharm(self, currentCharm):
        self.sendUpdate('setCurrentCharm', [currentCharm])

    def b_setCurrentCharm(self, currentCharm):
        self.setCurrentCharm(currentCharm)
        self.d_setCurrentCharm(currentCharm)

    def getCurrentCharm(self):
        return self.currentCharm

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def setInInvasion(self, inInvasion):
        self.inInvasion = inInvasion

    def d_setInInvasion(self, inInvasion):
        self.sendUpdate('setInInvasion', [inInvasion])

    def b_setInInvasion(self, inInvasion):
        self.setInInvasion(inInvasion)
        self.d_setInInvasion(inInvasion)

    def getInInvasion(self):
        return self.inInvasion

    def isInInvasion(self):
        return self.getInInvasion()

    def setLuck(self, luck):
        self.luck = luck

    def d_setLuck(self, luck):
        self.sendUpdate('setLuck', [luck])

    def b_setLuck(self, luck):
        self.setLuck(luck)
        self.d_setLuck(luck)

    def getLuck(self):
        return self.luck

    def setSwiftness(self, swiftness):
        self.swiftness = swiftness

    def d_setSwiftness(self, swiftness):
        self.sendUpdate('setSwiftness', [swiftness])

    def b_setSwiftness(self, swiftness):
        self.setSwiftness(swiftness)
        self.d_setSwiftness(swiftness)

    def getSwiftness(self):
        return self.swiftness

    def setMaxSwiftness(self, maxSwiftness):
        self.maxSwiftness = maxSwiftness

    def d_setMaxSwiftness(self, maxSwiftness):
        self.sendUpdate('setMaxSwiftnes', [maxSwiftness])

    def b_setMaxSwiftness(self, maxSwiftness):
        self.setMaxSwiftnes(maxSwiftness)
        self.d_setMaxSwiftness(maxSwiftness)

    def getMaxSwiftness(self):
        return self.maxSwiftness

    def setMaxLuck(self, luck):
        self.maxluck = luck

    def d_setMaxLuck(self, luck):
        self.sendUpdate('setMaxLuck', [luck])

    def b_setMaxLuck(self, luck):
        self.setMaxLuck(luck)
        self.d_setMaxLuck(luck)

    def getMaxLuck(self):
        return self.maxluck

    def setEnsnaredTargetId(self, avId):
        self.ensnaredTargetId = avId

    def d_setEnsnaredTargetId(self, avId):
        self.sendUpdate('setEnsnaredTargetId', [avId])

    def b_setEnsnaredTargetId(self, avId):
        self.setEnsnaredTargetId(avId)
        self.d_setEnsnaredTargetId(avId)

    def getEnsnaredTargetId(self):
        return self.ensnaredTargetId

    def addSkillEffect(self, effectId, attacker=0):
        # TO DO
        timestamp = 0
        duration = 0
        timeLeft = 0
        recur = 0
        data = [0]

        self.skillEffects.append([effectId, attacker, timestamp, duration, timeLeft, recur, data])
        self.sendUpdate('setSkillEffects', [self.skillEffects])
        # TO DO: expire task

    def removeSkillEffect(self, effectId, attacker=0):
        newEffectList = []
        for buff in self.skillEffects:
            if buff[0] == effectId:
                if (not attacker) or buff[1] == attacker:
                    continue

            newEffectList.append(buff)

        if newEffectList != self.skillEffects:
            self.skillEffects = newEffectList
            self.sendUpdate('setSkillEffects', [self.skillEffects])

        # TO DO: expire task

    def getSkillEffects(self):
        # Extremely hackful
        if not hasattr(self, 'battleRandom'):
            return self.skillEffects

        buffIds = set()
        for buff in self.skillEffects:
            buffIds.add(buff[0])

        return buffIds
    
    def hasSkillEffect(self, effectId):
        return effectId in self.getSkillEffects()

    def getSkillRankBonus(self, skillId):
        upgradeAmt = WeaponGlobals.getAttackUpgrade(skillId)
        realSkillId = WeaponGlobals.getLinkedSkillId(skillId)
        if not realSkillId:
            realSkillId = skillId

        rank = self.getSkillRank(realSkillId)
        if WeaponGlobals.getSkillTrack(skillId) != WeaponGlobals.PASSIVE_SKILL_INDEX:
            rank -= 1

        statBonus = 0
        if rank > 5:
            statBonus = 5 * upgradeAmt
            statBonus = (rank - 5) * (upgradeAmt / 2.0)
        else:
            statBonus = rank * upgradeAmt
        return statBonus


    def getSkillRank(self, skillId):
        if self.isNpc:
            return 0

        skillLvl = 0
        inv = self.getInventory()
        if inv:
            skillLvl = max(0, inv.getStackQuantity(skillId) - 1)
            skillLvl = ItemGlobals.getWeaponBoosts(self.currentWeaponId, skillId)
            skillLvl = ItemGlobals.getWeaponBoosts(self.getCurrentCharm(), skillId)

        return skillLvl