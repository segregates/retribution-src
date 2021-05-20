from panda3d.core import Point3, TextNode, Vec3, Vec4
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from otp.distributed import OtpDoGlobals
from otp.otpgui import OTPDialog
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals, PDialog
from pirates.piratesbase import PLocalizer
import webbrowser

POP_COLORS = (Vec4(0.4, 0.4, 1.0, 1.0),
              Vec4(0.4, 1.0, 0.4, 1.0),
              Vec4(1.0, 0.4, 0.4, 1.0))
POP_ADMIN_ACCESS = Vec4(1.0, 0.65, 0.0, 1.0)

class ShardPanel(DirectFrame):
    UPPOS = Vec3(0.550000, 0, 1.52)
    DOWNPOS = Vec3(0.550000, 0, 0.71)
    SHOWTIME = 0.5
    POP_SHOWIDEAL_THRESHOLD = 0.800000

    def __init__(self, parent, gear, **kw):
        gui = loader.loadModel('models/gui/gui_map_window_drawer')
        dotcard = loader.loadModel('models/gui/toplevel_gui')
        self.dot = dotcard.find('**/topgui_icon_ship_hulldot_on')
        self.shards = { }
        optiondefs = (('image', gui.find('**/drawer'), None), ('image_scale', 0.320, None), ('pos', ShardPanel.UPPOS, None), ('uppos', ShardPanel.UPPOS, None), ('downpos', ShardPanel.DOWNPOS, None), ('showtime', ShardPanel.SHOWTIME, None), ('shardSelected', self.shardSelected, None), ('inverted', False, None), ('buttonFont', PiratesGlobals.getPirateFont(), None), ('preferredShard', 0, self.setPreferredShard))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(ShardPanel)
        bounds = self.getBounds()
        self['frameSize'] = Vec4(bounds[0], bounds[1], bounds[2], bounds[3]) * 1.25
        self.shards = { }
        self.stopLightButtons = { }
        self.textRolloverColor = Vec4(0.4, 0.4, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.800000, 0.4, 0.4, 1)
        self.textSelectedColor = Vec4(0.4, 0.800000, 0.4, 1)
        self.gear = gear
        self.up = True
        self.showIval = None
        self.hideIval = None

        self.showPop = config.GetBool('show-total-population', True)
        self.teleportAll = config.GetBool('teleport-all', False)

        self.noTeleport = not self.teleportAll
        self.rotationFrame = DirectFrame(parent = self, relief = None, state = DGG.DISABLED)

        if self['inverted']:
            self.rotationFrame.setR(180)
            self.rotationFrame.setPos(-0.02, 0, 0.418)

        self.titleLabel = DirectLabel(parent = self.rotationFrame, relief = None, text = PLocalizer.ShardActiveWorlds, text_font = PiratesGlobals.getPirateOutlineFont(), text_scale = 0.08, text_fg = PiratesGuiGlobals.TextFG2, textMayChange = 0, pos = (0, 0, 0.545000))
        if self['inverted']:
            self.titleLabel.hide()

        self.button = DirectButton(parent = self, relief = None, geom = gui.find('**/drawer_button_over'), geom_scale = 0.320, command = self.handleButtonPressed)
        if self['inverted']:
            self.button['frameSize'] = (-0.37, 0.348, -0.320, -0.11)

        self.currentShardLabel = DirectLabel(parent = self.rotationFrame, text = '', text_font = self['buttonFont'], text_scale = 0.050000, text_fg = PiratesGuiGlobals.TextFG2, textMayChange = 1, pos = (0, 0, -0.233))
        if self['inverted']:
            self.currentShardLabel.setZ(0.60498)
            self.currentShardLabel.setAlphaScale(0.9)

        self.shardScrolledFrame = DirectScrolledFrame(parent = self.rotationFrame, relief = 1, state = DGG.NORMAL, frameColor = (1, 1, 1, 0), borderWidth = PiratesGuiGlobals.BorderWidth, frameSize = (0, 0.685000, -0.826, -0.125), canvasSize = (0, 0, 0, 0), verticalScroll_frameColor = PiratesGuiGlobals.ScrollbarColor, verticalScroll_borderWidth = (0.00500, 0.00500), verticalScroll_frameSize = (0, PiratesGuiGlobals.ScrollbarSize, 0, 0), verticalScroll_thumb_frameColor = PiratesGuiGlobals.ButtonColor2, verticalScroll_incButton_frameColor = PiratesGuiGlobals.ButtonColor2, verticalScroll_decButton_frameColor = PiratesGuiGlobals.ButtonColor2, verticalScroll_scrollSize = 0.096, horizontalScroll_frameColor = PiratesGuiGlobals.ScrollbarColor, horizontalScroll_borderWidth = (0.00500, 0.00500), horizontalScroll_frameSize = (0, 0, 0, PiratesGuiGlobals.ScrollbarSize), horizontalScroll_thumb_frameColor = PiratesGuiGlobals.ButtonColor2, horizontalScroll_incButton_frameColor = PiratesGuiGlobals.ButtonColor2, horizontalScroll_decButton_frameColor = PiratesGuiGlobals.ButtonColor2, pos = (-0.35198, 0, 0.65600))
        self.shardScrolledFrame.accept('press-wheel_up-%s' % self.shardScrolledFrame.guiId, self.mouseWheelUp)
        self.shardScrolledFrame.accept('press-wheel_down-%s' % self.shardScrolledFrame.guiId, self.mouseWheelDown)
        self.refreshShardLabels()
        self.accept('shardSwitchComplete', self.refreshCurrentShard)
        self.alertDialog = None

    def removeAlertDialog(self, *args):
        if self.alertDialog:
            self.alertDialog.destroy()
            webbrowser.open('https://piratesonline.us/rewards-store')
        
        self.alertDialog = None

    def mouseWheelUp(self, task = None):
        if self.shardScrolledFrame.verticalScroll.isHidden():
            return None

        amountScroll = 0.050000
        if self.shardScrolledFrame.verticalScroll['value'] > 0:
            self.shardScrolledFrame.verticalScroll['value'] -= amountScroll

    def mouseWheelDown(self, task = None):
        if self.shardScrolledFrame.verticalScroll.isHidden():
            return None

        amountScroll = 0.050000
        if self.shardScrolledFrame.verticalScroll['value'] < 1.0:
            self.shardScrolledFrame.verticalScroll['value'] += amountScroll

    def destroy(self):
        self.ignore('shardSwitchComplete')
        self.cancelIval()
        self.showIval = None
        self.hideIval = None
        self.gear = None
        self.stopListening()
        self.shards = { }
        DirectFrame.destroy(self)

    def handleButtonPressed(self):
        if self.up:
            try: self.getShowIval().start()
            except: pass
        else:
            try: self.getHideIval().start()
            except: pass

    def toggleUpState(self, up):
        self.up = up
        if self.up:
            self['state'] = DGG.DISABLED
            self.stopListening()
        else:
            self['state'] = DGG.NORMAL
            self.syncShardList()
            self.startListening()

    def getShowIval(self):
        if self.showIval:
            return self.showIval

        self.showIval = Sequence(Func(self.cancelIval, 'hide'), Func(self.toggleUpState, 0), Parallel(self.gear.hprInterval(self['showtime'], Vec3(0, 0, -180), blendType = 'easeInOut'), self.posInterval(self['showtime'], self['downpos'], blendType = 'easeInOut')))
        return self.showIval

    def getHideIval(self):
        if self.hideIval:
            return self.hideIval

        self.hideIval = Sequence(Func(self.cancelIval, 'show'), Func(self.toggleUpState, 1), Parallel(self.gear.hprInterval(self['showtime'], Vec3(0, 0, 0), blendType = 'easeInOut'), self.posInterval(self['showtime'], self['uppos'], blendType = 'easeInOut')))
        return self.hideIval

    def cancelIval(self, type=['show', 'hide']):
        if 'show' in type:
            if self.showIval:
                if self.showIval.isPlaying():
                    self.showIval.pause()

        if 'hide' in type:
            if self.hideIval:
                if self.hideIval.isPlaying():
                    self.hideIval.pause()

    def hideIfShown(self):
        if not self.up:
            self.getHideIval().start()

    def syncShardList(self):
        current = set(self.shards.keys())
        shards = base.cr.listActiveShards()
        active = [shard[0] for shard in shards]
        old = list(set(current) - set(active))
        new = list(set(active) - set(current))

        for id in old:
            self.removeShard(id)

        for id in new:
            for shard in shards:
                if shard[0] == id:
                    self.addShard(id, shard[1], False)
                    break

        self.refreshShardLabels()
        self.refreshCurrentShard()

    def getShardName(self, doId):
        shard = base.cr.doId2do.get(doId)
        if shard:
            return shard.getName()
        return ''

    def addShard(self, id, name, sort = True):
        self.shards[id] = self.makeShardButton(id, name)

        if self['inverted'] and self['preferredShard'] == id:
            self['preferredShard'] = id

        if sort:
            self.refreshShardLabels()
            self.refreshCurrentShard()

    def removeShard(self, id):
        sLabel = self.shards.pop(id, None)
        if self['inverted'] and self['preferredShard'] == id:
            self['preferredShard'] = id

        if sLabel:
            sLabel.destroy()
            self.refreshShardLabels()

    def handleShardPopulationUpdate(self, shardId, population):
        if base.cr.isShardAvailable(shardId) and population >= 0:
            self.updateShard(shardId, avatarCount = population)
        else:
            self.removeShard(shardId)

    def handleShardPopLimitsUpdate(self, shardId, min, max):
        if base.cr.isShardAvailable(shardId):
            self.updateShard(shardId, popLimits = (min, max))

    def updateShard(self, id, name = '', avatarCount = -1, popLimits = ()):
        sLabel = self.shards.get(id)
        if not sLabel:
            name = self.getShardName(id)
            if name:
                self.addShard(id, name, True)

        if avatarCount >= 0:
            self.updateAvCount(id, avatarCount)

        if popLimits:
            self.updatePopLimits(id, popLimits[0], popLimits[1])

    def getPopColor(self, id, pop, min, max):
        shard = base.cr.activeDistrictMap.get(id)

        if shard and shard.minimumAdminAccess > 0:
            return POP_ADMIN_ACCESS

        if pop <= min * ShardPanel.POP_SHOWIDEAL_THRESHOLD:
            newColor = POP_COLORS[0]
        elif pop < max:
            newColor = POP_COLORS[1]
        else:
            newColor = POP_COLORS[2]
        return newColor

    def getPopText(self, pop, min, max):
        if pop <= min * ShardPanel.POP_SHOWIDEAL_THRESHOLD:
            popText = PLocalizer.ShardPageLow
        elif pop <= max:
            popText = PLocalizer.ShardPageMed
        else:
            popText = PLocalizer.ShardPageHigh
        return popText

    def makeShardButton(self, shardId, shardName):
        shardButton = DirectButton(parent = self.shardScrolledFrame.getCanvas(), relief = None, borderWidth = (0.001, 0.001), frameSize = (0.00600, 0.680000, -0.01, 0.0448), frameColor = (Vec4(0, 0, 0, 0), self.textDownColor, self.textRolloverColor, Vec4(0, 0, 0, 0)), text = shardName, text_scale = 0.050000, text_font = self['buttonFont'], text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text3_fg = self.textDisabledColor, text_pos = (0.01, 0), textMayChange = 1, command = self.shardButtonPressed, extraArgs = [
            shardId])
        popLabel = DirectLabel(parent = shardButton, relief = None, state = DGG.DISABLED, image = self.dot, image_scale = (0.5, 1, 0.5), image_color = POP_COLORS[0], pos = (0.62, 0, 0.0125), text = '', text_scale = 0.050000, text_align = TextNode.ARight, text_pos = (-0.0299, -0.0125), text_font = self['buttonFont'], text_fg = Vec4(1))
        shardButton.popLabel = popLabel
        shardButton.avCount = 0
        shardButton.min = 0
        shardButton.max = 0
        shardButton.accept('press-wheel_up-%s' % shardButton.guiId, self.mouseWheelUp)
        shardButton.accept('press-wheel_down-%s' % shardButton.guiId, self.mouseWheelDown)
        return shardButton

    def isShardSpecial(self, id):
        return id in base.cr.activeDistrictMap and base.cr.activeDistrictMap[id].minimumAdminAccess > 0

    def refreshShardLabels(self):
        shardIds = self.shards.keys()
        shardIds.sort()
        startPos = Point3(0, 0, -0.050000)
        offset = Point3(0, 0, -0.070)
        x = 0
        l1 = [shardId for shardId in shardIds if self.isShardSpecial(shardId)]
        l2 = [shardId for shardId in shardIds if shardId not in l1]

        for id in sorted(l1, key=lambda x: self.shards[x]['text']) + sorted(l2, key=lambda x: self.shards[x]['text']):
            dLabel = self.shards[id]
            dLabel.setPos(startPos + offset * x)
            x += 1

        canvasHeight = offset * len(shardIds)
        self.shardScrolledFrame['canvasSize'] = (0, 0, canvasHeight[2] - 0.00500, 0)

    def refreshCurrentShard(self):
        if base.cr.distributedDistrict:
            self.currentShardLabel['text'] = PLocalizer.ShardCurrentWorld + ' : %s %s' % (base.cr.distributedDistrict.getName(), PLocalizer.Ocean)
            for id in self.shards:
                self.shards[id]['state'] = DGG.NORMAL
                self.shards[id]['relief'] = DGG.RAISED

            curButton = self.shards.get(base.cr.distributedDistrict.getDoId())
            if curButton:
                curButton['state'] = DGG.DISABLED
                curButton['relief'] = DGG.SUNKEN

    def setPreferredShard(self):
        if self['preferredShard'] in self.shards:
            self.shards[self['preferredShard']]['state'] = DGG.DISABLED
            self.shards[self['preferredShard']]['relief'] = DGG.FLAT
            self.shards[self['preferredShard']]['text3_fg'] = self.textSelectedColor

        if hasattr(self, 'currentShardLabel'):
            district = base.cr.doId2do.get(self['preferredShard'])
            if district:
                self.currentShardLabel['text'] = '\x01gold\x01' + PLocalizer.ShardPreferredWorld + ' :\n%s %s\x02' % (district.getName(), PLocalizer.Ocean)
            else:
                self.currentShardLabel['text'] = '\x01gold\x01' + PLocalizer.ShardPreferredWorld + ' :\n%s\x02' % PLocalizer.ShardNone

    def getShardText(self, name, avCount):
        return '%-20s:%8d' % (name, avCount)

    def updateAvCount(self, id, avatarCount):
        sLabel = self.shards.get(id)
        if sLabel:
            sLabel.avCount = avatarCount
            sLabel.popLabel['image_color'] = self.getPopColor(id, avatarCount, sLabel.min, sLabel.max)
            if self.showPop:
                sLabel.popLabel['text'] = str(avatarCount)
            else:
                sLabel.popLabel['text'] = str(self.getPopText(avatarCount, sLabel.min, sLabel.max))
            self.updateLabelState(id)

    def updatePopLimits(self, id, min, max):
        sLabel = self.shards.get(id)
        if sLabel:
            sLabel.min = min
            sLabel.max = max
            sLabel.popLabel['image_color'] = self.getPopColor(id, sLabel.avCount, min, max)
            if self.showPop:
                sLabel.popLabel['text'] = str(sLabel.avCount)
            else:
                sLabel.popLabel['text'] = str(self.getPopText(sLabel.avCount, min, max))
            self.updateLabelState(id)

    def updateLabelState(self, id):
        sLabel = self.shards.get(id)
        if sLabel:
            if sLabel.avCount < sLabel.max or self.teleportAll or (hasattr(base, 'localAvatar') and base.localAvatar.getAdminAccess() >= 110):
                sLabel['state'] = DGG.NORMAL
                sLabel['relief'] = DGG.RAISED
            else:
                sLabel['state'] = DGG.DISABLED
                sLabel['relief'] = DGG.FLAT

    def startListening(self):
        self.accept('ShardPopulationUpdate', self.handleShardPopulationUpdate)
        self.accept('ShardPopLimitsUpdate', self.handleShardPopLimitsUpdate)
        
        for shardId, shard in base.cr.activeDistrictMap.iteritems():
            self.handleShardPopulationUpdate(shardId, shard.avatarCount)
            self.handleShardPopLimitsUpdate(shardId, *shard.populationLimits)

    def stopListening(self):
        self.ignore('ShardPopulationUpdate')
        self.ignore('ShardPopLimitUpdate')

    def shardButtonPressed(self, shardId):
        if not self['inverted']:
            for id in self.shards:
                self.updateLabelState(id)
        else:
            for id in self.shards:
                self.updateLabelState(id)
                self.shards[id]['text3_fg'] = self.textDisabledColor

        if hasattr(base, 'localAvatar') and localAvatar.guiMgr.crewHUD.crew:
            localAvatar.guiMgr.handleLeaveCrewWarning(shardId)
        else:
            shard = base.cr.activeDistrictMap[shardId]

            if not shard.hasAdminAccess():
                name = '\x01%s\x01%ss\x02' % PLocalizer.MasterNametags[shard.minimumAdminAccess]
                self.removeAlertDialog()
                
                self.alertDialog = PDialog.PDialog(text = PLocalizer.VIPServerWarning % name, text_align = TextNode.ACenter, text_wordwrap=25, style = OTPDialog.Acknowledge, command = self.removeAlertDialog)
                self.alertDialog.show()
                return

            self['preferredShard'] = shardId
            self['shardSelected'](shardId)

    def shardSelected(self, shardId):
        self.handleButtonPressed()
        localAvatar.guiMgr.hideSeaChest()
        base.cr.teleportMgr.requestTeleport(PiratesGlobals.INSTANCE_MAIN, 'piratesWorld', shardId)
