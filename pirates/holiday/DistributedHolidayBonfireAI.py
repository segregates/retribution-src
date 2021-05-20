from direct.directnotify import DirectNotifyGlobal
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI

class DistributedHolidayBonfireAI(DistributedHolidayObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayBonfireAI')

    def __init__(self, air):
        DistributedHolidayObjectAI.__init__(self, air)

    def setFireStarted(self, value):
        self.fireStarted = value

    def d_setFireStarted(self, value):
        self.sendUpdate('setFireStarted', [value])

    def b_setFireStarted(self, value):
        self.setFireStarted(value)
        self.d_setFireStarted(value)

    def getFireStarted(self):
        return self.fireStarted

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        if cls is None:
            cls = DistributedHolidayBonfireAI
        obj = DistributedHolidayObjectAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setFireStarted(False)
        return obj