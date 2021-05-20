from direct.interval.IntervalGlobal import ActorInterval
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from direct.showbase.PythonUtil import report
from pirates.movement.AnimationMixer import ReducedAnimationMixer

class UsesAnimationMixer:
    def __init__(self, animationMixerType=None):
        if hasattr(self, 'animationMixer') and self.animationMixer:
            if not isinstance(self.animationMixer, animationMixerType):
                return

        self.__mixer = None
        if animationMixerType:
            self.animationMixer = animationMixerType(self)
        else:
            self.animationMixer = None
        self.reducedMixer = None

    def delete(self):
        if self.animationMixer:
            self.animationMixer.delete()
            self.animationMixer = None

        if self.reducedMixer:
            self.reducedMixer.delete()
            self.reducedMixer = None

    def play(self, *args, **kwargs):
        if self.__mixer:
            defaultBlendT = self.__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendInT = kwargs.pop('blendInT', defaultBlendT)
        blendOutT = kwargs.pop('blendOutT', defaultBlendT)
        blendInto = kwargs.pop('blendInto', None)
        if self.__mixer:
            self.__mixer.play(blendInT = blendInT, blendOutT = blendOutT, blendInto = blendInto, *args, **kwargs)
        else:
            Actor.play(self, *args, **kwargs)

    def loop(self, *args, **kwargs):
        if self.__mixer:
            defaultBlendT = self.__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        blendDelay = kwargs.pop('blendDelay', 0)
        if self.__mixer:
            self.__mixer.loop(blendT = blendT, blendDelay = blendDelay, *args, **kwargs)
        elif 'rate' in kwargs:
            rate = kwargs.pop('rate')
            Actor.loop(self, *args, **kwargs)
            self.setPlayRate(rate, args[0])
        else:
            Actor.loop(self, *args, **kwargs)

    def pingpong(self, *args, **kwargs):
        if self.__mixer:
            defaultBlendT = self.__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        if self.__mixer:
            self.__mixer.pingpong(blendT = blendT, *args, **kwargs)
        else:
            Actor.pingpong(self, *args, **kwargs)

    def pose(self, *args, **kwargs):
        if self.__mixer:
            defaultBlendT = self.__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        if self.__mixer:
            self.__mixer.pose(blendT = blendT, *args, **kwargs)
        else:
            Actor.pose(self, *args, **kwargs)

    def stop(self, *args, **kwargs):
        if self.__mixer:
            self.__mixer.stop(*args, **kwargs)
        else:
            Actor.stop(self, *args, **kwargs)

    def actorInterval(self, *args, **kwargs):
        mixingWanted = kwargs.pop('mixingWanted', bool(self.__mixer))
        if mixingWanted and self.__mixer:
            defaultBlendT = self.__mixer.defaultBlendT
        elif mixingWanted and self.animationMixer:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendInT = kwargs.pop('blendInT', defaultBlendT)
        blendOutT = kwargs.pop('blendOutT', defaultBlendT)
        blendInto = kwargs.pop('blendInto', None)
        if mixingWanted:
            partName = kwargs.get('partName', None)
            return self.__mixer.actorInterval(ActorInterval(self, *args, **kwargs), partName, blendInT, blendOutT, blendInto)
        else:
            return ActorInterval(self, *args, **kwargs)

    def disableMixing(self):
        if self.__mixer:
            self.__mixer.cleanup()
            self.__mixer = None

        Actor.disableBlend(self)
        Actor.stop(self)

    def enableMixing(self):
        if self.__mixer != self.animationMixer:
            self.disableMixing()

        self.__mixer = self.animationMixer
        if self.__mixer:
            Actor.enableBlend(self)
            self.__mixer.cleanup()

    def enableReducedMixing(self):
        if not self.reducedMixer:
            self.reducedMixer = ReducedAnimationMixer(self)

        if self.__mixer != self.reducedMixer:
            self.disableMixing()

        self.__mixer = self.reducedMixer
        self.__mixer.cleanup()

    def isMixing(self):
        return self.__mixer is not None

    def printMixer(self):
        print self.__mixer
