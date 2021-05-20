from otp.distributed.DistributedDistrictAI import DistributedDistrictAI
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals

import time

class PiratesDistrictAI(DistributedDistrictAI):
    parentingRules = ('', '')
    mainWorld = WorldGlobals.PiratesWorldSceneFileBase
    tutorialWorld = WorldGlobals.PiratesTutorialSceneFileBase
    shardType = PiratesGlobals.SHARD_MAIN
    avatarCount = 0

    def __init__(self, air):
        DistributedDistrictAI.__init__(self, air)
        self.minimumAdminAccess = config.GetInt('minimum-admin-access', 0)

    def announceGenerate(self):
        DistributedDistrictAI.announceGenerate(self)

        self.created = int(time.time())
        self.accept('queryShardStatus', self.d_updateRPCStatus)
        self.air.addPostRemove(self.air.prepareMessage('shardDeath'))

        self.d_updateRPCStatus()

    def d_updateRPCStatus(self):
        # Send a shard status update with the information we have:
        status = {
            'available': bool(self.available),
            'name': self.name,
            'created': self.created
        }
        self.air.sendNetEvent('shardStatus', [status])

    def setParentingRules(self, rule1, rule2):
        self.parentingRules = (rule1, rule2)

    def d_setParentingRules(self, rule1, rule2):
        self.sendUpdate('setParentingRules', [rule1, rule2])

    def b_setParentingRules(self, rule1, rule2):
        self.setParentingRules(rule1, rule2)
        self.d_setParentingRules(rule1, rule2)

    def getParentingRules(self):
        return self.parentingRules

    def setMainWorld(self, mainWorld):
        self.mainWorld = mainWorld

    def d_setMainWorld(self, mainWorld):
        self.sendUpdate('setMainWorld', [mainWorld])

    def b_setMainWorld(self, mainWorld):
        self.setMainWorld(mainWorld)
        self.d_setMainWorld(mainWorld)

    def getMainWorld(self):
        return self.mainWorld

    def setShardType(self, shardType):
        self.shardType = shardType

    def d_setShardType(self, shardType):
        self.sendUpdate('setShardType', [shardType])

    def b_setShardType(self, shardType):
        self.setShardType(shardType)
        self.b_setShardType(shardType)

    def getShardType(self):
        return self.shardType

    def d_setAvailable(self, available):
        DistributedDistrictAI.d_setAvailable(self, available)
        self.d_updateRPCStatus()

    def rpcSetAvailable(self, available):
        self.b_setAvailable(available)
    
    def setMinimumAdminAccess(self, minimumAdminAccess):
        self.minimumAdminAccess = minimumAdminAccess

    def d_setMinimumAdminAccess(self, minimumAdminAccess):
        self.sendUpdate('setNewAvatarCount', [minimumAdminAccess])

    def b_setMinimumAdminAccess(self, minimumAdminAccess):
        self.d_setMinimumAdminAccess(minimumAdminAccess)
        self.setMinimumAdminAccess(minimumAdminAccess)
    
    def getMinimumAdminAccess(self):
        return self.minimumAdminAccess
    
    def setAvatarCount(self, avCount):
        self.avatarCount = avCount

    def getAvatarCount(self):
        return self.avatarCount

    def d_setAvatarCount(self, avCount):
        self.sendUpdate('setAvatarCount', [avCount])

    def b_setAvatarCount(self, avCount):
        self.d_setAvatarCount(avCount)
        self.setAvatarCount(avCount)

