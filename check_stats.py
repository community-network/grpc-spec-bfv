import json
from statics import BFV_WEAPONS, BFV_VEHICLES, BFV_CLASSES, BFV_STAT_GAMEMODE, BFV_STAT_GAMEMODE_EXTR, BFV_STAT_MAPS

with open('t.json', 'r') as f:
    data = json.load(f)

    new_dict = {}
    # MP data
    for field in data["playerStats"][0]["categories"][1]["catFields"]["fields"]:
        new_dict[field["name"]] = field.get("value", None)

    for item in BFV_WEAPONS:
        _ = [new_dict.pop(current+item, None) for current in ["kw_", "scrw_", "hsw_", "shw_", "sfw_", "tpw_"]]
    for item in BFV_VEHICLES:
        _ = [new_dict.pop(current+item, None) for current in ["tpw_", "kw_", "vdw_"]]
    for item in BFV_CLASSES:
        _ = [new_dict.pop("kit_"+item+current, None) for current in ["_kills", "_deaths", "_time", "_hits", "_shots"]]
        _ = [new_dict.pop(current+item, None) for current in ["rank_", "sc_"]]
    for item in BFV_STAT_GAMEMODE:
        _ = [new_dict.pop(item+current, None) for current in ["_wins", "_losses"]]
        extra = BFV_STAT_GAMEMODE_EXTR.get(item)
        _ = [new_dict.pop(current+extra, None) for current in ["sc_"]]
        _ = [new_dict.pop(current+extra+"_raw", None) for current in ["sc_"]]
    for item in BFV_STAT_MAPS:
        _ = [new_dict.pop(current+item, None) for current in ["sc_lvl_"]]
        _ = [new_dict.pop(current+item+"_raw", None) for current in ["sc_lvl_"]]

    ##### remove _raw
    to_remove = []
    for item in new_dict:
        if item.endswith("_raw"):
            to_remove.append(item)
    _ = [new_dict.pop(current, None) for current in to_remove]
    #####

    others = [
        "rank",
        "wins",
        "losses",
        "kills",
        "deaths",
        "headshots",
        "rounds_completed",
        "longest_hs",
        "revives",
        "dogtags",
        "awardScore",
        "bonusScore",
        "squadScore",
        "avenger_kills",
        "savior_kills",
        "heals",
        "repairs",
        "kill_assists",
        "time",
        "sc_roundscore",
        "hits",
        "shots",
        "resupplies",
        "highest_ks",
        "rounds",
        "objective_armed",
        "objective_destroyed",
        "objective_disarmed",
        "sc_objective",
        "sc_car",
        "sc_amr",
        "sc_vehicles",
        "sc_weapons",
        "sc_assaultrifles",
        "sc_mmgs",
        "sc_lmgs",
        "sc_squad",
        "sc_gamemode",
        "sc_transportvehicles",
        "sc_shotguns",
        "sc_sars",
        "sc_alllandvehicles",
        "sc_combat",
        "sc_award",
        "sc_tanks",
        "kills_pvp",
        "kills_offensive",
        "kills_defensive",
        "kills_aggregated",
        "nemesis_kills",
        "resupplies_support",
        "resupplies_medic",
        "heals_medic",
        "repairs_support",
        "vehicle_damage",
        "soldier_damages",
    ]
    _ = [new_dict.pop(current, None) for current in others]

    with open("unused.json", "w", encoding="utf-8") as f:
        json.dump(new_dict, f, ensure_ascii=False, indent=4)
