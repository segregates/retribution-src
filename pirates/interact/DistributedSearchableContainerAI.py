from direct.distributed.DistributedObjectAI import *
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import *

class DistributedSearchableContainerAI(DistributedInteractiveAI, DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)
        self.color = [0, 0, 0, 0]
        self.visZone = ''

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def setSearchTime(self, searchTime):
        self.searchTime = searchTime

    def getSearchTime(self):
        return self.searchTime

    def setType(self, searchType):
        self.type = searchType

    def getType(self):
        return self.type

    def setVisZone(self, visZone):
        self.visZone = visZone

    def getVisZone(self):
        return self.visZone

    def setContainerColor(self, color1, color2, color3, color4):
        self.color = [color1, color2, color3, color4]

    def getContainerColor(self):
        return self.color

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def getSphereScale(self):
        return self.sphereScale

    def handleInteract(self, avId, interactType, instant):
        # TO DO: If av has a quest to search, allow them
        return REJECT

    @classmethod
    def makeFromObjectKey(cls, air, objKey, data):
        obj = DistributedInteractiveAI.makeFromObjectKey(cls, air, objKey, data)
        if 'searchTime' in data:
            obj.setSearchTime(int(float(data['searchTime'])))
        else:
            obj.setSearchTime(1)

        if 'type' in data:
            obj.setType(data['type'])
        else:
            obj.setType('Barrel')

        if 'VisZone' in data:
            obj.setVisZone(data['VisZone'])

        if 'Visual' in data:
            visual = data['Visual']

            if 'Color' in visual:
                obj.setContainerColor(*visual['Color'])

        gridPos = data.get('GridPos')
        if gridPos:
            obj.setPos(gridPos)

        obj.setSphereScale(int(float(data.get('Aggro Radius', 1.0))))
        return obj
