

@router.get(
    "/bfv/temp/",
    summary="Get all stats for website",
    description=doc.pidOidnameInfo,
    responses=doc.bfAllExample,
    response_model=combined_response.BfvCombined,
)
async def bfvTemp(
    persona: dict = Depends(personaResolver),
    lang: Tag = Depends(valid_language_tag),
    format_values: Optional[bool] = True,
):
    methods = [
        "Stats.detailedStatsByPersonaId",
        "Progression.getSoldierClasses",
        *constants.SPARTA_COMMON_ALL_STATS_METHODS,
    ]

    (
        overview_stats,
        class_stats,
        weapons_stats,
        vehicle_stats,
        active_platoon,
        platoons,
        *_,
    ) = await jsonrpc_call_methods_persona("casablanca", lang, methods, persona)
    
    if overview_stats.get("result", None) is not None:
        raw_stats = await grpc_client.get_stats(
            [persona.get("personaId")], True, format_values, multiple=True
        )
        
        new_dict = {}
        for field in raw_stats["playerStats"][0]["categories"][1]["catFields"]["fields"]:
            new_dict[field["name"]] = field.get("value", None)
        
        def add_vehicle(vehicle_result, key, vehicle_group, vehicle):
            vehicle_result[key] = {"type": vehicle_group["name"].capitalize(), "vehicleName": vehicle["name"], "image": replace_bb_prefix(vehicle["imageUrl"])}
            return vehicle_result
        
        def add_weapon(weapon_result, key, weapon_group, weapon):
            weapon_result[key] = {"type": weapon_group["name"].capitalize(), "weaponName": weapon["name"], "image": replace_bb_prefix(weapon["imageUrl"])}
            return weapon_result

        
        with open("results/vehicle_result.json", "r+", encoding="utf-8") as r:
            vehicle_result = json.load(r)
        
            for vehicle_group in vehicle_stats["result"]:
                for vehicle in vehicle_group["vehicles"]:
                    values = vehicle["stats"]["values"]
                    keys = list(filter(lambda x: new_dict[x] == int(values.get("seconds", 0)) and "tpw_" in x, new_dict))
                    if len(keys) == 1:
                        vehicle_result = add_vehicle(vehicle_result, keys[0].replace("tpw_", ""), vehicle_group, vehicle)
                    else:
                        keys = list(filter(lambda x: new_dict[x] == int(values.get("kills", 0)) and "kw_" in x, new_dict))
                        if len(keys) == 1:
                            vehicle_result = add_vehicle(vehicle_result, keys[0].replace("kw_", ""), vehicle_group, vehicle)
                        else:
                            keys = list(filter(lambda x: new_dict[x] == int(values.get("vehicle destroy", 0)) and "vdw_" in x, new_dict))
                            if len(keys) == 1:
                                vehicle_result = add_vehicle(vehicle_result, keys[0].replace("vdw_", ""), vehicle_group, vehicle)
            
            vehicle_names = [value['vehicleName'] for key, value in vehicle_result.items()]
            
            others = []
            for vehicle_group in vehicle_stats["result"]:
                for vehicle in vehicle_group["vehicles"]:
                    if vehicle["name"] not in vehicle_names:
                        others.append(vehicle["name"])
            print(len(others), ": ", others)
                
            r.seek(0)
            json.dump(vehicle_result, r, ensure_ascii=False, indent=4)
        
        with open("results/weapon_result.json", "r+", encoding="utf-8") as wr:
            weapon_result = json.load(wr)
        
            for weapon_group in weapons_stats["result"]:
                for weapon in weapon_group["weapons"]:
                    values = weapon["stats"]["values"]
                    keys = list(filter(lambda x: new_dict[x] == int(values.get("seconds", 0)) and "tpw_" in x, new_dict))
                    if len(keys) == 1:
                        weapon_result = add_weapon(weapon_result, keys[0].replace("tpw_", ""), weapon_group, weapon)
                    else:
                        keys = list(filter(lambda x: new_dict[x] == int(values.get("score", 0)) and "scrw_" in x, new_dict))
                        if len(keys) == 1:
                            weapon_result = add_weapon(weapon_result, keys[0].replace("scrw_", ""), weapon_group, weapon)
                        else:
                            keys = list(filter(lambda x: new_dict[x] == int(values.get("kills", 0)) and "kw_" in x, new_dict))
                            if len(keys) == 1:
                                weapon_result = add_weapon(weapon_result, keys[0].replace("kw_", ""), weapon_group, weapon)
                            else:
                                keys = list(filter(lambda x: new_dict[x] == int(values.get("shots", 0)) and "sfw_" in x, new_dict))
                                if len(keys) == 1:
                                    weapon_result = add_weapon(weapon_result, keys[0].replace("sfw_", ""), weapon_group, weapon)
            
            weapon_names = [value['weaponName'] for key, value in weapon_result.items()]
            
            others = []
            for weapon_group in weapons_stats["result"]:
                for weapon in weapon_group["weapons"]:
                    if weapon["name"] not in weapon_names:
                        others.append(weapon["name"])
            print(len(others), ": ", others)
                
            wr.seek(0)
            json.dump(weapon_result, wr, ensure_ascii=False, indent=4)
        
        
        stats = {
            **await bf5.format_overview_stats(overview_stats, format_values),
            "classes": await companion.format_bfv_class_stats(class_stats),
            "weapons": await companion.format_weapon_stats(
                weapons_stats, format_values
            ),
            "vehicles": await companion.format_vehicle_stats(
                vehicle_stats, "vehicle destroy"
            ),
            "activePlatoon": await companion.format_player_active_platoon(
                active_platoon
            ),
            "platoons": await companion.format_player_platoon_list(platoons),
        }
        return PersonaStatsJSONResponse(content=stats, persona=persona)
    else:
        raise HTTPException(status_code=404, detail="playername not found")



