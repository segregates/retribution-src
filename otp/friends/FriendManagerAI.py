from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.otpbase import OTPGlobals
import datetime, uuid, time, string, random

AVAILABLE_CHARS = string.ascii_lowercase + string.digits

class AddTrueFriend:

    def __init__(self, manager, av, targetId, code):
        self.air = manager.air
        self.manager = manager
        self.av = av
        self.targetId = targetId
        self.code = code

    def start(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.targetId, self.__gotAvatar)
    
    def remove(self):
        avId = self.av.doId

        if avId in self.manager.tfFsms:
            del self.manager.tfFsms[avId]
            self.manager.addDelay(avId)
    
    def __gotAvatar(self, dclass, fields):
        dclasses = self.air.dclassesByName['DistributedToonAI']

        if dclass != dclasses:
            self.remove()
            return

        try:
            maxFriends = fields['setMaxFriends'][0]
        except:
            maxFriends = 200

        if maxFriends < 200:
            maxFriends = 200

        friendsList = fields['setFriendsList'][0]
        trueFriendsList = fields['setTrueFriends'][0]
        name = fields['setName'][0]
        avId = self.av.doId
        
        if avId in trueFriendsList and avId in friendsList:
            self.manager.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_ALREADY_FRIENDS_NAME, name])
            return
        elif avId not in friendsList:
            if len(friendsList) >= maxFriends:
                self.manager.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_FRIENDS_LIST_FULL_HIM, name])
                return
            
            friendsList.append(avId)
            self.air.send(dclasses.aiFormatUpdate('setFriendsList', self.targetId, self.targetId, self.air.ourChannel, [friendsList]))
        
        if self.targetId not in self.av.friendsList:
            self.av.extendFriendsList(self.targetId)
        
        self.air.dbGlobalCursor.trueFriends.remove({'_id': self.code})
        self.av.addTrueFriend(self.targetId)
        trueFriendsList.append(avId)
        self.air.send(dclasses.aiFormatUpdate('setTrueFriends', self.targetId, self.targetId, self.air.ourChannel, [trueFriendsList]))
        self.av.sendUpdate('friendsNotify', [self.targetId, 2])
        self.air.send(dclasses.aiFormatUpdate('friendsNotify', self.targetId, self.targetId, self.air.ourChannel, [avId, 2]))
        self.manager.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_SUCCESS, name])
        self.remove()

