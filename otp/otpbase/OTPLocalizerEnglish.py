from panda3d.core import Light, TextProperties, TextPropertiesManager
import string
from otp.otpbase.OTPLocalizerEnglishProperty import *
lCancel = 'Cancel'
lClose = 'Close'
lOK = 'OK'
lNext = 'Next'
lNo = 'No'
lQuit = 'Quit'
lYes = 'Yes'
Cog = 'Cog'
Cogs = 'Cogs'
DialogOK = lOK
DialogCancel = lCancel
DialogYes = lYes
DialogNo = lNo
DialogDoNotShowAgain = 'Do Not\nShow Again'
WhisperNoLongerFriend = '%s left your friends list.'
WhisperNowSpecialFriend = '%s is now your True Friend!'
WhisperComingToVisit = '%s is coming to visit you.'
WhisperFailedVisit = '%s tried to visit you.'
WhisperTargetLeftVisit = '%s has gone somewhere else. Try again!'
WhisperGiveupVisit = "%s couldn't find you because you're moving around!"
WhisperIgnored = 'I am ignoring you!'
TeleportGreeting = 'Hi, %s.'
WhisperUnavailable = 'That player is no longer available for whispers.'
DialogSpecial = 'ooo'
DialogExclamation = '!'
DialogQuestion = '?'
ChatInputNormalSayIt = 'Say It'
ChatInputNormalCancel = lCancel
ChatInputNormalWhisper = 'Whisper'
ChatInputWhisperLabel = 'To %s'
SCEmoteNoAccessMsg = 'You do not have access\nto this emotion yet.'
SCEmoteNoAccessOK = lOK
ChatGarblerDefault = ['yarr', 'arrr', 'garr', 'arrrrr']
ChatManagerChat = 'Chat'
ChatManagerWhisperTo = 'Whisper to:'
ChatManagerWhisperToName = 'Whisper To:\n%s'
ChatManagerCancel = lCancel
ChatManagerWhisperOffline = '%s is offline.'
OpenChatWarning = 'To become True Friends with somebody, click on them, and select "True Friends" from the detail panel.\n\nSpeedChat Plus can also be enabled, which allow users to chat by typing words found in the Disney SpeedChat Plus dictionary.\n\nTo activate these features or to learn more, exit Toontown and then click on Membership and select Manage Account.  Log in to edit your "Community Settings."\n\nIf you are under 18, you need a Parent Account to manage these settings.'
OpenChatWarningOK = lOK
NoSecretChatWarningTitle = 'Parental Controls'
NoSecretChatWarning = 'To chat with a friend, the True Friends feature must first be enabled.  Kids, have your parent visit the Toontown Web site to learn about True Friends.'
RestrictedSecretChatWarning = 'To get or enter a True Friend Code, log in with the Parent Account. You can disable this prompt by changing your True Friends options.'
NoSecretChatWarningOK = lOK
NoSecretChatWarningCancel = lCancel
NoSecretChatWarningWrongPassword = "That's not the correct Parent Account.  Please log in with the Parent Account that is linked to this account."
NoSecretChatAtAllTitle = 'Open Chat With True Friends'
NoSecretChatAtAll = 'Open Chat with True Friends allows real-life friends to chat openly with each other by means of a True Friend Code that must be shared outside of the game.\n\nTo activate these features or to learn more, exit Toontown and then click on Membership and select Manage Account. Log in to edit your "Community Settings." If you are under 18, you need a Parent Account to manage these settings.'
NoSecretChatAtAllAndNoWhitelistTitle = 'Chat button'
NoSecretChatAtAllAndNoWhitelist = 'You can use the blue Chat button to communicate with other Toons by using Speechat Plus or Open Chat with True Friends.\n\nSpeedchat Plus is a form of type chat that allows users to communicate by using the Disney SpeedChat Plus dictionary.\n\nOpen Chat with True Friends allows real-life friends to chat openly with each other by means of a True Friend Code that must be shared outside of the game.\n\nTo activate these features or to learn more, exit Toontown and then click on Membership and select Manage Account.  Log in to edit your "Community Settings." If you are under 18, you need a Parent Account to manage these settings.'
NoSecretChatAtAllOK = lOK
ChangeSecretFriendsOptions = 'Change True Friends Options'
ChangeSecretFriendsOptionsWarning = '\nPlease enter the Parent Account Password to change your True Friends options.'
WhisperToFormat = 'To %s %s'
WhisperToFormatName = 'To %s'
WhisperFromFormatName = '%s whispers'
ThoughtOtherFormatName = '%s thinks'
ThoughtSelfFormatName = 'You think'


propertyManager = TextPropertiesManager.getGlobalPtr()

shadow = TextProperties()
shadow.setShadow(-0.025, -0.025)
shadow.setShadowColor(0, 0, 0, 1)
italic = TextProperties()
italic.setSlant(0.3)
small = TextProperties()
small.setGlyphScale(0.8)
bold = TextProperties()
bold.setGlyphScale(1.1)
propertyManager.setProperties('shadow', shadow)
propertyManager.setProperties('italic', italic)
propertyManager.setProperties('small', small)
propertyManager.setProperties('bold', bold)

TextColors = {
 'red': (1, 0, 0, 1),
 'green': (0, 1, 0, 1),
 'blue': (0, 0, 1, 1),
 'yellow': (1, 1, 0, 1),
 'purple': (1, 0, 1, 1),
 'cyan': (0, 1, 1, 1),
 'midgreen': (0.2, 1, 0.2, 1),
 'white': (1, 1, 1, 1),
 'black': (0, 0, 0, 1),
 'grey': (0.5, 0.5, 0.5, 1),
 'gold': (1, 0.84, 0, 1),
 'brown': (0.8, 0.4, 0, 1),
 'orange': (1, 0.54, 0, 1),
 'darkGray': (0.2, 0.2, 0.2, 1),
 'darkPink': (0.75, 0.5, 0.85, 1),
 'darkGreen': (0, 0.45, 0, 1),
 'darkRed': (0.85, 0.15, 0.15, 1),
 'skillRed': (0.5, 0, 0, 1),
 'lightBlue': (0.4, 0.6, 1, 1),
 'skyBlue': (0, 0.6, 1, 1),
 'waterGreen': (0.2, 0.6, 0.3, 1),
 'maroon': (0.5, 0, 0, 1),
 'lightGold': (0.98, 0.98, 0.82, 1),
 'beige': (1, 0.95, 0.7, 1),           # Light yellow
 'amber': (1, 0.75, 0, 1),             # Orange
 'amaranth': (0.9, 0.15, 0.3, 1),      # Pink
 'androidGreen': (0.65, 0.75, 0.2, 1), # Green
 'caribbeanGreen': (0, 0.8, 0.6, 1),   # Turquoise-green
 'azure': (0, 0.5, 1, 1),              # Blue
 'cobalt': (0, 0.3, 0.65, 1),          # Cobalt-blue
 'forestGreen': (0.15, 0.8, 0.15, 1)   # Forest-green
}
DynamicColors = []
DynamicFonts = []

