from pirates.world.LocationConstants import LocationIds
from pirates.uberdog import UberDogGlobals
import random


def loadSfx(audioName):
    return loader.loadSfx('audio/' + audioName)

def loadSfxString(audioName):
    return 'audio/' + audioName

AUDIO_EXTENSION = 'ogg'
MUSIC_MAIN = 0
MUSIC_ALT = 1
MUSIC_COMBAT = 2
MUSIC_NONE = 'Not Found'

AMBIENT_DAY = 0
AMBIENT_NIGHT = 1
AMBIENT_NONE = 'Not Found'

MUSIC_CANGREJOS = 'music_cangrejos.%s' % AUDIO_EXTENSION
MUSIC_CANGREJOS_ALT = 'music_cangrejos_alt.%s' % AUDIO_EXTENSION
MUSIC_CANGREJOS_COMBAT = 'music_cangrejos_combat.%s' % AUDIO_EXTENSION
MUSIC_CUBA = 'music_cuba.%s' % AUDIO_EXTENSION
MUSIC_CUBA_ALT = 'music_cuba_alt.%s' % AUDIO_EXTENSION
MUSIC_CUBA_COMBAT = 'music_cuba_combat.%s' % AUDIO_EXTENSION
MUSIC_CUTTHROAT = 'music_cutthroat.%s' % AUDIO_EXTENSION
MUSIC_CUTTHROAT_ALT = 'music_cutthroat_alt.%s' % AUDIO_EXTENSION
MUSIC_CUTTHROAT_COMBAT = 'music_cutthroat_combat.%s' % AUDIO_EXTENSION
MUSIC_DEVILS_ANVIL = 'music_devils_anvil.%s' % AUDIO_EXTENSION
MUSIC_DEVILS_ANVIL_ALT = 'music_devils_anvil_alt.%s' % AUDIO_EXTENSION
MUSIC_DEVILS_ANVIL_COMBAT = 'music_devils_anvil_combat.%s' % AUDIO_EXTENSION
MUSIC_DRIFTWOOD = 'music_driftwood.%s' % AUDIO_EXTENSION
MUSIC_DRIFTWOOD_ALT = 'music_driftwood_alt.%s' % AUDIO_EXTENSION
MUSIC_DRIFTWOOD_COMBAT = 'music_driftwood_combat.%s' % AUDIO_EXTENSION
MUSIC_ISLA_AVARICIA = 'music_isla_de_porc.%s' % AUDIO_EXTENSION
MUSIC_ISLA_DE_PORC = 'music_ile_detable.%s' % AUDIO_EXTENSION
MUSIC_KINGSHEAD = 'music_kingshead.%s' % AUDIO_EXTENSION
MUSIC_KINGSHEAD_ALT = 'music_kingshead_alt.%s' % AUDIO_EXTENSION
MUSIC_KINGSHEAD_COMBAT = 'music_kingshead_combat.%s' % AUDIO_EXTENSION
MUSIC_OUTCAST = 'music_outcast.%s' % AUDIO_EXTENSION
MUSIC_PADRES = 'music_madre_del_fuego.%s' % AUDIO_EXTENSION
MUSIC_PADRES_ALT = 'music_padres_alt.%s' % AUDIO_EXTENSION
MUSIC_PADRES_COMBAT = 'music_padres_combat.%s' % AUDIO_EXTENSION
MUSIC_PERDIDA = 'music_perdida.%s' % AUDIO_EXTENSION
MUSIC_PERDIDA_ALT = 'music_perdida_alt.%s' % AUDIO_EXTENSION
MUSIC_PERDIDA_COMBAT = 'music_perdida_combat.%s' % AUDIO_EXTENSION
MUSIC_PORT_ROYAL = 'music_port_royal.%s' % AUDIO_EXTENSION
MUSIC_PORT_ROYAL_ALT = 'music_port_royal_alt.%s' % AUDIO_EXTENSION
MUSIC_PORT_ROYAL_COMBAT = 'music_port_royal_combat.%s' % AUDIO_EXTENSION
MUSIC_RUMRUNNERS = 'music_rumrunner.%s' % AUDIO_EXTENSION
MUSIC_RUMRUNNERS_ALT = 'music_rumrunners_alt.%s' % AUDIO_EXTENSION
MUSIC_RUMRUNNERS_COMBAT = 'music_rumrunners_combat.%s' % AUDIO_EXTENSION
MUSIC_TORMENTA = 'music_tormenta.%s' % AUDIO_EXTENSION
MUSIC_TORMENTA_ALT = 'music_tormenta_alt.%s' % AUDIO_EXTENSION
MUSIC_TORMENTA_COMBAT = 'music_tormenta_combat.%s' % AUDIO_EXTENSION
MUSIC_TORTUGA = 'music_tortuga.%s' % AUDIO_EXTENSION
MUSIC_TORTUGA_ALT = 'music_tortuga_alt.%s' % AUDIO_EXTENSION
MUSIC_TORTUGA_COMBAT = 'music_tortuga_combat.%s' % AUDIO_EXTENSION
MUSIC_CAVE = 'music_creepy_a.%s' % AUDIO_EXTENSION
MUSIC_JUNGLE = 'music_creepy_b.%s' % AUDIO_EXTENSION
MUSIC_SWAMP = 'music_creepy_c.%s' % AUDIO_EXTENSION
MUSIC_SAILING_A = 'music_sailing_a.%s' % AUDIO_EXTENSION
MUSIC_SAILING_B = 'music_sailing_b.%s' % AUDIO_EXTENSION
MUSIC_SAILING_C = 'music_sailing_c.%s' % AUDIO_EXTENSION
MUSIC_SAILING_D = 'music_sailing_d.%s' % AUDIO_EXTENSION
MUSIC_SAILING_E = 'music_sailing_e.%s' % AUDIO_EXTENSION
MUSIC_SHIP_COMBAT_01 = 'music_highseas_combat.%s' % AUDIO_EXTENSION
MUSIC_SHIP_COMBAT_02 = 'he_is_a_pirate.%s' % AUDIO_EXTENSION
MUSIC_SHIP_ENSNARED = 'music_wheel_08.%s' % AUDIO_EXTENSION
MUSIC_KRAKEN_SINK = 'music_kraken_sink_ship.%s' % AUDIO_EXTENSION
MUSIC_COMBAT_A = 'music_combat_a.%s' % AUDIO_EXTENSION
MUSIC_COMBAT_B = 'music_combat_b.%s' % AUDIO_EXTENSION
MUSIC_COMBAT_C = 'music_combat_c.%s' % AUDIO_EXTENSION
MUSIC_SHIP_COMBAT_02 = 'he_is_a_pirate.%s' % AUDIO_EXTENSION
MUSIC_TAVERN_A = 'music_tavern_a.%s' % AUDIO_EXTENSION
MUSIC_TAVERN_B = 'music_tavern_b.%s' % AUDIO_EXTENSION
MUSIC_TAVERN_C = 'music_tavern_c.%s' % AUDIO_EXTENSION
MUSIC_PERFORMERS_02 = 'music_performers_02.%s' % AUDIO_EXTENSION
MUSIC_PERFORMERS_07 = 'music_performers_07.%s' % AUDIO_EXTENSION
MUSIC_PERFORMERS_09 = 'music_performers_09.%s' % AUDIO_EXTENSION
MUSIC_PERFORMERS_10 = 'music_performers_10.%s' % AUDIO_EXTENSION
MUSIC_HOLIDAY_01 = 'music_ballad_of_a_buccaneer.%s' % AUDIO_EXTENSION
MUSIC_HOLIDAY_02 = 'music_caribbean_holiday.%s' % AUDIO_EXTENSION
MUSIC_RAVENS_COVE_DAY = 'music_ravens_cove_day.%s' % AUDIO_EXTENSION
MUSIC_RAVENS_COVE_NIGHT = 'music_ravens_cove_night.%s' % AUDIO_EXTENSION
MUSIC_EL_PATRONS_MINE = 'music_el_patrons_mine.%s' % AUDIO_EXTENSION
MUSIC_RAVENS_COVE_TOWN_BATTLE = 'music_battle_town.%s' % AUDIO_EXTENSION
MUSIC_RAVENS_COVE_CAVE_BATTLE = 'music_battle_caves.%s' % AUDIO_EXTENSION
MUSIC_AVATAR_CHOOSER = 'will_and_elizabeth.%s' % AUDIO_EXTENSION
MUSIC_MAKE_A_PIRATE = 'music_jack_01.%s' % AUDIO_EXTENSION
MUSIC_JACK_02 = 'music_jack_02.%s' % AUDIO_EXTENSION
MUSIC_JACK_03 = 'music_jack_03.%s' % AUDIO_EXTENSION
MUSIC_JACK_04 = 'music_jack_04.%s' % AUDIO_EXTENSION
MUSIC_JACK_05 = 'music_jack_05.%s' % AUDIO_EXTENSION
MUSIC_JACK_06 = 'music_jack_06.%s' % AUDIO_EXTENSION
MUSIC_JACK_07 = 'music_jack_07.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_01 = 'music_wheel_01.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_04 = 'music_wheel_04.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_05 = 'music_wheel_05.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_06 = 'music_wheel_06.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_07 = 'music_wheel_07.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_09 = 'music_wheel_09.%s' % AUDIO_EXTENSION
MUSIC_VICTORY = 'music_wheel_02.%s' % AUDIO_EXTENSION
MUSIC_SEARCHING = 'music_wheel_03.%s' % AUDIO_EXTENSION
MUSIC_DEATH = 'music_wheel_08_short.%s' % AUDIO_EXTENSION
MUSIC_AMBUSH = 'music_wheel_10.%s' % AUDIO_EXTENSION
MUSIC_WHEEL_13 = 'music_wheel_13.%s' % AUDIO_EXTENSION
MUSIC_FINAL_BATTLE = 'music_final_battle.%s' % AUDIO_EXTENSION
MUSIC_FIREWORKS = 'music_fireworks.%s' % AUDIO_EXTENSION
MUSIC_REWARD_WEAPON = 'music_wheel_11.%s' % AUDIO_EXTENSION
MUSIC_INVASION_VICTORY = 'music_wheel_11.%s' % AUDIO_EXTENSION
MUSIC_INVASION_DEFEAT = 'music_wheel_12.%s' % AUDIO_EXTENSION
MUSIC_DEFAULT_MAIN = MUSIC_SWAMP
MUSIC_DEFAULT_ALT = MUSIC_SWAMP
MUSIC_DEFAULT_COMBAT = MUSIC_COMBAT_A
AMBIENT_JUNGLE = 'sfx_jungle_mix.ogg'
AMBIENT_VOLCANO = 'sfx_cave_drips.ogg'
AMBIENT_CAVE = 'sfx_cave_drips.ogg'
AMBIENT_SWAMP = 'sfx_swamp_mix.ogg'
AMBIENT_SPANISH = 'sfx_town_npchouse-spanish.ogg'
AMBIENT_SHANTY = 'sfx_town_npchouse-shanty.ogg'
AMBIENT_SHIP = 'sfx_ship_idle.ogg'
AMBIENT_JAIL = 'sfx_jail_interior_loop.ogg'
AMBIENT_WAVES = 'sfx_ocean_shore.%s' % AUDIO_EXTENSION
AMBIENT_CROW = 'sfx_crow_caw.%s' % AUDIO_EXTENSION
AMBIENT_BIRDS = 'sfx_bird_wings.%s' % AUDIO_EXTENSION
AMBIENT_WIND = 'sfx_ocean_wind.%s' % AUDIO_EXTENSION
AMBIENCE_PORT_ROYAL = 'sfx_town_ambience_port_royal.%s' % AUDIO_EXTENSION
AMBIENCE_PORT_ROYAL_NIGHT = 'sfx_town_ambience_port_royal_night.%s' % AUDIO_EXTENSION
AMBIENCE_FORT = 'sfx_fort_ambience.%s' % AUDIO_EXTENSION
AMBIENCE_TAVERN_INTERIOR = 'sfx_town_tavern_int.%s' % AUDIO_EXTENSION
AMBIENCE_TAVERN_EXTERIOR = 'sfx_town_tavern_ext.%s' % AUDIO_EXTENSION
AMBIENCE_SPANISH = 'sfx_town_ambience_spanish.%s' % AUDIO_EXTENSION
AMBIENCE_SPANISH_NIGHT = 'sfx_town_ambience_spanish_night.%s' % AUDIO_EXTENSION
CS_1_1_A_JS = 'cs_tut_1_1_a_js.%s' % AUDIO_EXTENSION
CS_1_1_B_JS = 'cs_tut_1_1_b_js.%s' % AUDIO_EXTENSION
CS_1_1_5_A_DAN = 'cs_tut_1_1_5_a_dan.%s' % AUDIO_EXTENSION
CS_1_1_5_B_DAN = 'cs_tut_1_1_5_b_dan.%s' % AUDIO_EXTENSION
CS_1_1_5_C_DAN = 'cs_tut_1_1_5_c_dan.%s' % AUDIO_EXTENSION
CS_1_2_B_DOCK = 'cs_tut_1_2_b_dock.%s' % AUDIO_EXTENSION
CS_1_2_DOCK = 'cs_tut_1_2_dock.%s' % AUDIO_EXTENSION
CS_1_3_JR = 'cs_tut_1_3_jr.%s' % AUDIO_EXTENSION
CS_2_1_A_WT = 'cs_tut_2_1_a_wt.%s' % AUDIO_EXTENSION
CS_2_1_B_WT = 'cs_tut_2_1_b_wt.%s' % AUDIO_EXTENSION
CS_2_2_TD = 'cs_tut_2_2_td.%s' % AUDIO_EXTENSION
CS_2_3_ES = 'cs_tut_2_3_es.%s' % AUDIO_EXTENSION
CS_2_4_A_CB = 'cs_tut_2_4_a_cb.%s' % AUDIO_EXTENSION
CS_2_4_B_CB = 'cs_tut_2_4_b_cb.%s' % AUDIO_EXTENSION
CS_2_5_JS = 'cs_tut_2_5_js.%s' % AUDIO_EXTENSION
CS_3_1_BP = 'cs_tut_3_1_bp.%s' % AUDIO_EXTENSION
CS_3_2_JS = 'cs_tut_3_2_js.%s' % AUDIO_EXTENSION
CS_6_1_TD = 'cs_tut_6_1_td.%s' % AUDIO_EXTENSION
JSD_ANYTIME_01 = 'jsd_anytime_1.%s' % AUDIO_EXTENSION
JSD_ANYTIME_02 = 'jsd_anytime_2.%s' % AUDIO_EXTENSION
JSD_ANYTIME_03 = 'jsd_anytime_3.%s' % AUDIO_EXTENSION
JSD_ANYTIME_04 = 'jsd_anytime_4.%s' % AUDIO_EXTENSION
JSD_BODY_MS_01 = 'jsd_body_ms_1.%s' % AUDIO_EXTENSION
JSD_BODY_MS_02 = 'jsd_body_ms_2.%s' % AUDIO_EXTENSION
JSD_BODY_SF_01 = 'jsd_body_sf_1.%s' % AUDIO_EXTENSION
JSD_BODY_SF_02 = 'jsd_body_sf_2.%s' % AUDIO_EXTENSION
JSD_BODY_TM_01 = 'jsd_body_tm_1.%s' % AUDIO_EXTENSION
JSD_BODY_TM_02 = 'jsd_body_tm_2.%s' % AUDIO_EXTENSION
JSD_CLOTHES_01 = 'jsd_clothes_1.%s' % AUDIO_EXTENSION
JSD_CLOTHES_02 = 'jsd_clothes_2.%s' % AUDIO_EXTENSION
JSD_CLOTHES_03 = 'jsd_clothes_3.%s' % AUDIO_EXTENSION
JSD_CLOTHES_04 = 'jsd_clothes_4.%s' % AUDIO_EXTENSION
JSD_CLOTHES_05 = 'jsd_clothes_5.%s' % AUDIO_EXTENSION
JSD_CLOTHES_END_01 = 'jsd_clothes_finish_1.%s' % AUDIO_EXTENSION
JSD_CLOTHES_END_02 = 'jsd_clothes_finish_2.%s' % AUDIO_EXTENSION
JSD_COAT_01 = 'jsd_coat_good.%s' % AUDIO_EXTENSION
JSD_FACE_01 = 'jsd_face_long.%s' % AUDIO_EXTENSION
JSD_FACE_02 = 'jsd_face_pretty.%s' % AUDIO_EXTENSION
JSD_FACE_03 = 'jsd_face_rogue.%s' % AUDIO_EXTENSION
JSD_FACE_04 = 'jsd_face_ugly.%s' % AUDIO_EXTENSION
JSD_HAIR_01 = 'jsd_hair_lot.%s' % AUDIO_EXTENSION
JSD_HAIR_02 = 'jsd_hair_mop.%s' % AUDIO_EXTENSION
JSD_HAT_01 = 'jsd_hat_good.%s' % AUDIO_EXTENSION
JSD_PANT_01 = 'jsd_pant_good.%s' % AUDIO_EXTENSION
JSD_NAME_ANYTIME_01 = 'jsd_name_anytime.%s' % AUDIO_EXTENSION
JSD_NAME_F_INTRO_01 = 'jsd_name_f_intro.%s' % AUDIO_EXTENSION
JSD_NAME_LONG_01 = 'jsd_name_long_1.%s' % AUDIO_EXTENSION
JSD_NAME_LONG_02 = 'jsd_name_long_2.%s' % AUDIO_EXTENSION
JSD_NAME_LONG_03 = 'jsd_name_long_3.%s' % AUDIO_EXTENSION
JSD_NAME_SHORT_01 = 'jsd_name_short_1.%s' % AUDIO_EXTENSION
JSD_NAME_SHORT_02 = 'jsd_name_short_2.%s' % AUDIO_EXTENSION
JSD_SHOE_BARB = 'jsd_shoe_barbossa.%s' % AUDIO_EXTENSION
JSD_SHOE_01 = 'jsd_shoe_good.%s' % AUDIO_EXTENSION
BBD_TELL_SHOOT = 'beck_cs12_4_4c_tell_to_shoot.%s' % AUDIO_EXTENSION
BBD_GIVE_PRAISE = 'beck_cs12_5_5a_tell_praise.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_DRAW = 'sfx_dagger_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_PUTAWAY = 'sfx_dagger_sheathe.%s' % AUDIO_EXTENSION
SFX_WEAPON_NONBLADE_DRAW = 'sfx_weapon_nonblade_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_NONBLADE_PUTAWAY = 'sfx_weapon_nonblade_put_away.%s' % AUDIO_EXTENSION
SFX_WEAPON_STAFF_CHARGE = 'sfx_wand_charge.%s' % AUDIO_EXTENSION
SFX_WEAPON_STAFF_CHARGE_LOOP = 'sfx_wand_charge_loop.ogg'
SFX_WEAPON_BAYONET_HIT = 'sfx_dagger_impact.%s' % AUDIO_EXTENSION
SFX_WEAPON_BAYONET_MISS = 'whoosh-10.%s' % AUDIO_EXTENSION
SFX_WEAPON_BAYONET_MISS_ALT = 'arm-Whoosh-05.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_FIRE_01 = 'cball_fire_1.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_FIRE_02 = 'cball_fire_2.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_FIRE_03 = 'cball_fire_3.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_FIRE_04 = 'cball_fire_4.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_FIRE_05 = 'cball_fire_5.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_HIT = 'in_cball_hit_1_f.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_01 = 'dist_cannon_01.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_02 = 'dist_cannon_02.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_03 = 'dist_cannon_03.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_04 = 'dist_cannon_04.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_05 = 'dist_cannon_05.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_06 = 'dist_cannon_06.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_07 = 'dist_cannon_07.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_08 = 'dist_cannon_08.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_09 = 'dist_cannon_09.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_DIST_FIRE_10 = 'dist_cannon_10.%s' % AUDIO_EXTENSION
SFX_WEAPON_CANNON_EMPTY = 'outofammo.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_CLASHCLANG = 'sword-clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SWIPECLANG_01 = 'sword-swipeNclang1.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SWIPECLANG_02 = 'sword-swipeNclang2.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SWIPECLANG_03 = 'sword-swipeNclang3.%s' % AUDIO_EXTENSION
SFX_WEAPON_SABRE_CLASHCLANG = 'pir_s_wpn_sabre_clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_SABRE_SWIPECLANG_01 = 'pir_s_wpn_sabre_clang1.%s' % AUDIO_EXTENSION
SFX_WEAPON_SABRE_SWIPECLANG_02 = 'pir_s_wpn_sabre_clang2.%s' % AUDIO_EXTENSION
SFX_WEAPON_SABRE_SWIPECLANG_03 = 'pir_s_wpn_sabre_clang3.%s' % AUDIO_EXTENSION
SFX_WEAPON_SCIMITAR_CLASHCLANG = 'pir_s_wpn_scimitar_clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_SCIMITAR_SWIPECLANG_01 = 'pir_s_wpn_scimitar_clang1.%s' % AUDIO_EXTENSION
SFX_WEAPON_SCIMITAR_SWIPECLANG_02 = 'pir_s_wpn_scimitar_clang2.%s' % AUDIO_EXTENSION
SFX_WEAPON_SCIMITAR_SWIPECLANG_03 = 'pir_s_wpn_scimitar_clang3.%s' % AUDIO_EXTENSION
SFX_WEAPON_BROADSWORD_CLASHCLANG = 'pir_s_wpn_broadsword_clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_BROADSWORD_SWIPECLANG_01 = 'pir_s_wpn_broadsword_clang1.%s' % AUDIO_EXTENSION
SFX_WEAPON_BROADSWORD_SWIPECLANG_02 = 'pir_s_wpn_broadsword_clang2.%s' % AUDIO_EXTENSION
SFX_WEAPON_BROADSWORD_SWIPECLANG_03 = 'pir_s_wpn_broadsword_clang3.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_MISTIMEDHIT = 'sword-unsheath.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SWOOSH_01 = 'sword-swoosh1.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SWOOSH_02 = 'sword-swoosh2.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_HACK = 'sfx_cutlass_hack.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SLASH = 'sfx_cutlass_slash.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_STAB = 'sfx_cutlass_stab.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_FLOURISH = 'sfx_cutlass_flourish.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_CLEAVE = 'sfx_cutlass_cleave.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_TAUNT = 'sfx_cutlass_taunt.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_BRAWL = 'sfx_cutlass_headbutt.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SWEEP = 'sfx_cutlass_sweep.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_BLADESTORM = 'sfx_cutlass_bladestorm.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_DRAW = 'sfx_cutlass_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_SHEATHE = 'sfx_cutlass_sheathe.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_BLOWBACK = 'pir_s_skl_blowback.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_CAPTAINS_FURY = 'pir_s_skl_captainsFury.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_CURSED_FIRE = 'pir_s_wpn_cursedFireHack.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_CURSED_THUNDER = 'pir_s_wpn_cursedThunderHack.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_CURSED_ICE = 'pir_s_wpn_cursedIceHack.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_FIRE_HIT = 'pir_s_wpn_cursedFireHit.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_THUNDER_HIT = 'pir_s_wpn_cursedThunderHit.%s' % AUDIO_EXTENSION
SFX_WEAPON_CUTLASS_ICE_HIT = 'pir_s_wpn_cursedIceHit.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_MISS_01 = 'swordSwipeSingle-01.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_MISS_02 = 'swordSwipeSingle-02.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_HIT = 'sfx_dagger_impact.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_MISTIMEDHIT = 'sword-unsheath.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_CUT = 'sfx_dagger_cut.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_SWIPE = 'sfx_dagger_swipe.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_GOUGE = 'sfx_dagger_gouge.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_EVISCERATE = 'sfx_dagger_eviscerate.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_ASP = 'sfx_dagger_thrown.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_ADDER = 'sfx_dagger_poison.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_THROW_DIRT = 'sfx_dagger_throw_dirt.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_SIDEWINDER = 'sfx_dagger_sidewinder.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_VIPER_NEST = 'sfx_dagger_vipersnest.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_DRAW = 'sfx_dagger_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_SHEATHE = 'sfx_dagger_sheathe.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_BARRAGE = 'sfx_dagger_vipersnest.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_RAIN = 'sfx_dagger_vipersnest.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_THROW_COMBO_1 = 'sfx_dagger_sidewinder.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_THROW_COMBO_2 = 'sfx_dagger_sidewinder.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_THROW_COMBO_3 = 'sfx_dagger_sidewinder.%s' % AUDIO_EXTENSION
SFX_WEAPON_DAGGER_THROW_COMBO_4 = 'sfx_dagger_thrown.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_HIT = 'sword-clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_MISS_01 = 'sword-swoosh1.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_MISS_02 = 'sword-swoosh2.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_ATTUNE = 'sfx_doll_attune.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_UNATTUNE = 'sfx_doll_unattune.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_ATTUNE_LOOP = 'sfx_doll_attune_loop.ogg'
SFX_WEAPON_DOLL_POKE = 'sfx_doll_poke.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_SWARM = 'sfx_doll_swarm.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_HEAL = 'sfx_doll_heal.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_CURSE = 'sfx_doll_curse.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_SCORCH = 'sfx_doll_burn.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_CURE = 'sfx_doll_cure.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_SHACKLES = 'sfx_doll_poke.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_LIFE_DRAIN = 'sfx_doll_poke.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_DRAW = 'sfx_grenade_bigbomb_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_SHEATHE = 'sfx_grenade_bigbomb_put_away.%s' % AUDIO_EXTENSION
SFX_WEAPON_DOLL_EVIL_EYE = 'pir_s_skl_evilEye.%s' % AUDIO_EXTENSION
SFX_WEAPON_SKILL_MONKEY_RAGE = 'pir_s_skl_gorillaRage.%s' % AUDIO_EXTENSION
SFX_WEAPON_SKILL_CAPTAINS_RESOLVE = 'pir_s_skl_captainsResolve.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_HIT_01 = 'sword-clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_HIT_02 = 'sword-swipeNclang1.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_HIT_03 = 'sword-swipeNclang2.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_HIT_04 = 'sword-swipeNclang3.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_MISS_01 = 'sword-swoosh1.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_MISS_02 = 'sword-swoosh2.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_DRAW = 'sfx_cutlass_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_DUALCUTLASS_SHEATHE = 'sfx_cutlass_sheathe.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_HIT_01 = 'sword-clashNclang.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_HIT_02 = 'sword-swipeNclang1.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_HIT_03 = 'sword-swipeNclang2.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_HIT_04 = 'sword-swipeNclang3.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_MISS_01 = 'sword-swoosh1.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_MISS_02 = 'sword-swoosh2.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_DRAW = 'sfx_cutlass_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_FOIL_SHEATHE = 'sfx_cutlass_sheathe.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_AIM = 'sfx_pistol_cock.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_RELOAD = 'sfx_grenade_bigbomb_put_away.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_THROW = 'sfx_grenade_throw.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_SEIGE = 'sfx_grenade_bigbomb_throw.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_LONG_VOLLEY = 'sfx_grenade_long_volley_throw.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_CHARGING = 'sfx_grenade_long_volley_charging.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_DRAW = 'sfx_grenade_bigbomb_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_SHEATHE = 'sfx_grenade_bigbomb_put_away.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_FIREBOMB = 'sfx_grenade_impact_firebomb_loop.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_IMPACT = 'sfx_grenade_impact.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_FIREBOMB_EXPLODE = 'sfx_grenade_impact_firebomb_explo.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_STINK = 'sfx_grenade_impact_stink_pot.%s' % AUDIO_EXTENSION
SFX_WEAPON_GRENADE_SMOKE = 'sfx_grenade_impact_smoke.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_HP_HIT = 'sfx_pistol_effective.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_MANA_HIT = 'sfx_pistol_mana_drain.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_MISS = 'sfx_pistol_shoot.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_AIM = 'musketCock.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_SHOOT = 'sfx_pistol_shoot.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_WELL_AIMED = 'sfx_pistol_shoot.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_DRAW = 'sfx_pistol_draw.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_COCK = 'sfx_pistol_cock.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_RELOAD = 'sfx_pistol_reload.%s' % AUDIO_EXTENSION
SFX_WEAPON_PISTOL_SHEATHE = 'sfx_pistol_put_away.%s' % AUDIO_EXTENSION
SFX_WEAPON_BLUNDERBUSS_SHOOT = 'pir_s_wpn_blunderbussShot.%s' % AUDIO_EXTENSION
SFX_WEAPON_MUSKET_SHOOT = 'pir_s_wpn_musketShot.%s' % AUDIO_EXTENSION
SFX_MISC_HEART_BEAT_LOOP = 'pir_s_msc_heartBeat_loop.ogg'
SFX_SEAGULL_01 = 'seagull_1_fix.%s' % AUDIO_EXTENSION
SFX_SEAGULL_02 = 'seagull_2_fix.%s' % AUDIO_EXTENSION
SFX_SEAGULL_03 = 'seagull_3_fix.%s' % AUDIO_EXTENSION
SFX_SEAGULL_WAVES = 'seagullsNwaves.%s' % AUDIO_EXTENSION
SFX_MELEE_HIT_01 = 'swipeImpact-03.%s' % AUDIO_EXTENSION
SFX_MELEE_HIT_02 = 'swipeImpact-09.%s' % AUDIO_EXTENSION
SFX_MELEE_MISS_01 = 'whoosh-10.%s' % AUDIO_EXTENSION
SFX_MELEE_MISS_02 = 'arm_Whoosh-05.%s' % AUDIO_EXTENSION
SFX_MELEE_DRAW = 'sword-unsheath.%s' % AUDIO_EXTENSION
SFX_MONSTER_HIT = 'body_blow.%s' % AUDIO_EXTENSION
SFX_MONSTER_MISS = 'whoosh-10.%s' % AUDIO_EXTENSION
SFX_MONSTER_ENSNARE = 'kraken2.%s' % AUDIO_EXTENSION
SFX_MONSTER_SMASH_01 = 'wood_impact_1.%s' % AUDIO_EXTENSION
SFX_MONSTER_SMASH_02 = 'wood_impact_3.%s' % AUDIO_EXTENSION
SFX_MONSTER_SMASH_03 = 'wood_impact_4.%s' % AUDIO_EXTENSION
SFX_MONSTER_DEATH = 'bodyFall-08.%s' % AUDIO_EXTENSION
SFX_MONSTER_BAT_ATTACK = 'sfx_bat_attack_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_BAT_DEATH = 'sfx_bat_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_BAT_PAIN = 'sfx_bat_pain_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_ALLIGATOR_ATTACK_LEFT = 'sfx_alligator_attack_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_ALLIGATOR_ATTACK_STRAIGHT = 'sfx_alligator_attack_straight.%s' % AUDIO_EXTENSION
SFX_MONSTER_ALLIGATOR_DEATH = 'sfx_alligator_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_ALLIGATOR_PAIN = 'sfx_alligator_flinch_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_ATTACK_LEFT = 'sfx_scorp_attack_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_ATTACK_BOTH = 'sfx_scorp_attack_both.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_ATTACK_TAIL = 'sfx_scorp_attack_tail.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_PICKUP = 'sfx_scorp_pickup_human.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_REARUP = 'sfx_scorpion_rearup.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_DEATH = 'sfx_scorpion_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_SCORPION_PAIN = 'sfx_scorpion_knockback.%s' % AUDIO_EXTENSION
SFX_MONSTER_CRAB_ATTACK_LEFT = 'sfx_crab_attack_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_CRAB_ATTACK_BOTH = 'sfx_crab_attack_both.%s' % AUDIO_EXTENSION
SFX_MONSTER_CRAB_DEATH = 'sfx_crab_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_CRAB_PAIN = 'sfx_crab_pain.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_ATTACK = 'sfx_flytrap_attack_a.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_JAB = 'sfx_flytrap_attaack_jab.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_FAKE = 'sfx_flytrap_attack_take.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_SPIT = 'sfx_flytrap_spit.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_DEATH = 'sfx_flytrap_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_PAIN = 'sfx_flytrap_hit.%s' % AUDIO_EXTENSION
SFX_MONSTER_FLYTRAP_SPAWN = 'sfx_flytrap_rise_ground.%s' % AUDIO_EXTENSION
SFX_MONSTER_KRAKEN_DEATH = 'sfx_crab_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_KRAKEN_PAIN = 'sfx_crab_pain.%s' % AUDIO_EXTENSION
SFX_MONSTER_KRAKEN_ROAR_01 = 'kraken1.%s' % AUDIO_EXTENSION
SFX_MONSTER_KRAKEN_ROAR_02 = 'kraken2.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_ATTACK_KICK = 'sfx_mossman_kick.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_ATTACK_SLAP = 'sfx_mossman_slap_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_ATTACK_SWAT = 'sfx_mossman_swat_left.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_JUMP = 'sfx_mossman_jump.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_DEATH = 'sfx_mossman_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_PAIN = 'sfx_mossman_agitated.%s' % AUDIO_EXTENSION
SFX_MONSTER_MOSSMAN_SPAWN = 'sfx_mossman_intro.%s' % AUDIO_EXTENSION
SFX_MONSTER_WASP_STING = 'sfx_wasp_sting.%s' % AUDIO_EXTENSION
SFX_MONSTER_WASP_LEAP_STING = 'sfx_wasp_leap_sting.%s' % AUDIO_EXTENSION
SFX_MONSTER_WASP_DEATH = 'sfx_wasp_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_WASP_PAIN = 'sfx_wasp_ouch.%s' % AUDIO_EXTENSION
SFX_MONSTER_SERPENT_DEATH = 'sfx_wasp_death.%s' % AUDIO_EXTENSION
SFX_MONSTER_SERPENT_PAIN = 'sfx_wasp_ouch.%s' % AUDIO_EXTENSION
SFX_RAGE_KILL = 'sfx_wand_pestilence_impact.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ACCEPT = 'jollyroger_accept.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ALL_YOU_GOT = 'jollyroger_all_you_got.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ATTACK = 'jollyroger_attack.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ATTACK_01 = 'jollyroger_attack1.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ATTACK_03 = 'jollyroger_attack3.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ATTACK_06 = 'jollyroger_attack6.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ATTACK_07 = 'jollyroger_attack7.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ATTACK_THE_TOWN = 'jollyroger_attack_the_town.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_BARRICADES_A = 'jollyroger_barricades_a.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_BARRICADES_B = 'jollyroger_barricades_b.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_BEG_MERCY = 'jollyroger_bef_mercy.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_BREAK = 'jollyroger_break.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_BRING = 'jollyroger_bring.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_BRING_OPPONENT = 'jollyroger_bring_opponent.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_CANT = 'jollyroger_cant.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_CHILDS_PLAY = 'jollyroger_childs_play.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_CRABS = 'jollyroger_crabs.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_01 = 'jollyroger_damage1.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_03 = 'jollyroger_damage3.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_04 = 'jollyroger_damage4.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_06 = 'jollyroger_damage6.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_07 = 'jollyroger_damage7.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_10 = 'jollyroger_damage10.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_13 = 'jollyroger_damage13.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DAMAGE_14 = 'jollyroger_damage14.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DEAD = 'jollyroger_dead.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DESTROY_EVERYTHING = 'jollyroger_destroy_everything.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_DISPATCH = 'jollyroger_dispatch.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ENJOY = 'jollyroger_enjoy.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ENJOYING = 'jollyroger_enjoying.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_EVERYONE_WILL_PAY = 'jollyroger_everyone_will_pay.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FAITHFUL_BRIDE = 'jollyroger_faithful_bride.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FASTER_YOU_SCABS = 'jollyroger_faster_you_scabs.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FEAR_ME = 'jollyroger_fear_me.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FEAST_SOULS = 'jollyroger_feast_souls.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FIGHT = 'jollyroger_fight.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FIGHT_BEFORE_MEAL = 'jollyroger_fight_before_meal.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FIGHT_ON = 'jollyroger_fight_on.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FOLLOW_ME_NOW = 'jollyroger_follw_me_now.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FOOLS = 'jollyroger_fools.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FORWARD = 'jollyroger_forward.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FORWARD_ATTACK = 'jollyroger_forward_attack.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_FUNERAL_FIRE = 'jollyroger_funeral_fire.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_GET_YE = 'jollyroger_get_ye.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_GOGOGO = 'jollyroger_gogogo.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_HOW_ITS_DONE = 'jollyroger_how_its_done.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_HOWS_THIS = 'jollyroger_howsthis.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_IF_ONLY = 'jollyroger_ifonly.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_IS_THAT_THE_BEST = 'jollyroger_isthatthebest.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_ITCHING_TO_FIGHT = 'jollyroger_itching_to_fight.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_JOIN = 'jollyroger_joinme.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_LAUGH_01 = 'jollyroger_laugh_01.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_LAUGH_02 = 'jollyroger_laugh_02.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_MANSION_DESTROYED = 'jollyroger_mansion_destroyed.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_MEET_YOUR_MAKER = 'jollyroger_meet_your_maker.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NEED_TO_FIND_SOMEONE_ELSE = 'jollyroger_need_to_find_someone_else.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NEXT_BRIGADE = 'jollyroger_next_brigade.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NEXT_CONQUEST = 'jollyroger_next_conquest.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NEXT_TARGET = 'jollyroger_next_target.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NO_MERCY = 'jollyroger_no_mery.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NO_TIME = 'jollyroger_no_time.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NOT_BAD = 'jollyroger_notbad.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_NOT_SEEN = 'jollyroger_notseen.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_PORT_ROYAL_MINE = 'jollyroger_port_royal_mine.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_QUIP_03 = 'jollyroger_quip3.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_QUIP_04 = 'jollyroger_quip4.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_RANSACK_TOWN = 'jollyroger_ransack_town.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_REALLY_IS_A_LAUGH = 'jollyroger_really_is_a_laugh.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_RETREAT = 'jollyroger_retreat.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_RIP = 'jollyroger_rip.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_RUBBLE = 'jollyroger_rubble.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SMELL = 'jollyroger_smell.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SO_MUCH_FUN = 'jollyroger_so_much_fun.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SOULS_TO_DEVOUR = 'jollyroger_souls_to_devour.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SPARROW_ALIVE = 'jollyroger_sparrow_alive.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SPARROW_ESCAPED = 'jollyroger_sparrow_escaped.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SPINELESS_FOOLS = 'jollyroger_spineless_fools.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_STAND = 'jollyroger_stand.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_STORM_THE_BEACHES = 'jollyroger_storm_the_beaches.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SUBMIT = 'jollyroger_submit.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_SUBMIT_TO_ME = 'jollyroger_submittome.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_TONIGHT = 'jollyroger_tonight.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_USELESS_SCABS = 'jollyroger_useless_scabs.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_VICTORY_MINE = 'jollyroger_victory_mine.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_WEAPON_NUISANCE = 'jollyroger_weapon_nuisance.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_YOU_CALL = 'jollyroger_youcall.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_YOULL_PAY = 'jollyroger_youllpay.%s' % AUDIO_EXTENSION
SFX_MONSTER_JR_YOUR_DESTINY = 'jollyroger_your_destiny.%s' % AUDIO_EXTENSION
SFX_MONSTER_EP_BEWARE = 'el_patron_beware.%s' % AUDIO_EXTENSION
SFX_MONSTER_EP_LAUGHTER = 'el_patron_laughter.%s' % AUDIO_EXTENSION
SFX_MONSTER_EP_RUNAWAY = 'el_patron_runaway.%s' % AUDIO_EXTENSION
SFX_MONSTER_EP_SHORT_LAUGH = 'el_patron_short_laugh.%s' % AUDIO_EXTENSION
SFX_CONSUMABLE_DRINK = 'sfx_tonic_drink.%s' % AUDIO_EXTENSION
SFX_CONSUMABLE_SHIP_REPAIR = 'sfx_ship_teleport_in.%s' % AUDIO_EXTENSION
SFX_CONSUMABLE_MISS = 'whoosh-10.%s' % AUDIO_EXTENSION
SFX_CONSUMABLE_MISS_ALT = 'arm-Whoosh-05.%s' % AUDIO_EXTENSION
SFX_CONSUMABLE_EAT_MEAT = 'sfx_eat_meat.%s' % AUDIO_EXTENSION
SFX_SKILL_RECHARGED = 'sfx_skill_recharged.%s' % AUDIO_EXTENSION
SFX_SKILL_BLAST_FIRE = 'sfx_wand_blast_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_BLAST_HIT = 'sfx_wand_blast_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_SOULFLAY_CHARGE = 'sfx_wand_soul_flay_charge.%s' % AUDIO_EXTENSION
SFX_SKILL_SOULFLAY_HOLD = 'sfx_wand_soul_flay_hold.ogg'
SFX_SKILL_SOULFLAY_FIRE = 'sfx_wand_soul_flay_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_SOULFLAY_HIT = 'sfx_wand_soul_flay_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_PESTILENCE_CHARGE = 'sfx_wand_pestilence_charge.%s' % AUDIO_EXTENSION
SFX_SKILL_PESTILENCE_HOLD = 'sfx_wand_pestilence_hold.ogg'
SFX_SKILL_PESTILENCE_FIRE = 'sfx_wand_pestilence_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_PESTILENCE_HIT = 'sfx_wand_pestilence_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_WITHER_CHARGE = 'sfx_wand_wither_charge.%s' % AUDIO_EXTENSION
SFX_SKILL_WITHER_HOLD = 'sfx_wand_wither_hold.ogg'
SFX_SKILL_WITHER_FIRE = 'sfx_wand_wither_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_WITHER_HIT = 'sfx_wand_wither_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_HELLFIRE_CHARGE = 'sfx_wand_hellfire_charge.%s' % AUDIO_EXTENSION
SFX_SKILL_HELLFIRE_HOLD = 'sfx_wand_hellfire_hold.ogg'
SFX_SKILL_HELLFIRE_FIRE = 'sfx_wand_hellfire_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_HELLFIRE_HIT = 'sfx_wand_hellfire_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_BANISH_CHARGE = 'sfx_wand_banish_charge.%s' % AUDIO_EXTENSION
SFX_SKILL_BANISH_HOLD = 'sfx_wand_banish_hold.ogg'
SFX_SKILL_BANISH_FIRE = 'sfx_wand_banish_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_BANISH_HIT = 'sfx_wand_banish_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_DESOLATION_CHARGE = 'sfx_wand_desolation_charge.%s' % AUDIO_EXTENSION
SFX_SKILL_DESOLATION_HOLD = 'sfx_wand_desolation_hold.ogg'
SFX_SKILL_DESOLATION_FIRE = 'sfx_wand_desolation_fire.%s' % AUDIO_EXTENSION
SFX_SKILL_DESOLATION_HIT = 'sfx_wand_desolation_impact.%s' % AUDIO_EXTENSION
SFX_SKILL_AURA_CAST = 'pir_s_skl_auraCast.%s' % AUDIO_EXTENSION
SFX_SKILL_AURA_LOOP = 'pir_s_skl_aura_loop.ogg'
SFX_SKILL_AURA_OFF = 'pir_s_skl_auraOff.%s' % AUDIO_EXTENSION
SFX_SKILL_CLEANSE = 'pir_s_skl_cleanse.%s' % AUDIO_EXTENSION
SFX_SKILL_HEX_WARD = 'pir_s_skl_hexWard.%s' % AUDIO_EXTENSION
SFX_SKILL_REFLECT_WARD = 'pir_s_skl_reflectWard.%s' % AUDIO_EXTENSION
SFX_SKILL_WARD_LOOP = 'pir_s_skl_ward_loop.ogg'
SFX_STOWAWAY_CRATE_SHUT = 'crate_shut.%s' % AUDIO_EXTENSION
SFX_GUI_WHISPER = 'sfx_gui_whisper.%s' % AUDIO_EXTENSION
SFX_GUI_ROLLOVER_01 = 'sfx_gui_click_08.%s' % AUDIO_EXTENSION
SFX_GUI_CLICK_01 = 'sfx_gui_click_22.%s' % AUDIO_EXTENSION
SFX_GUI_SKILL_RECHARGED = 'sword-swoosh2.%s' % AUDIO_EXTENSION
SFX_GUI_ZOOM_OUT = 'sfx_gui_zoom-io.%s' % AUDIO_EXTENSION
SFX_GUI_ZOOM_IN = 'sfx_gui_zoom-oi.%s' % AUDIO_EXTENSION
SFX_GUI_ALARM = 'sfx_gui_click_20.ogg'
SFX_GUI_OUT_OF_TIME = 'sfx_gui_negative.%s' % AUDIO_EXTENSION
SFX_GUI_SHOW_PANEL = 'sfx_gui_reminder.%s' % AUDIO_EXTENSION
SFX_GUI_STACK_POPUP = 'sfx_gui_zoom-io.%s' % AUDIO_EXTENSION
SFX_GUI_LOOT = 'treasure_hit_1.%s' % AUDIO_EXTENSION
SFX_GUI_LEVELUP = 'treasure_whoosh.%s' % AUDIO_EXTENSION
SFX_GUI_OPEN_SEACHEST = 'sfx_gui_seachest-open.%s' % AUDIO_EXTENSION
SFX_GUI_CLOSE_SEACHEST = 'sfx_gui_seachest-close.%s' % AUDIO_EXTENSION
SFX_GUI_REWARD_POPUP = 'sfx_combat_level_up.%s' % AUDIO_EXTENSION
SFX_GUI_TAKE_ALL = 'sfx_cards_chips-collect.%s' % AUDIO_EXTENSION
SFX_GUI_TAKE_GOLD = 'sfx_cards_chips-all.%s' % AUDIO_EXTENSION
SFX_GUI_TAKE_NONGOLD = 'sfx_combat_resist.%s' % AUDIO_EXTENSION
SFX_PVP_TREASURE_DEPOSIT = 'treasure_hit_1.%s' % AUDIO_EXTENSION
SFX_FX_EXPLODE_WOOD_01 = 'explo_wood_1.%s' % AUDIO_EXTENSION
SFX_FX_EXPLODE_WOOD_02 = 'explo_wood_2.%s' % AUDIO_EXTENSION
SFX_FX_EXPLODE_WOOD_GLASS = 'explode-w-glass.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_DISTANT_01 = 'firework_distance_01.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_DISTANT_02 = 'firework_distance_02.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_DISTANT_03 = 'firework_distance_03.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_EXPLODE_01 = 'firework_explosion_01.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_EXPLODE_02 = 'firework_explosion_02.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_EXPLODE_03 = 'firework_explosion_03.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_WHISTLE_01 = 'firework_whistle_01.%s' % AUDIO_EXTENSION
SFX_FX_FIREWORK_WHISTLE_02 = 'firework_whistle_02.%s' % AUDIO_EXTENSION
SFX_FX_FIRE_LOOP = 'sfx_fire_loop.ogg'
SFX_FX_WATER_SPLASH_01 = 'wtrsplash_1.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_02 = 'wtrsplash_2.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_03 = 'wtrsplash_3.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_04 = 'wtrsplash_4.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_05 = 'wtrsplash_5.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_06 = 'wtrsplash_6.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_07 = 'wtrsplash_7.%s' % AUDIO_EXTENSION
SFX_FX_WATER_SPLASH_08 = 'wtrsplash_8.%s' % AUDIO_EXTENSION
SFX_FX_WATERFALL_SMALL = 'sfx_waterfall_small.ogg'
SFX_FX_WATERFALL_CAVE = 'sfx_cave_waterfall.ogg'
SFX_FX_WOOD_IMPACT_01 = 'wood_impact_1.%s' % AUDIO_EXTENSION
SFX_FX_WOOD_IMPACT_02 = 'wood_impact_2.%s' % AUDIO_EXTENSION
SFX_FX_WOOD_IMPACT_03 = 'wood_impact_3.%s' % AUDIO_EXTENSION
SFX_FX_WOOD_IMPACT_04 = 'wood_impact_4.%s' % AUDIO_EXTENSION
SFX_FX_WOOD_SHATTER_02 = 'sfx_wood_shatter2.%s' % AUDIO_EXTENSION
SFX_FX_WOOD_SHATTER_03 = 'sfx_wood_shatter3.%s' % AUDIO_EXTENSION
SFX_FX_THUNDERCLAP = 'thunderclap.%s' % AUDIO_EXTENSION
SFX_FX_THUNDER_START = 'thunder-start.%s' % AUDIO_EXTENSION
SFX_FX_JUNGLE_BIRDS_01 = 'sfx_jungle_birds_v1.%s' % AUDIO_EXTENSION
SFX_FX_JUNGLE_BIRDS_02 = 'sfx_jungle_birds_v2.%s' % AUDIO_EXTENSION
SFX_FX_SWAMP_FROG_01 = 'sfx_swamp_frog_crowd.%s' % AUDIO_EXTENSION
SFX_FX_SWAMP_OWL_01 = 'sfx_swamp_owl_call01.%s' % AUDIO_EXTENSION
SFX_FX_SWAMP_OWL_02 = 'sfx_swamp_owl_call02.%s' % AUDIO_EXTENSION
SFX_FX_VOLCANO_ERUPT = 'eruption.%s' % AUDIO_EXTENSION
SFX_FX_VOLCANO_ERUPT_LOOP = 'eruption_loop.ogg'
SFX_FX_OCEAN_LOOP = 'oceanloop.%s' % AUDIO_EXTENSION
SFX_FX_SACK_APPEAR_01 = 'sfx_cards_chips-bet.%s' % AUDIO_EXTENSION
SFX_FX_CHEST_APPEAR_01 = 'sfx_gui_positive_alt.%s' % AUDIO_EXTENSION
SFX_FX_CHEST_APPEAR_02 = 'sfx_gui_rejected.%s' % AUDIO_EXTENSION
SFX_FX_OPEN_SACK_01 = 'sfx_combat_resist.%s' % AUDIO_EXTENSION
SFX_FX_OPEN_CHEST_01 = 'sfx_door_shanty_open.%s' % AUDIO_EXTENSION
SFX_FX_OPEN_CHEST_02 = 'unlock_try.%s' % AUDIO_EXTENSION
SFX_FX_BOOM = 'Boom2.%s' % AUDIO_EXTENSION
SFX_FX_ELEVATOR = 'sfx_elevator_gears.%s' % AUDIO_EXTENSION
SFX_MINIGAME_BH_MISS = 'sfx_cards_deal_01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_BH_HIT = 'ship_deck_hammer.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_HIT = 'sfx_cards_hit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_SHUFFLE = 'sfx_cards_shuffle.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_01 = 'sfx_cards_deal_01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_02 = 'sfx_cards_deal_02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_03 = 'sfx_cards_deal_03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_04 = 'sfx_cards_deal_04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_05 = 'sfx_cards_deal_05.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_06 = 'sfx_cards_deal_06.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_07 = 'sfx_cards_deal_07.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_DEAL_08 = 'sfx_cards_deal_08.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_FOLD = 'sfx_cards_fold.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_FLIP = 'sfx_cards_flip.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_PICKUP = 'sfx_cards_pickup.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_CHECK = 'sfx_cards_check.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_CHIPS_BET = 'sfx_cards_chips-bet.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_CHIPS_COLLECT = 'sfx_cards_chips-collect.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CARDS_CHIPS_ALL = 'sfx_cards_chips-all.%s' % AUDIO_EXTENSION
SFX_MINIGAME_LEVELUP = 'treasure_whoosh.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_FAIL = 'pir_s_gam_srp_bad_bilge.ogg'
SFX_MINIGAME_REPAIR_GENERAL_GUIUP = 'sfx_srp_guiup.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_GENERAL_GUIDOWN = 'sfx_srp_guidown.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_BRACE_PIECEMOVE = 'sfx_srp_brac_piecemove.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_BRACE_LINECOMPLETE = 'sfx_srp_brace_complete.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_CHRGCOMP = 'sfx_srp_careen_chrgcomp.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_CHRGEMPTY = 'sfx_srp_careen_chrgempty.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_COMPLETE1 = 'sfx_srp_careen_complete01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_COMPLETE2 = 'sfx_srp_careen_complete02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_COMPLETE3 = 'sfx_srp_careen_complete03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_COMPLETE4 = 'sfx_srp_careen_complete04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_COMPLETE5 = 'sfx_srp_careen_complete05.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB01 = 'sfx_srp_careen_scrub01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB02 = 'sfx_srp_careen_scrub02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB03 = 'sfx_srp_careen_scrub03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB04 = 'sfx_srp_careen_scrub04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB05 = 'sfx_srp_careen_scrub05.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB06 = 'sfx_srp_careen_scrub06.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB07 = 'sfx_srp_careen_scrub07.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_CAREEN_SCRUB08 = 'sfx_srp_careen_scrub08.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_GENERAL_GAMECOMPLETE = 'sfx_srp_gamecomplete.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_GENERAL_CYCLECOMPLETE = 'sfx_srp_cyclecomplete.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_GENERAL_READY = 'sfx_srp_ready.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_GENERAL_GO = 'sfx_srp_go.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_COMPLETE = 'sfx_srp_hammer_complete.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_HIT01 = 'sfx_srp_hammer_hit01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_HIT02 = 'sfx_srp_hammer_hit02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_HIT03 = 'sfx_srp_hammer_hit03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_PERFECT = 'sfx_srp_hammer_perfect.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_WEAKHIT01 = 'sfx_srp_hammer_weakhit01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_HAMMER_WEAKHIT02 = 'sfx_srp_hammer_weakhit02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_LEAK01 = 'sfx_srp_pitch_leak01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_LEAK02 = 'sfx_srp_pitch_leak02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_LEAK03 = 'sfx_srp_pitch_leak03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_LEAK04 = 'sfx_srp_pitch_leak04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_PLUG01 = 'sfx_srp_pitch_plug01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_PLUG02 = 'sfx_srp_pitch_plug02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PITCH_PLUG03 = 'sfx_srp_pitch_plug03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_BAD = 'sfx_srp_pump_bad.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_DOWN01 = 'sfx_srp_pump_down01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_DOWN02 = 'sfx_srp_pump_down02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_DOWN03 = 'sfx_srp_pump_down03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_GOOD01 = 'sfx_srp_pump_good01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_GOOD02 = 'sfx_srp_pump_good02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_GOOD03 = 'sfx_srp_pump_good03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_GOOD04 = 'sfx_srp_pump_good04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_GOOD05 = 'sfx_srp_pump_good05.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_GOOD06 = 'sfx_srp_pump_good06.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_UP01 = 'sfx_srp_pump_up01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_UP02 = 'sfx_srp_pump_up02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_PUMP_UP03 = 'sfx_srp_pump_up03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_SAW_COMPLETE = 'sfx_srp_saw_complete.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_SAW_FAIL = 'sfx_srp_saw_fail.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_SAW_INOUT01 = 'sfx_srp_saw_inout01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_SAW_INOUT02 = 'sfx_srp_saw_inout02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_SAW_INOUT03 = 'sfx_srp_saw_inout03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_REPAIR_SAW_INOUT04 = 'sfx_srp_saw_inout04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_ALLIGATOR = 'sfx_pot_fx_alligator.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_SCORPION = 'sfx_pot_fx_scorpion.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_CRAB = 'sfx_pot_fx_crab.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BARF_1 = 'sfx_pot_fx_barf.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BARF_2 = 'sfx_pot_fx_barf02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BARF_3 = 'sfx_pot_fx_barf03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BARF_4 = 'sfx_pot_fx_barf04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BURP_1 = 'sfx_pot_fx_burp.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BURP_2 = 'sfx_pot_fx_burp02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_BURP_3 = 'sfx_pot_fx_burp03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_FART_1 = 'sfx_pot_fx_fart.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_FART_2 = 'sfx_pot_fx_fart02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_FART_3 = 'sfx_pot_fx_fart03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_FART_4 = 'sfx_pot_fx_fart04.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_FART_5 = 'sfx_pot_fx_fart05.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_GROW = 'sfx_pot_fx_grow.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_SHRINK = 'sfx_pot_fx_shrink.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_SPARKLE = 'sfx_pot_fx_sparkle.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_TRANFORMATION = 'sfx_pot_fx_transformation.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FX_DEBUFF = 'sfx_pot_fx_debuff.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_CANTPLACE = 'pir_s_gam_pot_cantplace.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FLIP = 'pir_s_gam_pot_ingredflip.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_LOSE = 'pir_s_gam_pot_boardfail.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_WIN = 'pir_s_gam_pot_recipecomp.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_FILL = 'pir_s_gam_pot_ingredsucc.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_WRONG = 'pir_s_gam_pot_ingredwrong.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_DROP = 'pir_s_gam_pot_ingreddrop.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_DROP_2 = 'pir_s_gam_pot_ingreddrop02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_DROP_SOFT = 'pir_s_gam_pot_ingreddropsoft01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_DROP_SOFT_2 = 'pir_s_gam_pot_ingreddropsoft02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_MATCH = 'pir_s_gam_pot_ingredcomb.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_SOULMATCH = 'pir_s_gam_pot_matchsouls.%s' % AUDIO_EXTENSION
SFX_MINIGAME_POTION_SOULMADE = 'pir_s_gam_pot_soulcomb.%s' % AUDIO_EXTENSION
MUSIC_MINIGAME_POTION = 'music_potions.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_BITE_LARGE = 'sfx_fsh_bitelarge.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_BITE_MEDIUM = 'sfx_fsh_bitemed.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_BITE_SMALL = 'sfx_fsh_bitesmall.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_BITE_ALERT = 'sfx_fsh_fishbitealert.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_ESCAPE = 'sfx_fsh_fishescape.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_FIGHT_01 = 'sfx_fsh_fishfight01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_FIGHT_02 = 'sfx_fsh_fishfight02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_LARGE_01 = 'sfx_fsh_fishoutlarge01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_LARGE_02 = 'sfx_fsh_fishoutlarge02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_LARGE_03 = 'sfx_fsh_fishoutlarge03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_SMALL_01 = 'sfx_fsh_fishoutsmall01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_SMALL_02 = 'sfx_fsh_fishoutsmall02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_SMALL_03 = 'sfx_fsh_fishoutsmall03.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_CAST_LARGE = 'sfx_fsh_linecastlarge.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_CAST_SMALL = 'sfx_fsh_linecastsmall.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LURE_EQUIP = 'sfx_fsh_lureequip.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_SUCCESS_CAUGHT = 'sfx_fsh_successcaught.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_USABILITY = 'sfx_fsh_useability.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_AMBIENCE = 'sfx_fsh_ambience.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LEGENDARY_REEL_SPIN = 'sfx_fsh_legendaryreelspin.ogg'
SFX_MINIGAME_FISHING_LINE_REEL_FAST = 'sfx_fsh_linereelfast.ogg'
SFX_MINIGAME_FISHING_LINE_REEL_SLOW = 'sfx_fsh_linereelslow.ogg'
SFX_MINIGAME_FISHING_FISH_OUT_MEDIUM_01 = 'sfx_fsh_fishoutmed01.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_FISH_OUT_MEDIUM_02 = 'sfx_fsh_fishoutmed02.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LEGENDARY_MUSIC = 'music_fsh_legendary.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LEGENDARY_RED = 'sfx_fsh_legendaryred.ogg'
SFX_MINIGAME_FISHING_LEGENDARY_GREEN = 'music_fsh_legendarygreen.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LEGENDARY_SUCCESS = 'music_fsh_legendarycaught.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LEGENDARY_FAIL = 'music_fsh_legendaryfail.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LURE_HIT = 'sfx_fsh_lurehit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_LURE_OUT = 'sfx_fsh_lureout.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_REEL_END = 'sfx_fsh_reelend.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_ROD_OUT = 'sfx_fsh_rodout.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_ROD_PUT_AWAY = 'sfx_fsh_rodputaway.%s' % AUDIO_EXTENSION
SFX_MINIGAME_FISHING_SKILL = 'sfx_fsh_fishingSkill.%s' % AUDIO_EXTENSION
MUSIC_MINIGAME_FISHING = 'music_fishing.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_SHIP_SINK = 'sfx_can_shipsink.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_POWDERKEG_EXPLODE = 'sfx_can_powderkeg.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_MAST_BREAK = 'sfx_can_mastbreak.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_MINE_HIT = 'sfx_can_minehit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_ICE_FREEZE = 'sfx_can_icefreeze.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_ICE_HIT = 'sfx_can_icehit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_BOMB_HIT = 'sfx_can_bombhit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_HOTSHOT_HIT = 'sfx_can_hotshothit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_FLAMING = 'sfx_can_flamingprojectile.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_FIRESTORM_HIT = 'sfx_can_firestormhit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_AMMO_BOUGHT = 'sfx_can_ammobought.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_AMMO_OUT = 'sfx_can_ammoout.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_AMMO_DENY = 'sfx_can_ammocantbuy.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_AMMO_RECHARGE = 'sfx_can_ammochrgremind.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_TRANSFORM_REPEATER = 'sfx_can_transformrepeater.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_TRANSFORM_NAVY = 'sfx_can_transformnavy.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_GOLD_ATTACK = 'sfx_can_goldattack.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_SHARK = 'sfx_can_baitshotshark.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_BARREL_LAUNCH = 'sfx_can_barrellaunch.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_BARREL_HIT = 'sfx_can_barrelhit.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_BARREL_SHOTDOWN = 'sfx_can_barrelshotdown.%s' % AUDIO_EXTENSION
SFX_MINIGAME_CANNON_BARREL_CLOSE = 'sfx_can_barrelclose.%s' % AUDIO_EXTENSION
MUSIC_MINIGAME_CANNON = 'music_cannon_repair.%s' % AUDIO_EXTENSION
SFX_LOCKPICK_SUCCESS = 'unlock_success.%s' % AUDIO_EXTENSION
SFX_LOCKPICK_FAIL = 'unlock_fail.%s' % AUDIO_EXTENSION
SFX_LOCKPICK_TRY = 'unlock_try.%s' % AUDIO_EXTENSION
SFX_AVATAR_DIG = 'sfx_avatar_dig.%s' % AUDIO_EXTENSION
SFX_AVATAR_KICK_DOOR = 'sfx_kick_door_loop.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_SAND = 'sfx_avatar_run_sandx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_WOOD = 'sfx_avatar_run_woodx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_CAVE = 'sfx_avatar_run_cavex2.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_ROCK = 'sfx_avatar_run_rockx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_GRASS = 'sfx_avatar_walk_grassx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_GRAVEL = 'sfx_avatar_run_gravelx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_RUN_WATER = 'sfx_avatar_splash_run2.%s' % AUDIO_EXTENSION
SFX_AVATAR_SWIM = 'sfx_avatar_swim.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_SAND = 'sfx_avatar_walk_sandx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_WOOD = 'sfx_avatar_walk_woodx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_CAVE = 'sfx_avatar_walk_cavex2.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_ROCK = 'sfx_avatar_walk_rockx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_GRASS = 'sfx_avatar_walk_grassx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_GRAVEL = 'sfx_avatar_walk_gravelx2.%s' % AUDIO_EXTENSION
SFX_AVATAR_WALK_WATER = 'sfx_avatar_splash_run1.%s' % AUDIO_EXTENSION
SFX_AVATAR_NOISEMAKER = 'sfx_noisemaker.%s' % AUDIO_EXTENSION
SFX_AVATAR_TELEPORT = 'sfx_ship_teleport_out.%s' % AUDIO_EXTENSION
SFX_AVATAR_CLAP = 'sfx_emote_clap.ogg'
SFX_DOOR_SLAM = 'sfx_door_shanty_slam.%s' % AUDIO_EXTENSION
SFX_DOOR_OPEN_ENGLISH = 'sfx_door_english_open.%s' % AUDIO_EXTENSION
SFX_DOOR_OPEN_SHANTY = 'sfx_door_shanty_open.%s' % AUDIO_EXTENSION
SFX_DOOR_OPEN_SPANISH = 'sfx_door_spanish_open.%s' % AUDIO_EXTENSION
SFX_SHIP_RIGGING = 'ship_rigging_std.%s' % AUDIO_EXTENSION
SFX_SHIP_HAMMER = 'ship_deck_hammer.%s' % AUDIO_EXTENSION
SFX_SHIP_SAIL_UNFURL = 'sfx_ship_sails-unfurl.%s' % AUDIO_EXTENSION
SFX_SHIP_SAIL_FURL = 'sfx_ship_sails-furl.%s' % AUDIO_EXTENSION
SFX_SHIP_RAMMING = 'sfx_ship_ramming.%s' % AUDIO_EXTENSION
SFX_SHIP_SINKING = 'sfx_ship_sinking.%s' % AUDIO_EXTENSION
SFX_SHIP_GRAPPLE = 'grappling_ratchet_groan.%s' % AUDIO_EXTENSION
SFX_SHIP_GLASS_BREAK_01 = 'glass_break1.%s' % AUDIO_EXTENSION
SFX_SHIP_GLASS_BREAK_02 = 'glass_break2.%s' % AUDIO_EXTENSION
SFX_SHIP_GLASS_BREAK_03 = 'glass_break3.%s' % AUDIO_EXTENSION
SFX_SHIP_GLASS_BREAK_04 = 'explode-w-glass.%s' % AUDIO_EXTENSION
SFX_SHIP_MAST_BREAK_01 = 'mastBreak1.%s' % AUDIO_EXTENSION
SFX_SHIP_MAST_BREAK_02 = 'mastBreak2.%s' % AUDIO_EXTENSION
SFX_SHIP_SAIL_TEAR = 'x_impact_sail.%s' % AUDIO_EXTENSION
SFX_AMBIENT_SHORE = 'sfx_ocean_shore.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_BUT_OPEN_CUBA = 'VO_Threat_Port_But_Open_Cuba.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_BUT_OPEN_DEVILSANVIL = 'VO_Threat_Port_But_Open_Devilsanvil.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_BUT_OPEN_RAVENSCOVE = 'VO_Threat_Port_But_Open_Ravenscove.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_BUT_OPEN_TORTUGA = 'VO_Threat_Port_But_Open_Tortuga.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_CLOSE_ALL = 'VO_Threat_Port_Close_All.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_CLOSE_CUBA = 'VO_Threat_Port_Close_Cuba.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_CLOSE_DEVILSANVIL = 'VO_Threat_Port_Close_Devilsanvil.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_CLOSE_RAVENSCOVE = 'VO_Threat_Port_Close_Ravenscove.%s' % AUDIO_EXTENSION
VO_THREAT_PORT_CLOSE_TORTUGA = 'VO_Threat_Port_Close_Tortuga.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_BOUNTYHUNTER_A = 'VO_Threat_Inbound_Bountyhunter_a.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_BOUNTYHUNTER_B = 'VO_Threat_Inbound_Bountyhunter_b.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_BOUNTYHUNTER_C = 'VO_Threat_Inbound_Bountyhunter_c.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_WARSHIP_A = 'VO_Threat_Inbound_Warship_a.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_WARSHIP_B = 'VO_Threat_Inbound_Warship_b.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_HELP_A = 'VO_Threat_Inbound_Help_a.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_HELP_B = 'VO_Threat_Inbound_Help_b.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_SIMPLE_A = 'VO_Threat_Inbound_Simple_a.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_SIMPLE_B = 'VO_Threat_Inbound_Simple_b.%s' % AUDIO_EXTENSION
VO_THREAT_INBOUND_SIMPLE_C = 'VO_Threat_Inbound_Simple_c.%s' % AUDIO_EXTENSION
VO_THREAT_L1_ANNOUNCE_A = 'VO_Threat_L1_Announce_a.%s' % AUDIO_EXTENSION
VO_THREAT_L1_ANNOUNCE_B = 'VO_Threat_L1_Announce_b.%s' % AUDIO_EXTENSION
VO_THREAT_L1_ANNOUNCE_C = 'VO_Threat_L1_Announce_c.%s' % AUDIO_EXTENSION
VO_THREAT_L2_ANNOUNCE_A = 'VO_Threat_L2_Announce_a.%s' % AUDIO_EXTENSION
VO_THREAT_L2_ANNOUNCE_B = 'VO_Threat_L2_Announce_b.%s' % AUDIO_EXTENSION
VO_THREAT_L3_ANNOUNCE_A = 'VO_Threat_L3_Announce_a.%s' % AUDIO_EXTENSION
VO_THREAT_L3_ANNOUNCE_B = 'VO_Threat_L3_Announce_b.%s' % AUDIO_EXTENSION
VO_THREAT_L4_ANNOUNCE_A = 'VO_Threat_L4_Announce_a.%s' % AUDIO_EXTENSION
VO_THREAT_CANT_PORT_WILD_A = 'VO_Threat_Cant_Port_Wild_a.%s' % AUDIO_EXTENSION
VO_THREAT_CANT_PORT_NAVY_A = 'VO_Threat_Cant_Port_Navy_a.%s' % AUDIO_EXTENSION
VO_THREAT_CANT_PORT_NAVY_B = 'VO_Threat_Cant_Port_Navy_b.%s' % AUDIO_EXTENSION
VO_THREAT_SHIPSUNK_A = 'VO_Threat_ShipSunk_a.%s' % AUDIO_EXTENSION
VO_THREAT_SHIPSUNK_B = 'VO_Threat_ShipSunk_b.%s' % AUDIO_EXTENSION
VO_THREAT_SHIPSUNK_C = 'VO_Threat_ShipSunk_c.%s' % AUDIO_EXTENSION
VO_THREAT_SHIPSUNK_D = 'VO_Threat_ShipSunk_d.%s' % AUDIO_EXTENSION
VO_THREAT_SHIPSUNK_E = 'VO_Threat_ShipSunk_e.%s' % AUDIO_EXTENSION
VO_THREAT_SHIPSUNK_F = 'VO_Threat_ShipSunk_f.%s' % AUDIO_EXTENSION
VO_THREAT_FORT_SHOOTING_A = 'VO_Threat_Fort_Shooting_a.%s' % AUDIO_EXTENSION
Music2IslandDict = {
    LocationIds.RAMBLESHACK: {
        MUSIC_MAIN: MUSIC_CUBA,
        MUSIC_ALT: MUSIC_CUBA_ALT,
        MUSIC_COMBAT: MUSIC_CUBA_COMBAT },
    LocationIds.RAMBLESHACK_INSIDE: {
        MUSIC_COMBAT: None },
    LocationIds.PORT_ROYAL_ISLAND: {
        MUSIC_MAIN: MUSIC_PORT_ROYAL,
        MUSIC_ALT: MUSIC_PORT_ROYAL_ALT,
        MUSIC_COMBAT: MUSIC_PORT_ROYAL_COMBAT },
    LocationIds.TORTUGA_ISLAND: {
        MUSIC_MAIN: MUSIC_TORTUGA,
        MUSIC_ALT: MUSIC_TORTUGA_ALT,
        MUSIC_COMBAT: MUSIC_TORTUGA_COMBAT },
    LocationIds.DEL_FUEGO_ISLAND: {
        MUSIC_MAIN: MUSIC_PADRES,
        MUSIC_ALT: MUSIC_PADRES_ALT,
        MUSIC_COMBAT: MUSIC_PADRES_COMBAT },
    LocationIds.ANVIL_ISLAND: {
        MUSIC_MAIN: MUSIC_DEVILS_ANVIL,
        MUSIC_ALT: MUSIC_DEVILS_ANVIL_ALT,
        MUSIC_COMBAT: MUSIC_DEVILS_ANVIL_COMBAT },
    LocationIds.DRIFTWOOD_ISLAND: {
        MUSIC_MAIN: MUSIC_DRIFTWOOD,
        MUSIC_ALT: MUSIC_DRIFTWOOD_ALT,
        MUSIC_COMBAT: MUSIC_DRIFTWOOD_COMBAT },
    LocationIds.RUMRUNNER_ISLE: {
        MUSIC_MAIN: MUSIC_RUMRUNNERS,
        MUSIC_ALT: MUSIC_RUMRUNNERS_ALT,
        MUSIC_COMBAT: MUSIC_RUMRUNNERS_COMBAT },
    LocationIds.ISLA_PERDIDA: {
        MUSIC_MAIN: MUSIC_PERDIDA,
        MUSIC_ALT: MUSIC_PERDIDA_ALT,
        MUSIC_COMBAT: MUSIC_PERDIDA_COMBAT },
    LocationIds.CUBA_ISLAND: {
        MUSIC_MAIN: MUSIC_CUBA,
        MUSIC_ALT: MUSIC_CUBA_ALT,
        MUSIC_COMBAT: MUSIC_CUBA_COMBAT },
    LocationIds.KINGSHEAD_ISLAND: {
        MUSIC_MAIN: MUSIC_KINGSHEAD,
        MUSIC_ALT: MUSIC_KINGSHEAD_ALT,
        MUSIC_COMBAT: MUSIC_KINGSHEAD_COMBAT },
    LocationIds.ISLA_CANGREJOS: {
        MUSIC_MAIN: MUSIC_CANGREJOS,
        MUSIC_ALT: MUSIC_CANGREJOS_ALT,
        MUSIC_COMBAT: MUSIC_CANGREJOS_COMBAT },
    LocationIds.CUTTHROAT_ISLAND: {
        MUSIC_MAIN: MUSIC_CUTTHROAT,
        MUSIC_ALT: MUSIC_CUTTHROAT_ALT,
        MUSIC_COMBAT: MUSIC_CUTTHROAT_COMBAT },
    LocationIds.OUTCAST_ISLE: {
        MUSIC_MAIN: MUSIC_OUTCAST,
        MUSIC_ALT: MUSIC_OUTCAST },
    LocationIds.ISLA_TORMENTA: {
        MUSIC_MAIN: MUSIC_TORMENTA,
        MUSIC_ALT: MUSIC_TORMENTA_ALT,
        MUSIC_COMBAT: MUSIC_TORMENTA_COMBAT },
    LocationIds.ISLA_AVARICIA: {
        MUSIC_MAIN: MUSIC_ISLA_AVARICIA,
        MUSIC_ALT: MUSIC_ISLA_AVARICIA },
    LocationIds.ISLA_DE_PORC: {
        MUSIC_MAIN: MUSIC_ISLA_DE_PORC,
        MUSIC_ALT: MUSIC_ISLA_DE_PORC },
    LocationIds.PEARL_ISLAND: {
        MUSIC_ALT: None },
    LocationIds.RAVENS_COVE_ISLAND: {
        MUSIC_MAIN: MUSIC_RAVENS_COVE_DAY,
        MUSIC_ALT: MUSIC_RAVENS_COVE_NIGHT,
        MUSIC_COMBAT: MUSIC_RAVENS_COVE_TOWN_BATTLE },
    LocationIds.RAVENS_COVE_MINE: {
        MUSIC_MAIN: MUSIC_EL_PATRONS_MINE,
        MUSIC_ALT: None,
        MUSIC_COMBAT: MUSIC_RAVENS_COVE_CAVE_BATTLE } }

