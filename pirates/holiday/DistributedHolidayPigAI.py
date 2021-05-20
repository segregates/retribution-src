from direct.directnotify import DirectNotifyGlobal
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI

class DistributedHolidayPigAI(DistributedHolidayObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayPigAI')

    TRADE_INVENTORY_FULL = 0
    TRADE_SUCCESS = 1
    TRADE_FAILED = 2

    def __init__(self, air):
        DistributedHolidayObjectAI.__init__(self, air)
        self.pigRoasting = False

    def setPigRoasting(self, value):
        self.pigRoasting = value

    def d_setPigRoasting(self, value):
        self.sendUpdate('setPigRoasting', [value])

    def b_setPigRoasting(self, value):
        self.setPigRoasting(value)
        self.d_setPigRoasting(value)

    def getPigRoasting(self):
        return self.pigRoasting

    def makeTradeResponse(self, result):
        self.sendUpdate('makeTradeResponse', [result])

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        if cls is None:
            cls = DistributedHolidayPigAI
        obj = DistributedHolidayObjectAI.makeFromObjectKey(cls, air, objKey, data)
        return obj