class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.currentContext = 0
        self.requests = {}
        self.tfFsms = {}
        self.tfDelays = {}
        #self.air.dbGlobalCursor.trueFriends.create_index('date', expireAfterSeconds=OTPGlobals.TF_EXPIRE_SECS)

    def friendQuery(self, requested):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to friend a player that does not exist!')
            return

        requestedAv = self.air.doId2do.get(requested)
        
        if not requestedAv:
            self.sendUpdateToAvatarId(avId, 'friendConsidering', [11, context])
            return

        context = self.currentContext
        self.currentContext += 1
        
        if len(av.getFriendsList()) >= av.getMaxFriends():
            self.sendUpdateToAvatarId(avId, 'friendConsidering', [12, context])
            return
        if len(requestedAv.getFriendsList()) >= requestedAv.getMaxFriends():
            self.sendUpdateToAvatarId(avId, 'friendConsidering', [13, context])
            return
        if requested == avId:
            self.sendUpdateToAvatarId(avId, 'friendConsidering', [3, context])
            return
        if requested in av.getFriendsList():
            self.sendUpdateToAvatarId(avId, 'friendConsidering', [2, context])
            return

        self.requests[context] = [ [ avId, requested ], 'friendQuery']
        self.sendUpdateToAvatarId(requested, 'inviteeFriendQuery', [avId, av.getName(), av.getDNAString(), context])

    def cancelFriendQuery(self, context):
        avId = self.air.getAvatarIdFromSender()

        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to cancel a request that doesn\'t exist!')
            return

        if avId != self.requests[context][0][0]:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to cancel someone elses request!')
            return

        self.requests[context][1] = 'cancelled'
        self.sendUpdateToAvatarId(self.requests[context][0][1], 'inviteeCancelFriendQuery', [context])

    def inviteeFriendConsidering(self, yesNo, context):
        avId = self.air.getAvatarIdFromSender()

        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to consider a friend request that doesn\'t exist!')
            return

        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to consider for someone else!')
            return

        if self.requests[context][1] != 'friendQuery':
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to reconsider friend request!')
            return

        if yesNo != 1:
            self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendConsidering', [yesNo, context])
            del self.requests[context]
            return

        self.requests[context][1] = 'friendConsidering'
        self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendConsidering', [yesNo, context])

    def inviteeFriendResponse(self, response, context):
        avId = self.air.getAvatarIdFromSender()

        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to respond to a friend request that doesn\'t exist!')
            return

        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to respond to someone else\'s request!')
            return

        if self.requests[context][1] == 'cancelled':
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to respond to non-active friend request!')
            return

        self.sendUpdateToAvatarId(self.requests[context][0][0], 'friendResponse', [response, context])

        if response == 1:
            requested = self.requests[context][0][1]

            if requested in self.air.doId2do:
                requested = self.air.doId2do[requested]
            else:
                del self.requests[context]
                return

            requester = self.requests[context][0][0]

            if requester in self.air.doId2do:
                requester = self.air.doId2do[requester]
            else:
                del self.requests[context]
                return

            requested.extendFriendsList(requester.getDoId())
            requester.extendFriendsList(requested.getDoId())

        del self.requests[context]

    def inviteeAcknowledgeCancel(self, context):
        avId = self.air.getAvatarIdFromSender()

        if not context in self.requests:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to acknowledge the cancel of a friend request that doesn\'t exist!')
            return

        if avId != self.requests[context][0][1]:
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to acknowledge someone else\'s cancel!')
            return

        if self.requests[context][1] != 'cancelled':
            self.air.writeServerEvent('suspicious', avId=avId, message='Player tried to cancel non-cancelled request!')
            return

        del self.requests[context]
    
    def getRandomCharSequence(self, count):
        return ''.join(random.choice(AVAILABLE_CHARS) for i in xrange(count))
    
    def getTFCode(self, tryNumber):
        if tryNumber == OTPGlobals.MAX_TF_TRIES:
            return str(uuid.uuid4())
        
        code = 'TT %s %s' % (self.getRandomCharSequence(3), self.getRandomCharSequence(3))

        if self.air.dbGlobalCursor.trueFriends.find({'_id': code}).count() > 0:
            return self.getTFCode(tryNumber + 1)
        
        return code
    
    def addDelay(self, avId):
        self.tfDelays[avId] = time.time() + 1.0
    
    def hasDelay(self, avId):
        return avId in self.tfDelays and self.tfDelays[avId] > time.time()
    
    def requestTFCode(self):
        avId = self.air.getAvatarIdFromSender()
        
        if self.hasDelay(avId):
            return

        av = self.air.doId2do.get(avId)
        
        if not av:
            return
        
        tfRequest = av.getTFRequest()
        
        if tfRequest[1] >= OTPGlobals.MAX_TF_TRIES and tfRequest[0] >= time.time():
            self.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_COOLDOWN, ''])
            return
        
        self.addDelay(avId)
        code = self.getTFCode(0)
        
        self.air.dbGlobalCursor.trueFriends.insert({'_id': code, 'date': datetime.datetime.utcnow(), 'avId': avId})
        av.b_setTFRequest((time.time() + OTPGlobals.TF_COOLDOWN_SECS, tfRequest[1] + 1))
        self.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_SUCCESS, code])
        self.addDelay(avId)
    
    def redeemTFCode(self, code):
        avId = self.air.getAvatarIdFromSender()

        if avId in self.tfFsms or self.hasDelay(avId):
            return

        av = self.air.doId2do.get(avId)
        
        if not av:
            return
        
        self.addDelay(avId)
        fields = self.air.dbGlobalCursor.trueFriends.find_one({'_id': code})
        
        if not fields:
            self.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_UNKNOWN_SECRET, ''])
            return
            
        targetId = fields['avId']
        
        if avId == targetId:
            self.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_SELF_SECRET, ''])
            return
        elif av.isTrueFriends(targetId):
            self.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_ALREADY_FRIENDS, ''])
            return
        elif targetId not in av.getFriendsList() and len(av.getFriendsList()) >= av.getMaxFriends():
            self.sendUpdateToAvatarId(avId, 'tfResponse', [OTPGlobals.TF_FRIENDS_LIST_FULL_YOU, ''])
            return
        
        tfOperation = AddTrueFriend(self, av, targetId, code)
        self.tfFsms[avId] = tfOperation
        tfOperation.start()