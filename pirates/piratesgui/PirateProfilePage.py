from panda3d.core import Buffer, Camera, CardMaker, DisplayRegion, Lens, NodePath, PerspectiveLens, Point3, TextNode, Texture, VBase4, Vec3, Vec4
# File: P (Python 2.4)

from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from direct.task import Task
from otp.avatar import Avatar
from otp.otpbase import OTPGlobals
from pirates.friends import PirateFriendSecret
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import DistributedBandMember
from pirates.piratesgui import TeleportConfirm
from pirates.piratesgui import GuiButton
from pirates.piratesgui import BorderFrame
from pirates.pirate import MasterHuman
from pirates.pirate import Human
from pirates.pirate import HumanDNA
from pirates.pirate import DistributedPlayerPirate
from pirates.band import DistributedBandMember
from direct.showbase.PythonUtil import StackTrace
from pirates.world.LocationConstants import LocationIds
import copy
import string
from direct.interval.LerpInterval import LerpPosInterval
GUILDRANK_VETERAN = 4
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1
OPEN_CHAT = 2
SPEEDCHAT_PLUS = 1
SPEEDCHAT = 0

class SkillFrame(DirectFrame):

    def __init__(self, parent, height, minigame = False):
        DirectFrame.__init__(self, relief = None, parent = parent, frameSize = (0, 0.5, 0, 0.100), text = '', text_scale = PiratesGuiGlobals.TextScaleSmall, text_pos = (0, 0, 0), text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, state = DGG.DISABLED, pos = (-0.12, 0, height))
        shipgui = loader.loadModel('models/gui/ship_battle')
        self.bar = OnscreenImage(parent = self, image = shipgui.find('**/ship_battle_speed_bar'), scale = (0.28000, 0, 0.5), pos = (0.188, 0, -0.024))
        if minigame:
            range = ReputationGlobals.MinigameLevelCap
        else:
            range = ReputationGlobals.LevelCap
        self.meter = DirectWaitBar(parent = self, relief = DGG.RAISED, borderWidth = (0.002, 0.002), range = range, value = 0, frameColor = (0.050000, 0.050000, 0.050000, 1), barColor = PiratesGuiGlobals.TextFG14, pos = (0, 0, -0.0299), frameSize = (0, 0.375, 0, 0.02), text = '', text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleSmall, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0.375, 0.0299, 0), textMayChange = 1)



class SocialButton(GuiButton.GuiButton):
    socialButtonColor = (VBase4(1, 1, 1, 1), VBase4(0.348, 0.348, 0.348, 1), VBase4(1.0, 0.0, 0.0, 1))

    def __init__(self, parent, pos, image, command, helpText, scale):
        topgui = loader.loadModel('models/gui/toplevel_gui')
        self.mainCommand = command
        self.circle = GuiButton.GuiButton(parent = parent, relief = None, image = (topgui.find('**/pir_t_gui_frm_base_circle'), topgui.find('**/pir_t_gui_frm_base_circle'), topgui.find('**/pir_t_gui_frm_base_circle_over'), topgui.find('**/pir_t_gui_frm_base_circle')), image_scale = 0.348, pos = pos, command = command, helpText = helpText, helpPos = (-0.100, 0, -0.070), helpOpaque = 1)
        self.button = None
        self.button2 = None
        if helpText == PLocalizer.ProfilePageFriend:
            self.button = OnscreenImage(parent = self.circle, image = image, scale = scale)
        elif helpText == PLocalizer.ProfilePageGuild:
            self.button = OnscreenImage(parent = self.circle, image = image, scale = scale, pos = (0, 0, -0.00300))
        elif helpText in (PLocalizer.ProfilePageIgnore, PLocalizer.ProfilePageUnignore):
            self.button = OnscreenImage(parent = self.circle, image = image, scale = scale)
            self.button2 = GuiButton.GuiButton(parent = self.circle, relief = None, image = (topgui.find('**/pir_t_gui_but_circle_slash'), topgui.find('**/pir_t_gui_but_circle_slash'), topgui.find('**/pir_t_gui_but_circle_slash_over'), topgui.find('**/pir_t_gui_but_circle_slash')), image_scale = 0.348, command = command, helpText = helpText, helpPos = (-0.100, 0, -0.070), helpOpaque = 1)
        else:
            self.button = OnscreenImage(parent = self.circle, image = image, scale = scale)
        breakImage = topgui.find('**/pir_t_gui_but_circle_slash')
        bsUpscale = 8.0
        if type(scale) in [
            type(1.10),
            type(1)]:
            bsScale = float(scale) * bsUpscale
        else:
            bsScale = scale[0] * bsUpscale
        self.breakSymbol = OnscreenImage(parent = self.circle, image = breakImage, scale = 0.320, pos = (0, 0, 0))
        self.breakSymbol.hide()


    def enable(self):
        self.breakSymbol.hide()
        self.circle['image_color'] = self.socialButtonColor[0]
        self.circle['command'] = self.mainCommand
        self.circle['extraArgs'] = []
        self.button['color'] = self.socialButtonColor[0]

        if self.button2:
            self.button2['state'] = DGG.NORMAL
            self.button2['image_color'] = self.socialButtonColor[0]



    def disable(self, text = None, example = False):
        self.breakSymbol.hide()
        if example:
            self.circle['image_color'] = self.socialButtonColor[0]
            self.button['color'] = self.socialButtonColor[0]

            if self.button2:
                self.button2['state'] = DGG.DISABLED
                self.button2['image_color'] = self.socialButtonColor[0]

        else:
            self.circle['image_color'] = self.socialButtonColor[1]
            self.button['color'] = self.socialButtonColor[1]

            if self.button2:
                self.button2['state'] = DGG.DISABLED
                self.button2['image_color'] = self.socialButtonColor[1]

        if text:
            self.circle['command'] = localAvatar.guiMgr.createWarning
            self.circle['extraArgs'] = [
                text,
                PiratesGuiGlobals.TextFG6]
        else:
            self.circle['command'] = None


    def dim(self):
        self.breakSymbol.show()
        self.circle['image_color'] = self.socialButtonColor[0]
        self.button['color'] = self.socialButtonColor[0]


    def destroy(self):
        self.mainCommand = None
        self.circle.destroy()
        del self.circle
        self.button.destroy()
        del self.button
        if self.button2:
            self.button2.destroy()
            del self.button2




