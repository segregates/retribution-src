from panda3d.core import AlphaTestAttrib, CollideMask, CollisionInvSphere, CollisionNode, FadeLODNode, Fog, LODNode, Light, NodePath, RenderAttrib, TextNode, Texture, TextureStage, VBase4, Vec3, Vec4
import random
import re
import imp
from direct.actor import *
from direct.distributed import DistributedCartesianGrid
from direct.task import Task
from direct.showbase.PythonUtil import report
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DGG
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from pirates.ai import HolidayGlobals
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.LanternGlow import LanternGlow
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.VolcanoEffect import VolcanoEffect
from pirates.effects.FeastFire import FeastFire
from pirates.effects import FireworkGlobals
from pirates.effects.FireworkShow import FireworkShow
from pirates.world import ZoneLOD
from pirates.world import WorldGlobals
from pirates.world import DistributedGameArea
from pirates.world.LocationConstants import LocationIds
from pirates.distributed import DistributedInteractive
from pirates.piratesgui import PiratesGuiGlobals, RadarGui
from pirates.seapatch.Water import IslandWaterParameters
from pirates.swamp.Swamp import Swamp
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.seapatch.Reflection import Reflection
from pirates.piratesbase import TODGlobals
from pirates.pvp import PVPGlobals
from pirates.map.Minimap import IslandMap
from pirates.map.Mappable import MappableGrid
from direct.gui import DirectGuiGlobals
from pirates.battle.Teamable import Teamable

