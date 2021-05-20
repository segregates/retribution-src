from panda3d.core import Thread

from direct.distributed.PyDatagram import *

from otp.ai.TimeManagerAI import TimeManagerAI
from otp.chat.ChatAgentAI import ChatAgentAI
from otp.distributed.OtpDoGlobals import *
from otp.friends.FriendManagerAI import FriendManagerAI
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from otp.ai.BanManagerAI import BanManagerAI
from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from pirates.instance.DistributedMainWorldAI import DistributedMainWorldAI
from pirates.distributed.DistrictManagerAI import DistrictManagerAI
from pirates.ai.NewsManagerAI import NewsManagerAI
from pirates.world.WorldCreatorAI import WorldCreatorAI
from pirates.inventory.LootManagerAI import LootManagerAI
from pirates.piratesbase.DistributedTimeOfDayManagerAI import DistributedTimeOfDayManagerAI
from pirates.piratesbase.DistributedGameStatManagerAI import DistributedGameStatManagerAI
from pirates.instance.DistributedTeleportMgrAI import DistributedTeleportMgrAI
from pirates.distributed.TargetManagerAI import TargetManagerAI
from pirates.battle.BattleManagerAI import BattleManagerAI
from pirates.coderedemption.CodeRedemptionAI import CodeRedemptionAI
from pirates.band.DistributedPirateBandManagerAI import DistributedPirateBandManagerAI
from pirates.tutorial.DistributedPiratesTutorialWorldAI import DistributedPiratesTutorialWorldAI
import threading, sys

class PiratesAIRepository(PiratesInternalRepository):
    def __init__(self, baseChannel, stateServerChannel, districtName):
        PiratesInternalRepository.__init__(
            self, baseChannel, stateServerChannel, dcSuffix='AI')

        self.districtName = districtName
        self.districtManager = None
        self.uid2do = {}

        self.notify.setInfo(True)

    def createManagers(self):
        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(2)
        
        self.chatAgent = ChatAgentAI(self)
        self.chatAgent.generateWithRequired(2)

        self.todManager = DistributedTimeOfDayManagerAI(self)
        self.todManager.generateWithRequired(2)

        self.newsManager = NewsManagerAI(self)
        self.newsManager.generateWithRequired(2)
        
        self.friendManager = FriendManagerAI(self)
        self.friendManager.generateWithRequired(2)

        self.tpMgr = DistributedTeleportMgrAI(self)
        self.tpMgr.generateWithRequired(2)

        self.targetMgr = TargetManagerAI(self)
        self.targetMgr.generateWithRequired(2)

        self.gameStatManager = DistributedGameStatManagerAI(self)
        self.gameStatManager.generateWithRequired(2)

        self.magicWordManager = MagicWordManagerAI(self)
        self.magicWordManager.generateWithRequired(2)

        self.codeRedemption = CodeRedemptionAI(self)
        self.codeRedemption.generateWithRequired(2)

        self.bandManager = DistributedPirateBandManagerAI(self)
        self.bandManager.generateWithRequired(2)

        self.lootManager = LootManagerAI(self)

        self.banMgr = BanManagerAI(self)
        self.battleMgr = BattleManagerAI(self)

    def createMainWorld(self):
        self.worldCreator = WorldCreatorAI(self)

        self.mainWorld = DistributedMainWorldAI(self)
        self.mainWorld.generateWithRequired(2)

        self.worldCreator.setCurrentWorld(self.mainWorld)
        self.worldCreator.makeMainWorld(self.districtManager.district.mainWorld)
        self.worldCreator.createTunnels()

    def createTutorialWorld(self):
        if not hasattr(self, "worldCreator"):
            self.notify.warning("No world creator found. Generating")
            self.worldCreator = WorldCreatorAI(self)

        self.tutorialWorld = DistributedPiratesTutorialWorldAI(self)
        self.tutorialWorld.generateWithRequired(2)

        self.worldCreator.setCurrentWorld(self.tutorialWorld)
        self.worldCreator.makeTutorialWorld(self.districtManager.district.tutorialWorld)

    def handleConnected(self):
        PiratesInternalRepository.handleConnected(self)

        if sys.platform == 'win32':
            threading.Thread(target=self.startDistrict).start()
        else:
            self.startDistrict()

    def startDistrict(self):
        self.districtId = self.allocateChannel()
        self.notify.info('Creating PiratesDistrictAI(%d)...' % self.districtId)

        self.districtManager = DistrictManagerAI(self)
        self.districtManager.generateDistrict()

        self.notify.info('Claiming ownership of channel ID: %d...' % self.districtId)
        self.claimOwnership(self.districtId)

        self.notify.info('Creating managers...')
        self.createManagers()

        self.notify.info('Creating the main world...')
        self.createMainWorld()

        if config.GetBool('want-tutorial', False):
            self.notify.info("Creating the tutorial world...")
            self.createTutorialWorld()

        self.notify.info('Making district available...')
        self.districtManager.openDistrict()
        self.notify.info('Done.')
        messenger.send('startShardActivity')

        if config.GetBool('want-missing-prints', True):
            from pirates.battle.DistributedEnemySpawnerAI import DistributedEnemySpawnerAI
            DistributedEnemySpawnerAI.printMissingAvatarTypes()
            DistributedEnemySpawnerAI.printMissingShipTypes()
            DistributedEnemySpawnerAI.printMissingAnimalTypes()
            DistributedEnemySpawnerAI.printMissingBossTypes()
            DistributedEnemySpawnerAI.printBadBossTypes()
            
            WorldCreatorAI.printMissingTypes()
            WorldCreatorAI.printUnimplemented()

    def getTrackClsends(self):
        return False

    def incrementPopulation(self, user=None):
        self.districtManager.districtStats.b_setAvatarCount(self.districtManager.districtStats.getAvatarCount() + 1)
        self.districtManager.district.b_setAvatarCount(self.districtManager.district.getAvatarCount() + 1)

    def decrementPopulation(self, user=None):
        self.districtManager.districtStats.b_setAvatarCount(self.districtManager.districtStats.getAvatarCount() - 1)
        self.districtManager.district.b_setAvatarCount(self.districtManager.district.getAvatarCount() - 1)
