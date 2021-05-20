from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.PotentialAvatar import PotentialAvatar
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.HumanDNA import HumanDNA
import hashlib, hmac, sys, os

try:
    import challenge
except ImportError:
    class challenge:
        @staticmethod
        def solve(*args):
            return 'There is a simple truth to be learned here'

def flip(a):
    # This is SIMPLE OBFUSCATION not ENCRYPTION
    return ''.join(chr(~ord(x) & 0xFF) for x in a)

class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')

    def performLogin(self, doneEvent):
        self.doneEvent = doneEvent
        self.loginCookie = os.environ.get('POR_PLAYCOOKIE', 'dev')
        self.sendUpdate('requestChallenge', [])

    def challenge(self, data):
        key = config.GetString('csmud-secret', 'dev')
        key = flip(key)

        resp = challenge.solve(key, self.loginCookie, data)

        sig = hmac.new(key, self.loginCookie, hashlib.sha512).digest()
        self.sendUpdate('login', [resp, self.loginCookie, sig])

    def acceptLogin(self, username):
        self.username = username
        messenger.send(self.doneEvent, [{'mode': 'success'}])

    def requestAvatars(self):
        self.sendUpdate('requestAvatars')
    
    def requestDeletedAvatars(self):
        self.sendUpdate('requestDeletedAvatars')

    def setAvatars(self, avatars, adminAccess):
        avList = [PiratesGlobals.AvatarSlotAvailable] * 6

        for avNum, avName, avDNA, avPosition, nameState, wishName in avatars:
            if avPosition > len(avList):
                continue

            wishState = 'OPEN' if int(nameState == 1) else 'CLOSED'

            if nameState == 2: # PENDING
                wishState = 'REQUESTED'
            elif nameState == 3: # APPROVED
                wishState = 'APPROVED'
            elif nameState == 4: # REJECTED
                wishState = 'DENIED'

            dna = HumanDNA()
            dna.makeFromNetString(avDNA)
            avList[avPosition] = PotentialAvatar(avNum, avName, dna, avPosition, wishState=wishState, wishName=wishName)

        self.cr.handleAvatarsList(avList)
        base.setAdminAccess(adminAccess)
        self.requestDeletedAvatars()
    
    def setDeletedAvatars(self, avatars):
        avList = []
        
        for avatar in avatars:
            dna = HumanDNA()
            dna.makeFromNetString(avatar[3])
            
            avList.append(PotentialAvatar(avatar[0], avatar[2], dna, avatar[1]))

        self.cr.handleDeletedAvatarsList(avList)

    def sendCreateAvatar(self, avDNA, index, allegiance, name):
        self.sendUpdate('createAvatar', [avDNA.makeNetString(), index, allegiance, name])

    def createAvatarResp(self, avId):
        messenger.send('createdNewAvatar', [avId])

    def sendChooseAvatar(self, avId, index):
        self.sendUpdate('chooseAvatar', [avId, index])

    def avatarResponse(self, avId, avDetails):
        print 'Got avatarResponse: avId: %s, avDetails: %s' % (avId, avDetails)

    def sendDeleteAvatar(self, avatarId):
        self.sendUpdate('deleteAvatar', [avatarId])

    def avDeleted(self, avatarId):
        messenger.send('avDeleted', [avatarId])

    def sendAcknowledgeName(self, avId):
        self.sendUpdate('acknowledgeName', [avId])

    def sendNewName(self, avId, name):
        self.sendUpdate('newName', [avId, name])

    def newNameResp(self):
        messenger.send('newNameResp')
