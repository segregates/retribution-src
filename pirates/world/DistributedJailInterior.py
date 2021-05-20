from pirates.world.DistributedGAInterior import DistributedGAInterior
from pirates.piratesbase import PiratesGlobals

class DistributedJailInterior(DistributedGAInterior):
    notify = directNotify.newCategory('DistributedJailInterior')

    def announceGenerate(self):
        DistributedGAInterior.announceGenerate(self)
        doorPlanes = self.geom.findAllMatches('**/door_collision_planar_*;+s')
        doorPlanes.stash()

    def handleChildArrive(self, childObj, zoneId):
        DistributedGAInterior.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal() and childObj.belongsInJail():
            localAvatar.b_setGameState('ThrownInJail')
            if not self.footstepSound:
                localAvatar.setAreaFootstep('Rock')

    def handleAvatarSetLocation(self, parentId, zoneId):
        pass