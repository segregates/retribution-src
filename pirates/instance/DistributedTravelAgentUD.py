from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD


class DistributedTravelAgentUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('DistributedTravelAgentUD')

    def requestInitLoc(self, desiredShard):
        sender = self.air.getMsgSender()
        self.sendUpdateToChannel(sender, 'requestInitLocResponse', [True, desiredShard])
