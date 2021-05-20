from panda3d.core import TextNode
# File: F (Python 2.4)

from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from direct.fsm import StateData
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPGlobals
import GuiButton
from pirates.piratesgui import PirateMemberList
from direct.task import Task
from pirates.uberdog.UberDogGlobals import InventoryType

class FriendsPage(SocialPage.SocialPage):
    NumVisible = 6

    def __init__(self, showAvatar = 1):
        self.showAvatar = showAvatar

        if self.showAvatar:
            myTitle = PLocalizer.AvatarFriendsListLabel

        SocialPage.SocialPage.__init__(self, myTitle)
        self.initialiseoptions(FriendsPage)
        charGui = loader.loadModel('models/gui/char_gui')
        self.membersList = PirateMemberList.PirateMemberList(10, self, 'FOOLIO HC', height = 0.680000, memberWidth = 0.598, width = 0.62, sort = 1)
        self.membersList.setPos(-0.0864, 0.0, 0.0299)
        self.accept(self.membersList.onlineChangeEvent, self.updateCount)
        if self.showAvatar:
            self.accept(OTPGlobals.AvatarFriendAddEvent, self.addAvatarFriend)
            self.accept(OTPGlobals.AvatarFriendUpdateEvent, self.updateAvatarFriend)
            self.accept(OTPGlobals.AvatarFriendRemoveEvent, self.removeAvatarFriend)

        charGui.remove_node()
        self.headingLabel = DirectLabel(parent = self, relief = None, state = DGG.NORMAL, text = myTitle, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), text_fg = PiratesGuiGlobals.TextFG1, pos = (0.239, 0, 0.794000))
        self.maintainNormalButtonState()


    def show(self):
        SocialPage.SocialPage.show(self)
        self.membersList.updateOnlineData()


    def destroy(self):
        self.stopMaintainNormalButtonState()
        self.ignoreAll()
        self.membersList.destroy()
        SocialPage.SocialPage.destroy(self)


    def addAvatarFriend(self, avId, info):
        self.updateAvatarFriend(avId, info)
        if hasattr(base, 'localAvatar'):
            inv = base.localAvatar.getInventory()
            if inv and not inv.getStackQuantity(InventoryType.NewFriend):
                base.localAvatar.sendRequestContext(InventoryType.NewFriend)

    def updateAvatarFriend(self, avId, info):
        self.membersList.updateOrAddMember(avId, PirateMemberList.MODE_FRIEND_AVATAR, info)
        self.startRecountMembers()

    def removeAllFriends(self):
        self.membersList.removeAll()
        self.membersList.arrangeMembers()
        self.startRecountMembers()
    
    def removeAvatarFriend(self, avId):
        self.membersList.removeMember(avId, PirateMemberList.MODE_FRIEND_AVATAR)
        self.membersList.arrangeMembers()
        self.startRecountMembers()

    def maintainNormalButtonState(self):
        taskMgr.remove('friendsMaintainNormalButtonState')
        taskMgr.doMethodLater(15, self.friendsMaintainNormalButtonState, 'friendsMaintainNormalButtonState')


    def stopMaintainNormalButtonState(self):
        taskMgr.remove('friendsMaintainNormalButtonState')


    def friendsMaintainNormalButtonState(self, task):
        for friendButton in self.membersList.members:
            friendButton['state'] = DGG.NORMAL

        return Task.again


    def updateCount(self, task = None):
        self.count = self.membersList.getSize()
        self.headingLabel['text'] = '%s %s/%s' % (self.title, self.membersList.onlineCount, self.count)
        if task:
            return task.done