for name, color in TextColors.iteritems():
    property = TextProperties()
    property.setTextColor(*color)
    propertyManager.setProperties(name, property)
    property.setShadow(-0.025, -0.025)
    property.setShadowColor(0, 0, 0, 1)
    propertyManager.setProperties(name + 'Shadow', property)

def getPropertiesForFont(font):
    if font in DynamicFonts:
        return 'dynamicFont%d' % DynamicFonts.index(font)
    
    name = 'dynamicFont%d' % len(DynamicFonts)
    property = TextProperties()
    property.setFont(font)
    propertyManager.setProperties(name, property)
    DynamicFonts.append(font)

    return name

def getPropertiesForColor(color):
    if color in TextColors.values():
        return TextColors.keys()[TextColors.values().index(color)]
    if color in DynamicColors:
        return 'dynamic%d' % DynamicColors.index(color)

    name = 'dynamic%d' % len(DynamicColors)
    property = TextProperties()
    property.setTextColor(*color)
    propertyManager.setProperties(name, property)
    DynamicColors.append(color)
    
    return name

MultiPageTextFrameNext = lNext
MultiPageTextFramePrev = 'Previous'
MultiPageTextFramePage = 'Page %s/%s'
GuiScreenToontownUnavailable = 'The server appears to be temporarily unavailable, still trying...'
GuiScreenCancel = lCancel
CRConnecting = 'Connecting...'
CRNoConnectTryAgain = 'Could not connect to %s:%s. Try again?'
CRMissingGameRootObject = 'Missing some root game objects.  (May be a failed network connection).\n\nTry again?'
CRNoDistrictsTryAgain = 'No Districts are available. Try again?'
CRRejectRemoveAvatar = 'The avatar was not able to be deleted, try again another time.'
CRLostConnection = 'Your internet connection to the servers has been unexpectedly broken.'
CRBootedReasons = {1: 'An unexpected problem has occurred.  Your connection has been lost, but you should be able to connect again and go right back into the game.',
 100: 'You have been disconnected because someone else just logged in using your account on another computer.',
 122: 'There has been an unexpected problem logging you in.  Please contact customer support.',
 124: 'Your installed files are out of date.  Please launch the game from the official launcher so that it can install updates.  If you continue to get this error, contact support.',
 125: 'Your installed files appear to be invalid.  Please use the Play button on the official website to run.',
 126: 'You are not authorized to use administrator privileges.',
 151: 'You have been logged out by an administrator working on the servers.',
 152: "You were banned by a Moderator for:\n\n%(reason)s\n\nPlease contact us via the forums or the Discord channel for more information.",
 153: 'The district you were playing on has been reset.  Everyone who was playing on that district has been disconnected.  However, you should be able to connect again and go right back into the game.',
 154: 'Pirates Online Retribution is temporarily closing for a scheduled maintenance.\nFor more information, please visit the Pirates Online Retribution website.',
 155: 'You were kicked by a Moderator. Behave next time!\n\n%(reason)s',
 166: 'You were disconnected to prevent a district reset.'}
