# from ContainerApp.webapp.routes import datacards
import os
import json

class Content_Loader:
    def __init__():
        self.DATACARD_TAGS = [] # list of all tags present on any datacard
        self.RULES = ""         # string object with html from Google Drive rules doc
        self.DATACARDS = {}     # dict, keys are faction names

    def _load_rules():
        pass

    def _load_datacards():
        pass


def get_large_json(path, faction_name, json_dir):
    """
    Returns a list of dictionaries containing data extracted from multiple JSON files.
    Function is data agnostic but should only be used when a list of dictionaries is required.

    Args:
    path: base path to pull files from NOTE: this should be changed before the full deployment.
    faction_name: the parent folder for all faction related JSON files.
    json_dir: the directory inside the factions directory that the function pulls files from.
    """

    # TODO Replace fixed directories with ones from a .env file.

    if not os.path.isdir(path + faction_name + json_dir) or len(os.listdir(path + faction_name + json_dir)) == 0:
        return []

    list_of_cards = []

    json_files = [pos_json for pos_json in os.listdir(path + faction_name + json_dir) if pos_json.endswith('.json')]

    for index, js in enumerate(json_files):
        with open(os.path.join(path + faction_name + json_dir, js), encoding="utf8") as json_file:
            card_dict = json.load(json_file)
            list_of_cards.append(card_dict)

    return list_of_cards


def get_small_json(path, faction_name, json_dir, filename):
    """
    Returns a dictionary from a JSON file in the given directory.
    Function is data agnostic.

    Args:
    path: base path to pull files from NOTE: this should be changed before the full deployment.
    faction_name: the parent folder for all faction related JSON files.
    json_dir: the directory inside the factions directory that the function pulls files from.
    filename: the specific JSON file this function will read.
    """

    # TODO Replace fixed directories with ones from a .env file.

    if not os.path.isdir(path + faction_name + json_dir) or len(os.listdir(path + faction_name + json_dir)) == 0:
        return {}

    with open(os.path.join(path + faction_name + json_dir + filename), "r", encoding="utf8") as json_file:
        card_dict = json.load(json_file)

    return card_dict


def construct_factions_dict():
    """
    Returns a dictionary from of data constructed from multiple JSON files.
    """

    # TODO Replace fixed directories with ones from a .env file.

    factions_dict = {}

    path = os.getcwd() + "/ContainerApp/webapp/json/"
    factions = os.listdir(path)

    for li in factions:
        if li.endswith(".json"):
            factions.remove(li)

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


def load_weapon_abilities():
    """
    Returns a dictionary of weapon abilities from a JSON file.
    """

    # TODO Replace fixed directories with ones from a .env file.

    weapon_abilities = {}

    with open(os.path.join("ContainerApp/webapp/json/weapon_abilities.json"), "r", encoding="utf8") as json_file:
        weapon_abilities = json.load(json_file)

    return weapon_abilities


def load_changelog_json():
    """
    Returns a list of dictionaries using changelog data pulled from JSON files.
    """

    # TODO Replace fixed directories with ones from a .env file.

    changelog = []

    json_files = [pos_json for pos_json in os.listdir("ContainerApp/webapp/changelogs/") if pos_json.endswith('.json')]

    for index, js in enumerate(json_files):
        with open(os.path.join("ContainerApp/webapp/changelogs/", js), encoding="utf8") as json_file:
            changelog_dict = json.load(json_file)
            changelog.append(changelog_dict)

    return changelog


def weapon_ability_tooltip(weapon_ability):
    """
    Returns a specific weapon tooltip as a string.

    Args:
    weapon_ability: the key to get the value of.
    """

    # TODO Replace fixed directories with ones from a .env file.

    assert isinstance(weapon_ability, str), "weapon ability must be a string"

    weapon_abilities = load_weapon_abilities()

    if weapon_ability.count("(") == 1 and weapon_ability.count(")") == 1:
        contents = weapon_ability[weapon_ability.find("(") + 1:weapon_ability.find(")")]
        weapon_ability = weapon_ability.split("(")[0].strip()

        if weapon_ability not in weapon_abilities.keys():
            return "ERROR"

        tooltip = weapon_abilities[weapon_ability].replace("X", contents)

    if weapon_ability not in weapon_abilities.keys():
        return "ERROR"

    tooltip = weapon_abilities[weapon_ability]

    return tooltip


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

    return False


def any_keywords_shared(datacard_keywords, searched_keywords):
    datacard_set = set(datacard_keywords)
    searched_set = set(searched_keywords)

    if (datacard_set & searched_set):
        return True

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
