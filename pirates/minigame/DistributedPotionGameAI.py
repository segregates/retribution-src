from direct.distributed.DistributedObjectAI import *
from direct.directnotify import DirectNotifyGlobal

from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals

import PotionRecipeData, PotionGlobals

'''
dclass DistributedPotionGame : DistributedObject {
  setColorSet(uint8(0-5)) required;
  start(uint8(0-5));
  completeRecipe(uint8, bool) clsend airecv;
  claimXPBonus(uint8(0-17)) clsend airecv;
  completeSurvival(uint32, uint32) clsend airecv;
  setHintsActive(bool) clsend airecv;
  setXpBonus(uint32) broadcast;
  stop();
  reset() clsend airecv;
  checkExit();
  finish() clsend airecv;
};
'''

class DistributedPotionGameAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionGameAI')

    def __init__(self, air, avId):
        DistributedObjectAI.__init__(self, air)
        self.avId = avId
        self.av = self.air.doId2do[avId]

        self.__workingRecipe = -1
        self.__numIngredientsDone = 0
        self.__bonus = 0

        self.recipes = {}
        for recipeData in PotionRecipeData.PotionRecipeList:
            if not recipeData.get('disabled', False):
                if self.av.inventory.getCategoryLevel(InventoryType.PotionsRep) >= recipeData['level']:
                    self.recipes[recipeData['potionID']] = len(recipeData['ingredients'])

    def getColorSet(self):
        return 0 # Disney is fucking retarded, this is determined by client

    def completeRecipe(self, recipe, flag):
        if self.air.getAvatarIdFromSender() != self.avId:
            return

        if self.__workingRecipe == -1:
            if not self.recipes.get(recipe):
                msg = 'recipe invalid: %d; self.recipes = %r' % (recipe, self.recipes)
                self.notify.warning(msg)
                return

            self.__workingRecipe = recipe

        elif recipe != self.__workingRecipe:
            msg = 'tried to complete recipe they are not working on: %d (%d)' % (recipe, self.__workingRecipe)
            self.notify.warning(msg)
            return

        self.__numIngredientsDone += 1
        if self.__numIngredientsDone >= self.recipes[recipe]:
            self.notify.debug("recipe done %s" %  recipe)

            potionGiven = self.givePotion(recipe)
            if not potionGiven:
                self.air.writeServerEvent('recipe-error', avId=self.avId, recipe=recipe, message='Failed to give player potion from PotionGame')

            self.air.writeServerEvent('recipe-done', avId=self.avId, recipe=recipe)
            self.av.addReputation(InventoryType.PotionsRep, PotionGlobals.getPotionBuffXP(recipe))
            self.reset()

        self.av.addReputation(InventoryType.PotionsRep, 25)

    def givePotion(self, recipeId):
        recipe = PotionRecipeData.getRecipeFromPotionId(recipeId)
        if recipe == None:
            self.notify.warning("Unable to give potion. PotionID (%s) not in PotionRecipeList" % recipeId)
            return False

        inv = self.av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % self.avId)
            return False

        if not 'potionID' in recipe:
            self.notify.warning("Unable to give potion. No potionID defined in recipe")
            return False

        potionId = PotionGlobals.potionBuffIdToInventoryTypeId(recipe['potionID'])
        location = inv.findAvailableLocation(InventoryType.ItemTypeConsumable, itemId=potionId, count=1)
        if location != -1:
            success = inv.addLocatable(potionId, location, 1)
            if not success:
                self.notify.warning("Failed to add potion to players inventory. AvId: %s" % self.avId)
                return False
            return True
        return False

    def completeSurvival(self, ingredientsMade, tilesUsed):
        if self.air.getAvatarIdFromSender() != self.avId:
            return

        # TO DO

    def claimXPBonus(self, bonus):
        if self.air.getAvatarIdFromSender() != self.avId:
            return

        if bonus >= len(PotionGlobals.BONUS_XP_AMT):
            # Trying to cheat? No bonus for ya!
            bonus = -1
            self.air.writeServerEvent('suspisious', avId=self.avId, bonus=bonus, message="Bonus greater then BONUS_XP_AMT")

        self.__bonus = bonus

        rep = 10 * (self.__bonus + 1)
        self.av.inventory.addReputation(InventoryType.PotionsRep, rep)
        self.av.repChanged()

    def reset(self):
        if self.air.getAvatarIdFromSender() != self.avId:
            return

        self.__workingRecipe = -1
        self.__numIngredientsDone = 0
        self.__bonus = 0

    def finish(self):
        if self.air.getAvatarIdFromSender() != self.avId:
            return

        self.reset()
        self.sendUpdateToAvatarId(self.avId, 'checkExit', [])
        messenger.send(self.uniqueName('potiongame-exit'))
