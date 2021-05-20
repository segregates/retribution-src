from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.uberdog.ClientServicesManagerUD import createAccountDB
from otp.ai.MagicWordGlobal import *

class RPCMethod:
    methods = []
    def __init__(self, category, args):
        self.accessLevel = category.access
        self.args = args

    def __call__(self, method):
        method.accessLevel = self.accessLevel
        method.args = self.args
        RPCMethod.methods.append(method)
        return method

rpcmethod = RPCMethod

class PiratesRPCHandlerBase:
    notify = directNotify.newCategory('PiratesRPCHandlerBase')

    def __init__(self, air):
        self.air = air
        self.accountDB = createAccountDB(self)

    def authenticate(self, token, method):
        """
        Ensure the provided token is valid, and meets the access level
        requirements of the method.
        """
        if not token:
            if method.accessLevel > CATEGORY_ANY.access:
                return (-32005, 'Insufficient access')

            # No token, but the method requires no auth
            return None

        token = self.accountDB.decodeToken(token)
        if not token['success']:
            return (-32001, token['reason'])

        if token['accessLevel'] < method.accessLevel:
            return (-32005, 'Insufficient access')

    def listCommands(self, callback):
        result = []
        for method in RPCMethod.methods:
            result.append((method.func_name[4:], method.accessLevel, method.args))

        callback(result)