CRBootedReasonUnknownCode = 'An unexpected problem has occurred (error code %s).  Your connection has been lost, but you should be able to connect again and go right back into the game.'
CRTryConnectAgain = '\n\nTry to connect again?'
CRToontownUnavailable = 'The server appears to be temporarily unavailable, still trying...'
CRToontownUnavailableCancel = lCancel
CRNameCongratulations = 'CONGRATULATIONS!!'
CRNameAccepted = 'Your name has been\napproved by the Toon Council.\n\nFrom this day forth\nyou will be named\n"%s"'
AfkForceAcknowledgeMessage = 'Your toon got sleepy and went to bed.'
CREnteringToontown = 'Entering...'
DialogSpecial = 'ooo'
DialogExclamation = '!'
DialogQuestion = '?'
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20
GlobalSpeedChatName = 'SpeedChat'
FriendSecretIntro = "If you are playing Disney's Toontown Online with someone you know in the real world, you can become True Friends.  You can chat using the keyboard with your True Friends.  Other Toons won't understand what you're saying.\n\nYou do this by getting a True Friend Code.  Tell the True Friend Code to your friend, but not to anyone else.  When your friend types in your True Friend Code on his or her screen, you'll be True Friends in Toontown!"
FriendSecretGetSecret = 'Get a True Friend Code'
FriendSecretEnterSecret = 'If you have a True Friend Code from someone you know, type it here.'
FriendSecretOK = lOK
FriendSecretEnter = 'Enter True Friend Code'
FriendSecretCancel = lCancel
FriendSecretGettingSecret = 'Getting True Friend Code. . .'
FriendSecretGotSecret = "Here is your new True Friend Code.  Be sure to write it down!\n\nYou may give this True Friend Code to one person only.  Once someone types in your True Friend Code, it will not work for anyone else.  If you want to give a True Friend Code to more than one person, get another True Friend Code.\n\nThe True Friend Code will only work for the next two days.  Your friend will have to type it in before it goes away, or it won't work.\n\nYour True Friend Code is:"
FriendSecretTooMany = "Sorry, you can't have any more True Friend Codes today.  You've already had more than your fair share!\n\nTry again tomorrow."
FriendSecretTryingSecret = 'Trying True Friend Code. . .'
FriendSecretEnteredSecretSuccess = 'You are now True Friends with %s!'
FriendSecretTimeOut = 'Sorry, secrets are not working right now.'
FriendSecretEnteredSecretUnknown = "That's not anyone's True Friend Code.  Are you sure you spelled it correctly?\n\nIf you did type it correctly, it may have expired.  Ask your friend to get a new True Friend Code for you (or get a new one yourself and give it to your friend)."
FriendSecretEnteredSecretFull = "You can't be friends with %s because one of you has too many friends on your friends list."
FriendSecretEnteredSecretFullNoName = "You can't be friends because one of you has too many friends on your friends list."
FriendSecretEnteredSecretSelf = 'You just typed in your own True Friend Code!  Now no one else can use that True Friend Code.'
FriendSecretEnteredSecretWrongProduct = "You have entered the wrong type of True Friend Code.\nThis game uses codes that begin with '%s'."
FriendSecretNowFriends = 'You are now True Friends with %s!'
FriendSecretNowFriendsNoName = 'You are now True Friends!'
FriendSecretDetermineSecret = 'What type of True Friend would you like to make?'
FriendSecretDetermineSecretAvatar = 'Avatar'
FriendSecretDetermineSecretAvatarRollover = 'A friend only in this game'
FriendSecretDetermineSecretAccount = 'Account'
FriendSecretDetermineSecretAccountRollover = 'A friend across the Disney.com network'
GuildMemberTitle = 'Member Options'
GuildMemberPromote = 'Make Officer'
GuildMemberPromoteInvite = 'Make Veteran'
GuildMemberDemoteInvite = 'Demote to Veteran'
GuildMemberGM = 'Make Guildmaster'
GuildMemberGMConfirm = 'Confirm'
GuildMemberDemote = 'Demote to Member'
GuildMemberKick = 'Remove Member'
GuildMemberCancel = lCancel
GuildMemberOnline = 'has come online.'
GuildMemberOffline = 'has gone offline.'
GuildPrefix = '(G):'
GuildNewMember = 'New Guild Member'
GuildMemberUnknown = 'Unknown'
GuildMemberGMMessage = 'Warning! Would you like to give up leadership of your guild and make %s your guild master?\n\nYou will become an officer'
GuildInviteeOK = lOK
GuildInviteeNo = lNo
GuildInviteeInvitation = '%s is inviting you to join %s.'
GuildRedeemErrorInvalidToken = 'Sorry, that code is invalid. Please try again.'
GuildRedeemErrorGuildFull = 'Sorry, this guild has too many members already.'
FriendInviteeTooManyFriends = '%s would like to be your friend, but you already have too many friends on your list!'
FriendInviteeInvitation = '%s would like to be your friend.'
FriendNotifictation = '%s is now your friend.'
FriendInviteeOK = lOK
FriendInviteeNo = lNo
You = 'You'
LowerYou = 'you'
GuildRankNames = {
    1: 'Member',
    2: 'Officer',
    3: 'Guildmaster',
    4: 'Veteran'
}
GuildKicksMaxed = 'Officers are only allowed to remove five guild members per day.'
GuildInviterWentAway = '%s is no longer present.'
GuildInviterAlready = '%s is already in a guild.'
GuildInviterBusy = '%s is busy right now.'
GuildInviterNotYet = 'Invite %s to join your guild?'
GuildInviterCheckAvailability = 'Inviting %s to join your guild.'
GuildInviterOK = lOK
GuildInviterNo = lNo
GuildInviterCancel = lCancel
GuildInviterYes = lYes
GuildInviterTooFull = 'Guild has reached maximum size.'
GuildInviterNo = lNo
GuildInviterClickToon = 'Click on the pirate you would like to invite.'
GuildInviterTooMany = 'This is a bug'
GuildInviterNotAvailable = '%s is busy right now; try again later.'
GuildInviterGuildSaidNo = '%s has declined your guild invitation.'
GuildInviterAlreadyInvited = '%s has already been invited.'
GuildInviterEndGuildship = 'Remove %s from the guild?'
GuildInviterFriendsNoMore = '%s has left the guild.'
GuildInviterSelf = 'You are already in the guild!'
GuildInviterIgnored = '%s is ignoring you.'
GuildInviterAsking = 'Asking %s to join the guild.'
GuildInviterFriendKickedOutSelf = 'You have left the guild.'
GuildInviterGuildSaidYes = '%s has joined the guild!'
GuildInviterFriendKickedOut = '%s has kicked out %s from the Guild.'
GuildInviterFriendKickedOutP = '%s have kicked out %s from the Guild.'
GuildInviterFriendInvited = '%s has invited %s to the Guild.'
GuildInviterFriendInvitedP = '%s have invited %s to the Guild.'
GuildInviterFriendPromoted = '%s has promoted %s to the rank of %s.'
GuildInviterFriendPromotedP = '%s have promoted %s to the rank of %s.'
GuildInviterFriendDemoted = '%s has demoted %s to the rank of %s.'
GuildInviterFriendDemotedP = '%s have demoted %s to the rank of %s.'
GuildInviterFriendPromotedGM = '%s has named %s as the new %s'
GuildInviterFriendPromotedGMP = '%s have named %s as the new %s'
GuildInviterFriendDemotedGM = '%s has been named by %s as the new GuildMaster who became the rank of %s'
GuildInviterFriendDemotedGMP = '%s have been named by %s as the new GuildMaster who beaome the rank of %s'
FriendOnline = 'has come online.'
FriendOffline = 'has gone offline.'
FriendInviterOK = lOK
FriendInviterCancel = lCancel
FriendInviterStopBeingFriends = 'Stop being friends'
FriendInviterConfirmRemove = 'Remove'
FriendInviterYes = lYes
FriendInviterNo = lNo
FriendInviterClickToon = 'Click on the toon you would like to make friends with.'
FriendInviterTooMany = 'You have too many friends on your list to add another one now. You will have to remove some friends if you want to make friends with %s.'
FriendInviterToonTooMany = 'You have too many toon friends on your list to add another one now. You will have to remove some toon friends if you want to make friends with %s.'
FriendInviterNotYet = 'Would you like to make friends with %s?'
FriendInviterCheckAvailability = 'Seeing if %s is available.'
FriendInviterNotAvailable = '%s is busy right now; try again later.'
FriendInviterCantSee = 'This only works if you can see %s.'
FriendInviterNotOnline = 'This only works if %s is online'
FriendInviterNotOpen = '%s does not have open chat, use secrets to make friends'
FriendInviterWentAway = '%s went away.'
FriendInviterAlready = '%s is already your friend.'
FriendInviterAlreadyInvited = '%s has already been invited.'
FriendInviterAskingCog = 'Asking %s to be your friend.'
FriendInviterAskingPet = '%s jumps around, runs in circles and licks your face.'
FriendInviterAskingMyPet = '%s is already your BEST friend.'
FriendInviterEndFriendship = 'Are you sure you want to stop being friends with %s?'
FriendInviterFriendsNoMore = '%s is no longer your friend.'
FriendInviterSelf = "You are already 'friends' with yourself!"
FriendInviterIgnored = '%s is ignoring you.'
FriendInviterAsking = 'Asking %s to be your friend.'
FriendInviterFriendSaidYes = 'You are now friends with %s!'
FriendInviterFriendSaidNo = '%s said no, thank you.'
FriendInviterFriendSaidNoNewFriends = "%s isn't looking for new friends right now."
FriendInviterOtherTooMany = '%s has too many friends already!'
FriendInviterMaybe = '%s was unable to answer.'
FriendInviterDown = 'Cannot make friends now.'
TalkGuild = 'G'
TalkParty = 'P'
TalkPVP = 'PVP'
AntiSpamInChat = '***Spamming***'
IgnoreConfirmOK = lOK
IgnoreConfirmCancel = lCancel
IgnoreConfirmYes = lYes
IgnoreConfirmNo = lNo
IgnoreConfirmNotYet = 'Would you like to ignore %s?'
IgnoreConfirmAlready = 'You are already ignoring %s.'
IgnoreConfirmSelf = 'You cannot ignore yourself!'
IgnoreConfirmNewIgnore = 'You are ignoring %s.'
IgnoreConfirmEndIgnore = 'You are no longer ignoring %s.'
IgnoreConfirmRemoveIgnore = 'Stop ignoring %s?'
EmoteList = ['Wave',
 'Happy',
 'Sad',
 'Angry',
 'Sleepy',
 'Shrug',
 'Dance',
 'Think',
 'Bored',
 'Applause',
 'Cringe',
 'Confused',
 'Belly Flop',
 'Bow',
 'Banana Peel',
 'Resistance Salute',
 'Laugh',
 lYes,
 lNo,
 lOK,
 'Surprise',
 'Cry',
 'Delighted',
 'Furious',
 'Laugh']
