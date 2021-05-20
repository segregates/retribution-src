from direct.directnotify import DirectNotifyGlobal
from pirates.npc.BossBase import BossBase
from pirates.npc.BossNPCList import BOSS_NPC_LIST

class BossAI(BossBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossAI')

    def __init__(self, air):
        self.air = air

    def _getDefaultValue(self, key):
        return BOSS_NPC_LIST[''][key]

    def _getHpScale(self):
        return self.bossData['HpScale']

    def _getMpScale(self):
        return self.bossData['MpScale']

    def _getLevel(self):
        return self.bossData['Level']

    def _getScale(self):
        return self.bossData['ModelScale']

    def _getWeapon(self):
        return self.bossData['Weapon']

    def _getWeaponLevel(self):
        return self.bossData['WeaponLevel']

    def _getSkills(self):
        return self.bossData['Skills']

    def _getSkillLevel(self):
        return self.bossData['SkillLevel']

    def _getGoldScale(self):
        return self.bossData['GoldScale']

    def _getDamageScale(self):
        return self.bossData['DamageScale']

    def _getAvatarType(self):
        return self.bossData['AvatarType']

    def _setupBossValues(self, uid, avType):
        self.loadBossData(uid, avType)

        scale = self._getScale()
        #self.setScale(scale, scale, scale)
        self.setName(self.getNameText())
        self.setDamageScale(self._getDamageScale())