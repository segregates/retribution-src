from direct.distributed import DistributedObjectAI

class DistributedNPCToyAI(DistributedObjectAI.DistributedObjectAI):

    def ___init___(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)

    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def disable(self):
        DistributedObjectAI.DistributedObjectAI.disable(self)