EmoteWhispers = ['%s waves.',
 '%s is happy.',
 '%s is sad.',
 '%s is angry.',
 '%s is sleepy.',
 '%s shrugs.',
 '%s dances.',
 '%s thinks.',
 '%s is bored.',
 '%s applauds.',
 '%s cringes.',
 '%s is confused.',
 '%s does a belly flop.',
 '%s bows to you.',
 '%s slips on a banana peel.',
 '%s gives the resistance salute.',
 '%s laughs.',
 "%s says '" + lYes + "'.",
 "%s says '" + lNo + "'.",
 "%s says '" + lOK + "'.",
 '%s is surprised.',
 '%s is crying.',
 '%s is delighted.',
 '%s is furious.',
 '%s is laughing.']
SpeedChatStaticTextCommon = {1: lYes,
 2: lNo,
 3: lOK,
 4: 'SPEEDCHAT PLUS'}
SpeedChatStaticTextPirates = {50001: 'Aye',
 50002: 'Nay',
 50003: 'Yes',
 50004: 'No',
 50005: 'Ok',
 50100: 'Gangway!',
 50101: 'Blimey!',
 50102: 'Well blow me down!',
 50103: 'Walk the plank!',
 50104: 'Dead men tell no tales....',
 50105: 'Shiver me timbers!',
 50106: "Salty as a Kraken's kiss.",
 50107: 'Treasure be the measure of our pleasure!',
 50108: "I don't fear death - I attune it.",
 50700: 'Ahoy!',
 50701: 'Ahoy, mate!',
 50702: 'Yo-Ho-Ho',
 50703: 'Avast!',
 50704: 'Hey Bucko.',
 50800: 'Until next time.',
 50801: 'May fair winds find ye.',
 50802: 'Godspeed.',
 50900: 'How are ye, mate?',
 50901: '',
 51000: "It's like the sky is raining gold doubloons!",
 51001: 'May a stiff wind be at our backs, the sun on our faces and our cannons fire true!',
 51100: 'I be sailing some rough waters today.',
 51200: 'Me apologies, mate.',
 51201: 'Sorry.',
 51202: 'Sorry, I was busy before.',
 51203: 'Sorry, I already have plans.',
 51204: "Sorry, I don't need to do that.",
 51300: 'Attack the weakest one!',
 51301: 'Attack the strongest one!',
 51302: 'Attack me target!',
 51303: 'I be needing help!',
 51304: "I can't do any damage!",
 51305: 'I think we be in trouble.',
 51306: 'Surround the most powerful one.',
 51307: 'We should retreat.',
 51308: 'Run for it!',
 51400: 'Fire a Broadside!',
 51401: 'Port Side! (left)',
 51402: 'Starboard Side! (right)',
 51403: 'Incoming!',
 51404: 'Come about!',
 51405: 'Broadside! Take Cover!',
 51406: 'To the Cannons!',
 51407: 'Open fire!',
 51408: 'Hold yer fire!',
 51409: 'Aim for the masts!',
 51410: 'Aim for the hull!',
 51411: 'Prepare to board!',
 51412: "She's coming about.",
 51413: 'Ramming speed!',
 51414: "We've got her on the run.",
 51415: 'We be taking on water!',
 51416: "We can't take anymore!",
 51417: "I don't have a shot!",
 51418: "Let's find port for repair.",
 51419: 'Man overboard!',
 51420: 'Enemy spotted.',
 51421: 'Handsomely now, mates!',
 50400: "Let's set sail.",
 50401: "Let's get out of here.",
 51500: "Let's sail to Port Royal.",
 51501: "Let's sail to Tortuga.",
 51502: "Let's sail to Padres Del Fuego.",
 51503: "Let's sail to Devil's Anvil.",
 51504: "Let's sail to Kingshead.",
 51505: "Let's sail to Isla Perdida.",
 51506: "Let's sail to Cuba.",
 51507: "Let's sail to Tormenta.",
 51508: "Let's sail to Outcast Isle.",
 51509: "Let's sail to Driftwood.",
 51510: "Let's sail to Cutthroat.",
 51511: "Let's sail to Rumrunner's Isle.",
 51512: "Let's sail to Isla Cangrejos.",
 51600: "Let's head into town.",
 51601: "Let's go to the docks.",
 51602: "Let's head to the tavern.",
 51800: "Let's go to Fort Charles.",
 51801: "Let's go to the Governor's Mansion.",
 52500: 'Where be I, mate?',
 51700: 'Yer already there.',
 51701: "I don't know.",
 51702: 'Yer on the wrong island.',
 51703: "That's in town.",
 51704: 'Look just outside of town.',
 51705: 'Ye will have to search through the jungle.',
 51706: 'Deeper inland.',
 51707: 'Oh, that be by the coast.',
 50200: 'Bilge rat!',
 50201: 'Scurvy dog!',
 50202: 'See ye in Davy Jones locker!',
 50203: 'Scoundrel!',
 50204: 'Landlubber!',
 50205: 'Addle-minded fool!',
 50206: 'You need a sharp sword and sharper wits.',
 50207: 'Ye be one doubloon short of a full hull mate!',
 50208: "Watch yer tongue or I'll pickle it with sea salt!",
 50209: 'Touch me loot and you get the boot!',
 50210: 'The horizon be as empty as yer head.',
 50211: "You're a canvas shy of a full sail, aren't ye mate?",
 50300: 'Fine shooting mate!',
 50301: 'A well placed blow!',
 50302: 'Nice shot!',
 50303: 'Well met!',
 50304: 'We showed them!',
 50305: 'Yer not so bad yerself!',
 50306: 'A fine plunder haul!',
 52400: 'May luck be my lady.',
 52401: 'I think these cards be marked!',
 52402: 'Blimey cheater!',
 51900: "That's a terrible flop!",
 51901: 'Trying to buy the hand, are ye?',
 51902: 'Ye be bluffing.',
 51903: "I don't think ye had it.",
 51904: 'Saved by the river.',
 52600: 'Hit me.',
 52601: 'Can I get another dealer?',
 53101: 'I caught a fish!',
 53102: 'I saw a Legendary Fish!',
 53103: 'What did you catch?',
 53104: 'This will make a whale of a tale!',
 53105: 'That was a beauty!',
 53106: 'Arr, the sea is treacherous today.',
 53107: 'What a bountiful haul of fish!',
 53110: 'Do you have the Legendary Lure?',
 53111: 'Have you ever caught a Legendary Fish?',
 53112: 'Can you sail on a fishing boat?',
 53113: 'Where is the Fishing Master?',
 53114: 'Have you completed your fish collection?',
 53120: 'Fire at my target!',
 53121: 'Fire at the ship closest to the shore!',
 53122: "There's a ship getting away!",
 53123: 'Fire at the big ships!',
 53124: 'Fire at the small ships!',
 53125: 'More are coming!',
 53126: "We're not going to last much longer!",
 53127: 'Shoot the barrels!',
 53128: "We've got new ammo!",
 53129: 'Sturdy defense, mates!',
 53141: 'Look at the potion I made!',
 53142: 'Have you completed your potion collection?',
 53143: 'Where is the Gypsy?',
 53144: 'What potion is that?',
 53145: 'This potion was easy enough.',
 53146: "This potion was hard brewin', I tell ye!",
 53160: 'We need someone to bilge pump!',
 53161: 'We need someone to scrub!',
 53162: 'We need someone to saw!',
 53163: 'We need someone to brace!',
 53164: 'We need someone to hammer!',
 53165: 'We need someone to patch!',
 53166: "I'll do it!",
 53167: "Keep it up, this ship won't repair itself!",
 53168: 'Great job repairing the ship!',
 52100: 'Want to group up?',
 52101: 'Join me crew?',
 52200: 'Fight some skeletons?',
 52201: 'Fight some crabs?',
 52300: "How 'bout a game of Mayhem?",
 52301: 'Join me Mayhem game.',
 52302: 'Want to start a Mayhem game?',
 52303: 'Want to start a team battle game?',
 52304: 'Join me team battle game.',
 52350: 'Join my Cannon Defense.',
 52351: 'Want to start a Cannon Defense?',
 52352: 'Can you lend me a hand with Repair?',
 52353: 'We need to Repair the ship now!',
 52354: 'Care to catch some fish?',
 52355: 'Want to go fishing with me?',
 52356: "Join me crew for some fishin'?",
 52357: 'Time to brew some potions!',
 52358: 'You should try your hand at brewing potions.',
 52000: 'Welcome to Pirates Online Retribution!',
 52001: 'Find any bugs yet?',
 52002: 'What feature do you hope they add next?',
 52003: 'How many times have you crashed?',
 52004: "It's good to be back in the Caribbean!",
 52005: 'Have you spotted any bugs recently?',
 52006: '',
 52007: '',
 52700: '',
 53000: '',
 52800: '',
 52900: '',
 50500: '',
 50600: '',
 60100: 'Hi!',
 60101: 'Hello!',
 60102: 'Hey!',
 60103: 'Yo!',
 60104: 'Hi everybody!',
 60105: 'How are you doing?',
 60106: "What's Up?",
 60200: 'Bye!',
 60201: 'Later!',
 60202: 'See ya!',
 60203: "I'll be right back.",
 60204: 'I need to go.',
 60300: ':-)',
 60301: 'Cool!',
 60302: 'Yeah!',
 60303: 'Ha ha!',
 60304: 'Sweet!',
 60305: 'Yeah!',
 60306: 'That rocks!',
 60307: 'Funky!',
 60308: 'Awesome!',
 60309: 'Wow!',
 60400: ':-(',
 60401: 'Doh!',
 60402: 'Aw man!',
 60403: 'Ouch!',
 60404: 'Bummer!',
 60500: 'Where are you?',
 60501: "Let's go to the Gateway Store.",
 60502: "Let's go to the Disco Hall.",
 60503: "Let's go to Toontown.",
 60504: "Let's go to Pirates of the Caribbean.",
 60505: 'Flip coin',
 60506: 'Dance',
 60507: 'Chant 1',
 60508: 'Chant 2',
 60509: 'Dance a jig',
 60510: 'Sleep',
 60511: 'Flex',
 60512: 'Play Lute',
 60513: 'Play Flute',
 60514: 'Frustrated',
 60515: 'Searching',
 60516: 'Yawn',
 60517: 'Kneel',
 60518: 'Sweep',
 60519: 'Primp',
 60520: 'Yawn',
 60521: 'Dance',
 60522: 'No',
 60523: 'Yes',
 60524: 'Laugh',
 60525: 'Clap',
 60526: 'Smile',
 60527: 'Anger',
 60528: 'Fear',
 60529: 'Sad',
 60530: 'Celebrate',
 60668: 'Celebrate',
 60669: 'Sleep',
 60602: 'Angry',
 60614: 'Clap',
 60622: 'Scared',
 60640: 'Laugh',
 60652: 'Sad',
 60657: 'Smile',
 60664: 'Wave',
 60665: 'Wink',
 60666: 'Yawn',
 60669: 'Sleep',
 60670: 'Dance',
 60676: 'Flirt',
 60677: 'Zombie dance',
 60678: 'Noisemaker',
 60671: "Hello, I'm a Pirate, and I'm here to steal your heart.",
 60672: "I just found the treasure I've been searching for.",
 60673: "If you were a booger, I'd pick you first.",
 60674: 'Come to Tortuga often?',
 60675: 'Do you have a map?  I just keep getting lost in your eyes.',
 65000: 'Yes',
 65001: 'No',
 60909: 'Check Hand'}
