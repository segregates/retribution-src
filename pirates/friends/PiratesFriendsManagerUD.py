from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.fsm.FSM import FSM
from pirates.reputation import ReputationGlobals
from pirates.uberdog import InventoryInit
from pirates.uberdog.UberDogGlobals import InventoryType
import time

BasicCache = {}
DetailedCache = {}

def deleteFromBasicCache(doId):
    if doId in BasicCache:
        del BasicCache[doId]

# -- FSMS --
class OperationFSM(FSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None):
        FSM.__init__(self, 'OperationFSM-%s' % senderAvId)
        self.mgr = mgr
        self.air = air
        self.sender = senderAvId
        self.result = None
        self.target = targetAvId
        self.callback = callback
        self.deleted = False
    
    def fsmName(self, name):
        return 'OperationFSM-%s-%s' % (id(self), name)
    
    def deleteOperation(self):
        if not self.deleted:
            taskMgr.doMethodLater(0.25, self.__deleteOperation, self.fsmName('deleteOperation'))
            self.deleted = True
    
    def __deleteOperation(self, task):
        if self.sender in self.mgr.operations:
            del self.mgr.operations[self.sender]

    def enterOff(self):
        if self.callback:
            if self.result is not None:
                self.callback(self.sender, self.result)
            else:
                self.callback()
        
        self.deleteOperation()

    def enterError(self, message=None):
        self.mgr.notify.warning("An error has occurred in a '%s'. Message: %s" % (self.__class__.__name__, message))
        self.deleteOperation()

class GetAvatarOperation(OperationFSM):

    def getRequiredAccumulators(self):
        return [InventoryType.OverallRep, InventoryType.CannonRep, InventoryType.SailingRep, InventoryType.CutlassRep,
                InventoryType.PistolRep, InventoryType.DollRep, InventoryType.DaggerRep, InventoryType.GrenadeRep,
                InventoryType.WandRep, InventoryType.PotionsRep, InventoryType.FishingRep]
    
    def getLevelFromAccumulator(self, accumulators, accumulator):
        return ReputationGlobals.getLevelFromTotalReputation(accumulator, accumulators.get(accumulator, 0))[0]
    
    def getLevelsFromAccumulators(self, accumulators):
        return [self.getLevelFromAccumulator(accumulators, accumulator) for accumulator in self.getRequiredAccumulators()]
    
    def getPirateFields(self):
        return ('setDNAString', 'setFounder', 'setHp', 'setMaxHp', 'setMojo', 'setMaxMojo', 'setInventoryId',
            'setDefaultShard', 'setReturnLocation', 'setGuildId', 'setGuildName', 'setChatType', 'setMutedUntil')

    def getPirateDefaults(self):
        return ('', False, 0, 0, 0, 0, 0, 0, '', 0, '', 0, 0)
    
    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.target, self.handleRetrieve)
    
    def handleRetrieve(self, dclass, fields):
        DetailedCache[self.target] = {'expire': time.time() + 5}

        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Distributed Class was not a Pirate.')
            return

        dna, founder, hp, maxHp, mojo, maxMojo, inventoryId, shardId, returnLocation, guildId, guildName, chat, mutedUntil = [fields.get(field, [self.getPirateDefaults()[i]])[0] for i, field in enumerate(self.getPirateFields())]
        showGoTo = self.target in self.mgr.onlinePirates
        siege = False
        profileIcon = 0
        
        if mutedUntil == 1 or mutedUntil > int(time.time()):
            chat = 2
        
        avatar = [dna, guildId, guildName, founder, hp, maxHp, mojo, maxMojo, shardId, showGoTo, chat, returnLocation, siege, profileIcon]

        DetailedCache[self.target]['avatar'] = avatar
        self.mgr.d_receiveAvatarInfo(self.sender, *avatar)
        self.air.dbInterface.queryObject(self.air.dbId, inventoryId, self.handleRetrieveInventory)

    def handleRetrieveInventory(self, dclass, fields):
        if dclass != self.air.dclassesByName['PirateInventoryUD']:
            self.demand('Error', 'Distributed Class was not an Inventory.')
            return
        if fields.get('setInventoryVersion', [None])[0] != InventoryInit.UberDogRevision:
            self.demand('Error', 'Inventory is in the wrong format!')
            return
        if fields.get('setOwnerId', [None])[0] != self.target:
            self.demand('Error', 'Inventory belongs to someone else!')
            return
        
        accumulators = dict(fields['setAccumulators'][0])
        levels = self.getLevelsFromAccumulators(accumulators)

        DetailedCache[self.target]['levels'] = levels
        self.mgr.d_receiveAvatarSkillLevels(self.sender, *levels)
        self.demand('Off')

