from panda3d.core import Texture, Vec4
import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.interval.IntervalGlobal import *
from pirates.battle.EnemySkills import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects import PolyTrail
import random

class Axe(Weapon.Weapon):
    modelTypes = [
        'models/handheld/pir_m_hnd_axe_boarding_a',
        'models/handheld/pir_m_hnd_axe_boarding_b',
        'models/handheld/pir_m_hnd_axe_boarding_c',
        'models/handheld/pir_m_hnd_axe_boarding_d']
    models = { }
    icons = { }
    vertex_list = [
        Vec4(0.0, 0.4, 0.0, 1.0),
        Vec4(0.0, 2.0, 0.0, 1.0),
        Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {
        ItemGlobals.MotionBlurDefault: [
            Vec4(0.3, 0.3, 0.3, 0.5),
            Vec4(0.3, 0.3, 0.3, 0.5),
            Vec4(0.6, 0.6, 0.6, 0.5)],
        ItemGlobals.MotionBlurRusty: [
            Vec4(0.3, 0.4, 0.1, 0.5),
            Vec4(0.3, 0.3, 0.3, 0.5),
            Vec4(0.6, 0.6, 0.6, 0.5)],
        ItemGlobals.MotionBlurIron: [
            Vec4(0.1, 0.2, 0.4, 0.5),
            Vec4(0.4, 0.5, 0.7, 0.5),
            Vec4(0.5, 0.5, 0.9, 0.75)],
        ItemGlobals.MotionBlurSteel: [
            Vec4(1, 1, 0.4, 0.5),
            Vec4(0.4, 0.5, 0.6, 0.5),
            Vec4(0.7, 0.7, 0.8, 0.75)],
        ItemGlobals.MotionBlurFine: [
            Vec4(0.6, 0.6, 0.75, 1),
            Vec4(0.6, 0.5, 0.2, 1),
            Vec4(0.6, 0.6, 0.4, 1)],
        ItemGlobals.MotionBlurPirate: [
            Vec4(1, 0.2, 0.2, 0.5),
            Vec4(0.5, 0.5, 0.5, 0.75),
            Vec4(0.7, 0.7, 0.9, 1)],
        ItemGlobals.MotionBlurDark: [
            Vec4(1, 1, 0, 0.5),
            Vec4(0.3, 0.3, 0.3, 0.5),
            Vec4(0.1, 0.1, 0.1, 1.0)],
        ItemGlobals.MotionBlurGreen: [
            Vec4(0.5, 1, 0.1, 1.0),
            Vec4(0.2, 1, 0.2, 1.0),
            Vec4(0.3, 1, 0.4, 1.0)],
        ItemGlobals.MotionBlurRed: [
            Vec4(1, 0.5, 0.2, 1.0),
            Vec4(1, 0.3, 0.3, 1.0),
            Vec4(1, 0.1, 0.1, 1.0)] }
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'sword_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'axe')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def delete(self):
        taskMgr.remove('stopSpecialEffectTask')
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)

    def getDrawIval(self, av, ammoSkillId = 0, blendInT = 0.1, blendOutT = 0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node = av, cutoff = 60), av.actorInterval('sword_draw', playRate = 1.5, endFrame = 15, blendInT = blendInT, blendOutT = blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT = 0, blendOutT = 0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node = av, cutoff = 60), av.actorInterval('sword_putaway', playRate = 2, endFrame = 35, blendInT = blendInT, blendOutT = blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        self.setOffset()
        self.createTrail(av)

    def setOffset(self):
        startPos = self.getPos()
        endPos = startPos - (0, 0.8, 0)
        self.setPos(endPos)

    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        self.removeTrail()

    def createTrail(self, target):
        if self.isEmpty():
            return None

        if not self.motion_trail:
            motion_trail_color = []
            colorId = ItemGlobals.getVfxType1(self.itemId)
            motion_trail_color = self.motion_color.get(colorId)
            if not motion_trail_color:
                motion_trail_color = self.motion_color.get(ItemGlobals.MotionBlurDefault)

            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, motion_trail_color)
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModel('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            self.motion_trail.setBlendModeOn()
            if colorId == ItemGlobals.MotionBlurDark:
                self.motion_trail.setBlendModeOff()

            card.remove_node()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None

    def getBlurColor(self):
        colorId = ItemGlobals.getVfxType1(self.itemId)
        motion_trail_color = self.motion_color.get(colorId)
        if not motion_trail_color:
            motion_trail_color = self.motion_color.get(ItemGlobals.MotionBlurDefault)

        return motion_trail_color[2]

    def startSpecialEffect(self, skillId = None):
        taskMgr.doMethodLater(1.0, self.stopSpecialEffect, 'stopSpecialEffectTask', [
            skillId])

    def stopSpecialEffect(self, skillId = None):
        pass

    def setupSounds(cls):
        Axe.hitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_03))
        Axe.missSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_02))
        Axe.mistimedHitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_MISTIMEDHIT),)
        Axe.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_DRAW)
        Axe.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SHEATHE)

    setupSounds = classmethod(setupSounds)

def getHitSfx():
    return Axe.hitSfxs

def getMistimedHitSfx():
    return Axe.mistimedHitSfxs

def getMissSfx():
    return Axe.missSfxs
