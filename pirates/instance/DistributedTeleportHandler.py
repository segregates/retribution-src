from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.world.DistributedOceanGrid import DistributedOceanGrid
from pirates.instance.DistributedInstanceBase import DistributedInstanceBase
from pirates.instance.DistributedMainWorld import DistributedMainWorld
from pirates.distributed.PiratesDistrict import PiratesDistrict
from pirates.piratesbase import PLocalizer

class DistributedTeleportHandler(DistributedObject):
    notify = directNotify.newCategory('DistributedTeleportHandler')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.destWorldGrid = None
        self.destInstance = None
        self.numInterestsCleared = 0
        self.pendingWorld = None
        self.spawnWorldName = None
        self.instanceWorldName = None
        self.doneCallback = None


    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.doId)


    def generate(self):
        DistributedObject.generate(self)


    def disable(self):
        if self.pendingWorld:
            self.cr.relatedObjectMgr.abortRequest(self.pendingWorld)
            self.pendingWorld = None

        self.ignoreAll()
        DistributedObject.disable(self)

    def getRemoveInterestEventName(self):
        return self.uniqueName('teleportRemoveInterest')


    def getAddInterestEventName(self):
        return self.uniqueName('teleportAddInterest')


    def startTeleport(self):
        bandId = localAvatar.getBandId()
        if bandId == None:
            bandId = 0
        elif bandId != 0:
            bandId = bandId[1]

        self.sendUpdate('startTeleportProcess', [
            0,
            0,
            bandId])

    def waitInTZ(self, objIds, destParentId):
        self.otherTeleportingObjIds = objIds
        parent = localAvatar.getParentObj()
        if parent:
            parentsParent = parent.getParentObj()
            if isinstance(parentsParent, DistributedInstanceBase):
                parentsParent.removeWorldInterest()

        elif self.cr.activeWorld:
            self.notify.warning('***JCW*** localAvatar has no parentObj, but has activeWorld: %s,%s' % (self.cr.activeWorld.__class__.__name__, self.cr.activeWorld.doId))
            self.cr.activeWorld.removeWorldInterest()
        else:
            self.notify.warning('***JCW*** localAvatar has no parentObj, and has no activeWorld')
        self.waitInTZ2(0, 0)

    def waitInTZ2(self, destParentId, destZoneId):
        destParentId = self.getLocation()[0]
        destZoneId = localAvatar.doId
        base.loadingScreen.beginStep('enterArea', 29, 80)
        base.loadingScreen.tick(tickNumber = 200)
        localAvatar.b_setLocation(destParentId, destZoneId)
        self.teleportingObjAtDest(destParentId, destZoneId, self.teleportRemoveInterestCompleteTZ)


    def teleportingObjAtDest(self, destParentId, destZoneId, callback, clearInterest = True):
        if clearInterest:
            leaveEvent = self.getRemoveInterestEventName()
            numInterests = localAvatar.clearInterestNamed(leaveEvent, [
                'instanceInterest',
                'worldInterest'])
            localAvatar.clearInterestNamed(leaveEvent + 'Door', [
                'instanceInterest-Door'])
            self.numInterestsCleared = 0
            if numInterests == 0:
                callback(destZoneId, numInterests)
            else:
                self.accept(leaveEvent, callback, extraArgs = [
                    destZoneId,
                    numInterests])
        else:
            callback()

    def teleportRemoveInterestCompleteTZ(self, zoneId, numInterests):
        self.numInterestsCleared += 1
        if self.numInterestsCleared < numInterests:
            return None

        self.accept('shardSwitchComplete', self.shardSwitchComplete, [
            zoneId])
        district = self.getParentObj()
        self.cr.distributedDistrict = district
        self.cr.alterInterest(self.cr.uberZoneInterest, district.getDoId(), 2, event = 'shardSwitchComplete')

    def shardSwitchComplete(self, zoneId):
        self.oldWorld = base.cr.activeWorld

        def clockSyncComplete():
            self.sendUpdate('teleportToInstanceReady', [
                zoneId])

        if base.cr.timeManager and base.cr.timeManager.gotInitialTimeSync():
            clockSyncComplete()
        else:
            self.acceptOnce('gotTimeSync', clockSyncComplete)


    def continueTeleportToInstance(self, instanceParent, instanceZone, instanceDoId, instanceFileName, spawnParent, spawnZone, spawnDoId, spawnFileName, spawnWorldGridDoId):
        self.spawnWorldName = spawnFileName + '.py'
        base.worldCreator.fileDicts = { }
        base.worldCreator.registerFileObject(self.spawnWorldName)
        base.worldCreator.registerFileObject(instanceFileName + '.py')
        base.worldCreator.loadFileDataRecursive(instanceFileName + '.py')
        self.instanceWorldName = None
        if instanceFileName:
            self.instanceWorldName = instanceFileName + '.py'

        localAvatar.setInterest(instanceParent, instanceZone, [
            'worldInterest'])

        def worldArrived(worldObj):
            self.teleportAddInterestWorldComplete(worldObj, spawnParent, spawnZone, spawnDoId, spawnWorldGridDoId, self.spawnWorldName)

        if self.pendingWorld:
            self.cr.relatedObjectMgr.abortRequest(self.pendingWorld)

        self.pendingWorld = self.cr.relatedObjectMgr.requestObjects([
            instanceDoId], eachCallback = worldArrived)

    def teleportAddInterestWorldComplete(self, instance, spawnParent, spawnZone, spawnDoId, spawnWorldGridDoId, worldName):
        addEvent = self.getAddInterestEventName()
        if instance.doId != spawnDoId:
            instance.removeWorldInterest()

        self.acceptOnce(addEvent, self.teleportAddInterestDestComplete, extraArgs = [
            spawnDoId,
            spawnWorldGridDoId,
            worldName])
        localAvatar.setInterest(spawnParent, spawnZone, [
            'instanceInterest'], addEvent)

    def teleportAddInterestDestComplete(self, spawnDoId, spawnWorldGridDoId, worldName):
        base.cr.relatedObjectMgr.requestObjects([
            spawnDoId], eachCallback = lambda param1, param2 = spawnWorldGridDoId, param3 = spawnDoId, param4 = worldName: self.teleportInstanceExists(param1, param2, param3, param4))

    def teleportInstanceExists(self, instanceObj, worldGridDoId, instanceDoId, worldName):
        self.destInstance = instanceObj
        base.cr.relatedObjectMgr.requestObjects([
            worldGridDoId], eachCallback = lambda param1, param2 = instanceDoId, param3 = worldName: self.teleportWorldGridExists(param1, param2, param3))

    def teleportWorldGridExists(self, worldGridObj, instanceDoId, worldName):
        oceanAreas = base.cr.distributedDistrict.worldCreator.getOceanData(worldName)
        if oceanAreas:
            for currArea in oceanAreas:
                worldGridObj.addOceanArea(*currArea[:4])

            worldGridObj.addOceanAreasToMap()

        self.teleportInstanceComplete(worldGridObj, instanceDoId)

    def teleportInstanceComplete(self, worldGrid, instanceDoId):
        self.setDestWorldGrid(worldGrid)
        if base.cr.distributedDistrict.shardType == PiratesGlobals.SHARD_WELCOME:
            localAvatar.b_setTeleportFlag(PiratesGlobals.TFInWelcomeWorld)
        else:
            localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInWelcomeWorld)
        self.sendUpdate('readyToFinishTeleport', [
            instanceDoId])

    def teleportToInstanceCleanup(self):
        if self.destInstance == None or self.destInstance.spawnInfo == None:
            self.notify.warning('no local destInstance reference for %s %s %s %s %s' % (localAvatar.doId, self.doId, self.getLocation(), self.spawnWorldName, self.instanceWorldName))
            self.sendAvatarLeft()
            self.abortTeleport()
            return None

        (self.spawnPos, zoneId, parents) = self.destInstance.spawnInfo
        self.cr.teleportMgr.createSpawnInterests(parents, self.teleportToInstanceCleanup3, self.destWorldGrid, localAvatar)

    def teleportToInstanceCleanup3(self, parentObj, teleportingObj):
        self.cr.teleportMgr.localTeleportToId(parentObj.doId, teleportingObj, self.spawnPos)
        if isinstance(parentObj, DistributedGameArea):
            self.destInstance.addWorldInterest(parentObj)
        else:
            self.destInstance.addWorldInterest()
        messenger.send('localAvatarExitWater')
        (currParentId, currZoneId) = teleportingObj.getLocation()
        self.teleportingObjAtDest(currParentId, currZoneId, self.teleportCleanupComplete, False)
        self.oldWorld = None

    def teleportCleanupComplete(self):
        self.cr.activeWorld.setWorldGrid(self.destWorldGrid)
        localAvatar.teleportCleanupComplete(self.instanceType)
        self.sendUpdate('teleportToInstanceFinal', [
            localAvatar.getDoId()])
        self.clearTZInterest()

    def clearTZInterest(self):
        localAvatar.clearInterestNamed(None, [
            'TZInterest'])
        if self.doneCallback:
            self.doneCallback(self.destInstance)
            self.doneCallback = None

        messenger.send('localAvTeleportFinished')
        base.cr.teleportMgr.clearAmInTeleport()
        if self.destInstance:
            self.destInstance.queryActiveQuests()



    def setDestWorldGrid(self, worldGrid):
        self.destWorldGrid = worldGrid

    def abortTeleport(self):
        self.notify.debug('%s: abortTeleport called' % self.doId)
        self.clearTZInterest()
        base.cr.teleportMgr.failTeleport(message = PLocalizer.TeleportGenericFailMessage)


    def sendAvatarLeft(self):
        self.sendUpdate('avatarLeft')
