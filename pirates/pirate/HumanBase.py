from panda3d.core import Texture
from pirates.pirate import HumanDNA

class HumanBase:

    def __init__(self):
        self.style = None

    def setDNA(self, dna=None):
        self.setDNAString(dna)

    def setDNAString(self, dnaString=None):
        if isinstance(dnaString, HumanDNA.HumanDNA):
            dnaString = dnaString.makeNetString()

        self.style = HumanDNA.HumanDNA()

        if dnaString:
            self.style.makeFromNetString(dnaString)

    def setDefaultDNA(self):
        self.style = HumanDNA.HumanDNA()

    def setTutorial(self, val):
        self.style.setTutorial(val)

    def setName(self, val):
        pass

    def setGender(self, val):
        self.style.setGender(val)

    def setBodyShape(self, val):
        self.style.setBodyShape(val)

    def setBodyHeight(self, val):
        self.style.setBodyHeight(val)

    def setBodyColor(self, val):
        self.style.setBodyColor(val)

    def setBodySkin(self, val):
        self.style.setBodySkin(val)

    def setHeadSize(self, val):
        self.style.setHeadSize(val)

    def setHeadWidth(self, val):
        self.style.setHeadWidth(val)

    def setHeadHeight(self, val):
        self.style.setHeadHeight(val)

    def setHeadRoundness(self, val):
        self.style.setHeadRoundness(val)

    def setJawWidth(self, val):
        self.style.setJawWidth(val)

    def setJawRoundness(self, val):
        self.style.setJawRoundness(val)

    def setJawAngle(self, val):
        self.style.setJawAngle(val)

    def setJawLength(self, val):
        self.style.setJawLength(val)

    def setMouthWidth(self, val):
        self.style.setMouthWidth(val)

    def setMouthLipThickness(self, val):
        self.style.setMouthLipThickness(val)

    def setMouthFrown(self, val):
        self.style.setMouthFrown(val)

    def setCheekBoneHeight(self, val):
        self.style.setCheekBoneHeight(val)

    def setCheekBoneWidth(self, val):
        self.style.setCheekBoneWidth(val)

    def setCheekFat(self, val):
        self.style.setCheekFat(val)

    def setBrowWidth(self, val):
        self.style.setBrowWidth(val)

    def setBrowProtruding(self, val):
        self.style.setBrowProtruding(val)

    def setBrowAngle(self, val):
        self.style.setBrowAngle(val)

    def setBrowHeight(self, val):
        self.style.setBrowHeight(val)

    def setEyeCorner(self, val):
        self.style.setEyeCorner(val)

    def setEyeOpeningSize(self, val):
        self.style.setEyeOpeningSize(val)

    def setEyeBulge(self, val):
        self.style.setEyeBulge(val)

    def setNoseBridgeWidth(self, val):
        self.style.setNoseBridgeWidth(val)

    def setNoseNostrilWidth(self, val):
        self.style.setNoseNostrilWidth(val)

    def setNoseLength(self, val):
        self.style.setNoseLength(val)

    def setNoseBump(self, val):
        self.style.setNoseBump(val)

    def setNoseNostrilHeight(self, val):
        self.style.setNoseNostrilHeight(val)

    def setNoseNostrilAngle(self, val):
        self.style.setNoseNostrilAngle(val)

    def setNoseNostrilIndent(self, val):
        self.style.setNoseNostrilIndent(val)

    def setNoseBridgeBroke(self, val):
        self.style.setNoseBridgeBroke(val)

    def setNoseNostrilBroke(self, val):
        self.style.setNoseNostrilBroke(val)

    def setEarScale(self, val):
        self.style.setEarScale(val)

    def setEarFlapAngle(self, val):
        self.style.setEarFlapAngle(val)

    def setEarPosition(self, val):
        self.style.setEarPosition(val)

    def setEarLobe(self, val):
        self.style.setEarLobe(val)

    def setHeadTexture(self, val):
        self.style.setHeadTexture(val)

    def setEyesColor(self, val):
        self.style.setEyesColor(val)

    def setHairHair(self, val):
        self.style.setHairHair(val)

    def setHairBeard(self, val):
        self.style.setHairBeard(val)

    def setHairMustache(self, val):
        self.style.setHairMustache(val)

    def setHairColor(self, val):
        self.style.setHairColor(val)

    def setHatIdx(self, val):
        self.style.setHatIdx(val)

    def setHatTexture(self, val):
        self.style.setHatTexture(val)

    def setHatColor(self, val):
        self.style.setHatColor(val)

    def setClothesByType(self, type, val1, val2, val3 = -1):
        self.style.setClothesByType(type, val1, val2, val3)

    def setClothesShirt(self, val1, val2):
        self.style.setClothesShirt(val1, val2)

    def setClothesPant(self, val1, val2):
        self.style.setClothesPant(val1, val2)

    def setClothesSock(self, val1, val2):
        self.style.setClothesSock(val1, val2)

    def setClothesShoe(self, val1, val2):
        self.style.setClothesShoe(val1, val2)

    def setClothesVest(self, val1, val2):
        self.style.setClothesVest(val1, val2)

    def setClothesCoat(self, val1, val2):
        self.style.setClothesCoat(val1, val2)

    def setClothesBelt(self, val1, val2):
        self.style.setClothesBelt(val1, val2)

    def setClothesTopColor(self, val1, val2, val3):
        self.style.setClothesTopColor(val1, val2, val3)

    def setClothesBotColor(self, val1, val2, val3):
        self.style.setClothesBotColor(val1, val2, val3)

    def setTattooChest(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooChest(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone2(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone2(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone3(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone3(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone4(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone4(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone5(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone5(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone6(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone6(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone7(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone7(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone8(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.setTattooZone8(tattoo, offsetX, offsetY, scale, rotate, color)

    def setJewelryZone1(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone1(val, primary, secondary)

    def setJewelryZone2(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone2(val, primary, secondary)

    def setJewelryZone3(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone3(val, primary, secondary)

    def setJewelryZone4(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone4(val, primary, secondary)

    def setJewelryZone5(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone5(val, primary, secondary)

    def setJewelryZone6(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone6(val, primary, secondary)

    def setJewelryZone7(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone7(val, primary, secondary)

    def setJewelryZone8(self, val, primary = 0, secondary = 0):
        self.style.setJewelryZone8(val, primary, secondary)