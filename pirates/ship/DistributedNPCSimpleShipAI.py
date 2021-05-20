from direct.directnotify import DirectNotifyGlobal
from pirates.ship.DistributedSimpleShipAI import DistributedSimpleShipAI

class DistributedNPCSimpleShipAI(DistributedSimpleShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSimpleShipAI')

    def __init__(self, air):
        DistributedSimpleShipAI.__init__(self, air)

   #announceAttack(DoId, uint8) broadcast;
   #setHunterLevel(int8) broadcast ram;