from direct.distributed import DistributedObjectAI
from pirates.inventory.LootableAI import LootableAI

class DistributedQuestPropAI(DistributedObjectAI.DistributedObjectAI, LootableAI):

    def ___init___(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        LootableAI.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)

    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def disable(self):
        DistributedObjectAI.DistributedObjectAI.disable(self)

    def posControlledByCell(self):
        return True

    @staticmethod
    def makeFromObjectKey(air, objKey, data):
        cls = DistributedQuestPropAI
        obj = cls(air)
        #obj.setUniqueId(objKey)
        #obj.setPos(data.get('Pos', 0))
        #obj.setHpr(data.get('Hpr', 0))
        return obj