class DistributedIsland(DistributedGameArea.DistributedGameArea, DistributedCartesianGrid.DistributedCartesianGrid, ZoneLOD.ZoneLOD, Teamable, MappableGrid):
    SiegeIcon = None
    notify = directNotify.newCategory('DistributedIsland')

    def __init__(self, cr):
        DistributedGameArea.DistributedGameArea.__init__(self, cr)
        DistributedCartesianGrid.DistributedCartesianGrid.__init__(self, cr)
        Teamable.__init__(self)
        MappableGrid.__init__(self)
        self.islandShoreWave = None
        self.islandObjectsLoaded = False
        self.animControls = None
        self.sphereRadii = [
            1000,
            2000,
            3000,
            100000]
        self.sphereCenter = [
            0,
            0]
        ZoneLOD.ZoneLOD.__init__(self, self.uniqueName)
        self.parentWorld = None
        self.gridSphere = None
        self.nameText = None
        self.nameNode = None
        self.geom = None
        self.dockingLOD = None
        self.dockingLodFog = None
        self.dockingChar = None
        self.playerBarrierNP = None
        self.islandLowLod = None
        self.islandLowLodFog = None
        self.fogTransitionIval = None
        self.gold = 0
        self.islandTunnel = []
        self.hasTunnelsOnRadar = False
        self.name = 'Island Name'
        self.volcanoEffect = None
        self.feastFireEnabled = False
        self.feastFireEffect = None
        self.fireworkShowEnabled = False
        self.fireworkShowLegal = False
        self.fireworkShowType = 0
        self.fireworkShow = None
        self.islandMapModelPath = None
        self.mapName = None
        self.objsCached = False
        self.oceanVisEnabled = config.GetBool('ocean-visibility', False)
        self.flatShipsOnIsland = config.GetBool('flat-ships-on-island', True)
        self.locationSphereName = ''
        self.SiegeIcons = []
        if not DistributedIsland.SiegeIcon:
            logos = loader.loadModel('models/textureCards/sailLogo')
            if logos:
                DistributedIsland.SiegeIcon = [
                    logos.find('**/logo_french_flag'),
                    logos.find('**/logo_spanish_flag')]

    def announceGenerate(self):
        DistributedGameArea.DistributedGameArea.announceGenerate(self)
        DistributedCartesianGrid.DistributedCartesianGrid.announceGenerate(self)
        self.accept('docked', self.resetZoneLODs)
        self.loadDockingLOD()
        self.loadIslandLowLod()
        detailLevel = base.options.terrain_detail_level
        sailingLOD = FadeLODNode('sailingLOD')
        sailingLOD.setFadeTime(2)
        if detailLevel == 0:
            sailingLOD.addSwitch(5000, 0)
            sailingLOD.addSwitch(100000, 5000)
        elif detailLevel == 1:
            sailingLOD.addSwitch(10000, 0)
            sailingLOD.addSwitch(100000, 10000)
        elif detailLevel == 2:
            sailingLOD.addSwitch(20000, 0)
            sailingLOD.addSwitch(100000, 20000)

        self.sailingLOD = self.attachNewNode(sailingLOD)
        if self.dockingLOD:
            self.dockingLOD.reparentTo(self.sailingLOD)
            self.islandLowLod.reparentTo(self.sailingLOD)
        else:
            self.islandLowLod.reparentTo(self.sailingLOD)
            self.islandLowLod.copyTo(self.sailingLOD)
        self.loadWaterRing()
        gridSphereName = self.uniqueName('GridSphere')
        self.gridSphereEnterEvent = 'enter' + gridSphereName
        self.gridSphereExitEvent = 'exit' + gridSphereName
        self.setLodCollideMask(self.getLodCollideMask() | PiratesGlobals.ShipCollideBitmask)
        self.setZoneRadii(self.sphereRadii, self.sphereCenter)
        islandLOD = FadeLODNode('islandLOD')
        islandLOD.addSwitch(10000, 0)
        islandLOD.addSwitch(20000, 10000)
        islandLOD.setFadeTime(0.5)
        lodnp = NodePath(islandLOD)
        lodnp.reparentTo(self.builder.areaGeometry)
        lodnp.showThrough(OTPRender.ReflectionCameraBitmask)
        self.geomLOD = lodnp
        self.highDetail = lodnp.attachNewNode('highDetail')
        self.lowDetail = lodnp.attachNewNode('lowDetail')
        self.parentWorld.islands[self.doId] = self
        self.initializeNameText()
        self.setName(self.name)
        self.placeOnMap()
        self.accept('timeOfDayChange', self.timeOfDayChanged)

    def disable(self):
        self.turnOff()
        self.unloadIslandLowLod()
        self.unloadDockingLOD()
        self.sailingLOD.detachNode()
        self.sailingLOD = None
        self.unloadWaterRing()
        self.removeFromMap()
        self.stopCustomEffects()
        if self.fogTransitionIval:
            self.fogTransitionIval.pause()
            self.fogTransitionIval = None

        ZoneLOD.ZoneLOD.cleanup(self)
        DistributedGameArea.DistributedGameArea.disable(self)
        DistributedCartesianGrid.DistributedCartesianGrid.disable(self)
        self.deleteZoneCollisions()
        
        try:
            self.parentWorld.islands.pop(self.doId, None)
        except:
            pass

        self.parentWorld = None
        self.deleteNameText()
        self.ignoreAll()

    def delete(self):
        DistributedGameArea.DistributedGameArea.delete(self)
        DistributedCartesianGrid.DistributedCartesianGrid.delete(self)
        ZoneLOD.ZoneLOD.delete(self)
        self.unloadPlayerBarrier()
        self.remove_node()
        self.ignoreAll()
        while len(self.SiegeIcons):
            icon = self.SiegeIcons.pop()
            icon.remove_node()
            icon = None

    def turnOff(self, cache = False):
        self.stopCustomEffects()
        if not cache:
            self.setZoneLevelOuter()

        localAvatar.clearInterestNamed(None, [
            'IslandLocal'])
        DistributedGameArea.DistributedGameArea.turnOff(self)
        DistributedCartesianGrid.DistributedCartesianGrid.turnOff(self)
        ZoneLOD.ZoneLOD.turnOff(self)

    def turnOn(self, av = None):
        self.startCustomEffects()
        if base.shipsVisibleFromIsland:
            self.parentWorld.worldGrid.startProcessVisibility(localAvatar)

        if av:
            self.setZoneLevel(0)
            self.addObjectToGrid(av)
            localAvatar.setInterest(self.doId, PiratesGlobals.IslandLocalZone, [
                'IslandLocal'])

        DistributedGameArea.DistributedGameArea.turnOn(self)
        DistributedCartesianGrid.DistributedCartesianGrid.turnOn(self, av)
        ZoneLOD.ZoneLOD.turnOn(self)

    def isGridParent(self):
        return 1

    def addObjectToGrid(self, av):
        DistributedCartesianGrid.DistributedCartesianGrid.addObjectToGrid(self, av)
        if av.isLocal():
            self.updateAvReturnLocation(av)
            self.startProcessVisibility(av)

    def setLocation(self, parentId, zoneId):
        DistributedGameArea.DistributedGameArea.setLocation(self, parentId, zoneId)
        world = self.cr.doId2do.get(parentId)
        if parentId not in (0, self.cr.getGameDoId()):
            pass
        if world:
            self.reparentTo(world)
            self.parentWorld = world

    def setZoneSphereSize(self, rad0, rad1, rad2):
        self.sphereRadii = [
            rad0,
            rad1,
            rad2,
            100000]

    def getZoneSphereSize(self):
        return self.sphereRadii

    def setZoneSphereCenter(self, x, y):
        self.sphereCenter = [
            x,
            y]

    def getZoneSphereCenter(self):
        return self.sphereCenter

    def getMusicName(self):
        islandName = self.getName()
        musicName = self.MusicNames.get(islandName, self.MusicDefault)
        return musicName

    def loadZoneLevel(self, level):
        if level == 0:
            self.islandObjectsLoaded = True
            self.hideSailingLOD()
            base.loadingScreen.beginStep('island terrain')
            self.retrieveIslandTerrain()
            base.loadingScreen.endStep('island terrain')
            self.builder.loadObjects()
            base.loadingScreen.beginStep('rest', 1, 8)
            base.loadingScreen.tick()
            self.listenForLocationSphere()
            base.loadingScreen.tick()
            self.startCustomEffects(island = True)
            base.loadingScreen.tick()
            self.type = 'Island Zone'
            base.loadingScreen.tick()
            if self.parentWorld and self.parentWorld.getWater():
                self.parentWorld.getWater().enable()
            base.loadingScreen.tick()
            if self.isDockable():
                self.setupMinimap()

            if self.minimap and localAvatar.getMinimapObject():
                self.minimap.addObject(localAvatar.getMinimapObject())
                localAvatar.guiMgr.setMinimap(self.minimap)

            localAvatar.setInterest(self.doId, PiratesGlobals.IslandLocalZone, [
                'IslandLocal'])
            if config.GetBool('island-prepare-scene', 1) and base.win.getGsg():
                render.prepareScene(base.win.getGsg())

            self.initBlockers(self)
            base.loadingScreen.tick()
            self.builder.checkForHolidayObjects()
            base.loadingScreen.tick()
            self.handleEnterGameArea()
            base.loadingScreen.tick()
            base.loadingScreen.endStep('rest')
        elif level == 1:
            localAvatar.setInterest(self.doId, PiratesGlobals.IslandShipDeployerZone, [
                'ShipDeployer'])
            if not self.undockable:
                localAvatar.setPort(self.doId)
            else:
                localAvatar.guiMgr.createWarning(PLocalizer.HeavyFogWarning, PiratesGuiGlobals.TextFG6, duration = 6.0)
        elif level == 2:
            if self.waterRing:
                self.setIslandWaterParameters(True)

            self.addToOceanSeapatch()
        elif level == 3:
            self.allEnabled = False
            self.showName()
        elif level == 4:
            pass

        base.loadingScreen.tick()
        self.updateCustomEffects(level)

    def unloadZoneLevel(self, level):
        if level == 0:
            self.islandObjectsLoaded = False
            self.handleExitGameArea()
            self.cleanupIslandData()
            self.unloadIslandShoreWave()
            self.stopListenForLocationSphere()
            base.localAvatar.guiMgr.clearMinimap(self.minimap)
            self.destroyMinimap()
            base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist = True)
            self.showSailingLOD()
            print self.parentWorld
            print self.parentWorld.getWater()
            if self.parentWorld and self.parentWorld.getWater():
                print 'self.parentWorld.getWater()'
                self.parentWorld.getWater().disable()
                print 'self.parentWorld.getWater().disable'
            localAvatar.clearInterestNamed(None, [
                'IslandLocal'])
        elif level == 1:
            localAvatar.clearInterestNamed(None, [
                'ShipDeployer'])
            localAvatar.clearPort(self.doId)
        elif level == 2:
            self.showName()
            self.removeFromOceanSeapatch()
        elif level == 3:
            self.hideName()
        elif level == 4:
            pass

        self.updateCustomEffects(level + 1)

    def handleChildArrive(self, child, zoneId):
        DistributedGameArea.DistributedGameArea.handleChildArrive(self, child, zoneId)
        base.loadingScreen.tick()
        if child.isLocal():
            self.childArrived(self.doId, self.getParentObj())
            messenger.send('docked')
            self.accept('ship_vis_change', self.shipVisibilityChanged)
            base.loadingScreen.tick()
            if not base.cr.config.GetBool('remove-island-barriers', 0):
                self.setupPlayerBarrier()

            #if not base.shipsVisibleFromIsland:
            #    self.parentWorld.worldGrid.stopProcessVisibility()
            #else:
            self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
            base.hideShipNametags = True
            base.loadingScreen.tick()
            messenger.send('hide-ship-nametags')
            base.loadingScreen.tick()
            if base.shipsVisibleFromIsland == 1:
                base.showShipFlats = True
                messenger.send('far-ships')
            else:
                base.showShipFlats = False
                messenger.send('normal-ships')
            self.setZoneLevel(0)
            self.turnOn(localAvatar)

    def handleChildLeave(self, child, zoneId):
        if child.isLocal():
            self.childLeft(self.doId, self.getParentObj())
            self.ignore('ship_vis_change')
            self.unloadPlayerBarrier()
            messenger.send('normal-ships')
            base.showShipFlats = False
            base.hideShipNametags = False
            messenger.send('show-ship-nametags')
            self.turnOff()

        DistributedGameArea.DistributedGameArea.handleChildLeave(self, child, zoneId)

    def handleEnterGameArea(self, collEntry = None):
        if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
            self.accept(PiratesGlobals.EVENT_SPHERE_SNEAK + PiratesGlobals.SPHERE_ENTER_SUFFIX, self._handleSneakIntoKingshead)

        DistributedGameArea.DistributedGameArea.handleEnterGameArea(self, collEntry)

    def handleExitGameArea(self, collEntry = None):
        if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
            self.ignore(PiratesGlobals.EVENT_SPHERE_SNEAK + PiratesGlobals.SPHERE_ENTER_SUFFIX)

        DistributedGameArea.DistributedGameArea.handleExitGameArea(self, collEntry)

    def _handleSneakIntoKingshead(self, msgName, avId):
        if avId == localAvatar.doId:
            localAvatar.motionFSM.off()
            self.sendUpdate('requestEntryToIsland')
            if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.EnterKingsheadMessage)

    def setupPlayerBarrier(self):
        if not self.playerBarrierNP:
            playerBarrier = CollisionInvSphere(self.zoneCenter[0], self.zoneCenter[1], 0, self.zoneRadii[0] * 0.95)
            playerBarrier.setTangible(1)
            cName = self.uniqueName('PlayerBarrier')
            cSphereNode = CollisionNode(cName)
            cSphereNode.setIntoCollideMask(OTPGlobals.WallBitmask | OTPGlobals.GhostBitmask)
            cSphereNode.addSolid(playerBarrier)
            self.playerBarrierNP = self.attachNewNode(cSphereNode)
            self.accept('enter' + self.uniqueName('PlayerBarrier'), self.enteredPlayerBarrier)
            self.accept('islandPlayerBarrier', self.setPlayerBarrier)

        self.setPlayerBarrier(1)

    def enteredPlayerBarrier(self, *args):
        localAvatar.guiMgr.createWarning(PLocalizer.IslandPlayerBarrierWarning, PiratesGuiGlobals.TextFG6)

    def unloadPlayerBarrier(self):
        self.ignore('enter' + self.uniqueName('PlayerBarrier'))
        self.ignore('islandPlayerBarrier')
        if self.playerBarrierNP:
            self.playerBarrierNP.remove_node()
            self.playerBarrierNP = None

    def setPlayerBarrier(self, isOn):
        if self.playerBarrierNP:
            if isOn:
                self.playerBarrierNP.unstash()
            else:
                self.playerBarrierNP.stash()

    def addIslandToOcean(self):
        if self.parentWorld.worldGrid:
            self.parentWorld.worldGrid.addIslandGrid(self)
        else:
            self.notify.error('worldGrid is none for %s %s' % (self.parentWorld, self))

    def removeIslandFromOcean(self):
        if self.parentWorld:
            self.parentWorld.worldGrid.removeIslandGrid(self)

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def loadIslandLowLod(self):
        flatName = self.modelPath.split('_zero')[0]
        if not self.islandLowLod:
            self.islandLowLod = loader.loadModel('%s_low' % flatName, okMissing = False)
            self.islandLowLod.flattenStrong()
            self.islandLowLod.hide(OTPRender.MainCameraBitmask)
            self.islandLowLod.showThrough(OTPRender.EnviroCameraBitmask)
            self.islandLowLodFog = self.islandLowLod.find('**/fog')
            if self.islandLowLodFog:
                self.islandLowLodFog.setLightOff()
                self.islandLowLodFog.setDepthWrite(0)
                todMgr = base.cr.timeOfDayManager
                if todMgr:
                    self.islandLowLodFog.setColorScale(TODGlobals.getTodEnvSetting(todMgr.currentState, todMgr.environment, 'FogColor') / 3.0 + Vec4(0, 0, 0, 1))

    def unloadIslandLowLod(self):
        if self.islandLowLod:
            self.islandLowLod.remove_node()

        self.islandLowLod = None

    def loadIslandMapModel(self):
        if not self.islandMapModelPath:
            mapModelName = self.modelPath.split('_zero')
            self.islandMapModelPath = mapModelName[0] + '_worldmap'

    def placeOnMap(self):
        self.loadIslandMapModel()
        if not (self.mapName) and self.islandMapModelPath:
            mapPage = localAvatar.guiMgr.mapPage
            self.mapName = mapPage.addIsland(self.name, self.uniqueId, self.islandMapModelPath, self.getPos(), self.getH())

    def removeFromMap(self):
        if self.mapName:
            mapPage = localAvatar.guiMgr.mapPage
            mapPage.removeIsland(self.mapName)

        self.mapName = None

    def loadIslandShoreWave(self, parent):
        base.loadingScreen.tick()
        if self.islandShoreWave:
            return None

        lowend = ''
        if base.options.getTerrainDetailSetting() == 0:
            lowend = '_lowend'

        islandBaseName = self.modelPath.split('_zero')[0]
        waveModel = loader.loadModel(islandBaseName + lowend + '_wave_none', okMissing = True)
        if lowend != '' and not waveModel:
            lowend = ''
            waveModel = loader.loadModel(islandBaseName + lowend + '_wave_none', okMissing = True)

        if waveModel:
            self.islandShoreWave = Actor.Actor(waveModel)
            self.islandShoreWave.loadAnims({
                'idle': islandBaseName + lowend + '_wave_idle' })
            self.islandShoreWave.reparentTo(parent)
            self.islandShoreWave.loop('idle')
            meshes = self.islandShoreWave.findAllMatches('**/mesh_tide1')
            if not meshes.isEmpty():
                mesh = meshes[0]
                joints = self.islandShoreWave.findAllMatches('**/uvj_WakeWhiteTide1')
                if joints.getNumPaths():
                    mesh.setTexProjector(mesh.findTextureStage('default'), joints[0], parent)


            meshes = self.islandShoreWave.findAllMatches('**/mesh_tide2')
            if not meshes.isEmpty():
                mesh = meshes[0]
                joints = self.islandShoreWave.findAllMatches('**/uvj_WakeWhiteTide2')
                if joints.getNumPaths():
                    mesh.setTexProjector(mesh.findTextureStage('default'), joints[0], parent)


            lavaCombo = self.islandShoreWave.findAllMatches('**/lava_combo_*')
            if lavaCombo.getNumPaths():
                lavaComboRoot = self.islandShoreWave.find('**/+Character').attachNewNode('lavaCombo')
                lavaComboRoot.setDepthWrite(1, 100)
                lavaCombo.reparentTo(lavaComboRoot)
                joint = self.islandShoreWave.find('**/uvj_LavaCombo1')
                lavaComboRoot.setTexProjector(lavaComboRoot.findTextureStage('default'), joint, parent)

            lavaHot = self.islandShoreWave.findAllMatches('**/lava_hot_*')
            if lavaHot.getNumPaths():
                lavaHotRoot = self.islandShoreWave.find('**/+Character').attachNewNode('lavaHot')
                lavaHotRoot.setDepthWrite(1, 100)
                lavaHot.reparentTo(lavaHotRoot)
                joint = self.islandShoreWave.find('**/uvj_LavaHot1')
                lavaHotRoot.setTexProjector(lavaHotRoot.findTextureStage('default'), joint, parent)

            lavaCool = self.islandShoreWave.findAllMatches('**/lava_cool_*')
            if lavaCool.getNumPaths():
                lavaCoolRoot = self.islandShoreWave.find('**/+Character').attachNewNode('lavaCool')
                lavaCoolRoot.setDepthWrite(1, 100)
                lavaCool.reparentTo(lavaCoolRoot)
                joint = self.islandShoreWave.find('**/uvj_LavaCool1')
                lavaCoolRoot.setTexProjector(lavaCoolRoot.findTextureStage('default'), joint, parent)

            #animSpeed = 0.8
            #self.islandShoreWave.setPlayRate(animSpeed, 'idle')
            #self.accept('windSpeedChange', self.adjustShoreWaveSpeed)
            #OTPRender.renderReflection(False, self.islandShoreWave, 'p_island_shore', None)
            alpha_test_attrib = AlphaTestAttrib.make(RenderAttrib.MAlways, 0)
            self.islandShoreWave.setAttrib(alpha_test_attrib, 100)
            self.islandShoreWave.setTwoSided(1, 100)
            self.islandShoreWave.setDepthWrite(0, 100)

    def adjustShoreWaveSpeed(self, wind):
        if self.islandShoreWave:
            self.islandShoreWave.setPlayRate(0.8, 'idle')

    def unloadIslandShoreWave(self):
        print 'unloadIslandShoreWave'
        #if self.islandShoreWave:
            #self.ignore('windSpeedChange')
        self.islandShoreWave.delete()
        self.islandShoreWave = None

    def foo(self):
        collNodes = self.geom.findAllMatches('**/+CollisionNode')
        for collNode in collNodes:
            curMask = collNode.node().getIntoCollideMask()
            if curMask.hasBitsInCommon(OTPGlobals.FloorBitmask):
                self.setupCannonballLandColl(collNode, PiratesGlobals.TargetBitmask | curMask, 0)
                continue

    def loadDockingLOD(self):
        islandBaseName = self.modelPath.split('_zero')[0]
        if self.dockingLOD:
            self.dockingLOD.detachNode()

        self.dockingLOD = loader.loadModel(islandBaseName + '_dock_lod', okMissing = True)
        if self.dockingLOD:
            self.dockingLOD.hide(OTPRender.MainCameraBitmask)
            self.dockingLOD.showThrough(OTPRender.EnviroCameraBitmask)
            self.dockingLOD.findAllMatches('**/water_*').detach()
            
            for obj in self.dockingLOD.findAllMatches('**/=ignore-lighting'):
                obj.setLightOff(1000)
            
            self.dockingLOD.flattenStrong()
            self.dockingLodFog = self.dockingLOD.find('**/fog')
            if self.dockingLodFog:
                self.dockingLodFog.setLightOff()
                self.dockingLodFog.setDepthWrite(0)
                todMgr = base.cr.timeOfDayManager
                if todMgr:
                    self.dockingLodFog.setColorScale(TODGlobals.getTodEnvSetting(todMgr.currentState, todMgr.environment, 'FogColor') / 3.0 + Vec4(0, 0, 0, 1))

    def unloadDockingLOD(self):
        if self.dockingLOD:
            self.dockingLOD.remove_node()
            self.dockingLOD = None

    def showSailingLOD(self):
        self.sailingLOD.show()

    def hideSailingLOD(self):
        self.sailingLOD.hide()

    def loadTerrain(self):
        islandBaseName = self.modelPath.split('_zero')[0]
        self.geom = self.loadWholeModel(islandBaseName)
        self.geom.findAllMatches('**/water_*').detach()
        
        for flat in self.geom.findAllMatches('**/island_flat_lod'):
            flat.removeNode()
        
        for obj in self.geom.findAllMatches('**/=ignore-lighting'):
            obj.setLightOff(1000)

    def loadWholeModel(self, name):
        lowend = ''
        if base.options.getTerrainDetailSetting() == 0:
            lowend = '_lowend'

        zeroModel = loader.loadModel(name + lowend + '_zero', okMissing = True)
        if not zeroModel:
            zeroModel = loader.loadModel(name + lowend, okMissing = True)

        if lowend != '' and not zeroModel:
            zeroModel = loader.loadModel(name + '_zero', okMissing = True)
            if not zeroModel:
                zeroModel = loader.loadModel(name)

        geom = zeroModel
        collNode = geom.find('**/cannoncol*')
        if collNode != collNode.notFound():
            collNode.node().setIntoCollideMask(collNode.node().getIntoCollideMask() | PiratesGlobals.TargetBitmask | OTPGlobals.CameraBitmask)
            collNode.setTag('objType', str(PiratesGlobals.COLL_BLOCKER))

        return geom

    def addToOceanSeapatch(self):
        if self.parentWorld and self.parentWorld.getWater():
            self.parentWorld.getWater().patch.addFlatWell(self.uniqueName('flatWell'), self, self.zoneCenter[0], self.zoneCenter[1], self.zoneRadii[0], self.zoneRadii[0] + 100)

    def removeFromOceanSeapatch(self):
        if self.parentWorld.getWater():
            self.parentWorld.getWater().patch.removeFlatWell(self.uniqueName('flatWell'))

    def loadIslandStuff(self):
        self.largeObjects = self.geom.findAllMatches('**/*bldg*')
        for b in self.largeObjects:
            b.wrtReparentTo(self.largeObjectsHigh)
            wallGeom = b.find('**/wall*_n_window*')
            roofGeom = b.find('**/roof')
            for c in [
                wallGeom,
                roofGeom]:
                self.setupCannonballBldgColl(c, PiratesGlobals.TargetBitmask)

        details = [
            self.geom.find('**/barrels'),
            self.geom.find('**/crates'),
            self.geom.find('**/canopys'),
            self.geom.find('**/bushes')]
        for detail in details:
            if not detail.isEmpty():
                detail.wrtReparentTo(self.smallObjectsHigh)
                detail.flattenLight()
                continue

        self.smallObjects = details
        del details
        details = [
            self.geom.find('**/palmtrees'),
            self.geom.find('**/pier')]
        for detail in details:
            if not detail.isEmpty():
                detail.wrtReparentTo(self.medObjectsHigh)
                detail.flattenLight()
                continue

        self.mediumObjects = details

    def setName(self, name):
        self.name = name
        if self.nameNode:
            self.nameNode.setText(name)
            siegeTeam = self.getSiegeTeam()
            if siegeTeam and self.SiegeIcon:
                color = VBase4(PVPGlobals.getSiegeColor(siegeTeam))
                color.setW(0.7)
                icon = self.SiegeIcon[siegeTeam - 1].copyTo(NodePath('siegeIcons'))
                icon.reparentTo(self.nameText)
                self.SiegeIcons.append(icon)
                icon.setZ(1.5)
                icon.setScale(0.75)
            else:
                color = Vec4(0.6, 0.6, 1, 0.4)
            self.nameNode.setTextColor(color)

    def getName(self):
        return self.name

    def setNameVisible(self, bool):
        if bool:
            self.showName()
        else:
            self.hideName()

    def hideName(self):
        if self.nameText:
            self.nameText.hide()

    def showName(self):
        if self.nameText:
            self.nameText.show()
    
    def initializeNameText(self):
        scale = WorldGlobals.getNametagScale(self.name)
        self.nameNode = TextNode('islandText')
        self.nameNode.setText(self.name)
        self.nameNode.setFont(PiratesGlobals.getPirateFont())
        self.nameNode.setWordwrap(PiratesGlobals.NAMETAG_WORDWRAP)
        self.nameText = self.attachNewNode(self.nameNode)
        self.nameText.setPos(0, 0, WorldGlobals.getNametagHeight(self.name))
        self.nameText.setFogOff()
        self.nameText.setLightOff()
        self.nameText.setScale(WorldGlobals.getNametagScale(self.name))
    
    def deleteNameText(self):
        if self.nameText:
            self.nameText.removeNode()
        
        self.nameNode = None
        self.nameText = None

    def setIslandWaterParameters(self, use_alpha_map):
        if self.islandWaterParameters:
            if self.parentWorld:
                self.islandWaterParameters.setIslandWaterParameters(self.parentWorld.getWater(), use_alpha_map)

    def setX(self, *args, **kwargs):
        DistributedGameArea.DistributedGameArea.setX(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, worldPos = self.getPos())

    def setY(self, *args, **kwargs):
        DistributedGameArea.DistributedGameArea.setY(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, worldPos = self.getPos())

    def setH(self, *args, **kwargs):
        DistributedGameArea.DistributedGameArea.setH(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, rotation = self.getH())

    def getTeam(self):
        return PiratesGlobals.ISLAND_TEAM

    def updateAvReturnLocation(self, av):
        av.d_requestReturnLocation(self.doId)

    def updateAvIsland(self, av):
        av.d_requestCurrentIsland(self.doId)

    def startFloatables(self):
        world = base.cr.getActiveWorld()
        if world:
            water = world.getWater()
            if water:
                for (uid, obj) in self.floatables.iteritems():
                    water.addFloatable(uid, obj, mass = 5)

    def stopFloatables(self):
        world = base.cr.getActiveWorld()
        if world:
            water = world.getWater()
            if water:
                for uid in self.floatables:
                    water.removeFloatable(uid)

    def setOceanVisEnabled(self, enabled):
        self.oceanVisEnabled = enabled
        if self.lastZoneLevel == 0:
            if not self.oceanVisEnabled:
                self.parentWorld.worldGrid.stopProcessVisibility()
            else:
                self.parentWorld.worldGrid.startProcessVisibility(localAvatar)

    def setFlatShips(self, value):
        self.flatShipsOnIsland = value
        if self.lastZoneLevel == 0:
            if self.flatShipsOnIsland:
                messenger.send('far-ships')
                base.showShipFlats = True
            else:
                messenger.send('normal-ships')
                base.showShipFlats = False

    def listenForLocationSphere(self):
        self.locationSphereName = 'locSphere-%s' % self.uniqueId
        msgName = PiratesGlobals.LOCATION_SPHERE
        self.accept('enter' + self.locationSphereName, self.cr.getActiveWorld().enteredSphere, extraArgs = [
            [
                msgName]])
        self.accept('exit' + self.locationSphereName, self.cr.getActiveWorld().exitedSphere, extraArgs = [
            [
                msgName]])

    def stopListenForLocationSphere(self):
        if self.locationSphereName:
            self.ignore('enter' + self.locationSphereName)
            self.ignore('exit' + self.locationSphereName)

    def retrieveDockingLOD(self):
        self.loadDockingLOD()
        islandBaseName = self.modelPath.split('_zero')[0]
        dockingChar = loader.loadModel(islandBaseName + '_dock_lod_none', okMissing = True)
        if dockingChar:
            self.dockingChar = Actor.Actor(dockingChar)
            self.dockingChar.loadAnims({
                'idle': islandBaseName + '_dock_lod_idle' })
            self.dockingChar.reparentTo(self.dockingLOD)
            joint = self.dockingChar.find('**/uvj_LavaCombo1')
            self.dockingChar.loop('idle')
            self.dockingChar.setTexProjector(self.dockingChar.findTextureStage('default'), joint, self.dockingLOD)

        self.dockingLOD.reparentTo(self)
        self.dockingLOD.hide(OTPRender.MainCameraBitmask)
        self.dockingLOD.showThrough(OTPRender.EnviroCameraBitmask)

    def retrieveIslandTerrain(self):
        self.loadTerrain()
        self.geom.reparentTo(self)
        self.geom.hide(OTPRender.MainCameraBitmask)
        self.geom.showThrough(OTPRender.EnviroCameraBitmask)
        self.hideMapNodes()
        self.loadIslandShoreWave(self.geom)

    def cleanupIslandData(self):
        self.builder.cleanupData()
        self.cleanupTerrain()

    def cleanupTerrain(self):
        self.geom.remove_node()
        self.geom = None

    def cleanupDockingLOD(self):
        if self.dockingChar:
            self.dockingChar.cleanup()

        self.dockingChar = None
        self.dockingLOD.remove_node()
        self.dockingLOD = None

    def getSiegeTeam(self):
        return base.cr.distributedDistrict.worldCreator.getPvpIslandTeam(self.uniqueId)

    def isInInvasion(self):
        return False

    def setUndockable(self, undockable):
        self.undockable = undockable

    def isDockable(self):
        return not (self.undockable)

    def shipVisibilityChanged(self, value):
        if value == 0:
            self.parentWorld.worldGrid.stopProcessVisibility()
        elif value == 1:
            self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
            base.showShipFlats = True
            messenger.send('far-ships')
        elif value == 2:
            self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
            base.showShipFlats = False
            messenger.send('normal-ships')

    def setupMinimap(self):
        if not (self.minimap) and not self.getMapNode().isEmpty():
            self.minimap = IslandMap(self)

    def destroyMinimap(self):
        if self.minimap:
            self.minimap.destroy()
            self.minimap = None

    def getGridParameters(self):
        return (self.cellWidth, self.viewingRadius)

    def getMapName(self):
        return 'map-' + self.getName()

    if __dev__:

        def setZoneLevel(self, *args, **kw):
            ZoneLOD.ZoneLOD.setZoneLevel(self, *args, **kw)

    def getIslandTransform(self):
        return (self.getX(), self.getY(), self.getZ(), self.getH())

    def setIslandTransform(self, x, y, z, h):
        self.setXYZH(x, y, z, h)

    def startCustomEffects(self, interior = False, island = False):
        DistributedGameArea.DistributedGameArea.startCustomEffects(self, interior = False, loadIslandMusic = island)
        if self.uniqueId == LocationIds.DEL_FUEGO_ISLAND:
            self.startVolcanoEffects()

        if self.uniqueId == LocationIds.TORTUGA_ISLAND:
            if not (self.feastFireEffect) and self.getFeastFireEnabled():
                self.startFeastEffects()

        self.updateCustomEffects(self.lastZoneLevel)
        self.builder.resumeSFX()

    def updateCustomEffects(self, level):
        if self.uniqueId == LocationIds.DEL_FUEGO_ISLAND:
            self.startVolcanoEffects()

        if self.uniqueId == LocationIds.TORTUGA_ISLAND:
            if not (self.feastFireEffect) and self.getFeastFireEnabled():
                self.startFeastEffects()

            if level == 0:
                if self.feastFireEffect:
                    self.feastFireEffect.startMainEffects()
                    self.feastFireEffect.stopFarEffects()

            if level == 1 or level == 2:
                if self.feastFireEffect:
                    self.feastFireEffect.stopMainEffects()
                    self.feastFireEffect.startFarEffects()

            if level == 3:
                if self.feastFireEffect:
                    self.feastFireEffect.stopMainEffects()
                    self.feastFireEffect.startFarEffects()

        if self.fireworkShowEnabled:
            if level in [
                0,
                1,
                2]:
                self.fireworkShowLegal = True
                self.fireWorksStartTime = 0.0
                if base.cr.timeOfDayManager and not base.cr.timeOfDayManager.checkTimeOfDayToggle('fireWorksShow'):
                    base.cr.timeOfDayManager.addTimeOfDayToggle('fireWorksShow', self.fireWorksStartTime, self.fireWorksStartTime + 2.0, startMethod = self.beginDailyFireworkShow, endMethod = self.destroyFireworkShow)

            else:
                self.fireWorksStartTime = None
                self.fireworkShowLegal = False
                self.destroyFireworkShow()
                if base.cr.timeOfDayManager:
                    base.cr.timeOfDayManager.removeTimeOfDayToggle('fireWorksShow')

    def stopCustomEffects(self):
        DistributedGameArea.DistributedGameArea.stopCustomEffects(self)
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.removeTimeOfDayToggle('fireWorksShow')

        self.destroyFireworkShow()
        if self.volcanoEffect:
            self.volcanoEffect.destroy()
            self.volcanoEffect = None

        if self.feastFireEffect:
            self.feastFireEffect.stopMainEffects()
            self.feastFireEffect.stopFarEffects()

        if self.fireworkShow:
            self.destroyFireworkShow()

        if self.builder:
            self.builder.pauseSFX()

    def startVolcanoEffects(self):
        if not self.volcanoEffect:
            self.volcanoEffect = VolcanoEffect()
            self.volcanoEffect.reparentTo(self)
            self.volcanoEffect.setPos(Vec3(-286, 180, 865))
            self.volcanoEffect.enable()

    def makeLavaErupt(self):
        if self.lastZoneLevel in [
            0,
            1,
            2]:
            if not self.volcanoEffect:
                self.startVolcanoEffects()

            self.volcanoEffect.startLavaEruption()

    def startLavaFlow(self):
        self.stopLavaFlow()
        lavaGeom = self.geom.find('**/lava')
        if not lavaGeom.isEmpty():
            lavaGeom.setLightOff()
            if base.main_rtt:
                lavaGeom.setFogOff()
                lavaGeom.showThrough(OTPRender.GlowCameraBitmask)

            tex = None
            if not lavaGeom.findTextureStage('VertexColor'):
                ts = TextureStage('VertexColor')
                ts.setSort(30)
                tex = lavaGeom.findTexture('*')
                if tex:
                    lavaGeom.setTexture(ts, tex)

            tsSet = lavaGeom.findAllTextureStages()
            tsSet = [ tsSet[x] for x in xrange(tsSet.getNumTextureStages()) ]
            tsSet.sort(key = lambda x: x.getSort())
            if not tsSet:
                return None

            TS = TextureStage
            tsSet[0].setCombineRgb(TS.CMReplace, TS.CSTexture, TS.COSrcColor)
            tsSet[1].setCombineRgb(TS.CMAdd, TS.CSTexture, TS.COSrcColor, TS.CSPrevious, TS.COSrcColor)
            tsSet[2].setCombineRgb(TS.CMInterpolate, TS.CSTexture, TS.COSrcColor, TS.CSPrevious, TS.COSrcColor, TS.CSPrimaryColor, TS.COSrcAlpha)
            lavaSpeed = {
                0: 0.04,
                1: 0.02,
                2: 0.01 }
            if tex:
                tsSet[3].setCombineRgb(TS.CMModulate, TS.CSPrevious, TS.COSrcColor, TS.CSPrimaryColor, TS.COSrcColor)
                tsSet[3].setCombineAlpha(TS.CMReplace, TS.CSConstant, TS.COSrcAlpha)
                tsSet[3].setColor(Vec4(1))
                lavaSpeed[3] = 0.0

            def flowLava(task):
                dt = globalClock.getDt()
                for key in lavaSpeed.keys():
                    offset = lavaGeom.getTexOffset(tsSet[key])[0]
                    offset -= lavaSpeed[key] * dt
                    offset %= 1.0
                    lavaGeom.setTexOffset(tsSet[key], offset, 0)

                return Task.cont

            taskMgr.add(flowLava, self.uniqueName('flowLava'))

    def stopLavaFlow(self):
        return None
        if self.geom and not self.geom.isEmpty():
            lavaGeom = self.geom.find('**/lava_red*')
            if lavaGeom and not lavaGeom.isEmpty():
                lavaGeom.clearLight()
                lavaGeom.clearFog()

        taskMgr.remove(self.uniqueName('flowLava'))

    def setFeastFireEnabled(self, value):
        if self.feastFireEnabled == value:
            return None

        self.feastFireEnabled = value
        if self.feastFireEnabled:
            self.startFeastEffects()
            self.updateCustomEffects(self.lastZoneLevel)
        else:
            self.stopFeastEffects()

    def getFeastFireEnabled(self):
        return self.feastFireEnabled

    def startFeastEffects(self):
        if not (self.feastFireEffect) and self.getFeastFireEnabled():
            self.feastFireEffect = FeastFire()
            self.feastFireEffect.setCustomSettings()
            self.feastFireEffect.reparentTo(self)
            self.feastFireEffect.setPos(278, -166, 4.5)

    def stopFeastEffects(self):
        if self.feastFireEffect:
            self.feastFireEffect.stopLoop()
            self.feastFireEffect = None

    def setFireworkShowEnabled(self, isEnabled, showType):
        self.fireworkShowEnabled = isEnabled
        self.fireworkShowType = showType
        if self.fireworkShowEnabled:
            self.createFireworkShow()
            self.updateCustomEffects(self.lastZoneLevel)
        else:
            self.destroyFireworkShow()

    def getFireworkShowEnabled(self):
        return self.fireworkShowEnabled

    def createFireworkShow(self):
        if not self.fireworkShow:
            self.fireworkShow = FireworkShow(self.fireworkShowType)

    def destroyFireworkShow(self):
        if self.fireworkShow:
            self.fireworkShow.cleanupShow()
            self.fireworkShow = None

    def tryToBeginFireworkShow(self):
        if self.fireworkShowLegal and base.cr.timeOfDayManager:
            timeUntilShow = base.cr.timeOfDayManager.getTimeUntil(PiratesGlobals.TOD_STARS)
            if timeUntilShow <= 0:
                self.beginFireworkShow(timeStamp = -1 * timeUntilShow)
            else:
                self.destroyFireworkShow()

    def beginFireworkShow(self, task = None, timeStamp = 0.0):
        self.createFireworkShow()
        if self.fireworkShow and not self.fireworkShow.isPlaying():
            self.fireworkShow.begin(timeStamp)
            self.fireworkShow.reparentTo(self)
            self.fireworkShow.setPos(render, FireworkGlobals.getShowPosition(self.uniqueId))
            self.fireworkShow.setHpr(render, FireworkGlobals.getShowOrientation(self.uniqueId))

    def beginDailyFireworkShow(self, task = None):
        self.createFireworkShow()
        if self.fireworkShow and not self.fireworkShow.isPlaying():
            currentTime = base.cr.timeOfDayManager.getCurrentIngameTime()
            startTimeDiff = currentTime - self.fireWorksStartTime
            startTimeDifSeconds = base.cr.timeOfDayManager.gameHoursToRealSeconds(startTimeDiff)
            duration = self.fireworkShow.getDuration()
            if startTimeDifSeconds < duration:
                self.fireworkShow.begin(startTimeDiff)
                self.fireworkShow.reparentTo(self)
                self.fireworkShow.setPos(render, FireworkGlobals.getShowPosition(self.uniqueId))
                self.fireworkShow.setHpr(render, FireworkGlobals.getShowOrientation(self.uniqueId))

    def ensureLoaded(self):
        self.setZoneLevel(0)
        DistributedGameArea.DistributedGameArea.ensureLoaded(self)

    def resetZoneLODs(self):
        if localAvatar.parentId != self.doId:
            self.setZoneLevel(3)

    def loadWaterRing(self):
        islandBaseName = self.modelPath.split('_zero')[0]
        self.waterRing = loader.loadModel(islandBaseName + '_ocean', okMissing = True)
        if self.waterRing:
            self.waterRing.hide(OTPRender.MainCameraBitmask)
            self.waterRing.show(OTPRender.EnviroCameraBitmask)
            self.waterRing.reparentTo(self)
            self.initializeIslandWaterParameters(self.waterRing)
        else:
            self.setIslandWaterParameters(False)

    def unloadWaterRing(self):
        self.setIslandWaterParameters(False)
        if self.waterRing:
            self.waterRing.detachNode()
            self.waterRing = None

    def setFogColor(self, fogColor):
        if self.dockingLodFog:
            self.dockingLodFog.setColorScale(fogColor)

        if self.islandLowLodFog:
            self.islandLowLodFog.setColorScale(fogColor)

    def timeOfDayChanged(self, stateId = None, stateDuration = 0.0, elapsedTime = 0.0, transitionTime = 0.0):
        if self.dockingLodFog:
            todMgr = base.cr.timeOfDayManager
            if not todMgr:
                return
            transitionTime = todMgr.cycleDuration * TODGlobals.getStateTransitionTime(todMgr.cycleType, todMgr.currentState)
            fromFogColor = TODGlobals.getTodEnvSetting(todMgr.lastState, todMgr.environment, 'FogColor') / 2.5 + Vec4(0, 0, 0, 1)
            toFogColor = TODGlobals.getTodEnvSetting(todMgr.currentState, todMgr.environment, 'FogColor') / 2.5 + Vec4(0, 0, 0, 1)
            if self.fogTransitionIval:
                self.fogTransitionIval.pause()
                self.fogTransitionIval = None

            self.fogTransitionIval = LerpFunctionInterval(self.setFogColor, duration = transitionTime, toData = toFogColor, fromData = fromFogColor)
            self.fogTransitionIval.start(elapsedTime)