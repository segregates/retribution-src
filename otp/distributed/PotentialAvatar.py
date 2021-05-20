class PotentialAvatar:

    def __init__(self, id, name, dna, position, wishState = 'CLOSED', wishName = '', defaultShard = 0):
        self.id = id
        self.name = name
        self.dna = dna
        self.position = position
        self.wishState = wishState
        self.wishName = wishName
        self.defaultShard = defaultShard
