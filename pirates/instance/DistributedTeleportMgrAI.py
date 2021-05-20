from direct.distributed import DistributedObjectAI

class DistributedTeleportMgrAI(DistributedObjectAI.DistributedObjectAI):

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid,
                         instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        obj = self.air.uid2do.get(locationUid)
        doId, parentId, zoneId = 0, 0, 0
        if obj:
            doId = obj.doId
            parentId, zoneId = obj.getLocation()

        if obj and 'JailInterior' in obj.dclass.getName():
            if av:
                self.__pendingJail(obj, av)

            else:
                self.acceptOnce('generate-%d' % avId, lambda av: self.__pendingJail(obj, av))

        self.sendUpdateToAvatarId(avId, '_localTeleportToIdResponse', [doId, parentId, zoneId])

    def __pendingJail(self, obj, av):
        if av.getUnderArrest():
            obj.allocateCell(av)
            av.addDeathPenalty()

    def requestTargetsLocation(self, todo0):
        pass

    def requestTeleportToIsland(self, todo0):
        pass

    def requestTeleportToFishingShip(self):
        pass

    def requestClearPreventDamage(self):
        pass

    def requestCrossShardDeploy(self, todo0, todo1, todo2):
        pass

    def teleportToObjectReq(self, todo0):
        pass

    def teleportToObjectResp(self, todo0, todo1, todo2, todo3):
        pass

    def initiateStowawayTeleport(self, locationUid):
        avId = self.air.getAvatarIdFromSender()

        obj = self.air.uid2do.get(locationUid)
        doId, parentId, zoneId = 0, 0, 0
        if obj:
            doId = obj.doId
            parentId, zoneId = obj.getLocation()
        self.sendUpdateToAvatarId(avId, 'stowawayTeleportResponse', [parentId, doId])