HolidayMusic2IslandDict = {
    LocationIds.PORT_ROYAL_ISLAND: {
        MUSIC_MAIN: MUSIC_HOLIDAY_02,
        MUSIC_ALT: MUSIC_HOLIDAY_02 },
    LocationIds.TORTUGA_ISLAND: {
        MUSIC_MAIN: MUSIC_HOLIDAY_02,
        MUSIC_ALT: MUSIC_HOLIDAY_02 } }

def getMainMusic(locationId):
    song = MUSIC_DEFAULT_MAIN
    if locationId in Music2IslandDict:
        if MUSIC_MAIN in Music2IslandDict.get(locationId):
            song = Music2IslandDict.get(locationId).get(MUSIC_MAIN)
        if base.cr.newsManager and base.cr.newsManager.getHoliday(17):
            if locationId in HolidayMusic2IslandDict:
                if MUSIC_MAIN in HolidayMusic2IslandDict.get(locationId):
                    song = HolidayMusic2IslandDict.get(locationId).get(MUSIC_MAIN)
    return song

def getAltMusic(locationId):
    song = MUSIC_DEFAULT_ALT
    if locationId in Music2IslandDict:
        if MUSIC_ALT in Music2IslandDict.get(locationId):
            song = Music2IslandDict.get(locationId).get(MUSIC_ALT)
        if base.cr.newsManager and base.cr.newsManager.getHoliday(17):
            if locationId in HolidayMusic2IslandDict:
                if MUSIC_ALT in HolidayMusic2IslandDict.get(locationId):
                    song = HolidayMusic2IslandDict.get(locationId).get(MUSIC_ALT)
    return song

