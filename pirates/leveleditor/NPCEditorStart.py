from panda3d.core import AntialiasAttrib, ConfigVariable, ConfigVariableString, Filename, Vec4, loadPrcFile, loadPrcFileData
loadPrcFile("config/editor.prc")
print 'EditorStart: Starting the game.'
import __builtin__

print 'EditorStart: Loading the settings...'
from otp.settings.Settings import Settings
preferencesFilename = ConfigVariableString('preferences-filename', 'config/preferences.json').getValue()
print 'EditorStart: Reading {0}...'.format(preferencesFilename)
settings = Settings(preferencesFilename)
res = settings.get('res', (1180, 672))
fullscreen = settings.get('fullscreen', False)
if 'fullscreen' not in settings.all():
    settings.set('fullscreen', fullscreen)
music = settings.get('music', True)
if 'music' not in settings.all():
    settings.set('music', music)
sfx = settings.get('sfx', True)
if 'sfx' not in settings.all():
    settings.set('sfx', sfx)
musicVol = settings.get('musicVol', 1.0)
if 'musicVol' not in settings.all():
    settings.set('musicVol', musicVol)
sfxVol = settings.get('sfxVol', 1.0)
if 'sfxVol' not in settings.all():
    settings.set('sfxVol', sfxVol)
loadDisplay = settings.get('loadDisplay', 'pandagl')
if 'loadDisplay' not in settings.all():
    settings.set('loadDisplay', loadDisplay)
loadPrcFileData('editorBase Settings Window Res', 'win-size %s %s' % (res[0], res[1]))
loadPrcFileData('editorBase Settings Window FullScreen', 'fullscreen %s' % fullscreen)
loadPrcFileData('editorBase Settings Music Active', 'audio-music-active %s' % music)
loadPrcFileData('editorBase Settings Sound Active', 'audio-sfx-active %s' % sfx)
loadPrcFileData('editorBase Settings Music Volume', 'audio-master-music-volume %s' % musicVol)
loadPrcFileData('editorBase Settings Sfx Volume', 'audio-master-sfx-volume %s' % sfxVol)
loadPrcFileData('editorBase Settings Load Display', 'load-display %s' % loadDisplay)

class game:
    name = 'pirates'
    process = 'client'

__builtin__.game = game()
import time
import os
import sys
import random
import __builtin__
import gc
gc.disable()

from pirates.launcher.PiratesOnlineLauncher import PiratesOnlineLauncher
launcher = PiratesOnlineLauncher()
__builtin__.launcher = launcher

from direct.gui import DirectGuiGlobals
launcher.setPandaErrorCode(7)
import EditorBase
EditorBase.EditorBase()
from direct.showbase.ShowBaseGlobal import *

if base.win == None:
    print 'Unable to open window; aborting.'
    sys.exit()

launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
if base.config.GetBool("want-improved-graphics", 0):
    print "Enabling improved graphics..."
    render.setAntialias(AntialiasAttrib.MMultisample)
base.sfxPlayer.setCutoffDistance(500.0)
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
serverVersion = base.config.GetString('server-version', 'no_version_set')
print 'serverVersion: ', serverVersion
from pirates.distributed import PiratesClientRepository
cr = PiratesClientRepository.PiratesClientRepository(serverVersion, launcher)
base.initNametagGlobals()
base.startShow(cr)
from otp.distributed import OtpDoGlobals
from pirates.piratesbase import UserFunnel
UserFunnel.logSubmit(1, 'CLIENT_OPENS')
UserFunnel.logSubmit(0, 'CLIENT_OPENS')
if base.config.GetBool('want-portal-cull', 0):
    base.cam.node().setCullCenter(base.camera)
    base.graphicsEngine.setPortalCull(1)

if base.options:
    base.options.options_to_config()
    base.options.setRuntimeOptions()
    try:
        base.run()
    except:
        sys.exit(1)