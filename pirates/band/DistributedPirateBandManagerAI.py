from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM
from pirates.band import BandConstance

class LoadBandMemberFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('LoadBandMemberFSM')

    def __init__(self, mgr, pirate, bandId, callback):
        FSM.__init__(self, 'LoadBandMemberFSM')
        self.mgr = mgr
        self.pirate = pirate
        self.bandId = 0
        self.callback = callback
        self.done = False

    def start(self):
        self.memberId = 0 #TODO generate id
        if not self.memberId in self.mgr.air.doId2do:
            zoneId = 0
            self.mgr.air.sendActivate(self.memberId, self.mgr.air.districtId, zoneId)
            self.acceptOnce('generate-%d' % self.memberId, self.__generated)
        else:
            self.__generated(self.mgr.air.doId2do(self.memberId))

    def __generated(self, member):
        self.member = member
        self.member.b_setAvatarId(self.memberId)
        self.member.b_setBandId(self.bandId)

        self.mgr.bandMembers.append(self.member)
        self.demand('Off')

    def enterOff(self):
        self.done = True
        self.callback(self.member)

class DistributedPirateBandManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBandManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.activeInvites = {}
        self.bandMembers = {}

    def delete(self):
        DistributedObjectAI.delete(self)
        self.activeInvites = {}
        #TODO clear invites?

    def pirateWentOffline(self, avatarId):
        if avatarId in self.activeInvites:
            invites = self.activeInvites.get(avatarId)
            for invite in invites:
                self.sendUpdateToAvatarId(invite, "invitationCancel", [avatarId])
            self.activeInvites.pop(avatarId, None)

    def joinCrew(self, avId, managerId):
        pass

    def createInvite(self, senderId, receiverId):
        sender = self.air.doId2do.get(senderId)

        if not sender:
            self.notify.warning("Failed to create invite. Sender is not online.")
            return False

        receiver = self.air.doId2do.get(receiverId)

        if not receiver:
            self.notify.warning("Failed to create invite. Receiver is not online.")
            return False

        if senderId in self.activeInvites:
            inviteList = self.activeInvites.get(senderId)
            invitelist.append(receiverId)
            self.activeInvites.pop(senderId, inviteList)

        self.sendUpdateToAvatarId(receiverId, "InvitationFrom", [senderId, sender.getName()])

    def hasInvite(self, senderId, receiverId):
        if senderId not in self.activeInvites:
            return False

        invites = self.activeInvites.get(senderId)
        if receiverId in invites:
            return True

        return False

    def sendRequestOutcome(self, receiverId, avatarId, avatarName=None, responce=BandConstance.outcome_ok):
        self.notify.info("Sending request outcome. receiverId: %s avatarId: %s avatarName: %s responce: %s" % (receiverId,avatarId, avatarName, responce))

        name = "Unknown"
        if avatarName is None:
            avatar = self.air.doId2do.get(avatarId)
            if not avatar:
                name = avatar.getName()

        self.sendUpdateToAvatarId(receiverId, "requestOutCome", [avatarId, name, responce])

    def requestInvite(self, avId):
        self.notify.info("requestInvite: avId(%s)" % avId)

        senderId = self.air.getAvatarIdFromSender()

        if not config.GetBool('want-crews', False):
            self.sendRequestOutcome(senderId, avId, responce=BandConstance.outcome_declined)

        if self.hasInvite(senderId, avId):
            self.sendRequestOutcome(senderId, avId, responce=BandConstance.outcome_already_invited)
            return

        self.createInvite(senderId, avId)

    def requestRejoin(self, avId, isManager):
        self.notify.info("requestRejoin: avId(%s) isManager(%s)" % (avId, isManager))

    def requestCancel(self, avId):
        self.notify.info("requestCancel: avId(%s)" % avId)

    def invitationResponce(self, avId, avName, responce):
        self.notify.info("inviationResponce: avId(%s) avName(%s) responce(%s)" % (avId, avName, responce))

    def rejoinResponce(self, avId, isManager, responce):
        self.notify.info("rejoinResponse: avId(%s) isManager(%s) responce(%s)" % (avId, isManager, responce))

    def requestBoot(self, avId):
        self.notify.info("requestBoot: avId(%s)" % avId)

    def requestRemove(self, avId):
        self.notify.info("requestRemove: avId(%s)" % avId)

    def requestRejoinCheck(self, avId):
        self.notify.info("requestRejoinCheck: avId(%s)" % avId)

    def requestCrewIconUpdate(self, iconKey):
        self.notify.info("requestCrewIconUpdate: iconKey(%s)" % iconKey)
