from panda3d.core import BitMask32, TextNode
QuietZone = 1
UberZone = 2
WallBitmask = BitMask32(1)
FloorBitmask = BitMask32(2)
CameraBitmask = BitMask32(4)
CameraTransparentBitmask = BitMask32(8)
SafetyNetBitmask = BitMask32(512)
SafetyGateBitmask = BitMask32(1024)
GhostBitmask = BitMask32(2048)
PathFindingBitmask = BitMask32.bit(29)
OriginalCameraFov = 52.0
DefaultCameraFov = 52.0
DefaultCameraFar = 400.0
DefaultCameraNear = 1.0

FriendChat = 1
CommonChat = 1
SuperChat = 2
MaxCustomMessages = 25
SPInvalid = 0
SPHidden = 1
SPRender = 2
SPDynamic = 5
DisconnectUnknown = 0
DisconnectBookExit = 1
DisconnectCloseWindow = 2
DisconnectPythonError = 3
DisconnectSwitchShards = 4
DisconnectGraphicsError = 5
DisconnectReasons = {DisconnectUnknown: 'unknown',
 DisconnectBookExit: 'book exit',
 DisconnectCloseWindow: 'closed window',
 DisconnectPythonError: 'python error',
 DisconnectSwitchShards: 'switch shards',
 DisconnectGraphicsError: 'graphics error'}
DatabaseDialogTimeout = 20.0
DatabaseGiveupTimeout = 45.0
FloorOffset = 0.025
AvatarDefaultRadius = 1
InterfaceFont = None
InterfaceFontPath = None
SignFont = None
SignFontPath = None
NametagFonts = {}
NametagFontPaths = {}
DialogClass = None
GlobalDialogClass = None

def getInterfaceFont():
    global InterfaceFontPath
    global InterfaceFont
    if InterfaceFont == None:
        if InterfaceFontPath == None:
            InterfaceFont = TextNode.getDefaultFont()
        else:
            InterfaceFont = loader.loadFont(InterfaceFontPath, lineHeight=1.0)
    return InterfaceFont


def setInterfaceFont(path):
    global InterfaceFontPath
    global InterfaceFont
    InterfaceFontPath = path
    InterfaceFont = None


def getSignFont():
    global SignFont
    global SignFontPath
    if SignFont == None:
        if SignFontPath == None:
            InterfaceFont = TextNode.getDefaultFont()
            SignFont = TextNode.getDefaultFont()
        else:
            SignFont = loader.loadFont(SignFontPath, lineHeight=1.0)
    return SignFont


def setSignFont(path):
    global SignFontPath
    SignFontPath = path


def getNametagFont(index):
    global NametagFontPaths
    global NametagFonts
    if not index in NametagFonts or NametagFonts[index] == None:
        if not index in NametagFontPaths or NametagFontPaths[index] == None:
            InterfaceFont = TextNode.getDefaultFont()
            NametagFonts[index] = TextNode.getDefaultFont()
        else:
            NametagFonts[index] = loader.loadFont(NametagFontPaths[index], lineHeight=1.0)
    return NametagFonts[index]


def setNametagFont(index, path):
    NametagFontPaths[index] = path


def getDialogClass():
    global DialogClass
    if DialogClass == None:
        from otp.otpgui.OTPDialog import OTPDialog
        DialogClass = OTPDialog
    return DialogClass


def getGlobalDialogClass():
    global GlobalDialogClass
    if DialogClass == None:
        from otp.otpgui.OTPDialog import GlobalDialog
        GlobalDialogClass = GlobalDialog
    return GlobalDialogClass


def setDialogClasses(dialogClass, globalDialogClass):
    global DialogClass
    global GlobalDialogClass
    DialogClass = dialogClass
    GlobalDialogClass = globalDialogClass


NetworkLatency = 1.0
STAND_INDEX = 0
WALK_INDEX = 1
RUN_INDEX = 2
REVERSE_INDEX = 3
STRAFE_LEFT_INDEX = 4
STRAFE_RIGHT_INDEX = 5
ToonSpeedFactor = 1.25
ToonForwardSpeed = 16.0 * ToonSpeedFactor
ToonJumpForce = 24.0
ToonReverseSpeed = 8.0 * ToonSpeedFactor
ToonRotateSpeed = 80.0 * ToonSpeedFactor
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0
ThinkPosHotkey = 'shift-f1'
PlaceMarkerHotkey = 'f2'
FriendsListHotkey = 'f7'
StickerBookHotkey = 'f8'
OptionsPageHotkey = 'escape'
ScreenshotHotkey = 'f9'
SynchronizeHotkey = 'shift-f6'
QuestsHotkeyOn = 'end'
QuestsHotkeyOff = 'end-up'
InventoryHotkeyOn = 'home'
InventoryHotkeyOff = 'home-up'
MapHotkeyOn = 'delete'
MapHotkeyOff = 'delete-up'
PrintCamPosHotkey = 'f12'
GlobalDialogColor = (1,
 1,
 0.75,
 1)
DefaultBackgroundColor = (0.3,
 0.3,
 0.3,
 1)
RandomButton = 'Randomize'
TypeANameButton = 'Type Name'
PickANameButton = 'Pick-A-Name'
NoPunctuation = "You can't use punctuation marks in your name!"
PeriodOnlyAfterLetter = 'You can use a period in your name, but only after a letter.'
ApostropheOnlyAfterLetter = 'You can use an apostrophe in your name, but only after a letter.'
NoNumbersInTheMiddle = 'Numeric digits may not appear in the middle of a word.'
ThreeWordsOrLess = 'Your name must be three words or fewer.'
GuildUpdateMembersEvent = 'guildUpdateMembersEvent'
GuildRejectInviteEvent = 'guildRejectInviteEvent'
AvatarFriendAddEvent = 'avatarFriendAddEvent'
AvatarFriendUpdateEvent = 'avatarFriendUpdateEvent'
AvatarFriendRemoveEvent = 'avatarFriendRemoveEvent'
AvatarFriendConsideringEvent = 'avatarFriendConsideringEvent'
AvatarFriendInvitationEvent = 'avatarFriendInvitationEvent'
AvatarFriendRejectInviteEvent = 'avatarFriendRejectInviteEvent'
AvatarFriendRejectRemoveEvent = 'avatarFriendRejectRemoveEvent'
AvatarSlotAvailable = -1

from otp.ai.MagicWordGlobal import *

CHAT_CHANNELS = {
 0: 0,
 1: MINIMUM_MAGICWORD_ACCESS
}
CHAT_CHANNEL_COLORS = {
 0: (1, 1, 1, 1),
 1: (1, 1, 0, 1)
}

MAX_TF_TRIES = 5
TF_COOLDOWN_SECS = 60 * 60 * 24
TF_EXPIRE_SECS = 3 * 60 * 60 * 24
TF_COOLDOWN = 0
TF_UNKNOWN_SECRET = 1
TF_SELF_SECRET = 2
TF_FRIENDS_LIST_FULL_YOU = 3
TF_FRIENDS_LIST_FULL_HIM = 4
TF_ALREADY_FRIENDS = 5
TF_ALREADY_FRIENDS_NAME = 6
TF_SUCCESS = 7

GUILD_COST = 500
RECOVERY_TIME = 259200