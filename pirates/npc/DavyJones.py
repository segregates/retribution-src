from direct.directnotify import DirectNotifyGlobal
from pirates.npc.Skeleton import Skeleton
from pirates.movement.AnimationMixer import AnimationMixer
from pirates.pirate.BipedAnimationMixer import BipedAnimationMixer
from pirates.pirate import AvatarTypes
from pirates.pirate.AvatarType import AvatarType
from pirates.pirate import Biped
AnimDict = { }

class DavyJones(Skeleton):
    AnimList = Biped.djCustomAnimList

    class AnimationMixer(AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('DavyJonesAnimationMixer')
        LOOP = BipedAnimationMixer.LOOP
        ACTION = BipedAnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
            'walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
            'hit': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
            'idle_hit': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
            'attack01': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
            'attack02': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
            'attack03': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
            'jump_attack': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
            'defeat': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE'])
        }


    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))

    setupAnimInfo = classmethod(setupAnimInfo)

    def __init__(self):
        Skeleton.__init__(self, animationMixerClass = self.AnimationMixer)


    def setAvatarType(self, avatarType = AvatarTypes.DavyJones):
        if self.loaded:
            return None

        self.avatarType = AvatarType.fromTuple(avatarType)
        self.generateSkeleton()
        self.style = 'dj'
        self.initializeDropShadow()
        self.initializeNametag3d()
        self.setHeight(8.0)


    def generateSkeletonBody(self, copy = 1):
        filePrefix = 'models/char/dj'
        animPrefix = 'models/char/dj'
        if filePrefix is None:
            self.notify.error('unknown body style: %s' % self.style)

        animList = DavyJones.AnimList
        for anim in animList:
            AnimDict[anim[0]] = animPrefix + '_' + anim[1]

        lodString = '2000'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '1000', copy)
        self.loadAnims(AnimDict, 'modelRoot', 'all')
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '500', copy)
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '250', copy)
        self.makeSubpart('head', [
            'def_head01'], [])
        self.makeSubpart('torso', [
            'def_spine01'], [
            'def_head01'])
        self.makeSubpart('legs', [
            'master_group'], [
            'def_spine01'])
        self.setSubpartsComplete(True)
        self.find('**/actorGeom').setH(180)
        self.flattenSkeleton()
        self.setLightOff(1)


    def getDeathAnimName(self):
        return 'defeat'
