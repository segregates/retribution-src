from panda3d.core import Camera, ColorWriteAttrib, DisplayRegion, FrameRateMeter, Lens, StereoDisplayRegion, TPLow, VBase4
from direct.showbase.ShowBase import ShowBase
import OTPRender
import time
import math
import re
from otp.ai.MagicWordGlobal import *
from otp.otpbase import OTPGlobals
from otp.chat.ChatGarbler import ChatGarbler
from otp.chat import WhiteList, SequenceListData
import traceback

class OTPBase(ShowBase):

    def __init__(self, windowType = None):
        self.wantEnviroDR = False
        ShowBase.__init__(self, windowType=windowType)
        self.idTags = config.GetBool('want-id-tags', 0)
        self.wantNametags = self.config.GetBool('want-nametags', 1)
        self.slowCloseShard = self.config.GetBool('slow-close-shard', 0)
        self.slowCloseShardDelay = self.config.GetFloat('slow-close-shard-delay', 1.0)
        self.fillShardsToIdealPop = self.config.GetBool('fill-shards-to-ideal-pop', 1)

        self.wantDynamicShadows = 1
        self.stereoEnabled = False
        self.FPSEnabled = False
        self.enviroDR = None
        self.enviroCam = None
        self.pixelZoomSetup = False

        self.chatGarbler = ChatGarbler()
        
        if base.cam:
            if self.wantEnviroDR:
                base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
            else:
                base.cam.node().setCameraMask(OTPRender.MainCameraBitmask | OTPRender.EnviroCameraBitmask)

        taskMgr.setupTaskChain('net')
        
        self.whiteList = None
        
        if config.GetBool('want-whitelist', True):
            self.whiteList = WhiteList.WhiteList()

            if config.GetBool('want-sequence-list', True):
                self.whiteList.setSequenceList(SequenceListData.SEQUENCES)
        
        self.adminAccess = 0
    
    def setAdminAccess(self, adminAccess):
        self.adminAccess = adminAccess

    def getAdminAccess(self):
        return self.adminAccess

    def setTaskChainNetThreaded(self):
        if config.GetBool('want-threaded-network', 0):
            taskMgr.setupTaskChain('net', numThreads=1, frameBudget=0.001, threadPriority=TPLow)

    def setTaskChainNetNonthreaded(self):
        taskMgr.setupTaskChain('net', numThreads=0, frameBudget=-1)

    def toggleStereo(self):
        self.stereoEnabled = not self.stereoEnabled
        if self.stereoEnabled:
            if not base.win.isStereo():
                base.win.setRedBlueStereo(True, ColorWriteAttrib.CRed, ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue)
        if self.wantEnviroDR:
            self.setupEnviroCamera()
            return

        mainDR = base.camNode.getDisplayRegion(0)
        if self.stereoEnabled:
            if not mainDR.isStereo():
                base.win.removeDisplayRegion(mainDR)
                mainDR = base.win.makeStereoDisplayRegion()
                mainDR.getRightEye().setClearDepthActive(True)
                mainDR.setCamera(base.cam)
        elif mainDR.isStereo():
            base.win.removeDisplayRegion(mainDR)
            mainDR = base.win.makeMonoDisplayRegion()
            mainDR.setCamera(base.cam)

    def toggleFPS(self):
        self.FPSEnabled = not self.FPSEnabled
        if self.FPSEnabled:
            base.setFrameRateMeter(True)
        if not self.FPSEnabled:
            base.setFrameRateMeter(False)
            return


    def setupEnviroCamera(self):
        clearColor = VBase4(0, 0, 0, 1)
        if self.enviroDR:
            clearColor = self.enviroDR.getClearColor()
            self.win.removeDisplayRegion(self.enviroDR)
        if not self.enviroCam:
            self.enviroCam = self.cam.attachNewNode(Camera('enviroCam'))
        mainDR = self.camNode.getDisplayRegion(0)
        if self.stereoEnabled:
            self.enviroDR = self.win.makeStereoDisplayRegion()
            if not mainDR.isStereo():
                self.win.removeDisplayRegion(mainDR)
                mainDR = self.win.makeStereoDisplayRegion()
                mainDR.setCamera(self.cam)
            ml = mainDR.getLeftEye()
            mr = mainDR.getRightEye()
            el = self.enviroDR.getLeftEye()
            er = self.enviroDR.getRightEye()
            el.setSort(-8)
            ml.setSort(-6)
            er.setSort(-4)
            er.setClearDepthActive(True)
            mr.setSort(-2)
            mr.setClearDepthActive(False)
        else:
            self.enviroDR = self.win.makeMonoDisplayRegion()
            if mainDR.isStereo():
                self.win.removeDisplayRegion(mainDR)
                mainDR = self.win.makeMonoDisplayRegion()
                mainDR.setCamera(self.cam)
            self.enviroDR.setSort(-10)
        self.enviroDR.setClearColor(clearColor)
        self.win.setClearColor(clearColor)
        self.enviroDR.setCamera(self.enviroCam)
        self.enviroCamNode = self.enviroCam.node()
        self.enviroCamNode.setLens(self.cam.node().getLens())
        self.enviroCamNode.setCameraMask(OTPRender.EnviroCameraBitmask)
        render.hide(OTPRender.EnviroCameraBitmask)
        self.camList.append(self.enviroCam)
        self.backgroundDrawable = self.enviroDR
        self.enviroDR.setTextureReloadPriority(-10)
        if self.pixelZoomSetup:
            self.setupAutoPixelZoom()

    def setupAutoPixelZoom(self):
        self.win.setPixelZoom(1)
        self.enviroDR.setPixelZoom(1)
        if not self.stereoEnabled:
            self.enviroDR.setClearColorActive(True)
            self.enviroDR.setClearDepthActive(True)
            self.win.setClearColorActive(False)
            self.win.setClearDepthActive(False)
            self.backgroundDrawable = self.enviroDR
        else:
            self.enviroDR.setClearColorActive(False)
            self.enviroDR.setClearDepthActive(False)
            self.enviroDR.getRightEye().setClearDepthActive(True)
            self.win.setClearColorActive(True)
            self.win.setClearDepthActive(True)
            self.backgroundDrawable = self.win
        self.pixelZoomSetup = True
        self.targetPixelZoom = 1.0
        self.pixelZoomTask = None
        self.pixelZoomCamHistory = 2.0
        self.pixelZoomCamMovedList = []
        self.pixelZoomStarted = None
        flag = self.config.GetBool('enable-pixel-zoom', True)
        self.enablePixelZoom(flag)
        return

    def enablePixelZoom(self, flag):
        if not self.backgroundDrawable.supportsPixelZoom():
            flag = False
        self.pixelZoomEnabled = flag
        taskMgr.remove('chasePixelZoom')
        if flag:
            taskMgr.add(self.__chasePixelZoom, 'chasePixelZoom', priority=-52)
        else:
            self.backgroundDrawable.setPixelZoom(1)

    def __chasePixelZoom(self, task):
        now = globalClock.getFrameTime()
        pos = base.cam.getNetTransform().getPos()
        prevPos = base.cam.getNetPrevTransform().getPos()
        d2 = (pos - prevPos).lengthSquared()
        if d2:
            d = math.sqrt(d2)
            self.pixelZoomCamMovedList.append((now, d))
        while self.pixelZoomCamMovedList and self.pixelZoomCamMovedList[0][0] < now - self.pixelZoomCamHistory:
            del self.pixelZoomCamMovedList[0]

        dist = sum(map(lambda pair: pair[1], self.pixelZoomCamMovedList))
        speed = dist / self.pixelZoomCamHistory
        if speed < 5:
            self.backgroundDrawable.setPixelZoom(4)
            self.pixelZoomStart = None
        elif speed > 10:
            if self.pixelZoomStart == None:
                self.pixelZoomStart = now
            elapsed = now - self.pixelZoomStart
            if elapsed > 10:
                self.backgroundDrawable.setPixelZoom(16)
            elif elapsed > 5:
                self.backgroundDrawable.setPixelZoom(8)
        return task.cont

    def getShardPopLimits(self):
        return (300, 600, 1200)

    def getRepository(self):
        return self.cr

    def openMainWindow(self, *args, **kw):
        result = ShowBase.openMainWindow(self, *args, **kw)
        if result:
            self.wantEnviroDR = not self.win.getGsg().isHardware() or config.GetBool('want-background-region', 1)
            self.backgroundDrawable = self.win
        return result

    def run(self):
        try:
            taskMgr.run()
        except SystemExit:
            self.notify.info('Normal exit.')
            self.destroy()
            raise
        except:
            self.notify.warning('Handling Python exception.')
            if getattr(self, 'cr', None):
                if self.cr.timeManager:
                    self.cr.timeManager.setExceptionInfo()
                    self.cr.timeManager.setDisconnectReason(OTPGlobals.DisconnectPythonError)
                self.cr.sendDisconnect()
            self.notify.info('Exception exit.\n')
            self.destroy()

@magicWord(CATEGORY_MEDIA_TEAM)
def oobe():
    'Toggle "out of body experience" view.'
    base.oobe()

@magicWord(CATEGORY_STAFF)
def oobeCull():
    'Toggle "out of body experience" view, with culling debugging.'
    base.oobeCull()

@magicWord(CATEGORY_STAFF)
def wire():
    'Toggle wireframe view.'
    base.toggleWireframe()

@magicWord(CATEGORY_MODERATION)
def showAvIds():
    'Show avId in Nametags.'
    messenger.send('nameTagShowAvId')

@magicWord(CATEGORY_MODERATION)
def showNames():
    'Remove avIds in Nametags.'
    messenger.send('nameTagShowName')

@magicWord(CATEGORY_BASIC)
def showAccess():
    return "Access level: " + str(spellbook.getTarget().getAdminAccess())

@magicWord(CATEGORY_STAFF)
def toga2d():
    if aspect2d.isHidden():
        aspect2d.show()
    else:
        aspect2d.hide()

@magicWord(CATEGORY_STAFF)
def placer():
    base.camera.place()

@magicWord(CATEGORY_STAFF)
def explorer():
    base.render.explore()
