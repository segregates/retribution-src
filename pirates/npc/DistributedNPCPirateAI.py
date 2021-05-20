from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI

class DistributedNPCPirateAI(DistributedBattleNPCAI):
    notify = directNotify.newCategory('DistributedNPCPirateAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        self.dnaString = ''

    def disable(self):
        DistributedBattleNPCAI.disable(self)

    def delete(self):
        DistributedBattleNPCAI.delete(self)

    def generate(self):
        DistributedBattleNPCAI.generate(self)

    def announceGenerate(self):
        DistributedBattleNPCAI.announceGenerate(self)
    
    def setDNAString(self, dnaString):
        self.dnaString = dnaString
    
    def getDNAString(self):
        return self.DNAString

    def isBattleable(self):
        return 0

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedBattleNPCAI.makeFromObjectKey(air, objKey, data)
        return obj
