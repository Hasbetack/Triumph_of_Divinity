# from ContainerApp.webapp.routes import datacards
import os
import json


def get_large_json(path, faction_name, json_dir):

    if len(os.listdir(path + faction_name + json_dir)) == 0:
        return []

    list_of_cards = []

    json_files = [pos_json for pos_json in os.listdir(path + faction_name + json_dir) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path + faction_name + json_dir, js), encoding="utf8") as json_file:
            card_dict = json.load(json_file)
            list_of_cards.append(card_dict)

    return list_of_cards


def get_small_json(path, faction_name, json_dir, filename):

    if len(os.listdir(path + faction_name + json_dir)) == 0:
        return {}

    with open(os.path.join(path + faction_name + json_dir + filename), "r", encoding="utf8") as json_file:
        card_dict = json.load(json_file)

    return card_dict


def construct_factions_dict():

    factions_dict = {}

    path = os.getcwd() + "/ContainerApp/webapp/json/"
    factions = os.listdir(path)

    for dir in factions:
        faction_name = os.path.basename(dir)
        factions_dict[faction_name] = {
            "Abilities": get_small_json(path, faction_name, "/abilities/", "abilities.json"),
            "Companies": get_large_json(path, faction_name, "/companies/"),
            "Units": get_large_json(path, faction_name, "/datacards/"),
            "Traits": get_small_json(path, faction_name, "/traits/", "traits.json"),
            "Faction Primary": get_small_json(path, faction_name, "/primaries/", "primaries.json")
        }

    return factions_dict


def load_datacards_from_files():
    factions = construct_factions_dict()
    return factions, factions.keys(), ["Infantry", "Cavalry", "Character", 'Magistro Malitiae', "Elite", "Legendary", "Line Troop"]


def load_changelog_json():
    # Create something like this from saved JSON
    changelog = [
        {
            'Version': '1.0.0',
            'Name': 'First Release',
            'Main_Changes': ['Release of 4 starting factions', 'Launch of the Webapp'],
            'Minor_Changes': [],
            'Notes': ''
        },
        {
            'Version': '1.0.1',
            'Name': 'Balance Patch',
            'Main_Changes': ['Errata for Greeks'],
            'Minor_Changes': ['Poseidon went from 2700 points to 2800 points.', 'Hoplites had their armor save improved to 4+ from 5+ but lost the benefit of +2 to saves if the unit was 15 models or larger.'],
            'Notes': 'Greeks were proving too dependant on Poseidon, so his points were raised to make him less of an autopick. Hoplites are still bad tho lol.'
        },
        {
            'Version': '1.1.0',
            'Name': 'Pirate Update',
            'Main_Changes': ['Release of Pirate faction', 'Points adjustments for Greeks'],
            'Minor_Changes': ['Hoplites went from 20 points per model to 15 points per model.'],
            'Notes': 'Hoplites bad lul.'
        }
    ]
    return changelog


def filter_datacards_by_faction(datacards, searched_factions):
    """
    Returns only datacards that belong to one of the specified
    factions.

    Args:
    datacards:          datastructure containing all datacards.
    searched_factions : list containing faction name keywords searched for.
    """
    assert type(searched_factions) == list, "searched_factions must be a list"
    return {k: v for k, v in datacards.items() if k in searched_factions}


def all_keywords_shared(datacard_keywords, searched_keywords):
    datacard_set = set(datacard_keywords)
    searched_set = set(searched_keywords)
    if (datacard_set | searched_set) == datacard_set:
        return True
    else:
        return False


def any_keywords_shared(datacard_keywords, searched_keywords):
    datacard_set = set(datacard_keywords)
    searched_set = set(searched_keywords)
    if (datacard_set & searched_set):
        return True
    else:
        return False


def filter_datacards_by_keyword(datacards, searched_keywords, strict):
    """
    Returns only datacards that contain the specified unit keywords.
    Can be set to either any or all searched keywords must be present on datacard
    for it to be shown.

    Args:
    datacards:         datastructure containing all datacards.
    searched_keywords: list containing unit keywords searched for.
    strict (bool):     if True all searched_keywords must be present on the datacard, otherwise at least one must be present.
    """
    assert type(searched_keywords) == list, "searched_keywords must be a list"
    for faction in datacards.keys():
        if strict:
            datacards[faction]["Units"] = [unit for unit in datacards[faction]["Units"] if all_keywords_shared(unit["Keywords"], searched_keywords)]
        else:
            datacards[faction]["Units"] = [unit for unit in datacards[faction]["Units"] if any_keywords_shared(unit["Keywords"], searched_keywords)]
    return datacards
