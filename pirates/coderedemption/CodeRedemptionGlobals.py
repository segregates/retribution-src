from otp.otpbase import OTPLocalizer
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.ai import HolidayGlobals
NEVER_EXPIRE = 0
EXPIRE_ON_REDEEM = 1
EXPIRE_AFTER_N_REDEMPTIONS = 2
DATE_DEPENDENT_EXPIRE_ON_REDEEM = 3
DATE_DEPENDENT_EXPIRE_AFTER_N_REDEMPTIONS = 4
ERROR_ID_GOOD = 0
ERROR_ID_BAD = 1
ERROR_ID_OVERFLOW = 2
ERROR_ID_TIMEOUT = 3
TIMEOUT_DURATION = 10
CODE_TYPES = {
    0: 'Never Expire',
    1: 'Expire on Redeem',
    2: 'Expire after n redemptions',
    3: 'Date Dependent Expire on Redeem',
    4: 'Date Dependent Expire after n redemptions' }
NORMAL_INVENTORY = 1
CLOTHING = 2
JEWELRY = 3
TATTOO = 4
HAIR = 5

class AwardTypes:
    GOLD = 1
    FREE_HAT = 2
    KRAKEN_TATTOO = 3
    DARKFIRE_CUTLASS = 4
    FLATULENT_FIZZ = 5
    BUCCANEER_HAT = 6
    SEAFANG_BLADE = 7
    SWORD_OF_TRITON = 8
    HAYMAKER_PISTOL = 9
    ZOMBIE_KABAB_BAYONET = 10
    SPECTRAL_CUTLASS = 11
    NEMESIS_BLADE = 12
    DARKFROST_BLADE = 13
    SUPER_XP_POTION = 14
    SCOUNDREL_HAT = 15
    GOLDEN_KNUCKLES = 16
    NORRINGTONS_SPYGLASS = 17
    ELIXIR = 18
    POTION_HEADFIRE = 19
    POTION_INVIS_2 = 20
    JACK_SPARROW_BLADE = 21
    JACK_SPARROW_REVENGE = 22
    HEART_OF_PADRES = 23
    AMMO_FURY = 24
    LOST_BLADE_OF_LEVIATHAN = 25
    LOST_SWORD_OF_EL_PATRON = 26
    BARBOSSAS_FURY = 27
    RUSTY_SCIMITAR = 28
    SCIMITAR_46 = 29
    SCIMITAR_47 = 30
    SCIMITAR_48 = 31
    POTION_SUMMON_CHICKEN = 32
    POTION_SUMMON_WASP = 33
    POTION_SUMMON_DOG = 34
    TREASURE = 35
    DUAL_CUTLASSES = 36
    BOARDING_AXE = 37
    HALLOWEEN = 38
    THANKSGIVING = 39
    SANTA = 40
    WINTER = 41
    WONDERLAND = 42
    SAVVY20K = 43
    TYPE_IDX = 0
    MALE_IDX = 1
    FEME_IDX = 2
    QTTY_IDX = 3
    DESC_IDX = 4

