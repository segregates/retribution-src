from panda3d.core import getConfigExpress
import string
import types

try:
    language = getConfigExpress().GetString('language', 'english')
    checkLanguage = getConfigExpress().GetBool('check-language', -0)
except:
    language = config.GetString('language', 'english')
    checkLanguage = config.GetBool('check-language', 0)


def getLanguage():
    return language

print ':PLocalizer: Running in language: %s' % language

from pirates.piratesbase.PLocalizerEnglish import *
from pirates.piratesbase.PQuestStringsEnglish import *
from pirates.piratesbase.PGreetingStringsEnglish import *
from pirates.piratesbase.PDialogStringsEnglish import *

if checkLanguage:
    l = { }
    g = { }
    englishModule = __import__('pirates.piratesbase.PLocalizerEnglish', g, l)
    foreignModule = __import__(_languageModule, g, l)
    for (key, val) in englishModule.__dict__.items():
        if not key in foreignModule.__dict__:
            print 'WARNING: Foreign module: %s missing key: %s' % (_languageModule, key)
            locals()[key] = val
            continue
        if isinstance(val, types.DictType):
            fval = foreignModule.__dict__.get(key)
            for (dkey, dval) in val.items():
                if not dkey in fval:
                    print 'WARNING: Foreign module: %s missing key: %s.%s' % (_languageModule, key, dkey)
                    fval[dkey] = dval
                    continue
            for dkey in fval.keys():
                if not dkey in val:
                    print 'WARNING: Foreign module: %s extra key: %s.%s' % (_languageModule, key, dkey)
                    continue
    for key in foreignModule.__dict__.keys():
        if not key in englishModule.__dict__:
            print 'WARNING: Foreign module: %s extra key: %s' % (_languageModule, key)
            continue
