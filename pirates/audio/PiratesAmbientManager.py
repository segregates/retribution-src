from direct.directnotify import DirectNotifyGlobal
from pirates.audio import AmbientManagerBase
from pirates.audio import SoundGlobals


class PiratesAmbientManager(AmbientManagerBase.AmbientManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesAmbientManager')

    def __init__(self):
        AmbientManagerBase.AmbientManagerBase.__init__(self)
        self.volumeModifierDict = {
            SoundGlobals.AMBIENT_JUNGLE: 0.60,
            SoundGlobals.AMBIENT_SWAMP: 0.75,
            SoundGlobals.AMBIENT_JAIL: 1.25,
            SoundGlobals.AMBIENCE_PORT_ROYAL: 0.4,
            SoundGlobals.AMBIENCE_PORT_ROYAL_NIGHT: 0.4,
            SoundGlobals.AMBIENCE_FORT: 0.3
        }

    def requestFadeIn(self, name, duration = 5, finalVolume = 1.0, priority = 0, modifier = False):
        if name and not name in self.ambientDict:
            self.load(name, 'audio/' + name)
        if name in self.volumeModifierDict.keys() and modifier:
            finalVolume = finalVolume * self.volumeModifierDict[name]
        AmbientManagerBase.AmbientManagerBase.requestFadeIn(self, name, duration, finalVolume, priority)

    def requestChangeVolume(self, name, duration, finalVolume, priority = 0):
        newFinalVolume = finalVolume
        if name in self.volumeModifierDict.keys():
            newFinalVolume = finalVolume * self.volumeModifierDict[name]
        AmbientManagerBase.AmbientManagerBase.requestChangeVolume(self, name, duration, newFinalVolume, priority)
