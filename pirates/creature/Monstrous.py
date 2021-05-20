from panda3d.core import NodePath
from pirates.piratesbase import PiratesGlobals

class Monstrous:

    def initializeMonstrousTags(self, rootNodePath):
        rootNodePath.setPythonTag('MonstrousObject', self)
        self.setPythonTag('MonstrousObject', self)
        rootNodePath.setTag('objType', str(PiratesGlobals.COLL_MONSTROUS))
        self.setTag('objType', str(PiratesGlobals.COLL_MONSTROUS))

    def cleanupMontstrousTags(self, rootNodePath):
        rootNodePath.clearPythonTag('MonstrousObject')
        self.clearPythonTag('MonstrousObject')

    def initializeBattleCollisions(self):
        pass
