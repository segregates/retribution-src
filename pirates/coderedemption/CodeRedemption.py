from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.coderedemption import CodeRedemptionGlobals

class CodeRedemption(DistributedObject):
    notify = directNotify.newCategory('CodeRedemption')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.waiting = False

    def announceGenerate(self):
        self.cr.codeRedemption = self
        DistributedObject.announceGenerate(self)

    def disable(self):
        self.cr.codeRedemption = None
        DistributedObject.disable(self)

    def redeemCode(self, code):
        if code:
            userName = base.cr.csm.username
            accountId = 0 #TODO. not used
            self.waiting = True
            self.sendUpdate('sendCodeForRedemption', [code, userName, accountId])
            taskMgr.doMethodLater(CodeRedemptionGlobals.TIMEOUT_DURATION, self.performTimeout, 'redeem-timeout')

    def performTimeout(self, task):
        if self.waiting:
            self.notify.info("Code redemption timed out. Returning to input gui.")
            self.notifyClientCodeRedeemStatus(CodeRedemptionGlobals.ERROR_ID_TIMEOUT, -1, 0)
        return Task.done

    def notifyClientCodeRedeemStatus(self, status, type, uid):

        if not self.waiting:
            return
        self.waiting = False

        if status == CodeRedemptionGlobals.ERROR_ID_GOOD:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionGood)
        elif status == CodeRedemptionGlobals.ERROR_ID_OVERFLOW:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionFull)
        elif status == CodeRedemptionGlobals.ERROR_ID_TIMEOUT:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionTimeout)
        else:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionBad)
        if type == -1:
            pass
        if type == CodeRedemptionGlobals.CLOTHING:
            localAvatar.guiMgr.messageStack.showLoot([], cloth = uid)
        elif type == CodeRedemptionGlobals.JEWELRY:
            localAvatar.guiMgr.messageStack.showLoot([], jewel = uid)
        elif type == CodeRedemptionGlobals.TATTOO:
            localAvatar.guiMgr.messageStack.showLoot([], tattoo = uid)

        messenger.send('codeRedeemed', [status])
