from panda3d.direct import DCFile
from panda3d.core import DatagramIterator, Filename, HTTPClient, getModelPath
import types
import random
import gc, os
import __builtin__
base.loadingScreen.beginStep('PCR', 20, 15)
from direct.showbase.ShowBaseGlobal import *
base.loadingScreen.tick()
from direct.distributed.ClockDelta import *
base.loadingScreen.tick()
from direct.gui.DirectGui import *
base.loadingScreen.tick()
base.loadingScreen.tick()
from otp.nametag import NametagGlobals
base.loadingScreen.tick()
from direct.interval.IntervalGlobal import *
base.loadingScreen.tick()
from direct.showbase.EventGroup import EventGroup
base.loadingScreen.tick()
from direct.showbase.PythonUtil import report
base.loadingScreen.tick()
from pirates.piratesbase.PiratesGlobals import *
base.loadingScreen.tick()
from PiratesMsgTypes import *
base.loadingScreen.tick()
from direct.directnotify.DirectNotifyGlobal import directNotify
base.loadingScreen.tick()
from direct.fsm import ClassicFSM
base.loadingScreen.tick()
from direct.fsm import State
base.loadingScreen.tick()
from direct.task import Task
base.loadingScreen.tick()
from direct.distributed.PyDatagram import PyDatagram
base.loadingScreen.tick()
from direct.distributed.PyDatagramIterator import PyDatagramIterator
base.loadingScreen.tick()
from direct.distributed import DistributedSmoothNode
base.loadingScreen.tick()
from direct.distributed.InterestWatcher import InterestWatcher
base.loadingScreen.tick()
from direct.distributed import DoInterestManager
from direct.distributed.ClientRepositoryBase import ClientRepositoryBase
from otp.distributed import OTPClientRepository
from otp.distributed import PotentialShard
from otp.distributed.PotentialAvatar import PotentialAvatar
from otp.distributed import DistributedDistrict
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.login.AvatarChooser import AvatarChooser
from pirates.makeapirate.MakeAPirate import MakeAPirate
from pirates.pirate import HumanDNA
from pirates.pirate import MasterHuman, Human
from pirates.pirate import AvatarTypes
from pirates.pirate.LocalPirate import LocalPirate
from pirates.pirate import DistributedPlayerPirate
from pirates.piratesbase import PLocalizer
from pirates.world import WorldGlobals
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.battle import BattleManager
from pirates.battle import DistributedBattleNPC
from pirates.battle import CombatAnimations
from pirates.band import DistributedBandMember
from pirates.cutscene import Cutscene
import PlayGame
import PiratesDistrictStats
from pirates.piratesbase import PiratesGlobals
from pirates.battle import DistributedBattleNPC
from pirates.ship import DistributedSimpleShip
from pirates.instance import DistributedTeleportMgr
from pirates.interact import InteractionManager
from pirates.piratesbase import UniqueIdManager
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import LoadingScreen
from pirates.ai import NewsManager
from pirates.makeapirate import PCPickANamePattern
from pirates.coderedemption.CodeRedemption import CodeRedemption

base.loadingScreen.endStep('PCR')
from pirates.quest import QuestLadderDynMap
from pirates.quest.QuestLadderDependency import QuestLadderDependency
from pirates.quest.QuestChoiceDynMap import QuestChoiceDynMap
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from otp.ai.MagicWordManager import MagicWordManager
from otp.friends.FriendHandle import FriendHandle
from direct.distributed.DoInterestManager import InterestHandle