# -- Friends list --
class FriendsListOperation(OperationFSM):

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender, self.handleRetrieveSender)

    def handleRetrieveSender(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Distributed Class was not a Pirate.')
            return

        self.demand('Retrieved', fields['setName'][0], fields['setFriendsList'][0])

    def enterRetrieved(self, name, friendsList):
        self.name = name
        self.friendsList = friendsList

        if len(self.friendsList) <= 0:
            self.result = [[], name]
            self.demand('Off')
            return

        self.friendIndex = -1
        self.realFriendsList = []
        self.queryNext()

    def addFriend(self, dclass, fields):
        friendId = self.friendsList[self.friendIndex]

        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Friend was not a Pirate')
            BasicCache[friendId] = {'expire': time.time() + 30}
            return

        info = [friendId, fields['setName'][0], fields['setHp'][0], fields['setMaxHp'][0], friendId in self.mgr.onlinePirates]

        BasicCache[friendId] = {'expire': time.time() + 30, 'info': info}
        self.addFriendInfo(info)
    
    def addFriendInfo(self, info):
        self.realFriendsList.append(info)
        
        if len(self.realFriendsList) >= len(self.friendsList):
            self.result = [self.realFriendsList, self.name]
            self.demand('Off')
            return

        self.queryNext()
    
    def queryNext(self):
        self.friendIndex += 1
        next = self.friendsList[self.friendIndex]
        
        if next in BasicCache:
            cache = BasicCache[next]

            if cache['expire'] >= time.time():
                if 'info' not in cache:
                    self.queryNext()
                else:
                    self.addFriendInfo(cache['info'])

                return
        
        self.air.dbInterface.queryObject(self.air.dbId, next, self.addFriend)

# -- Remove Friends --
class RemoveFriendOperation(OperationFSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None, alert=False):
        OperationFSM.__init__(self, mgr, air, senderAvId, targetAvId, callback)
        self.alert = alert

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender, self.handleRetrieve)

    def handleRetrieve(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Error', 'Distributed Class was not a Pirate.')
            return

        self.demand('Retrieved', fields['setFriendsList'][0], fields['setTrueFriends'][0])

    def enterRetrieved(self, friendsList, trueFriendsList):
        dclass = self.air.dclassesByName['DistributedPlayerPirateUD']

        if self.target in friendsList:
            friendsList.remove(self.target)
            self.air.send(dclass.aiFormatUpdate('setFriendsList', self.sender, self.sender, self.air.ourChannel, [friendsList]))
        if self.target in trueFriendsList:
            trueFriendsList.remove(self.target)
            self.air.send(dclass.aiFormatUpdate('setTrueFriends', self.sender, self.sender, self.air.ourChannel, [trueFriendsList]))
        if self.alert and self.sender in self.mgr.onlinePirates:
            self.air.send(dclass.aiFormatUpdate('friendsNotify', self.sender, self.sender, self.air.ourChannel, [self.target, 1]))

        deleteFromBasicCache(self.target)
        self.mgr.requestFriendsListFor(self.sender)
        self.demand('Off')

# -- FriendsManager --

class PiratesFriendsManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('PiratesFriendsManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.onlinePirates = []
        self.tpRequests = {}
        self.whisperRequests = {}
        self.operations = {}
        self.delayTime = 1.0
        self.accept('goingOffline', self.goingOffline)

    def checkWhisperRequest(self, fromId):
        currentTime = time.time()
        allow = fromId not in self.whisperRequests or self.whisperRequests[fromId] <= currentTime

        self.whisperRequests[fromId] = currentTime + self.delayTime
        return allow
    
    def addOperation(self, operation):
        if operation.sender in self.operations:
            return

        self.operations[operation.sender] = operation
        operation.demand('Start')
    
    # dna, guildId, guildName, founder, hp, maxHp, voodoo, maxVoodoo, shardId, showGoTo, chat, islandName, locationName, siege, profileIcon
    def d_receiveAvatarInfo(self, avId, *args):
        self.sendUpdateToAvatarId(avId, 'receiveAvatarInfo', args)
    
    # see getRequiredAccumulators
    def d_receiveAvatarSkillLevels(self, avId, *args):
        self.sendUpdateToAvatarId(avId, 'receiveAvatarSkillLevels', args)
    
    # guildState, crewState, friendState
    def d_receiveAvatarShipInfo(self, avId, *args):
        self.sendUpdateToAvatarId(avId, 'receiveAvatarShipInfo', args)
    
    # -- Friends list --
    def requestFriendsList(self):
        self.requestFriendsListFor(self.air.getAvatarIdFromSender())
    
    def requestFriendsListFor(self, avId):
        if avId not in self.operations:
            self.addOperation(FriendsListOperation(self, self.air, avId, callback=self.sendFriendsList))

    def sendFriendsList(self, sender, extraArgs):
        friendsList, name = extraArgs
        self.sendUpdateToAvatarId(sender, 'friendList', [friendsList])

        if sender not in self.onlinePirates:
            self.pirateOnline(sender, name, friendsList)

    # -- Remove Friend --
    def removeFriend(self, friendId):
        avId = self.air.getAvatarIdFromSender()

        if avId in self.operations or friendId in self.operations:
            return

        self.addOperation(RemoveFriendOperation(self, self.air, avId, friendId))
        self.addOperation(RemoveFriendOperation(self, self.air, friendId, avId, alert=True))

    # -- Avatar Info --
    def getAvatarDetails(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        
        if avId in DetailedCache:
            cache = DetailedCache[avId]
            
            if cache['expire'] >= time.time() and 'avatar' in cache and 'levels' in cache:
                self.d_receiveAvatarInfo(senderId, *cache['avatar'])
                self.d_receiveAvatarSkillLevels(senderId, *cache['levels'])
                return

        if avId not in self.operations:
            self.addOperation(GetAvatarOperation(self, self.air, senderId, avId))
    
    # -- Pirate Online/Offline --
    def pirateOnline(self, doId, name, friendsList):
        if doId in self.onlinePirates:
            return

        messenger.send('pirateOnline', [doId])
        self.onlinePirates.append(doId)
        deleteFromBasicCache(doId)
        
        for friend in friendsList:
            friend = friend[0]

            if friend in self.onlinePirates:
                self.sendUpdateToAvatarId(friend, 'friendOnline', [doId, name])
                self.requestFriendsListFor(friend)

    def goingOffline(self, doId):
        if doId not in self.onlinePirates:
            return
        
        self.onlinePirates.remove(doId)
        deleteFromBasicCache(doId)

        def handlePirate(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
                return

            friendsList = fields['setFriendsList'][0]
            name = fields['setName'][0]

            for friend in friendsList:
                if friend in self.onlinePirates:
                    self.sendUpdateToAvatarId(friend, 'friendOffline', [doId, name])
                    self.requestFriendsListFor(friend)

        self.air.dbInterface.queryObject(self.air.dbId, doId, handlePirate)

    # -- Teleport and Whispers --
    def routeTeleportQuery(self, toId):
        fromId = self.air.getAvatarIdFromSender()

        if fromId in self.tpRequests.values():
            return

        self.tpRequests[fromId] = toId
        self.sendUpdateToAvatarId(toId, 'teleportQuery', [fromId])
        taskMgr.doMethodLater(5, self.giveUpTeleportQuery, 'tp-query-timeout-%d' % fromId, extraArgs=[fromId, toId])

    def giveUpTeleportQuery(self, fromId, toId):
        # The client didn't respond to the query within the set time,
        # So we will tell the query sender that the pirate is unavailable.
        if fromId in self.tpRequests:
            del self.tpRequests[fromId]
            self.sendUpdateToAvatarId(fromId, 'setTeleportResponse', [toId, 0, 0, 0, 0])
            self.notify.warning('Teleport request that was sent by %d to %d timed out.' % (fromId, toId))

    def teleportResponse(self, toId, available, shardId, hoodId, zoneId):
        # Here is where the toId and fromId swap (because we are now sending it back)
        fromId = self.air.getAvatarIdFromSender()

        # We got the query response, so no need to give up!
        if taskMgr.hasTaskNamed('tp-query-timeout-%d' % toId):
            taskMgr.remove('tp-query-timeout-%d' % toId)

        if toId not in self.tpRequests:
            return
        if self.tpRequests.get(toId) != fromId:
            self.air.writeServerEvent('suspicious', avId=fromId, message='Pirate tried to send teleportResponse for a query that isn\'t theirs!')
            return

        self.sendUpdateToAvatarId(toId, 'setTeleportResponse', [fromId, available, shardId, hoodId, zoneId])
        del self.tpRequests[toId]

    def whisperSCTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        
        if self.checkWhisperRequest(fromId):
            self.sendUpdateToAvatarId(toId, 'setWhisperSCFrom', [fromId, msgIndex])

    def whisperSCCustomTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        
        if self.checkWhisperRequest(fromId):
            self.sendUpdateToAvatarId(toId, 'setWhisperSCCustomFrom', [fromId, msgIndex])

    def whisperSCEmoteTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        
        if self.checkWhisperRequest(fromId):
            self.sendUpdateToAvatarId(toId, 'setWhisperSCEmoteFrom', [fromId, msgIndex])

    def sendTalkWhisper(self, toId, message):
        fromId = self.air.getAvatarIdFromSender()
        
        if not self.checkWhisperRequest(fromId):
            return

        self.sendUpdateToAvatarId(toId, 'receiveTalkWhisper', [fromId, message])
        self.air.writeServerEvent('whisper-said', fromId=fromId, toId=toId, message=message)

    # -- Routes --
    def teleportGiveup(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setTeleportGiveup', [requester])