class PirateProfilePage(SocialPage.SocialPage):
    socialButtonColor = (VBase4(1, 0.9, 0.696, 1), VBase4(0.9, 0.810000, 0.63, 1), VBase4(1, 0.94495, 0.734, 1), VBase4(0.450, 0.450, 0.450, 1))

    def __init__(self):
        SocialPage.SocialPage.__init__(self, 'Pirate Profile Page')
        self.TC = None
        avatarGui = loader.loadModel('models/gui/avatar_chooser_rope')
        topgui = loader.loadModel('models/gui/toplevel_gui')
        self.goldFounder = topgui.find('**/founders_coin')
        maingui = loader.loadModel('models/gui/gui_main')
        box = (maingui.find('**/exit_button'), maingui.find('**/exit_button'), maingui.find('**/exit_button_over'), maingui.find('**/exit_button'))
        box2 = (maingui.find('**/exit_button1'), maingui.find('**/exit_button1'), maingui.find('**/exit_button_over1'), maingui.find('**/exit_button1'))
        x = maingui.find('**/x2')
        flagLogos = loader.loadModel('models/textureCards/sailLogo')
        self.spanishFlag = flagLogos.find('**/logo_spanish_flag')
        self.frenchFlag = flagLogos.find('**/logo_french_flag')
        basicgui = loader.loadModel('models/textureCards/basic_unlimited')
        icons = loader.loadModel('models/textureCards/icons')
        shopCoins = loader.loadModel('models/textureCards/shopCoins')
        self.profileIcons = [
            icons.find('**/pir_t_gui_gen_land'),
            topgui.find('**/topgui_icon_ship'),
            shopCoins.find('**/shopCoin_cannon')]
        shipgui = loader.loadModel('models/gui/ship_battle')
        chargui = loader.loadModel('models/gui/char_gui')
        self.mainFrame = DirectFrame(relief = None, parent = base.a2dTopLeft, state = DGG.NORMAL, image = maingui.find('**/profile_card_main'), image_scale = 0.275, pos = (1.5, 0, -1.0))
        self.skillFrame = DirectFrame(relief = None, parent = self.mainFrame, state = DGG.NORMAL, image = maingui.find('**/profile_card_weapons_levels'), image_scale = 0.275, pos = (-0.44, 0, 0))
        self.skillFrameClosed = True
        self.skillFrameIval = None
        self.skillButton = GuiButton.GuiButton(relief = None, parent = self.skillFrame, image = (maingui.find('**/side_tab'), maingui.find('**/side_tab'), maingui.find('**/side_tab_over'), maingui.find('**/side_tab')), image_scale = 0.275, state = DGG.NORMAL, command = self.toggleSkillFrame)
        self.skillLabel = DirectLabel(relief = None, parent = self.skillFrame, image = avatarGui.find('**/avatar_c_C_box'), image_scale = (0.4, 0, 0.299), text = PLocalizer.ProfilePageSkillLevels, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_pos = (0, -0.01, 0), text_shadow = PiratesGuiGlobals.TextShadow, state = DGG.DISABLED, pos = (0.0670000, 0, 0.44))
        self.cannonFrame = SkillFrame(self.skillFrame, 0.359)
        self.cannonFrame['text'] = PLocalizer.ProfilePageCannon
        self.sailingFrame = SkillFrame(self.skillFrame, 0.29498)
        self.sailingFrame['text'] = PLocalizer.ProfilePageSailing
        self.cutlassFrame = SkillFrame(self.skillFrame, 0.230)
        self.cutlassFrame['text'] = PLocalizer.ProfilePageCutlass
        self.pistolFrame = SkillFrame(self.skillFrame, 0.165)
        self.pistolFrame['text'] = PLocalizer.ProfilePagePistol
        self.dollFrame = SkillFrame(self.skillFrame, 0.100)
        self.dollFrame['text'] = PLocalizer.ProfilePageDoll
        self.daggerFrame = SkillFrame(self.skillFrame, 0.035000)
        self.daggerFrame['text'] = PLocalizer.ProfilePageDagger
        self.grenadeFrame = SkillFrame(self.skillFrame, -0.0299)
        self.grenadeFrame['text'] = PLocalizer.ProfilePageGrenade
        self.staffFrame = SkillFrame(self.skillFrame, -0.0950)
        self.staffFrame['text'] = PLocalizer.ProfilePageStaff
        self.potionsFrame = SkillFrame(self.skillFrame, -0.16, minigame = True)
        self.potionsFrame['text'] = PLocalizer.ProfilePagePotions
        self.fishingFrame = SkillFrame(self.skillFrame, -0.225, minigame = True)
        self.fishingFrame['text'] = PLocalizer.ProfilePageFishing
        self.mainFrame.setBin('fixed', -1)
        self.mainFrame.hide()
        self.skillFrame.setBin('fixed', -2)
        self.skillFrame.hide()
        self.pirateFrame = DirectFrame(parent = self.mainFrame, relief = None, state = DGG.DISABLED, scale = 0.800000, pos = (-0.44, 0, -0.200))
        self.founderFrame = DirectFrame(parent = self.mainFrame, relief = None, state = DGG.DISABLED, image = None, image_pos = (0, 0, 0), pos = (-0.65, 0, 0.489))
        self.siegeFrame = DirectFrame(parent = self.mainFrame, relief = None, state = DGG.DISABLED, image = None, image_pos = (0, 0, 0), pos = (-0.25, 0, 0.489))
        self.pirateLabel = OnscreenText(parent = self.mainFrame, scale = PiratesGuiGlobals.TextScaleLarge, align = TextNode.ACenter, fg = (0.5, 0.5, 0.5, 1), font = PiratesGlobals.getPirateOutlineFont(), shadow = PiratesGuiGlobals.TextShadow, mayChange = 1, pos = (-0.44, 0.495))
        self.guildLabel = OnscreenText(parent = self.mainFrame, text = '', scale = PiratesGuiGlobals.TextScaleSmall, align = TextNode.ACenter, fg = PiratesGuiGlobals.TextFG2, shadow = PiratesGuiGlobals.TextShadow, mayChange = 1, pos = (-0.44, 0.46))
        self.notorietyLabel = DirectLabel(relief = None, parent = self.mainFrame, image = basicgui.find('**/but_nav'), image_scale = 0.348, text = '', text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0, -0.01, 0), text_shadow = PiratesGuiGlobals.TextShadow, state = DGG.DISABLED, pos = (-0.63, 0, 0.408))
        self.hpMeter = DirectWaitBar(parent = self.mainFrame, relief = DGG.RAISED, borderWidth = (0.002, 0.002), range = 1, value = 0, frameColor = (0.050000, 0.050000, 0.050000, 1), barColor = (0.100, 0.696, 0.100, 1), pos = (-0.714, 0, 0.35698), frameSize = (0, 0.200, 0, 0.0149), text = PLocalizer.ProfilePageHp, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleSmall, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0.02, 0), textMayChange = 1, scale = 0.800000)
        self.hpBar = OnscreenImage(parent = self.mainFrame, image = shipgui.find('**/ship_battle_speed_bar'), scale = (0.12, 1.0, 0.299), pos = (-0.635, 0, 0.362))
        self.voodooMeter = DirectWaitBar(parent = self.mainFrame, relief = DGG.RAISED, borderWidth = (0.00300, 0.00300), range = 1, value = 0, frameColor = (0.050000, 0.050000, 0.050000, 1), barColor = (0.598, 0.598, 0.946, 1), pos = (-0.714, 0, 0.321), frameSize = (0, 0.200, 0, 0.0149), text = PLocalizer.ProfilePageVoodoo, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleSmall, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0.02, 0), textMayChange = 1, scale = 0.800000)
        self.voodooBar = OnscreenImage(parent = self.mainFrame, image = shipgui.find('**/ship_battle_speed_bar'), scale = (0.12, 1.0, 0.299), pos = (-0.635, 0, 0.327))
        self.chatLabel = OnscreenText(parent = self.mainFrame, text = '', scale = PiratesGuiGlobals.TextScaleSmall, align = TextNode.ACenter, fg = PiratesGuiGlobals.TextFG2, shadow = PiratesGuiGlobals.TextShadow, mayChange = 1, pos = (-0.635, 0.275), wordwrap = 5)
        self.xFrame = GuiButton.GuiButton(parent = self.mainFrame, relief = None, image = box, image_scale = 0.275, command = self.hide)
        self.xButton = OnscreenImage(parent = self.xFrame, image = x, scale = 0.140, pos = (-0.174, 0, 0.526))
        self.crewButton = SocialButton(self.mainFrame, (-0.230, 0, 0.37), icons.find('**/pir_t_gui_gen_crew_mug'), self._PirateProfilePage__handleCrew, PLocalizer.ProfilePageCrew, 0.070)
        self.avatarFriendButton = SocialButton(self.mainFrame, (-0.230, 0, 0.27), topgui.find('**/pir_t_gui_gen_friends_pirates'), self._PirateProfilePage__handleAvatarFriend, PLocalizer.ProfilePageFriend, (0.27, 0, 0.27))
        self.guildButton = SocialButton(self.mainFrame, (-0.230, 0, 0.170), icons.find('**/pir_t_gui_gen_guild'), self._PirateProfilePage__handleGuild, PLocalizer.ProfilePageGuild, 0.070)
        self.whisperButton = SocialButton(self.mainFrame, (-0.230, 0, 0.070), icons.find('**/pir_t_gui_gen_whisper'), self._PirateProfilePage__handleWhisper, PLocalizer.ProfilePageWhisper, 0.0598)
        self.challengeButton = SocialButton(self.mainFrame, (-0.230, 0, -0.0299), topgui.find('**/lookout_win_pvp_game_icon'), self._PirateProfilePage__handleChallenge, PLocalizer.ProfilePageChallenge, 0.275)
        self.problemButton = SocialButton(self.mainFrame, (-0.640, 0, -0.13), icons.find('**/moderation'), self._PirateProfilePage__handleProblem, PLocalizer.ProfilePageProblem, 0.074)
        self.ignoreButton = SocialButton(self.mainFrame, (-0.640, 0, -0.0299), icons.find('**/icon_stickman'), self._PirateProfilePage__handleIgnore, PLocalizer.ProfilePageIgnore, (0.050000, 0, 0.0598))
        self.ignoreButtonLabel = DirectLabel(parent = self.ignoreButton.circle, relief = None, text = PLocalizer.ProfilePageIgnore, textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 14, text_pos = (0, 0.050000, 0.0), pos = (0.0, 0.0, 0.0))
        self.loadingLabel = OnscreenText(parent = self.mainFrame, text = PLocalizer.ProfilePageLoading, scale = PiratesGuiGlobals.TextScaleTitleSmall, align = TextNode.ACenter, fg = PiratesGuiGlobals.TextFG2, shadow = PiratesGuiGlobals.TextShadow, pos = (-0.44, -0.282))
        self.locationTextLabel = OnscreenText(parent = self.mainFrame, text = PLocalizer.ProfilePageLocation, scale = PiratesGuiGlobals.TextScaleMed, align = TextNode.ALeft, fg = PiratesGuiGlobals.TextFG2, font = PiratesGlobals.getPirateOutlineFont(), shadow = PiratesGuiGlobals.TextShadow, pos = (-0.685, -0.239))
        self.locationCircleFrame = DirectFrame(parent = self.mainFrame, relief = None, state = DGG.DISABLED, image = topgui.find('**/pir_t_gui_frm_base_circle'), image_scale = 0.325, pos = (-0.65, 0, -0.28498))
        self.locationFrame = DirectFrame(parent = self.locationCircleFrame, relief = None, state = DGG.DISABLED)
        self.islandLabel = OnscreenText(parent = self.mainFrame, text = '', scale = PiratesGuiGlobals.TextScaleMed, align = TextNode.ACenter, fg = PiratesGuiGlobals.TextFG1, font = PiratesGlobals.getPirateOutlineFont(), shadow = PiratesGuiGlobals.TextShadow, mayChange = 1, pos = (-0.465, -0.273))
        self.locationLabel = OnscreenText(parent = self.mainFrame, text = '', scale = PiratesGuiGlobals.TextScaleSmall, align = TextNode.ACenter, fg = PiratesGuiGlobals.TextFG2, shadow = PiratesGuiGlobals.TextShadow, mayChange = 1, pos = (-0.465, -0.31))
        self.goToButton = GuiButton.GuiButton(parent = self.mainFrame, relief = None, image = (chargui.find('**/chargui_text_block_small'), chargui.find('**/chargui_text_block_small_down'), chargui.find('**/chargui_text_block_small_over'), chargui.find('**/chargui_text_block_small')), image_scale = (0.299, 0, 0.200), pos = (-0.25, 0, -0.28000), text = PLocalizer.ProfilePageGoto, text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, -0.01, 0), command = self._PirateProfilePage__handleGoto)
        self.problemFrame = DirectFrame(relief = None, parent = self.mainFrame, state = DGG.NORMAL, sortOrder = 0, image = maingui.find('**/profile_card_moderation'), image_scale = 0.275, text = PLocalizer.ProfilePageProblem, text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (-0.82496, 0.0170, 0), text_shadow = PiratesGuiGlobals.TextShadow)
        self.problemXFrame = GuiButton.GuiButton(parent = self.problemFrame, relief = None, image = box2, image_scale = 0.275, command = self._PirateProfilePage__handleProblemClose)
        self.problemXButton = OnscreenImage(parent = self.problemXFrame, image = x, scale = 0.070, pos = (-0.742, 0, 0.0379))
        self.bootButton = SocialButton(self.problemFrame, (-0.82295, 0, -0.089), icons.find('**/pir_t_gui_gen_boot'), self._PirateProfilePage__handleBoot, PLocalizer.ProfilePageBoot, (0.050000, 0, 0.074))
        self.reportButton = SocialButton(self.problemFrame, (-0.82295, 0, -0.230), icons.find('**/pir_t_gui_gen_report'), self._PirateProfilePage__handleReport, PLocalizer.ProfilePageReport, (0.074, 0, 0.065))
        for frame in [
            self.mainFrame,
            self.skillFrame,
            self.problemFrame]:
            frame.bind(DGG.B1PRESS, self.dragStart)
            frame.bind(DGG.B1RELEASE, self.dragStop)
            frame.bind(DGG.B2PRESS, self.dragStart)
            frame.bind(DGG.B2RELEASE, self.dragStop)
            frame.bind(DGG.B3PRESS, self.dragStart)
            frame.bind(DGG.B3RELEASE, self.dragStop)

        self.pirate = Human.Human()
        self.pirate.ignoreAll()
        self.pirate.mixingEnabled = False
        self.pirate.setPos(0, 2.75, -0.670000)
        self.pirate.setScale(0.2475, 0.22, 0.22)
        self.pirate.setH(188)
        self.masterHuman = [
            MasterHuman.MasterHuman(),
            MasterHuman.MasterHuman()]
        mh = self.masterHuman
        mh[0].style = HumanDNA.HumanDNA('m')
        mh[1].style = HumanDNA.HumanDNA('f')
        mh[0].generateHuman('m')
        mh[1].generateHuman('f')
        mh[0].ignoreAll()
        mh[1].ignoreAll()
        mh[0].stopBlink()
        mh[1].stopBlink()
        self.cm = CardMaker('profileCard')
        self.cm.setFrame(-0.34, 0.348, 0.0149, 0.78800)
        self.buffer = None
        self.lens = PerspectiveLens()
        self.lens.setNear(0.5)
        self.profileCard = None
        self.portraitSceneGraph = NodePath('PortraitSceneGraph')
        self.pirate.reparentTo(self.portraitSceneGraph)
        self.bg = maingui.find('**/background_map')
        self.logo = maingui.find('**/background_logo')
        self.bg.setScale(1.8, 1.60, 1.60)
        self.bg.setPos(2.85, 3, -0.680000)
        self.bg.reparentTo(self.portraitSceneGraph)
        self.logo.reparentTo(self.bg)


    def showProfile(self, profileId, profileName = None):
        if profileId == self.profileId:
            return

        self.profileId = profileId

        handle = base.cr.identifyAvatar(profileId)
        if handle:
            self.profileName = handle.getName()
        elif profileName:
            self.profileName = profileName
        else:
            self.profileName = ''
        self.loadingLabel.show()
        self.pirateLabel['text'] = self.profileName
        self.pirateLabel['fg'] = (0.5, 0.5, 0.5, 1)
        self.guildLabel['text'] = ''
        self.chatLabel['text'] = ''
        self.islandName = ''
        self.locationName = ''
        self.onlineNow = 0
        self.showGoTo = False
        self.islandLabel['text'] = ''
        self.locationLabel['text'] = ''
        self.founderFrame['image'] = None
        self.siegeFrame['image'] = None
        self.locationTextLabel.hide()
        self.locationCircleFrame.hide()
        self.locationFrame.hide()
        self.hpMeter['range'] = 1
        self.hpMeter['value'] = 0
        self.voodooMeter['range'] = 1
        self.voodooMeter['value'] = 0
        self.siege = None
        self.crewButton.disable()
        self.avatarFriendButton.disable()
        self.guildButton.disable()
        self.whisperButton.disable()
        self.challengeButton.disable()
        self.problemButton.disable()
        self.bootButton.disable()
        self.reportButton.disable()
        self.ignoreButton.disable()
        self.ignoreButtonLabel['text'] = ''
        self.notorietyLabel['text'] = PLocalizer.ProfilePageNotoriety % '??'
        self.cannonFrame.meter['value'] = 0
        self.cannonFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.sailingFrame.meter['value'] = 0
        self.sailingFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.cutlassFrame.meter['value'] = 0
        self.cutlassFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.pistolFrame.meter['value'] = 0
        self.pistolFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.dollFrame.meter['value'] = 0
        self.dollFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.daggerFrame.meter['value'] = 0
        self.daggerFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.grenadeFrame.meter['value'] = 0
        self.grenadeFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.staffFrame.meter['value'] = 0
        self.staffFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.potionsFrame.meter['value'] = 0
        self.potionsFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.fishingFrame.meter['value'] = 0
        self.fishingFrame.meter['text'] = PLocalizer.ProfilePageLevel % '??'
        self.goToButton.hide()
        self.problemFrame.hide()
        if localAvatar.getDoId() == self.profileId:
            self.mainFrame.setPos(1.5, 0, -1.0)

        self.mainFrame.show()
        self.skillFrame.show()
        self.pirate.setDNA()
        self.pirate.generateHuman('m', self.masterHuman)
        self.pirate.stopBlink()
        self.pirate.pose('idle', 1)
        lodNode = self.pirate.find('**/+LODNode').node()
        lodNode.forceSwitch(lodNode.getHighestSwitch())
        self.pirate.setColor(0, 0, 0, 1)
        self.pirate.show()
        self.createBuffer()
        
        self.accept('avatarInfoRetrieved', self.fillInAvatarInfo)
        self.accept('avatarShipInfoRetrieved', self.copyAvatarShipInfo)
        self.accept('avatarSkillLevelsRetrieved', self.copySkillLevels)
        self.accept('open_main_window', self.createBuffer)
        self.accept('aspectRatioChanged', self.createBuffer)
        self.accept('close_main_window', self.destroyBuffer)
        base.cr.piratesFriendsManager.d_getAvatarDetails(profileId)

    def hide(self):
        self.mainFrame.hide()
        self.skillFrame.hide()
        self.profileId = None
        self.xFrame['state'] = DGG.NORMAL
        for frame in [
            self.mainFrame,
            self.skillFrame,
            self.problemFrame]:
            frame.bind(DGG.B1PRESS, self.dragStart)
            frame.bind(DGG.B1RELEASE, self.dragStop)
            frame.bind(DGG.B2PRESS, self.dragStart)
            frame.bind(DGG.B2RELEASE, self.dragStop)
            frame.bind(DGG.B3PRESS, self.dragStart)
            frame.bind(DGG.B3RELEASE, self.dragStop)

        if self.profileCard:
            self.profileCard.remove_node()
            self.profileCard = None

        self.destroyBuffer()
        self.ignoreAll()


    def _PirateProfilePage__handleAvatarFriend(self):
        base.localAvatar.guiMgr.handleAvatarFriendInvite(self.profileId, self.profileName)

    def _PirateProfilePage__handleGoto(self):
        if self.TC:
            self.TC.destroy()
            self.TC = None

        self.TC = TeleportConfirm.TeleportConfirm(self.profileId, self.profileName)
        self.TC.setPos(-0.25, 0, -0.149)
        self.hide()


    def _PirateProfilePage__handleTrade(self):
        base.localAvatar.guiMgr.handleTradeInvite(self.profileId, self.profileName)


    def _PirateProfilePage__handleChallenge(self):
        base.localAvatar.guiMgr.handlePVPInvite(self.profileId, self.profileName)


    def _PirateProfilePage__handleWhisper(self):
        base.localAvatar.chatMgr.activateWhisperChat(self.profileId)


    def _PirateProfilePage__handleGuild(self):
        options = base.cr.guildManager.getOptionsFor(self.profileId)
        if options[-1]:
            base.localAvatar.guiMgr.handleGuildMember(self.profileId, self.profileName, localAvatar.guildId, options[0], options[1], options[2])
        else:
            base.localAvatar.guiMgr.handleGuildInvite(self.profileId, self.profileName)


    def _PirateProfilePage__handleRemovedFromGuild(self):
        pass


    def _PirateProfilePage__handleCrew(self):
        base.localAvatar.guiMgr.handleCrewInvite(self.profileId, self.profileName)


    def _PirateProfilePage__handleBoot(self):
        base.localAvatar.guiMgr.handleCrewBoot(self.profileId, self.profileName)


    def _PirateProfilePage__handleIgnore(self):
        base.localAvatar.guiMgr.handleIgnore(self.profileId, self.profileName)


    def _PirateProfilePage__handleReport(self):
        base.localAvatar.guiMgr.handleReport(self.profileId, self.profileName)


    def _PirateProfilePage__handleProblem(self):
        if self.problemFrame.isHidden():
            self.problemFrame.show()
        else:
            self.problemFrame.hide()


    def _PirateProfilePage__handleProblemClose(self):
        self.problemFrame.hide()


    def destroy(self):
        if self.TC:
            self.TC.destroy()
            self.TC = None
            self.ignoreAll()

        self.destroyBuffer()
        self.skillFrame.destroy()
        self.mainFrame.destroy()
        for icon in self.profileIcons:
            icon.remove_node()

        del self.profileIcons
        self.problemButton = None
        self.ignoreButton = None
        self.ignoreButtonLabel = None
        self.reportButton = None
        self.guildButton = None
        self.challengeButton = None
        self.avatarFriendButton = None
        self.whisperButton = None
        self.bootButton = None
        self.crewButton = None
        self.pirate.delete()
        for mh in self.masterHuman:
            mh.delete()

        SocialPage.SocialPage.destroy(self)


    def _PirateProfilePage__newIgnore(self, avId = None):
        ignoreText = PLocalizer.ProfilePageIgnore
        if base.localAvatar.isIgnored(self.profileId):
            ignoreText = PLocalizer.ProfilePageStopIgnore

        self.ignoreButton.circle['helpText'] = ignoreText
        self.determineButtonState()


    def gotOnShard(self, local, onShard, online):
        self.skillButton['state'] = DGG.NORMAL
        self.ignoreButton.enable()

        if local:
            self.avatarFriendButton.disable()
            self.whisperButton.disable()
            self.crewButton.disable()
            self.guildButton.disable()
            self.challengeButton.disable()
            self.problemButton.disable()
            self.bootButton.disable()
            self.reportButton.disable()
            self.ignoreButton.disable()
            return
        
        self.avatarFriendButton.enable()
        
        if not online:
            self.whisperButton.disable()
            self.crewButton.disable()
            self.guildButton.disable()
            self.challengeButton.disable()
            self.problemButton.disable()
            self.bootButton.disable()
            self.reportButton.disable()
            self.ignoreButton.disable()
        else:
            if onShard:
                self.crewButton.enable()
                self.bootButton.enable()
            else:
                self.crewButton.disable()
                self.bootButton.disable()

            self.whisperButton.enable()
            self.guildButton.enable()
            self.challengeButton.enable()
            self.problemButton.enable()
            self.reportButton.enable()
            self.ignoreButton.enable()
        

        if base.localAvatar.isIgnored(self.profileId):
            self.crewButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
            self.avatarFriendButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
            self.guildButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
            self.whisperButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
            self.goToButton.hide()
            self.challengeButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
            return

        if DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.profileId):
            self.crewButton.dim()
            if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                self.crewButton.circle['helpText'] = PLocalizer.ProfilePageRemoveCrew
            else:
                self.crewButton.circle['helpText'] = PLocalizer.ProfilePageLeaveCrew
        else:
            self.crewButton.circle['helpText'] = PLocalizer.ProfilePageCrew
        
        self.testFriendsButtons()
        
        if not DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.profileId):
            if base.localAvatar.isFriend(self.profileId) or base.localAvatar.guiMgr.guildPage.membersList.getMemberByAvId(self.profileId):
                if self.showGoTo:
                    self.goToButton.show()

        inPVP = base.cr.activeWorld.getType() == PiratesGlobals.INSTANCE_PVP
        inSameCrew = DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.profileId)
        profile = base.cr.doId2do.get(self.profileId)
        
        if inPVP or inSameCrew:
            if inPVP:
                self.challengeButton.disable(PLocalizer.PlayerNotChallengeWarning % self.profileName)
            else:
                self.challengeButton.disable(PLocalizer.PlayerSameCrewWarning)

        if not base.localAvatar.getSiegeTeam() or not base.localAvatar.getActiveShipId():
            self.bootButton.disable(PLocalizer.PlayerNotPrivateeringWarning)
        elif not profile or profile.getShipId() != base.localAvatar.getActiveShipId():
            self.bootButton.disable(PLocalizer.PlayerNotOnShipWarning % self.profileName)
        else:
            self.bootButton.enable()
        
        self.checkGuildRank(True)

    def handleNewAvatarInfo(self, id = None, info = None):
        if id and id == self.profileId:
            self.determineButtonState()

    def testFriendsButtons(self):
        if base.localAvatar.isFriend(self.profileId):
            self.avatarFriendButton.circle['helpText'] = PLocalizer.ProfilePageRemoveFriend
            self.avatarFriendButton.enable()
            self.avatarFriendButton.dim()
        else:
            self.avatarFriendButton.circle['helpText'] = PLocalizer.ProfilePageFriend
            self.avatarFriendButton.enable()

    def testOnline(self):
        self.onlineNow = 0
        info = base.cr.identifyAvatar(self.profileId)
        if info:
            self.onlineNow = info.isOnline()
        elif base.cr.doId2do.get(self.profileId):
            self.onlineNow = 1


    def setIslandLabel(self, island, location = None):
        if island:
            self.islandLabel['text'] = island
            self.locationLabel['text'] = ''
        else:
            self.islandLabel['text'] = PLocalizer.ProfilePageOffline
            self.locationLabel['text'] = ''
        self.islandLabel.setScale(PiratesGuiGlobals.TextScaleLarge)
        self.islandLabel.setPos(-0.465, -0.29298)
        self.locationTextLabel.show()


    def determineButtonState(self, extra = None, extra2 = None, extra3 = None):
        self.skillButton['state'] = DGG.NORMAL
        if self.profileId:
            self.checkGuildRank()
            if base.cr.activeWorld:
                pass
            inPVP = base.cr.activeWorld.getType() == PiratesGlobals.INSTANCE_PVP
            inSameCrew = DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.profileId)
            if not base.localAvatar.isIgnored(self.profileId):
                self.testOnline()
                self.testFriendsButtons()
                self.whisperButton.enable()
                if not DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.profileId):
                    if base.localAvatar.isFriend(self.profileId) or base.localAvatar.guiMgr.guildPage.membersList.getMemberByAvId(self.profileId):
                        if self.showGoTo:
                            self.goToButton.show()


                self.problemButton.enable()
                self.checkGuildRank()
                profile = base.cr.doId2do.get(self.profileId)
                crew = localAvatar.guiMgr.crewHUD.crew
                if crew:
                    crewMember = crew.get(self.profileId)
                else:
                    crewMember = False

                if not (self.onlineNow):
                    if not inSameCrew and not crew and not crewMember or not (crewMember[0].hudOnline):
                        self.crewButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
                        self.testFriendsButtons()
                        self.whisperButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
                        self.goToButton.hide()
                        self.challengeButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
                        self.bootButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
                        self.setIslandLabel(None)
                    elif inPVP or inSameCrew:
                        if inPVP:
                            self.challengeButton.disable(PLocalizer.PlayerNotChallengeWarning % self.profileName)
                        else:
                            self.challengeButton.disable(PLocalizer.PlayerSameCrewWarning)

                if not base.localAvatar.getSiegeTeam() or not base.localAvatar.getActiveShipId():
                    self.bootButton.disable(PLocalizer.PlayerNotPrivateeringWarning)
                elif not profile or profile.getShipId() != base.localAvatar.getActiveShipId():
                    self.bootButton.disable(PLocalizer.PlayerNotOnShipWarning % self.profileName)
                else:
                    self.bootButton.enable()
            else:
                self.crewButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
                self.avatarFriendButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
                self.guildButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
                self.whisperButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
                self.goToButton.hide()
                self.challengeButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
                self.bootButton.disable(PLocalizer.PlayerIgnoredWarning % self.profileName)
        else:
            self.crewButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
            self.testFriendsButtons()
            self.whisperButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
            self.goToButton.hide()
            self.challengeButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
            self.bootButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
            self.setIslandLabel(None)


    def checkGuildRank(self, onlyDisable = False):
        self.testOnline()
        if not base.localAvatar.getGuildId():
            self.guildButton.disable(PLocalizer.PlayerNotInGuildWarning)
        elif base.localAvatar.getGuildRank() < GUILDRANK_OFFICER:
            self.guildButton.disable(PLocalizer.PlayerNotGuildOfficerWarning)
        elif base.localAvatar.getGuildRank() == GUILDRANK_VETERAN and base.localAvatar.guiMgr.guildPage.membersList.getMemberByAvId(self.profileId):
            self.guildButton.disable(PLocalizer.PlayerNotGuildRemoveWarning)
        elif not (self.onlineNow) and not base.localAvatar.guiMgr.guildPage.membersList.getMemberByAvId(self.profileId):
            self.guildButton.disable(PLocalizer.PlayerOfflineWarning % self.profileName)
        elif not onlyDisable:
            self.guildButton.enable()



    def handleGuildMemberUpdated(self, avId):
        self.checkGuildRank()


    def constrainToScreen(self):
        height = self.getHeight()
        width = self.getWidth()
        cHeight = self.chain.getHeight()
        pos = self.getPos(aspect2d)
        x = max(min(pos[0], base.a2dRight - width), base.a2dLeft)
        z = max(min(pos[2], base.a2dTop - height), base.a2dBottom + cHeight)
        return self.setPos(aspect2d, x, 0, z)


    def fillInAvatarInfo(self, dna, guildId, guildName, founder, hp, maxHp, voodoo, maxVoodoo, shardId, showGoTo, chat, returnLocation, siege, profileIcon):
        self.loadingLabel.hide()
        self.guildId = guildId
        self.guildName = guildName
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp
        self.voodooMeter['range'] = maxVoodoo
        self.voodooMeter['value'] = voodoo
        self.shardId = shardId
        self.showGoTo = showGoTo
        if self.guildName == 'Null':
            self.guildName = ''

        profile = base.cr.doId2do.get(self.profileId)
        if profile:
            if not isinstance(profile, DistributedPlayerPirate.DistributedPlayerPirate):
                if isinstance(profile, DistributedBandMember.DistributedBandMember):
                    self.profileId = profile.avatarId
                    profile = base.cr.doId2do.get(self.profileId)
                    if profile:
                        self.guildName = profile.getGuildName()
            else:
                self.guildName = profile.getGuildName()

        elif base.cr.guildManager.getBandId(localAvatar.doId) == base.cr.guildManager.getBandId(self.profileId):
            self.guildName = localAvatar.getGuildName()

        if self.guildId == 0:
            self.guildName = ''

        if returnLocation in PLocalizer.LocationNames:
            self.islandName = PLocalizer.LocationNames[returnLocation]
        else:
            self.islandName = ''

        if self.shardId in base.cr.activeDistrictMap:
            self.locationName = base.cr.activeDistrictMap[self.shardId].getName()
        else:
            self.locationName = ''

        self.locationFrame['image'] = self.profileIcons[profileIcon]

        if profileIcon == PiratesGuiGlobals.PROFILE_ICON_LAND:
            self.locationFrame['image_scale'] = 0.065
        elif profileIcon == PiratesGuiGlobals.PROFILE_ICON_OCEAN:
            self.locationFrame['image_scale'] = 0.135
        elif profileIcon == PiratesGuiGlobals.PROFILE_ICON_CANNON:
            self.locationFrame['image_scale'] = 0.085

        self.locationTextLabel.show()
        self.locationCircleFrame.show()
        self.locationFrame.show()
        self.siege = siege

        self.chatLabel['text'] = PLocalizer.PlayerChats[chat]
        self.guildLabel['text'] = '\x01slant\x01%s\x02' % self.guildName
        self.islandLabel['text'] = self.islandName
        self.locationLabel['text'] = '\x01slant\x01%s\x02' % self.locationName
        if self.locationName == '':
            self.islandLabel.setScale(PiratesGuiGlobals.TextScaleLarge)
            self.islandLabel.setPos(-0.465, -0.29298)
        else:
            self.islandLabel.setScale(PiratesGuiGlobals.TextScaleMed)
            self.islandLabel.setPos(-0.465, -0.273)
        self.founder = founder
        av = base.cr.doId2do.get(self.profileId)
        if av:
            if av.getFounder():
                self.founder = 3
            else:
                self.founder = 2

        if self.founder == 3:
            self.founderFrame['image'] = self.goldFounder
            self.pirateLabel['fg'] = (1, 0.800000, 0.4, 1)
        elif self.founder == 2:
            self.pirateLabel['fg'] = (0.4, 0.299, 0.946, 1)

        self.founderFrame['image_scale'] = 0.225
        if self.siege:
            if self.siege == 2:
                self.siegeFrame['image'] = self.spanishFlag
            else:
                self.siegeFrame['image'] = self.frenchFlag
            self.siegeFrame['image_scale'] = 0.0529

        dnaObj = HumanDNA.HumanDNA()
        dnaObj.makeFromNetString(dna)

        self.pirate.setDNA(dna)
        self.pirate.generateHuman(dnaObj.gender, self.masterHuman)
        self.pirate.stopBlink()
        self.pirate.pose('idle', 1)
        lodNode = self.pirate.find('**/+LODNode').node()
        lodNode.forceSwitch(lodNode.getHighestSwitch())
        self.pirate.setColor(1, 1, 1, 1)
        self.createBuffer()

        if localAvatar.getDoId() != self.profileId:
            self.avDisableName = 'disable-%s' % self.profileId
            self.accept(self.avDisableName, self.determineButtonState)
            self.accept('AvatarIgnoreChange', self._PirateProfilePage__newIgnore)
            self.accept('generate-%s' % self.profileId, self.determineButtonState)
            self.accept('AvatarChange', self.determineButtonState)
            self.accept('CrewChange', self.determineButtonState)
            self.accept('kickedFromGuild-%s' % self.profileId, self._PirateProfilePage__handleRemovedFromGuild)
            self.accept(OTPGlobals.AvatarFriendAddEvent, self.handleNewAvatarInfo)
            self.accept(OTPGlobals.AvatarFriendUpdateEvent, self.handleNewAvatarInfo)
            self.accept(OTPGlobals.AvatarFriendRemoveEvent, self.handleNewAvatarInfo)
            self.accept('guildMemberUpdated', self.handleGuildMemberUpdated)

        self.crewButton.disable(example = True)
        self.crewButton.circle['helpText'] = PLocalizer.ProfilePageCrew
        self.avatarFriendButton.disable(example = True)
        self.avatarFriendButton.circle['helpText'] = PLocalizer.ProfilePageFriend
        self.guildButton.disable(example = True)
        self.whisperButton.disable(example = True)
        self.challengeButton.disable(example = True)
        self.problemButton.disable(example = True)
        
        self.determineButtonState()
        self.gotOnShard(localAvatar.getDoId() == self.profileId, self.shardId == localAvatar.getDefaultShard(), self.showGoTo)

    def copyAvatarShipInfo(self, crewState, friendState, guildState):
        self.locationFrame['image'] = self.profileIcons[PiratesGuiGlobals.PROFILE_ICON_OCEAN]
        self.locationFrame['image_scale'] = 0.135
        self.locationTextLabel.show()
        self.locationCircleFrame.show()
        self.locationFrame.show()
        if localAvatar.getDoId() != self.profileId:
            if DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.profileId) and crewState:
                self.showGoTo = True
            elif base.localAvatar.isFriend(self.profileId) and friendState:
                self.showGoTo = True
            elif base.localAvatar.guiMgr.guildPage.membersList.getMemberByAvId(self.profileId) and guildState:
                self.showGoTo = True

            if self.showGoTo:
                self.goToButton.show()

    def copySkillLevels(self, level, cannon, sailing, cutlass, pistol, doll, dagger, grenade, staff, potions, fishing):
        self.level = level
        if self.level > ReputationGlobals.GlobalLevelCap:
            self.level = ReputationGlobals.GlobalLevelCap

        self.cannonLevel = cannon
        if self.cannonLevel > ReputationGlobals.LevelCap:
            self.cannonLevel = ReputationGlobals.LevelCap

        self.sailingLevel = sailing
        if self.sailingLevel > ReputationGlobals.LevelCap:
            self.sailingLevel = ReputationGlobals.LevelCap

        self.cutlassLevel = cutlass
        if self.cutlassLevel > ReputationGlobals.LevelCap:
            self.cutlassLevel = ReputationGlobals.LevelCap

        self.pistolLevel = pistol
        if self.pistolLevel > ReputationGlobals.LevelCap:
            self.pistolLevel = ReputationGlobals.LevelCap

        self.dollLevel = doll
        if self.dollLevel > ReputationGlobals.LevelCap:
            self.dollLevel = ReputationGlobals.LevelCap

        self.daggerLevel = dagger
        if self.daggerLevel > ReputationGlobals.LevelCap:
            self.daggerLevel = ReputationGlobals.LevelCap

        self.grenadeLevel = grenade
        if self.grenadeLevel > ReputationGlobals.LevelCap:
            self.grenadeLevel = ReputationGlobals.LevelCap

        self.staffLevel = staff
        if self.staffLevel > ReputationGlobals.LevelCap:
            self.staffLevel = ReputationGlobals.LevelCap

        self.potionsLevel = potions
        if self.potionsLevel > ReputationGlobals.MinigameLevelCap:
            self.potionsLevel = ReputationGlobals.MinigameLevelCap

        self.fishingLevel = fishing
        if self.fishingLevel > ReputationGlobals.MinigameLevelCap:
            self.fishingLevel = ReputationGlobals.MinigameLevelCap

        self.notorietyLabel['text'] = PLocalizer.ProfilePageNotoriety % self.level
        self.cannonFrame.meter['value'] = self.cannonLevel
        self.cannonFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.cannonLevel
        self.sailingFrame.meter['value'] = self.sailingLevel
        self.sailingFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.sailingLevel
        if cutlass:
            self.cutlassFrame.meter['value'] = self.cutlassLevel
            self.cutlassFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.cutlassLevel
            self.cutlassFrame.show()
        else:
            self.cutlassFrame.hide()
        if pistol:
            self.pistolFrame.meter['value'] = self.pistolLevel
            self.pistolFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.pistolLevel
            self.pistolFrame.show()
        else:
            self.pistolFrame.hide()
        if doll:
            self.dollFrame.meter['value'] = self.dollLevel
            self.dollFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.dollLevel
            self.dollFrame.show()
        else:
            self.dollFrame.hide()
        if dagger:
            self.daggerFrame.meter['value'] = self.daggerLevel
            self.daggerFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.daggerLevel
            self.daggerFrame.show()
        else:
            self.daggerFrame.hide()
        if grenade:
            self.grenadeFrame.meter['value'] = self.grenadeLevel
            self.grenadeFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.grenadeLevel
            self.grenadeFrame.show()
        else:
            self.grenadeFrame.hide()
        if staff:
            self.staffFrame.meter['value'] = self.staffLevel
            self.staffFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.staffLevel
            self.staffFrame.show()
        else:
            self.staffFrame.hide()
        self.potionsFrame.meter['value'] = self.potionsLevel
        self.potionsFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.potionsLevel
        self.fishingFrame.meter['value'] = self.fishingLevel
        self.fishingFrame.meter['text'] = PLocalizer.ProfilePageLevel % self.fishingLevel

    def toggleSkillFrame(self):
        if self.skillFrameIval:
            self.skillFrameIval.pause()

        if self.skillFrameClosed:
            self.skillFrameIval = LerpPosInterval(self.skillFrame, 0.200, pos = (self.skillFrame.getX() + 0.44, 0, self.skillFrame.getZ()))
            self.skillFrameClosed = False
        else:
            self.skillFrameIval = LerpPosInterval(self.skillFrame, 0.200, pos = (self.skillFrame.getX() - 0.44, 0, self.skillFrame.getZ()))
            self.skillFrameClosed = True
        self.skillFrameIval.start()


    def dragStart(self, event):
        taskMgr.remove(self.taskName('dragTask'))
        vWidget2render2d = self.mainFrame.getPos(render2d)
        vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
        editVec = Vec3(vWidget2render2d - vMouse2render2d)
        task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
        task.editVec = editVec


    def dragTask(self, task):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d + task.editVec
            self.mainFrame.setPos(render2d, newPos)
            newPos = self.mainFrame.getPos(aspect2d)
            x = newPos[0]
            y = newPos[1]
            z = newPos[2]
            y = 0
            x = min(base.a2dRight + 0.5, max(base.a2dLeft + 0.5, x))
            z = min(base.a2dTop, max(base.a2dBottom, z))
            self.mainFrame.setPos(aspect2d, x, y, z)

        return Task.cont


    def dragStop(self, event):
        taskMgr.remove(self.taskName('dragTask'))


    def createBuffer(self):
        self.destroyBuffer()
        if self.mainFrame.isHidden():
            return None

        self.buffer = base.win.makeTextureBuffer('par', 256, 256)
        self.buffer.setOneShot(True)
        self.cam = base.makeCamera(win = self.buffer, scene = self.portraitSceneGraph, clearColor = Vec4(1), lens = self.lens)
        self.cam.node().getDisplayRegion(0).setIncompleteRender(False)
        self.cam.reparentTo(self.portraitSceneGraph)
        if self.profileCard:
            self.profileCard.remove_node()

        tex = self.buffer.getTexture()
        self.profileCard = NodePath(self.cm.generate())
        self.profileCard.setTexture(tex, 1)
        self.profileCard.reparentTo(self.pirateFrame)


    def destroyBuffer(self):
        if self.buffer:
            base.graphicsEngine.removeWindow(self.buffer)
            self.buffer = None
            self.cam.remove_node()
            self.cam = None
