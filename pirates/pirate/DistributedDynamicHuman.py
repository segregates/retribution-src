from pirates.battle.DistributedBattleAvatar import DistributedBattleAvatar
from DynamicHuman import DynamicHuman

class DistributedDynamicHuman(DistributedBattleAvatar, DynamicHuman):

    def __init__(self, other=None):
        DistributedBattleAvatar.__init__(self, base.cr)
        DynamicHuman.__init__(self, other)