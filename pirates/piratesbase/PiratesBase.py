from panda3d.physics import AngularEulerIntegrator, AngularIntegrator, ForceNode, LinearControlForce, LinearEulerIntegrator, LinearForce, LinearFrictionForce, LinearIntegrator, PhysicsManager
from panda3d.core import Camera, ClockObject, CollisionHandler, CollisionHandlerEvent, CollisionTraverser, Connection, CullBinEnums, CullBinManager, EventHandler, ExecutionEnvironment, Filename, GeomVertexArrayData, GraphicsPipe, GraphicsPipeSelection, Lens, MouseWatcher, NodePath, PGButton, Plane, PlaneNode, Point3, TPHigh, TPLow, TextProperties, TextPropertiesManager, Texture, TextureStage, TrueClock, URLSpec, VBase4, Vec3, Vec4, VertexDataPage, WindowProperties
import sys
import time
import os
from otp.nametag import NametagGlobals
from otp.nametag.ChatBalloon import ChatBalloon
from otp.margins.MarginManager import MarginManager
from direct.showbase.DirectObject import *
from direct.showbase.PythonUtil import *
from direct.showbase.Transitions import Transitions
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from otp.otpbase.OTPBase import OTPBase
from pirates.audio import MusicManager
from pirates.audio import PiratesAmbientManager
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.GameOptions import Options
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship import ShipFactory
from pirates.piratesgui import ScreenshotViewer
from pirates.piratesbase import FancyLoadingScreen
from pirates.piratesbase import LoadingScreen
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from pirates.piratesgui import PDialog
import PiratesGlobals
import __builtin__

