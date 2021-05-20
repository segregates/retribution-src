from panda3d.core import BitMask32, Camera, ClockObject, CollideMask, CollisionHandler, CollisionHandlerEvent, CollisionHandlerQueue, CollisionNode, CollisionRay, CollisionSphere, CollisionTraverser, CollisionTube, EventHandler, LODNode, Lens, NodePath, PStatCollector, Point3, PolylightEffect, TextNode, VBase3, Vec4, lookAt
import math
import copy
import types
import random
from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import *
from direct.directnotify import DirectNotifyGlobal
from direct.controls import ControlManager
from direct.interval.IntervalGlobal import *
from direct.controls import BattleWalker
from direct.actor import Actor
from direct.showbase.InputStateGlobal import inputState
from direct.distributed.ClockDelta import *
from direct.showbase.ShadowPlacer import ShadowPlacer
from direct.fsm.StatePush import StateVar
from otp.avatar.LocalAvatar import LocalAvatar
from otp.avatar import PositionExaminer
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from otp.otpgui import OTPDialog
from pirates.audio import SoundGlobals
from pirates.piratesgui import PDialog
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedBattleAvatar
from pirates.chat.PiratesChatManager import PiratesChatManager
from pirates.chat.PTalkAssistant import PTalkAssistant
from pirates.ship import ShipGlobals
from pirates.piratesgui import GuiManager
from pirates.piratesgui import PiratesGuiGlobals
from pirates.tutorial import ChatTutorial
from pirates.tutorial import ChatTutorialAlt
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import EmoteGlobals
from pirates.reputation import ReputationGlobals
from pirates.battle import RangeDetector
from pirates.battle import BattleSkillDiary
from pirates.movement.CameraFSM import CameraFSM
from pirates.economy.EconomyGlobals import *
from pirates.economy import EconomyGlobals
from pirates.piratesbase import TeamUtils
from pirates.ship import DistributedSimpleShip
from pirates.instance import DistributedMainWorld
from pirates.world import DistributedGameArea
from pirates.world import OceanZone
from pirates.interact import InteractiveBase
from pirates.effects.CloudScud import CloudScud
from pirates.effects.ProtectionSpiral import ProtectionSpiral
from pirates.battle.EnemySkills import EnemySkills
from pirates.inventory import InventoryGlobals
from pirates.inventory.InventoryGlobals import Locations
from direct.controls.GhostWalker import GhostWalker
from direct.controls.PhysicsWalker import PhysicsWalker
from direct.controls.ObserverWalker import ObserverWalker
from pirates.movement.PiratesGravityWalker import PiratesGravityWalker
from pirates.movement.PiratesSwimWalker import PiratesSwimWalker
from pirates.quest import QuestDB
from pirates.quest import QuestStatus
from pirates.world.LocationConstants import LocationIds, getParentIsland
from pirates.world import WorldGlobals
from pirates.map.MinimapObject import GridMinimapObject
from pirates.pirate import TitleGlobals
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
import Pirate
import LocalPirateGameFSM
from DistributedPlayerPirate import DistributedPlayerPirate
from pirates.pirate import PlayerStateGlobals
from pirates.pirate import AvatarTypes
from pirates.makeapirate import ClothingGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import ItemGlobals
from direct.task.Task import Task
from pirates.effects.PooledEffect import PooledEffect
from pirates.piratesgui.GameOptions import Options
from direct.gui import OnscreenText
from otp.nametag.NametagConstants import *
globalClock = ClockObject.getGlobalClock()
if config.GetBool('want-pstats', 0):
    import profile
    import pstats

from direct.controls.ControlManager import ControlManager
if config.GetBool('want-custom-keys', 0):
    ControlManager.wantCustomKeys = 1
    ControlManager.wantWASD = 0
else:
    ControlManager.wantCustomKeys = 0
    ControlManager.wantWASD = 1

