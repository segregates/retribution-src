from direct.task import Task
from direct.distributed import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.world import ZoneLOD
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog
from pirates.quest import QuestDB, QuestLadderDB

'''
Congratulations, Disney! You've managed to write this very gay code.
DistributedTeleportMgr is the gayest thing ever existed.
Do not try to understand this shit, I've already done it for you.
By the way it gave me cancer and aids.
'''

class DistributedTeleportMgr(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('DistributedTeleportMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.instanceType = None
        self.fromInstanceType = None
        self.lastLocalTeleportLoc = None
        self.teleportQueryId = None
        self.inInstanceType = PiratesGlobals.INSTANCE_MAIN
        self.instanceName = 'mainWorld'
        self.doneCallback = None
        self.startedCallback = None
        self.oldWorld = None
        self.requestData = None
        self.localTeleportId = None
        self.localTeleportingObj = None
        self.localTeleportCallback = None
        self.localTeleportDestPos = None
        self.popupDialog = None
        self.doEffect = False
        self.stowawayEffect = False
        self.teleportQueue = []
        self.teleportQueueProcess = None


    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        base.cr.teleportMgr = self
        self.localTeleportingObj = localAvatar
        self.__pendingGoNow = [True]
        localAvatar.readyToTeleport(self)
        self.accept('localAvTeleportFinishedRequest', self.localAvTeleportFinishedRequest)


    def requestLocalTeleport(self, locationName = None):
        self.requestData = ((), {
            'locationName': locationName })
        localAvatar.confirmTeleport(self.localTeleportConfirmation, feedback = True)


    def localTeleportConfirmation(self, confirmed):
        if confirmed:
            requestData = self.requestData
            self.localTeleport(*requestData[0], **requestData[1])
            locationUid = requestData['locationUid']
            base.cr.loadingScreen.showTarget(locationUid)
            base.cr.loadingScreen.showHint(locationUid)

        self.requestData = None


    def localTeleportEffect(self, teleportPosHpr, parent=None, smooth=False, goNow=False):
        if localAvatar.testTeleportFlag(PiratesGlobals.TFInWater) or goNow:
            self.localTeleportPos(teleportPosHpr, parent, smooth)
        else:
            localAvatar.b_setGameState('TeleportOut')
            taskMgr.doMethodLater(5, self.localTeleportPos, self.uniqueName('localTeleportPos'), extraArgs = [
                teleportPosHpr,
                parent,
                smooth])

    def localTeleportPos(self, teleportPosHpr, parent = None, smooth = False):
        localAvatar.b_setGameState('TeleportOut', [
            None,
            False])
        currParent = localAvatar.getParentObj()
        if isinstance(currParent, ZoneLOD.ZoneLOD):
            localAvatar.leaveZoneLOD(currParent)

        if parent == None:
            parent = self.cr.activeWorld.worldGrid

        messenger.send('islandPlayerBarrier', [
            0])
        if not hasattr(parent, 'getZoneFromXYZ'):
            self.acceptOnce(base.cr.getAllInterestsCompleteEvent(), localAvatar.b_setGameState, extraArgs = [
                'TeleportIn'])
            return
        teleportZone = parent.getZoneFromXYZ(teleportPosHpr[:3])
        localAvatar.reparentTo(parent)
        localAvatar.setPosHpr(*teleportPosHpr)
        localAvatar.spawnWiggle()
        localAvatar.b_setLocation(parent.getDoId(), teleportZone)
        parent.addObjectToGrid(localAvatar)
        parent.setPlayerBarrier(1)
        currParent = localAvatar.getParentObj()
        if isinstance(currParent, ZoneLOD.ZoneLOD):
            localAvatar.enterZoneLOD(currParent)

        parent.processVisibility(None)
        if base.cr._completeEventCount.num > 0:
            self.acceptOnce(base.cr.getAllInterestsCompleteEvent(), localAvatar.b_setGameState, extraArgs = [
                'TeleportIn'])
        else:
            localAvatar.b_setGameState('TeleportIn')

    def localTeleport(self, locationName=None, goNow=False, locationUid=None):
        if locationName and locationUid:
            locationName = None

        for currIsle in base.cr.doId2do.values():
            if not (hasattr(currIsle, 'getName') and hasattr(currIsle, 'getUniqueId')):
                continue
            if not hasattr(currIsle, 'getZoneFromXYZ'):
                continue
            if currIsle.getName() == locationName:
                break

            elif currIsle.getUniqueId() == locationUid:
                break

        else:
            self.notify.error('not found: (%s, %s)' % (locationName, locationUid))

        currInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currInteractive:
            currInteractive.requestExit()

        questStateSpawnIdx = QuestLadderDB.getPreferredAreaSpawnNode(currIsle.getUniqueId(), localAvatar)
        teleportPos = base.cr.activeWorld.getPlayerSpawnPt(currIsle.getDoId(), index = questStateSpawnIdx)
        if teleportPos == None:
            teleportPos = (0, 0, 0, 0, 0, 0)

        self.localTeleportEffect(teleportPos, currIsle, goNow=goNow)
        self.lastLocalTeleportLoc = currIsle.getDoId()

    def requestTeleportToFishingShip(self):
        print 'requestTeleportToFishingShip'
        self.cr.teleportMgr.sendUpdate('requestTeleportToFishingShip')


    def teleportToFishingShipResponse(self, shipId):
        print 'teleportToFishingShipResponse'
        print 'shipId=', shipId
        self.cr.teleportMgr.localTeleportToId(shipId, localAvatar, showLoadingScreen = False)


    def localTeleportToId(self, locationId, teleportingObj = None, destPos = None, callback = None, objectLocation = None, showLoadingScreen = True):
        if showLoadingScreen:
            self.cr.loadingScreen.show(waitForLocation = True)

        self.localTeleportId = locationId
        self.localTeleportingObj = teleportingObj
        self.localTeleportCallback = callback
        self.localTeleportDestPos = destPos
        destObj = self.cr.doId2do.get(locationId)
        if destObj:
            self._localTeleportToIdInterestComplete()
            self.notify.debug('destination object %s found, teleporting to there now' % locationId)
        elif objectLocation:
            self._localTeleportToIdResponse(objectLocation[0], objectLocation[1])
            self.notify.debug('destination object %s not found, but location %s given' % (locationId, objectLocation))
        else:
            self.sendUpdate('requestTargetsLocation', [
                int(locationId)])
            self.notify.debug('destination object %s not found, querying AI for its location' % locationId)

    def _localTeleportToIdResponse(self, objectId, parentId, zoneId):
        self.localTeleportId = objectId
        if parentId != 0 and zoneId != 0:
            if self.cr.doId2do.get(parentId):
                localAvatar.setInterest(parentId, zoneId, [
                    'localTeleportToId'], 'localTeleportToIdInterestAddComplete')
                self.acceptOnce('localTeleportToIdInterestAddComplete', self._localTeleportToIdInterestComplete)
                self.notify.debug('parent %s of destination object found, setting up interest' % parentId)
            else:
                self.notify.warning('parent %s of destination object not found, teleport failure' % parentId)
        else:
            self.failTeleport(parentId, zoneId)

    def failTeleport(self, parentId = None, zoneId = None, message = PLocalizer.TeleportToPlayerFailMessage):
        self.sendUpdate('requestClearPreventDamage')
        fallbackAreaId = localAvatar.getReturnLocation()
        if fallbackAreaId != '':
            areaDoId = base.cr.uidMgr.getDoId(fallbackAreaId)
            self.clearAmInTeleport()
            if areaDoId:
                destPos = base.cr.activeWorld.getPlayerSpawnPt(areaDoId)
                if destPos and self.localTeleportingObj:
                    self.localTeleportToId(areaDoId, self.localTeleportingObj, destPos)
                else:
                    self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld', doEffect = False)
            else:
                self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld', doEffect = False)
            self._DistributedTeleportMgr__createDialog(message)
        else:
            self.notify.warning("  teleport to object (%s %s) AND 'return location' %s failed" % (parentId, zoneId, fallbackAreaId))


    def _DistributedTeleportMgr__cleanupDialog(self, value = None):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None



    def _DistributedTeleportMgr__createDialog(self, message):
        if message:
            popupDialogText = message
            if self.popupDialog:
                self._DistributedTeleportMgr__cleanupDialog()

            self.popupDialog = PDialog.PDialog(text = popupDialogText, style = OTPDialog.Acknowledge, command = self._DistributedTeleportMgr__cleanupDialog)



    def _localTeleportToIdInterestComplete(self):
        teleportToObj = self.cr.doId2do.get(self.localTeleportId)
        if not teleportToObj:
            self.sendUpdate('requestTargetsLocation', [
                self.localTeleportId])
            return None

        curParent = localAvatar.getParentObj()
        parentIsZoneLOD = isinstance(curParent, ZoneLOD.ZoneLOD)
        if parentIsZoneLOD:
            localAvatar.leaveZoneLOD(curParent)

        try:
            isAShip = teleportToObj._isShip()
        except AttributeError:
            isAShip = False

        if isAShip:
            if not teleportToObj.isSailable():
                self.failTeleport(0, 0, PLocalizer.TeleportToGoneShipFailMessage)
                return None
            elif teleportToObj.gameFSM.getCurrentOrNextState() in ('InBoardingPosition', 'OtherShipBoarded'):
                self.failTeleport(0, 0, PLocalizer.TeleportToBoardingShipFailMessage)
                return None

            teleportToObj.setZoneLevel(3)
            teleportToObj.registerMainBuiltFunction(localAvatar.placeOnShip, [
                teleportToObj])
            teleportToObj.registerBuildCompleteFunction(teleportToObj.enableOnDeckInteractions)
            teleportToObj.registerBuildCompleteFunction(self._localTeleportToIdDone)
        else:
            self.__pendingGoNow.append(False)
            goNow = self.__pendingGoNow.pop(0)
            self.localTeleport(locationUid=teleportToObj.getUniqueId(), goNow=goNow)

    def _localTeleportToIdDone(self):
        self.cr.loadingScreen.scheduleHide(base.cr.getAllInterestsCompleteEvent())
        curParent = localAvatar.getParentObj()
        if isinstance(curParent, ZoneLOD.ZoneLOD):
            localAvatar.enterZoneLOD(curParent)

        if self.localTeleportCallback:
            self.localTeleportCallback()

        self.localTeleportId = None
        self.localTeleportingObj = None
        self.localTeleportCallback = None
        self.localTeleportDestPos = None
        localAvatar.guiMgr.socialPanel.updateAll()

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        messenger.send('destroyCrewMatchInvite')
        taskMgr.removeTasksMatching('teleportRemoveInterest')
        taskMgr.removeTasksMatching('teleportAddInterest')
        taskMgr.removeTasksMatching(self.uniqueName('localTeleportPos'))
        taskMgr.removeTasksMatching(self.uniqueName('fadeDone'))
        self.requestData = None
        self.ignoreAll()
        if base.cr.teleportMgr == self:
            base.cr.teleportMgr = None

        requestData = self.requestData
        self.requestData = None
        if self.teleportQueueProcess:
            taskMgr.remove(self.teleportQueueProcess)



    def requestTeleport(self, instanceType, instanceName, shardId = 0, locationUid = '', instanceDoId = 0, doneCallback = None, startedCallback = None, gameType = -1, friendDoId = 0, friendAreaDoId = 0, doEffect = True):
        self.requestData = ((instanceType, instanceName), {
            'shardId': shardId,
            'locationUid': locationUid,
            'instanceDoId': instanceDoId,
            'doneCallback': doneCallback,
            'startedCallback': startedCallback,
            'gameType': gameType,
            'friendDoId': friendDoId,
            'friendAreaDoId': friendAreaDoId,
            'doEffect': doEffect })
        localAvatar.confirmTeleport(self.teleportConfirmation, feedback = True)

    def teleportConfirmation(self, confirmed):
        if confirmed:
            requestData = self.requestData
            self.initiateTeleport(*requestData[0], **requestData[1])
            locationUid = requestData[1]['locationUid']
            base.cr.loadingScreen.showTarget(locationUid)
            base.cr.loadingScreen.showHint(locationUid)

        self.requestData = None


    def requestTeleportToAvatar(self, shardId, instanceDoId, avatarId, avatarParentId):
        self.requestTeleport(PiratesGlobals.INSTANCE_MAIN, '', shardId, '', instanceDoId, friendDoId = avatarId, friendAreaDoId = avatarParentId)

    def teleportToObjectResp(self, shardId, instanceId, objId, parentId):
        self.requestTeleport(PiratesGlobals.INSTANCE_MAIN, '', shardId, '', instanceId, friendDoId = objId, friendAreaDoId = parentId)


    def requestTeleportToShip(self, shardId, instanceDoId, shipId):
        self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, '', shardId, '', instanceDoId, friendDoId = 0, friendAreaDoId = shipId)


    def requestTeleportToIsland(self, islandUid):

        def teleportConfirmation(confirmed, islandUid = islandUid):
            self.islandTeleportConfirmation(confirmed, islandUid)

        localAvatar.setTeleportFlag(PiratesGlobals.TFNoIslandToken, localAvatar.confirmIslandTokenTeleport, [
            islandUid])
        localAvatar.setTeleportFlag(PiratesGlobals.TFSameArea, localAvatar.confirmNotSameAreaTeleport, [
            islandUid])
        localAvatar.confirmTeleport(teleportConfirmation, feedback = True)
        localAvatar.clearTeleportFlag(PiratesGlobals.TFNoIslandToken)
        localAvatar.clearTeleportFlag(PiratesGlobals.TFSameArea)

    def islandTeleportConfirmation(self, confirmed, islandUid):
        if confirmed:
            islandDoId = self.cr.uidMgr.getDoId(islandUid)
            island = self.cr.getDo(islandDoId)
            if island and island.getParentObj() is self.cr.activeWorld:
                self.localTeleport(locationName = island.getName())
            else:
                self.sendUpdate('requestTeleportToIsland', [
                    islandUid])
            base.cr.loadingScreen.showTarget(islandUid)
            base.cr.loadingScreen.showHint(islandUid)

    def teleportToIslandResponse(self, instanceDoId, islandDoId):
        if instanceDoId and islandDoId:
            self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, '', self.cr.distributedDistrict.doId, '', instanceDoId, friendAreaDoId = islandDoId)

    def stowawayTeleportResponse(self, instanceDoId, islandDoId):
        if instanceDoId and islandDoId:
            self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, '', self.cr.distributedDistrict.doId, '', instanceDoId, friendAreaDoId = islandDoId, doEffect = False, stowawayEffect = True)
            base.cr.loadingScreen.showTarget(base.cr.doId2do[islandDoId].getUniqueId())

    def queryAvatarForTeleport(self, avId):
        self.setTeleportQueryId(avId)

        def teleportConfirmation(confirmed, avId = avId):
            if confirmed:
                handle = self.cr.identifyAvatar(avId)
                if handle:
                    shardId = self.cr.distributedDistrict.doId
                    if not localAvatar.getBandId():
                        pass
                    (bandMgr, bandId) = (0, 0)
                    guildId = localAvatar.getGuildId()
                    handle.sendTeleportQuery(avId, bandMgr, bandId, guildId, shardId)

        localAvatar.confirmTeleport(teleportConfirmation, feedback = True)

    def handleAvatarTeleportQuery(self, requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId):
        handle = self.cr.identifyAvatar(requesterId)
        if not handle:
            return None

        if self.cr.identifyFriend(requesterId):
            if base.localAvatar.isIgnored(requesterId):
                handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(PiratesGlobals.TFIgnore), 0, 0, 0, sendToId = requesterId)
                return None

        avName = handle.getName()

        def confirmed(canTeleportTo, avId, failedFlag, avName = avName):
            if canTeleportTo:
                if self.cr.getActiveWorld() and self.cr.distributedDistrict and localAvatar.getParentObj():
                    handle.sendTeleportResponse(PiratesGlobals.TAAvailable, self.cr.distributedDistrict.doId, self.cr.getActiveWorld().doId, localAvatar.getParentObj().doId, sendToId = requesterId)
                else:
                    handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(PiratesGlobals.TFUnavailable), 0, 0, 0, sendToId = requesterId)
            elif localAvatar.failedTeleportMessageOk(requesterId):
                localAvatar.setSystemMessage(requesterId, OTPLocalizer.WhisperFailedVisit % avName)

            handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(failedFlag), 0, 0, 0, sendToId = requesterId)

        localAvatar.confirmTeleportTo(confirmed, requesterId, avName, requesterBandMgrId, requesterBandId, requesterGuildId)

    def handleAvatarTeleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
        if not avId == self.teleportQueryId:
            self.clearTeleportQueryId()
            return None

        self.clearTeleportQueryId()
        handle = self.cr.identifyAvatar(avId)
        if handle:
            avName = handle.getName()
        else:
            return None
        if available == PiratesGlobals.TAAvailable:

            def teleportConfirmation(confirmed, shardId = shardId, instanceDoID = instanceDoId, avId = avId, avatarParentId = areaDoId):
                if confirmed:
                    self.requestTeleportToAvatar(shardId, instanceDoId, avatarId = avId, avatarParentId = areaDoId)

            localAvatar.setTeleportFlag(PiratesGlobals.TFSameArea, localAvatar.confirmNotSameAreaTeleportToPlayer, [
                areaDoId])
            localAvatar.confirmTeleport(teleportConfirmation, feedback = True)
            localAvatar.clearTeleportFlag(PiratesGlobals.TFSameArea)
        else:
            flag = PiratesGlobals.decodeTeleportFlag(available)
            if flag == PiratesGlobals.TAIgnore:
                pass
            1
            if flag in PiratesGlobals.TFNoTeleportToReasons:
                localAvatar.guiMgr.createWarning(PiratesGlobals.TFNoTeleportToReasons[flag] % avName, duration = 10)

    def initiateTeleport(self, instanceType, instanceName, shardId = 0, locationUid = '', instanceDoId = 0, doneCallback = None, startedCallback = None, gameType = -1, friendDoId = 0, friendAreaDoId = 0, doEffect = True, queue = False, stowawayEffect = False):
        currInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currInteractive:
            currInteractive.requestExit()

        if self.cr.activeWorld:
            fromInstanceType = self.cr.activeWorld.getType()
        else:
            fromInstanceType = PiratesGlobals.INSTANCE_NONE
        if instanceType not in [
            PiratesGlobals.INSTANCE_MAIN,
            PiratesGlobals.INSTANCE_WELCOME] and fromInstanceType not in [
            PiratesGlobals.INSTANCE_MAIN,
            PiratesGlobals.INSTANCE_GENERIC,
            PiratesGlobals.INSTANCE_NONE]:
            if not config.GetBool('can-break-teleport-rules', 0):
                import pdb as pdb
                pdb.set_trace()
                return None

        if self.amInTeleport() and not stowawayEffect:
            if queue:
                self.queueInitiateTeleport(instanceType, instanceName, shardId, locationUid, instanceDoId, doneCallback, startedCallback, gameType, friendDoId, friendAreaDoId, doEffect, stowawayEffect)
                return None

            return None

        self.setAmInTeleport()
        if instanceType == PiratesGlobals.INSTANCE_MAIN and not locationUid:
            locationUid = localAvatar.returnLocation

        localAvatar.teleportFriendDoId = friendDoId
        self.doEffect = doEffect
        self.stowawayEffect = stowawayEffect
        self.sendUpdate('initiateTeleport', [
            instanceType,
            fromInstanceType,
            shardId,
            locationUid,
            instanceDoId,
            instanceName,
            gameType,
            friendDoId,
            friendAreaDoId])
        self.doneCallback = doneCallback
        self.startedCallback = startedCallback
        self.teleportInit(instanceType, fromInstanceType, instanceName)

    def queueInitiateTeleport(self, instanceType, instanceName, shardId = 0, locationUid = '', instanceDoId = 0, doneCallback = None, startedCallback = None, gameType = -1, friendDoId = 0, friendAreaDoId = 0, doEffect = True, stowawayEffect = False):
        teleInfo = [
            instanceType,
            instanceName,
            shardId,
            locationUid,
            instanceDoId,
            doneCallback,
            startedCallback,
            gameType,
            friendDoId,
            friendAreaDoId,
            doEffect,
            stowawayEffect]
        self.teleportQueue.append(teleInfo)

        def processTeleportQueue(task = None):
            if self.amInTeleport():
                return Task.again

            if not self.teleportQueue:
                return Task.done

            teleportInfo = self.teleportQueue.pop(0)
            self.initiateTeleport(*teleportInfo)
            if self.teleportQueue:
                return Task.again

            return Task.done

        self.teleportQueueProcess = taskMgr.doMethodLater(1, processTeleportQueue, 'processTeleportQueue')


    def amInTeleport(self):
        return localAvatar.testTeleportFlag(PiratesGlobals.TFInTeleport) and not config.GetBool('can-ignore-teleport-flags', 0)


    def setAmInTeleport(self):
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFInTeleport)
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFLookoutJoined)


    def clearAmInTeleport(self):
        localAvatar.clearTeleportFlag(PiratesGlobals.TFInInitTeleport)
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInTeleport)


    def setTeleportQueryId(self, avId):
        self.teleportQueryId = avId

    def clearTeleportQueryId(self):
        self.teleportQueryId = 0

    def initiateTeleportAI(self, instanceType, instanceName):
        self.teleportInit(instanceType, instanceName)

    def teleportInit(self, instanceType, fromInstanceType, instanceName, gameType = None):
        self.clearTeleportQueryId()
        self.oldWorld = base.cr.activeWorld
        self.instanceType = instanceType
        self.fromInstanceType = fromInstanceType
        self.instanceName = instanceName
        self.gameType = gameType

    def teleportHasBegun(self, instanceType, fromInstanceType, instanceName, gameType):
        if self.startedCallback:
            self.startedCallback()
            self.startedCallback = None

        if self.oldWorld == None or self.oldWorld.isEmpty():
            self.teleportInit(instanceType, fromInstanceType, instanceName, gameType)

    def getRemoveInterestEventName(self):
        return self.uniqueName('teleportRemoveInterest')


    def getAddInterestEventName(self):
        return self.uniqueName('teleportAddInterest')


    def forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        self.setAmInTeleport()
        localAvatar.guiMgr.request('Cutscene')
        if not base.transitions.fadeOutActive():
            base.transitions.fadeOut()

        if self.fromInstanceType == PiratesGlobals.INSTANCE_MAIN:
            self.inInstanceType = PiratesGlobals.INSTANCE_MAIN
        else:
            self.inInstanceType = self.instanceType
        if self.fromInstanceType == PiratesGlobals.INSTANCE_PVP:
            localAvatar.clearTeleportFlag(PiratesGlobals.TFInPVP)
        elif self.fromInstanceType == PiratesGlobals.INSTANCE_TUTORIAL:
            localAvatar.clearTeleportFlag(PiratesGlobals.TFInTutorial)


        def fadeDone():
            base.cr.loadingScreen.show()
            curParent = localAvatar.getParentObj()
            parentIsZoneLOD = isinstance(curParent, ZoneLOD.ZoneLOD)
            if parentIsZoneLOD:
                localAvatar.leaveZoneLOD(curParent)
                curParent.turnOff()

            if self.cr.doId2do.get(tzParent) == None:
                self.failTeleport(None, None, PLocalizer.TeleportGenericFailMessage)
            else:
                self.teleportAddInterestTZ(instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone)

        localAvatar.guiMgr.request('Interactive')
        taskMgr.removeTasksMatching(self.uniqueName('fadeDone'))
        taskMgr.doMethodLater(1, fadeDone, self.uniqueName('fadeDone'), extraArgs = [])

    def teleportAddInterestTZ(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        addEvent = self.getAddInterestEventName()
        self.accept(addEvent, self.teleportAddInterestCompleteTZ, extraArgs = [
            tzDoId,
            thDoId,
            worldGridDoId])
        localAvatar.setInterest(tzParent, tzZone, [
            'TZInterest'], addEvent)
        self.instanceName = instanceName


    def teleportAddInterestCompleteTZ(self, tzDoId, thDoId, worldGridDoId):
        base.cr.relatedObjectMgr.requestObjects([
            tzDoId], eachCallback = lambda param1, param2 = thDoId: self.teleportZoneExists(param1, param2))

    def teleportZoneExists(self, teleportZone, thDoId):
        base.cr.relatedObjectMgr.requestObjects([
            thDoId], eachCallback = lambda param1, param2 = teleportZone: self.teleportHandlerExists(param1, param2))

    def teleportHandlerExists(self, teleportHandler, teleportZone):
        teleportHandler.instanceName = self.instanceName
        teleportHandler.instanceType = self.instanceType
        teleportHandler.doneCallback = self.doneCallback
        self.doneCallback = None
        teleportHandler.oldWorld = self.oldWorld
        self.oldWorld = None
        teleportHandler.startTeleport()

    def localAvTeleportFinishedRequest(self, task = None):
        if not self.amInTeleport():
            messenger.send('localAvTeleportFinished')

    def createSpawnInterests(self, parents, callback, destGrid, teleportingObj):
        parentsLen = len(parents)

        if parentsLen == 0:
            callback(destGrid, teleportingObj)
        else:
            parentObj = base.cr.doId2do.get(parents[0])
            if parentObj:
                callback(parentObj, teleportingObj)
            elif parentsLen > 2 and parents[2] in base.cr.doId2do:
                base.cr.relatedObjectMgr.requestObjects([
                    parents[0]], eachCallback = lambda param1 = None, param2 = teleportingObj: callback(param1, param2))
                localAvatar.setInterest(parents[2], parents[1], [
                    'instanceInterest'])
            elif parentsLen > 2:
                parentParentId = parents[2]
                parentParentZone = parents[1]
            else:
                parentParentId = '<None Given>'
                parentParentZone = '<None Given>'
            parentId = parents[0]
            self.notify.warning(('createSpawnInterests: parent %s of parent %s in zone %s ' + 'does not exist locally, aborting teleport') % (parentParentId, parentId, parentParentZone))
            self.failTeleport(None, None, PLocalizer.TeleportGenericFailMessage)

    def initiateCrossShardDeploy(self, shardId = 0, islandUid = '', shipId = 0, doneCallback = None, startedCallback = None, doEffect = True):
        if not islandUid or not shipId:
            return None

        currInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currInteractive:
            currInteractive.requestExit()

        if self.cr.activeWorld:
            fromInstanceType = self.cr.activeWorld.getType()
        else:
            fromInstanceType = PiratesGlobals.INSTANCE_NONE
        if self.amInTeleport():
            return None

        self.setAmInTeleport()
        self.doEffect = doEffect
        self.sendUpdate('requestCrossShardDeploy', [
            shardId,
            islandUid,
            shipId])
        self.doneCallback = doneCallback
        self.startedCallback = startedCallback
        self.teleportInit(PiratesGlobals.INSTANCE_MAIN, fromInstanceType, 'Main World')


    def notifyFriendVisit(self, avId):
        av = base.cr.identifyAvatar(avId)
        if av:
            avName = av.getName()
        else:
            avName = PLocalizer.Someone
        localAvatar.setSystemMessage(avId, OTPLocalizer.WhisperComingToVisit % avName)
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.WhisperComingToVisit % avName, icon = ('friends', None))
