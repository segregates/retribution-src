from direct.distributed.DistributedObject import DistributedObject
from otp.ai.MagicWordGlobal import *
from otp.otpbase import OTPGlobals, OTPLocalizer

class ChatAgent(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.chatAgent = self
        self.channel = 0

    def delete(self):
        DistributedObject.delete(self)
        self.cr.chatAgent = None

    def verifyMessage(self, message):
        try:
            message.decode('ascii')
            return True
        except:
            return False

    def sendChatMessage(self, message):
        if self.verifyMessage(message):
            if base.localAvatar.isMuted():
                base.localAvatar.sendMuteWarning()
            else:
                self.sendUpdate('chatMessage', [message, self.channel])

@magicWord(category=CATEGORY_MODERATION, types=[int])
def channel(channel=-1):
    """ Set the chat channel of the current avatar. """

    if channel == -1:
        return "You are currently talking in the %s channel." % OTPLocalizer.ChatChannels[base.cr.chatAgent.channel]
    elif channel not in OTPGlobals.CHAT_CHANNELS:
        return "Invalid channel specified."
    elif spellbook.getInvoker().getAdminAccess() < OTPGlobals.CHAT_CHANNELS[channel]:
        return "This channel is reserved for %ss." % OTPLocalizer.ChatChannels[channel].lower()

    base.cr.chatAgent.channel = channel
    return "You are now talking in the %s channel." % OTPLocalizer.ChatChannels[channel]
