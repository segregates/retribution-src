from direct.directnotify import DirectNotifyGlobal

class Lootable:
    notify = directNotify.newCategory('Lootable')

    def __init__(self):
        pass
    
    def startLooting(self, plunderList, timer = 0):
        pass

    def d_requestItem(self, itemInfo):
        self.sendUpdate('requestItem', [itemInfo])

    def d_requestItems(self):
        self.sendUpdate('requestItems', [])

    def doneTaking(self):
        pass

    def getRating(self):
        return -1

    def getTypeName(self):
        return ''
