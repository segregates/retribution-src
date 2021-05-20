from direct.distributed.MsgTypes import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from LoginBase import LoginBase

class LoginPiratesAccount(LoginBase):
    notify = directNotify.newCategory('LoginPiratesAccount')

    def __init__(self, cr):
        LoginBase.__init__(self, cr)

    def supportsRelogin(self):
        return 0

    def authorize(self, username, password):
        return 0 # No error!

    def sendLoginMsg(self):
        pass

    def getErrorCode(self):
        return 0

    def authenticateDelete(self, loginName, password):
        return 1