SpeedChatStaticText = SpeedChatStaticTextCommon
Emotes_Root = 'EMOTES'
Emotes_Dances = 'Dances'
Emotes_General = 'General'
Emotes_Music = 'Music'
Emotes_Expressions = 'Emotions'
Emote_ShipDenied = 'Cannot emote while sailing.'
Emote_MoveDenied = 'Cannot emote while moving.'
Emote_CombatDenied = 'Cannot emote while in combat.'
Emote_CannonDenied = 'Cannot emote while using a cannon.'
Emote_SwimDenied = 'Cannot emote while swimming.'
Emote_ParlorGameDenied = 'Cannot emote while playing a parlor game.'
Emotes = (60505,
 60506,
 60509,
 60510,
 60511,
 60516,
 60519,
 60520,
 60521,
 60522,
 60523,
 60524,
 60525,
 60526,
 60527,
 60528,
 60529,
 60530,
 60602,
 60607,
 60611,
 60614,
 60615,
 60622,
 60627,
 60629,
 60632,
 60636,
 60638,
 60640,
 60644,
 60652,
 60654,
 60657,
 60658,
 60663,
 60664,
 60665,
 60666,
 60668,
 60669,
 60612,
 60661,
 60645,
 60629,
 60641,
 60654,
 60630,
 60670,
 60633,
 60676,
 60677,
 65000,
 65001,
 60517,
 60678,
 60909)
