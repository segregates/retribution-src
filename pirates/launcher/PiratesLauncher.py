from direct.directnotify import DirectNotifyGlobal
import os

class PiratesLauncher:
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesLauncher')

    def getGameServer(self):
        return self.getValue('POR_GAMESERVER', '25.91.142.158')

    def setPandaErrorCode(self, code):
        pass

    def getValue(self, key, default=None):
        return os.environ.get(key, default)

    def setValue(self, key, value):
        os.environ[key] = str(value)

    def isTestServer(self):
        return False
