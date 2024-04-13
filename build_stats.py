import json

def replace_bb_prefix(url_with_prefix: str) -> str:
    return url_with_prefix.replace(
        "[BB_PREFIX]", "https://eaassets-a.akamaihd.net/battlelog/battlebinary"
    )

def add_vehicle(vehicle_result, key, vehicle_group, vehicle):
    vehicle_result[key] = {"type": vehicle_group["name"].capitalize(), "vehicleName": vehicle["name"], "image": replace_bb_prefix(vehicle["imageUrl"])}
    return vehicle_result

with open('t.json', 'r') as f:
    data = json.load(f)
    
    new_dict = {}
    # MP data
    for field in data["playerStats"][0]["categories"][1]["catFields"]["fields"]:
        new_dict[field["name"]] = field.get("value", None)
    
    with open('vehicle_stats.json', 'r') as v:
        vehicles = json.load(v)
        vehicle_result = {}
        others = []
        
        with open("results/vehicle_result.json", "r+", encoding="utf-8") as r:
            vehicle_result = json.load(r)
        
            for vehicle_group in vehicles["result"]:
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
            for vehicle_group in vehicles["result"]:
                for vehicle in vehicle_group["vehicles"]:
                    if vehicle["name"] not in vehicle_names:
                        print(vehicle["name"])
                
            print(len(vehicle_result))
            
            r.seek(0)
            json.dump(vehicle_result, r, ensure_ascii=False, indent=4)
    
    # with open('weapons_stats.json', 'r') as w:
    #     weapons = json.load(w)
        
    #     weapon_list = []
    #     weapon_result = {}
    #     others = []
        
    #     for weapon_group in weapons["result"]:
    #         for weapon in weapon_group["weapons"]:
    #             values = weapon["stats"]["values"]
    #             seconds_used = int(values.get("seconds", 0))
    #             keys = list(filter(lambda x: new_dict[x] == seconds_used and "tpw_" in x, new_dict))
    #             # if len(keys) > 1:
    #             #     print("to many for", weapon["name"], keys)
    #             # elif len(keys) < 1:
    #             #     print("not found for", weapon["name"], keys)
    #             if len(keys) == 1:
    #                 weapon_result[keys[0].replace("tpw_", "")] = {"type": weapon_group["name"].capitalize(), "weaponName": weapon["name"], "image": replace_bb_prefix(weapon["imageUrl"])}
    #             else:
    #                 others.append({"weapon": weapon, "group": {"name": weapon_group["name"]}})
                    
    #     new_others = []
    #     for weapon in others:
    #         values = weapon["weapon"]["stats"]["values"]
    #         score = int(values.get("score", 0))
    #         keys = list(filter(lambda x: new_dict[x] == score and "scrw_" in x, new_dict))
    #         if len(keys) == 1:
    #             weapon_result[keys[0].replace("scrw_", "")] = {"type": weapon["group"]["name"].capitalize(), "weaponName": weapon["weapon"]["name"], "image": replace_bb_prefix(weapon["weapon"]["imageUrl"])}
    #         else:
    #             new_others.append(weapon)
                
        
    #     others = []
    #     for weapon in new_others:
    #         values = weapon["weapon"]["stats"]["values"]
    #         kills = int(values.get("kills", 0))
    #         keys = list(filter(lambda x: new_dict[x] == kills and "kw_" in x, new_dict))
    #         if len(keys) == 1:
    #             weapon_result[keys[0].replace("kw_", "")] = {"type": weapon["group"]["name"].capitalize(), "weaponName": weapon["weapon"]["name"], "image": replace_bb_prefix(weapon["weapon"]["imageUrl"])}
    #         else:
    #             others.append(weapon)
                
                
    #     new_others = []
    #     for weapon in others:
    #         values = weapon["weapon"]["stats"]["values"]
    #         shots = int(values.get("shots", 0))
    #         keys = list(filter(lambda x: new_dict[x] == shots and "sfw_" in x, new_dict))
    #         if len(keys) == 1:
    #             weapon_result[keys[0].replace("sfw_", "")] = {"type": weapon["group"]["name"].capitalize(), "weaponName": weapon["weapon"]["name"], "image": replace_bb_prefix(weapon["weapon"]["imageUrl"])}
    #         else:
    #             new_others.append(weapon)
                
    #     print(len(new_others))
    #     print(len(weapon_result))
    #     with open("results/weapon_result.json", "w", encoding="utf-8") as f:
    #         json.dump(weapon_result, f, ensure_ascii=False, indent=4)
    #     with open("results/other_weapons.json", "w", encoding="utf-8") as f:
    #         json.dump(new_others, f, ensure_ascii=False, indent=4)