AWARD_ID = {
    AwardTypes.GOLD: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeMoney, 0)),
        None,
        200,
        PLocalizer.CodeRedemptionGold],   
    AwardTypes.FREE_HAT: [
        CLOTHING,
        InvItem((InventoryType.ItemTypeClothing, ItemGlobals.CROSSBONES_BANDANA, 0, 0)),
        InvItem((InventoryType.ItemTypeClothing, ItemGlobals.CROSSBONES_BANDANA, 0, 0)),
        1,
        PLocalizer.CodeRedemptionFreeHat],
    AwardTypes.KRAKEN_TATTOO: [
        TATTOO,
        InvItem((InventoryType.ItemTypeTattoo, ItemGlobals.TATTOO_ARM_OCTOPUS_SLEEVES, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionKrakenTattoo],
    AwardTypes.DARKFIRE_CUTLASS: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.DARKFIRE_CUTLASS, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionDarkfireCutlass],
    AwardTypes.FLATULENT_FIZZ: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_FART_2, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionFlatulentFizz],
    AwardTypes.BUCCANEER_HAT: [
        CLOTHING,
        InvItem((InventoryType.ItemTypeClothing, ItemGlobals.BLACK_BUCCANEER_HAT, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionBlackBuccaneerHat],
    AwardTypes.SEAFANG_BLADE: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.SEAFANG_BLADE, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionSeafangBlade],
    AwardTypes.SWORD_OF_TRITON: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.SWORD_OF_TRITON, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionSwordOfTriton],
    AwardTypes.HAYMAKER_PISTOL: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.HAYMAKER_PISTOL, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionHaymakerPistol],
    AwardTypes.ZOMBIE_KABAB_BAYONET: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.ZOMBIE_KABAB_BAYONET, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionZombieKababBayonet],
    AwardTypes.SPECTRAL_CUTLASS: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.SPECTRAL_CUTLASS, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionSpectralCutlass],
    AwardTypes.NEMESIS_BLADE: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.NEMESIS_BLADE, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionNemesisBlade],
    AwardTypes.DARKFROST_BLADE: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.DARKFROST_BLADE, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionDarkfrostBlade],
    AwardTypes.SUPER_XP_POTION: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_REP_COMP, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionSuperReputationPotion],
    AwardTypes.SCOUNDREL_HAT: [
        CLOTHING,
        InvItem((InventoryType.ItemTypeClothing, ItemGlobals.CRIMSON_BUCCANEER_HAT, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionScoundrelHat],
    AwardTypes.GOLDEN_KNUCKLES: [
        JEWELRY,
        InvItem((InventoryType.ItemTypeJewelry, ItemGlobals.GOLDEN_KNUCKLES, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionGoldenKnuckles],
    AwardTypes.NORRINGTONS_SPYGLASS: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeCharm, ItemGlobals.NORRINGTON_SPYGLASS, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionNorringtonsSpyglass],
    AwardTypes.ELIXIR: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.ELIXIR, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionElixir],
    AwardTypes.POTION_HEADFIRE: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_HEADONFIRE, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionPotionHeadOnFire],
    AwardTypes.POTION_INVIS_2: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_INVIS_2, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionPotionInvis2],
    AwardTypes.JACK_SPARROW_BLADE: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.JACK_SPARROW_BLADE, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionJackSparrowBlade],
    AwardTypes.JACK_SPARROW_REVENGE: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.JACK_SPARROW_REVENGE, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionJackSparrowRevenge],
    AwardTypes.HEART_OF_PADRES: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.HEART_OF_PADRES_DEL_FUEGO, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionHeartOfPadres],
    AwardTypes.AMMO_FURY: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.AmmoFury, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionAmmoFury],
    AwardTypes.LOST_BLADE_OF_LEVIATHAN: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.CURSED_BLADE_47, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionLostBladeOfLeviathan],
    AwardTypes.LOST_SWORD_OF_EL_PATRON: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.LOST_SWORD_OF_EL_PATRON, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionLostSwordOfElPatron],
    AwardTypes.BARBOSSAS_FURY: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.BARBOSSA_FURY, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionBarbossaFury],
    AwardTypes.RUSTY_SCIMITAR: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.RUSTY_SCIMITAR, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionRustyScimitar],
    AwardTypes.SCIMITAR_46: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.SCIMITAR_46, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionScimitar46],
    AwardTypes.SCIMITAR_47: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.SCIMITAR_47, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionScimitar47],
    AwardTypes.SCIMITAR_48: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.SCIMITAR_48, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionScimitar48],
    AwardTypes.POTION_SUMMON_CHICKEN: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_SUMMON_CHICKEN, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionSummonChicken],
    AwardTypes.POTION_SUMMON_WASP: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_SUMMON_WASP, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionSummonWasp],
    AwardTypes.POTION_SUMMON_DOG: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeConsumable, ItemGlobals.POTION_SUMMON_DOG, 0, 0)),
        None,
        1,
        PLocalizer.CodeRedemptionSummonDog],
    AwardTypes.DUAL_CUTLASSES: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.DUAL_RUSTY_CUTLASS, 0, [])),
        None,
        1,
        PLocalizer.CodeRedemptionDualCutlasses],  
    AwardTypes.SANTA: [
        CLOTHING,
        InvItem((InventoryType.ItemTypeClothing, ItemGlobals.XMAS_CAP, 0, 0)),
        InvItem((InventoryType.ItemTypeClothing, ItemGlobals.XMAS_CAP, 0, 0)),
        1,
        PLocalizer.CodeRedemptionSanta],
    AwardTypes.WINTER: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeMoney, 0)),
        None,
        5000,
        PLocalizer.CodeRedemptionWinter],
    AwardTypes.WONDERLAND: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeMoney, 0)),
        None,
        10000,
        PLocalizer.CodeRedemptionWonderland],
    AwardTypes.SAVVY20K: [
        NORMAL_INVENTORY,
        InvItem((InventoryType.ItemTypeMoney, 0)),
        None,
        2000,
        PLocalizer.CodeRedemptionSavvy20k
    ] 
    #AwardTypes.BOARDING_AXE: [
    #    NORMAL_INVENTORY,
    #    InvItem((InventoryType.ItemTypeWeapon, ItemGlobals.CRUDE_BOARDING_AXE, 0, [])),
    #    None,
    #    1,
    #    PLocalizer.CodeRedemptionBoardingAxe],
    #AwardTypes.TREASURE: [
    #    NORMAL_INVENTORY,
    #    InvItem((InventoryType.ItemTypeMoney, 0)),
    #    None,
    #    10000,
    #    PLocalizer.CodeRedemptionTreasure],
}

HOLIDAY_AWARD_ID = {
    HolidayGlobals.THANKSGIVING: {
        AwardTypes.THANKSGIVING: [
            NORMAL_INVENTORY,
            InvItem((InventoryType.ItemTypeMoney, 0)),
            None,
            3000,
            PLocalizer.CodeRedemptionThanksgiving
        ]
    },
    HolidayGlobals.HALLOWEEN: {
        AwardTypes.HALLOWEEN: [
            NORMAL_INVENTORY,
            InvItem((InventoryType.ItemTypeMoney, 0)),
            None,
            5000,
            PLocalizer.CodeRedemptionHalloween
        ] 
    }
}

def getAwardFromCode(code, holidayList=None):
    for award in AWARD_ID:
        award = AWARD_ID.get(award)
        codeword = award[4].lower()
        if codeword == code.lower():
            return award
    if holidayList != None:
        for holiday in holidayList:
            if holiday in HOLIDAY_AWARD_ID:
                awards = HOLIDAY_AWARD_ID.get(holiday)
                for award in awards:
                    award = awards.get(award)
                    codeword = award[4].lower()
                    if codeword == code.lower():
                        return award                    
    return None

def getAwardIdFromCode(code, holidayList=None):
    for award in AWARD_ID:
        data = AWARD_ID.get(award)
        codeword = award[4].lower()
        if codeword == code.lower():   
            return award
    if holidayList != None:
        for holiday in holidayList:
            if holiday in HOLIDAY_AWARD_ID:
                awards = HOLIDAY_AWARD_ID.get(holiday)
                for award in awards:
                    award = awards.get(award)
                    codeword = award[4].lower()
                    if codeword == code.lower():
                        return award   
    return -1
