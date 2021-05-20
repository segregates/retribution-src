from panda3d.core import getModelPath
# STUB

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedGAConnectorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAConnectorAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

    # setModelPath(string) required broadcast ram
    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    # setLinks(uint8, string, Link []) broadcast ram
    def setLinks(self, isExterior, links):
        self.isExterior = isExterior
        self.links = links
    
    def d_setLinks(self, isExterior, links):
        self.sendUpdate('setLinks', [isExterior, links])
    
    def b_setLinks(self, isExterior, links):
        self.setLinks(isExterior, links)
        self.d_setLinks(isExterior, links)
    
    def getLinks(self):
        return self.isExterior, self.links
    
    # setVisAllowed(bool) required broadcast ram
    def setVisAllowed(self, visAllowed):
        self.visAllowed = visAllowed
    
    def d_setVisAllowed(self, visAllowed):
        self.sendUpdate('setVisAllowed', [visAllowed])
    
    def b_setVisAllowed(self, visAllowed):
        self.setVisAllowed(visAllowed)
        self.d_setVisAllowed(visAllowed)
    
    def getVisAllowed(self):
        return self.visAllowed

    # setUniqueId(string) required broadcast ram
    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    # requestPrivateArea(uint32) airecv clsend

    # setPrivateArea(uint32, uint32, uint32, bool) airecv clsend

    def posControlledByCell(self):
        return False
    
    def requestPrivateArea(self, id):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return
        
        if self.links[0][1] == id:
            link = self.links[0]
        elif self.links[1][1] == id:
            link = self.links[1]
        else:
            return

        self.sendUpdateToAvatarId(avId,
                                  'setPrivateArea',
                                  [link[4], link[5], link[1], 1])