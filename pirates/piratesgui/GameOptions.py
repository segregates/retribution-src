from panda3d.core import AntialiasAttrib, Camera, ConfigVariable, ConfigVariableBool, ConfigVariableDouble, ConfigVariableInt, GraphicsStateGuardian, WindowProperties, loadPrcFile, loadPrcFileData
import copy
import string
import os
import sys
import datetime
from direct.gui.DirectGui import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesbase import PLocalizer
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from otp.settings.Settings import Settings
from pirates.piratesgui import PDialog
from pirates.seapatch.Water import Water
from direct.motiontrail.MotionTrail import MotionTrail
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesgui.GameOptionsGui import *
from pirates.uberdog.UberDogGlobals import InventoryType

resolution_table = [(800, 600), (1024, 768), (1280, 720), (1280, 1024), (1360, 768), (1600, 900), (1600, 1200), (1920, 1080)]

class DisplayOptions:
    notify = DirectNotifyGlobal.directNotify.newCategory('DisplayOptions')

    def set(self, options, pipe, width, height):
        fullscreen = options.fullscreen

        self.current_pipe = base.pipe
        self.current_properties = WindowProperties(base.win.getProperties())

        properties = self.current_properties

        if self.current_pipe == pipe and self.current_properties.getFullscreen() == fullscreen and self.current_properties.getXSize() == width and self.current_properties.getYSize() == height:
            return True

        properties = WindowProperties()
        properties.setSize(width, height)
        properties.setFullscreen(fullscreen)

        if self.resetWindowProperties(pipe, properties):
            properties = base.win.getProperties()

            if properties.getFullscreen() == fullscreen and properties.getXSize() == width and properties.getYSize() == height:
                return True
        
        self.restoreWindowProperties(options)
        return False

    def resetWindowProperties(self, pipe, properties):
        currentProperties = WindowProperties(base.win.getProperties())
        gsg = base.win.getGsg()

        newProperties = WindowProperties(currentProperties)
        newProperties.addProperties(properties)
        newProperties.clearOrigin()

        if base.pipe != pipe:
            gsg = None

        if gsg == None and currentProperties.getFullscreen() != newProperties.getFullscreen() or currentProperties.getParentWindow() != newProperties.getParentWindow():
            base.pipe = pipe

            if not base.openMainWindow(props = newProperties, gsg = gsg, keepCamera = True):
                return False

            base.graphicsEngine.openWindows()

            if base.win.isClosed():
                base.closeWindow(base.win)
                return False
        else:
            base.win.requestProperties(properties)
            base.graphicsEngine.renderFrame()

        return True

    def restoreWindowProperties(self, options):
        if self.resetWindowProperties(self.current_pipe, self.current_properties):
            return
        
        if self.current_properties.getFullscreen():
            options.fullscreen = 0
            tryProps = self.current_properties
            tryProps.setFullscreen(0)
            
            if self.resetWindowProperties(self.current_pipe, tryProps):
                self.current_properties = copy.copy(tryProps)
                return

        self.notify.error('Failed opening regular window!')

