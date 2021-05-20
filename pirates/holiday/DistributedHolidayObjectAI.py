from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *

class DistributedHolidayObjectAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayObjectAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

    def setHoliday(self, holiday):
        self.holiday = holiday

    def getHoliday(self):
        return self.holiday

    def setInteractRadius(self, radius):
        self.radius = radius

    def setInteractMode(self, mode):
        self.mode = mode

    def getInteractRadius(self):
        return self.radious

    def getInteractMode(self):
        return self.mode

    @staticmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setHoliday(data.get('Holiday', 'FoundersFeast'))
        obj.setInteractMode(data.get('Interact Mode', 'All'))
        obj.setInteractRadius(data.get('Aggro Radious', '6.0'))
        return obj