class PiratesBase(OTPBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesBase')
    apiNames = ['pandagl', 'pandadx9', 'tinydisplay']

    def __init__(self):
        OTPBase.__init__(self, windowType = 'none')
        self.shipFactory = None
        self.isMainWindowOpen = False
        self.shipLookAhead = 0

        self.fourthOfJuly = config.GetBool('test-fourth-of-july', 0)
        self.effectsRoot = render.attachNewNode('Effects Root')

        self.musicMgr = None
        self.options = Options()
        self.options.load()
        self.options.applyPre()

        GeomVertexArrayData.getIndependentLru().setMaxSize(5242880)
        VertexDataPage.getGlobalLru(VertexDataPage.RCResident).setMaxSize(5242880)
        taskMgr.setupTaskChain('background', numThreads = 0)
        
        if not self.isClientBuilt():
            selection = GraphicsPipeSelection.getGlobalPtr()
            pipe = selection.makeModulePipe(self.options.api)

            if pipe:
                self.pipe = pipe
                self.notify.info('Loaded requested graphics %s' % self.pipe.getType().getName())
            else:
                self.notify.warning('Requested graphics API is not implemented!')

        if not self.pipe:
            self.makeDefaultPipe()

            if not self.pipe:
                self.notify.error('Could not find any graphics API.')

        self.shipsVisibleFromIsland = self.options.ocean_visibility
        self.overrideShipVisibility = False
        wp = WindowProperties()
        wp.setSize(self.options.getWidth(), self.options.getHeight())
        wp.setFullscreen(self.options.getFullscreen())
        self.openDefaultWindow(props = wp)
        self.options.setRuntimeOptions()
        self.eventMgr.doEvents()
        loadingMode = config.GetInt('loading-screen', 0)
        if loadingMode == 0:
            self.loadingScreen = LoadingScreen.LoadingScreen(None)
        else:
            self.loadingScreen = FancyLoadingScreen.FancyLoadingScreen(None)
        
        self.loadingScreen.showTarget(pickapirate = True)
        self.loadingScreen.show()
        self.loadingScreen.beginStep('PiratesBase', 34, 25)

        if not self.isMainWindowOpen:
            sys.exit(1)

        self.loadingScreen.tick()
        if self.wantEnviroDR:
            self.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
            self.setupEnviroCamera()
            self.setupAutoPixelZoom()
        else:
            self.cam.node().setCameraMask(OTPRender.MainCameraBitmask | OTPRender.EnviroCameraBitmask)
        self.loadingScreen.tick()

        self._PiratesBase__alreadyExiting = False
        self.exitFunc = self.userExit
        TextureStage.getDefault().setPriority(10)
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface:
            self.mouseInterface.reparentTo(render)

        if self.mouse2cam:
            self.mouse2cam.reparentTo(render)

        for key in PiratesGlobals.ScreenshotHotkeyList:
            self.accept(key, self.takeScreenShot)

        self.wantMarketingViewer = config.GetBool('want-marketing-viewer', 0)
        self.marketingViewerOn = False
        if self.wantMarketingViewer:
            for key in PiratesGlobals.MarketingHotkeyList:
                self.accept(key, self.toggleMarketingViewer)


        self.accept('panda3d-render-error', self.panda3dRenderError)
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setMinFov(PiratesGlobals.DefaultCameraFov)
        self.camLens.setNearFar(PiratesGlobals.DefaultCameraNear, PiratesGlobals.DefaultCameraFar)
        farCullNode = PlaneNode('farCull')
        farCullNode.setPlane(Plane(Vec3(0, -1, 0), Point3(0, 0, 0)))
        farCullNode.setClipEffect(0)
        self.farCull = camera.attachNewNode(farCullNode)
        self.positionFarCull()
        globalClockMaxDt = config.GetFloat('pirates-max-dt', 0.200)
        globalClock.setMaxDt(globalClockMaxDt)
        self.loadingScreen.tick()

        if self.config.GetBool('want-particles', 0):
            self.notify.debug('Enabling particles')
            self.enableParticles()

        self.loadingScreen.tick()
        self.notify.debug('Enabling new ship controls')
        self.avatarPhysicsMgr = PhysicsManager()
        integrator = LinearEulerIntegrator()
        self.avatarPhysicsMgr.attachLinearIntegrator(integrator)
        integrator = AngularEulerIntegrator()
        self.avatarPhysicsMgr.attachAngularIntegrator(integrator)
        self.taskMgr.add(self.doAvatarPhysics, 'physics-avatar')
        fn = ForceNode('ship viscosity')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        viscosity = LinearFrictionForce(0.0, 1.0, 0)
        viscosity.setCoef(0.5)
        viscosity.setAmplitude(2)
        fn.addForce(viscosity)
        self.avatarPhysicsMgr.addLinearForce(viscosity)
        self.loadingScreen.tick()
        fn = ForceNode('avatarControls')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        controlForce = LinearControlForce()
        self.controlForce = controlForce
        controlForce.setAmplitude(5)
        fn.addForce(controlForce)
        self.avatarPhysicsMgr.addLinearForce(controlForce)
        self.loadingScreen.tick()
        self.accept('PandaPaused', self.disableAllAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        self.emoteGender = None

        shadow = loader.loadModel('models/misc/drop_shadow')
        self.loadingScreen.tick()
        taskMgr.setupTaskChain('phasePost', numThreads = 0, threadPriority = TPHigh)

        self.phase3Post()
        self.phase4Post()
        self.phase5Post()

        tpMgr = TextPropertiesManager.getGlobalPtr()
        WLDisplay = TextProperties()
        WLDisplay.setSlant(0.299)
        WLEnter = TextProperties()
        WLEnter.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLDisplay', WLDisplay)
        tpMgr.setProperties('WLEnter', WLEnter)
        del tpMgr

        cbm = CullBinManager.getGlobalPtr()
        cbm.addBin('background', CullBinManager.BT_fixed, 10)
        cbm.addBin('ground', CullBinManager.BT_unsorted, 15)
        cbm.addBin('opaque', CullBinManager.BT_state_sorted, 20)
        cbm.addBin('shadow', CullBinManager.BT_unsorted, 25)
        cbm.addBin('water', CullBinEnums.BT_fixed, 28)
        cbm.addBin('transparent', CullBinManager.BT_back_to_front, 30)
        cbm.addBin('fixed', CullBinManager.BT_fixed, 40)
        cbm.addBin('unsorted', CullBinManager.BT_unsorted, 50)
        cbm.addBin('ShipRigging', CullBinEnums.BTBackToFront, 52)
        cbm.addBin('pre-additive', CullBinEnums.BTFixed, 53)
        cbm.addBin('additive', CullBinEnums.BTBackToFront, 54)
        cbm.addBin('gui-fixed', CullBinManager.BTUnsorted, 58)
        cbm.addBin('gui-popup', CullBinManager.BTUnsorted, 60)

        self.showShipFlats = False
        self.hideShipNametags = False
        self.showGui = True
        if self.win.getGsg():
            self.useStencils = self.win.getGsg().getSupportsStencil()
        else:
            self.useStencils = False
        self.supportAlphaFb = self.win.getFbProperties().getAlphaBits()
        taskMgr.setupTaskChain('background', frameBudget = 0.001, threadPriority = TPLow)

        gsg = self.win.getGsg()

        if gsg:
            if gsg.getShaderModel() < gsg.SM20:
                self.options.shader = 0

        self.noticeSystemOn = 1
        self.lodTrav = CollisionTraverser('base.lodTrav')
        self.zoneLODEventHandler = CollisionHandlerEvent()
        self.zoneLODEventHandler.addInPattern('enter%in')
        self.zoneLODEventHandler.addOutPattern('exit%in')
        self.zoneLODTarget = None
        self.transitions.loadLetterbox()
        self.transitions.letterbox.setColorScale(0, 0, 0, 1)
        self.loadingScreen.endStep('PiratesBase')
    
    def isClientBuilt(self):
        try:
            import niraidata
            return True
        except:
            return False

    def setNoticeSystem(self, on):
        if self.noticeSystemOn == on:
            return None
        else:
            self.noticeSystemOn = on
            messenger.send('noticeStateChanged')

    def setShipLookAhead(self, value):
        self.shipLookAhead = value

    def phase3Post(self):
        from pirates.battle import Sword, Dagger
        Sword.Sword.setupAssets()
        Dagger.Dagger.setupAssets()
        self.buildShips()

    def phase4Post(self):
        self.buildPhase4Assets()
        self.buildPhase4Ships()


    def phase5Post(self):
        from pirates.creature import Raven
        Raven.Raven.setupAssets()
        self.buildPhase5Ships()


    def buildPhase4Assets(self):
        from pirates.battle import WeaponGlobals, Pistol, Sword, Dagger, Doll, Wand
        from pirates.battle import Grenade, Bayonet, Melee, DualCutlass, Foil, Gun
        from pirates.battle import Axe, FishingRod, Torch, PowderKeg

        if config.GetBool('want-kraken', 0):
            from pirates.kraken import Holder
            Holder.Holder.setupAssets()
            self.loadingScreen.tick()

        if config.GetBool('want-seamonsters', 0):
            from pirates.creature import SeaSerpent
            SeaSerpent.SeaSerpent.setupAssets()
            self.loadingScreen.tick()

        PowderKeg.PowderKeg.setupAssets()
        self.loadingScreen.tick()
        Torch.Torch.setupAssets()
        self.loadingScreen.tick()
        FishingRod.FishingRod.setupAssets()
        self.loadingScreen.tick()
        Bayonet.Bayonet.setupAssets()
        self.loadingScreen.tick()
        Pistol.Pistol.setupAssets()
        self.loadingScreen.tick()
        Doll.Doll.setupAssets()
        self.loadingScreen.tick()
        Grenade.Grenade.setupAssets()
        self.loadingScreen.tick()
        Wand.Wand.setupAssets()
        self.loadingScreen.tick()
        Melee.Melee.setupSounds()
        self.loadingScreen.tick()
        DualCutlass.DualCutlass.setupAssets()
        self.loadingScreen.tick()
        Foil.Foil.setupAssets()
        self.loadingScreen.tick()
        Axe.Axe.setupAssets()
        self.loadingScreen.tick()
        Gun.Gun.setupAssets()
        self.loadingScreen.tick()

        from pirates.creature import Alligator, Bat, Chicken, Crab, Dog, FlyTrap
        from pirates.creature import Monkey, Pig, Rooster, Scorpion, Seagull
        from pirates.creature import Stump, Wasp

        Alligator.Alligator.setupAssets()
        self.loadingScreen.tick()
        Bat.Bat.setupAssets()
        self.loadingScreen.tick()
        Chicken.Chicken.setupAssets()
        self.loadingScreen.tick()
        Crab.Crab.setupAssets()
        self.loadingScreen.tick()
        Dog.Dog.setupAssets()
        self.loadingScreen.tick()
        FlyTrap.FlyTrap.setupAssets()
        self.loadingScreen.tick()
        Monkey.Monkey.setupAssets()
        self.loadingScreen.tick()
        Pig.Pig.setupAssets()
        self.loadingScreen.tick()
        Rooster.Rooster.setupAssets()
        self.loadingScreen.tick()
        Scorpion.Scorpion.setupAssets()
        self.loadingScreen.tick()
        Seagull.Seagull.setupAssets()
        self.loadingScreen.tick()
        Stump.Stump.setupAssets()
        self.loadingScreen.tick()
        Wasp.Wasp.setupAssets()
        self.loadingScreen.tick()


    def buildAssets(self):
        pass


    def buildShips(self):
        if not self.shipFactory:
            self.shipFactory = ShipFactory.ShipFactory(phasedLoading = True)

        self.loadingScreen.tick()


    def buildPhase4Ships(self):
        if not self.shipFactory:
            self.buildShips()

        self.shipFactory.handlePhase4()
        self.loadingScreen.tick()


    def buildPhase5Ships(self):
        if not self.shipFactory:
            self.buildShips()

        self.shipFactory.handlePhase5()
        self.loadingScreen.tick()

    def openMainWindow(self, *args, **kw):
        kw['stereo'] = bool(self.stereoEnabled)
        success = OTPBase.openMainWindow(self, *args, **kw)
        if self.win:
            self.win.setSort(500)
            self.win.setChildSort(10)
            self.postOpenWindow()
        self.isMainWindowOpen = success
        self.setCursorAndIcon()
        return success

    def setCursorAndIcon(self):
        wp = WindowProperties()
        
        if self.isClientBuilt():
            wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'icon.ico')))
        else:
            wp.setIconFilename(Filename.fromOsSpecific(os.path.join(os.getcwd(), 'resources/phase_3/etc/icon.ico')))

        self.win.requestProperties(wp)

    def postOpenWindow(self):
        NametagGlobals.setCamera(base.cam)
        if base.wantEnviroDR:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
        else:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask | OTPRender.EnviroCameraBitmask)
        self.mouseWatcherNode.setEnterPattern('mouse-enter-%r')
        self.mouseWatcherNode.setLeavePattern('mouse-leave-%r')
        self.mouseWatcherNode.setButtonDownPattern('button-down-%r')
        self.mouseWatcherNode.setButtonUpPattern('button-up-%r')
        NametagGlobals.setMouseWatcher(base.mouseWatcherNode)
        if base.wantEnviroDR:
            base.setupEnviroCamera()

        if self.config.GetBool('show-tex-mem', False):
            if not (self.texmem) or self.texmem.cleanedUp:
                self.toggleTexMem()

    def positionFarCull(self):
        gridDetail = config.GetString('grid-detail', 'high')
        self.gridDetail = gridDetail
        if gridDetail == 'high':
            self.farCull.setPos(0, 10000, 0)
        elif gridDetail == 'med':
            self.farCull.setPos(0, 5000, 0)
        elif gridDetail == 'low':
            self.farCull.setPos(0, 200, 0)
        else:
            raise StandardError, 'Invalid grid-detail: %s' % gridDetail


    def disableFarCull(self):
        self.farCull.setPos(0, 10000, 0)

    def setupRender2d(self):
        OTPBase.setupRender2d(self)
        self.a2dTopRight.reparentTo(self.aspect2d, sort = 1)


    def doAvatarPhysics(self, state):
        dt = ClockObject.getGlobalClock().getDt()
        freq = config.GetFloat('avatar-physics-freq', 1.0)
        maxSteps = config.GetInt('avatar-physics-maxsteps', 5)
        if not freq:
            self.avatarPhysicsMgr.doPhysics(dt)
        elif not hasattr(state, 'dtRollover'):
            state.dtRollover = 0

        maxDt = 1.0 / freq
        dt += state.dtRollover
        steps = int(dt / maxDt)
        state.dtRollover = dt % maxDt
        for x in xrange(min(steps, maxSteps)):
            self.avatarPhysicsMgr.doPhysics(maxDt)

        finalStep = max(steps - maxSteps, 0)
        if finalStep:
            self.avatarPhysicsMgr.doPhysics(finalStep * maxDt)

        return Task.cont


    def takeScreenShot(self):
        self.notify.info('Beginning screenshot capture')
        dt = time.localtime()
        date_time = '%04d-%02d-%02d_%02d-%02d-%02d' % (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
        uFilename = PLocalizer.ScreenshotDir + '/' + PLocalizer.Screenshot + '_' + date_time + '.' + base.screenshotExtension
        pandafile = Filename(str(ExecutionEnvironment.getCwd()) + '/' + str(uFilename))
        pandafile.makeDir()
        fn = base.screenshot(namePrefix = uFilename, defaultFilename = 0)
        winfile = pandafile.toOsSpecific()
        self.notify.info('Screenshot captured: ' + winfile)
        screenShotNotice = DirectLabel(text = PLocalizer.ScreenshotCaptured + ':\n' + winfile, scale = 0.050000, pos = (0.0, 0.0, 0.299), text_bg = (1, 1, 1, 0), text_fg = (1, 1, 1, 1), frameColor = (1, 1, 1, 0), text_font = PiratesGlobals.getInterfaceOutlineFont())
        screenShotNotice.reparentTo(base.a2dBottomCenter)
        screenShotNotice.setBin('gui-popup', 0)

        def clearScreenshotMsg(event):
            screenShotNotice.destroy()

        taskMgr.doMethodLater(3.0, clearScreenshotMsg, 'clearScreenshot')


    def showScreenshots(self):
        filenames = os.listdir(os.curdir + '/' + PLocalizer.ScreenshotDir)
        for f in filenames:
            if 'jpg' in f:
                if not self.screenshotViewer:
                    self.screenshotViewer = ScreenshotViewer.ScreenshotViewer()

                self.screenshotViewer.toggleShow()
                continue

    def startShow(self, cr):
        self.cr = cr
        from pirates.world import WorldCreator
        self.worldCreator = WorldCreator.WorldCreator(self.cr, None, None)

        base.graphicsEngine.renderFrame()
        gameServer = os.environ.get('POR_GAMESERVER', '25.91.142.158')
        serverPort = config.GetInt('server-port', 7969)
        self.wantTattoos = config.GetBool('want-tattoos', 0)
        self.wantSocks = config.GetBool('want-socks', 0)
        self.wantJewelry = config.GetBool('want-jewelry', 0)
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            if config.GetBool('server-force-ssl', False):
                url.setScheme('s')
            if not url.hasPort():
                url.setPort(serverPort)

            serverList.append(url)

        if len(serverList) == 1:
            failover = config.GetString('server-failover', '')
            serverURL = serverList[0]
            for arg in failover.split():

                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)

                if url != serverURL:
                    serverList.append(url)
                    continue


        cr.loginFSM.request('connect', [serverList])
        self.musicMgr = MusicManager.MusicManager()
        self.ambientMgr = PiratesAmbientManager.PiratesAmbientManager()

        def toggleGUI():
            self.showGui = not (self.showGui)
            render2d.toggleVis()
            npc = render.findAllMatches('**/nametag3d')
            for i in xrange(npc.getNumPaths()):
                np = npc.getPath(i)
                np.toggleVis()

            if not self.showGui:
                messenger.send('GUIHidden')
            else:
                messenger.send('GUIShown')


        def toggleWorld():
            if base.cr.activeWorld.isHidden():
                base.cr.activeWorld.show()
                render.find('**/*sky*').show()
                render.find('**/*seapatch*').show()
                base.win.setClearColor(Vec4(0, 0, 0, 1.0))
            else:
                base.cr.activeWorld.hide()
                render.find('**/*sky*').hide()
                render.find('**/*seapatch*').hide()
                base.win.setClearColor(Vec4(0.5, 0.5, 0.5, 1.0))

        self.accept(PiratesGlobals.HideGuiHotkey, toggleGUI)
        self.lastSpeedHackCheck = time.time()
        self.lastTrueClockTime = TrueClock.getGlobalPtr().getLongTime()
        taskMgr.add(self.__speedHackCheckTick, 'speedHackCheck-tick')

    def __speedHackCheckTick(self, task):
        elapsed = time.time() - self.lastSpeedHackCheck
        elapsed2 = TrueClock.getGlobalPtr().getLongTime() - self.lastTrueClockTime

        if elapsed2 > (elapsed + 0.1):
            self.cr.stopReaderPollTask()
            self.cr.lostConnection()

            return task.done

        self.lastSpeedHackCheck = time.time()
        self.lastTrueClockTime = TrueClock.getGlobalPtr().getLongTime()

        return task.cont

    def panda3dRenderError(self):
        if launcher:
            launcher.setPandaErrorCode(14)

        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectGraphicsError)

        self.cr.sendDisconnect()
        sys.exit()


    def userExit(self):
        if self._PiratesBase__alreadyExiting:
            return None

        self._PiratesBase__alreadyExiting = True
        requestResult = False
        try:
            if hasattr(base, 'cr'):
                if self.cr.timeManager:
                    self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectCloseWindow)

                if self.cr.loginFSM.getCurrentState().getName() == 'playingGame':
                    requestResult = self.cr.gameFSM.request('closeShard', ['shutdown'])

                else:
                    requestResult = self.cr.loginFSM.request('shutdown')

            self.loadingScreen.destroy()
            if not requestResult:
                self.notify.warning('Could not request shutdown; exiting anyway.')
                self.exitShow()

        finally:
            os._exit(0)

    def exitShow(self, errorCode = None):
        self.ignore('f12')
        if hasattr(base, 'cr'):
            self.musicMgr.delete()
            self.ambientMgr.delete()
            self.cr.ignoreAll()

        self.notify.info('Exiting Pirates')
        if self.launcher and errorCode is not None:
            self.launcher.setPandaErrorCode(errorCode)

        sys.exit()


    def initNametagGlobals(self):
        arrow = loader.loadModel('models/gui/arrow')
        card = NodePath('card')
        speech3d = ChatBalloon(loader.loadModel('models/gui/chatbox'))
        thought3d = ChatBalloon(loader.loadModel('models/gui/chatbox_thought_cutout'))
        speech2d = ChatBalloon(loader.loadModel('models/gui/chatbox_noarrow'))
        chatButtonGui = loader.loadModel('models/gui/triangle')
        chatButtonGui.setScale(0.100)
        chatButtonGui.flattenStrong()
        lookoutButtonGui = loader.loadModel('models/gui/lookout_gui')
        lookoutButtonGui.setScale(0.4)
        lookoutButtonGui.flattenStrong()
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-1, 1, -1, 1))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)

        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/triangle'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/triangle_down'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/triangle_over'))
        NametagGlobals.setQuitButton(PGButton.SReady, lookoutButtonGui.find('**/lookout_close_window'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, lookoutButtonGui.find('**/lookout_close_window_down'))
        NametagGlobals.setQuitButton(PGButton.SRollover, lookoutButtonGui.find('**/lookout_close_window_over'))
        rolloverSound = PiratesGuiGlobals.getDefaultRolloverSound()
        clickSound = PiratesGuiGlobals.getDefaultClickSound()
        NametagGlobals.setRolloverSound(rolloverSound)
        NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)
        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager
        self.leftCells = [
            mm.addGridCell(0, 1.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(0, 2.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(0, 3.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]
        self.bottomCells = [
            mm.addGridCell(0.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(1.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(2.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(3.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(4.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]
        self.rightCells = [
            mm.addGridCell(5, 2.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(5, 1.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]


    def getShardPopLimits(self):
        low = self.config.GetInt('shard-pop-limit-low', 100)
        mid = self.config.GetInt('shard-pop-limit-mid', 200)
        high = self.config.GetInt('shard-pop-limit-high', 300)
        return (low, mid, high)


    def toggleMarketingViewer(self):
        if not self.marketingViewerOn:
            if self.cr:
                if self.cr.tutorialObject and self.cr.tutorialObject.map:
                    self.cr.tutorialObject.map.marketingOn()
                elif self.cr.avCreate:
                    self.cr.avCreate.marketingOn()


            self.marketingViewerOn = True
        elif self.cr:
            if self.cr.tutorialObject and self.cr.tutorialObject.map:
                self.cr.tutorialObject.map.marketingOff()
            elif self.cr.avCreate:
                self.cr.avCreate.marketingOff()


        self.marketingViewerOn = False


    def setOverrideShipVisibility(self, value):
        self.overrideShipVisibility = value
        if value:
            self.shipsVisibleFromIsland = 2
        elif localAvatar.guiMgr.mainMenu and localAvatar.guiMgr.mainMenu.gameOptions:
            localAvatar.guiMgr.mainMenu.gameOptions.updateShipVisibility()
        else:
            self.shipsVisibleFromIsland = self.options.ocean_visibility
            messenger.send('ship_vis_change', [
                self.options.ocean_visibility])

    def hideEffects(self):
        self.effectsRoot.hide()


    def showEffects(self):
        self.effectsRoot.show()


    def zoneLODCollLoop(self, task):
        if self.zoneLODTarget:
            self.lodTrav.traverse(self.zoneLODTarget)

        return Task.cont


    def enableZoneLODs(self, target):
        self.zoneLODTarget = target
        taskMgr.add(self.zoneLODCollLoop, 'zoneLODloop', priority = 39)


    def disableZoneLODs(self):
        self.zoneLODTarget = None
        self.zoneLODEventHandler.clear()
        taskMgr.remove('zoneLODloop')