class Options(Settings):
    notify = DirectNotifyGlobal.directNotify.newCategory('Options')
    option_low = 0
    option_medium = 1
    option_high = 2
    option_custom = 3
    texture_low = 256
    texture_medium = 512
    texture_high = 1024
    texture_maximum = -1
    default_max_texture_dimension = -1
    texture_scale_low = 0.25
    texture_scale_medium = 0.5
    texture_scale_high = 1.0
    texture_scale_maximum = 1.0
    SpecialEffectsHigh = 2
    SpecialEffectsMedium = 1
    SpecialEffectsLow = 0
    RadarAxisMap = 0
    RadarAxisCamera = 1
    Frames = 0

    def __init__(self):
        Settings.__init__(self, 'settings.json')
        self.default()
        self.texture_scale_mode = True
        self.invasionOn = False
        self.display = DisplayOptions()
    
    def getOptions(self):
        return {
            'windowWidth': self.window_width,
            'windowHeight': self.window_height,
            'fullscreenWidth': self.fullscreen_width,
            'fullscreenHeight': self.fullscreen_height,
            'fullscreenMode': bool(self.fullscreen),
            'reflection': self.reflection,
            'shader': bool(self.shader),
            'smoothEdges': bool(self.smoothEdges),
            'shadow': bool(self.shadow),
            'textureSize': self.texture,
            'textureCompression': bool(self.textureCompression),
            'soundEnabled': bool(self.sound),
            'soundVolume': self.sound_volume,
            'musicEnabled': bool(self.music),
            'musicVolume': self.music_volume,
            'guiScale': self.gui_scale,
            'chatboxScale': self.chatbox_scale,
            'specialEffects': self.special_effects,
            'textureScale': self.texture_scale,
            'characterDetails': self.character_detail_level,
            'terrainDetails': self.terrain_detail_level,
            'mouseLook': bool(self.mouse_look),
            'gamma': self.gamma,
            'gammaEnabled': bool(self.gamma_enable),
            'hdrEnabled': bool(self.hdr),
            'hdrFactor': self.hdr_factor,
            'oceanVisibility': self.ocean_visibility,
            'landMapRadarAxis': self.land_map_radar_axis,
            'oceanMapRadarAxis': self.ocean_map_radar_axis,
            'FramesPerSecond': bool(self.FPS),
            'simpleDisplayOption': self.simple_display_option,
            'useStereo': bool(self.use_stereo),
        }

    def save(self):
        self.write(self.getOptions())

    def validate(self, options, dataType, dataName, default, acceptableValues = []):
        if dataName not in options:
            return default

        data = options[dataName]
        
        if isinstance(data, dataType) and (data in acceptableValues or not acceptableValues):
            return data
        else:
            return default

    def load(self):
        self.api = os.environ.get('POR_GRAPHICS_API', 'pandagl')
        options = self.read()
        
        if not options:
            self.default()
            self.save()
            return

        validWidths = [width for width, height in resolution_table]
        validHeights = [height for width, height in resolution_table]

        self.window_width = self.validate(options, int, 'windowWidth', 800, validWidths)
        self.window_height = self.validate(options, int, 'windowHeight', 600, validHeights)
        self.fullscreen_width = self.validate(options, int, 'fullscreenWidth', 800, validWidths)
        self.fullscreen_height = self.validate(options, int, 'fullscreenHeight', 600, validHeights)
        self.fullscreen = self.validate(options, bool, 'fullscreenMode', False)
        self.reflection = self.validate(options, int, 'reflection', 0)
        self.shader = self.validate(options, bool, 'shader', False)
        self.smoothEdges = self.validate(options, bool, 'smoothEdges', False)
        self.shadow = self.validate(options, bool, 'shadow', False)
        self.texture = self.validate(options, int, 'textureSize', -1, [-1, 256, 512, 1024])
        self.textureCompression = self.validate(options, bool, 'textureCompression', False)
        self.sound = self.validate(options, bool, 'soundEnabled', False)
        self.sound_volume = self.validate(options, float, 'soundVolume', 1.0)
        self.music = self.validate(options, bool, 'musicEnabled', False)
        self.music_volume = self.validate(options, float, 'musicVolume', 1.0)
        self.gui_scale = self.validate(options, float, 'guiScale', 0.5)
        self.chatbox_scale = self.validate(options, float, 'chatboxScale', 0.0)
        self.special_effects = self.validate(options, int, 'specialEffects', 2, [0, 1, 2])
        self.texture_scale = self.validate(options, float, 'textureScale', 1.0)

        if self.texture_scale <= 0.0:
            self.texture_scale = 1.0

        self.character_detail_level = self.validate(options, int, 'characterDetails', 2, [0, 1, 2])
        self.terrain_detail_level = self.validate(options, int, 'terrainDetails', 2, [0, 1, 2])
        self.mouse_look = self.validate(options, bool, 'mouseLook', False)
        self.gamma = self.validate(options, float, 'gamma', 0.25)
        self.gamma_enable = self.validate(options, bool, 'gammaEnabled', False)
        self.hdr = self.validate(options, bool, 'hdrEnabled', False)
        self.hdr_factor = self.validate(options, float, 'hdrFactor', 1.0)
        self.ocean_visibility = self.validate(options, int, 'oceanVisibility', 1, [0, 1, 2])
        self.land_map_radar_axis = self.validate(options, int, 'landMapRadarAxis', self.RadarAxisMap, [self.RadarAxisMap, self.RadarAxisCamera])
        self.ocean_map_radar_axis = self.validate(options, int, 'oceanMapRadarAxis', self.RadarAxisCamera, [self.RadarAxisMap, self.RadarAxisCamera])
        self.simple_display_option = self.validate(options, int, 'simpleDisplayOption', 3, [0, 1, 2, 3])
        self.use_stereo = self.validate(options, bool, 'useStereo', False)
        self.FPS = self.validate(options, bool, 'FramesPerSecond', False)
    
    def applyPre(self):
        self.options_to_config()
        self.setPrc(self.optionsToPrcData())

    def config_to_options(self):
        self.default()

        win_size = ConfigVariableInt('win-size')
        horizontal_resolution = win_size.getWord(0)
        vertical_resolution = win_size.getWord(1)

        self.fullscreen = config.GetBool('fullscreen', 0)

        if config.GetBool('want-water-reflection', 0):
            self.reflection = 2

            if config.GetBool('want-water-reflection-show-through-only', 0):
                self.reflection = 1
        else:
            self.reflection = 0

        if config.GetBool('want-water-reflect-all', 0):
            self.reflection = 3

        self.window_width = horizontal_resolution
        self.window_height = vertical_resolution
        self.fullscreen_width = horizontal_resolution
        self.fullscreen_height = vertical_resolution
        self.shader = config.GetBool('want-shaders', 1)
        self.shadow = config.GetBool('want-avatar-shadows', 0)
        self.texture = config.GetInt('max-texture-dimension', Options.default_max_texture_dimension)
        self.textureCompression = config.GetBool('compressed-textures', 0)
        self.texture_scale = config.GetFloat('texture-scale', 1.0)
        self.sound = config.GetBool('audio-sfx-active', 1)
        self.sound_volume = config.GetFloat('audio-sfx-volume', 1.0)
        self.music = config.GetBool('audio-music-active', 1)
        self.music_volume = config.GetFloat('audio-music-volume', 1.0)
        self.ocean_visibility = config.GetInt('ocean-visibility', 0)
        self.land_map_radar_axis = config.GetInt('land-map-radar-axis', self.RadarAxisMap)
        self.ocean_map_radar_axis = config.GetInt('ocean-map-radar-axis', self.RadarAxisCamera)

    def options_to_config(self):
        ConfigVariableBool('want-water-reflection', 0).setValue(bool(self.reflection))
        ConfigVariableBool('want-water-reflection-show-through-only', 0).setValue(self.reflection == 1)
        ConfigVariableBool('want-water-reflect-all', 0).setValue(self.reflection == 3)
        ConfigVariableBool('want-shaders', 0).setValue(bool(self.shader))
        ConfigVariableBool('want-avatar-shadows', 0).setValue(bool(self.shadow))
        ConfigVariableBool('compressed-textures', 0).setValue(bool(self.textureCompression))

    def getWidth(self):
        if self.fullscreen:
            return self.fullscreen_width
        else:
            return self.window_width

    def getHeight(self):
        if self.fullscreen:
            return self.fullscreen_height
        else:
            return self.window_height

    def getFullscreen(self):
        return self.fullscreen

    def getWindowed(self):
        return not self.fullscreen

    def optionsToPrcData(self):
        return 'win-size %s %s\nfullscreen %s\ncompressed-textures %s' % (self.getWidth(), self.getHeight(), bool(self.fullscreen), bool(self.textureCompression))

    def setRuntimeOptions(self):
        base.enableSoundEffects(self.sound)
        base.enableMusic(self.music)
        
        for manager in base.sfxManagerList:
            manager.setVolume(self.sound_volume)

        if base.musicManager:
            base.musicManager.setVolume(self.music_volume)

        self.setRuntimeSpecialEffects()
        self.setRuntimeGridDetailLevel(self.terrain_detail_level)
        self.setRuntimeAvatarDetailLevel(self.character_detail_level)

        if self.smoothEdges:
            render.setAntialias(AntialiasAttrib.MMultisample)

        if base.win and base.win.getGsg():
            if self.gamma_enable:
                base.win.getGsg().setGamma(self.optionsGammaToGamma(self.gamma))

        self.setTextureScale()
        self.setRuntimeStereo()
        self.setLandMapRadarAxis()
        self.setOceanMapRadarAxis()

    def setTextureScale(self):
        config_variable = ConfigVariableDouble('texture-scale', 1.0)
        config_variable.setValue(min(1.0, max(0.0, self.texture_scale)))

    def getGUIScale(self):
        return self.gui_scale * 0.598 + 0.696

    def default(self):
        self.window_width = 800
        self.window_height = 600
        self.fullscreen_width = 800
        self.fullscreen_height = 600
        self.fullscreen = 0
        self.reflection = 1
        self.shader = 0
        self.smoothEdges = 0
        self.shadow = 0
        self.texture = self.texture_low
        self.textureCompression = 1
        self.sound = 1
        self.sound_volume = 1.0
        self.music = 1
        self.music_volume = 1.0
        self.gui_scale = 0.245
        self.chatbox_scale = 0.0
        self.special_effects = self.SpecialEffectsMedium
        self.texture_scale = 1.0
        self.character_detail_level = Options.option_medium
        self.terrain_detail_level = Options.option_medium
        self.mouse_look = 0
        self.gamma = 0.25
        self.gamma_enable = 0
        self.ocean_visibility = 0
        self.hdr = 0
        self.hdr_factor = 1.0
        self.simple_display_option = Options.option_custom
        self.use_stereo = 0
        self.FPS = self.Frames
        self.land_map_radar_axis = self.RadarAxisMap
        self.ocean_map_radar_axis = self.RadarAxisCamera

    def setPrc(self, string):
        loadPrcFileData('game_options', string)

    def getTextureScaleString(self):
        if self.texture_scale == Options.texture_scale_low:
            return 'low'
        elif self.texture_scale == Options.texture_scale_medium:
            return 'medium'
        elif self.texture_scale == Options.texture_scale_high:
            return 'high'

    def getGameOptionString(self, level):
        if level == Options.option_low:
            return 'low'
        elif level == Options.option_medium:
            return 'med'
        else:
            return 'high'

    def setRuntimeGridDetailLevel(self, level):
        self.setPrc('grid-detail %s\n' % self.getGameOptionString(level))

        try:
            messenger.send('grid-detail-changed', [level])
            base.positionFarCull()
        except:
            pass

    def setRuntimeAvatarDetailLevel(self, level):
        self.setPrc('avatar-detail %s\n' % self.getGameOptionString(level))

    def optionsGammaToGamma(self, gamma):
        return gamma * 2.0 + 0.5

    def setInvasion(self, invasionOn):
        self.invasionOn = invasionOn

    def getCharacterDetailSetting(self):
        return self.character_detail_level and not self.invasionOn

    def getTerrainDetailSetting(self):
        return self.terrain_detail_level and not self.invasionOn

    def getSpecialEffectsSetting(self):
        return self.special_effects and not self.invasionOn

    def setRuntimeSpecialEffects(self):
        if hasattr(base, 'localAvatar'):
            area = localAvatar.getParentObj()

            if hasattr(area, 'envEffects') and area.envEffects:
                area.envEffects.unloadEffects()
                area.envEffects.loadEffects()

        if self.special_effects == Options.SpecialEffectsLow or self.invasionOn:
            MotionTrail.setGlobalEnable(False)
        elif self.special_effects == Options.SpecialEffectsMedium:
            MotionTrail.setGlobalEnable(True)
        elif self.special_effects == Options.SpecialEffectsHigh:
            MotionTrail.setGlobalEnable(True)

    def setRuntimeStereo(self):
        if self.use_stereo:
            if not base.stereoEnabled:
                base.toggleStereo()
        elif base.stereoEnabled:
            base.toggleStereo()

    def setRuntimeFPS(self):
        if self.FPS:
            if not base.FPSEnabled:
                base.toggleFPS()
        elif base.FPSEnabled:
            base.toggleFPS()

    def setLandMapRadarAxis(self):
        messenger.send('landMapRadarAxisChanged', [
            self.land_map_radar_axis])


    def getLandMapRadarAxis(self):
        return self.land_map_radar_axis


    def setOceanMapRadarAxis(self):
        messenger.send('oceanMapRadarAxisChanged', [self.ocean_map_radar_axis])

    def setFPS(self):
        messenger.send('FPSChanged', [self.FPS])


    def getOceanMapRadarAxis(self):
        return self.ocean_map_radar_axis