class PiratesClientRepository(OTPClientRepository.OTPClientRepository):
    notify = directNotify.newCategory('PiratesClientRepository')
    SupportTutorial = 0
    GameGlobalsId = OTP_DO_ID_PIRATES
    StopVisibilityEvent = 'pirates-stop-visibility'
    ClearInterestDoneEvent = 'pirates-clear-interest'

    def __init__(self, serverVersion, launcher = None):
        self.loadingScreen = base.loadingScreen
        self.loadingScreen.parent = self
        self.accept('connectionIssue', self.loadingScreen.hide)
        self.accept('connectionRetrying', self.loadingScreen.show)
        OTPClientRepository.OTPClientRepository.__init__(self, serverVersion, launcher, playGame = PlayGame.PlayGame)
        self.createAvatarClass = DistributedPlayerPirate.DistributedPlayerPirate

        self.csm = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.guildManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_GUILD_MANAGER, 'GuildManager')
        self.matchMaker = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_MATCH_MAKER, 'DistributedMatchMaker')
        self.travelAgent = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
        self.crewMatchManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_CREW_MATCH_MANAGER, 'DistributedCrewMatchManager')
        self.piratesFriendsManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_FRIENDS_MANAGER, 'PiratesFriendsManager')

        self.wantSeapatch = config.GetBool('want-seapatch', 0)
        self.wantSpecialEffects = config.GetBool('want-special-effects', 0)
        self.wantMakeAPirate = config.GetBool('wantMakeAPirate', 0)
        self.forceTutorial = config.GetBool('force-tutorial', 0)
        self.skipTutorial = config.GetBool('skip-tutorial', 0)
        self.tutorialObject = None
        self.avChoiceDoneEvent = None
        self.avChoice = None
        self.avCreate = None
        self.currentCutscene = None
        self.activeWorld = None
        self.oldWorld = None
        self.teleportMgr = None
        self.treasureMap = None
        self.targetMgr = None
        self.newsManager = None
        self.friendManager = None
        self.distributedDistrict = None
        self.district = None
        self.currCamParent = None
        self.fakeMSP = None
        self.timeOfDayManager = None
        self.tradeManager = None
        self.pvpManager = None
        self.codeRedemption = None
        self.battleMgr = BattleManager.BattleManager(self)
        self.combatAnims = CombatAnimations.CombatAnimations()
        self.interactionMgr = InteractionManager.InteractionManager()
        self.uidMgr = UniqueIdManager.UniqueIdManager(self)
        self.questDynMap = QuestLadderDynMap.QuestLadderDynMap()
        self.questDependency = QuestLadderDependency()
        self.questChoiceSibsMap = QuestChoiceDynMap()

        self.old_setzone_interest_handle = None
        self._deletedSubShardDoIds = set()

        base.loadingScreen.beginStep('MasterHumans', 52, 45)

        self.humanHigh = [MasterHuman.MasterHuman(), MasterHuman.MasterHuman()]
        self.humanHigh[0].billboardNode.remove_node()
        self.humanHigh[1].billboardNode.remove_node()
        self.humanHigh[0].style = HumanDNA.HumanDNA('m')
        self.humanHigh[1].style = HumanDNA.HumanDNA('f')
        self.humanHigh[0].generateHuman('m')
        self.humanHigh[1].generateHuman('f')
        self.humanHigh[0].ignoreAll()
        self.humanHigh[1].ignoreAll()
        self.humanHigh[0].stopBlink()
        self.humanHigh[1].stopBlink()

        self.human = self.humanHigh

        base.loadingScreen.endStep('MasterHumans')

        self.preloadedCutscenes = { }
        self.defaultShard = 0

        if __dev__:
            __builtin__.go = self.getDo
            self.effectTypes = {
                'damageSmoke': [
                    'BlackSmoke'],
                'damageFire': [
                    'Fire'],
                'cannonDeckFire': [
                    'CannonSmokeSimple',
                    'CannonBlastSmoke'],
                'cannonBSFire': [
                    'MuzzleFlameBS',
                    'CannonSmokeSimpleBS',
                    'CannonBlastSmokeBS',
                    'GrapeshotEffectBS'],
                'cannonHit': [
                    'SimpleSmokeCloud',
                    'ExplosionFlip'],
                'cannonSplash': [
                    'CannonSplash'] }
            self.effectToggles = { }

        self.cannonballCollisionDebug = 1
        self.clearFriendState()

    def gotoFirstScreen(self):
        base.loadingScreen.beginStep('PrepLogin', 9, 0.14)
        self.startReaderPollTask()
        self.startHeartbeat()
        base.loadingScreen.tick()
        self.loginFSM.request('login')
        base.loadingScreen.tick()
        base.loadingScreen.endStep('PrepLogin')

    def getOldWorld(self):
        return self.oldWorld


    def getActiveWorld(self):
        return self.activeWorld


    def preloadCutscene(self, name):
        if name not in self.preloadedCutscenes:
            newCutscene = Cutscene.Cutscene(self, name)
            self.preloadedCutscenes[name] = newCutscene



    def getPreloadedCutsceneInfo(self, name):
        return self.preloadedCutscenes.get(name)


    def cleanupPreloadedCutscene(self, name):
        plCutscene = self.preloadedCutscenes.get(name)
        if plCutscene:
            if not plCutscene.isEmpty():
                plCutscene.destroy()

            del self.preloadedCutscenes[name]



    def setActiveWorld(self, world):
        if self.activeWorld != world:
            self.oldWorld = self.activeWorld

        self.activeWorld = world

    def getWaterHeight(self, node):
        if self.wantSeapatch and self.activeWorld:
            water = self.activeWorld.getWater()
            if water:
                return water.calcHeight(node = node)

        else:
            return 0.0


    def isOceanEnabled(self):
        if self.wantSeapatch and self.activeWorld and self.activeWorld.hasWater():
            return self.activeWorld.getWater().enabled

        return 0

    def __handleReject(self, avList, index):
        self.rejectDialog.cleanup()
        avid = 0
        for k in avList:
            if k.position == index:
                avid = k.id

        if avid == 0:
            self.notify.error('Avatar rejected not found in avList.  Index is: ' + str(index))
        self.csm.sendAcknowledgeAvatarName(
            avid,
            lambda: self.loginFSM.request('waitForAvatarList'))

    def enterChooseAvatar(self, avList):
        base.loadingScreen.beginStep('AvChooser', 14, 10)
        self.sendSetAvatarIdMsg(0, 0)
        self.handler = self.handleMessageType

        self.clearFriendState()
        self.avChoiceDoneEvent = 'avatarChooserDone'
        self.avChoice = AvatarChooser(self.loginFSM, self.avChoiceDoneEvent)
        base.loadingScreen.tick()
        self.avChoice.load()
        base.loadingScreen.tick()
        self.avChoice.enter()
        base.loadingScreen.tick()
        self.accept(self.avChoiceDoneEvent, self.__handleAvatarChooserDone)
        base.loadingScreen.endStep('AvChooser')
        base.cr.loadingScreen.hide()

    def __handleAvatarChooserDone(self, doneStatus):
        done = doneStatus['mode']
        if done == 'exit':
            self.notify.info('handleAvatarChooserDone: shutting down')
            self.loginFSM.request('shutdown')
            return None

        slot = self.avChoice.getChoice()
        self.avChoice.exit()
        self.handleAvatarChoice(done, slot)

    def handleAvatarChoice(self, done, slot):
        if done == 'chose':
            av = self.avList[slot]
            if av.dna.getTutorial() < 3 and self.skipTutorial == 0:
                self.tutorial = 1
            else:
                self.tutorial = 0
            self.loadingScreen.beginStep('waitForAv')
            self.loginFSM.request('waitForSetAvatarResponse', [av, av.position])
        elif done == 'create':
            self.loginFSM.request('createAvatar', [self.avList, slot])

    def exitChooseAvatar(self):
        self.handler = None
        if self.avChoice:
            self.avChoice.exit()
            self.avChoice.unload()
            self.avChoice = None

        if self.avChoiceDoneEvent:
            self.ignore(self.avChoiceDoneEvent)
            self.avChoiceDoneEvent = None

    def enterCreateAvatar(self, avList, index):
        self.tutorial = 0
        self.avCreate = MakeAPirate(avList, 'makeAPirateComplete', index, isNPCEditor=config.GetBool('want-npc-editor', False))
        self.avCreate.load()
        self.avCreate.enter()
        self.accept('makeAPirateComplete', self.__handleMakeAPirate)

    def handleAvatarCreated(self, newPotAv, avatarId):
        newPotAv.id = avatarId
        self.loginFSM.request('waitForSetAvatarResponse', [newPotAv, newPotAv.position])

    def __handleMakeAPirate(self):
        done = self.avCreate.getDoneStatus()
        if done == 'cancel':
            self.avCreate.exit()
            self.loginFSM.request('chooseAvatar', [self.avList])
        elif done == 'created':
            self.handleAvatarCreated(self.avCreate.newPotAv, self.avCreate.avId)
        else:
            self.notify.error('Invalid doneStatus from MakeAPirate: ' + str(done))

    def exitCreateAvatar(self):
        if self.skipTutorial:
            self.ignore('makeAPirateComplete')
            self.ignore('nameShopPost')
            self.ignore('nameShopCreateAvatar')
            self.avCreate.exit()
            self.avCreate.unload()
            self.avCreate = None
            self.handler = None

        self.ignore('createdNewAvatar')

    def handleCreateAvatarResponse(self, avId):
        self.avId = avId
        newPotAv = PotentialAvatar(self.avId, self.newName, self.newDNA, self.newPosition)
        self.loginFSM.request('waitForSetAvatarResponse', [newPotAv, self.newPosition])

    def avatarListFailed(self, reason):
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.avatarListFailedBox = dialogClass(message = PLocalizer.CRAvatarListFailed, doneEvent = 'avatarListFailedAck', text_wordwrap = 18, style = OTPDialog.Acknowledge)
        self.avatarListFailedBox.show()
        self.acceptOnce('avatarListFailedAck', self.__handleAvatarListFailedAck)

    def __handleAvatarListFailedAck(self):
        self.ignore('avatarListFailedAck')
        self.avatarListFailedBox.cleanup()
        self.loginFSM.request('shutdown')

    def avatarList(self, avatars):
        self.ignore('avatarListFailed')
        self.ignore('avatarList')
        self.avList = avatars
        if self.loginFSM.getCurrentState().getName() == 'chooseAvatar':
            self.avChoice.updateAvatarList()
        else:
            self.loginFSM.request('chooseAvatar', [self.avList])

    def handleGetAvatarsRespMsg(self, di):
        pass

    def handleGetAvatarsResp2Msg(self, di):
        pass

    def handleGenerateWithRequiredOtherOwner(self, di):
        if self.loginFSM.getCurrentState().getName() == 'waitForSetAvatarResponse':
            doId = di.getUint32()
            parentId = di.getUint32()
            zoneId = di.getUint32()
            dclassId = di.getUint16()
            self.handleAvatarResponseMsg(doId, di)

    def handleAvatarResponseMsg(self, avatarId, di):
        self.localAvatarDoId = avatarId
        self.loadingScreen.endStep('waitForAv')
        self.cleanupWaitingForDatabase()
        dclass = self.dclassesByName['DistributedPlayerPirate']
        NametagGlobals.setMasterArrowsOn(0)
        self.loadingScreen.show(waitForLocation = True, expectedLoadScale = 4)
        self.loadingScreen.beginStep('LocalAvatar', 36, 120)
        localAvatar = LocalPirate(self)
        localAvatar.dclass = dclass
        base.localAvatar = localAvatar
        __builtins__['localAvatar'] = base.localAvatar
        localAvatar.doId = avatarId
        self.doId2do[avatarId] = localAvatar
        parentId = None
        zoneId = None
        localAvatar.setLocation(parentId, zoneId)
        localAvatar.generate()
        localAvatar.updateAllRequiredFields(dclass, di)
        locUID = localAvatar.getReturnLocation()
        if not locUID:
            locUID = '1150922126.8dzlu'
            localAvatar.setReturnLocation(locUID)
        self.loadingScreen.showTarget(locUID)
        self.loadingScreen.showHint(locUID)
        self.loadingScreen.endStep('LocalAvatar')
        self.sendGetFriendsListRequest()
        self.loginFSM.request('playingGame')

    def enterWaitForDeleteAvatarResponse(self, potentialAvatar):
        raise StandardError, 'This should be handled within AvatarChooser.py'

    def exitWaitForDeleteAvatarResponse(self):
        raise StandardError, 'This should be handled within AvatarChooser.py'

    def sendUpdateToGlobalDoId(self, dclassName, fieldName, doId, args):
        dcfile = self.getDcFile()
        dclass = dcfile.getClassByName(dclassName)
        dg = dclass.clientFormatUpdate(fieldName, doId, args)
        self.send(dg)

    def sendMsgToTravelAgent(self, fieldName, args):
        self.sendUpdateToGlobalDoId('DistributedTravelAgent', fieldName, OtpDoGlobals.OTP_DO_ID_PIRATES_TRAVEL_AGENT, args)

    def enterPlayingGame(self):
        OTPClientRepository.OTPClientRepository.enterPlayingGame(self)
        self._userLoggingOut = False

        if False: # TODO: localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER and self.skipTutorial == 0:
            localAvatar.teleportToType = PiratesGlobals.INSTANCE_TUTORIAL
            localAvatar.teleportToName = WorldGlobals.PiratesTutorialSceneFileBase
            self.sendMsgToTravelAgent('requestInitLocUD', ['unused', 0])
        elif False: # TODO: localAvatar.onWelcomeWorld and self.defaultShard != 0 and config.GetBool('want-welcome-worlds', 0):
            localAvatar.teleportToType = PiratesGlobals.INSTANCE_WELCOME
            localAvatar.teleportToName = 'Welcome World'
            self.sendMsgToTravelAgent('requestInitLocUD', ['unused', 0])
        else:
            desiredShard = self.defaultShard
            localAvatar.teleportToType = PiratesGlobals.INSTANCE_MAIN
            localAvatar.teleportToName = WorldGlobals.PiratesWorldSceneFileBase
            self.travelAgent.sendRequestInitLoc(desiredShard)

    def playingGameLocReceived(self, shardId, zoneId):
        self.gameFSM.request('waitOnEnterResponses', [shardId, zoneId, zoneId, -1])

    def exitPlayingGame(self):
        self.notify.info('exitPlayingGame')
        ivalMgr.interrupt()
        self.notify.info('sending clientLogout')
        messenger.send('cancelFriendInvitation')
        messenger.send('clientLogout')
        if config.GetDouble('want-dev-hotkeys', 0):
            self.ignore(PiratesGlobals.KrakenHotkey)
            self.ignore(PiratesGlobals.ShipHotkey)

        self.uidMgr.reset()
        if self.distributedDistrict:
            self.distributedDistrict.worldCreator.cleanupAllAreas()

        for (doId, obj) in self.doId2do.items():
            if not isinstance(obj, LocalPirate) and not isinstance(obj, DistributedDistrict.DistributedDistrict):
                if hasattr(self, 'disableObject'):
                    self.disableObject(doId)

            hasattr(self, 'disableObject')

        if hasattr(base, 'localAvatar'):
            camera.reparentTo(render)
            camera.setPos(0, 0, 0)
            camera.setHpr(0, 0, 0)

        base.transitions.noTransitions()
        OTPClientRepository.OTPClientRepository.exitPlayingGame(self)

    def enterGameOff(self):
        OTPClientRepository.OTPClientRepository.enterGameOff(self)

    def enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId):
        self.resetDeletedSubShardDoIds()
        OTPClientRepository.OTPClientRepository.enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId)

    def enterTutorialQuestion(self, hoodId, zoneId, avId):
        self.__requestTutorial(hoodId, zoneId, avId)

    def handleTutorialQuestion(self, msgType, di):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            self.handleGenerateWithRequiredOther(di)
        elif msgType == CLIENT_OBJECT_UPDATE_FIELD:
            self.handleUpdateField(di)
        elif msgType == CLIENT_OBJECT_DISABLE:
            self.handleDisable(di)
        elif msgType == CLIENT_OBJECT_DISABLE_OWNER:
            self.handleDisableOwner(di)
        elif msgType == CLIENT_OBJECT_DELETE_RESP:
            self.handleDelete(di)
        else:
            self.handleUnexpectedMsgType(msgType, di)

    def exitTutorialQuestion(self):
        self.handler = None
        self.handlerArgs = None
        self.ignore('startTutorial')
        taskMgr.remove('waitingForTutorial')

    def __requestTutorial(self, hoodId, zoneId, avId):
        self.acceptOnce('startTutorial', self.__handleStartTutorial, [
            avId])
        messenger.send('requestTutorial')

    def __handleStartTutorial(self, avId, zoneId):
        pass # TODO

    def enterSwitchShards(self, shardId, hoodId, zoneId, avId):
        OTPClientRepository.OTPClientRepository.enterSwitchShards(self, shardId, hoodId, zoneId, avId)
        self.handler = self.handleCloseShard

    def exitSwitchShards(self):
        OTPClientRepository.OTPClientRepository.exitSwitchShards(self)
        self.ignore(PiratesClientRepository.ClearInterestDoneEvent)
        self.handler = None
        return

    def enterCloseShard(self, loginState = None):
        OTPClientRepository.OTPClientRepository.enterCloseShard(self, loginState)
        self.handler = self.handleCloseShard
        self._removeLocalAvFromStateServer()

    def handleCloseShard(self, msgType, di):
        if msgType == CLIENT_ENTER_OBJECT_REQUIRED:
            di2 = PyDatagramIterator(di)
            parentId = di2.getUint32()
            if self._doIdIsOnCurrentShard(parentId):
                return
        elif msgType == CLIENT_ENTER_OBJECT_REQUIRED_OTHER:
            di2 = PyDatagramIterator(di)
            parentId = di2.getUint32()
            if self._doIdIsOnCurrentShard(parentId):
                return
        elif msgType == CLIENT_OBJECT_SET_FIELD:
            di2 = PyDatagramIterator(di)
            doId = di2.getUint32()
            if self._doIdIsOnCurrentShard(doId):
                return
        self.handleMessageType(msgType, di)

    def _logFailedDisable(self, doId, ownerView):
        if doId not in self.doId2do and doId in self._deletedSubShardDoIds:
            return
        OTPClientRepository.OTPClientRepository._logFailedDisable(self, doId, ownerView)

    def exitCloseShard(self):
        OTPClientRepository.OTPClientRepository.exitCloseShard(self)
        self.ignore(PiratesClientRepository.ClearInterestDoneEvent)
        self.handler = None
        return

    def isShardInterestOpen(self):
        return self.old_setzone_interest_handle is not None or self.uberZoneInterest is not None

    def resetDeletedSubShardDoIds(self):
        self._deletedSubShardDoIds.clear()

    def dumpAllSubShardObjects(self):
        if self.KeepSubShardObjects:
            return

        messenger.send('clientCleanup')
        doIds = self.doId2do.keys()

        for doId in doIds:
            obj = self.doId2do[doId]

            if obj.parentId != localAvatar.defaultShard or obj is localAvatar or obj.neverDisable:
                continue
            
            self.deleteObject(doId)
            self._deletedSubShardDoIds.add(doId)

    def _removeCurrentShardInterest(self, callback):
        if self.old_setzone_interest_handle is None:
            self.notify.warning('removePiratesShardInterest: no shard interest open')
            callback()
            return
        self.acceptOnce(PiratesClientRepository.ClearInterestDoneEvent, Functor(self._tcrRemoveUberZoneInterest, callback))
        self._removeEmulatedSetZone(PiratesClientRepository.ClearInterestDoneEvent)
        return

    def _tcrRemoveUberZoneInterest(self, callback):
        self.acceptOnce(PiratesClientRepository.ClearInterestDoneEvent, Functor(self._tcrRemoveShardInterestDone, callback))
        self.removeInterest(self.uberZoneInterest, PiratesClientRepository.ClearInterestDoneEvent)

    def _tcrRemoveShardInterestDone(self, callback):
        self.uberZoneInterest = None
        callback()
        return

    def _doIdIsOnCurrentShard(self, doId):
        if doId == base.localAvatar.defaultShard:
            return True
        do = self.getDo(doId)
        if do:
            if do.parentId == base.localAvatar.defaultShard:
                return True
        return False

    def _wantShardListComplete(self):
        if self._shardsAreReady():
            self.acceptOnce(PiratesDistrictStats.EventName(), self.shardDetailStatsComplete)
            PiratesDistrictStats.refresh()
        else:
            self.loginFSM.request('noShards')

    def shardDetailStatsComplete(self):
        self.loginFSM.request('waitForAvatarList')

    def exitWaitForShardList(self):
        self.ignore(PiratesDistrictStats.EventName())
        OTPClientRepository.OTPClientRepository.exitWaitForShardList(self)
    
    def handleGetFriendsList(self, resp):
        base.localAvatar.guiMgr.friendsPage.removeAllFriends()
        self.friendsMap = {}

        for pirate in resp:
            doId, name, hp, maxHp, online = pirate
            handle = FriendHandle(*pirate)
            
            self.friendsMap[doId] = handle
            messenger.send(OTPGlobals.AvatarFriendUpdateEvent, [doId, handle])

        self.friendsMapPending = 0
        messenger.send('friendsMapComplete')
    
    def fillUpFriendsMap(self):
        if self.isFriendsMapComplete():
            return 1
        if not self.friendsMapPending:
            self.notify.warning('Friends list stale; fetching new list.')
            self.sendGetFriendsListRequest()
        return 0

    def isFriend(self, doId):
        if doId in base.localAvatar.friendsList:
            self.identifyFriend(doId)
            return 1

        return 0

    def isFriendOnline(self, doId):
        friend = self.identifyFriend(doId)
        
        return friend is not None and friend.isOnline()

    def identifyAvatar(self, doId, source=None):
        if doId in self.doId2do:
            return self.doId2do[doId]
        elif doId in self.friendsMap:
            return self.friendsMap[doId]
        
        self.notify.warning("Don't know who avatar %s is." % doId)
    
    def identifyFriend(self, doId, source=None):
        return self.identifyAvatar(doId)

    def isFriendsMapComplete(self):
        for friendId in base.localAvatar.friendsList:
            if self.identifyFriend(friendId) == None:
                return 0
        return 1

    def removeFriend(self, avatarId):
        messenger.send(OTPGlobals.AvatarFriendRemoveEvent, [avatarId])
        self.piratesFriendsManager.d_removeFriend(avatarId)

    def clearFriendState(self):
        self.friendsMap = {}
        self.friendsMapPending = 0

    def sendGetFriendsListRequest(self, task=None):
        self.friendsMapPending = 1
        self.piratesFriendsManager.d_requestFriendsList()

    def _abandonShard(self):
        for doId, obj in self.doId2do.items():
            if obj.parentId == localAvatar.defaultShard and obj is not localAvatar:
                self.deleteObject(doId)

    def getFriendFlags(self, doId):
        return 0

    def handleObjDelete(self, obj):
        if self.currCamParent == obj.getDoId():
            self.currCamParent = None

    def readDCFile(self, dcFileNames = None):
        """
        Reads in the dc files listed in dcFileNames, or if
        dcFileNames is None, reads in all of the dc files listed in
        the Config.prc file.
        """

        dcFile = self.getDcFile()
        dcFile.clear()
        self.dclassesByName = {}
        self.dclassesByNumber = {}
        self.hashVal = 0

        if isinstance(dcFileNames, types.StringTypes):
            # If we were given a single string, make it a list.
            dcFileNames = [dcFileNames]

        dcImports = {}
        if dcFileNames == None:
            try:
                readResult = dcFile.read(dcStream, '__dc__')
                del __builtin__.dcStream

            except NameError:
                readResult = dcFile.readAll()

            if not readResult:
                self.notify.error("Could not read dc file.")

        else:
            searchPath = getModelPath().getValue()
            for dcFileName in dcFileNames:
                pathname = Filename(dcFileName)
                vfs.resolveFilename(pathname, searchPath)
                readResult = dcFile.read(pathname)
                if not readResult:
                    self.notify.error("Could not read dc file: %s" % (pathname))

        self.hashVal = dcFile.getHash()

        # Now import all of the modules required by the DC file.
        for n in xrange(dcFile.getNumImportModules()):
            moduleName = dcFile.getImportModule(n)[:]

            # Maybe the module name is represented as "moduleName/AI".
            suffix = moduleName.split('/')
            moduleName = suffix[0]
            suffix=suffix[1:]
            if self.dcSuffix in suffix:
                moduleName += self.dcSuffix
            elif self.dcSuffix == 'UD' and 'AI' in suffix: #HACK:
                moduleName += 'AI'

            importSymbols = []
            for i in xrange(dcFile.getNumImportSymbols(n)):
                symbolName = dcFile.getImportSymbol(n, i)

                # Maybe the symbol name is represented as "symbolName/AI".
                suffix = symbolName.split('/')
                symbolName = suffix[0]
                suffix=suffix[1:]
                if self.dcSuffix in suffix:
                    symbolName += self.dcSuffix
                elif self.dcSuffix == 'UD' and 'AI' in suffix: #HACK:
                    symbolName += 'AI'

                importSymbols.append(symbolName)

            self.importModule(dcImports, moduleName, importSymbols)

        # Now get the class definition for the classes named in the DC
        # file.
        for i in xrange(dcFile.getNumClasses()):
            dclass = dcFile.getClass(i)
            number = dclass.getNumber()
            className = dclass.getName() + self.dcSuffix

            # Does the class have a definition defined in the newly
            # imported namespace?
            classDef = dcImports.get(className)
            if classDef is None and self.dcSuffix == 'UD': #HACK:
                className = dclass.getName() + 'AI'
                classDef = dcImports.get(className)

            # Also try it without the dcSuffix.
            if classDef == None:
                className = dclass.getName()
                classDef = dcImports.get(className)
            if classDef is None:
                self.notify.debug("No class definition for %s." % (className))
            else:
                if type(classDef) == types.ModuleType:
                    if not hasattr(classDef, className):
                        self.notify.warning("Module %s does not define class %s." % (className, className))
                        continue
                    classDef = getattr(classDef, className)

                if type(classDef) != types.ClassType and type(classDef) != types.TypeType:
                    self.notify.error("Symbol %s is not a class name." % (className))
                else:
                    dclass.setClassDef(classDef)

            self.dclassesByName[className] = dclass
            if number >= 0:
                self.dclassesByNumber[number] = dclass

        # Owner Views
        if self.hasOwnerView():
            ownerDcSuffix = self.dcSuffix + 'OV'
            # dict of class names (without 'OV') that have owner views
            ownerImportSymbols = {}

            # Now import all of the modules required by the DC file.
            for n in xrange(dcFile.getNumImportModules()):
                moduleName = dcFile.getImportModule(n)

                # Maybe the module name is represented as "moduleName/AI".
                suffix = moduleName.split('/')
                moduleName = suffix[0]
                suffix=suffix[1:]
                if ownerDcSuffix in suffix:
                    moduleName = moduleName + ownerDcSuffix

                importSymbols = []
                for i in xrange(dcFile.getNumImportSymbols(n)):
                    symbolName = dcFile.getImportSymbol(n, i)

                    # Check for the OV suffix
                    suffix = symbolName.split('/')
                    symbolName = suffix[0]
                    suffix=suffix[1:]
                    if ownerDcSuffix in suffix:
                        symbolName += ownerDcSuffix
                    importSymbols.append(symbolName)
                    ownerImportSymbols[symbolName] = None

                self.importModule(dcImports, moduleName, importSymbols)

            # Now get the class definition for the owner classes named
            # in the DC file.
            for i in xrange(dcFile.getNumClasses()):
                dclass = dcFile.getClass(i)
                if ((dclass.getName()+ownerDcSuffix) in ownerImportSymbols):
                    number = dclass.getNumber()
                    className = dclass.getName() + ownerDcSuffix

                    # Does the class have a definition defined in the newly
                    # imported namespace?
                    classDef = dcImports.get(className)
                    if classDef is None:
                        self.notify.error("No class definition for %s." % className)
                    else:
                        if type(classDef) == types.ModuleType:
                            if not hasattr(classDef, className):
                                self.notify.error("Module %s does not define class %s." % (className, className))
                            classDef = getattr(classDef, className)
                        dclass.setOwnerClassDef(classDef)
                        self.dclassesByName[className] = dclass

    def enterConnect(self, serverList=[]):
        # TLS config
        self.checkHttp()
        certPem = None

        if 'certPem' in __builtin__.__dict__:
            certPem = __builtin__.certPem
        elif not base.isClientBuilt():
            certFile = os.path.join('astron', 'certs', 'cert.crt')
            
            if os.path.exists(certFile):
                with open(certFile, 'r') as file:
                    certPem = file.read()
        
        if certPem:
            self.notify.info('Adding TLS certificate.')

            for server in serverList:
                self.http.addPreapprovedServerCertificatePem(server, certPem)

        self.http.setVerifySsl(HTTPClient.VSNoDateCheck)
        OTPClientRepository.OTPClientRepository.enterConnect(self, serverList)
    
    def handleFriendOnline(self, doId, name):
        messenger.send('friendOnline', [doId, name])

    def handleFriendOffline(self, doId, name):
        messenger.send('friendOffline', [doId, name])