def getCombatMusic(locationId):
    if locationId in Music2IslandDict:
        if MUSIC_COMBAT in Music2IslandDict.get(locationId):
            return Music2IslandDict.get(locationId).get(MUSIC_COMBAT)

    return random.choice([MUSIC_COMBAT_A ,MUSIC_COMBAT_B, MUSIC_COMBAT_C])

def getAmbientFromStr(str):

    if not str:
        return None
    if 'jungle' in str:
        return AMBIENT_JUNGLE
    elif 'cave' in str:
        return AMBIENT_CAVE
    elif 'swamp' in str:
        return AMBIENT_SWAMP
    elif 'volcano' in str:
        return AMBIENT_VOLCANO
    elif 'spanish' in str:
        return AMBIENT_SPANISH
    elif 'shanty' in str:
        return AMBIENT_SHANTY
    elif 'tavern' in str:
        return AMBIENCE_TAVERN_INTERIOR
    elif 'fort' in str:
        return AMBIENCE_FORT
    elif 'jail_interior' in str:
        return AMBIENT_JAIL

Ambient2IslandDict = {
    LocationIds.PORT_ROYAL_ISLAND: {
        AMBIENT_DAY: AMBIENCE_PORT_ROYAL,
        AMBIENT_NIGHT: AMBIENCE_PORT_ROYAL_NIGHT
    },
    LocationIds.KINGSHEAD_ISLAND: {
        AMBIENT_DAY: AMBIENCE_FORT
    },
    LocationIds.ISLA_AVARICIA: {
        AMBIENT_DAY: AMBIENCE_SPANISH,
        AMBIENT_NIGHT: AMBIENCE_SPANISH_NIGHT
    },  
}

