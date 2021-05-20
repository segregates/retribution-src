import sys, os

os.chdir('..')

# Parse the DC
from panda3d.core import *
from panda3d.direct import *

dc = DCFile()
dc.read('astron/dclass/otp.dc')
dc.read('astron/dclass/pirates.dc')

importDict = {}
dclassesByName = {}

for i in xrange(dc.getNumImportModules()):
    moduleName = '.'.join(dc.getImportModule(i).split('.')[:2])
    importSymbols = []
    for j in xrange(dc.getNumImportSymbols(i)):
        symbolName, suffixes = (dc.getImportSymbol(i, j) + '/').split('/', 1)
        suffixes = suffixes.split('/')
        if 'AI' in suffixes:
            symbolName += 'AI'

        importDict[symbolName] = moduleName

for i in xrange(dc.getNumClasses()):
    dclass = dc.getClass(i)
    name = dclass.getName()
    if name + 'AI' in importDict:
        name += 'AI'

    parents = []
    for j in xrange(dclass.getNumParents()):
        base = dclass.getParent(j).getName()
        if base + 'AI' in importDict:
            base += 'AI'

        parents.append(base)

    dclassesByName[name] = (parents, dclass)

# Make the stubs
def getDefault(args):
    r = []
    for arg in args:
        if 'int' in arg:
            r.append(0)

        elif 'string' in arg:
            r.append('')

        elif '[' in arg:
            r.append([])

        else:
            raise ValueError(arg)

    return r if len(r) > 1 else r[0]

staticImports = ['from direct.directnotify import DirectNotifyGlobal']

importstub = 'from %s import %s'

stubbody = '''# STUB
%(comment)s
%(imports)s
class %(dclassName)s(%(bases)s):
    notify = DirectNotifyGlobal.directNotify.newCategory('%(dclassName)s')

    def __init__(self, air):
%(init)s
%(defvalues)s
%(methods)s
'''

exceptionList = ('NewsManagerAI', 'DistributedBattleAvatarAI', 'DistributedEnemySpawnerAI', 'DistributedInteractiveAI', 'DistributedPopulationTrackerAI', 'DistributedTargetableObjectAI', 'DistrictManagerAI', 'PiratesDistrictAI', 'PiratesDistrictStatsAI', 'PiratesNetMessengerAI', 'DistributedShopKeeperAI', 'DistributedMainWorldAI', 'DistributedTeleportHandlerAI', 'DistributedTeleportMgrAI', 'DistributedWelcomeWorldAI', 'DistributedInteractivePropAI', 'DistributedNPCToyAI', 'DistributedSearchableContainerAI', 'DistributedFishingSpotAI', 'DistributedPotionCraftingTableAI', 'DistributedPotionGameAI', 'DistributedRepairBenchAI', 'DistributedRepairGameAI', 'DistributedMovingObjectAI', 'DistributedNPCNavySailorAI', 'DistributedNPCPirateAI', 'DistributedNPCSkeletonAI', 'DistributedNPCTownfolkAI', 'DistributedPlayerPirateAI', 'DistributedTimeOfDayManagerAI', 'DistributedQuestAvatarAI', 'DistributedQuestGiverAI', 'DistributedQuestPropAI', 'DistributedReputationAvatarAI', 'DistributedBuriedTreasureAI', 'AdministrativeServicesManagerAI', 'DistributedInventoryAI', 'PirateInventoryAI', 'DistributedDinghyAI', 'DistributedGameAreaAI', 'DistributedIslandAI', 'DistributedLocatableObjectAI', 'DistributedLocationManagerAI', 'DistributedOceanGridAI', 'WorldCreatorAI')

for basedir, dir, files in os.walk('.'):
    basedir = basedir[2:]
    if basedir.split(os.sep, 1)[0] != 'pirates':
        continue

    for file in files:
        fullpath = os.path.join(basedir, file)
        if file.endswith('AI.py'):
            f = open(fullpath, 'rb')
            data = f.read(20)
            f.close()

            if not '# STUB' in data:
                # Do not overwrite
                continue

            dclassName = file[:-3]
            if dclassName in exceptionList:
                continue

            basesList, dclass = dclassesByName.get(dclassName, ([], None))
            comment = ''
            if not basesList:
                basesList.append('DistributedObjectAI')
                comment = '# NO BASE CLASS WAS FOUND!\n# IT MEANS THAT THIS FILE HAD NO DEF\n# IN PIRATES.DC WHEN AI-GEN WAS RUN!\n'

            bases = ', '.join(basesList)
            init = '\n'.join(' ' * 8 + '%s.__init__(self, air)' % base for base in basesList)

            imports = '\n'.join(staticImports + ['from %s.%s import %s\n' % (importDict[base], base, base) for base in basesList])

            methods = ''
            defvalues = ''
            if dclass:
                for i in xrange(dclass.getNumFields()):
                    field = repr(dclass.getField(i))
                    if '(' not in field:
                        continue

                    fieldName, keywords = field.rsplit(')', 1)
                    fieldName, args = fieldName.split('(', 1)
                    args = args.split(',')
                    keywords = keywords.split()

                    # Ignore list
                    if fieldName in ('setParentingRules',):
                        continue

                    fieldName1 = fieldName[1:]
                    methods += ' ' * 4 + '# %s\n' % field

                    if 'required' in keywords:
                        paramName = fieldName[3].lower() + fieldName[4:] if fieldName.startswith('set') else fieldName
                        parameters = ['todo_%s_%d' % (type.strip(' []'), j) for j, type in enumerate(args)]
                        parameters[0] = paramName
                        parameters = ', '.join(parameters)

                        # Setter / getter
                        defvalues += '        self.%s = %r\n' % (paramName, getDefault(args))
                        methods += '''    def %(fieldName)s(self, %(parameters)s):
        self.%(paramName)s = %(paramName)s

    def d_%(fieldName)s(self, %(parameters)s):
        self.sendUpdate('%(fieldName)s', [%(parameters)s])

    def b_%(fieldName)s(self, %(parameters)s):
        self.%(fieldName)s(%(parameters)s)
        self.d_%(fieldName)s(%(parameters)s)

    def g%(fieldName1)s(self):
        return [self.%(paramName)s]

''' % locals()
                    else:
                        methods += '\n'

            else:
                print 'Warning: %s has no dclass!' % dclassName
                comment = '# NO BASE CLASS WAS FOUND!\n# IT MEANS THAT THIS FILE HAD NO DEF\n# IN PIRATES.DC WHEN AI-GEN WAS RUN!\n'

            print 'Generating', fullpath
            f = open(fullpath, 'wb')
            f.write(stubbody % locals())
            f.close()
