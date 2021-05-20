from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.fsm.FSM import FSM
from otp.otpbase import OTPUtils, OTPGlobals
from otp.uberdog.RejectCode import RejectCode
import time

GUILDRANK_VETERAN = 4
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

class OperationFSM(FSM):
    DELAY = 0.25

    def __init__(self, mgr, sender, target=None):
        FSM.__init__(self, 'OperationFSM-%s' % sender)
        self.mgr = mgr
        self.air = mgr.air
        self.sender = sender
        self.target = target
        self.deleted = False
        
        if self.DELAY:
            self.mgr.operations[self.sender] = self
    
    def fsmName(self, name):
        return 'OperationFSM-%s-%s' % (id(self), name)
    
    def deleteOperation(self):
        if not self.deleted:
            if self.DELAY:
                taskMgr.doMethodLater(self.DELAY, self.__deleteOperation, self.fsmName('deleteOperation'))
            
            self.deleted = True
    
    def __deleteOperation(self, task):
        if self.sender in self.mgr.operations:
            del self.mgr.operations[self.sender]

    def enterOff(self):
        self.deleteOperation()
    
    def enterError(self, message=None):
        self.mgr.notify.warning("An error has occurred in a '%s'. Message: %s" % (self.__class__.__name__, message))
        self.deleteOperation()