CustomSCStrings = {10: 'Oh, well.',
 20: 'Why not?',
 30: 'Naturally!',
 40: "That's the way to do it.",
 50: 'Right on!',
 60: 'What up?',
 70: 'But of course!',
 80: 'Bingo!',
 90: "You've got to be kidding...",
 100: 'Sounds good to me.',
 110: "That's kooky!",
 120: 'Awesome!',
 130: 'For crying out loud!',
 140: "Don't worry.",
 150: 'Grrrr!',
 160: "What's new?",
 170: 'Hey, hey, hey!',
 180: 'See you tomorrow.',
 190: 'See you next time.',
 200: 'See ya later, alligator.',
 210: 'After a while, crocodile.',
 220: 'I need to go soon.',
 230: "I don't know about this!",
 240: "You're outta here!",
 250: 'Ouch, that really smarts!',
 260: 'Gotcha!',
 270: 'Please!',
 280: 'Thanks a million!',
 290: "You are stylin'!",
 300: 'Excuse me!',
 310: 'Can I help you?',
 320: "That's what I'm talking about!",
 330: "If you can't take the heat, stay out of the kitchen.",
 340: 'Well shiver me timbers!',
 350: "Well isn't that special!",
 360: 'Quit horsing around!',
 370: 'Cat got your tongue?',
 380: "You're in the dog house now!",
 390: 'Look what the cat dragged in.',
 400: 'I need to go see a Toon.',
 410: "Don't have a cow!",
 420: "Don't chicken out!",
 430: "You're a sitting duck.",
 440: 'Whatever!',
 450: 'Totally!',
 460: 'Sweet!',
 470: 'That rules!',
 480: 'Yeah, baby!',
 490: 'Catch me if you can!',
 500: 'You need to heal first.',
 510: 'You need more Laff Points.',
 520: "I'll be back in a minute.",
 530: "I'm hungry.",
 540: 'Yeah, right!',
 550: "I'm sleepy.",
 560: "I'm ready!",
 570: "I'm bored.",
 580: 'I love it!',
 590: 'That was exciting!',
 600: 'Jump!',
 610: 'Got gags?',
 620: "What's wrong?",
 630: 'Easy does it.',
 640: 'Slow and steady wins the race.',
 650: 'Touchdown!',
 660: 'Ready?',
 670: 'Set!',
 680: 'Go!',
 690: "Let's go this way!",
 700: 'You won!',
 710: 'I vote yes.',
 720: 'I vote no.',
 730: 'Count me in.',
 740: 'Count me out.',
 750: "Stay here, I'll be back.",
 760: 'That was quick!',
 770: 'Did you see that?',
 780: "What's that smell?",
 790: 'That stinks!',
 800: "I don't care.",
 810: 'Just what the doctor ordered.',
 820: "Let's get this party started!",
 830: 'This way everybody!',
 840: 'What in the world?',
 850: "The check's in the mail.",
 860: 'I heard that!',
 870: 'Are you talking to me?',
 880: "Thank you, I'll be here all week.",
 890: 'Hmm.',
 900: "I'll get this one.",
 910: 'I got it!',
 920: "It's mine!",
 930: 'Please, take it.',
 940: 'Stand back, this could be dangerous.',
 950: 'No worries!',
 960: 'Oh, my!',
 970: 'Whew!',
 980: 'Owoooo!',
 990: 'All Aboard!',
 1000: 'Hot Diggity Dog!',
 1010: 'Curiosity killed the cat.',
 2000: 'Act your age!',
 2010: 'Am I glad to see you!',
 2020: 'Be my guest.',
 2030: 'Been keeping out of trouble?',
 2040: 'Better late than never!',
 2050: 'Bravo!',
 2060: 'But seriously, folks...',
 2070: 'Care to join us?',
 2080: 'Catch you later!',
 2090: 'Changed your mind?',
 2100: 'Come and get it!',
 2110: 'Dear me!',
 2120: 'Delighted to make your acquaintance.',
 2130: "Don't do anything I wouldn't do!",
 2140: "Don't even think about it!",
 2150: "Don't give up the ship!",
 2160: "Don't hold your breath.",
 2170: "Don't ask.",
 2180: 'Easy for you to say.',
 2190: 'Enough is enough!',
 2200: 'Excellent!',
 2210: 'Fancy meeting you here!',
 2220: 'Give me a break.',
 2230: 'Glad to hear it.',
 2240: 'Go ahead, make my day!',
 2250: 'Go for it!',
 2260: 'Good job!',
 2270: 'Good to see you!',
 2280: 'Got to get moving.',
 2290: 'Got to hit the road.',
 2300: 'Hang in there.',
 2310: 'Hang on a second.',
 2320: 'Have a ball!',
 2330: 'Have fun!',
 2340: "Haven't got all day!",
 2350: 'Hold your horses!',
 2360: 'Horsefeathers!',
 2370: "I don't believe this!",
 2380: 'I doubt it.',
 2390: 'I owe you one.',
 2400: 'I read you loud and clear.',
 2410: 'I think so.',
 2420: 'I think you should pass.',
 2430: "I wish I'd said that.",
 2440: "I wouldn't if I were you.",
 2450: "I'd be happy to!",
 2460: "I'm helping my friend.",
 2470: "I'm here all week.",
 2480: 'Imagine that!',
 2490: 'In the nick of time...',
 2500: "It's not over 'til it's over.",
 2510: 'Just thinking out loud.',
 2520: 'Keep in touch.',
 2530: 'Lovely weather for ducks!',
 2540: 'Make it snappy!',
 2550: 'Make yourself at home.',
 2560: 'Maybe some other time.',
 2570: 'Mind if I join you?',
 2580: 'Nice place you have here.',
 2590: 'Nice talking to you.',
 2600: 'No doubt about it.',
 2610: 'No kidding!',
 2620: 'Not by a long shot.',
 2630: 'Of all the nerve!',
 2640: 'Okay by me.',
 2650: 'Righto.',
 2660: 'Say cheese!',
 2670: 'Say what?',
 2680: 'Tah-dah!',
 2690: 'Take it easy.',
 2700: 'Ta-ta for now!',
 2710: 'Thanks, but no thanks.',
 2720: 'That takes the cake!',
 2730: "That's funny.",
 2740: "That's the ticket!",
 2750: "There's a Cog invasion!",
 2760: 'Toodles.',
 2770: 'Watch out!',
 2780: 'Well done!',
 2790: "What's cooking?",
 2800: "What's happening?",
 2810: 'Works for me.',
 2820: 'Yes sirree.',
 2830: 'You betcha.',
 2840: 'You do the math.',
 2850: 'You leaving so soon?',
 2860: 'You make me laugh!',
 2870: 'You take right.',
 2880: "You're going down!",
 3000: 'Anything you say.',
 3010: 'Care if I join you?',
 3020: 'Check, please.',
 3030: "Don't be too sure.",
 3040: "Don't mind if I do.",
 3050: "Don't sweat it!",
 3060: "Don't you know it!",
 3070: "Don't mind me.",
 3080: 'Eureka!',
 3090: 'Fancy that!',
 3100: 'Forget about it!',
 3110: 'Going my way?',
 3120: 'Good for you!',
 3130: 'Good grief.',
 3140: 'Have a good one!',
 3150: 'Heads up!',
 3160: 'Here we go again.',
 3170: 'How about that!',
 3180: 'How do you like that?',
 3190: 'I believe so.',
 3200: 'I think not.',
 3210: "I'll get back to you.",
 3220: "I'm all ears.",
 3230: "I'm busy.",
 3240: "I'm not kidding!",
 3250: "I'm speechless.",
 3260: 'Keep smiling.',
 3270: 'Let me know!',
 3280: 'Let the pie fly!',
 3290: "Likewise, I'm sure.",
 3300: 'Look alive!',
 3310: 'My, how time flies.',
 3320: 'No comment.',
 3330: "Now you're talking!",
 3340: 'Okay by me.',
 3350: 'Pleased to meet you.',
 3360: 'Righto.',
 3370: 'Sure thing.',
 3380: 'Thanks a million.',
 3390: "That's more like it.",
 3400: "That's the stuff!",
 3410: 'Time for me to hit the hay.',
 3420: 'Trust me!',
 3430: 'Until next time.',
 3440: 'Wait up!',
 3450: 'Way to go!',
 3460: 'What brings you here?',
 3470: 'What happened?',
 3480: 'What now?',
 3490: 'You first.',
 3500: 'You take left.',
 3510: 'You wish!',
 3520: "You're toast!",
 3530: "You're too much!",
 4000: 'Toons rule!',
 4010: 'Cogs drool!',
 4020: 'Toons of the world unite!',
 4030: 'Howdy, partner!',
 4040: 'Much obliged.',
 4050: 'Get along, little doggie.',
 4060: "I'm going to hit the hay.",
 4070: "I'm chomping at the bit!",
 4080: "This town isn't big enough for the two of us!",
 4090: 'Saddle up!',
 4100: 'Draw!!!',
 4110: "There's gold in them there hills!",
 4120: 'Happy trails!',
 4130: 'This is where I ride off into the sunset...',
 4140: "Let's skedaddle!",
 4150: 'You got a bee in your bonnet?',
 4160: 'Lands sake!',
 4170: 'Right as rain.',
 4180: 'I reckon so.',
 4190: "Let's ride!",
 4200: 'Well, go figure!',
 4210: "I'm back in the saddle again!",
 4220: 'Round up the usual suspects.',
 4230: 'Giddyup!',
 4240: 'Reach for the sky.',
 4250: "I'm fixing to.",
 4260: 'Hold your horses!',
 4270: "I can't hit the broad side of a barn.",
 4280: "Y'all come back now.",
 4290: "It's a real barn burner!",
 4300: "Don't be a yellow belly.",
 4310: 'Feeling lucky?',
 4320: "What in Sam Hill's goin' on here?",
 4330: 'Shake your tail feathers!',
 4340: "Well, don't that take all.",
 4350: "That's a sight for sore eyes!",
 4360: 'Pickins is mighty slim around here.',
 4370: 'Take a load off.',
 4380: "Aren't you a sight!",
 4390: "That'll learn ya!",
 6000: 'I want candy!',
 6010: "I've got a sweet tooth.",
 6020: "That's half-baked.",
 6030: 'Just like taking candy from a baby!',
 6040: "They're cheaper by the dozen.",
 6050: 'Let them eat cake!',
 6060: "That's the icing on the cake.",
 6070: "You can't have your cake and eat it too.",
 6080: 'I feel like a kid in a candy store.',
 6090: 'Six of one, half a dozen of the other...',
 6100: "Let's keep it short and sweet.",
 6110: 'Keep your eye on the doughnut not the hole.',
 6120: "That's pie in the sky.",
 6130: "But it's wafer thin.",
 6140: "Let's gum up the works!",
 6150: "You're one tough cookie!",
 6160: "That's the way the cookie crumbles.",
 6170: 'Like water for chocolate.',
 6180: 'Are you trying to sweet talk me?',
 6190: 'A spoonful of sugar helps the medicine go down.',
 6200: 'You are what you eat!',
 6210: 'Easy as pie!',
 6220: "Don't be a sucker!",
 6230: 'Sugar and spice and everything nice.',
 6240: "It's like butter!",
 6250: 'The candyman can!',
 6260: 'We all scream for ice cream!',
 6270: "Let's not sugar coat it.",
 6280: 'Knock knock...',
 6290: "Who's there?",
 7000: 'Quit monkeying around!',
 7010: 'That really throws a monkey-wrench in things.',
 7020: 'Monkey see, monkey do.',
 7030: 'They made a monkey out of you.',
 7040: 'That sounds like monkey business.',
 7050: "I'm just monkeying with you.",
 7060: "Who's gonna be monkey in the middle?",
 7070: "That's a monkey off my back...",
 7080: 'This is more fun than a barrel of monkeys!',
 7090: "Well I'll be a monkey's uncle.",
 7100: "I've got monkeys on the brain.",
 7110: "What's with the monkey suit?",
 7120: 'Hear no evil.',
 7130: 'See no evil.',
 7140: 'Speak no evil.',
 7150: "Let's make like a banana and split.",
 7160: "It's a jungle out there.",
 7170: "You're the top banana.",
 7180: 'Cool bananas!',
 7190: "I'm going bananas!",
 7200: "Let's get into the swing of things!",
 7210: 'This place is swinging!',
 7220: "I'm dying on the vine.",
 7230: 'This whole affair has me up a tree.',
 7230: "Let's make like a tree and leave.",
 7240: "Jellybeans don't grow on trees!",
 10000: 'This place is a ghost town.',
 10001: 'Nice costume!',
 10002: 'I think this place is haunted.',
 10003: 'Trick or Treat!',
 10004: 'Boo!',
 10005: 'Happy Haunting!',
 10006: 'Happy Halloween!',
 10007: "It's time for me to turn into a pumpkin.",
 10008: 'Spooktastic!',
 10009: 'Spooky!',
 10010: "That's creepy!",
 10011: 'I hate spiders!',
 10012: 'Did you hear that?',
 10013: "You don't have a ghost of a chance!",
 10014: 'You scared me!',
 10015: "That's spooky!",
 10016: "That's freaky!",
 10017: 'That was strange....',
 10018: 'Skeletons in your closet?',
 10019: 'Did I scare you?',
 11000: 'Bah! Humbug!',
 11001: 'Better not pout!',
 11002: 'Brrr!',
 11003: 'Chill out!',
 11004: 'Come and get it!',
 11005: "Don't be a turkey.",
 11006: 'Gobble gobble!',
 11007: 'Happy holidays!',
 11008: 'Happy New Year!',
 11009: 'Happy Thanksgiving!',
 11010: 'Happy Turkey Day!',
 11011: 'Ho! Ho! Ho!',
 11012: 'It\'s "snow" problem.',
 11013: 'It\'s "snow" wonder.',
 11014: 'Let it snow!',
 11015: "Rake 'em in.",
 11016: "Season's greetings!",
 11017: 'Snow doubt about it!',
 11018: 'Snow far, snow good!',
 11019: 'Yule be sorry!',
 11020: 'Have a Wonderful Winter!',
 11021: 'The Holiday Party decorations are Toontastic!',
 11022: 'Toon Troopers are hosting Holiday Parties!',
 12000: 'Be mine!',
 12001: 'Be my sweetie!',
 12002: "Happy ValenToon's Day!",
 12003: 'Aww, how cute.',
 12004: "I'm sweet on you.",
 12005: "It's puppy love.",
 12006: 'Love ya!',
 12007: 'Will you be my ValenToon?',
 12008: 'You are a sweetheart.',
 12009: 'You are as sweet as pie.',
 12010: 'You are cute.',
 12011: 'You need a hug.',
 12012: 'Lovely!',
 12013: "That's darling!",
 12014: 'Roses are red...',
 12015: 'Violets are blue...',
 12016: "That's sweet!",
 12050: 'I LOVE busting Cogs!',
 12051: "You're dynamite!",
 12052: 'I only have hypno-eyes for you!',
 12053: "You're sweeter than a jellybean!",
 12054: "I'd LOVE for you to come to my ValenToon's party!",
 13000: "Top o' the mornin' to you!",
 13001: "Happy St. Patrick's Day!",
 13002: "You're not wearing green!",
 13003: "It's the luck of the Irish.",
 13004: "I'm green with envy.",
 13005: 'You lucky dog!',
 13006: "You're my four leaf clover!",
 13007: "You're my lucky charm!",
 14000: "Let's have a summer Estate party!",
 14001: "It's party time!",
 14002: 'Last one in the pond is a rotten Cog!',
 14003: 'Group Doodle training time!',
 14004: 'Doodle training time!',
 14005: 'Your Doodle is cool!',
 14006: 'What tricks can your Doodle do?',
 14007: 'Time for Cannon Pinball!',
 14008: 'Cannon Pinball rocks!',
 14009: 'Your Estate rocks!',
 14010: 'Your Garden is cool!',
 14011: 'Your Estate is cool!'}
