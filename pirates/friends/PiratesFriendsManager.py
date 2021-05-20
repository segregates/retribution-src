from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.otpbase import OTPLocalizer

class PiratesFriendsManager(DistributedObjectGlobal):

    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])

    def d_requestFriendsList(self):
        self.sendUpdate('requestFriendsList', [])

    def friendList(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id, name):
        base.cr.handleFriendOnline(id, name)

    def friendOffline(self, id, name):
        base.cr.handleFriendOffline(id, name)

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])

    def receiveAvatarInfo(self, *args):
        messenger.send('avatarInfoRetrieved', list(args))

    def receiveAvatarSkillLevels(self, *args):
        messenger.send('avatarSkillLevelsRetrieved', list(args))

    def receiveAvatarShipInfo(self, *args):
        messenger.send('avatarShipInfoRetrieved', list(args))

    def d_teleportQuery(self, toId):
        self.sendUpdate('routeTeleportQuery', [toId])

    def teleportQuery(self, fromId):
        if not hasattr(base, 'localAvatar'):
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not hasattr(base.localAvatar, 'getTeleportAvailable') or not hasattr(base.localAvatar, 'ghostMode'):
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not base.localAvatar.getTeleportAvailable() or base.localAvatar.ghostMode or base.cr.playGame.getPlaceId() in [10000, 11000, 12000, 13000]:
            if hasattr(base.cr.identifyFriend(fromId), 'getName'):
                base.localAvatar.setSystemMessage(0, OTPLocalizer.WhisperFailedVisit % base.cr.identifyFriend(fromId).getName())
            self.sendUpdate('routeTeleportResponse', [ fromId, 0, 0, 0, 0 ])
            return

        hoodId = base.cr.playGame.getPlaceId()
        if hasattr(base.cr.identifyFriend(fromId), 'getName'):
            base.localAvatar.setSystemMessage(0, OTPLocalizer.WhisperComingToVisit % base.cr.identifyFriend(fromId).getName())
        self.sendUpdate('routeTeleportResponse', [
            fromId,
            base.localAvatar.getTeleportAvailable(),
            base.localAvatar.defaultShard,
            hoodId,
            base.localAvatar.getZoneId()
        ])

    def teleportResponse(self, fromId, available, shardId, hoodId, zoneId):
        base.localAvatar.teleportResponse(fromId, available, shardId, hoodId, zoneId)

    def d_whisperSCTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCTo', [toId, msgIndex])

    def setWhisperSCFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCFrom'):
            return
        base.localAvatar.setWhisperSCFrom(fromId, msgIndex)

    def d_whisperSCCustomTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCCustomTo', [toId, msgIndex])

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCCustomFrom'):
            return
        base.localAvatar.setWhisperSCCustomFrom(fromId, msgIndex)

    def d_whisperSCEmoteTo(self, toId, emoteId):
        self.sendUpdate('whisperSCEmoteTo', [toId, emoteId])

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCEmoteFrom'):
            return
        base.localAvatar.setWhisperSCEmoteFrom(fromId, emoteId)

    def receiveTalkWhisper(self, fromId, message):
        pirate = base.cr.identifyAvatar(fromId)
        if pirate:
            base.localAvatar.setTalkWhisper(fromId, pirate.getName(), message)
