from pirates.distributed.DistributedInteractiveAI import *
from pirates.piratesbase import PiratesGlobals

class DistributedDinghyAI(DistributedInteractiveAI):
    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.air = air
        self.radius = 25
        self.locationId = 0

    def generate(self):
        DistributedInteractiveAI.generate(self)

    def handleInteract(self, avId, interactType, instant):
        # It's set on the clients to deny interaction, but
        # if they manage get past the sanity check the server will
        # deny them anyway.
        if config.GetBool('want-seas-closed', False):
            msg = 'Client bypassed sanity check and called DistributedDinghyAI'
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), message=msg)

        return REJECT # TO DO

    def selectOption(self, optionId):
        self.optionId = optionId

    def setInteractRadius(self, radius):
        self.radius = radius

    def d_setInteractRadius(self, radius):
        self.sendUpdate('setInteractRadius', [radius])

    def b_setInteractRadius(self, radius):
        self.setInteractRadius(radius)
        self.d_setInteractRadius(radius)

    def getInteractRadius(self):
        return self.radius

    def setLocationId(self, locationId):
        self.locationId = locationId

    def d_setLocationId(self, locationId):
        self.sendUpdate('setLocationId', [locationId])

    def b_setLocationId(self, locationId):
        self.setLocationId(locationId)
        self.d_setLocationId(locationId)

    def getLocationId(self):
        return self.locationId

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        obj.setInteractRadius(int(float(data['Aggro Radius'])))
        return obj
