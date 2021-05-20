from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals

class FriendManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.otherToon = 0

    def generate(self):
        base.cr.friendManager = self
        DistributedObject.generate(self)

    def disable(self):
        base.cr.friendManager = None
        DistributedObject.disable(self)

    def delete(self):
        base.cr.friendManager = None
        DistributedObject.delete(self)

    def up_friendQuery(self, inviteeId):
        self.otherToon = inviteeId
        self.sendUpdate('friendQuery', [inviteeId])
        self.notify.debug('Client: friendQuery(%d)' % inviteeId)

    def up_cancelFriendQuery(self, context):
        self.sendUpdate('cancelFriendQuery', [context])
        self.notify.debug('Client: cancelFriendQuery(%d)' % context)

    def up_inviteeFriendConsidering(self, yesNo, context):
        self.sendUpdate('inviteeFriendConsidering', [yesNo, context])
        self.notify.debug('Client: inviteeFriendConsidering(%d, %d)' % (yesNo, context))

    def up_inviteeFriendResponse(self, yesNoMaybe, context):
        if yesNoMaybe == 1:
            friend = base.cr.identifyFriend(self.otherToon)
            base.cr.piratesFriendsManager.friendOnline(self.otherToon, friend.getName())
            messenger.send(OTPGlobals.AvatarFriendAddEvent, [self.otherToon, friend])

        self.sendUpdate('inviteeFriendResponse', [yesNoMaybe, context])
        self.notify.debug('Client: inviteeFriendResponse(%d, %d)' % (yesNoMaybe, context))

    def up_inviteeAcknowledgeCancel(self, context):
        self.sendUpdate('inviteeAcknowledgeCancel', [context])
        self.notify.debug('Client: inviteeAcknowledgeCancel(%d)' % context)

    def friendConsidering(self, yesNoAlready, context):
        self.notify.info('Roger Client: friendConsidering(%d, %d)' % (yesNoAlready, context))
        messenger.send(OTPGlobals.AvatarFriendConsideringEvent, [yesNoAlready, context])

    def friendResponse(self, yesNoMaybe, context):
        if yesNoMaybe == 1:
            friend = base.cr.identifyFriend(self.otherToon)
            base.cr.piratesFriendsManager.friendOnline(self.otherToon, friend.getName())
            messenger.send(OTPGlobals.AvatarFriendAddEvent, [self.otherToon, friend])
        else:
            messenger.send(OTPGlobals.AvatarFriendConsideringEvent, [yesNoMaybe, context])

        self.notify.debug('Client: friendResponse(%d, %d)' % (yesNoMaybe, context))
        messenger.send('friendResponse', [yesNoMaybe, context])

    def inviteeFriendQuery(self, inviterId, inviterName, inviterDna, context):
        self.notify.debug('Client: inviteeFriendQuery(%d, %s, dna, %d)' % (inviterId, inviterName, context))
        if not hasattr(base, 'localAvatar'):
            self.up_inviteeFriendConsidering(0, context)
            return
        if base.localAvatar.isIgnored(inviterId):
            self.up_inviteeFriendConsidering(4, context)
            return
        if not base.localAvatar.acceptingNewFriends:
            self.up_inviteeFriendConsidering(6, context)
            return
        self.up_inviteeFriendConsidering(1, context)
        self.otherToon = inviterId
        messenger.send(OTPGlobals.AvatarFriendInvitationEvent, [inviterId, inviterName, context])

    def inviteeCancelFriendQuery(self, context):
        self.notify.debug('Client: inviteeCancelFriendQuery(%d)' % context)
        messenger.send('cancelFriendInvitation', [context])
        self.up_inviteeAcknowledgeCancel(context)
    
    def requestTFCode(self, callback):
        self.tfCallback = callback
        self.sendUpdate('requestTFCode')
    
    def redeemTFCode(self, code, callback):
        self.tfCallback = callback
        self.sendUpdate('redeemTFCode', [code])
    
    def tfResponse(self, response, code):
        self.tfCallback(response, code)