from panda3d.core import LODNode, NodePath, TransparencyAttrib, Vec3, Vec4, headsUp
import math
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class DistributedBuriedTreasure(DistributedInteractive.DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasure')
    UpdateDelay = 1.0

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedBuriedTreasure')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.showTreasureIval = None
        self.raiseTreasureIval = None
        self.currentDepth = 0.0
        self.startingDepth = 0.0
        self.visZone = ''
        self.orientation = 0.0
        self.chest = None
        self.spotRoot = None
        self.spot = None


    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        self.setInteractOptions(proximityText = PLocalizer.InteractBuriedTreasure, sphereScale = 10, diskRadius = 10, exclusive = 0)


    def announceGenerate(self):
        if not self.spot:
            self.spot = loader.loadModel('models/effects/pir_m_efx_msc_digSpot')
            self.spot.hide(OTPRender.MainCameraBitmask)
            self.spot.showThrough(OTPRender.EnviroCameraBitmask)
            self.spot.setTransparency(TransparencyAttrib.MAlpha)
            self.spot.setColorScale(0.8, 0.9, 0.8, 0.35)
            self.spot.setBin('shadow', -10)
            self.spot.setDepthTest(0)
            self.spot.setScale(50)
            self.spotRoot = self.attachNewNode('geomRoot')
            lod = LODNode('treeLOD')
            lodNP = self.spotRoot.attachNewNode(lod)
            self.spot.reparentTo(lodNP)
            lod.addSwitch(100, 0)

        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.getParentObj().builder.addSectionObj(self, self.visZone)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        if self.chest:
            self.chest.remove_node()
            self.chest = None

        if self.showTreasureIval:
            self.showTreasureIval.pause()
            self.showTreasureIval = None

        if self.raiseTreasureIval:
            self.raiseTreasureIval.pause()
            self.raiseTreasureIval = None

        if self.spot:
            self.spot.remove_node()
            self.spot = None

        if self.spotRoot:
            self.spotRoot.remove_node()
            self.spotRoot = None

        if self.getParentObj():
            self.getParentObj().builder.removeSectionObj(self, self.visZone)


    def loadChest(self):
        if self.chest:
            return None

        self.chest = loader.loadModel('models/props/treasureChest')
        self.chest.findAllMatches('**/pile_group').stash()
        self.chest.setH(self.orientation)
        self.chest.reparentTo(self)
        self.chest.setScale(0.8)
        self.dirt = loader.loadModel('models/props/dirt_pile')
        self.dirt.setH(self.orientation)
        self.dirt.reparentTo(self)
        self.dirt.flattenStrong()


    def handleEnterProximity(self, collEntry):
        DistributedInteractive.DistributedInteractive.handleEnterProximity(self, collEntry)


    def handleExitProximity(self, collEntry):
        DistributedInteractive.DistributedInteractive.handleExitProximity(self, collEntry)


    def requestInteraction(self, avId, interactType = 0):
        localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)


    def rejectInteraction(self):
        localAvatar.guiMgr.createWarning(PLocalizer.AlreadySearched)
        localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)


    def startDigging(self):
        if self.currentDepth == self.startingDepth:
            self.orientation = localAvatar.getH()

        self.acceptInteraction()
        localAvatar.b_setGameState('Digging')
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractDigging)
        localAvatar.guiMgr.workMeter.startTimer(self.startingDepth, self.currentDepth)
        pos = localAvatar.getPos(self)
        angle = math.atan2(pos[0], pos[1])
        radius = 5
        localAvatar.setPos(self, math.sin(angle) * radius, math.cos(angle) * radius, 0)
        localAvatar.headsUp(self)
        localAvatar.setH(localAvatar, -90)


    def stopDigging(self, questProgress):
        localAvatar.guiMgr.workMeter.stopTimer()
        localAvatar.guiMgr.showQuestProgress(questProgress)
        if localAvatar.gameFSM.state == 'Digging':
            if localAvatar.lootCarried > 0:
                localAvatar.b_setGameState('LandTreasureRoam')
            else:
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)



    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        self.stopDigging(0)


    def enterWaiting(self):
        DistributedInteractive.DistributedInteractive.enterWaiting(self)


    def exitWaiting(self):
        DistributedInteractive.DistributedInteractive.exitWaiting(self)


    def enterUse(self):
        DistributedInteractive.DistributedInteractive.enterUse(self)


    def exitUse(self):
        DistributedInteractive.DistributedInteractive.exitUse(self)


    def setStartingDepth(self, depth):
        self.startingDepth = depth


    def setCurrentDepth(self, depth):
        oldZ = (self.currentDepth / float(self.startingDepth)) * -2.6
        self.currentDepth = depth
        z = (self.currentDepth / float(self.startingDepth)) * -2.6
        dirtZ = min(z + 0.5, -1.5)
        dirtOldZ = min(oldZ + 0.5, -1.5)
        if self.currentDepth == self.startingDepth:
            if self.chest:
                self.chest.stash()
                self.dirt.stash()
                self.chest.setZ(z)
                self.dirt.setZ(z * 1.5)

        else:
            self.loadChest()
            self.chest.unstash()
            self.dirt.unstash()
            if self.raiseTreasureIval:
                self.raiseTreasureIval.pause()

            self.chest.setPos(Vec3(0, 0, oldZ))
            self.dirt.setPos(Vec3(0, 0, dirtOldZ))
            self.raiseTreasureIval = Sequence(Wait(0.5), Parallel(LerpPosInterval(self.chest, self.UpdateDelay, Vec3(0, 0, z)), LerpPosInterval(self.dirt, self.UpdateDelay, Vec3(0, 0, dirtZ))))
            self.raiseTreasureIval.start()
            if self.state == 'Use':
                localAvatar.guiMgr.workMeter.startTimer(self.startingDepth, self.currentDepth)



    def showTreasure(self, gold):
        self.loadChest()
        self.showTreasureIval = Sequence(Wait(4.0), Func(self.setTransparency, 1), LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 0)), Func(self.chest.stash))
        self.showTreasureIval.start()


    def setVisZone(self, zone):
        self.visZone = zone


    def getVisZone(self):
        return self.visZone
