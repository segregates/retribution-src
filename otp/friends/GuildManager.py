from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPLocalizer, OTPGlobals

GUILDRANK_VETERAN = 4
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

class GuildManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('GuildManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.id2Name = {}
        self.id2BandId = {}
        self.id2Rank = {}
        self.id2Online = {}

    def memberList(self):
        self.sendUpdate('requestMembers', [])

    def createGuild(self):
        messenger.send('declineGuildInvitation')
        self.sendUpdate('createGuild', [])

    def sendNameRequest(self, newName):
        self.sendUpdate('sendNameRequest', [newName])

    def removeMember(self, avatarId):
        self.sendUpdate('removeMember', [avatarId])

    def changeRank(self, avatarId, rank):
        self.sendUpdate('changeRank', [avatarId, rank])

    def requestLeaderboardTopTen(self):
        self.sendUpdate('requestLeaderboardTopTen', [])

    def sendRequestInvite(self, avatarId):
        self.sendUpdate('requestInvite', [avatarId])

    def sendAcceptInvite(self):
        self.sendUpdate('acceptInvite', [])

    def sendDeclineInvite(self):
        self.sendUpdate('declineInvite', [])

    def sendTalk(self, msgText, chatFlags = 0):
        self.sendUpdate('sendChat', [msgText])

    def sendSC(self, msgIndex):
        self.sendUpdate('sendSC', [msgIndex])

    def sendSCQuest(self, questInt, msgType, taskNum):
        self.sendUpdate('sendSCQuest', [questInt, msgType, taskNum])

    def sendTokenRequest(self):
        self.sendUpdate('sendTokenRequest', [])

    def sendTokenForJoinRequest(self, token):
        name = base.localAvatar.getName()
        self.sendUpdate('sendTokenForJoinRequest', [token, name])
    
    def recvNameRequest(self, code):
        if code == 3:
            base.localAvatar.guildNameRequest()
        else:
            base.localAvatar.guildNameReject(code)

    def isInGuild(self, avId):
        return avId in self.id2Name

    def getRank(self, avId):
        return self.id2Rank.get(avId)

    def getBandId(self, avId):
        return self.id2BandId.get(avId)

    def getOptionsFor(self, avId):
        if self.isInGuild(avId):
            myRank = self.id2Rank.get(localAvatar.doId, localAvatar.getGuildRank())
            hisRank = self.id2Rank[avId]

            if myRank == GUILDRANK_GM:
                return (True, True, True) # Promote, demote, kick
            if myRank > GUILDRANK_MEMBER and myRank != GUILDRANK_VETERAN and (hisRank <= GUILDRANK_MEMBER or hisRank == GUILDRANK_VETERAN):
                return (False, False, True)
        
        return (False, False, False)

    def updateTokenRValue(self, tokenString, rValue):
        rValue = int(rValue)
        self.sendUpdate('sendTokenRValue', [tokenString, rValue])
        if rValue == -1:
            base.localAvatar.guiMgr.guildPage.receivePermTokenValue(tokenString)

    def requestPermToken(self):
        self.sendUpdate('sendPermToken', [])

    def requestNonPermTokenCount(self):
        self.sendUpdate('sendNonPermTokenCount', [])

    def requestClearTokens(self, type):
        self.sendUpdate('sendClearTokens', [type])

    def receiveMembers(self, members):
        self.id2Name = {}
        self.id2Rank = {}
        self.id2BandId = {}

        for guy in members:
            id, name, rank, isOnline, bandMgrId, bandId = guy
            self.id2Name[id] = name
            self.id2Rank[id] = rank
            self.id2Online[id] = isOnline
            self.id2BandId[id] = (bandMgrId, bandId)

        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.guildPage.receiveMembers(members)

        messenger.send('guildMemberUpdated', sentArgs=[localAvatar.doId])

    def clearMembers(self):
        self.receiveMembers([])

    def guildStatusUpdate(self, guildId, guildName, guildRank):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guildStatusUpdate(guildId, guildName, guildRank)
        self.memberList()

    def guildNameChange(self, guildName, changeStatus):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guildNameChange(guildName, changeStatus)

    def invitationFrom(self, avatarId, avatarName, guildId, guildName):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.handleGuildInvitation(avatarId, avatarName, guildId, guildName)

    def leaderboardTopTen(self, stuff):
        base.localAvatar.guiMgr.handleTopTen(stuff)

    def guildRejectInvite(self, reason):
        messenger.send(OTPGlobals.GuildRejectInviteEvent, [reason])

    def rejectInvite(self, avatarId, reason):
        pass

    def recvChat(self, senderId, senderName, chat, garble=True):
        if not base.localAvatar.isIgnored(senderId):
            if base.whiteList and garble:
                chat = base.whiteList.processThroughAll(chat, base.chatGarbler)

            base.talkAssistant.receiveGuildTalk(senderId, senderName, chat)
    
    def recvSC(self, senderId, senderName, msgIndex):
        self.recvChat(senderId, senderName, OTPLocalizer.SpeedChatStaticText[msgIndex], False)

    def recvSCQuest(self, senderId, senderName, questInt, msgType, taskNum):
        message = base.talkAssistant.SCDecoder.decodeSCQuestMsgInt(questInt, msgType, taskNum)
        self.recvChat(senderId, senderName, message, False)

    def recvAvatarOnline(self, avatarId, avatarName):
        self.id2Online[avatarId] = True

        if not base.localAvatar.isIgnored(avatarId):
            base.talkAssistant.receiveGuildUpdate(avatarId, avatarName, True)

        messenger.send('guildMemberOnlineStatus', [avatarId, 1])

    def recvAvatarOffline(self, avatarId, avatarName):
        self.id2BandId[avatarId] = (0, 0)
        self.id2Online[avatarId] = False

        if not base.localAvatar.isIgnored(avatarId):
            base.talkAssistant.receiveGuildUpdate(avatarId, avatarName, False)
            
        messenger.send('guildMemberOnlineStatus', [avatarId, 0])

    def recvMemberAdded(self, memberInfo, inviterId, inviterName):
        avatarId, avatarName, rank, isOnline, bandManagerId, bandId = memberInfo
        
        if avatarId == localAvatar.doId:
            displayName = OTPLocalizer.LowerYou
        else:
            displayName = avatarName

        if inviterId == localAvatar.getDoId():
            base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendInvitedP, inviterId, OTPLocalizer.You, avatarId, displayName)
        elif inviterId:
            base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendInvited, inviterId, inviterName, avatarId, displayName)

        self.id2Name[avatarId] = avatarName
        self.id2Rank[avatarId] = rank
        self.id2BandId[avatarId] = (bandManagerId, bandId)
        self.id2Online[avatarId] = isOnline
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.guildPage.addMember(memberInfo)
        messenger.send('guildMemberUpdated', sentArgs=[avatarId])
        self.memberList()

    def recvMemberRemoved(self, avatarId, senderId, avatarName, senderName):
        if avatarId == localAvatar.doId:
            displayName = OTPLocalizer.LowerYou
        else:
            displayName = avatarName

        if avatarId == localAvatar.doId and senderId == localAvatar.doId:
            base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendKickedOutSelf, 0, '', 0, '')
        elif senderId == localAvatar.getDoId():
            base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendKickedOutP, senderId, OTPLocalizer.You, avatarId, displayName)
        elif senderId == avatarId:
            base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendsNoMore, senderId, senderName, 0, '')
        elif senderId:
            base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendKickedOut, senderId, senderName, avatarId, displayName)

        messenger.send('kickedFromGuild-%s' % avatarId)

        if avatarId in self.id2Name:
            del self.id2Name[avatarId]
        
        if avatarId in self.id2Rank:
            del self.id2Rank[avatarId]
        
        if avatarId in self.id2BandId:
            del self.id2BandId[avatarId]
        
        if avatarId in self.id2Online:
            del self.id2Online[avatarId]

        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.guildPage.removeMember(avatarId)

        messenger.send('guildMemberUpdated', sentArgs=[avatarId])
        self.memberList()

    def recvMemberUpdateRank(self, avatarId, senderId, avatarName, senderName, rank, promote):
        if avatarId == localAvatar.getDoId():
            avatarName = OTPLocalizer.You
        elif senderId == localAvatar.getDoId():
            senderName = OTPLocalizer.You
        
        if promote:
            if rank == GUILDRANK_GM:
                if senderId == localAvatar.getDoId():
                    message = OTPLocalizer.GuildInviterFriendPromotedGMP
                else:
                    message = OTPLocalizer.GuildInviterFriendPromotedGM
            elif senderId == localAvatar.getDoId():
                message = OTPLocalizer.GuildInviterFriendPromotedP
            else:
                message = OTPLocalizer.GuildInviterFriendPromoted
        else:
            if self.id2Rank.get(avatarId) == GUILDRANK_GM:
                if senderId == localAvatar.getDoId():
                    message = OTPLocalizer.GuildInviterFriendDemotedGMP
                else:
                    message = OTPLocalizer.GuildInviterFriendDemotedGM
            elif senderId == localAvatar.getDoId():
                message = OTPLocalizer.GuildInviterFriendDemotedP
            else:
                message = OTPLocalizer.GuildInviterFriendDemoted
       
        base.talkAssistant.receiveGuildUpdateMessage(message, senderId, senderName, avatarId, avatarName, [OTPLocalizer.GuildRankNames[rank]])
        self.id2Rank[avatarId] = rank
        
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.updateGuildMemberRank(avatarId, rank)

        messenger.send('guildMemberUpdated', sentArgs=[avatarId])
        self.memberList()

    def recvMemberUpdateBandId(self, avatarId, bandManagerId, bandId):
        self.id2BandId[avatarId] = (bandManagerId, bandId)
        messenger.send('guildMemberUpdated', sentArgs=[avatarId])

    def recvTokenInviteValue(self, tokenValue, preExistPerm):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.displayInviteGuild(tokenValue, preExistPerm)

    def recvTokenRedeemMessage(self, guildName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            if guildName == '***ERROR - GUILD CODE INVALID***':
                base.localAvatar.guiMgr.guildPage.displayRedeemErrorMessage(OTPLocalizer.GuildRedeemErrorInvalidToken)
            elif guildName == '***ERROR - GUILD FULL***':
                base.localAvatar.guiMgr.guildPage.displayRedeemErrorMessage(OTPLocalizer.GuildRedeemErrorGuildFull)
            else:
                base.localAvatar.guiMgr.guildPage.displayRedeemConfirmMessage(guildName)

    def recvPermToken(self, token):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            if token == '0':
                base.localAvatar.guiMgr.guildPage.receivePermTokenValue(None)
            else:
                base.localAvatar.guiMgr.guildPage.receivePermTokenValue(token)

    def recvNonPermTokenCount(self, tCount):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.receiveNonPermTokenCount(tCount)
    
    def notifyGuildKicksMaxed(self):
        base.localAvatar.guiMgr.createWarning(OTPLocalizer.GuildKicksMaxed, (1, 0.1, 0.1, 1))
