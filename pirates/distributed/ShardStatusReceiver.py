from direct.showbase.DirectObject import DirectObject

class ShardStatusReceiver(DirectObject):
    def __init__(self, air):
        self.air = air

        self.shards = {}

        # Accept the shardStatus event:
        self.accept('shardStatus', self.handleShardStatus)
        self.accept('shardDeath', self.handleShardDeath)

        # Query the status of any existing shards:
        self.air.sendNetEvent('queryShardStatus')

    def handleShardStatus(self, status):
        channel = self.air.getMsgSender()
        self.shards.setdefault(channel, {}).update(status)

    def handleShardDeath(self):
        channel = self.air.getMsgSender()
        if channel in self.shards:
            del self.shards[channel]

    def getShards(self):
        return self.shards
