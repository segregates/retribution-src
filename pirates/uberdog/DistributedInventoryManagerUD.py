from panda3d.core import Datagram
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import *
from direct.distributed.PyDatagram import *
from direct.distributed.MsgTypes import *
from direct.fsm.FSM import FSM
from UberDogGlobals import *
import InventoryInit

class InventoryRequest(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryRequest')

    def __init__(self, mgr):
        FSM.__init__(self, 'InventoryRequest')
        self.mgr = mgr
        self.air = self.mgr.air

        self.aborted = False

    def enterStart(self, ownerId, inventoryId):
        self.ownerId = ownerId
        self.inventoryId = inventoryId

        nextState = 'Query'

        if not self.inventoryId:
            nextState = 'Create'

        self.demand(nextState)

    def enterCreate(self):
        self.air.dbInterface.createObject(self.air.dbId, self.air.dclassesByName['PirateInventoryUD'],
                                          self.__getDefaultInventory(), self.__handleCreate)

    def __getDefaultInventory(self):
        locatables = InventoryInit.StartingLocatables

        defaults = {InventoryType.OverallRep: 0, InventoryType.GeneralRep: 0}
        accumulators = []
        for i in xrange(InventoryType.begin_Accumulator, InventoryType.end_Accumulator):
            accumulators.append((i, defaults.get(i, 0)))

        inventory = {}
        inventory['setInventoryVersion'] = [InventoryInit.UberDogRevision]
        inventory['setLocatables'] = [locatables]
        inventory['setAccumulators'] = [accumulators]
        inventory['setCategoryLimits'] = [InventoryInit.CategoryLimits.items()]
        inventory['setStacks'] = [InventoryInit.StackStartsWith.items()]
        inventory['setStackLimits'] = [InventoryInit.StackLimits.items()]
        inventory['setOwnerId'] = [self.ownerId]
        return inventory

    def __handleCreate(self, doId):
        if self.aborted:
            return

        if not doId:
            self.gotObject(None)
            return

        self.inventoryId = doId
        self.air.dbInterface.updateObject(self.air.dbId, self.ownerId,
                                          self.air.dclassesByName['DistributedPlayerPirateUD'],
                                          {'setInventoryId': [self.inventoryId]})

        self.gotObject(self)

    def enterQuery(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.inventoryId, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.air.dclassesByName['PirateInventoryUD']:
            self.gotObject(None)
            return

        version = fields.get('setInventoryVersion', [0])[0]
        if version != InventoryInit.UberDogRevision:
            # Need to update
            self.notify.info('Updating inventory %d from version %d to %d' % (self.inventoryId, version, InventoryInit.UberDogRevision))

            __def = self.__getDefaultInventory()
            fields['setInventoryVersion'] = [InventoryInit.UberDogRevision]
            fields['setStackLimits'] = __def['setStackLimits']
            fields['setCategoryLimits'] = __def['setCategoryLimits']

            stackLimits = dict(__def['setStackLimits'][0])
            stacks = InventoryInit.StackStartsWith
            stacks.update({item: min(amount, stackLimits.get(item, amount)) for item, amount in fields.get('setStacks', [[]])[0]})

            if config.GetBool('inv-force-skill-2', True):
                stacks.update(InventoryInit._StartingSkills)

            fields['setStacks'] = [stacks.items()]

            accumulators = [(item, min(amount, InventoryInit.AccumulatorLimits.get(item, amount)))
                            for item, amount in fields.get('setAccumulators', [[]])[0]]

            self.air.dbInterface.updateObject(self.air.dbId, self.inventoryId,
                                              self.air.dclassesByName['PirateInventoryUD'],
                                              fields)

        self.demand('Activate')

    def enterActivate(self):
        if self.aborted:
            return

        self.air.sendActivate(self.inventoryId, self.ownerId, 2,
                              self.air.dclassesByName['PirateInventoryUD'],
                              {'setOwnerId': [self.ownerId], 'locatablesReady': [1]})

        self.gotObject(self)

    def gotObject(self, obj):
        if self.aborted:
            return

        self.mgr.handleGotInventory(obj, self.ownerId)

class DistributedInventoryManagerUD(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerUD')

    def __init__(self, air):
        self.air = air
        self.inventories = {}

        self.accept('UD_avExit', self.__handleAvatarExit)

    def initiateAvatarInventory(self, avId, inventoryId):
        self.notify.debug('initiateAvatarInventory: %d %d' % (avId, inventoryId))
        request = InventoryRequest(self)
        request.demand('Start', avId, inventoryId)
        self.inventories[avId] = request

    def handleGotInventory(self, obj, avId):
        messenger.send('inventory-loaded-%d' % avId, [obj])
        if avId in self.inventories:
            del self.inventories[avId]

        if obj is None:
            self.notify.info('Failed to load %d\'s inventory!' % avId)
            channel = self.air.csm.GetPuppetConnectionChannel(avId)
            dg = PyDatagram()
            dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_EJECT)
            dg.addUint16(122)
            dg.addString('A problem happened while loading your inventory. Please contact support.')
            self.air.send(dg)

    def getInventoryFromAvatarId(self, avId):
        if avId in self.inventories:
            return self.inventories[avId]
        return None

    def __handleAvatarExit(self, avId):
        inv = self.inventories.pop(avId, None)
        if inv:
            if isinstance(inv, InventoryRequest):
                inv.aborted = True
