from direct.distributed.DistributedObject import DistributedObject

class DistributedGuild(DistributedObject):
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.name = ''
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name