from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify.DirectNotifyGlobal import directNotify

from TradableInventoryBase import TradableInventoryBase

class DistributedInventoryUD(TradableInventoryBase, DistributedObjectUD):
    notify = directNotify.newCategory('DistributedInventoryUD')
