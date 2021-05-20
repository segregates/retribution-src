from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from otp.otpbase import OTPGlobals
import time

class ChatAgentAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.timestampDict = {}

    def checkTimestamp(self, avId, delay=0.5):
        if avId in self.timestampDict and self.timestampDict[avId] > time.time():
            return False
        
        self.timestampDict[avId] = time.time() + delay
        return True
    
    def chatMessage(self, message, channel):
        avId = self.air.getAvatarIdFromSender()
        
        if not self.checkTimestamp(avId):
            return

        av = self.air.doId2do.get(avId)
        
        if not av:
            return
        
        if av.isMuted():
            self.air.writeServerEvent('chat-said-muted', avId=avId, name=av.getName(), accountId=av.DISLid)
            return

        self.air.writeServerEvent('chat-said', avId=avId, message=message)
        
        if not channel:
            av.d_setTalk(message)
        elif channel in OTPGlobals.CHAT_CHANNELS:
            minAccess = OTPGlobals.CHAT_CHANNELS[channel]
            
            if av.getAdminAccess() < minAccess:
                return

            for playerId, player in self.air.getObjectsOfClass(DistributedPlayerAI).items():
                if player.zoneId == av.zoneId and player.getAdminAccess() >= minAccess:
                    player.d_setTalkFrom(avId, channel, message)

    def __setChatMessage(self, avId, message):
        av = self.air.doId2do.get(avId)

        if av:
            av.d_setTalk(message)
