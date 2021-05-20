from panda3d.core import NodePath, Vec4, loadPrcFile
import PiratesLogger
import os

for dtool in ('children', 'parent', 'name'):
    del NodePath.DtoolClassDict[dtool]

if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/dev.prc')
    loadPrcFile('config/dev_client.prc')

    if os.path.isfile('config/personal.prc'):
        loadPrcFile('config/personal.prc')

    if os.path.isfile('config/local.prc'):
        loadPrcFile('config/local.prc')

import sys
if sys.platform == 'darwin':
    quality = 500
else:
    quality = 256

print ':PiratesStart: Starting the game.'
import __builtin__

from pirates.launcher.PiratesLauncher import PiratesLauncher
launcher = PiratesLauncher()
__builtin__.launcher = launcher

from direct.gui import DirectGuiGlobals
import PiratesGlobals
DirectGuiGlobals.setDefaultFontFunc(PiratesGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
import PiratesBase
PiratesBase.PiratesBase()
from direct.showbase.ShowBaseGlobal import *

if base.win == None:
    print 'Unable to open window; aborting.'
    sys.exit()

import PiratesLoader
base.loader = PiratesLoader.PiratesLoader(base)
base.loader.preloadModels()

__builtin__.loader = base.loader
launcher.setPandaErrorCode(0)
base.sfxPlayer.setCutoffDistance(500.0)

from pirates.piratesgui.PDialog import PDialog
dialog = PDialog(text='Pre-initialise PDialog')
dialog.destroy()

from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
rolloverSound = loadSfx(SoundGlobals.SFX_GUI_ROLLOVER_01)
rolloverSound.setVolume(0.5)
DirectGuiGlobals.setDefaultRolloverSound(rolloverSound)
clickSound = loadSfx(SoundGlobals.SFX_GUI_CLICK_01)
DirectGuiGlobals.setDefaultClickSound(clickSound)
clearColor = Vec4(0.0, 0.0, 0.0, 1.0)
base.win.setClearColor(clearColor)
from pirates.shader.Hdr import *
hdr = Hdr()
from pirates.seapatch.Reflection import Reflection
Reflection.initialize(render)
serverVersion = config.GetString('server-version', 'no_version_set')

from pirates.distributed import PiratesClientRepository
cr = PiratesClientRepository.PiratesClientRepository(serverVersion, launcher)
base.initNametagGlobals()
base.startShow(cr)
if config.GetBool('want-portal-cull', 0):
    base.cam.node().setCullCenter(base.camera)
    base.graphicsEngine.setPortalCull(1)

def _doExit(*args):
    print ':TaskManager: TaskManager.destroy()'
    os._exit(1)

taskMgr.destroy = _doExit

try:
    base.run()
finally:
    os._exit(0)