def getIslandAmbient(locationId, night=False):
    if locationId in Ambient2IslandDict:
        if not night or not AMBIENT_NIGHT in Ambient2IslandDict[locationId]:
            return Ambient2IslandDict[locationId][AMBIENT_DAY]
        else:
            return Ambient2IslandDict[locationId][AMBIENT_NIGHT]
    return None

SongItem2MusicLabel = {
    UberDogGlobals.InventoryType.Song_1: MUSIC_DRIFTWOOD,
    UberDogGlobals.InventoryType.Song_2: MUSIC_CANGREJOS,
    UberDogGlobals.InventoryType.Song_3: MUSIC_OUTCAST,
    UberDogGlobals.InventoryType.Song_4: MUSIC_PERFORMERS_02,
    UberDogGlobals.InventoryType.Song_5: MUSIC_PERFORMERS_10,
    UberDogGlobals.InventoryType.Song_6: MUSIC_SAILING_E,
    UberDogGlobals.InventoryType.Song_7: MUSIC_JACK_05,
    UberDogGlobals.InventoryType.Song_8: MUSIC_FIREWORKS,
    UberDogGlobals.InventoryType.Song_9: MUSIC_MINIGAME_CANNON,
    UberDogGlobals.InventoryType.Song_10: MUSIC_DEATH,
    UberDogGlobals.InventoryType.Song_11: MUSIC_PERFORMERS_07,
    UberDogGlobals.InventoryType.Song_12: MUSIC_PERFORMERS_09,
    UberDogGlobals.InventoryType.Song_13: MUSIC_CUTTHROAT,
    UberDogGlobals.InventoryType.Song_14: MUSIC_KINGSHEAD,
    UberDogGlobals.InventoryType.Song_15: MUSIC_RUMRUNNERS,
    UberDogGlobals.InventoryType.Song_16: MUSIC_TORTUGA,
    UberDogGlobals.InventoryType.Song_17: MUSIC_SAILING_D,
    UberDogGlobals.InventoryType.Song_18: MUSIC_WHEEL_07,
    UberDogGlobals.InventoryType.Song_19: MUSIC_SHIP_COMBAT_01,
    UberDogGlobals.InventoryType.Song_20: MUSIC_SHIP_COMBAT_02,
    UberDogGlobals.InventoryType.Song_21: MUSIC_HOLIDAY_01,
    UberDogGlobals.InventoryType.Song_22: MUSIC_HOLIDAY_02
}

