from panda3d.core import lookAt
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world import GridAreaBuilder
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
import DistributedGAConnector

class DistributedGATunnel(DistributedGAConnector.DistributedGAConnector):
    notify = directNotify.newCategory('DistributedGATunnel')

    def __init__(self, cr):
        DistributedGAConnector.DistributedGAConnector.__init__(self, cr, 'DistributedGATunnel')
        self.builder = GridAreaBuilder.GridAreaBuilder(self)
        self.loadSphere = [
            None,
            None]
        self.unloadSphere = None
        self.connectorNodes = [
            'portal_connector_1',
            'portal_connector_2']
        self.ambientNames = [
            None,
            None]
        self.avatarZoneContext = None
        self.floorIndex = -1
        self.lastFloor = -1
        self.lastFloorTime = 0
        self.loadedAreaDoId = 0
        self.floorNames = []
        self.quickLoadActive = False

    def generate(self):
        DistributedGAConnector.DistributedGAConnector.generate(self)
        self._DistributedGATunnel__startProcessVisibility()

    def announceGenerate(self):
        DistributedGAConnector.DistributedGAConnector.announceGenerate(self)

    def disable(self):
        DistributedGAConnector.DistributedGAConnector.disable(self)

    def delete(self):
        self._DistributedGATunnel__stopProcessVisibility()

        for sphere in self.loadSphere:
            if sphere:
                sphere.remove_node()
                continue

        del self.loadSphere
        self.fadeoutAllAmbient()
        DistributedGAConnector.DistributedGAConnector.delete(self)
        self.builder.delete()

    def loadModel(self):
        DistributedGAConnector.DistributedGAConnector.loadModel(self)

    def _DistributedGATunnel__startProcessVisibility(self):
        if not (self.avatarZoneContext) and self.isGenerated():
            self.avatarZoneContext = self.cr.addInterest(self.getDoId(), 500, self.uniqueName('visibility'))

    def _DistributedGATunnel__stopProcessVisibility(self):
        if self.avatarZoneContext:
            self.cr.removeInterest(self.avatarZoneContext)
            self.avatarZoneContext = None

    def setupCollisions(self):
        if self.floorNames == []:
            self.floorNames = [
                'collision_floor_1',
                'collision_floor_2',
                'collision_floor_middle']

        floors = []
        for i in xrange(len(self.floorNames)):
            floorName = self.floorNames[i]
            floor = self.find('**/' + floorName)
            uniqueFloorName = self.uniqueName(floorName)
            floor.setName(uniqueFloorName)
            self.floorNames[i] = uniqueFloorName
            self.accept('enterFloor' + uniqueFloorName, self._DistributedGATunnel__handleOnFloor, extraArgs = [
                i])

    def unloadWorldFinished(self, areaDoId):
        DistributedGAConnector.DistributedGAConnector.unloadWorldFinished(self, areaDoId)
        self.loadArea(self.floorIndex, False)

    def fadeOutAmbient(self, index):
        if self.ambientNames[index]:
            base.ambientMgr.requestFadeOut(self.ambientNames[index], duration = 0.01)

        if self.ambientNames[1 - index]:
            base.ambientMgr.requestChangeVolume(self.ambientNames[1 - index], duration = 0, finalVolume = 0)

    def fadeInAmbient(self, index):
        if self.ambientNames[index]:
            base.ambientMgr.requestChangeVolume(self.ambientNames[index], duration = 0.1, finalVolume = PiratesGlobals.DEFAULT_AMBIENT_VOLUME_NEAR)

    def __handleOnFloor(self, areaIndex, collEntry):
        if (not collEntry or areaIndex in (0, 1)) and not localAvatar.testTeleportFlag(PiratesGlobals.TFInTunnel):

            def enterTunnelFinished():
                if localAvatar.getGameState() in ('EnterTunnel', 'Off', 'Dialog', 'Cutscene', 'LandRoam'):
                    localAvatar.b_setLocation(self.doId, 500)
                    self.floorIndex = 1 - areaIndex
                    self.unloadLoadedArea()
                    if localAvatar.gameFSM.preTunnelState:
                        localAvatar.b_setGameState(localAvatar.gameFSM.preTunnelState)
                    else:
                        localAvatar.b_setGameState('LandRoam')

            if collEntry != None:
                area = self.getLoadedArea()
                if not area:
                    self.notify.warning('***JCW*** No loaded area in GATunnel: %s' % self.getUniqueId())
                    self.notify.warning('***JCW*** Areas: %s, %s' % (self.areaUid[0], self.areaUid[1]))
                    self.notify.warning('***JCW*** Ignoring __handleOnFloor(%s) event' % areaIndex)
                    return None

                entranceNode = self.areaNode[areaIndex]
                entryLocator = area.find('**/' + entranceNode + '*')
                if entryLocator.isEmpty():
                    return None

                camera.wrtReparentTo(render)
                localAvatar.lookAt(entryLocator, -50, 0, localAvatar.getZ(entryLocator))
                camera.wrtReparentTo(localAvatar)
                self.acceptOnce('EnterTunnelFinished', enterTunnelFinished)
                localAvatar.gameFSM.preTunnelState = localAvatar.getGameState()
                localAvatar.b_setGameState('EnterTunnel')
            else:
                base.transitions.fadeOut(0.75, Func(enterTunnelFinished))
            localAvatar.motionFSM.off()
            localAvatar.b_setTeleportFlag(PiratesGlobals.TFInTunnel)

    def loadAreaFinished(self, area, autoFadeIn = True):

        def leaveTunnel():
            areaIndex = self.getAreaIndex(area)
            entranceNode = self.areaNode[areaIndex]
            entryLocator = area.find('**/' + entranceNode + '*')
            localAvatar.reparentTo(entryLocator)
            localAvatar.setPos(0, 0, 0)
            if not autoFadeIn:
                if localAvatar.style.tutorial == PiratesGlobals.TUT_KILLED_1_SKELETON:
                    localAvatar.setX(30)
                    localAvatar.setH(90)

            else:
                localAvatar.setH(-90)
            localAvatar.wrtReparentTo(area)
            if autoFadeIn:

                def leaveTunnelFinished():
                    localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInTunnel)
                    if localAvatar.gameFSM.preTunnelState:
                        localAvatar.b_setGameState(localAvatar.gameFSM.preTunnelState)
                        if localAvatar.gameFSM.preTunnelState == 'Battle':
                            localAvatar.guiMgr.combatTray.toggleWeapon(localAvatar.currentWeaponId, localAvatar.currentWeaponSlotId)

                    else:
                        localAvatar.b_setGameState('LandRoam')

                self.acceptOnce('LeaveTunnelFinished', leaveTunnelFinished)
                base.localAvatar.b_setGameState('LeaveTunnel')
            else:
                self.sendUpdate('sendLeaveTunnelDone')
            self.fadeInAmbient(self.floorIndex)

        base.cr.setAllInterestsCompleteCallback(leaveTunnel)
        transform = localAvatar.getTransform(self)
        DistributedGAConnector.DistributedGAConnector.loadAreaFinished(self, area, autoFadeIn)
        self.lastFloorTime = globalClock.getFrameTime()
        self.loadedAreaDoId = area.doId
        localAvatar.setTransform(self, transform)
        localAvatar.wrtReparentTo(area)
        area.handleEnterGameArea(None)

    def handleChildArrive(self, childObj, zoneId):
        DistributedGAConnector.DistributedGAConnector.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal():
            childObj.wrtReparentTo(self)

    def handleChildLeave(self, childObj, zoneId):
        DistributedGAConnector.DistributedGAConnector.handleChildLeave(self, childObj, zoneId)

    def fadeoutAllAmbient(self):
        if self.lastFloor >= 0:
            for ambientName in self.ambientNames:
                if ambientName:
                    base.ambientMgr.requestFadeOut(ambientName)
                    continue

    def setLinks(self, exteriorUid, links):
        DistributedGAConnector.DistributedGAConnector.setLinks(self, exteriorUid, links)
        self.calcAmbientNames()

    def calcOneAmbientName(self, area):
        retval = None
        if area:
            parts = area.split('_')
            retval = SoundGlobals.getAmbientFromStr(parts[-1])

        return retval

    def calcAmbientNames(self):
        for i in xrange(2):
            area = self.areaNode[i]
            ambientName = self.calcOneAmbientName(area)
            self.ambientNames[i] = ambientName

        if not self.ambientNames[0] and not self.ambientNames[1]:
            self.ambientNames[1] = SoundGlobals.getAmbientFromStr(self.modelPath)
            self.notify.debug('Assuming self.ambientNames[1] = %s' % self.ambientNames[1])

    def quickLoadOtherSide(self):
        base.cr.loadingScreen.show(waitForLocation = True)
        if self.floorIndex != -1:
            self._DistributedGATunnel__handleOnFloor(self.floorIndex, None)

    def turnOn(self):
        DistributedGAConnector.DistributedGAConnector.turnOn(self)
        self._DistributedGATunnel__startProcessVisibility()

    def turnOff(self):
        self._DistributedGATunnel__stopProcessVisibility()
        DistributedGAConnector.DistributedGAConnector.turnOff(self)

    def isGridParent(self):
        return 0
