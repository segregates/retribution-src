from panda3d.core import NodePath
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pirate import Pirate
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import Beacon
from pirates.pvp import PVPGlobals


class DistributedPirateBase(DistributedObject.DistributedObject, Pirate.Pirate):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBase')

    def __init__(self, cr):
        self.masterHuman = base.cr.human
        DistributedObject.DistributedObject.__init__(self, cr)
        Pirate.Pirate.__init__(self)
        self.beacon = None
        self.dnaKey = None

    def delete(self):
        Pirate.Pirate.delete(self)
        DistributedObject.DistributedObject.delete(self)

    def disable(self):
        self.dnaKey = self.getDnaKey()
        DistributedObject.DistributedObject.disable(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if not (self.loaded) or self.dnaKey != self.getDnaKey():
            self.generateHuman(self.style.gender, self.masterHuman)

    def showBeacon(self, team):
        if self.beacon:
            self.hideBeacon()
        if team > 0:
            self.beaconNodePath = self.nametag3d.attachNewNode('beacon')
            self.beacon = Beacon.getBeacon(self.beaconNodePath)
            self.beacon.setZ(2)
            self.beacon.setBillboardPointWorld()
            self.exposeJoint(self.beaconNodePath, 'modelRoot', 'name_tag', '500')
            self.beacon.setColor(PVPGlobals.getTeamColor(team))

    def hideBeacon(self):
        if self.beacon:
            self.beacon.remove_node()
        self.beacon = None

    def getDnaKey(self):
        return self.getStyle().makeNetString()
