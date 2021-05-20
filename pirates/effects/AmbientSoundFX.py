from pirates.leveleditor.LevelEntity import LevelEntity

class AmbientSoundFX(LevelEntity):

    def __init__(self):
        LevelEntity.__init__(self)
        base.cr.timeOfDayManager.registerAmbientSFXNode(self)


    def setProperty(self, propertyName, propertyValue):
        if propertyName == 'Range':
            self.range = float(propertyValue)
        else:
            LevelEntity.setProperty(propertyName, propertyValue)


    def cleanUp(self):
        LevelEntity.cleanUp(self)
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.removeAmbientSFXNode(self)
