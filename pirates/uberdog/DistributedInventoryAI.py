from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.inventory import InventoryGlobals
from TradableInventoryBase import *
from UberDogGlobals import *

class DistributedInventoryAI(TradableInventoryBase, DistributedObjectAI):
    notify = directNotify.newCategory('DistributedInventoryAI')

    def __init__(self, air):
        TradableInventoryBase.__init__(self, air)
        DistributedObjectAI.__init__(self, air)
