from panda3d.core import NodePath
from direct.directnotify import DirectNotifyGlobal
from otp.distributed.DistributedDistrict import DistributedDistrict
from pirates.world import WorldCreator
from pirates.piratesbase import PiratesGlobals

class PiratesDistrict(DistributedDistrict, NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesDistrict')

    def __init__(self, cr):
        DistributedDistrict.__init__(self, cr)
        NodePath.__init__(self, render.attachNewNode('District-%s' % id(self)))
        self.mainWorldFile = None
        self.islands = { }
        self.shardType = 0
        self.minimumAdminAccess = 0

    def announceGenerate(self):
        DistributedDistrict.announceGenerate(self)
        self.worldCreator = base.worldCreator
        self.worldCreator.district = self
        if self.shardType == PiratesGlobals.SHARD_MAIN:
            self.worldCreator.makeMainWorld(self.mainWorldFile)
            self.worldCreator.registerFileObject(self.mainWorldFile)

    def setShardType(self, shardType):
        self.shardType = shardType

    def setMainWorld(self, world):
        self.mainWorldFile = world

    def delete(self):
        DistributedDistrict.delete(self)
        if self.worldCreator:
            self.worldCreator.destroy()

    def getName(self):
        return self.name
    
    def setMinimumAdminAccess(self, minimumAdminAccess):
        self.minimumAdminAccess = minimumAdminAccess
    
    def getMinimumAdminAccess(self):
        return self.minimumAdminAccess
    
    def hasAdminAccess(self):
        return base.getAdminAccess() >= self.minimumAdminAccess

    def setAvatarCount(self, avatarCount):
        if not hasattr(self, 'doId'):
            return

        if self.doId in self.cr.activeDistrictMap:
            self.cr.activeDistrictMap[self.doId].avatarCount = avatarCount
            messenger.send('ShardPopulationUpdate', [self.doId, avatarCount])
