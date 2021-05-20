from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedGuildUD(DistributedObjectUD):
    
    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.name = ''
    
    def setName(self, name):
        self.name = name
    
    def d_setName(self, name):
        self.sendUpdate('setName', [name])
    
    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)
    
    def getName(self):
        return self.name