SCMenuEmotions = 'EMOTIONS'
SCMenuCustom = 'MY PHRASES'
PSCMenuTesting = 'ALPHA'
PSCMenuExpressions = 'EXPRESSIONS'
PSCMenuGreetings = 'GREETINGS'
PSCMenuGoodbyes = 'GOODBYES'
PSCMenuFriendly = 'FRIENDLY'
PSCMenuHappy = 'HAPPY'
PSCMenuSad = 'SAD'
PSCMenuSorry = 'SORRY'
PSCMenuCombat = 'COMBAT'
PSCMenuSeaCombat = 'SEA COMBAT'
PSCMenuPlaces = 'PLACES'
PSCMenuLetsSail = "LET'S SAIL..."
PSCMenuLetsHeadTo = "LET'S HEAD TO..."
PSCMenuHeadToPortRoyal = 'PORT ROYAL'
PSCMenuWhereIs = 'WHERE IS ..?'
PSCMenuWhereIsPortRoyal = 'PORT ROYAL'
PSCMenuWhereIsTortuga = 'TORTUGA'
PSCMenuWhereIsPadresDelFuego = 'PADRES DEL FUEGO'
PSCMenuWhereIsLasPulgas = 'LAS PULGAS'
PSCMenuWhereIsLosPadres = 'LOS PADRES'
PSCMenuDirections = 'DIRECTIONS'
PSCMenuInsults = 'INSULTS'
PSCMenuCompliments = 'COMPLIMENTS'
PSCMenuCardGames = 'CARD GAMES'
PSCMenuPoker = 'POKER'
PSCMenuBlackjack = 'BLACKJACK'
PSCMenuMinigames = 'MINIGAMES'
PSCMenuFishing = 'FISHING'
PSCMenuCannonDefense = 'CANNON DEFENSE'
PSCMenuPotions = 'POTION BREWING'
PSCMenuRepair = 'REPAIR'
PSCMenuInvitations = 'INVITATIONS'
PSCMenuVersusPlayer = 'VERSUS'
PSCMenuHunting = 'HUNTING'
PSCMenuQuests = 'QUESTS'
PSCMenuShips = 'SHIPS'
PSCMenuAdventures = 'ADVENTURE'
RandomButton = 'Randomize'
TypeANameButton = 'Type Name'
PickANameButton = 'Pick-A-Name'
NoPunctuation = "You can't use punctuation marks in your name!"
PeriodOnlyAfterLetter = 'You can use a period in your name, but only after a letter.'
ApostropheOnlyAfterLetter = 'You can use an apostrophe in your name, but only after a letter.'
NoNumbersInTheMiddle = 'Numeric digits may not appear in the middle of a word.'
ThreeWordsOrLess = 'Your name must be three words or fewer.'
NCTooShort = 'That name is too short.'
NCNoDigits = 'Your name cannot contain numbers.'
NCNeedLetters = 'Each word in your name must contain some letters.'
NCNeedVowels = 'Each word in your name must contain some vowels.'
NCAllCaps = 'Your name cannot be all capital letters.'
NCMixedCase = 'That name has too many capital letters.'
NCBadCharacter = "Your name cannot contain the character '%s'"
NCRepeatedChar = "Your name has too many of the character '%s'"
NCGeneric = 'Sorry, that name will not work.'
NCTooManyWords = 'Your name cannot be more than four words long.'
NCDashUsage = "Dashes may only be used to connect two words together (like in 'Boo-Boo')."
NCCommaEdge = 'Your name may not begin or end with a comma.'
NCCommaAfterWord = 'You may not begin a word with a comma.'
NCCommaUsage = 'That name does not use commas properly. Commas must join two words together, like in the name "Dr. Quack, MD". Commas must also be followed by a space.'
NCPeriodUsage = 'That name does not use periods properly. Periods are only allowed in words like "Mr.", "Mrs.", "J.T.", etc.'
NCApostrophes = 'That name has too many apostrophes.'
AvatarPanelStopIgnore = 'Stop Ignoring'