def getMusicFromSongId(songId):
    return SongItem2MusicLabel.get(songId)

def isSongId(songId):
    return songId in SongItem2MusicLabel

MusicLabel2Length = {
    MUSIC_DRIFTWOOD: 62,
    MUSIC_CANGREJOS: 63,
    MUSIC_OUTCAST: 61,
    MUSIC_TORTUGA: 57,
    MUSIC_DEATH: 16,
    MUSIC_PERFORMERS_02: 64,
    MUSIC_PERFORMERS_07: 68,
    MUSIC_PERFORMERS_09: 62,
    MUSIC_PERFORMERS_10: 65,
    MUSIC_CUTTHROAT: 61,
    MUSIC_KINGSHEAD: 67,
    MUSIC_RUMRUNNERS: 59,
    MUSIC_FIREWORKS: 67,
    MUSIC_REWARD_WEAPON: 12,
    MUSIC_SAILING_A: 63,
    MUSIC_SAILING_B: 63,
    MUSIC_SAILING_C: 66,
    MUSIC_SAILING_D: 62,
    MUSIC_SAILING_E: 61,
    MUSIC_SHIP_COMBAT_01: 60,
    MUSIC_SHIP_COMBAT_02: 90,
    MUSIC_MINIGAME_CANNON: 130,
    MUSIC_JACK_05: 76,
    MUSIC_WHEEL_07: 52,
    MUSIC_HOLIDAY_01: 62,
    MUSIC_HOLIDAY_02: 96
}

def getMusicLength(musicLabel):
    return MusicLabel2Length.get(musicLabel)
