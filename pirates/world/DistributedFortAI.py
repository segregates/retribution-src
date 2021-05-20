# STUB

from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI

class DistributedFortAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFortAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)
        self.islandId = 0
        self.objKey = ''
        self.hp = [0, 0]
        self.level = 0

    # setIslandId(uint32) required broadcast ram
    def setIslandId(self, islandId):
        self.islandId = islandId

    def d_setIslandId(self, islandId):
        self.sendUpdate('setIslandId', [islandId])

    def b_setIslandId(self, islandId):
        self.setIslandId(islandId)
        self.d_setIslandId(islandId)

    def getIslandId(self):
        return [self.islandId]

    # setObjKey(string) required broadcast ram
    def setObjKey(self, objKey):
        self.objKey = objKey

    def d_setObjKey(self, objKey):
        self.sendUpdate('setObjKey', [objKey])

    def b_setObjKey(self, objKey):
        self.setObjKey(objKey)
        self.d_setObjKey(objKey)

    def getObjKey(self):
        return [self.objKey]

    # setHp(int16, uint8) required broadcast ram
    def setHp(self, hp, todo_uint8_1):
        self.hp = hp

    def d_setHp(self, hp, todo_uint8_1):
        self.sendUpdate('setHp', [hp, todo_uint8_1])

    def b_setHp(self, hp, todo_uint8_1):
        self.setHp(hp, todo_uint8_1)
        self.d_setHp(hp, todo_uint8_1)

    def getHp(self):
        return [self.hp]

    # setLevel(uint16) required broadcast ram
    def setLevel(self, level):
        self.level = level

    def d_setLevel(self, level):
        self.sendUpdate('setLevel', [level])

    def b_setLevel(self, level):
        self.setLevel(level)
        self.d_setLevel(level)

    def getLevel(self):
        return [self.level]

    # setDrawbridgesLerpR(uint8) broadcast

    # hideDrawbridges() broadcast

    # hitByProjectile(SkillId, SkillId) airecv clsend

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedBattleAvatarAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setObjKey(objKey)
        
        return obj