class RetrievePirateOperation(OperationFSM):
    
    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender, self.__retrievedPirate)
    
    def __retrievedPirate(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Sender is not a pirate.')
            return

        self.pirate = fields
        self.demand('RetrievedPirate')
    
    def enterRetrievedPirate(self):
        pass

class RetrievePirateGuildOperation(RetrievePirateOperation):

    def enterRetrievedPirate(self):
        self.guildId = self.pirate.get('setGuildId', [0])[0]
        
        if not self.guildId:
            self.demand('Off')
            return
        
        self.air.dbInterface.queryObject(self.air.dbId, self.guildId, self.__retrievedGuild)
    
    def __retrievedGuild(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedGuildUD']:
            self.demand('Error', 'Guild ID is not linked to a guild.')
            return

        self.guild = fields
        self.members = [list(member) for member in fields['setMembers'][0]]
        self.mgr.addMemberList(self.guildId, self.members)
        self.demand('RetrievedGuild')
    
    def enterRetrievedGuild(self):
        pass
    
    def getMember(self, avId):
        for i, member in enumerate(self.members):
            if member[0] == avId:
                return i, member
        
        return 0, None
    
    def isMember(self, avId):
        for i, member in enumerate(self.members):
            if member[0] == avId:
                return True
        
        return False
    
    def updateMembers(self, members):
        self.mgr.addMemberList(self.guildId, members)
        self.air.dbInterface.updateObject(self.air.dbId, self.guildId, self.air.dclassesByName['DistributedGuildUD'], {'setMembers': [members]})
    
    def convertMember(self, member):
        avId, rank, name, _, _ = member
        online = avId in self.air.piratesFriendsManager.onlinePirates
        bandManagerId = 0
        bandId = 0
            
        return [avId, name, rank, online, bandManagerId, bandId]

class UpdatePirateExtension(object):

    def enterUpdatePirate(self, avatar, guildId, guildName, rank):
        dclass = self.air.dclassesByName['DistributedPlayerPirateUD']
        
        self.air.send(dclass.aiFormatUpdate('setGuildId', avatar, avatar, self.air.ourChannel, [guildId]))
        self.air.send(dclass.aiFormatUpdate('setGuildName', avatar, avatar, self.air.ourChannel, [guildName]))
        self.mgr.d_guildStatusUpdate(avatar, guildId, guildName, rank)
        self.demand('Off')

class CreateGuildOperation(RetrievePirateOperation, UpdatePirateExtension):
    name = 'Pirate Guild'
    rank = GUILDRANK_GM

    def enterRetrievedPirate(self):
        guildId = self.pirate.get('setGuildId', [0])[0]

        if guildId:
            self.demand('Off')
            return
        
        gold = self.pirate['setGoldInPocket'][0]
        
        if gold < OTPGlobals.GUILD_COST:
            self.demand('Off')
            return

        dclass = self.air.dclassesByName['DistributedPlayerPirateUD']
        self.air.send(dclass.aiFormatUpdate('setGoldInPocket', self.sender, self.sender, self.air.ourChannel, [gold - OTPGlobals.GUILD_COST]))

        name = self.pirate['setName'][0]
        fields = {
            'setName': [self.name],
            'setWishName': [''],
            'setOldName': [''],
            'setMembers': [[[self.sender, GUILDRANK_GM, name, 0, 0]]]
        }
        self.air.dbInterface.createObject(self.air.dbId, self.air.dclassesByName['DistributedGuildUD'], fields, self.__createdGuild)
    
    def __createdGuild(self, doId):
        if not doId:
            self.demand('Error', "Couldn't create guild object on the database.")
            return

        self.demand('UpdatePirate', self.sender, doId, self.name, GUILDRANK_GM)

class PirateOnlineOperation(RetrievePirateGuildOperation, UpdatePirateExtension):
    DELAY = 0.0
    
    def enterRetrievedGuild(self):
        self.guildName = self.guild['setName'][0]
        pirateName = self.pirate['setName'][0]
        i, self.member = self.getMember(self.sender)
        
        if not self.member:
            self.demand('Off')
            return

        if self.member[2] != pirateName:
            self.member[2] = pirateName
            self.members[i] = self.member
            self.updateMembers(self.members)

        memberList = self.mgr.getMemberIds(self.guildId)
        self.mgr.d_recvAvatarOnline(memberList, self.sender, pirateName)
        self.demand('CheckName')
    
    def enterCheckName(self):
        if not self.guild['setWishName'][0]:
            self.demand('Finish')
            return
        
        self.wishName = self.guild['setWishName'][0]
        self.mgr.air.csm.accountDB.getGuildNameStatus(self.wishName, self.__gotGuildNameStatus, 'Check')

    def __gotGuildNameStatus(self, status):
        if status == 0:
            self.demand('Finish')
            return
        
        memberList = self.mgr.getMemberIds(self.guildId)
        
        if not memberList:
            self.demand('Finish')
            return

        if status == 1:
            self.air.dbInterface.updateObject(self.air.dbId, self.guildId, self.air.dclassesByName['DistributedGuildUD'], {'setWishName': ['']})
            self.mgr.d_guildNameChange(memberList, self.wishName, status)
            self.demand('Finish')
            return

        oldName = self.guildName
        self.guildName = self.wishName
        self.air.dbInterface.updateObject(self.air.dbId, self.guildId, self.air.dclassesByName['DistributedGuildUD'], {'setWishName': [''], 'setName': [self.wishName]})
        self.mgr.d_guildNameChange(memberList, self.wishName, status)
        
        dclass = self.air.dclassesByName['DistributedPlayerPirateUD']
        
        for memberId in memberList:
            i, member = self.getMember(memberId)

            self.air.send(dclass.aiFormatUpdate('setGuildName', memberId, memberId, self.air.ourChannel, [self.guildName]))
            self.mgr.d_guildStatusUpdate(memberId, self.guildId, self.guildName, member[1])
        
        if oldName != 'Pirate Guild':
            self.demand('RemoveName', oldName)
        else:
            self.demand('Off')
    
    def enterRemoveName(self, guildName):
        self.mgr.air.csm.accountDB.getGuildNameStatus(guildName, lambda status: None, 'Remove')
        self.demand('Off')
    
    def enterFinish(self):
        self.demand('UpdatePirate', self.sender, self.guildId, self.guildName, self.member[1])

class PirateOfflineOperation(RetrievePirateOperation):
    DELAY = 0.0

    def enterRetrievedPirate(self):
        guildId = self.pirate.get('setGuildId', [0])[0]
        
        if not guildId:
            self.demand('Off')
            return
        
        memberList = self.mgr.getMemberIds(guildId)
        
        if not memberList:
            self.demand('Off')
            return
        
        self.mgr.d_recvAvatarOffline(memberList, self.sender, self.pirate['setName'][0])
        self.demand('Off')

class RemoveMemberOperation(RetrievePirateGuildOperation, UpdatePirateExtension):
    
    def enterRetrievedGuild(self):
        memberList = self.mgr.getMemberIds(self.guildId)
        i, senderMember = self.getMember(self.sender)
        
        if not senderMember:
            self.demand('Off')
            return

        j, targetMember = self.getMember(self.target)
        
        if not targetMember:
            self.demand('Off')
            return

        senderRank = senderMember[1]
        targetRank = targetMember[1]
        selfKick = self.sender == self.target
        
        if not selfKick and senderRank not in (GUILDRANK_OFFICER, GUILDRANK_GM):
            self.demand('Off')
            return
        
        if targetRank == GUILDRANK_GM and len(self.members) > 1:
            self.demand('Off')
            return
        
        if senderRank == GUILDRANK_OFFICER and not selfKick:
            senderTime = senderMember[3]
            senderKickNum = senderMember[4]
            currentTime = int(time.time())
            
            if senderTime != 0 and senderTime > currentTime and senderKickNum == 5:
                self.mgr.d_notifyGuildKicksMaxed(self.sender)
                self.demand('Off')
                return
            
            if senderTime == 0 or senderTime <= currentTime:
                senderMember[3] = currentTime + 86400 # One day
                senderMember[4] = 1
            else:
                senderMember[4] += 1

            self.members[i] = senderMember

        guildName = self.guild['setName'][0]
        name = targetMember[2]

        del self.members[j]
        self.updateMembers(self.members)
        self.mgr.d_recvMemberRemoved(memberList, self.target, self.sender, name, senderMember[2])
    
        if len(self.members) == 0 and guildName != 'Pirate Guild':
            self.demand('RemoveName', guildName)
        else:
            self.demand('Finish')
    
    def enterRemoveName(self, guildName):
        self.mgr.air.csm.accountDB.getGuildNameStatus(guildName, lambda status: None, 'Remove')
        self.demand('Finish')
    
    def enterFinish(self):
        self.demand('UpdatePirate', self.target, 0, '', 0)

class MemberListOperation(RetrievePirateGuildOperation):
    DELAY = 1.5
    
    def enterRetrievedGuild(self):
        memberInfo = [self.convertMember(member) for member in self.members]
        self.mgr.d_receiveMembers(self.sender, memberInfo)
        self.demand('Off')

class RequestInviteOperation(RetrievePirateGuildOperation):
    DELAY = 1.5
    
    def enterRetrievedGuild(self):
        if self.isMember(self.target):
            self.mgr.d_guildRejectInvite(self.sender, RejectCode.ALREADY_IN_GUILD)
            self.demand('Off')
            return
    
        _, member = self.getMember(self.sender)
        
        if (not member) or member[1] == GUILDRANK_MEMBER:
            self.demand('Off')
            return

        self.air.dbInterface.queryObject(self.air.dbId, self.target, self.__retrievedPirate)
    
    def __retrievedPirate(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Sender is not a pirate.')
            return

        if fields.get('setGuildId', [0])[0]:
            self.mgr.d_guildRejectInvite(self.sender, RejectCode.ALREADY_IN_GUILD)
            self.demand('Off')
            return
        
        self.mgr.addInvitation(self.sender, self.target, self.pirate['setName'][0], self.guildId, self.guild['setName'][0])
        self.demand('Off')

class AddMemberOperation(RetrievePirateGuildOperation, UpdatePirateExtension):
    DELAY = 1.5
    
    def enterRetrievedGuild(self):
        if self.isMember(self.target):
            self.mgr.d_guildRejectInvite(self.sender, RejectCode.ALREADY_IN_GUILD)
            self.demand('Off')
            return
        
        self.air.dbInterface.queryObject(self.air.dbId, self.target, self.__retrievedPirate)
    
    def __retrievedPirate(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Target is not a pirate.')
            return

        if fields.get('setGuildId', [0])[0]:
            self.mgr.d_guildRejectInvite(self.sender, RejectCode.ALREADY_IN_GUILD)
            self.demand('Off')
            return
        
        i, senderMember = self.getMember(self.sender)
        
        if not senderMember:
            self.demand('Off')
            return

        name = fields['setName'][0]
        member = [self.target, GUILDRANK_MEMBER, name, 0, 0]

        self.members.append(member)
        self.updateMembers(self.members)
        self.demand('UpdatePirate', self.target, self.guildId, self.guild['setName'][0], GUILDRANK_MEMBER)
        self.mgr.d_recvMemberAdded(self.mgr.getMemberIds(self.guildId), self.convertMember(member), self.sender, senderMember[2])

class SendChatOperation(RetrievePirateOperation):
    DELAY = 0.5

    def __init__(self, mgr, sender, callback, extraArgs):
        RetrievePirateOperation.__init__(self, mgr, sender)
        self.callback = callback
        self.extraArgs = extraArgs
    
    def enterRetrievedPirate(self):
        guildId = self.pirate.get('setGuildId', [0])[0]
        
        if not guildId:
            self.demand('Off')
            return

        memberList = self.mgr.getMemberIds(guildId)
        
        if not memberList:
            self.demand('Off')
            return
        
        self.extraArgs.insert(1, self.pirate['setName'][0])
        self.callback(memberList, *self.extraArgs)
        self.demand('Off')

class ChangeRankOperation(RetrievePirateGuildOperation):

    def __init__(self, mgr, sender, target, rank):
        RetrievePirateGuildOperation.__init__(self, mgr, sender, target)
        self.rank = rank

    def enterRetrievedGuild(self):
        guildName = self.guild['setName'][0]
        memberList = self.mgr.getMemberIds(self.guildId)
        i, senderMember = self.getMember(self.sender)
        
        if not senderMember:
            self.demand('Off')
            return
        
        senderRank = senderMember[1]
        
        if senderRank != GUILDRANK_GM:
            self.demand('Off')
            return

        j, targetMember = self.getMember(self.target)
        
        if not targetMember:
            self.demand('Off')
            return
        
        targetRank = targetMember[1]
        
        if self.rank == targetRank:
            self.demand('Off')
            return

        senderName = senderMember[2]
        avatarName = targetMember[2]
        
        if self.rank == GUILDRANK_GM:
            promote = True
        elif self.rank == GUILDRANK_VETERAN and targetRank == GUILDRANK_MEMBER:
            promote = True
        elif self.rank == GUILDRANK_OFFICER and targetRank in (GUILDRANK_MEMBER, GUILDRANK_VETERAN):
            promote = True
        else:
            promote = False

        self.members[j][1] = self.rank
        self.mgr.d_guildStatusUpdate(self.target, self.guildId, guildName, self.rank)
        self.mgr.d_recvMemberUpdateRank(memberList, self.target, self.sender, avatarName, senderName, self.rank, promote)
        
        if self.rank == GUILDRANK_GM:
            self.members[i][1] = GUILDRANK_OFFICER
            self.mgr.d_guildStatusUpdate(self.sender, self.guildId, guildName, GUILDRANK_OFFICER)
            self.mgr.d_recvMemberUpdateRank(memberList, self.sender, self.target, senderName, avatarName, GUILDRANK_OFFICER, False)
        
        self.updateMembers(self.members)
        self.demand('Off')

class SendNameOperation(RetrievePirateGuildOperation):

    def __init__(self, mgr, sender, name):
        RetrievePirateGuildOperation.__init__(self, mgr, sender)
        self.name = name
    
    def enterRetrievedGuild(self):
        i, member = self.getMember(self.sender)
        
        if (not member) or member[1] != GUILDRANK_GM:
            self.mgr.d_recvNameRequest([self.sender], 0)
            self.demand('Off')
            return
        
        if self.guild['setWishName'][0]:
            self.mgr.d_recvNameRequest([self.sender], 1)
            self.demand('Off')
            return
            
        self.mgr.air.csm.accountDB.getGuildNameStatus(self.name, self.__gotGuildNameStatus, 'New')
    
    def __gotGuildNameStatus(self, status):
        if status == 3:
            self.mgr.d_recvNameRequest([self.sender], 2)
            self.demand('Off')
            return
        
        self.air.dbInterface.updateObject(self.air.dbId, self.guildId, self.air.dclassesByName['DistributedGuildUD'], {'setWishName': [self.name], 'setOldName': [self.guild['setName'][0]]})
        self.mgr.d_recvNameRequest([self.sender], 3)
        self.demand('Off')
        
class GuildManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("GuildManagerUD")
    
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.operations = {}
        self.invites = {}
        self.memberListCache = {}
        self.accept('pirateOnline', self.pirateOnline)
        self.accept('goingOffline', self.goingOffline)
    
    def addMemberList(self, guildId, memberList):
        self.memberListCache[guildId] = memberList
    
    def getMemberList(self, guildId):
        return self.memberListCache.get(guildId)
    
    def getMemberIds(self, guildId):
        memberList = self.getMemberList(guildId)
        
        if memberList:
            return [member[0] for member in memberList if member[0] in self.air.piratesFriendsManager.onlinePirates]
    
    def hasOperation(self, avId):
        return avId in self.operations

    def createGuild(self):
        avId = self.air.getAvatarIdFromSender()

        if avId not in self.operations:
            CreateGuildOperation(self, avId).demand('Start')
    
    def d_guildStatusUpdate(self, avId, guildId, guildName, guildRank):
        self.sendUpdateToAvatarId(avId, 'guildStatusUpdate', [guildId, guildName, guildRank])
    
    def d_notifyGuildKicksMaxed(self, avId):
        self.sendUpdateToAvatarId(avId, 'notifyGuildKicksMaxed', [])
    
    def d_receiveMembers(self, avId, members):
        self.sendUpdateToAvatarId(avId, 'receiveMembers', [members])
    
    def d_guildRejectInvite(self, avId, reason):
        self.sendUpdateToAvatarId(avId, 'guildRejectInvite', [reason])
    
    def d_invitationFrom(self, avId, fromId, fromName, guildId, guildName):
        self.sendUpdateToAvatarId(avId, 'invitationFrom', [fromId, fromName, guildId, guildName])
    
    def d_recvNameRequest(self, avIds, code):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvNameRequest', [code])
    
    def d_recvChat(self, avIds, senderId, senderName, message):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvChat', [senderId, senderName, message])
    
    def d_recvSC(self, avIds, senderId, senderName, msgIndex):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvSC', [senderId, senderName, msgIndex])
    
    def d_recvSCQuest(self, avIds, senderId, senderName, questInt, msgType, taskNum):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvSCQuest', [senderId, senderName, questInt, msgType, taskNum])
    
    def d_recvAvatarOnline(self, avIds, senderId, senderName):
        for avId in avIds:
            if avId != senderId:
                self.sendUpdateToAvatarId(avId, 'recvAvatarOnline', [senderId, senderName])
    
    def d_recvAvatarOffline(self, avIds, senderId, senderName):
        for avId in avIds:
            if avId != senderId:
                self.sendUpdateToAvatarId(avId, 'recvAvatarOffline', [senderId, senderName])
    
    def d_recvMemberRemoved(self, avIds, avatarId, senderId, avatarName, senderName):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvMemberRemoved', [avatarId, senderId, avatarName, senderName])
    
    def d_recvMemberAdded(self, avIds, memberInfo, inviterId, inviterName):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvMemberAdded', [memberInfo, inviterId, inviterName])
    
    def d_recvMemberUpdateRank(self, avIds, avatarId, senderId, avatarName, senderName, rank, promote):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'recvMemberUpdateRank', [avatarId, senderId, avatarName, senderName, rank, promote])

    def d_guildNameChange(self, avIds, guildName, code):
        for avId in avIds:
            self.sendUpdateToAvatarId(avId, 'guildNameChange', [guildName, code])
    
    def pirateOnline(self, doId):
        PirateOnlineOperation(self, doId).demand('Start')
    
    def goingOffline(self, doId):
        self.popInvite(doId)
        PirateOfflineOperation(self, doId).demand('Start')
    
    def removeMember(self, targetId):
        avId = self.air.getAvatarIdFromSender()
        
        if targetId and avId not in self.operations:
            RemoveMemberOperation(self, avId, targetId).demand('Start')
    
    def changeRank(self, targetId, targetRank):
        if targetRank not in (GUILDRANK_GM, GUILDRANK_MEMBER, GUILDRANK_OFFICER, GUILDRANK_VETERAN):
            return
        
        avId = self.air.getAvatarIdFromSender()
        
        if targetId == avId:
            return
        
        if targetId and avId not in self.operations:
            ChangeRankOperation(self, avId, targetId, targetRank).demand('Start')
    
    def popInvite(self, avId):
        return self.invites.pop(avId, None)
    
    def requestMembers(self):
        avId = self.air.getAvatarIdFromSender()

        if avId not in self.operations:
            MemberListOperation(self, avId).demand('Start')
    
    def isInInvite(self, avId):
        return avId in self.invites.keys() or avId in self.invites.values()
    
    def requestInvite(self, targetId):
        avId = self.air.getAvatarIdFromSender()
        
        if targetId == avId or self.isInInvite(targetId):
            self.d_guildRejectInvite(avId, RejectCode.BUSY)
            return
        
        if targetId not in self.air.piratesFriendsManager.onlinePirates:
            self.d_guildRejectInvite(avId, RejectCode.INVITEE_NOT_ONLINE)
            return
        
        if avId not in self.operations:
            RequestInviteOperation(self, avId, targetId).demand('Start')
    
    def acceptInvite(self):
        avId = self.air.getAvatarIdFromSender()
        senderId = self.popInvite(avId)
        
        if not senderId:
            return
        
        if avId not in self.operations:
            AddMemberOperation(self, senderId, avId).demand('Start')
    
    def declineInvite(self):
        avId = self.air.getAvatarIdFromSender()
        senderId = self.popInvite(avId)
        
        if senderId:
            self.d_guildRejectInvite(senderId, RejectCode.NO_GUILD)

    def sendNameRequest(self, name):
        if not name:
            return

        avId = self.air.getAvatarIdFromSender()
        
        if avId not in self.operations:
            SendNameOperation(self, avId, name).demand('Start')

    def addInvitation(self, sender, target, pirateName, guildId, guildName):
        self.invites[target] = sender
        self.d_invitationFrom(target, sender, pirateName, guildId, guildName)
    
    def __addChatOperation(self, callback, extraArgs):
        sender = self.air.getAvatarIdFromSender()
        
        if sender not in self.operations:
            extraArgs.insert(0, sender)
            SendChatOperation(self, sender, callback, extraArgs).demand('Start')
    
    def sendChat(self, message):
        self.__addChatOperation(self.d_recvChat, [message])
    
    def sendSC(self, msgIndex):
        self.__addChatOperation(self.d_recvSC, [msgIndex])
    
    def sendSCQuest(self, questInt, msgType, taskNum):
        self.__addChatOperation(self.d_recvSCQuest, [questInt, msgType, taskNum])