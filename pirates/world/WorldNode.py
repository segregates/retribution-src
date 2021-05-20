from panda3d.core import NodePath
from direct.distributed import DistributedNode
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals

class WorldNode(NodePath):
    notify = directNotify.newCategory('WorldNode')

    def __init__(self):
        NodePath.__init__(self, 'WorldNode')

    def delete(self):
        self.remove_node()
        if self.cr.activeWorld:
            if self.cr.activeWorld.isEmpty() or self.cr.activeWorld.compareTo(self) == 0:
                self.cr.setActiveWorld(None)

        self.ignoreAll()

    def disable(self):
        WorldNode.notify.debug('removing old activeWorld')
        self.detachNode()

    def announceGenerate(self):
        base.cr.setActiveWorld(self)
        self.reparentTo(render)
