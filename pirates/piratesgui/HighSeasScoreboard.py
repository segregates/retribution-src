from panda3d.core import TextNode, VBase4
# File: p (Python 2.4)

from direct.gui.DirectGui import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import Scoreboard
from pirates.piratesgui import DialogButton
from pirates.piratesgui import GuiButton
from pirates.ai import HolidayGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.economy import EconomyGlobals
from pirates.ship import ShipGlobals
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import InventoryUIPlunderGridContainer
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
import time
from pirates.piratesgui import MessageGlobals

class HighSeasScoreboard(GuiPanel.GuiPanel):
    width = PiratesGuiGlobals.PortPanelWidth
    height = PiratesGuiGlobals.PortPanelHeight
    titleHeight = PiratesGuiGlobals.PortTitleHeight
    buffer = 0.050000

    def __init__(self, name, stats, playerStats, ship):
        GuiPanel.GuiPanel.__init__(self, '', self.width, self.height, showClose = False)
        self.ship = ship
        self.stats = stats
        self.playerStats = playerStats
        self.plunderHeight = 1.64
        self.initialiseoptions(HighSeasScoreboard)
        self.leftPanel = None
        self.rightPanel = None
        self.addedLootInfoText = 0
        self.autoPlundered = 0
        self.preAutoPlundered = 0
        self.displayedGold = 0
        titleTxt = PLocalizer.ScoreboardTitle
        if self.ship.shipClass == ShipGlobals.BLACK_PEARL:
            titleTxt = PLocalizer.BlackPearlScoreboard
        else:
            titleTxt = PLocalizer.LootScoreboard
        self.title = DirectLabel(parent = self, relief = None, text = titleTxt, text_align = TextNode.ALeft, text_scale = self.titleHeight, text_fg = PiratesGuiGlobals.TextFG10, text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.0299, 0, self.height - self.titleHeight - 0.0299), text_font = PiratesGlobals.getPirateOutlineFont(), textMayChange = 1)
        self.closeButton = DialogButton.DialogButton(parent = self, buttonStyle = DialogButton.DialogButton.NO, text = PLocalizer.lClose, pos = (1.05, 0, 0.074), command = self.closePanel)
        self.labels = []
        self.grids = { }
        self.manager = base.localAvatar.guiMgr.inventoryUIManager
        self.buttonSize = self.manager.standardButtonSize
        main_gui = loader.loadModel('models/gui/gui_main')
        generic_x = main_gui.find('**/x2')
        generic_box = main_gui.find('**/exit_button')
        generic_box_over = main_gui.find('**/exit_button_over')
        main_gui.remove_node()
        self.newCloseButton = GuiButton.GuiButton(parent = self, relief = None, pos = (2.28, 0, 1.08), image = (generic_box, generic_box, generic_box_over, generic_box), image_scale = 0.4, command = self.closePanel)
        xButton = OnscreenImage(parent = self.newCloseButton, image = generic_x, scale = 0.200, pos = (-0.256, 0, 0.766))
        gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))
        gui.remove_node()
        self.takeAllButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.348, 1.0, 0.22), image0_color = VBase4(0.65, 0.65, 0.65, 1), image1_color = VBase4(0.4, 0.4, 0.4, 1), image2_color = VBase4(0.9, 0.9, 0.9, 1), image3_color = VBase4(0.408, 0.4, 0.4, 1), text = PLocalizer.InventoryPlunderTakeAll, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (1.3, 0, 0.074), command = self.takeAllLoot)
        self.takeAllIncidentalsButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.348, 1.0, 0.22), image0_color = VBase4(0.65, 0.65, 0.65, 1), image1_color = VBase4(0.4, 0.4, 0.4, 1), image2_color = VBase4(0.9, 0.9, 0.9, 1), image3_color = VBase4(0.408, 0.4, 0.4, 1), text = PLocalizer.InventoryPlunderTakeAllSundries, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.800000, 0, 0.074), command = self.requestAllIncidentals)
        self.setBin('gui-fixed', -1)
        self.autoLootList = [
            InventoryType.ItemTypeMoney,
            InventoryCategory.MONEY]
        self.incidentalsList = [
            InventoryType.ItemTypeMoney,
            InventoryType.ItemTypeConsumable,
            InventoryType.TreasureCollection,
            InventoryCategory.CARDS,
            InventoryCategory.MONEY,
            InventoryCategory.WEAPON_PISTOL_AMMO,
            InventoryCategory.WEAPON_GRENADE_AMMO,
            InventoryCategory.WEAPON_CANNON_AMMO,
            InventoryCategory.WEAPON_DAGGER_AMMO]
        self.incidentalsDict = { }
        base.hss = self
        self.initFlag = 0
        self.initPlunder()


    def startInitTask(self):
        taskMgr.add(self.startHHPlunderTask, 'startHHPlunderTask')


    def startHHPlunderTask(self, task = None):
        if self.isHidden():
            return task.cont
        elif self.initFlag == 0:
            self.initPlunder()

        taskMgr.remove('startHHPlunderTask')
        return task.done


    def initPlunder(self):
        self.createScoreboard()
        self.requestAutoLoot()
        self.arrangeGrids()
        self.accept('lootsystem-plunderContainer-Empty', self.onEmptyContainer, [
            False])
        self.initFlag = 1


    def destroy(self):
        self.ignore('lootsystem-plunderContainer-Empty')
        taskMgr.remove('prePlunderHighSeasLootPanel')
        self.labels = []
        if self.leftPanel:
            self.leftPanel.destroy()
            self.leftPanel = None

        if self.rightPanel:
            self.rightPanel.destroy()
            self.rightPanel = None

        for grid in self.grids.values():
            grid.destroy()

        self.grids = { }
        if self.manager:
            self.manager.removeScoreboard()
            self.manager = None

        GuiPanel.GuiPanel.destroy(self)


    def getMissionResults(self):
        (missionTime, shipDamage, skeletonKills, navyKills, creatureKills, seamonsterKills, pirateKills, townfolkKills, shipKills, repairCost, exp, gold, cargo, numCrew) = self.stats
        (pMissionTime, pShipDamage, pSkeletonKills, pNavyKills, pCreatureKills, pSeamonsterKills, pPirateKills, pTownfolkKills, pShipKills, pRepairCost, pExp, pGold, pCargo, pLootBoxes, dummyCrew) = self.playerStats

        t = time.gmtime(missionTime)
        totalTime = str(t[3]) + '"' + str(t[4]) + "'" + str(t[5])
        self.cargo = cargo
        cargoValue = EconomyGlobals.getCargoTotalValue(cargo)
        totalGold = max(cargoValue + gold - repairCost, 0)
        self.results = []
        self.results.append({
            'Type': 'Title',
            'Text': PLocalizer.PlunderedLootContainers,
            'Value1': '' })
        if len(pLootBoxes) == 0:
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.NoLootContainersPlundered,
                'Value1': '',
                'UnwrapMode': 1 })
        else:
            gold = 0
            height = self.plunderHeight
            for lootBox in pLootBoxes:
                plunderList = lootBox[1]
                gridText = self.getLootLabel(lootBox[2])
                self.makeLootLabel(gridText, self.plunderHeight)
                grid = self.setupPlunderGrid(plunderList, height, lootBox[0])
                grid.gridText = gridText

            self.manager.addScoreboard(self)
        return self.results


    def arrangeGrids(self):
        for label in self.labels:
            label.destroy()

        height = self.plunderHeight
        headingHeight = 0.0299
        marginHeight = 0.100
        containerCount = 0
        for grid in self.grids.values():
            gridHasStuff = 0
            for cell in grid.cellList:
                if cell.inventoryItem:
                    gridHasStuff = 1
                    continue

            if gridHasStuff:
                self.makeLootLabel(grid.gridText, height)
                height -= headingHeight
                gridHeight = grid.plunderRows / 2
                zPos = height - self.buttonSize * float(gridHeight)
                grid.setPos(0.100, 0, zPos)
                plunderLength = len(grid.cellList)
                plunderHeight = (int(len(grid.cellList)) / 2 + len(grid.cellList) % 2) * self.buttonSize
                height -= plunderHeight
                height -= marginHeight
                continue
            if not grid.isEmpty():
                continue



    def getCargoResults(self):
        (missionTime, shipDamage, skeletonKills, navyKills, creatureKills, seamonsterKills, pirateKills, townfolkKills, shipKills, repairCost, exp, gold, cargo, numCrew) = self.stats
        (pMissionTime, pShipDamage, pSkeletonKills, pNavyKills, pCreatureKills, pSeamonsterKills, pPirateKills, pTownfolkKills, pShipKills, pRepairCost, pExp, pGold, pCargo, pLootBoxes, dummyCrew) = self.playerStats

        avId = base.localAvatar.getDoId()
        cargoValue = EconomyGlobals.getCargoTotalValue(pCargo)
        totalGold = cargoValue + pGold
        bonusGold = 0
        if base.localAvatar.ship:
            if base.localAvatar.ship.getOwnerId() == avId and len(base.localAvatar.ship.getCrew()) > 1:
                bonusGold = int(totalGold * EconomyGlobals.CAPTAIN_LOOT_MULTIPLIER)
                totalGold += bonusGold
        
        totalGold *= 2

        netGold = totalGold - pRepairCost
        self.results = []
        self.results.append({
            'Type': 'Title',
            'Text': PLocalizer.CargoPlunder,
            'Value1': '' })
        if pGold:
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.GoldLooted,
                'Value1': pGold,
                'Value2': gold })

        if len(pCargo) == 0:
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.NoCargoLooted,
                'Value1': '',
                'UnwrapMode': 1 })
        else:
            cargoDict = { }
            for itemId in pCargo:
                cargoCount = cargoDict.get(itemId, None)
                if cargoCount == None:
                    cargoDict[itemId] = 0

                cargoDict[itemId] += 1

            for cargoKey in cargoDict:
                amount = cargoDict[cargoKey]
                self.results.append({
                    'Type': 'Cargo',
                    'Text': '',
                    'Value1': cargoKey,
                    'UnwrapMode': 1,
                    'Amount': amount })

        if bonusGold > 0:
            self.results.append({
                'Type': 'Space',
                'Text': '',
                'Value1': '',
                'UnwrapMode': 1 })
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.CaptainsBonus,
                'Value1': str(bonusGold) + ' ' + PLocalizer.MoneyName,
                'UnwrapMode': 1 })

        
        self.results.append({
            'Type': 'Space',
            'Text': '',
            'Value1': '',
            'UnwrapMode': 1 })
        self.results.append({
            'Type': 'Entry',
            'Text': PLocalizer.DoubleGoldBonus,
            'Value1': str(totalGold / 2) + ' ' + PLocalizer.MoneyName,
            'UnwrapMode': 1 })

        self.results.append({
            'Type': 'Space',
            'Text': '',
            'Value1': '',
            'UnwrapMode': 1 })
        self.results.append({
            'Type': 'Title',
            'Text': PLocalizer.PlunderShare,
            'Value1': str(netGold) + ' ' + PLocalizer.MoneyName,
            'UnwrapMode': 1 })
        return self.results


    def createScoreboard(self):
        (pMissionTime, pShipDamage, pSkeletonKills, pNavyKills, pCreatureKills, pSeamonsterKills, pPirateKills, pTownfolkKills, pShipKills, pRepairCost, pExp, pGold, pCargo, pLootBoxes, dummyCrew) = self.playerStats
        missionResults = self.getMissionResults()
        self.leftPanel = Scoreboard.Scoreboard('', (self.width - self.buffer * 2) / 2.0, self.height - 0.100, missionResults, self.titleHeight)
        self.leftPanel.reparentTo(self)
        self.leftPanel.setPos(self.buffer, 0, 0.200)
        cargoResults = self.getCargoResults()
        self.rightPanel = Scoreboard.Scoreboard('', (self.width - self.buffer * 2) / 2.0, self.height - 0.100, cargoResults, self.titleHeight)
        self.rightPanel.reparentTo(self)
        self.rightPanel.setPos((self.width + self.buffer) / 2.0, 0, 0.200)
        if len(pLootBoxes) == 0:
            self.leftPanel.hide()
            self.configure(frameSize = (self.width / 4.0, self.width * 3.0 / 4.0, 0, self.height))
            self.title.setX(self.width / 4.0 + 0.0299)
            self.rightPanel.setX(self.width / 4.0 + self.buffer)

        if len(pLootBoxes) == 0 and len(pCargo) == 0:
            self.takeAllButton.hide()
            self.newCloseButton.hide()
        elif len(pLootBoxes) == 0:
            self.closeButton.hide()
            self.newCloseButton.setX(1.77)
        else:
            self.closeButton.hide()


    def getListFinishedMessage(self):
        return 'listFinished'


    def setupPlunderGrid(self, plunderList, height, containerId):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            plunderLength = len(plunderList)
            odd = plunderLength % 2
            if odd:
                plunderLength += 1

            gridHeight = plunderLength / 2
            grid = InventoryUIPlunderGridContainer.InventoryUIPlunderGridContainer(self.manager, self.buttonSize * 6.5, self.buttonSize * float(gridHeight), 2, gridHeight)
            grid.reparentTo(self)
            zPos = height - self.buttonSize * float(gridHeight)
            grid.setupPlunder(plunderList)
            grid.plunderRows = plunderLength
            self.grids[containerId] = grid
            return grid



    def getLootLabel(self, lootType):
        gridText = 'Error Loot'
        if lootType == PiratesGlobals.ITEM_SAC:
            gridText = PLocalizer.LootContainerItemSac
        elif lootType == PiratesGlobals.TREASURE_CHEST:
            gridText = PLocalizer.LootContainerTreasureChest
        elif lootType == PiratesGlobals.RARE_CHEST:
            gridText = PLocalizer.LootContainerRareChest
        elif lootType == PiratesGlobals.UPGRADE_CHEST:
            gridText = PLocalizer.LootContainerUpgradeChest
        elif lootType == PiratesGlobals.RARE_UPGRADE_CHEST:
            gridText = PLocalizer.LootContainerRareUpgradeChest

        return gridText


    def onEmptyContainer(self, event = None):
        self.checkAllContainers()


    def checkAllContainers(self, event = None):
        self.arrangeGrids()
        panelHasStuff = 0
        for grid in self.grids.values():
            for cell in grid.cellList:
                if cell.inventoryItem:
                    panelHasStuff = 1
                    continue


        if not panelHasStuff:
            if not self.isEmpty():
                self.closePanel()




    def takeAllLoot(self, playSound = True):
        if not self.grids:
            if not self.isEmpty():
                self.closePanel()

            return None

        self.manager.takeAllLoot(self.grids.values(), playSound = playSound)
        self.checkAllContainers()


    def makeLootLabel(self, text, height):
        label = DirectLabel(parent = self, relief = None, text = text, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.100, 0, height))
        self.labels.append(label)


    def payForShipRepairs(self):
        self.ship.requestRepairAll()


    def getShowNextItemMessage(self):
        return 'showNextHighSeaStat'


    def closePanel(self):
        GuiPanel.GuiPanel.closePanel(self)
        self.destroy()
        messenger.send('highSeasScoreBoardClose')



    def handleAutoPlunderCell(self, cell, task = None):
        self.requestAutoLoot()


    def requestAutoLoot(self):
        self.requestAllIncidentals(stackOnly = True, autoLoot = 1)
        if not (self.displayedGold) and self.rightPanel:
            goldAmount = self.incidentalsDict.get((InventoryType.ItemTypeMoney, InventoryType.GoldInPocket), 0)
            if goldAmount:
                newItem = {
                    'Type': 'Title',
                    'Text': PLocalizer.PlunderGold,
                    'Value1': str(goldAmount) + ' ' + PLocalizer.MoneyName,
                    'UnwrapMode': 1 }
                self.rightPanel.addNewResult(newItem)
                self.displayedGold = 1


        for lootKey in self.incidentalsDict:
            lootAmount = self.incidentalsDict[lootKey]
            if lootKey[0] == InventoryCategory.MONEY:
                self.checkForAddLootInfoText()
                moneyName = PLocalizer.InventoryTypeNames.get(lootKey[1], 'No Name')
                newItem = {
                    'Type': 'ShipMaterial',
                    'Text': '',
                    'Value1': lootKey[1],
                    'UnwrapMode': 1,
                    'Amount': lootAmount }
                self.rightPanel.addNewResult(newItem)
                continue

        if self.rightPanel:
            self.rightPanel.list.redraw()
            self.rightPanel.fixHeight()



    def checkForAddLootInfoText(self):
        if not (self.addedLootInfoText) and self.rightPanel:
            self.addedLootInfoText = 1
            newItem = {
                'Type': 'MaterialText',
                'Text': '',
                'Value1': 0,
                'UnwrapMode': 1,
                'Amount': 0 }
            self.rightPanel.addNewResult(newItem)
        else:
            return None


    def requestAllIncidentals(self, stackOnly = False, autoLoot = 0):
        (pMissionTime, pShipDamage, pSkeletonKills, pNavyKills, pCreatureKills, pSeamonsterKills, pPirateKills, pTownfolkKills, pShipKills, pRepairCost, pExp, pGold, pCargo, pLootBoxes, dummyCrew) = self.playerStats
        checkList = self.incidentalsList
        if autoLoot:
            checkList = self.autoLootList

        for gridId in self.grids:
            grid = self.grids.get(gridId)
            if grid:
                for cell in grid.cellList:
                    if cell.inventoryItem:
                        if cell.inventoryItem.itemTuple[0] in checkList:
                            if not stackOnly or cell.inventoryItem.canStack:
                                itemInfo = cell.inventoryItem.itemTuple
                                lootKey = self.getLootKey(cell.inventoryItem)
                                itemEntry = self.incidentalsDict.get(lootKey, None)
                                if not itemEntry:
                                    self.incidentalsDict[lootKey] = 0

                                self.incidentalsDict[lootKey] += cell.inventoryItem.amount
                                self.manager.takePlunderItemFromCell(cell)

                        continue




    def getLootKey(self, item):
        return (item.getCategory(), item.getId())


    def printIncidentalsTaken(self):
        for itemKey in self.incidentalsDict:
            pass
