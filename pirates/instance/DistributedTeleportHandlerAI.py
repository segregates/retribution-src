from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedTeleportHandlerAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def startTeleportProcess(self, todo0, todo1, bandId):
        """No idea at all how this would go..."""

    def continueTeleportToTZ(self):
        sender = self.air.getMsgSender()
        self.sendUpdateToChannel(sender, 'waitInTZ', [[0], self.parentId]) # TODO: Get the objIds.

    def teleportToInstanceReady(self, zoneId):
        """Okay, I guess this would end up calling the continueTeleportToInstance method in the client class, but seriously, how would it get to that point with ALL of those variables that would have to be defined?"""

    def readyToFinishTeleport(self, instanceDoId):
        """I would guess this ends up calling teleportToInstanceCleanup in the main class... but what do you do with instanceDoId? Ah, who cares, let's call it:"""
        sender = self.air.getMsgSender()
        self.sendUpdateToChannel(sender, 'teleportToInstanceCleanup', [])

    def teleportToInstanceFinal(self, doId):
        """What does this even want you to do..."""

    def avatarLeft(self):
        """Yay, another confusing method with no idea on what you need to do."""