class LocalPirate(DistributedPlayerPirate, LocalAvatar):
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalPirate')
    isCollisions = 1

    def __init__(self, cr):

        try:
            self.LocalPirate_initialized
        except:
            self.LocalPirate_initialized = 1
            DistributedPlayerPirate.__init__(self, cr)
            self.masterHuman = base.cr.humanHigh
            chatMgr = PiratesChatManager()
            talkAssistant = PTalkAssistant()
            LocalAvatar.__init__(self, cr, chatMgr, talkAssistant = talkAssistant)
            self.gameFSM = None
            self.equippedWeapons = []
            self.monstrousTarget = None
            self.distanceToTarget = 0
            self.__lootUIEnabled = True
            self.setLocalAvatarUsingWeapon(1)
            self.cameraFSM = CameraFSM(self)
            self.guiMgr = GuiManager.GuiManager(self)
            self.interestHandles = []
            if config.GetBool('debug-local-animMixer', 0):
                self.animMixer.setVerbose(True)

            self.currentMouseOver = None
            self.currentAimOver = None
            self.currentSelection = None
            self.tutObject = None
            self.currentDialogMovie = None
            self.ship = None
            self.shipList = set()
            self.interior = None
            self.cannon = None
            self.__turboOn = 0
            self.__marioOn = 0
            self.speedIndex = 0
            self.curMoveSound = None
            self.setupMovementSounds()
            self.rangeDetector = RangeDetector.RangeDetector()
            self.rangeDetector.detachNode()
            self.showQuest = True
            self.currentOcean = 0
            self.soundWhisper = loadSfx(SoundGlobals.SFX_GUI_WHISPER)
            self.positionExaminer = PositionExaminer.PositionExaminer()
            self.skillDiary = BattleSkillDiary.BattleSkillDiary(self.cr, self)
            self.lookAtTarget = None
            self.lookAtTimer = None
            self.lookAtDummy = self.attachNewNode('lookAtDummy')
            self.lookFromNode = self.attachNewNode('lookFromTargetHelper')
            self.lookFromNode.setZ(self.getHeight())
            self.lookToNode = NodePath('lookToTargetHelper')
            if config.GetBool('want-dev', False):
                self.accept('shift-f12', self.toggleAvVis)

            self.money = 0
            self.enableAutoRun = 0
            self.kickEvents = None
            self.battleTeleportFlagTask = None
            self.openJailDoorTrack = None
            self.currentStoryQuests = []
            self.cloudScudEffect = None
            self.soloInteraction = False
            self.emoteAccess = []
            self.AFKDelay = config.GetInt('afk-delay', 600)
            self.playRewardAnimation = None
            self.localProjectiles = []
            self._cannonAmmoSkillId = InventoryType.CannonRoundShot
            self._siegeTeamSV = StateVar(0)
            self.guildPopupDialog = None
            self.moralePopupDialog = None
            soundEffects = [
                SoundGlobals.SFX_MONSTER_JR_LAUGH_01,
                SoundGlobals.SFX_MONSTER_JR_LAUGH_02,
                SoundGlobals.SFX_MONSTER_JR_ENJOY,
                SoundGlobals.SFX_MONSTER_JR_SUBMIT,
                SoundGlobals.SFX_MONSTER_JR_JOIN]
            self.jollySfx = loadSfx(random.choice(soundEffects))
            self.currCombatMusic = None
            self.sailHit = 0
            self.playersNearby = { }
            self.trackedRotation = []
            self.trackedTurning = 0
            self.lastCannonShot = globalClock.getFrameTime()
            self.levelFootStep = None
            self.wobbleList = []
            self.fovIval = None
            self.mistimedAttack = 0
            if config.GetBool('want-easy-combos', 0):
                self.wantComboTiming = 0
            else:
                self.wantComboTiming = 1
            self.zombieEffect = None
            self.zombieIval = None
            self.defenceEffects = { }
            self.skillSfxIval = None
            self.currentWeaponSlotId = 1
            if config.GetBool('want-pstats', 0):
                self.pstatsGen = PStatCollector('Battle Avatars:Avatar Generating')
                self.pstatsLoad = PStatCollector('Battle Avatars:Loading Asset')
                self.pstatsFPS = PStatCollector('Battle Avatars:fps')
                self.lastTime = None
                taskMgr.add(self.logPStats, 'avatarPstats')

            self.fishingGameHook = None
            self.accept('shipRemoved', self.checkHaveShip)
            self.rocketOn = 0
            if config.GetBool('want-rocketman', 0):
                self.startRocketJumpMode()

            self.dialogProp = None
            self.duringDialog = False
            self.efficiency = False
            self.boardedShip = False
            self.accept(PiratesGlobals.EscapeHotkey, self.guiMgr.toggleMainMenu, ['escape'])
            self.accept('f7', self.guiMgr.toggleMainMenu, ['escape'])
            self.accept('f', self.guiMgr.toggleSocialPanel)
            self.surfaceIndex = None
            self.movementIndex = None



    def startRocketJumpMode(self):
        self.oldGravity = None
        self.accept('space', self.moveUpStart)
        self.accept('space-up', self.moveUpEnd)
        self.rocketOn = 1


    def endRocketJumpMode(self):
        self.moveUpEnd()
        self.ignore('space')
        self.ignore('space-up')
        self.rocketOn = 0


    def moveUpEnd(self):
        taskMgr.remove('rocketDelayTask')
        if self.oldGravity != None:
            if self.oldGravity and 0:
                self.controlManager.get('walk').lifter.setGravity(self.oldGravity)
            else:
                self.controlManager.get('walk').lifter.setGravity(32.173 * 2.0)
            self.oldGravity = None



    def moveUpStart(self):
        self.lastJumpTime = None
        self.jumpStartTime = globalClock.getFrameTime()
        self.oldGravity = self.controlManager.get('walk').lifter.getGravity()
        if self.controlManager.get('walk').lifter.isOnGround():
            taskMgr.doMethodLater(0.5, self.rocketGrav, 'rocketDelayTask')
        else:
            self.rocketGrav()


    def rocketGrav(self, task = None):
        self.controlManager.get('walk').lifter.setGravity(-32.173)
        if task:
            return task.done



    def sendUpdate(self, *args, **kw):
        if self.isGenerated():
            return DistributedPlayerPirate.sendUpdate(self, *args, **kw)



    def logPStats(self, task):
        self.pstatsGen.setLevel(taskMgr.mgr.findTaskChain('background').getNumTasks() + 0)
        self.pstatsLoad.setLevel(taskMgr.mgr.findTaskChain('loader').getNumTasks() + 0)
        if self.lastTime == None:
            self.lastTime = globalClock.getRealTime()

        timeDelta = globalClock.getRealTime() - self.lastTime
        self.lastTime = globalClock.getRealTime()
        if timeDelta <= 0.0:
            fps = 0.0
        else:
            fps = 1.0 / timeDelta
        self.pstatsFPS.setLevel(fps)
        return task.cont


    def setupWalkControls(self, avatarRadius = 1.39, floorOffset = OTPGlobals.FloorOffset, reach = 4.0, wallBitmask = OTPGlobals.WallBitmask, floorBitmask = OTPGlobals.FloorBitmask, ghostBitmask = OTPGlobals.GhostBitmask):
        walkControls = PiratesGravityWalker(gravity = -32.173 * 2.0)
        walkControls.setWallBitMask(wallBitmask)
        walkControls.setFloorBitMask(floorBitmask)
        walkControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        walkControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(walkControls, 'walk')
        self.physControls = walkControls
        swimControls = PiratesSwimWalker()
        swimControls.setWallBitMask(wallBitmask)
        swimControls.setFloorBitMask(floorBitmask)
        swimControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, 4.0)
        swimControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(swimControls, 'swim')
        ghostControls = GhostWalker()
        ghostControls.setWallBitMask(ghostBitmask)
        ghostControls.setFloorBitMask(floorBitmask)
        ghostControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        ghostControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(ghostControls, 'ghost')
        observerControls = ObserverWalker()
        observerControls.setWallBitMask(ghostBitmask)
        observerControls.setFloorBitMask(floorBitmask)
        observerControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        observerControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(observerControls, 'observer')
        self.controlManager.use('walk', self)
        self.controlManager.disable()


    def createGameFSM(self):
        self.gameFSM = LocalPirateGameFSM.LocalPirateGameFSM(self)


    def updateReputation(self, category, value):
        DistributedPlayerPirate.updateReputation(self, category, value)
        self.guiMgr.updateReputation(category, value)


    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge = 0, targetId = 0, areaIdList = []):
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
            self.skillDiary.clearHits(skillId)
            self.guiMgr.combatTray.clearSkillCharge(skillId)
        else:
            self.skillDiary.startRecharging(skillId, ammoSkillId)
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.DEFENSE_SKILL_INDEX:
            if skillId == EnemySkills.MISC_VOODOO_REFLECT:
                self.showEffectString(PLocalizer.AttackReflected)
            else:
                self.showEffectString(PLocalizer.AttackBlocked)
            self.guiMgr.combatTray.startSkillRecharge(skillId)

        if skillId in (EnemySkills.STAFF_TOGGLE_AURA_WARDING, EnemySkills.STAFF_TOGGLE_AURA_NATURE, EnemySkills.STAFF_TOGGLE_AURA_DARK):
            if self.getAuraActivated():
                skillId = EnemySkills.STAFF_TOGGLE_AURA_OFF


        DistributedPlayerPirate.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId, areaIdList)

    def doRegeneration(self):
        DistributedPlayerPirate.doRegeneration(self)
        messenger.send('localAv-regenerate')

    def wearJewelry(self, itemToWear, location, remove = None):
        if remove:
            self.tryOnJewelry(None, location)
        else:
            self.tryOnJewelry(itemToWear, location)
        self.t_requestClothes()

    def wearItem(self, itemToWear, location, remove = None):
        if remove:
            self.removeClothes(location)
        else:
            self.tryOnClothes(location, itemToWear.itemTuple)
        self.t_requestClothes()


    def wearTattoo(self, itemToWear, location, remove = None):
        if remove:
            self.tryOnTattoo(None, location)
        else:
            self.tryOnTattoo(itemToWear, location)
        self.t_requestClothes()

    def t_requestClothes(self):
        if not taskMgr.hasTaskNamed('inventoryClothingUpdate'):
            taskMgr.doMethodLater(0.25, self.d_requestClothes, 'inventoryClothingUpdate')

    def d_requestClothes(self, task=None):
        self.sendUpdate('requestClothes', [self.style.makeNetString()])

    def checkForWeaponInSlot(self, weaponId, slot):
        inventory = localAvatar.getInventory()
        if slot == -1:
            return 1

        if inventory:
            weaponInSlot = inventory.getLocatables().get(slot)
            if weaponInSlot and weaponInSlot[1] == weaponId:
                return weaponInSlot[1]
            else:
                return None



    def getWeaponFromSlot(self, slot):
        inventory = localAvatar.getInventory()
        if inventory:
            weaponInSlot = inventory.getLocatables().get(slot)
            if weaponInSlot and weaponInSlot[1]:
                return weaponInSlot[1]
            else:
                return None



    def toggleWeapon(self, newWeaponId, slotId, fromWheel = 0):
        switchWeaponStates = [
            'LandRoam',
            'Battle',
            'WaterRoam',
            'Dialog']
        if self.getGameState() not in switchWeaponStates:
            return None

        if self.belongsInJail():
            return None

        if self.guiMgr.mainMenu and not self.guiMgr.mainMenu.isHidden():
            return None

        if not self.checkForWeaponInSlot(newWeaponId, slotId):
            return None

        newSlot = self.currentWeaponSlotId != slotId
        self.currentWeaponSlotId = slotId

        if (newWeaponId != self.currentWeaponId or newSlot) and self.isWeaponDrawn:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1, slotId)
            self.b_setGameState('Battle')
        elif not (self.isWeaponDrawn) and fromWheel:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1, slotId)
            self.b_setGameState('Battle')
        elif not self.isWeaponDrawn:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1, slotId)
            self.b_setGameState('Battle')
            messenger.send('weaponEquipped')
        else:
            self.d_requestCurrentWeapon(newWeaponId, 0)
            self.l_setCurrentWeapon(newWeaponId, 0, slotId)
            self.b_setGameState('LandRoam')
            messenger.send('weaponSheathed')


    def putWeaponAway(self):
        if self.isWeaponDrawn:
            self.d_requestCurrentWeapon(self.currentWeaponId, 0)
            self.l_setCurrentWeapon(self.currentWeaponId, 0, self.currentWeaponSlotId)
            self.b_setGameState('LandRoam')
            messenger.send('weaponSheathed')



    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        pass


    def l_setCurrentWeapon(self, currentWeaponId, isWeaponDrawn, slotId):
        if not self.gameFSM.isInTransition() and self.getGameState() in [
            'WaterRoam',
            'WaterTreasureRoam']:
            return None

        if self.currentWeaponId != currentWeaponId or self.isWeaponDrawn != isWeaponDrawn:
            self.d_clearStickyTargets()
            taskMgr.remove(self.uniqueName('runAuraDetection'))

        subtype = ItemGlobals.getSubtype(currentWeaponId)
        if WeaponGlobals.getWeaponCategory(currentWeaponId) == WeaponGlobals.VOODOO and isWeaponDrawn == True:
            self.guiMgr.attuneSelection.show()
        else:
            self.guiMgr.attuneSelection.hide()
        specialAttack = ItemGlobals.getSpecialAttack(self.currentWeaponId)
        if self.curAttackAnim:
            if specialAttack == EnemySkills.CUTLASS_ROLLTHRUST:
                self.curAttackAnim.pause()
            else:
                self.curAttackAnim.finish()
            self.curAttackAnim = None

        if self.secondWeapon:
            self.secondWeapon.remove_node()
            self.secondWeapon = None

        if ItemGlobals.getSubtype(currentWeaponId) == ItemGlobals.QUEST_PROP_POWDER_KEG and not isWeaponDrawn:
            currentWeaponId = 0

        self.checkWeaponSwitch(currentWeaponId, isWeaponDrawn)
        self.guiMgr.setCurrentWeapon(currentWeaponId, isWeaponDrawn, slotId)
        specialAttack = ItemGlobals.getSpecialAttack(currentWeaponId)
        if specialAttack and isWeaponDrawn:
            if WeaponGlobals.getSkillTrack(specialAttack) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
                self.skillDiary.clearHits(specialAttack)
                self.guiMgr.combatTray.clearSkillCharge(specialAttack)
            else:
                self.skillDiary.startRecharging(specialAttack, 0)
                self.guiMgr.combatTray.startSkillRecharge(specialAttack)



    def d_requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.sendUpdate('requestCurrentWeapon', [
            currentWeaponId,
            isWeaponDrawn])


    def d_requestCurrentAmmo(self, currentAmmoId):
        self.sendUpdate('requestCurrentAmmo', [
            currentAmmoId])


    def d_requestCurrentCharm(self, currentCharmId):
        self.sendUpdate('requestCurrentCharm', [
            currentCharmId])


    def setCurrentCharm(self, currentCharm):
        DistributedPlayerPirate.setCurrentCharm(self, currentCharm)
        self.guiMgr.combatTray.skillTray.updateCharmSkills()


    def __drawWeapon(self):
        self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId, self.currentWeaponSlotId)


    def __drawWeaponIfTarget(self):
        if self.isWeaponDrawn:
            return None

        if self.cr.targetMgr:
            target = self.cr.targetMgr.pickObject()
            if target and TeamUtils.damageAllowed(target, self):
                self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId, self.currentWeaponSlotId)




    def enableMouseWeaponDraw(self):
        self.accept('control', self.__drawWeapon)
        self.accept('mouse1', self.__drawWeaponIfTarget)
        self.accept('mouse2', self.__drawWeapon)


    def disableMouseWeaponDraw(self):
        self.ignore('control')
        self.ignore('mouse1')
        self.ignore('mouse2')


    def runAuraDetection(self, task):
        targets = []
        self.areaAuraSphere.reparentTo(self)
        self.areaAuraTrav.addCollider(self.areaAuraSphere, self.areaAuraQueue)
        self.areaAuraTrav.traverse(self.getRender())
        self.areaAuraTrav.removeCollider(self.areaAuraSphere)
        self.areaAuraSphere.detachNode()
        numEntries = self.areaAuraQueue.getNumEntries()
        if numEntries == 0:
            pass
        1
        for i in xrange(numEntries):
            entry = self.areaAuraQueue.getEntry(i)
            potentialTargetColl = entry.getIntoNodePath()
            potentialTarget = self.repository.targetMgr.getObjectFromNodepath(potentialTargetColl)
            if potentialTarget:
                if not TeamUtils.damageAllowed(potentialTarget, self):
                    potentialTargetId = potentialTarget.getDoId()
                    targets.append(potentialTargetId)

            TeamUtils.damageAllowed(potentialTarget, self)

        DistributedPlayerPirate.sendRequestAuraDetection(self, targets)
        return Task.again


    def setMoney(self, money):
        if money == None:
            money = self.getGoldInPocket()

        self.guiMgr.setMoney(money)
        if money != 0:
            gain = money - self.money
            if gain > 0 and self.__lootUIEnabled:
                if self.gameFSM.getCurrentOrNextState() == 'ParlorGame':
                    pass
                1
                self.guiMgr.messageStack.showLoot([], gold = gain)


        self.money = money
        inv = self.getInventory()
        if inv:
            if not self.money >= 300 and inv.getStackQuantity(InventoryType.BuyNewShip) == 0:
                if not self.money >= 800 and inv.getStackQuantity(InventoryType.BuyNewShip) == 1:
                    if not self.money >= 1000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 2:
                        if not self.money >= 3500 and inv.getStackQuantity(InventoryType.BuyNewShip) == 3:
                            if not self.money >= 5000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 4:
                                if not self.money >= 20000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 5:
                                    if self.money >= 40000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 6 and self.money >= 60000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 7:
                                        self.sendRequestContext(InventoryType.BuyNewShip)




    def _setCrewShip(self, ship):
        crewShip = self.crewShip
        if crewShip is not None and crewShip != ship:
            crewShip.hideStatusDisplay()
            if self.guiMgr and self.guiMgr.mapPage:
                self.guiMgr.mapPage.removeShip(crewShip.doId)

            mapObj = crewShip.getMinimapObject()
            if mapObj:
                mapObj.setAsLocalAvShip(False)


        DistributedPlayerPirate._setCrewShip(self, ship)
        if ship:
            ship.showStatusDisplay()
            self.d_requestCurrentIsland(0)
            if self.guiMgr and self.guiMgr.mapPage:
                pos = base.cr.activeWorld.getWorldPos(ship)
                self.guiMgr.mapPage.addShip(ship.getShipInfo(), pos)

            mapObj = ship.getMinimapObject()
            if mapObj:
                mapObj.setAsLocalAvShip(True)

        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFOnShip)
            self.b_clearTeleportFlag(PiratesGlobals.TFNotSameCrew)
            self.b_clearTeleportFlag(PiratesGlobals.TFSiegeCaptain)

    def setActiveShipId(self, shipId):
        DistributedPlayerPirate.setActiveShipId(self, shipId)
        messenger.send('activeShipChange', sentArgs = [
            shipId])

    def setReturnLocation(self, returnLocation):
        if returnLocation == '1142018473.22dxschafe':
            returnLocation = LocationIds.DEL_FUEGO_ISLAND

        DistributedPlayerPirate.setReturnLocation(self, returnLocation)

        def setIt(inventory, returnLocation = returnLocation):
            # TO DO: uncomment to forbid non-PR return location w/o a ship
            #if inventory:
             #   if inventory.getShipDoIdList():
                    self.guiMgr.mapPage.setReturnIsland(returnLocation)
              #  else:
               #     self.guiMgr.mapPage.setReturnIsland(LocationIds.PORT_ROYAL_ISLAND)


        DistributedInventoryBase.getInventory(self.inventoryId, setIt)


    def setCurrentIsland(self, islandUid):
        DistributedPlayerPirate.setCurrentIsland(self, islandUid)
        if self.guiMgr:
            if self.guiMgr.mapPage:
                self.guiMgr.mapPage.setCurrentIsland(islandUid)

    def setJailCellIndex(self, index):
        if not self.isGenerated():
            return
        DistributedPlayerPirate.setJailCellIndex(self, index)
        messenger.send('localAvatar-setJailCellIndex', [
            index])


    def setCurrentTarget(self, targetId):
        target = self.cr.doId2do.get(targetId)
        if target == self.currentTarget:
            if TeamUtils.damageAllowed(target, self):
                self.requestCombatMusic()

            return None

        if self.currentTarget:
            self.currentTarget.setLocalTarget(0)
            if self.currentTarget.state == 'Use':
                self.currentTarget.request('Idle')


        self.currentTarget = target
        if target:
            if (not hasattr(target, 'currentDialogMovie') or target.currentDialogMovie == None) and target.hideHpMeterFlag == 0:
                target.showHpMeter()

            target.setLocalTarget(1)
            target.request('Use')

        self.cr.interactionMgr.start()
        if self.currentTarget and TeamUtils.damageAllowed(self.currentTarget, self):
            self.requestCombatMusic()

        DistributedPlayerPirate.setCurrentTarget(self, targetId)


    def delete(self):

        try:
            self.LocalPirate_deleted
        except:
            self.LocalPirate_deleted = 1
            self.guiMgr.delete()
            del self.guiMgr
            self.cameraFSM.cleanup()
            del self.cameraFSM
            del self.currentMouseOver
            self.currentAimOver = None
            del self.currentSelection
            del self.skillDiary
            self.ignore('shipRemoved')
            DistributedPlayerPirate.delete(self)
            taskMgr.remove(self.uniqueName('questShow'))
            taskMgr.remove(self.uniqueName('oceanCheck'))
            taskMgr.remove(self.uniqueName('runAuraDetection'))
            self.currentStoryQuests = []
            LocalAvatar.delete(self)
            self.stopAllDefenceEffects()
            if self.cloudScudEffect:
                self.cloudScudEffect.stopLoop()
                self.cloudScudEffect = None

            self.questStatus.delete()
            del self.questStatus
            self.__cleanupGuildDialog()
            self.__cleanupMoraleDialog()
            del base.localAvatar
            del __builtins__['localAvatar']



    def targetMgrCreated(self):
        pass


    def generateHuman(self, *args, **kwargs):
        DistributedPlayerPirate.generateHuman(self, *args, **kwargs)
        self.deleteWeaponJoints()
        lod2000 = self.getLOD('2000')
        if lod2000:
            lod2000.flattenMedium()

        lod1000 = self.getLOD('1000')
        if lod1000:
            lod1000.flattenMedium()

        self.getWeaponJoints()
        self.setLODAnimation(1000, 1000, 0.001)


    def generate(self):
        base.localAvatar = self
        __builtins__['localAvatar'] = self
        DistributedPlayerPirate.generate(self)


    def announceGenerate(self):
        base.loadingScreen.tick()
        self.accept('avatarZoneChanged', self.handleZoneChanged)
        self.invInterest = self.addInterest(2, 'localAvatar-inventory')

        self.nametag.manage(base.marginManager)
        self.controlManager.setTag('avId', str(self.getDoId()))
        pe = PolylightEffect.make()
        brightness = 1.25
        darkness = 0.800000
        pe.setWeight(brightness)
        self.node().setEffect(pe)
        DistributedPlayerPirate.announceGenerate(self)
        self.questStatus = QuestStatus.QuestStatus(self)
        posHpr = (0, 0, 0, 0, 0, 0)
        self.setPosHpr(*posHpr)
        self.acceptOnce('targetMgrCreated', self.targetMgrCreated)
        if config.GetBool('osd-anim-blends', 0):
            self.toggleOsdAnimBlends(True)

        self.acceptOnce('generate-%s' % self.getInventoryId(), self.initInventoryGui)
        for weaponId in WeaponGlobals.getHumanWeaponTypes():
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), weaponId), self.refreshInventoryWeapons)

        for skillId in xrange(InventoryType.begin_WeaponSkillMelee, InventoryType.end_WeaponSkillMelee):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillBayonet, InventoryType.end_WeaponSkillBayonet):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillCannon, InventoryType.end_ExtendedWeaponSkillCannon):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for skillId in xrange(InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])

        for teleportTokenId in xrange(InventoryType.begin_TeleportToken, InventoryType.end_TeleportToken):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), teleportTokenId), self.guiMgr.mapPage.updateTeleportIsland, extraArgs = [
                teleportTokenId])

        self.accept('inventoryAccumulator-%s-%s' % (self.getInventoryId(), InventoryType.OverallRep), self.updateReputation, extraArgs = [
            InventoryType.OverallRep])
        for repCategory in ReputationGlobals.getReputationCategories():
            self.accept('inventoryAccumulator-%s-%s' % (self.getInventoryId(), repCategory), self.updateReputation, extraArgs = [
                repCategory])

        for unCat in ReputationGlobals.getUnspentCategories():
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), unCat), self.guiMgr.updateUnspent, extraArgs = [
                unCat])

        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(self.getInventoryId(), InventoryType.ItemTypeConsumable), self.guiMgr.updateTonic)
        self.guiMgr.combatTray.updateBestTonic()
        self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.ShipRepairKit), self.guiMgr.updateShipRepairKit)
        self.guiMgr.combatTray.updateShipRepairKits()
        taskMgr.add(self.shadowReach, 'shadowReach', priority = 40)
        self.accept('enterWater', self.handleWaterIn)
        self.accept('againWater', self.handleWaterAgain)
        self.accept('exitWater', self.handleWaterOut)
        if self.style.getTutorial() < PiratesGlobals.TUT_GOT_COMPASS and not config.GetBool('teleport-all', 0):
            self.b_setTeleportFlag(PiratesGlobals.TFNoCompass)

        if self.style.getTutorial() == PiratesGlobals.TUT_CHAPTER3_STARTED:
            if self.chatMgr.noChat:
                ct = ChatTutorialAlt.ChatTutorialAlt()
            else:
                ct = ChatTutorial.ChatTutorial()

        if not (self.inPvp):
            if self.style.getTutorial() >= PiratesGlobals.TUT_MET_JOLLY_ROGER or self.guiMgr.forceLookout:
                self.guiMgr.crewHUD.setHUDOn()
                self.guiMgr.crewHUDTurnedOff = False

        self.accept('InputState-forward', self.checkInputState)
        self.accept('InputState-reverse', self.checkInputState)
        self.accept('InputState-turnLeft', self.checkInputState)
        self.accept('InputState-turnRight', self.checkInputState)
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseProjectileSkill, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseShipSkill, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.checkAction)
        self.accept('action', self.checkAction)
        self.accept('moustacheFlip', self.handleMoustache)
        self.bindAnim([
            'idle',
            'run',
            'walk',
            'spin_right',
            'spin_left'])
        self.ignore('localAvatarVisZoneChanged')
        if base.options.getCharacterDetailSetting() in (0, 1):
            self.getLODNode().forceSwitch(1)

        messenger.send('localPirate-created', [])
        DistributedInventoryBase.getInventory(base.localAvatar.inventoryId, self.inventoryArrived)
        self.guiMgr.initQuestPage()
        self.reparentTo(render)


    def disable(self):
        self.ignore('avatarZoneChanged')
        if config.GetBool('want-pstats', 0):
            taskMgr.remove('avatarPstats')

        self.ignore('generate-%s' % self.getInventoryId())
        self.ignore('goldInPocketChanged')
        self.ignore('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.Dinghy))
        self.ignore('inventoryAddDoId-%s-%s' % (self.getInventoryId(), InventoryCategory.SHIPS))
        self.ignore('inventoryRemoveDoId-%s-%s' % (self.getInventoryId(), InventoryCategory.SHIPS))
        self.ignore('control-f3')
        self.ignore('shift-f12')
        self.ignore('enterWater')
        self.ignore('againWater')
        self.ignore('exitWater')
        self.ignore(self.cr.getAllInterestsCompleteEvent())
        self.ignore('moustacheFlip')
        taskMgr.remove(self.taskName('irisIn'))
        self.stopCombatMusic()
        self.clearBattleTeleportFlag(send = False)
        self.shipList = set()
        self.nametag.unmanage(base.marginManager)
        del self.invInterest
        if self.openJailDoorTrack:
            self.openJailDoorTrack.pause()
            self.openJailDoorTrack = None

        taskMgr.remove(self.uniqueName('monitorStickyTargets'))
        taskMgr.remove('localAvLookAtTarget')
        taskMgr.remove(self.uniqueName('setZombie'))
        base.chatPanel.updateDisplay()
        self.ignore('InputState-forward')
        self.ignore('InputState-backward')
        self.ignore('uber-enter')
        taskMgr.remove('autoAFK')
        self.cleanupLocalProjectiles()
        messenger.send('localPirateDisabled')
        DistributedPlayerPirate.disable(self)


    def inventoryArrived(self, inventory):
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(localAvatar.getInventoryId(), InventoryType.PVPTotalInfamyLand), self.infamyUpdate)
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(localAvatar.getInventoryId(), InventoryType.PVPTotalInfamySea), self.infamyUpdate)


    def setBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setBadgeIcon(self, titleId, rank)
        messenger.send('LocalBadgeChanged')


    def setShipBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setShipBadgeIcon(self, titleId, rank)
        messenger.send('LocalShipBadgeChanged')


    def infamyUpdate(self, task = None):
        if localAvatar.badge and len(localAvatar.badge) == 2:
            titleId = localAvatar.badge[0]
            inventoryType = TitleGlobals.getInventoryType(titleId)
            if inventoryType:
                exp = localAvatar.getInventory().getStackQuantity(TitleGlobals.getInventoryType(titleId))
                realRank = TitleGlobals.getRank(titleId, exp)
                if realRank != localAvatar.badge[1]:
                    localAvatar.sendRequestSetBadgeIcon(titleId, realRank)



        if localAvatar.shipBadge and len(localAvatar.shipBadge) == 2:
            titleId = localAvatar.shipBadge[0]
            inventoryType = TitleGlobals.getInventoryType(titleId)
            if inventoryType:
                exp = localAvatar.getInventory().getStackQuantity(TitleGlobals.getInventoryType(titleId))
                realRank = TitleGlobals.getRank(titleId, exp)
                if realRank != localAvatar.shipBadge[1]:
                    localAvatar.sendRequestSetShipBadgeIcon(titleId, realRank)



        messenger.send('LocalAvatarInfamyUpdated')


    def clearInventoryInterest(self):
        self.removeInterest(self.invInterest, event = self.uniqueName('localAvatar-close-inventory'))

    def handleMoustache(self, moustache = 0):
        self.t_requestClothes()


    def initInventoryGui(self, inventory):
        gold = self.getGoldInPocket()
        self.setMoney(gold)
        self.accept('goldInPocketChanged', self.setMoney)
        self.refreshInventoryWeapons()


    def refreshInventoryWeapons(self, args = None):
        self.equipSavedWeapons()
        self.guiMgr.refreshInventoryWeapons()


    def equipSavedWeapons(self):
        inventory = self.getInventory()
        if not inventory:
            return None

        self.equippedWeapons = [
            0,
            0,
            0,
            0,
            0,
            0]
        inventory.getEquippedWeapons(self.equippedWeapons)
        if not self.currentWeaponId:
            self.currentWeaponId = self.equippedWeapons[0]
            if self.currentWeaponId:
                self.currentWeaponSlotId = 1

            self.l_setCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn, 1)
            self.d_requestCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn)

        self.guiMgr.setEquippedWeapons(self.equippedWeapons)

    def died(self):
        if self.isGenerated():
            self.b_setGameState('Injured')

    def setupControls(self):
        floorOffset = OTPGlobals.FloorOffset
        reach = 8.0
        avatarRadius = 1.39
        controls = BattleWalker.BattleWalker()
        controls.setWallBitMask(OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask)
        controls.setFloorBitMask(OTPGlobals.FloorBitmask)
        controls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        controls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(controls, 'battle')
        self.setupWalkControls(avatarRadius = 1.39, floorOffset = OTPGlobals.FloorOffset, reach = reach, wallBitmask = OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask, floorBitmask = OTPGlobals.FloorBitmask, ghostBitmask = OTPGlobals.GhostBitmask)
        self.enableRun()
        self.startListenAutoRun()


    def startListenAutoRun(self):
        self.accept('shift-r', self.startAutoRun)
        self.accept('r', self.toggleAutoRun)
        self.accept('mouse4', self.toggleAutoRun)


    def stopListenAutoRun(self):
        self.ignore('shift-r')
        self.ignore('r')
        self.ignore('mouse4')


    def toggleAutoRun(self):
        if self.enableAutoRun:
            self.stopAutoRun()
        else:
            self.startAutoRun()
            self.removeContext(InventoryType.DockCommands, 6)


    def toggleTurbo(self):
        if self.__turboOn:
            self.__turboOn = 0
        else:
            self.__turboOn = 1


    def getTurbo(self):
        return self.__turboOn


    def toggleMario(self):
        if self.__marioOn:
            self.__marioOn = 0
            self.setSwiftness(1.0)
        else:
            self.__marioOn = 1
            self.setSwiftness(6.0)


    def getMario(self):
        return self.__marioOn


    def initializeCollisions(self):
        LocalAvatar.initializeCollisions(self)
        cRay = CollisionRay(0.0, 0.0, 8.0, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('LP.cRayNode')
        cRayNode.addSolid(cRay)
        cRayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.cFloorNodePath = self.attachNewNode(cRayNode)
        self.floorEventHandler = CollisionHandlerEvent()
        self.floorEventHandler.addInPattern('enterFloor%in')
        self.floorEventHandler.addOutPattern('exitFloor%in')
        cRay = CollisionRay(0.0, 0.0, 8.0, 0.0, 0.0, -1.0)
        cRayNode2 = CollisionNode('LP.cRayNode2')
        cRayNode2.addSolid(cRay)
        cRayNode2.setFromCollideMask(PiratesGlobals.WaterBitmask)
        cRayNode2.setIntoCollideMask(BitMask32.allOff())
        self.cWaterNodePath = self.attachNewNode(cRayNode2)
        self.waterEventHandler = CollisionHandlerEvent()
        self.waterEventHandler.addInPattern('enterWater')
        self.waterEventHandler.addAgainPattern('againWater')
        self.waterEventHandler.addOutPattern('exitWater')
        zoneSphere = CollisionSphere(0, 0, 0, 1)
        zoneNode = CollisionNode('LP.zoneLOD')
        zoneNode.setFromCollideMask(PiratesGlobals.ZoneLODBitmask)
        zoneNode.setIntoCollideMask(BitMask32.allOff())
        zoneNode.addSolid(zoneSphere)
        self.cZoneLODNodePath = self.attachNewNode(zoneNode)
        base.lodTrav.addCollider(self.cZoneLODNodePath, base.zoneLODEventHandler)
        auraSphere = CollisionSphere(0, 0, 0, WeaponGlobals.AURA_RADIUS)
        node = CollisionNode('areaTargetAuraSphere')
        node.addSolid(auraSphere)
        node.setFromCollideMask(PiratesGlobals.BattleAimBitmask)
        node.setIntoCollideMask(BitMask32.allOff())
        self.areaAuraSphere = NodePath(node)
        self.areaAuraSphere.setName('LocalPirate.auraSphere')
        self.areaAuraQueue = CollisionHandlerQueue()
        self.areaAuraHandler = CollisionHandlerEvent()
        self.areaAuraTrav = CollisionTraverser('LocalPirate.auraTrav')


    def deleteCollisions(self):
        LocalAvatar.deleteCollisions(self)
        self.cFloorNodePath.remove_node()
        self.cWaterNodePath.remove_node()
        del self.floorEventHandler
        del self.waterEventHandler
        base.lodTrav.removeCollider(self.cZoneLODNodePath)
        self.cZoneLODNodePath.remove_node()
        self.cZoneLODNodePath = None


    def collisionGhost(self):
        LocalAvatar.collisionsOff(self)


    def collisionUnghost(self):
        LocalAvatar.collisionsOn(self)


    def collisionsOn(self):
        LocalAvatar.collisionsOn(self)
        self.cTrav.addCollider(self.cFloorNodePath, self.floorEventHandler)
        self.cTrav.addCollider(self.cWaterNodePath, self.waterEventHandler)


    def collisionsOff(self):
        LocalAvatar.collisionsOff(self)
        self.cTrav.removeCollider(self.cFloorNodePath)
        self.cTrav.removeCollider(self.cWaterNodePath)


    def initializeBattleCollisions(self):
        if self.aimTubeNodePaths:
            return None

        self.aimTubeEvent = self.uniqueName('aimTube')
        aimTube = CollisionTube(0, 0, 0, 0, 0, self.height, self.battleTubeRadius * 1.5)
        aimTube.setTangible(0)
        aimTubeNode = CollisionNode(self.aimTubeEvent)
        aimTubeNode.addSolid(aimTube)
        aimTubeNode.setIntoCollideMask(PiratesGlobals.BattleAimBitmask)
        aimTubeNodePath = self.attachNewNode(aimTubeNode)
        aimTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        aimTubeNodePath.setTag('avId', str(self.doId))
        self.aimTubeNodePaths.append(aimTubeNodePath)


    def setupAnimationEvents(self):
        pass


    def clearPageUpDown(self):
        if self.isPageDown or self.isPageUp:
            self.lerpCameraFov(PiratesGlobals.DefaultCameraFov, 0.598)
            self.isPageDown = 0
            self.isPageUp = 0
            self.setCameraPositionByIndex(self.cameraIndex)



    def getClampedAvatarHeight(self):
        return max(self.getHeight(), 3.0)


    def isLocal(self):
        return 1


    def canChat(self):
        if self.cr.allowOpenChat():
            return 1

        if self.commonChatFlags & (OTPGlobals.CommonChat | OTPGlobals.SuperChat):
            return 1

        return 0


    def startChat(self):
        LocalAvatar.startChat(self)
        self.accept('chatUpdateSCQuest', self.b_setSpeedChatQuest)
        self.ignore(PiratesGlobals.ThinkPosHotkey)
        self.accept(PiratesGlobals.ThinkPosHotkey, self.thinkPos)
        self.ignore(PiratesGlobals.SpeedChatHotkey)
        self.accept(PiratesGlobals.SpeedChatHotkey, self.openSpeedChat)


    def stopChat(self):
        LocalAvatar.stopChat(self)
        self.ignore('chatUpdateSCQuest')
        self.ignore(PiratesGlobals.ThinkPosHotkey)
        self.ignore(PiratesGlobals.SpeedChatHotkey)


    def isMap(self):
        return self.name == 'map'


    def thinkPos(self):
        pos = self.getPos(render)
        hpr = self.getHpr(render)
        serverVersion = base.cr.getServerVersion()
        districtName = base.cr.getShardName(self.defaultShard)
        parentId = self.parentId
        zoneId = self.zoneId
        parent = self.cr.doId2do.get(parentId)
        model = None
        if parent:
            pos = self.getPos(parent)
            hpr = self.getHpr(parent)
            if isinstance(parent, DistributedSimpleShip.DistributedSimpleShip):
                model = PLocalizer.ShipClassNames[parent.shipClass]
            elif isinstance(parent, DistributedGameArea.DistributedGameArea):
                model = parent.modelPath
                model = model.split('/')[-1]


        strPos = 'Position: \n%.1f, %.1f, %.1f' % (pos[0], pos[1], pos[2]) + '\nH: %.1f' % hpr[0] + '\nModel: %s' % model + '\nTexture: %s, Terrain: %s, Avatar: %s' % (base.options.getTextureScaleString(), base.options.getGameOptionString(base.options.getTerrainDetailSetting()), base.options.getGameOptionString(base.options.getCharacterDetailSetting())) + '\nLoc: (%s, %s)' % (str(parentId), str(zoneId)) + ',\nVersion: %s, ' % serverVersion + '\nDistrict: %s' % districtName
        self.setChatAbsolute(strPos, CFThought | CFTimeout)
    
    def thinkDistrict(self):
        strPos = '\n'.join(['%s: %s' % (district.name, district.avatarCount) for district in base.cr.activeDistrictMap.values()])
        self.setChatAbsolute(strPos, CFThought | CFTimeout)
        
        return strPos


    def openSpeedChat(self):
        pass


    def setSwiftness(self, swiftness):
        DistributedPlayerPirate.setSwiftness(self, swiftness)
        self.updatePlayerSpeed()


    def setSwiftnessMod(self, swiftness):
        DistributedPlayerPirate.setSwiftnessMod(self, swiftness)
        self.notify.debug('LocalPirate: setSwiftnessMod %s' % swiftness)
        self.updatePlayerSpeed()


    def setStunMod(self, stun):
        DistributedPlayerPirate.setStunMod(self, stun)
        self.notify.debug('LocalPirate: setStunMod %s' % stun)
        self.updatePlayerSpeed()


    def setHasteMod(self, haste):
        DistributedPlayerPirate.setHasteMod(self, haste)
        self.notify.debug('LocalPirate: setHasteMod %s' % haste)
        self.updatePlayerSpeed()


    def setAimMod(self, stun):
        DistributedPlayerPirate.setAimMod(self, stun)
        self.updatePlayerSpeed()


    def setTireMod(self, tire):
        DistributedPlayerPirate.setTireMod(self, tire)
        self.notify.debug('LocalPirate: setTireMod %s' % tire)
        self.updatePlayerSpeed()


    def attackTire(self, seconds = 1.2):
        if base.cr.gameStatManager.aggroModelIndex == 1:
            self.setTireMod(-0.4)
            taskMgr.remove(self.uniqueName('tireTask'))
            taskMgr.doMethodLater(seconds, self.untire, self.uniqueName('tireTask'))



    def untire(self, task = None):
        self.setTireMod(0.0)
        if task:
            return task.done



    def targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge = 0, delay = None, multihit = 0, itemEffects = []):
        DistributedPlayerPirate.targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, delay)
        attacker.respondedToLocalAttack = 1


    def updatePlayerSpeed(self):
        speedMult = self.swiftness + self.hasteMod + self.stunMod + self.tireMod
        speedMult = max(speedMult, -1.0)
        if self.swiftness + self.swiftnessMod <= 0.0:
            speedMult = 0.0

        if speedMult > 0.5:
            speedMult += self.aimMod

        if config.GetBool('want-fake-speed-mult', True):
            speedMult = config.GetFloat('fake-speed-mult', 2)

        speedMult = (speedMult, 1, speedMult, 1)
        oldSpeeds = PiratesGlobals.PirateSpeeds[self.speedIndex]
        newSpeeds = map(lambda x: x[0] * x[1], zip(oldSpeeds, speedMult))
        self.controlManager.setSpeeds(*newSpeeds)


    def setWalkForWeapon(self):
        DistributedPlayerPirate.setWalkForWeapon(self)
        self.updatePlayerSpeed()


    def requestEnterBattle(self):
        if self.getGameState() == 'LandRoam':
            self.b_setGameState('Battle')
        elif self.getGameState() == 'Battle':
            self.notify.debug('You are already in battle!')
        else:
            self.notify.debug('You cannot use weapons now.')


    def requestExitBattle(self):
        if localAvatar.curAttackAnim:
            timeToLock = localAvatar.curAttackAnim.getDuration() - localAvatar.curAttackAnim.getT()
            self.guiMgr.combatTray.noAttackForTime(timeToLock)

        if self.guiMgr.mainMenu and not self.guiMgr.mainMenu.isHidden():
            self.guiMgr.toggleMainMenu()
            return None

        if self.getGameState() == 'Battle':
            if self.gameFSM.defaultState == 'Battle':
                self.b_setGameState('LandRoam')
            elif self.gameFSM.defaultState in ('Injured', 'Dying'):
                return None
            else:
                self.b_setGameState(self.gameFSM.defaultState)

        messenger.send('weaponSheathed')


    def autoBoardStopMove(self, task = None):
        inputState.releaseInputs('forward')
        inputState.releaseInputs('reverse')


    def enterSwimMode(self, task = None):
        self.prevDistSq = -1


    def exitSwimMode(self, task = None):
        pass


    def setupAutoShipBoarding(self):
        self.accept('use-swim-controls', self.enterSwimMode)
        self.accept('use-walk-controls', self.exitSwimMode)
        self.accept('use-ship-controls', self.exitSwimMode)
        self.prevDistSq = -1


    def togglePrintAnimBlends(self):
        if not hasattr(self, '_printAnimBlends'):
            self._printAnimBlends = True
        else:
            self._printAnimBlends = not self._printAnimBlends

        if self._printAnimBlends:
            def doPrint(task, self = self):
                self.printAnimBlends()
                return task.cont

            taskMgr.add(doPrint, 'printAnimBlends')
        else:
            taskMgr.remove('printAnimBlends')


    def toggleOsdAnimBlends(self, enable = None):
        if not hasattr(self, '_osdAnimBlends'):
            self._osdAnimBlends = True
        else:
            self._osdAnimBlends = not (self._osdAnimBlends)

        if self._osdAnimBlends:
            def doOsd(task, self = self):
                self.osdAnimBlends()
                return task.cont

            taskMgr.add(doOsd, 'osdAnimBlends')
        else:
            taskMgr.remove('osdAnimBlends')

    def toggleAvVis(self):
        self.getLOD('2000').toggleVis()
        self.find('**/drop_shadow*').toggleVis()


    def getAddInterestEventName(self):
        return self.uniqueName('addInterest')


    def getRemoveInterestEventName(self):
        return self.uniqueName('removeInterest')


    def setInterest(self, parentId, zone, interestTags, event = None):
        context = self.cr.addInterest(parentId, zone, interestTags[0], event)
        if context:
            self.notify.debug('adding interest %d: %d %d' % (context.asInt(), parentId, zone))
            self.interestHandles.append([
                interestTags,
                context])
        else:
            self.notify.warning('Tried to set interest when shard was closed')

    def clearInterest(self, event):
        if len(self.interestHandles) > 0:
            contextInfo = self.interestHandles[0]
            self.notify.debug('removing interest %d' % contextInfo[1])
            self.cr.removeInterest(contextInfo[1], event)
            self.interestHandles.remove(contextInfo)

    def clearInterestNamed(self, callback, interestTags):
        toBeRemoved = []
        numInterests = 0
        for currContext in self.interestHandles:
            matchFound = False
            for currTag in interestTags:
                if currTag in currContext[0]:
                    matchFound = True
                    break

            if matchFound:
                context = currContext[1]
                self.notify.debug('removing interest %s' % context)
                self.cr.removeInterest(context, callback)
                toBeRemoved.append(currContext)
                numInterests += 1
                continue

        for currToBeRemoved in toBeRemoved:
            self.interestHandles.remove(currToBeRemoved)

        if numInterests == 0 and callback:
            messenger.send(callback)

        return numInterests

    def replaceInterestTag(self, oldTag, newTag):
        for i in xrange(len(self.interestHandles)):
            tags, ctx = self.interestHandles.pop(0)
            newTags = [tag if tag != oldTag else newTag for tag in tags]
            self.interestHandles.append([newTags, ctx])

    def teleportToShard(self, shardId, zoneId, callbackEvent):
        messenger.send(callbackEvent)

    def handleTeleportToShardDone(self, *args, **kw):
        pass

    def setLootCarried(self, *args, **kw):
        pass

    def printState(self, *args, **kw):
        pass

    def playOuch(self, *args, **kw):
        pass

    def getGetupTrack(self, *args, **kw):
        pass

    def hasEffect(self, *args, **kw):
        pass

    def setBattleTeleportFlag(self, *args, **kw):
        pass

    def clearBattleTeleportFlag(self, *args, **kw):
        pass

    def setupMovementSounds(self):
        self.sfxRunSand = loadSfx(SoundGlobals.SFX_AVATAR_RUN_SAND)
        self.sfxRunWood = loadSfx(SoundGlobals.SFX_AVATAR_RUN_WOOD)
        self.sfxRunCave = loadSfx(SoundGlobals.SFX_AVATAR_RUN_CAVE)
        self.sfxRunRock = loadSfx(SoundGlobals.SFX_AVATAR_RUN_ROCK)
        self.sfxRunGrass = loadSfx(SoundGlobals.SFX_AVATAR_RUN_GRASS)
        self.sfxRunGravel = loadSfx(SoundGlobals.SFX_AVATAR_RUN_GRAVEL)
        self.sfxRunWater = loadSfx(SoundGlobals.SFX_AVATAR_RUN_WATER)

        self.sfxWalkSand = loadSfx(SoundGlobals.SFX_AVATAR_WALK_SAND)
        self.sfxWalkWood = loadSfx(SoundGlobals.SFX_AVATAR_WALK_WOOD)
        self.sfxWalkCave = loadSfx(SoundGlobals.SFX_AVATAR_WALK_CAVE)
        self.sfxWalkRock = loadSfx(SoundGlobals.SFX_AVATAR_WALK_ROCK)
        self.sfxWalkGrass = loadSfx(SoundGlobals.SFX_AVATAR_WALK_GRASS)
        self.sfxWalkGravel = loadSfx(SoundGlobals.SFX_AVATAR_WALK_GRAVEL)
        self.sfxWalkWater = loadSfx(SoundGlobals.SFX_AVATAR_WALK_WATER)

    def _setShip(self, *args, **kw):
        pass

    def setShipId(self, shipId):
        DistributedPlayerPirate.setShipId(self, shipId)
        messenger.send('settingLocalShipId', [])

    def getMinimapObject(self):
        if not (self.minimapObj) and not self.isDisabled():
            self.minimapObj = MinimapLocalAvatar(self)

        return self.minimapObj


    def getGridMinimapObject(self):
        return self.getMinimapObject()

    def setAreaFootstep(self, soundString):
        self.levelFootStep = soundString

    def setSurfaceIndexFromLevelDefault(self):
        if self.levelFootStep == 'Sand':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_SAND)
        elif self.levelFootStep == 'Cave':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_CAVE)
        elif self.levelFootStep == 'Rock':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_ROCK)
        elif self.levelFootStep == 'Wood':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_WOOD)
        elif self.levelFootStep == 'Grass':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_GRASS)
        elif self.levelFootStep == 'Gravel':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_GRAVEL)
        else:
            self.setSurfaceIndex(PiratesGlobals.SURFACE_DEFAULT)

    def setSurfaceIndex(self, surfaceIndex):
        self.surfaceIndex = surfaceIndex
        if surfaceIndex == PiratesGlobals.SURFACE_DEFAULT:
            if self.levelFootStep:
                self.setSurfaceIndexFromLevelDefault()

        if self.surfaceIndex:
            self._changeMoveSound(self.surfaceIndex, self.movementIndex)

    def setMovementIndex(self, movementIndex):
        self.movementIndex = movementIndex
        if self.surfaceIndex != None:
            self._changeMoveSound(self.surfaceIndex, movementIndex)

    def getTrackedRotation(self, *args, **kw):
        rot = self.getH()
        if rot < 0:
            rot = 360 - rot

        time = globalClock.getDt()
        if time <= 0.0:
            time = 0.02

        self.trackedRotation.insert(0, (self.getH(), time))
        self.trackedRotation = self.trackedRotation[:3]
        rotationValue = 0.0
        lastRot = None
        rotTime = 0.0
        for rotation in self.trackedRotation:
            if lastRot:
                rot0 = lastRot
                rot1 = rotation[0]
                rotChange = ((rot1 - rot0) % 360 + 540) % 360 - 180
                rotationValue += rotChange / rotation[1]

            lastRot = rotation[0]

        RUNTHRES = 150
        RUNSTOPTHRES = 50
        STANDTHRES = 40
        STOPTHRES = 10
        if rotationValue >= 0.0:
            if rotationValue > RUNTHRES:
                pass
            elif rotationValue < STOPTHRES:
                self.trackedTurning = 0
            elif rotationValue > STANDTHRES and self.trackedTurning != 2:
                self.trackedTurning = 1
            elif self.trackedTurning == 2 and rotationValue < RUNSTOPTHRES:
                self.trackedTurning = 1

        elif rotationValue < -RUNTHRES:
            pass
        elif rotationValue > -STOPTHRES:
            self.trackedTurning = 0
        elif rotationValue < -STANDTHRES and self.trackedTurning != -2:
            self.trackedTurning = -1
        elif self.trackedTurning == -2 and rotationValue > -RUNSTOPTHRES:
            self.trackedTurning = -1

        return self.trackedTurning

    def _changeMoveSound(self, surfaceIndex, movementIndex):
        self.surfaceIndex = surfaceIndex
        self.movementIndex = movementIndex
        sound = None
        moveSound = self.movementIndex
        surface = self.surfaceIndex
        if moveSound == PiratesGlobals.RUN_INDEX or moveSound == PiratesGlobals.STRAFE_LEFT_INDEX or moveSound == PiratesGlobals.STRAFE_RIGHT_INDEX or moveSound == PiratesGlobals.STRAFE_LEFT_DIAG_INDEX or moveSound == PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX or moveSound == PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX or moveSound == PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX:
            if surface == PiratesGlobals.SURFACE_GRASS:
                sound = self.sfxRunGrass
            elif surface == PiratesGlobals.SURFACE_SAND:
                sound = self.sfxRunSand
            elif surface == PiratesGlobals.SURFACE_ROCK:
                sound = self.sfxRunRock
            elif surface == PiratesGlobals.SURFACE_WOOD:
                sound = self.sfxRunWood
            elif surface == PiratesGlobals.SURFACE_WATER or surface == PiratesGlobals.SURFACE_WATERWALK:
                sound = self.sfxRunWater
            elif surface == PiratesGlobals.SURFACE_CAVE:
                sound = self.sfxRunCave
            elif surface == PiratesGlobals.SURFACE_GRAVEL:
                sound = self.sfxRunGravel

        elif moveSound == PiratesGlobals.WALK_INDEX or moveSound == PiratesGlobals.REVERSE_INDEX or moveSound == PiratesGlobals.SPIN_LEFT_INDEX or moveSound == PiratesGlobals.SPIN_RIGHT_INDEX:
            if surface == PiratesGlobals.SURFACE_GRASS:
                sound = self.sfxWalkGrass
            elif surface == PiratesGlobals.SURFACE_SAND:
                sound = self.sfxWalkSand
            elif surface == PiratesGlobals.SURFACE_ROCK:
                sound = self.sfxWalkRock
            elif surface == PiratesGlobals.SURFACE_WOOD:
                sound = self.sfxWalkWood
            elif surface == PiratesGlobals.SURFACE_WATER or surface == PiratesGlobals.SURFACE_WATERWALK:
                sound = self.sfxWalkWater
            elif surface == PiratesGlobals.SURFACE_CAVE:
                sound = self.sfxWalkCave
            elif surface == PiratesGlobals.SURFACE_GRAVEL:
                sound = self.sfxWalkGravel

        if sound != self.curMoveSound:
            self.stopSound()
            if sound:
                base.playSfx(sound, looping = 1, node = self, volume = 0.3)

            self.curMoveSound = sound

        self.surfaceIndex = surfaceIndex
        self.movementIndex = movementIndex

    def stopSound(self):
        if self.curMoveSound:
            self.curMoveSound.stop()
            self.curMoveSound = None
            self.surfaceIndex = None
            self.movementIndex = None

    def refreshStatusTray(self):
        if self.isGenerated():
            self.guiMgr.gameGui.statusTray.updateHp(self.hp, self.maxHp)
            self.guiMgr.gameGui.statusTray.updateVoodoo(self.getTotalMojo(), self.maxMojo)
            self.guiMgr.gameGui.statusTray.updateStatusEffects(self.skillEffects)
            self.guiMgr.combatTray.updateBestTonic()
            if self.maxHp:
                hpFraction = float(self.hp) / float(self.maxHp)
                if hpFraction < 0.4:
                    self.guiMgr.gameGui.startHealthAlert()

    def getConeOriginNode(self):
        if self.cannon:
            return self.cannon.prop.pivot
        else:
            return self

    def composeRequestProjectileSkill(self, skillId, ammoSkillId, posHpr, charge = 0):
        timestamp = 0
        self.sendRequestProjectileSkill(skillId, ammoSkillId, posHpr, charge, timestamp)
        skillResult = WeaponGlobals.RESULT_DELAY
        self.playSkillMovie(skillId, ammoSkillId, skillResult, charge)


    def composeRequestTargetedSkill(self, skillId, ammoSkillId, combo = 0, charge = 0):
        newPos = self.cr.targetMgr.getAimHitPos(self)
        if newPos:
            pos = [
                newPos[0],
                newPos[1],
                newPos[2]]
        else:
            pos = [
                0,
                0,
                0]
        areaCenter = None
        if WeaponGlobals.getIsShipSkill(skillId) or ammoSkillId == InventoryType.ShipRepairKit:
            targetId = self.ship.getDoId()
            areaCenter = self.ship
            areaIdList = []
            if WeaponGlobals.getIsShout(skillId):
                if self.ship:
                    areaIdList = self.ship.getCrew()[:]
                    doId = self.getDoId()
                    if areaIdList.count(doId):
                        areaIdList.remove(doId)
        elif WeaponGlobals.getIsDollAttackSkill(skillId) and ItemGlobals.getType(self.currentWeaponId) == ItemGlobals.DOLL and skillId != InventoryType.DollAttune:
            targetId = 0
            areaIdList = copy.copy(self.stickyTargets)
            friendlySkill = WeaponGlobals.isFriendlyFire(skillId)
            toRemove = []
            for avId in areaIdList:
                av = self.cr.doId2do.get(avId)
                if av:
                    if friendlySkill and TeamUtils.damageAllowed(self, av):
                        toRemove.append(avId)
                    elif not friendlySkill and not TeamUtils.damageAllowed(self, av):
                        toRemove.append(avId)

            for currToRemove in toRemove:
                areaIdList.remove(currToRemove)

        elif self.currentTarget:
            targetId = self.currentTarget.getDoId()
            areaCenter = self.currentTarget
        else:
            targetId = 0
            areaCenter = self
        if areaCenter:
            areaIdList = self.getAreaList(skillId, ammoSkillId, areaCenter, Point3(*pos), self.doId)
        skillResult = self.cr.battleMgr.doAttack(self, skillId, ammoSkillId, targetId, areaIdList, Point3(*pos), combo, charge)
        if not (localAvatar.wantComboTiming) and combo == -1:
            if skillResult == WeaponGlobals.RESULT_HIT:
                skillResult = WeaponGlobals.RESULT_MISTIMED_HIT
            elif skillResult == WeaponGlobals.RESULT_MISS:
                skillResult = WeaponGlobals.RESULT_MISTIMED_MISS

        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE and WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            messenger.send('skillFinished')
            return None

        timestamp32 = 0
        self.sendRequestTargetedSkill(skillId, ammoSkillId, skillResult, targetId, areaIdList, timestamp32, pos, charge)
        (attackerEffects, targetEffects, itemEffects) = self.cr.battleMgr.getModifiedSkillEffects(self, self.currentTarget, skillId, ammoSkillId, charge)
        areaEffects = []
        for avId in areaIdList:
            av = base.cr.doId2do.get(avId)
            if av:
                skillTargetEffects = self.cr.battleMgr.getModifiedSkillEffects(self, av, skillId, ammoSkillId, charge)[1]
                areaEffects.append(skillTargetEffects)
                continue

        if skillId in (EnemySkills.STAFF_TOGGLE_AURA_WARDING, EnemySkills.STAFF_TOGGLE_AURA_NATURE, EnemySkills.STAFF_TOGGLE_AURA_DARK):
            if self.getAuraActivated():
                skillId = EnemySkills.STAFF_TOGGLE_AURA_OFF


        self.useTargetedSkill(skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaEffects, itemEffects, timestamp32, pos, charge, localSignal = 1)
        if attackerEffects != [
            0,
            0,
            0,
            0,
            0]:
            self.targetedWeaponHit(skillId, ammoSkillId, WeaponGlobals.RESULT_HIT, attackerEffects, self, pos)



    def composeRequestShipSkill(self, skillId, ammoSkillId):
        targetId = self.ship.getDoId()
        areaCenter = self.ship
        areaIdList = []
        skillResult = self.cr.battleMgr.doAttack(self, skillId, ammoSkillId, targetId, areaIdList, Point3(0, 0, 0), 0)
        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE and WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            messenger.send('skillFinished')
            return None

        timestamp32 = 0
        self.sendRequestShipSkill(skillId, ammoSkillId, skillResult, targetId, timestamp32)
        (selfEffects, targetEffects, itemEffects) = self.cr.battleMgr.getModifiedSkillEffects(self, self.currentTarget, skillId, ammoSkillId)
        target = base.cr.doId2do.get(targetId)
        if target:
            target.useShipSkill(skillId, ammoSkillId, skillResult, targetId, selfEffects, targetEffects, timestamp32, localSignal = 1)

        self.skillDiary.startRecharging(skillId, ammoSkillId)


    def initCombatTray(self, rep):
        self.guiMgr.combatTray.initCombatTray(rep)


    def setStickyTargets(self, avList):
        DistributedPlayerPirate.setStickyTargets(self, avList)
        self.guiMgr.targetStatusTray.updateSticky(self.stickyTargets)
        if self.stickyTargets == []:
            taskMgr.remove(self.uniqueName('monitorStickyTargets'))
        else:
            self.startMonitorStickyTargets()


    def startMonitorStickyTargets(self):
        self.lastTick = 0
        if not taskMgr.hasTaskNamed(self.uniqueName('monitorStickyTargets')):
            taskMgr.add(self.monitorStickyTargets, self.uniqueName('monitorStickyTargets'))



    def monitorStickyTargets(self, task):
        TICK_DELAY = 1.0
        if task.time - self.lastTick > TICK_DELAY:
            for avId in self.stickyTargets:
                av = base.cr.doId2do.get(avId)
                if av is None or self.getDistance(av) > WeaponGlobals.getAttackRange(InventoryType.DollPoke) or av.isInvisibleGhost():
                    self.d_removeStickyTargets([avId])
                    continue

            self.lastTick = task.time

        return task.cont


    def openJailDoor(self, index = 1):
        stringIndex = str(index)
        jail = self.getParent().getParent()
        if jail == None or jail.isEmpty():
            return None

        jail_door = jail.find('**/jail_door0' + stringIndex)
        jail_lock = jail.find('**/lock0' + stringIndex)
        jail_door_collision = jail.find('**/door_collision_0' + stringIndex)
        seq = Sequence(LerpHprInterval(jail_door, 1, VBase3(120, jail_door.getP(), jail_door.getR()), blendType = 'easeInOut'), duration = 1.0)
        seq.start()
        self.openJailDoorTrack = seq
        jail_door_collision.setR(30)
        if not jail_lock.isEmpty():
            jail_lock.stash()



    def beginTrackTarget(self, target, timer = -1):
        self.lookAtTarget = target
        self.lookAtTimer = timer
        taskMgr.add(self.trackTarget, 'localAvTrackTarget')


    def trackTarget(self, task):
        if self.lookAtTimer >= 0:
            if task.time > self.lookAtTimer:
                return task.done


        self.lookAt(self.lookAtTarget)
        return task.cont


    def endTrackTarget(self):
        taskMgr.remove('localAvTrackTarget')
        self.lookAtTarget = None


    def startLookAtTarget(self):
        self.stopLookAroundTask()
        taskMgr.remove('localAvLookAtTarget')
        taskMgr.add(self.__lookAtTarget, 'localAvLookAtTarget', 49)


    def __lookAtTarget(self, task):
        if self.currentTarget and not self.currentTarget.isEmpty():
            if self.currentTarget.getY(self) < 0.0:
                self.headNode.setHpr(0, 0, 0)
            else:
                hFov = 120
                vFov = 60
                fromNode = self.lookFromNode
                toNode = self.lookToNode
                toNode.reparentTo(self.currentTarget)
                toNode.setZ(self.currentTarget.getHeight())
                fromNode.lookAt(toNode)
                pitch = max(-vFov * 0.5, min(vFov * 0.5, fromNode.getP()))
                heading = max(-hFov * 0.5, min(hFov * 0.5, fromNode.getH()))
                self.headNode.setHpr(0, heading, -pitch)
                toNode.detachNode()
        else:
            self.headNode.setHpr(0, 0, 0)
        return task.cont


    def stopLookAtTarget(self):
        taskMgr.remove('localAvLookAtTarget')
        self.lookToNode.detachNode()


    def testFacing(self):
        self.lastTick = 0
        taskMgr.add(self.findLegalTargets, self.uniqueName('findLegalTargets'))


    def findLegalTargets(self, task):
        TICK_DELAY = 0.5
        if task.time - self.lastTick > TICK_DELAY:
            for do in self.cr.doId2do.values():
                if hasattr(do, 'isNpc') and do.doId != self.doId:
                    self.checkViewingArc(do)
                    continue

            self.lastTick = task.time

        return task.cont


    def checkViewingArc(self, target):
        self.lookAtDummy.lookAt(target)
        targetHeading = self.lookAtDummy.getH()
        if targetHeading > -45 and targetHeading < 45:
            return 1
        else:
            return 0


    def addWobbleId(self, doId):
        oldLen = len(self.wobbleList)
        if doId not in self.wobbleList and doId != self.doId:
            self.wobbleList.append(doId)

        if len(self.wobbleList) and oldLen == 0:
            self.startFovWobble()



    def removeWobbleId(self, doId):
        while doId in self.wobbleList:
            self.wobbleList.remove(doId)
        if len(self.wobbleList) == 0:
            self.stopFovWobble()



    def startFovWobble(self):
        self.normFov = base.camLens.getFov() * 1.0
        self.minFov = self.normFov * 0.989
        self.maxFov = self.normFov * 1.01
        self.fovWobbleDir = 0
        self.doFovWobble()


    def doFovWobble(self, task = None):
        if self.fovIval:
            self.fovIval.pause()
            self.fovIval = None

        closestWobble = 100.0
        if len(self.wobbleList) == 0:
            if task:
                return task.done
            else:
                return None

        for id in self.wobbleList:
            av = go(id)
            if av:
                distance = localAvatar.getDistance(av)
                if distance < closestWobble:
                    closestWobble = distance

            distance < closestWobble

        distanceFactor = closestWobble / 50.0
        iDistanceFactor = 1 - distanceFactor
        if distanceFactor > 1.0:
            self.stopFovWobble()
            taskMgr.remove('wobbleLater')
            taskMgr.doMethodLater(3.0, self.doFovWobble, 'wobbleLater')
            if task:
                return task.done
            else:
                return None
        else:
            taskMgr.remove('wobbleLater')
        minFov = self.normFov - 0.200 * math.sqrt(iDistanceFactor)
        maxFov = self.normFov + 0.200 * math.sqrt(iDistanceFactor)
        minRoll = 0.0 - 0.5 * math.sqrt(iDistanceFactor)
        maxRoll = 0.0 + 0.5 * math.sqrt(iDistanceFactor)
        if self.fovWobbleDir == 0:
            fromFov = self.normFov
            toFov = maxFov
            fromRoll = 0
            toRoll = maxRoll
            self.fovWobbleDir = -1
        elif self.fovWobbleDir == 1:
            fromFov = minFov
            toFov = maxFov
            fromRoll = minRoll
            toRoll = maxRoll
            self.fovWobbleDir = -1
        elif self.fovWobbleDir == -1:
            fromFov = maxFov
            toFov = minFov
            fromRoll = maxRoll
            toRoll = minRoll
            self.fovWobbleDir = 1

        self.fovIval = Sequence(LerpFunctionInterval(self.setCamRoll, fromData = fromRoll, toData = toRoll, duration = 2.5 + 3.0 * distanceFactor, blendType = 'easeInOut'), Func(self.doFovWobble))
        self.fovIval.start()
        if task:
            return task.cont



    def setCamFov(self, fov):
        base.camLens.setFov(fov)


    def setCamRoll(self, fov):
        base.cam.setR(fov)


    def stopFovWobble(self):
        if self.fovIval:
            self.fovIval.pause()
            self.fovIval = None
            base.camLens.setFov(self.normFov)
            base.cam.setR(0)



    def _setCreatureTransformation(self, value, effectId):
        if self.creatureTransformation == value:
            return None

        if value:
            pass
        1
        taskMgr.doMethodLater(0.100, self.fakeEnemyAggroTask, 'fakeEnemyAggroTask')
        self.fakeEnemyAggroTask(None)
        DistributedPlayerPirate._setCreatureTransformation(self, value, effectId)


    def setCreatureTransformation(self, value, effectId, timeSince = 0):
        if self.creatureTransformation == value:
            return None

        if value:
            if not self.gameFSM.isInTransition() and self.getGameState() in [
                'Battle']:
                self.b_setGameState('LandRoam')


        DistributedPlayerPirate.setCreatureTransformation(self, value, effectId, timeSince)

    def setAvatarViewTarget(self, targetId = None):
        if localAvatar.guiMgr.profilePage and localAvatar.guiMgr.profilePage.profileId:
            avatar = base.cr.doId2do.get(localAvatar.guiMgr.profilePage.profileId)
            if avatar:
                self.sendUpdate('setAvatarViewTarget', [
                    int(localAvatar.guiMgr.profilePage.profileId),
                    avatar.getName()])
                return None


        self.sendUpdate('setAvatarViewTarget', [
            0])


    def acknowledgeViewTarget(self, targetId):
        avName = 'unknown'
        avatar = base.cr.doId2do.get(targetId)
        if avatar:
            avName = avatar.getName()

        message = 'Setting Target to Avatar Id:%s Name:%s' % (targetId, avName)
        base.talkAssistant.receiveGameMessage(message)


    def displayWhisper(self, fromAvId, chatString, whisperType):
        if base.localAvatar.isIgnored(fromAvId):
            return

        sender = base.cr.identifyAvatar(fromAvId)
        if not sender:
            self.notify.warning('displayWhisper: fromAvId: %s not found' % fromAvId)
            return

        if self.soundWhisper:
            base.playSfx(self.soundWhisper)


    def displayTalkWhisper(self, fromId, avatarName, chatString):
        if base.localAvatar.isIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return

        if self.soundWhisper:
            base.playSfx(self.soundWhisper)

        base.talkAssistant.receiveWhisperTalk(fromId, avatarName, chatString)

    def whisperTo(self, chatString, sendToId):
        recv = base.cr.identifyAvatar(sendToId)
        if recv:
            panelString = 'To %s: %s' % (recv.getName(), chatString)
        else:
            panelString = chatString
        DistributedPlayerPirate.whisperTo(self, chatString, sendToId)


    def setKickEvents(self, kickEventStart, kickEventConnect):
        self.kickEvents = [
            kickEventStart,
            kickEventConnect]


    def spendSkillPoint(self, skillId):
        self.sendUpdate('spendSkillPoint', [skillId])


    def checkForAutoTrigger(self, objDoId):
        avInv = self.getInventory()
        if avInv == None:
            return None

        questList = avInv.getQuestList()
        objRef = self.cr.doId2do.get(objDoId)
        if objRef == None:
            return None

        instanceArea = False
        for currQuest in questList:
            questDNA = currQuest.getQuestDNA()
            if questDNA:
                questTasks = questDNA.getTasks()
            else:
                self.notify.warning('quest %s: does not contain a dna; is it a rogue quest, given in error?' % currQuest.getQuestId())
                return None
            for currTask in questTasks:
                autoTriggerInfo = currTask.getAutoTriggerInfo()
                if len(autoTriggerInfo) > 0 and autoTriggerInfo[0] == QuestDB.AUTO_TRIGGER_OBJ_EXISTS:
                    firstObjId = autoTriggerInfo[1][0]
                    allObjsPresent = True
                    if objRef.getUniqueId() == firstObjId:
                        for objId in autoTriggerInfo[1]:
                            doId = self.cr.uidMgr.uid2doId.get(objId)
                            if self.cr.doId2do.get(doId) == None:
                                allObjsPresent = False
                                break
                                continue

                        if allObjsPresent:
                            if questDNA.getQuestId() == 'c2.11visitBarbossa':
                                if avInv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:

                                    def checkForKickOut(task):
                                        if self.getParentObj().getUniqueId() == LocationIds.ANVIL_CAVE_BARBOSA:
                                            base.cr.activeWorld.worldGrid.quickLoadOtherSide()
                                            taskMgr.doMethodLater(1, checkForKickOut, 'checkForKickOut')


                                    taskMgr.doMethodLater(0.100, checkForKickOut, 'checkForKickOut')
                                    return None
                                else:
                                    objRef.pistolTutorialPt1()

                            objRef.handleUseKey()
                        else:
                            taskMgr.doMethodLater(3, objRef.autoTriggerCheck, objRef.uniqueName('autoTriggerCheck'), extraArgs = [])
                        return None

                objRef.getUniqueId() == firstObjId




    def swapFloorCollideMask(self, oldMask, newMask):
        cMask = self.cFloorNodePath.node().getFromCollideMask()
        cMask = cMask & ~oldMask
        cMask |= newMask
        self.cFloorNodePath.node().setFromCollideMask(cMask)
        for name in [
            'walk',
            'battle',
            'swim']:
            controls = self.controlManager.get(name)
            if controls:
                controls.swapFloorBitMask(oldMask, newMask)
                continue



    def handleArrivedOnShip(self, ship):
        DistributedPlayerPirate.handleArrivedOnShip(self, ship)
        ship.localPirateArrived(self)
        self.ship = ship
        if __dev__:
            __builtins__['ship'] = ship

        self.refreshActiveQuestStep()
        self.guiMgr.setMinimap(ship.getMinimap())
        self.guiMgr.radarGui.showLocation('The_High_Seas')
        self.setSurfaceIndex(PiratesGlobals.SURFACE_WOOD)
        if self.getTutorialState() >= 3:
            base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_SAILING, { })

    def handleLeftShip(self, ship):
        DistributedPlayerPirate.handleLeftShip(self, ship)
        ship.localPirateLeft(self)
        self.ship = None
        if __dev__:
            __builtins__['ship'] = None

        self.guiMgr.combatTray.skillTray.removePowerRechargeEffect()
        minimap = ship.getMinimap()
        self.guiMgr.clearMinimap(minimap)

    def placeOnShip(self, ship, pvp = False):
        messenger.send('islandPlayerBarrier', [
            0])
        self.b_setLocation(ship.doId, PiratesGlobals.ShipZoneOnDeck)

        try:
            (pos, h) = ship.getClosestBoardingPosH()
        except:
            self.notify.error('ship %s boarding failed' % str(ship.getLocation()))

        self.setPos(pos)
        self.setH(h)
        localAvatar.b_setGameState('LandRoam')
        self.setPos(pos)
        self.setH(h)
        ship.turnOn()
        ship.localAvatarBoardShip()
        self.enterZoneLOD(ship)
        self.cnode.broadcastPosHprFull()
        ship.sendUpdate('shipBoarded')

    def removeFromShip(self, ship):
        ship.disableOnDeckInteractions()
        ship.localAvatarExitShip()

    def startAutoRun(self):
        if self.enableAutoRun:
            return None

        self.enableAutoRun = 1
        self.setAutoRun(1)
        self.accept('arrow_up', self.stopAutoRun)
        self.accept('arrow_down', self.stopAutoRun)
        self.accept('w', self.stopAutoRun)
        self.accept('s', self.stopAutoRun)


    def stopAutoRun(self):
        if not self.enableAutoRun:
            return None

        self.enableAutoRun = 0
        self.setAutoRun(0)
        self.ignore('arrow_up')
        self.ignore('arrow_down')
        self.ignore('w')
        self.ignore('s')


    def getName(self):
        return self.title + self.name


    def doShowReset(self):
        self.showQuest = True


    def resetQuestShow(self):
        self.showQuest = False
        taskMgr.doMethodLater(2.0, self.doShowReset, self.uniqueName('questShow'), extraArgs = [])


    def setGuildId(self, guildId):
        DistributedPlayerPirate.setGuildId(self, guildId)
        if self.guildId:
            self.chatMgr.enableGuildChat()
        else:
            self.chatMgr.disableGuildChat()


    def setBandId(self, bandmanager, bandId):
        DistributedPlayerPirate.setBandId(self, bandmanager, bandId)
        if self.BandId:
            self.chatMgr.enableCrewChat()
        else:
            self.chatMgr.disableCrewChat()


    def setSiegeTeam(self, team):
        self._siegeTeamSV.set(team)
        if team:
            self.chatMgr.enableShipPVPChat()
        else:
            self.chatMgr.disableShipPVPChat()
        DistributedPlayerPirate.setSiegeTeam(self, team)

    def setTutorial(self, *args, **kw):
        pass

    def startOceanCheck(self):
        if not taskMgr.hasTaskNamed(self.uniqueName('oceanCheck')):
            taskMgr.doMethodLater(10, self.checkCurrentOcean, self.uniqueName('oceanCheck'))

    def checkCurrentOcean(self, task):
        if self.ship:
            pos = self.ship.getPos(render)
            newOcean = OceanZone.getOceanZone(pos[0], pos[1])
            if self.currentOcean != newOcean:
                self.currentOcean = newOcean
                self.guiMgr.flashOceanMsg(PLocalizer.OceanZoneNames.get(newOcean))

            return task.again
        else:
            return task.done

    def l_setActiveQuest(self, questId):
        DistributedPlayerPirate.l_setActiveQuest(self, questId)
        if hasattr(self.guiMgr, 'questPage'):
            if self.guiMgr.questPage is not None:
                self.guiMgr.questPage.titleList.showTracked(questId)

    def enableWaterEffect(self):
        self.setSurfaceIndex(PiratesGlobals.SURFACE_WATERWALK)
        DistributedPlayerPirate.enableWaterEffect(self)

    def disableWaterEffect(self):
        self.setSurfaceIndex(PiratesGlobals.SURFACE_DEFAULT)
        DistributedPlayerPirate.disableWaterEffect(self)

    def adjustWaterEffect(self, offset, forwardSpeed = 0.0, rotateSpeed = 0.0, slideSpeed = 0.0):
        if self.getGameState() == 'LandRoam':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_WATERWALK)
        elif self.getGameState() == 'WaterRoam':
            self.setSurfaceIndex(PiratesGlobals.SURFACE_WATER)

        DistributedPlayerPirate.adjustWaterEffect(self, offset, forwardSpeed, rotateSpeed, slideSpeed)

    def handleWaterIn(self, entry):
        self.enableWaterEffect()

    def handleWaterAgain(self, entry):
        offset = entry.getSurfacePoint(self).getZ()
        if offset < 0.0:
            self.disableWaterEffect()
        else:
            speeds = self.controlManager.getSpeeds()
            self.adjustWaterEffect(offset + 0.149, *speeds)

    def handleWaterOut(self, entry):
        self.disableWaterEffect()

    def spawnWiggle(self):
        randX = random.randrange(-2, 3, 2)
        randY = random.randrange(-2, 3, 2)
        pos = self.getPos()
        self.setPos(pos[0] + randX, pos[1] + randY, pos[2])

    def setLifterDelayFrames(self, frames = 0):
        self.motionFSM.setLifterDelayFrames(frames)

    def queueStoryQuest(self, quest):
        self.currentStoryQuests.append(quest)
        if self.style.getTutorial() >= PiratesGlobals.TUT_GOT_SEACHEST and quest.getQuestId() == self.activeQuestIdPending:
            self.b_requestActiveQuest(quest.getQuestId())
            self.guiMgr.initQuestPage()
            self.activeQuestIdPending = ''

    def resetStoryQuest(self):
        self.currentStoryQuests = []


    def triggerNPCInteract(self):
        quest = self.getQuestById(self.activeQuestId)
        questGiverUid = quest.questDNA.getTasks()[0].npcId
        questGiverDoId = base.cr.uidMgr.uid2doId[questGiverUid]
        questGiver = base.cr.doId2do[questGiverDoId]
        questGiver.setQuestsCompleted(1, [
            self.activeQuestId], [], [], [])

    def leaveZoneLOD(self, zoneLODObj):
        if __dev__:
            import pirates.world.ZoneLOD as ZoneLOD

        zoneLODObj.setZoneLevelOuter()

    def enterZoneLOD(self, zoneLODObj):
        if self.controlManager.currentControls:
            collisionsOn = self.controlManager.currentControls.getCollisionsActive()
            self.collisionsOn()
            eventMgr.doEvents()
            self.controlManager.currentControls.cTrav.traverse(render)
            base.shadowTrav.traverse(render)
            eventMgr.doEvents()
            zoneLODObj.disableAllLODSpheres()
            self.controlManager.currentControls.cTrav.traverse(render)
            base.shadowTrav.traverse(render)
            eventMgr.eventQueue.clear()
            zoneLODObj.enableAllLODSpheres()
            self.controlManager.currentControls.cTrav.traverse(render)
            base.shadowTrav.traverse(render)
            eventMgr.doEvents()
            zoneLODObj.clearAllEnabled(True)
            if not collisionsOn:
                self.collisionsOff()

        else:
            self.notify.warning('localAvatar has no controls during teleport')

    def addStatusEffect(self, effectId, attackerId, duration, timeLeft, timestamp, buffData):
        DistributedPlayerPirate.addStatusEffect(self, effectId, attackerId, duration, timeLeft, timestamp, buffData)
        if effectId == WeaponGlobals.C_STUN or effectId == WeaponGlobals.C_KNOCKDOWN:
            if self.getGameState() not in ('Injured',):
                self.motionFSM.off()

    def removeStatusEffect(self, effectId, attackerId):
        DistributedPlayerPirate.removeStatusEffect(self, effectId, attackerId)
        if effectId == WeaponGlobals.C_STUN or effectId == WeaponGlobals.C_KNOCKDOWN:
            self.considerEnableMovement()

    def setDefaultShard(self, defaultShard):
        DistributedPlayerPirate.setDefaultShard(self, defaultShard)
        self.logDefaultShard()

    def logDefaultShard(self):
        pcrCat = DirectNotifyGlobal.directNotify.getCategory('PiratesClientRepository')
        sev = pcrCat.getSeverity()
        pcrCat.info('Current shard is: %s' % self.getDefaultShard())
        pcrCat.setSeverity(sev)

    def enableCloudScudEffect(self):
        if self.cloudScudEffect:
            return None

        self.cloudScudEffect = CloudScud.getEffect()
        if self.cloudScudEffect:
            self.cloudScudEffect.reparentTo(self)
            self.cloudScudEffect.startLoop()



    def disableCloudScudEffect(self):
        if self.cloudScudEffect:
            self.cloudScudEffect.stopLoop()
            self.cloudScudEffect = None



    def teleportCleanupComplete(self, instanceType):
        base.loadingScreen.beginStep('scheduleHide', 33, 16)
        if not self.belongsInJail():
            self.b_setGameState(self.gameFSM.defaultState)

        self.setLifterDelayFrames(frames = 3)
        self.cr.loadingScreen.scheduleHide(self.cr.getAllInterestsCompleteEvent())
        self.acceptOnce(self.cr.getAllInterestsCompleteEvent(), taskMgr.doMethodLater, [
            1,
            self.doFadeIn,
            self.taskName('irisIn')])
        if instanceType == PiratesGlobals.INSTANCE_PVP:
            self.setTeleportFlag(PiratesGlobals.TFInPVP)
        elif instanceType == PiratesGlobals.INSTANCE_TUTORIAL:
            self.setTeleportFlag(PiratesGlobals.TFInTutorial)

    def doFadeIn(self, task):

        try:
            if not self.belongsInJail() and self.getGameState() not in ('WaterRoam', 'Healing', 'Cannon'):
                self.b_setGameState(self.gameFSM.defaultState)

            return task.done
        except AttributeError:
            task.fadeInDone = 1
            tutorialException = base.cr.tutorial & (self.style.tutorial == PiratesGlobals.TUT_STARTED)
            if not tutorialException:
                base.transitions.fadeIn()

            if self.teleportFriendDoId:
                friendId = self.teleportFriendDoId
                self.teleportFriendDoId = 0

            return task.again

    def setSoloInteraction(self, solo):
        self.soloInteraction = solo
        if solo:
            messenger.send('hideOtherAvatars')
        else:
            messenger.send('showOtherAvatars')

    def getSoloInteraction(self):
        return self.soloInteraction

    def initVisibleToCamera(self):
        pass

    def isStateAIProtected(self):
        if self.getGameState() in PlayerStateGlobals.protectedStates:
            return 1
        else:
            return 0

    def setGameState(self, gameState, timestamp = None, localArgs = [], localChange = 0):
        protected = self.isStateAIProtected()
        if localChange:
            protected = False

        override = gameState in PlayerStateGlobals.overrideStates

        if (not protected) or override:
            DistributedPlayerPirate.setGameState(self, gameState, timestamp, localArgs)
            if self.getGameState() not in ('LandRoam',):
                self.cameraFSM.getFPSCamera().ignoreWheel()

    def motionFSMEnterState(self, anim):
        if anim == 'Idle' and self.getGameState() in ('LandRoam',):
            self.cameraFSM.getFPSCamera().acceptWheel()
        else:
            self.cameraFSM.getFPSCamera().ignoreWheel()

    def motionFSMExitState(self, anim):
        if anim == 'Idle':
            self.cameraFSM.getFPSCamera().ignoreWheel()

    def goAFK(self, task):
        if not self.isAFK:
            self.toggleAFK()

        return task.done

    def checkInputState(self, msg = None):
        if msg is True:
            self.delayAFK()

    def checkAction(self, *a, **b):
        self.delayAFK()

    def delayAFK(self, msg = None):
        if self.isAFK:
            self.toggleAFK()
        else:
            taskMgr.remove('autoAFK')
            taskMgr.doMethodLater(self.AFKDelay, self.goAFK, 'autoAFK')

    def toggleAFK(self):
        self.b_setAFK(not (self.isAFK))
        if self.isAFK and self.getGameState() not in [
            'Emote',
            'Injured']:
            self.requestEmote(EmoteGlobals.EMOTE_SLEEP)

        if not (self.isAFK) and self.getGameState() == 'Emote':
            self.b_setGameState('LandRoam')

        if not self.isAFK:
            taskMgr.remove('autoAFK')
            taskMgr.doMethodLater(self.AFKDelay, self.goAFK, 'autoAFK')

    def gotSpecialReward(self, *args, **kw):
        pass

    def addLocalProjectile(self, *args, **kw):
        pass

    def clearLocalProjectile(self, *args, **kw):
        pass

    def cleanupLocalProjectiles(self, *args, **kw):
        pass

    def addShipTarget(self, *args, **kw):
        pass

    def setCannonAmmoSkillId(self, *args, **kw):
        pass

    def getCannonAmmoSkillId(self, *args, **kw):
        pass

    def getShortName(self, *args, **kw):
        pass

    def getLevel(self):
        if self.level == 0 or self.level == None:
            level = 0
            totalReputation = 0
            inv = self.getInventory()
            if inv:
                for repCat in ReputationGlobals.getReputationCategories():
                    totalReputation += inv.getReputation(repCat)

                (level, leftover) = ReputationGlobals.getLevelFromTotalReputation(InventoryType.OverallRep, totalReputation)

            self.level = level

        return self.level

    def setBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setBadgeIcon(self, titleId, rank)
        messenger.send('landBadgeSet', [
            titleId,
            rank])
        self.refreshName()

    def setShipBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setShipBadgeIcon(self, titleId, rank)
        messenger.send('seaBadgeSet', [
            titleId,
            rank])

    def changeBodyType(self):
        if self.gameFSM.getCurrentOrNextState() == 'Battle':
            self.b_setGameState('LandRoam')

        DistributedPlayerPirate.changeBodyType(self)

    def setAvatarSkinCrazy(self, value, colorIndex = 0, timeSince = 0):
        if self.crazyColorSkin == value:
            return

        if self.gameFSM.getCurrentOrNextState() == 'Battle':
            self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId, self.currentWeaponSlotId)

        DistributedPlayerPirate.setAvatarSkinCrazy(self, value, colorIndex, timeSince)

    def playCurse(self):
        from pirates.effects.JRSpawn import JRSpawn
        self.zombieEffect = JRSpawn.getEffect()
        if self.zombieEffect:
            self.zombieEffect.reparentTo(self)
            self.zombieEffect.setPos(0, 1, 0)
            self.zombieIval = Sequence(Func(localAvatar.motionFSM.off), Func(self.zombieEffect.play), Func(localAvatar.play, 'death3'), Wait(1.7), Func(DistributedPlayerPirate.setZombie, self, True, True), Func(localAvatar.play, 'jail_standup', fromFrame = 65), Wait(2.25), Func(localAvatar.motionFSM.on))
            self.zombieIval.start()

    def setZombie(self, value, cursed):
        if self.zombie == value:
            return

        if self.gameFSM.getCurrentOrNextState() == 'Fishing':
            curInteractive = base.cr.interactionMgr.getCurrentInteractive()
            if curInteractive:
                curInteractive.requestExit()
                taskMgr.doMethodLater(2, self.setZombie, self.uniqueName('setZombie'), extraArgs=[value, cursed])
                return

        elif self.gameFSM.getCurrentOrNextState() == 'NPCInteract':
            curInteractive = base.cr.interactionMgr.getCurrentInteractive()
            if curInteractive and curInteractive.avatarType.isA(AvatarTypes.Fishmaster):
                curInteractive.requestExit()
                taskMgr.doMethodLater(2, self.setZombie, self.uniqueName('setZombie'), extraArgs=[value, cursed])

        if value:
            self.b_setTeleportFlag(PiratesGlobals.TFZombie)

        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFZombie)

        if value and cursed:
            messenger.send('LocalAvatarIsZombie')

        if self.currentWeapon:
            self.currentWeapon.detachNode()

        if cursed and not self.zombie and self.gameFSM.getCurrentOrNextState() != 'WaterRoam':
            self.playCurse()

        else:
            DistributedPlayerPirate.setZombie(self, value)

    def setCurseStatus(self, value):
        if value == 0:
            base.cr.newsManager.displayMessage(6)

        elif value == 1:
            base.cr.newsManager.displayMessage(5)
            base.playSfx(self.jollySfx)

        elif value == 2:
            base.cr.newsManager.displayMessage(4)

    def getAllowSocialPanel(self):
        return True # always setting this true for now, tutorial status doesn't matter in Alpha
        #if hasattr(self, 'allowSocialPanel'):
        #    return self.allowSocialPanel

    def setAllowSocialPanel(self, allow):
        self.allowSocialPanel = allow

    def displayMoraleMessage(self):
        inv = self.getInventory()
        if inv and self.getLevel() > 9:
            if not inv.getStackQuantity(InventoryType.Groggy):
                self.sendRequestContext(InventoryType.Groggy)

    def __cleanupMoraleDialog(self, value=None):
        if self.moralePopupDialog:
            self.moralePopupDialog.destroy()
            self.moralePopupDialog = None

    def __destroyedMoraleDialog(self):
        self.moralePopupDialog = None

    def guildStatusUpdate(self, guildId, guildName, guildRank):
        self.setGuildId(guildId)
        self.setGuildRank(guildRank)
        self.setGuildName(guildName)
        self.guiMgr.guildPage.initGuildPage()
        messenger.send('Guild Status Updated')

    def guildNameRequest(self):
        self.guildPopupDialog = PDialog.PDialog(text=PLocalizer.GuildNameRequest, style=OTPDialog.Acknowledge, text_align=TextNode.ACenter, command=self.__cleanupGuildDialog, destroyedCallback=self.__destroyedGuildDialog)

    def guildNameReject(self, code):
        if code == 0:
            text = PLocalizer.GuildNameNotGM
        elif code == 1:
            text = PLocalizer.GuildNameAlreadySubmitted
        elif code == 2:
            text = PLocalizer.GuildNameDuplicate

        self.guildPopupDialog = PDialog.PDialog(text=text, style=OTPDialog.Acknowledge, command=self.__cleanupGuildDialog, destroyedCallback = self.__destroyedGuildDialog)
        self.guiMgr.guildPage.resetRenameButton()

    def guildNameChange(self, guildName, change):
        if change == 1:
            title = PLocalizer.GuildNameRejectTitle
            mess = PLocalizer.GuildNameReject % guildName
        else:
            title = PLocalizer.GuildNameApproveTitle
            mess = PLocalizer.GuildNameApprove % guildName

        self.__cleanupGuildDialog()
        self.guildPopupDialog = PDialog.PDialog(text=mess, title_text=title, text_align=TextNode.ACenter, text_pos=(0, -0.4), style=OTPDialog.Acknowledge, command=self.__cleanupGuildDialog, destroyedCallback=self.__destroyedGuildDialog)

    def __cleanupGuildDialog(self, value = None):
        if self.guildPopupDialog:
            self.guildPopupDialog.destroy()
            self.guildPopupDialog = None

    def __destroyedGuildDialog(self):
        self.guildPopupDialog = None

    def getCanLogout(self):
        return self.getGameState() != 'Cutscene'

    def teleportQuery(self, requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId):
        if self.isGenerated():
            self.cr.teleportMgr.handleAvatarTeleportQuery(requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId)

    def teleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
        if self.isGenerated():
            self.cr.teleportMgr.handleAvatarTeleportResponse(avId, available, shardId, instanceDoId, areaDoId)

    def requestCombatMusic(self):
        taskMgr.remove('stopCombatMusic')
        if not self.currCombatMusic:
            if self.ship:
                self.currCombatMusic = SoundGlobals.MUSIC_SHIP_COMBAT

            elif self.getParentObj():
                if not hasattr(self.getParentObj(), 'uniqueId'):
                    self.currCombatMusic = None

                elif self.inInvasion:
                    self.currCombatMusic = None

                elif SoundGlobals.getCombatMusic(self.getParentObj().uniqueId):
                    self.currCombatMusic = SoundGlobals.getCombatMusic(self.getParentObj().uniqueId)

                else:
                    self.currCombatMusic = SoundGlobals.getCombatMusic(getParentIsland(self.getParentObj().uniqueId))


        if self.currCombatMusic:
            base.musicMgr.request(self.currCombatMusic, priority=3, looping=1, volume=.6)
            taskMgr.doMethodLater(12, self.stopCombatMusic, 'stopCombatMusic')

    def stopCombatMusic(self, task = None):
        taskMgr.remove('stopCombatMusic')
        if self.currCombatMusic:
            base.musicMgr.requestFadeOut(self.currCombatMusic)
            self.currCombatMusic = None

    def setEfficiency(self, efficiency):
        if efficiency != self.efficiency:
            self.efficiency = efficiency

            if self.efficiency:
                base.options.setInvasion(True)
                PooledEffect.setGlobalLimit(20)
                messenger.send('grid-detail-changed', [Options.option_low])
                base.options.setRuntimeSpecialEffects()
                base.setNoticeSystem(0)
                messenger.send('Local_Efficiency_Set', [self.efficiency])

            else:
                PooledEffect.setGlobalLimit(200)
                messenger.send('grid-detail-changed', [base.options.terrain_detail_level])
                base.options.setRuntimeSpecialEffects()
                base.setNoticeSystem(1)
                messenger.send('Local_Efficiency_Set', [self.efficiency])

    def setBoardedShip(self, boardedShip):
        if boardedShip != self.boardedShip:
            self.boardedShip = boardedShip
            messenger.send('localAvatar-BoardedShip', [self.boardedShip])

    def getGridMinimapObject(self):
        return self.getMinimapObject()

    def setVisZone(self, visZone):
        pass

    def b_boardShip(self, shipDoId, boardingSpot):
        self.b_setGameState('ShipBoarding')
        self.b_setLocation(ship.getDoId(), PiratesGlobals.ShipZoneOnDeck)
        self.d_boardShip(shipDoId, boardingSpot)
        self.boardShip(shipDoId, boardingSpot)

    def b_swingToShip(self, shipDoId, boardingSpot):
        currentShip = localAvatar.ship
        ship = self.cr.getDo(shipDoId)
        self.b_setGameState('ShipBoarding')
        self.b_setLocation(ship.getDoId(), PiratesGlobals.ShipZoneOnDeck)
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.d_swingToShip(currentShip.getDoId(), shipDoId, boardingSpot, timestamp)
        self.swingToShip(currentShip.getDoId(), shipDoId, boardingSpot, timestamp)

    def createSwingTrack(self, fromShip, ship, boardingSpot):
        swingTrack = DistributedPlayerPirate.createSwingTrack(self, fromShip, ship, boardingSpot)
        swingTrack.append(Func(self.b_setGameState, 'LandRoam'))
        return swingTrack

    def getSwingCameraOut(self, duration):
        return LerpPosHprInterval(camera, pos = (0, -30, 10), hpr = (0, -3.75, 0), other = self, duration = duration)

    def getSwingCameraIn(self, duration):
        return LerpPosInterval(camera, pos = (0, -14, 6.5), other = self, duration = duration)

    def refreshInventoryUI(self):
        self.guiMgr.inventoryBagPage.inventoryUIManager.discoveredInventory = False
        self.guiMgr.inventoryBagPage.askInventory()

    def setDefenceEffect(self, skillId):
        self.defenceEffect = skillId
        effect = None
        if skillId == EnemySkills.MISC_HEX_WARD:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                if not skillId in self.defenceEffects:
                    effect = ProtectionSpiral.getEffect(True)

                if effect:
                    effect.reparentTo(self)
                    effect.setEffectColor(Vec4(.4, .3, 1, .75))
                    effect.setPos(0, 0, 2)
                    effect.setScale(.8, .6, .9)
                    effect.startLoop()
                    self.defenceEffects[skillId] = effect


        else:
            self.stopAllDefenceEffects()

    def stopAllDefenceEffects(self):
        if self.skillSfxIval:
            self.skillSfxIval.finish()
            self.skillSfxIval = None

        for effect in self.defenceEffects:
            self.defenceEffects[effect].stopLoop()
            del self.defenceEffects[effect]

        self.defenceEffects = {}

    def testProtection(self):
        from pirates.effects.VoodooShield import VoodooShield
        from pirates.effects.VoodooAttuneShield import VoodooAttuneShield
        self.e = VoodooShield.getEffect()
        self.e.reparentTo(self)
        self.e.startLoop()
        self.e2 = VoodooAttuneShield.getEffect()
        self.e2.reparentTo(self)
        self.e2.startLoop()

    def testBlock(self):
        self.e.pulseEffect()
        self.e2.pulseEffect()

    def disableLootUI(self):
        self.__lootUIEnabled = False

    def enableLootUI(self):
        self.__lootUIEnabled = True

    def checkHaveShip(self):
        if not self.getInventory().getShipDoIdList():
            localAvatar.guiMgr.mapPage.setReturnIsland(LocationIds.PORT_ROYAL_ISLAND)

    def enterDialogMode(self):
        pass

    def exitDialogMode(self):
        pass

    def handleZoneChanged(self, avObj, parentId, zoneId):
        if avObj is self:
            self.b_setLocation(parentId, zoneId)

    def updateStatusTray(self):
        self.guiMgr.gameGui.show()
        statusTray = self.guiMgr.gameGui.statusTray
        statusTray.doId = self.doId
        statusTray.updateHp(self.getHp(), self.getMaxHp())
        statusTray.updateVoodoo(self.getMojo(), self.getMaxMojo())

        inv = self.getInventory()
        if inv:
            self.updateReputation(InventoryType.OverallRep, inv.getReputation(InventoryType.OverallRep))

    def setMaxHp(self, *args):
        DistributedPlayerPirate.setMaxHp(self, *args)
        self.updateStatusTray()

    def setHp(self, *args):
        DistributedPlayerPirate.setHp(self, *args)
        self.updateStatusTray()

    def setMojo(self, *args):
        DistributedPlayerPirate.setMojo(self, *args)
        self.updateStatusTray()

    def setMaxMojo(self, *args):
        DistributedPlayerPirate.setMaxMojo(self, *args)
        self.updateStatusTray()

