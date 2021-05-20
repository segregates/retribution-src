from panda3d.core import Vec3
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
import WeaponGlobals


class WeaponBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def requestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge):
        pass

    def useTargetedSkill(self, skillId, ammoSkillId, actualResult, targetId,
                         areaIdList, attackerEffects, targetEffects, areaIdEffects,
                         itemEffects, timestamp, pos, charge=0):
        self.sendUpdate('useTargetedSkill', [skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge])

    def requestShipSkill(self, skillId, ammoSkillId, clientResult, targetId, timestamp):
        pass

    def requestProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, power):
        pass

    def suggestProjectileSkillResult(self, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp):
        pass

    def getWorld(self):
        parent = self.getParentObj()
        while parent and not isinstance(parent, DistributedInstanceBaseAI):
            parent = parent.getParentObj()

        return parent

    def attemptUseTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList,
                                timestamp, pos, charge):
        distance = Vec3(pos)
        distance.setZ(distance.getZ() / 2)
        distance = distance.length()

        targetEffects = [0, 0, 0, 0, 0]
        attackerEffects = [0, 0, 0, 0, 0]
        actualAreaIdList = []
        areaIdEffects = []
        itemEffects = []

        actualResult = self.air.battleMgr.doAttack(self, skillId, ammoSkillId, targetId,
                                                   areaIdList, distance, charge=charge)
        if actualResult in (WeaponGlobals.RESULT_HIT,
                            WeaponGlobals.RESULT_DELAY,
                            WeaponGlobals.RESULT_REFLECTED):
            mojo = abs(WeaponGlobals.getMojoCost(skillId))
            
            if mojo:
                if self.getMojo() < mojo:
                    return WeaponGlobals.RESULT_MISS
                else:
                    self.b_setMojo(self.getMojo() - mojo)

            if targetId:
                target = self.air.doId2do.get(targetId)
                if isinstance(target, WeaponBaseAI):
                    attackerEffects, targetEffects, itemEffects = self.air.battleMgr.getModifiedSkillEffects(self,
                                                                   target, skillId, ammoSkillId, charge, distance)
                    hp = targetEffects[0]
                    target.hpDelta(hp)

            for tgId in areaIdList:
                target = self.air.doId2do.get(tgId)
                if isinstance(target, WeaponBaseAI):
                    attackerEffects, effect, _ = self.air.battleMgr.getModifiedSkillEffects(self,
                                                  target, skillId, ammoSkillId, charge, distance)
                    hp = effect[0]
                    target.hpDelta(hp)
                    actualAreaIdList.append(tgId)
                    areaIdEffects.append(effect)

        hp = attackerEffects[0]
        self.hpDelta(hp)
        self.useTargetedSkill(skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects,
                              targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge)

        return actualResult
