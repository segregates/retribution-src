from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedInstanceBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInstanceBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.accept('sendAvToJail', self.__sendAvToJail)

    def avatarDied(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            self.__sendAvToJail(av)

    def findAJail(self, av):
        returnLoc = av.getReturnLocation()
        obj = self.air.uid2do.get(returnLoc)
        jail = getattr(obj, 'jail', None)
        if jail is None:
            jail = self.air.portRoyalJail

        return jail

    def __sendAvToJail(self, av):
        jail = self.findAJail(av)
        jail.allocateCell(av)
        av.b_setUnderArrest(1)
        av.addDeathPenalty()
        self.sendUpdateToAvatarId(av.doId, 'sendLocalAvatarToJail', [jail.doId, jail.parentId, jail.zoneId])