class KeyMappings:
    notify = DirectNotifyGlobal.directNotify.newCategory('KeyMappings')

    def __init__(self):
        self.startWatcher()


    def startWatcher(self):
        base.buttonThrowers[0].node().setButtonDownEvent('GameOptions-buttonWatcher')


    def destroy(self):
        base.buttonThrowers[0].node().setButtonDownEvent('')



class GameOptions(BorderFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GameOptions')

    def __init__(self, title, x, y, width, height, options, chooser = 0, keyMappings = None):
        self.width = width
        self.height = height
        self.chooser = chooser
        self.enable_hdr = config.GetInt('want-game-options-hdr', 1)
        self.enable_ship_visibility = config.GetInt('want-game-options-ship-visibility', 0)
        self.dialog = None
        self.restore_options = None
        self.current_options = None
        self.options = options

        if not keyMappings:
            keyMappings = KeyMappings()
        
        self.keyMappings = keyMappings
        self.options.options_to_config()
        self.current_options = copy.copy(self.options)

        self.shader_support = False
        self.shader_model = GraphicsStateGuardian.SM00

        if base.win and base.win.getGsg():
            self.shader_model = base.win.getGsg().getShaderModel()

            if self.shader_model >= GraphicsStateGuardian.SM11:
                self.shader_support = True

        BorderFrame.__init__(self, relief = None, state = DGG.NORMAL, frameColor = PiratesGuiGlobals.FrameColor, borderWidth = PiratesGuiGlobals.BorderWidth, pos = (x, 0.0, y), frameSize = (0, width, 0, height), sortOrder = 20)
        self.initialiseoptions(GameOptions)
        self.gui = GameOptionsGui(self, title, x, y, width, height, options, chooser, keyMappings)
        BorderFrame.hide(self)

    def destroy(self):
        if self.gui:
            self.gui.destroy()
        else:
            self.ignoreAll()
        self.delete_dialogs()
        BorderFrame.destroy(self)

    def get_pipe(self):
        return base.pipe

    def set_display(self, options, pipe, width, height):
        success = options.display.set(options, pipe, width, height)
        if success:
            self.current_options = copy.copy(options)
        else:
            self.options = copy.copy(self.current_options)
            self.set_options(False)

    def fade_button(self, button):
        if button:
            button.setAlphaScale(self.not_selected_color)
            button['text_fg'] = (1.0, 1.0, 1.0, 1.0)
            button['selected'] = False

    def highlight_button(self, button):
        if button:
            button.setAlphaScale(self.selected_color)
            button['text_fg'] = (0.200, 0.800000, 0.598, 1.0)
            button['selected'] = True

    def inactive_highlight_button(self, button):
        if button:
            button.setAlphaScale(self.selected_color)
            button['text_fg'] = (0.100, 0.4, 0.299, 1.0)

    def inactive_button(self, button):
        if button:
            button.setAlphaScale(self.selected_color)
            button['text_fg'] = (0.200, 0.200, 0.200, 1.0)

    def default_button_function(self):
        self.options = Options()
        self.options.default()
        self.set_options(True)
        if hasattr(base, 'localAvatar') and base.localAvatar.isPopulated() and self.gui:
            self.tutPanelOptions = [0] * 3
            self.gui.setTutPanelOptions()

    def restore_button_function(self):
        if self.restore_options:
            self.options = copy.copy(self.restore_options)
            self.set_options(True)

        if hasattr(base, 'localAvatar') and base.localAvatar.isPopulated() and self.gui:
            self.tutPanelOptions = [0] * 3
            self.setTutPanelOptions()

    def delete_dialogs(self):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
    
    def show_dialog(self, text):
        self.delete_dialogs()
        self.dialog = PDialog.PDialog(text = text, style = OTPDialog.Acknowledge, giveMouse = False, command = self.default_dialog_command)
        self.dialog.setBin('gui-fixed', 2)

    def display_restart_dialog(self):
        self.show_dialog(PLocalizer.GameOptionsApplicationRestartMessage)

    def display_noteOnChange_dialog(self):
        self.show_dialog(PLocalizer.GameOptionsNoteOnChange)

    def display_stereoOption_dialog(self):
        self.show_dialog(PLocalizer.GameOptionsStereoOption)

    def save_button_function(self):
        self.options.save()
        self.show_dialog(PLocalizer.GameOptionsSaved)

        if hasattr(base, 'localAvatar') and base.localAvatar.isPopulated():
            inv = base.localAvatar.getInventory()
            if inv:
                if self.tutPanelOptions[0] != inv.getStackQuantity(InventoryType.TutTypeBasic):
                    base.localAvatar.sendRequestChangeTutType(InventoryType.TutTypeBasic, self.tutPanelOptions[0])

                if self.tutPanelOptions[1] != inv.getStackQuantity(InventoryType.TutTypeIntermediate):
                    base.localAvatar.sendRequestChangeTutType(InventoryType.TutTypeIntermediate, self.tutPanelOptions[1])

                if self.tutPanelOptions[2] != inv.getStackQuantity(InventoryType.TutTypeAdvanced):
                    base.localAvatar.sendRequestChangeTutType(InventoryType.TutTypeAdvanced, self.tutPanelOptions[2])

    def default_dialog_command(self, value):
        self.delete_dialogs()

    def close_button_function(self):
        self.hide()

    def reflection_off_button_function(self):
        self.options.reflection = 0
        Water.all_reflections_off()
        self.highlight_button(self.reflection_off_button)
        self.fade_button(self.reflection_sky_button)
        self.fade_button(self.reflection_default_button)
        self.fade_button(self.reflection_all_button)
        messenger.send('options_reflections_change', [0])
        self.update()

    def reflection_sky_button_function(self):
        self.options.reflection = 1
        Water.all_reflections_show_through_only()
        self.fade_button(self.reflection_off_button)
        self.highlight_button(self.reflection_sky_button)
        self.fade_button(self.reflection_default_button)
        self.fade_button(self.reflection_all_button)
        messenger.send('options_reflections_change', [1])
        self.update()

    def reflection_default_button_function(self):
        self.options.reflection = 2
        Water.all_reflections_on()
        self.fade_button(self.reflection_off_button)
        self.fade_button(self.reflection_sky_button)
        self.highlight_button(self.reflection_default_button)
        self.fade_button(self.reflection_all_button)
        messenger.send('options_reflections_change', [2])
        self.update()

    def reflection_all_button_function(self):
        self.options.reflection = 3
        Water.all_reflections_on()
        self.fade_button(self.reflection_off_button)
        self.fade_button(self.reflection_sky_button)
        self.fade_button(self.reflection_default_button)
        self.highlight_button(self.reflection_all_button)
        self.update()

    def shader_off_button_function(self):
        if self.options.shader != 0:
            self.display_restart_dialog()

        self.options.shader = 0
        self.fade_button(self.shader_on_button)
        self.highlight_button(self.shader_off_button)
        self.update()

    def shader_on_button_function(self):
        if self.options.shader != 1:
            self.display_restart_dialog()

        self.options.shader = 1
        self.fade_button(self.shader_off_button)
        self.highlight_button(self.shader_on_button)
        self.update()

    def simple_shadow_button_function(self):
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.disableAvatarShadows()

        self.options.shadow = 0
        self.highlight_button(self.simple_shadow_button)
        self.fade_button(self.shadow_button)
        self.update()

    def shadow_button_function(self):
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.enableAvatarShadows()

        self.options.shadow = 1
        self.fade_button(self.simple_shadow_button)
        self.highlight_button(self.shadow_button)
        self.update()

    def special_effects_low_button_function(self):
        self.highlight_button(self.special_effects_low_button)
        self.fade_button(self.special_effects_medium_button)
        self.fade_button(self.special_effects_high_button)
        self.options.special_effects = Options.SpecialEffectsLow
        self.options.setRuntimeSpecialEffects()

    def special_effects_medium_button_function(self):
        self.fade_button(self.special_effects_low_button)
        self.highlight_button(self.special_effects_medium_button)
        self.fade_button(self.special_effects_high_button)
        self.options.special_effects = Options.SpecialEffectsMedium
        self.options.setRuntimeSpecialEffects()

    def special_effects_high_button_function(self):
        self.fade_button(self.special_effects_low_button)
        self.fade_button(self.special_effects_medium_button)
        self.highlight_button(self.special_effects_high_button)
        self.options.special_effects = Options.SpecialEffectsHigh
        self.options.setRuntimeSpecialEffects()

    def texture_low_button_function(self):
        self.highlight_button(self.texture_low_button)
        self.fade_button(self.texture_medium_button)
        self.fade_button(self.texture_high_button)
        self.fade_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_low:
                self.display_restart_dialog()

            self.options.texture_scale = Options.texture_scale_low
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_low

    def texture_medium_button_function(self):
        self.fade_button(self.texture_low_button)
        self.highlight_button(self.texture_medium_button)
        self.fade_button(self.texture_high_button)
        self.fade_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_medium:
                self.display_restart_dialog()

            self.options.texture_scale = Options.texture_scale_medium
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_medium

    def texture_high_button_function(self):
        self.fade_button(self.texture_low_button)
        self.fade_button(self.texture_medium_button)
        self.highlight_button(self.texture_high_button)
        self.fade_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_high:
                self.display_restart_dialog()

            self.options.texture_scale = Options.texture_scale_high
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_high

    def texture_maximum_button_function(self):
        self.fade_button(self.texture_low_button)
        self.fade_button(self.texture_medium_button)
        self.fade_button(self.texture_high_button)
        self.highlight_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_maximum:
                self.display_restart_dialog()

            self.options.texture_scale = Options.texture_scale_maximum
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_scale_maximum

    def texture_compression_button_function(self):
        self.display_restart_dialog()
        if self.options.textureCompression:
            self.options.textureCompression = 0
        else:
            self.options.textureCompression = 1
        if self.options.textureCompression:
            self.highlight_button(self.texture_compression_button)
        else:
            self.fade_button(self.texture_compression_button)

    def texture_compression_button_display(self):
        if self.options.textureCompression:
            self.highlight_button(self.texture_compression_button)
        else:
            self.fade_button(self.texture_compression_button)

    def character_low_button_function(self):
        self.highlight_button(self.character_low_button)
        self.fade_button(self.character_medium_button)
        self.fade_button(self.character_high_button)
        level = Options.option_low
        self.options.setRuntimeAvatarDetailLevel(self.options.character_detail_level)
        self.options.character_detail_level = level
        self.options.setRuntimeAvatarDetailLevel(level)

    def character_medium_button_function(self):
        self.fade_button(self.character_low_button)
        self.highlight_button(self.character_medium_button)
        self.fade_button(self.character_high_button)
        level = Options.option_medium
        self.options.character_detail_level = level
        self.options.setRuntimeAvatarDetailLevel(level)

    def character_high_button_function(self):
        self.fade_button(self.character_low_button)
        self.fade_button(self.character_medium_button)
        self.highlight_button(self.character_high_button)
        level = Options.option_high
        self.options.character_detail_level = level
        self.options.setRuntimeAvatarDetailLevel(level)

    def terrain_low_button_function(self):
        self.highlight_button(self.terrain_low_button)
        self.fade_button(self.terrain_medium_button)
        self.fade_button(self.terrain_high_button)
        level = Options.option_low
        self.options.terrain_detail_level = level
        self.options.setRuntimeGridDetailLevel(level)

    def terrain_medium_button_function(self):
        self.fade_button(self.terrain_low_button)
        self.highlight_button(self.terrain_medium_button)
        self.fade_button(self.terrain_high_button)
        level = Options.option_medium
        self.options.terrain_detail_level = level
        self.options.setRuntimeGridDetailLevel(level)

    def terrain_high_button_function(self):
        self.fade_button(self.terrain_low_button)
        self.fade_button(self.terrain_medium_button)
        self.highlight_button(self.terrain_high_button)
        level = Options.option_high
        self.options.terrain_detail_level = level
        self.options.setRuntimeGridDetailLevel(level)

    def off_ship_vis_button_function(self):
        self.highlight_button(self.off_ship_vis_button)
        self.fade_button(self.low_ship_vis_button)
        self.fade_button(self.high_ship_vis_button)
        self.options.ocean_visibility = 0
        if not base.overrideShipVisibility:
            base.shipsVisibleFromIsland = 0
            messenger.send('ship_vis_change', [0])

    def low_ship_vis_button_function(self):
        self.fade_button(self.off_ship_vis_button)
        self.highlight_button(self.low_ship_vis_button)
        self.fade_button(self.high_ship_vis_button)
        self.options.ocean_visibility = 1
        if not base.overrideShipVisibility:
            base.shipsVisibleFromIsland = 1
            messenger.send('ship_vis_change', [1])

    def high_ship_vis_button_function(self):
        self.fade_button(self.off_ship_vis_button)
        self.fade_button(self.low_ship_vis_button)
        self.highlight_button(self.high_ship_vis_button)
        self.options.ocean_visibility = 2
        if not base.overrideShipVisibility:
            base.shipsVisibleFromIsland = 2
            messenger.send('ship_vis_change', [2])

    def sound_off_button_function(self):
        self.options.sound = 0
        self.fade_button(self.sound_on_button)
        self.highlight_button(self.sound_off_button)
        base.enableSoundEffects(False)
        self.update()

    def sound_on_button_function(self):
        self.options.sound = 1
        self.highlight_button(self.sound_on_button)
        self.fade_button(self.sound_off_button)
        base.enableSoundEffects(True)
        self.update()

    def music_off_button_function(self):
        self.options.music = 0
        self.fade_button(self.music_on_button)
        self.highlight_button(self.music_off_button)
        base.enableMusic(False)
        self.update()

    def music_on_button_function(self):
        self.options.music = 1
        self.highlight_button(self.music_on_button)
        self.fade_button(self.music_off_button)
        base.enableMusic(True)
        self.update()

    def mouse_look_off_button_function(self):
        self.options.mouse_look = 0
        self.fade_button(self.mouse_look_on_button)
        self.highlight_button(self.mouse_look_off_button)
        self.update()

    def mouse_look_on_button_function(self):
        self.options.mouse_look = 1
        self.highlight_button(self.mouse_look_on_button)
        self.fade_button(self.mouse_look_off_button)
        self.update()

    def open_key_mappings_page(self):
        self.controlsFrame = BorderFrame(parent = self, relief = None, frameSize = (0, self.width - 0.149, 0, PiratesGuiGlobals.TextScaleLarge * 2.5), pos = (0.08, 0, self.height - 0.149 - PiratesGuiGlobals.TextScaleLarge * 2.5))

    def gamma_off_button_function(self):
        self.options.gamma_enable = 0
        self.fade_button(self.gamma_on_button)
        self.highlight_button(self.gamma_off_button)

        if base.win and base.win.getGsg():
            base.win.getGsg().restoreGamma()

        self.update()

    def gamma_on_button_function(self):
        self.options.gamma_enable = 1
        self.highlight_button(self.gamma_on_button)
        self.fade_button(self.gamma_off_button)
        if base.win and base.win.getGsg():
            if self.options.gamma_enable:
                base.win.getGsg().setGamma(self.options.optionsGammaToGamma(self.options.gamma))

        self.update()

    def hdr_off_button_function(self):
        if self.options.hdr != 0:
            self.display_restart_dialog()

        self.options.hdr = 0
        self.fade_button(self.hdr_on_button)
        self.highlight_button(self.hdr_off_button)
        self.update()

    def hdr_on_button_function(self):
        if self.options.hdr != 1:
            self.display_restart_dialog()

        self.options.hdr = 1
        self.highlight_button(self.hdr_on_button)
        self.fade_button(self.hdr_off_button)
        self.update()

    def set_options(self, change_display):
        if self.gui:
            self.gui.set_options(change_display)

    def update(self):
        self.options.options_to_config()

    def isHidden(self):
        if self.gui:
            return self.gui.isHidden()

    def show(self):
        self.restore_options = copy.copy(self.options)
        if self.gui:
            self.gui.show()
            if hasattr(base, 'localAvatar') and base.localAvatar.isPopulated():
                self.setTutPanelOptions()
                self.gui.tutorialButton.show()
                self.gui.tutorialButtonFrame.show()
            else:
                self.gui.tutorialButton.hide()
                self.gui.tutorialButtonFrame.hide()


    def hide(self):
        self.delete_dialogs()
        if self.gui:
            self.gui.hide()

    def initDisplayButtons(self):
        windowed_index = self.resolutionToIndex(self.options.window_width, self.options.window_height)
        fullscreen_index = self.resolutionToIndex(self.options.fullscreen_width, self.options.fullscreen_height)

        for i in xrange(len(self.windowed_resolutions_button_array)):
            if i == windowed_index:
                self.highlight_button(self.windowed_resolutions_button_array[i])
                continue

            self.fade_button(self.windowed_resolutions_button_array[i])

        for i in xrange(len(self.fullscreen_resolutions_button_array)):
            if i == fullscreen_index:
                self.highlight_button(self.fullscreen_resolutions_button_array[i])
                continue

            self.fade_button(self.fullscreen_resolutions_button_array[i])

    def getResolutionTable(self):
        return resolution_table
    
    def resolutionToIndex(self, width, height):
        try:
            return resolution_table.index((width, height))
        except:
            return len(resolution_table) - 1

    def setTextureScale(self):
        self.options.setTextureScale()

    def updateShipVisibility(self):
        if self.enable_ship_visibility:
            if self.options.ocean_visibility == 0:
                self.off_ship_vis_button_function()
            elif self.options.ocean_visibility == 1:
                self.low_ship_vis_button_function()
            elif self.options.ocean_visibility == 2:
                self.high_ship_vis_button_function()

    def setTutPanelOptions(self):
        inv = base.localAvatar.getInventory()
        if inv:
            self.tutPanelOptions = [
                inv.getStackQuantity(InventoryType.TutTypeBasic),
                inv.getStackQuantity(InventoryType.TutTypeIntermediate),
                inv.getStackQuantity(InventoryType.TutTypeAdvanced)]
            if self.gui:
                self.gui.setTutPanelOptions()