@router.get(
    "/bfv/all/",
    summary="Get all stats for website",
    description=doc.pidOidnameInfo,
    responses=doc.bfAllExample,
    response_model=combined_response.BfvCombined,
)
async def bfvAll(
    persona: dict = Depends(personaResolver),
    lang: Tag = Depends(valid_language_tag),
    format_values: Optional[bool] = True,
):
    methods = [
        "Stats.detailedStatsByPersonaId",
        "Progression.getSoldierClasses",
        *constants.SPARTA_COMMON_ALL_STATS_METHODS,
    ]

    (
        overview_stats,
        class_stats,
        weapons_stats,
        vehicle_stats,
        active_platoon,
        platoons,
        *_,
    ) = await jsonrpc_call_methods_persona("casablanca", lang, methods, persona)
    
    with open("overview_stats.json", "w", encoding="utf-8") as f:
        json.dump(overview_stats, f, ensure_ascii=False, indent=4)
    with open("class_stats.json", "w", encoding="utf-8") as f:
        json.dump(class_stats, f, ensure_ascii=False, indent=4)
    with open("weapons_stats.json", "w", encoding="utf-8") as f:
        json.dump(weapons_stats, f, ensure_ascii=False, indent=4)
    with open("vehicle_stats.json", "w", encoding="utf-8") as f:
        json.dump(vehicle_stats, f, ensure_ascii=False, indent=4)

    
    if overview_stats.get("result", None) is not None:
        stats = {
            **await bf5.format_overview_stats(overview_stats, format_values),
            "classes": await companion.format_bfv_class_stats(class_stats),
            "weapons": await companion.format_weapon_stats(
                weapons_stats, format_values
            ),
            "vehicles": await companion.format_vehicle_stats(
                vehicle_stats, "vehicle destroy"
            ),
            "activePlatoon": await companion.format_player_active_platoon(
                active_platoon
            ),
            "platoons": await companion.format_player_platoon_list(platoons),
        }
        return PersonaStatsJSONResponse(content=stats, persona=persona)
    else:
        raise HTTPException(status_code=404, detail="playername not found")
