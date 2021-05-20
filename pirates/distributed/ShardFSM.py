from direct.fsm.FSM import FSM
from direct.task.Task import Task
from direct.distributed import DistributedSmoothNode
from pirates.piratesbase import PiratesGlobals
from pirates.world.LocationConstants import LocationIds

class ShardFSM(FSM):

    def __init__(self, cr):
        FSM.__init__(self, 'ShardFSM')
        self.cr = cr
        self.shardInterestHandle = None
        self.request('NoShard')


    def enterOff(self):
        self.cr.uidMgr.reset()
        if self.cr.distributedDistrict:
            self.cr.distributedDistrict.worldCreator.cleanupAllAreas()

        self.cr._removeAllOV()
        self.cr.cache.turnOff()
        self.cr.doDataCache.flush()
        self.cr.handler = self.cr.handleMessageType
        self.cr.cleanupWaitAllInterestsComplete()


    def enterNoShard(self):
        locUID = localAvatar.getReturnLocation()
        if locUID:
            self.cr.loadingScreen.showTarget(locUID)
            self.cr.loadingScreen.showHint(locUID)
        else:
            locUID = LocationIds.PORT_ROYAL_ISLAND
            localAvatar.setReturnLocation(locUID)
            self.cr.loadingScreen.showTarget(jail = True)
        base.graphicsEngine.renderFrame()

        self.cr._userLoggingOut = False

    def filterNoShard(self, request, args):
        if request == 'ShardReady':
            return None

        return self.defaultFilter(request, args)

    def exitNoShard(self):
        pass

    def enterOpenShard(self):
        shardId = self.cr.getShardId()
        self.cr.handler = self.cr.handleWaitOnEnterResponses
        self.cr.cache.turnOn()
        self.acceptOnce('shardInterestComplete', self.request, extraArgs = [
            'PrepareShard',
            shardId])
        self.shardInterestHandle = self.cr.addTaggedInterest(shardId, PiratesGlobals.ShardInterestZone, self.cr.ITAG_SHARD, 'shardInterest', event = 'shardInterestComplete')

    def exitOpenShard(self):
        pass

    def fromOpenShardToOff(self):
        self.exitOpenShard()
        self.ignore('shardInterestComplete')
        self.cr.removeTaggedInterest(self.shardInterestHandle)
        self.shardInterestHandle = None
        self.enterOff()

    def enterPrepareShard(self, shardId):
        self.cr.distributedDistrict = self.cr.getDo(shardId)
        DistributedSmoothNode.globalActivateSmoothing(1, 0)

        if self.cr.timeManager.synchronize('startup'):
            self.acceptOnce('gotTimeSync', self.request, extraArgs = [
                'ShardReady',
                shardId])
        else:
            self.demand('ShardReady', shardId)

    def exitPrepareShard(self):
        self.cr.removeTaggedInterest(self.shardInterestHandle)
        self.shardInterestHandle = None
        self.ignore('gotTimeSync')
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectSwitchShards)

    def fromPrepareShardToShardReady(self, shardId):
        self.ignore('gotTimeSync')
        self.enterShardReady(shardId)

    def enterShardReady(self, shardId):
        self.cr.handler = self.cr.handlePlayGame
        base.transitions.noFade()

        def checkScale(task):
            return Task.cont

        messenger.send('shardReady-%s' % (shardId,))

    def exitShardReady(self):
        self.cr.cache.turnOff()
        self.cr.removeInterestTag(self.cr.ITAG_GAME)
        self.cr.setWorldStack([])
        self.cr.removeInterestTag(self.cr.ITAG_WORLD)
        self.cr.removeTaggedInterest(self.shardInterestHandle)
        self.shardInterestHandle = None
        self.cr.removeInterestTag(self.cr.ITAG_SHARD)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectSwitchShards)

        taskMgr.remove('globalScaleCheck')
        self.handler = None