from panda3d.core import ColorBlendAttrib, Vec3
# File: L (Python 2.4)

from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GameOptions import Options
from PooledEffect import PooledEffect
from EffectController import EffectController

class LanternGlow(PooledEffect, EffectController):

    def __init__(self, effectParent = None, billboardOffset = 1.0):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)

        self.glow = loader.loadModel('models/effects/lanternGlow')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.glow.setBillboardPointEye(billboardOffset)
        self.glow.setColorScaleOff()
        self.glow.setLightOff()
        self.glow.setFogOff()
        self.glow.reparentTo(self)
        self.glow.setScale(1.0)
        self.glow.setPos(Vec3(0, 0, -0.149))
        self.glowHalo = loader.loadModel('models/effects/gypsyBallGlow').find('**/glow_aura')
        self.glowHalo.reparentTo(self.glow)
        self.glowHalo.setColorScale(0.800000, 0.696, 0.299, 0.100)
        self.glowHalo.setScale(0.5)
        self.fadeIval = None
        self.scaleIval = None


    def createTrack(self, lod = None):
        scaleUpHalo = self.glow.scaleInterval(0.149, 1.0, startScale = 0.9, blendType = 'easeInOut')
        scaleDownHalo = self.glow.scaleInterval(0.149, 0.9, startScale = 1.0, blendType = 'easeInOut')
        self.scaleIval = Sequence(scaleDownHalo, scaleUpHalo)
        self.startEffect = Sequence(Func(self.scaleIval.loop))
        self.endEffect = Sequence(Func(self.scaleIval.finish))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)


    def enableEffect(self):
        if self.scaleIval:
            self.scaleIval.loop()



    def disableEffect(self):
        if self.scaleIval:
            self.scaleIval.pause()



    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)


    def destroy(self):
        self.glow.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
