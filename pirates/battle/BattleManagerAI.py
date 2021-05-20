from BattleManagerBase import *
from pirates.inventory import ItemGlobals

class BattleManagerAI(BattleManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')
    wantComboTiming = config.GetBool('want-easy-combos', False)

    def __init__(self, air):
        self.air = air
    
    def getGameStatManager(self):
        return self.air.gameStatManager

    def targetInRange(self, attacker, target, skillId, ammoSkillId, distance):
        tolerance = .5
        range = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        if range == WeaponGlobals.INF_RANGE:
            return 1

        return distance <= range + tolerance

    def doAttack(self, attacker, skillId, ammoSkillId, targetId, areaIdList, distance, combo = 0, charge = 0):
        if (not targetId) and areaIdList:
            targetId = areaIdList[0]

        weaponHit = self.__doAttack(attacker, skillId, ammoSkillId, targetId, areaIdList, distance, combo, charge)

        if targetId and attacker and (not attacker.isNpc) and weaponHit == WeaponGlobals.RESULT_HIT:
            target = self.air.doId2do.get(targetId)
            if target:
                repId = ItemGlobals.getItemRepId(attacker.currentWeaponId)
                if repId:
                    target.enemySkills.setdefault(attacker.doId, set()).add((repId, skillId, ammoSkillId))

        return weaponHit

    def __doAttack(self, attacker, skillId, ammoSkillId, targetId, areaIdList, distance, combo = 0, charge = 0):
        attacker.battleRandom.advanceAttackSeed()
        if targetId:
            target = self.air.doId2do.get(targetId)
            if not (WeaponGlobals.getIsShipSkill(skillId) or WeaponGlobals.getIsDollAttackSkill(skillId)):
                if hasattr(target, 'getSkillEffects'):
                    if WeaponGlobals.C_SPAWN in set(target.getSkillEffects()):
                        return WeaponGlobals.RESULT_MISS

        else:
            target = None

        weaponHit = self.willWeaponHit(attacker, target, skillId, ammoSkillId, charge)
        
        if weaponHit == WeaponGlobals.RESULT_MISS:
            return weaponHit

        if combo == -1:
            if self.wantComboTiming:
                return WeaponGlobals.RESULT_MISS

        if not WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            return WeaponGlobals.RESULT_HIT

        if not target and not areaIdList:
            return WeaponGlobals.RESULT_MISS

        if target and not self.obeysPirateCode(attacker, target):
            return WeaponGlobals.RESULT_AGAINST_PIRATE_CODE

        if target and not self.targetInRange(attacker, target, skillId, ammoSkillId, distance):
            return WeaponGlobals.RESULT_OUT_OF_RANGE

        if target:
            skillEffects = target.getSkillEffects()
            if WeaponGlobals.C_SPAWN in skillEffects:
                return WeaponGlobals.RESULT_MISS

        return weaponHit