InjectorTitle = 'Injector'
InjectorInject = 'Inject'
InjectorInjectAI = 'Inject to AI'
InjectorSave = 'Save'
InjectorLoad = 'Load'
InjectorRemove = 'Remove'
InjectorOops = 'Oops!'
InjectorOhYea = 'Oh yea!'
InjectorSaveQuestion = 'What do you want to name this code snippet?'
InjectorNotSaved = 'Your code snippet was not saved!'
InjectorSnippetExists = 'That snippet already exists. Do you want to replace it with this new one?'
InjectorSaved = 'Your code snippet was saved under "%s"!'
InjectorLoadQuestion = 'Which code snippet would you like to load?'
InjectorOverwriteWarning = 'This will overwrite your current code. Would you like to continue?'
InjectorLoaded = '"%s" was loaded successfully!'
InjectorRemoveQuestion = 'Which code snippet would you like to remove?'
InjectorRemoveWarning = 'This will remove the snippet "%s"! Are you sure you want to do this?'
InjectorRemoved = '"%s" was removed successfully!'
InjectorAIUnavailable = 'Not connected to AI server!'
InjectorPStats = 'PStats Client'

ChatChannels = {0: 'User', 1: 'Staff'}
APlayer = 'A Player'

MutedWarning = "Sorry, but you can't talk. You are muted for %s!"
MutedUntil = 'You are currently muted for %s.'
MutedForever = 'forever'
UnmutedWarning = 'You have been unmuted!'

TimeIntervals = (
 ('weeks', 604800),
 ('days', 86400),
 ('hours', 3600),
 ('minutes', 60),
 ('seconds', 1),
)

def getHumanTime(seconds, granularity=4):
    result = []

    for name, count in TimeIntervals[:granularity]:
        value = seconds // count

        if value:
            seconds -= value * count

            if value == 1:
                name = name.rstrip('s')

            result.append("{} {}".format(value, name))

    if len(result) >= 2:
        result[-1] = 'and ' + result[-1]

    return ', '.join(result)

def timeElapsedString(timeDelta):
    timeDelta = abs(timeDelta)
    if timeDelta.days > 0:
        if timeDelta.days == 1:
            return '1 day ago'
        else:
            return '%s days ago' % timeDelta.days
    elif timeDelta.seconds / 3600 > 0:
        if timeDelta.seconds / 3600 == 1:
            return '1 hour ago'
        else:
            return '%s hours ago' % (timeDelta.seconds / 3600)
    elif timeDelta.seconds / 60 < 2:
        return '1 minute ago'
    else:
        return '%s minutes ago' % (timeDelta.seconds / 60)