class MinimapLocalAvatar(GridMinimapObject):
    SORT = 5
    ICON = None
    RING = None

    def __init__(self, avatar):
        if not MinimapLocalAvatar.ICON:
            gui = loader.loadModel('models/gui/toplevel_gui')
            MinimapLocalAvatar.ICON = gui.find('**/generic_arrow')
            MinimapLocalAvatar.ICON.clearTransform()
            MinimapLocalAvatar.ICON.setHpr(0, -90, 90)
            MinimapLocalAvatar.ICON.setAlphaScale(1, 1)
            MinimapLocalAvatar.ICON.setScale(400)
            MinimapLocalAvatar.ICON.flattenStrong()

        if not MinimapLocalAvatar.RING:
            gui = loader.loadModel('models/gui/gui_main')
            MinimapLocalAvatar.RING = gui.find('**/compass_radar')
            MinimapLocalAvatar.RING.setColorScale(1, 1, 1, 1, 1)
            MinimapLocalAvatar.RING.setHpr(0, -90, 90)
            MinimapLocalAvatar.RING.flattenStrong()

        GridMinimapObject.__init__(self, 'localAvatar', avatar, MinimapLocalAvatar.ICON)
        self.ring = MinimapLocalAvatar.RING.copyTo(self.overlayGridChild)


    def _addedToMap(self, map):
        (cellSize, cellRadius) = map.getGridParameters()
        self.ring.setScale(cellSize * cellRadius)


    def updateOnMap(self, map):
        GridMinimapObject.updateOnMap(self, map)
        map.updateRadarTransform(self.worldNode)
        if localAvatar.guiMgr.invasionScoreboard:
            self.mapGeom.hide()
            self.ring.hide()
        else:
            self.mapGeom.show()
            self.ring.show()


    def setIsTracked(self, isTracked):
        pass


    def setGridCell(self, grid, zoneId, updateInterest = False):
        DistributedPlayerPirate.setGridCell(self, grid, zoneId, updateInterest = updateInterest)
        if grid:
            self.cr.timeOfDayManager.setRelativeRotation(grid.getH())
        else:
            self.cr.timeOfDayManager.setRelativeRotation(0)