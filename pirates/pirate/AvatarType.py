from pirates.piratesbase import PLocalizer
import random

class AvatarType:
    Unspecified = -1
    Any = 0
    Faction = 1
    Track = 2
    Id = 3

    def __init__(self, faction=None, track=None, id=None, base=None, boss=0):
        if base:
            self.faction = base.faction
            self.track = base.track
            self.id = base.id
            self.boss = base.boss
        else:
            self.faction = AvatarType.Unspecified
            self.track = AvatarType.Unspecified
            self.id = AvatarType.Unspecified
            self.boss = 0
        if faction is not None:
            self.faction = faction

        if track is not None:
            self.track = track

        if id is not None:
            self.id = id

        if boss is not None:
            self.boss = boss

        self.__bossType = None

    def getFaction(self):
        return self.faction

    def getTrack(self):
        return self.track

    def getId(self):
        return self.id

    def getBoss(self):
        return self.boss

    def setFaction(self, faction):
        self.faction = faction

    def setTrack(self, track):
        self.track = track

    def setId(self, id):
        self.id = id

    def setBoss(self, boss):
        self.boss = boss

    def howSpecific(self):
        if self.id != AvatarType.Unspecified:
            return AvatarType.Id

        if self.track != AvatarType.Unspecified:
            return AvatarType.Track

        if self.faction != AvatarType.Unspecified:
            return AvatarType.Faction

        return AvatarType.Any

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.faction == other.faction and self.track == other.track and self.id == other.id and self.boss == other.boss

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.faction != other.faction or self.track != other.track or self.id != other.id or self.boss != other.boss

    def __cmp__(self, other):
        return hash(self) - hash(other)

    def isA(self, other):
        return other._contains(self)

    def _contains(self, other):
        if self.id != AvatarType.Unspecified:
            if other.id != self.id:
                return False

        if self.track != AvatarType.Unspecified:
            if other.track != self.track:
                return False

        if self.faction != AvatarType.Unspecified:
            if other.faction != self.faction:
                return False

        if self.boss and not (other.boss):
            return False

        return True

    def getName(self, forceNormal=False):
        spec = self.howSpecific()
        nameTable = PLocalizer.AvatarNames

        if self.boss and not forceNormal:
            nameTable = PLocalizer.BossNames

        try:
            if spec is AvatarType.Id:
                name = nameTable[self.faction][self.track][self.id][0]
            elif spec is AvatarType.Track:
                name = PLocalizer.TrackAvTypeNames[self.faction][self.track][0]
            elif spec is AvatarType.Faction:
                name = PLocalizer.FactionAvTypeNames[self.faction][0]
            else:
                name = PLocalizer.AnyAvType[0]
        except:
            if not self.boss:
                name = PLocalizer.Unknown
            else:
                return self.getName(forceNormal=True)

        if self.boss and forceNormal:
            name = "%s %s" % (name, PLocalizer.Boss)

        return name

    def getShortName(self):
        spec = self.howSpecific()
        if spec is AvatarType.Id:

            nameTable = PLocalizer.AvatarNames

            if self.boss:
                nameTable = PLocalizer.BossNames

            nameTable[self.faction][self.track][self.id]

            if len(PLocalizer.AvatarNames[self.faction][self.track][self.id]) >= 3:
                return PLocalizer.AvatarNames[self.faction][self.track][self.id][2]

        return self.getName()

    def getStrings(self):
        spec = self.howSpecific()
        if spec is AvatarType.Id:
            return PLocalizer.AvatarNames[self.faction][self.track][self.id][1]
        elif spec is AvatarType.Track:
            return PLocalizer.TrackAvTypeNames[self.faction][self.track][1]
        elif spec is AvatarType.Faction:
            return PLocalizer.FactionAvTypeNames[self.faction][1]
        else:
            return PLocalizer.AnyAvType[1]

    def __hash__(self):
        h = hash((self.faction, self.track, self.id))
        if hasattr(self, '_hash'):
            if h != self._hash:
                print ':AvatarType(error): inconsistent AvatarType hash values  new: %s (%s %s %s) previous: %s (%s %s %s)' % (h, self.faction, self.track, self.id, self._hash, self._hashedValues[0], self._hashedValues[1], self._hashedValues[2])
                raise 'inconsistent AvatarType hash values: %s, %s' % (h, self._hash)

        else:
            self._hash = h
            self._hashedValues = (self.faction, self.track, self.id)
        return h

    def __str__(self):
        return 'AvatarType(%s)' % self.getName()

    def __repr__(self):
        return "AvatarType(name='%s', faction=%s, track=%s, id=%s, boss=%s)" % (self.getName(), self.faction, self.track, self.id, self.boss)

    def getRandomBossType(self):
        if self.boss:
            return self

        if self.faction in PLocalizer.BossNames and self.track in PLocalizer.BossNames[self.faction] and self.id in PLocalizer.BossNames[self.faction][self.track]:
            bossLen = len(PLocalizer.BossNames[self.faction][self.track][self.id])
        else:
            bossLen = 0
        whichBoss = random.randint(0, bossLen)
        return AvatarType(base = self, boss = whichBoss)

    def getBossType(self):
        if not self.__bossType:
            self.__bossType = AvatarType(base=self, boss=1)

        return self.__bossType

    def getNonBossType(self):
        if not self.boss:
            return self

        if not self.__bossType:
            self.__bossType = AvatarType(base=self, boss=False)

        return self.__bossType

    def asTuple(self):
        return (self.faction, self.track, self.id, self.boss)

    @classmethod
    def fromTuple(cls, avType):
        if isinstance(avType, cls):
            return avType

        return cls(faction=avType[0], track=avType[1], id=avType[2], boss=avType[3])
