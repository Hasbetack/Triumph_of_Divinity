# from ContainerApp.webapp.routes import datacards
import os
import json

class Content_Loader:
    def __init__(self):
        self.RULES = ""             # string object with html from Google Drive rules doc
        self.WEAPON_ABILITIES = {}  # dictionary of all weapon abilities
        self.DATACARD_TAGS = []     # list of all tags present on any datacard
        self.DATACARDS = {}         # dict, keys are faction names
        self.FACTIONS = []          # list of all factions

        self.load_content()


    def load_content(self):
        path_json = os.getcwd() + "/ContainerApp/webapp/json/"
        path_armies = path_json + "/armies"
        path_game_data = path_json + "/game_data"

        assert os.path.exists(path_armies), "Could not find armies folder"
        assert os.path.exists(path_game_data), "Could not find game_data folder"

        assert os.path.isdir(path_armies), "Found something called 'armies' that is not folder"
        assert os.path.isdir(path_game_data), "Found something called 'game_data' that is not folder"

        factions = os.listdir(path_armies)
        faction_folders = []

        for faction in factions:
            faction_path = os.path.join(path_armies, faction)
            assert os.path.isdir(faction_path), "{} is not a folder in 'armies' folder".format(faction)
            faction_folders.append(faction_path)

        self._load_game_data(path_game_data)
        self._load_datacards(faction_folders)


    def weapon_ability_tooltip(self, weapon_ability):
        """
        Returns a specific weapon tooltip as a string.

        Args:
        weapon_ability: the key to get the value of.
        """
        assert isinstance(weapon_ability, str), "Was passed {}: weapon ability must be a string".format(weapon_ability)

        if weapon_ability.count("(") == 1 and weapon_ability.count(")") == 1:
            contents = weapon_ability[weapon_ability.find("(") + 1:weapon_ability.find(")")]
            weapon_ability = weapon_ability.split("(")[0].strip()

            if weapon_ability not in self.WEAPON_ABILITIES.keys():
                return "ERROR"

            tooltip = self.WEAPON_ABILITIES[weapon_ability].replace("X", contents)
            return tooltip

        if weapon_ability not in self.WEAPON_ABILITIES.keys():
            return "ERROR"

        tooltip = self.WEAPON_ABILITIES[weapon_ability]

        return tooltip

    def _load_datacards(self, faction_folders):
        for faction_folder in faction_folders:
            faction_name = os.path.basename(faction_folder).replace("_", " ")
            self.DATACARDS[faction_name] = {
                "Abilities":       self._load_faction_abilities(faction_folder),
                "Companies":       self._load_faction_companies(faction_folder),
                "Units":           self._load_faction_units(faction_folder),
                "Traits":          self._load_faction_traits(faction_folder),
                "Faction Primary": self._load_faction_primary(faction_folder),
            }
            self.FACTIONS.append(faction_name)


    def _load_game_data(self, path_game_data):
        path_rules = path_game_data + "/rules.json"
        path_weapon_abilities = path_game_data + "/weapon_abilities.json"
        path_formation_tags = path_game_data + "/formation_tags.json"

        assert os.path.isfile(path_rules), "Could not find rules.json"
        assert os.path.isfile(path_weapon_abilities), "Could not find weapon_abilities.json"
        assert os.path.isfile(path_formation_tags), "Could not find formation_tags.json"

        with open(path_rules, "r", encoding="utf8") as json_rules:
            self.RULES = json.load(json_rules)

        with open(path_weapon_abilities, "r", encoding="utf8") as json_weapon_abilities:
            self.WEAPON_ABILITIES = json.load(json_weapon_abilities)

        with open(path_formation_tags, "r", encoding="utf8") as json_formation_tags:
            self.DATACARD_TAGS = json.load(json_formation_tags)


    def _load_faction_abilities(self, faction_folder):
        path_abilities = faction_folder + "/abilities"
        if not os.path.exists(path_abilities):
            print("In {}: Did not contain a folder 'abilities'".format(faction_folder))
            return {}

        path_abilities_json = path_abilities + "/abilities.json"
        if not os.path.exists(path_abilities_json):
            print("In {}: Did not contain 'abilities.json'".format(path_abilities))
            return {}

        abilities = {}
        with open(path_abilities_json, "r", encoding="utf8") as json_abilities:
            abilities = json.load(json_abilities)
        
        assert isinstance(abilities, dict), "In {}: Abilities must be stored in dict".format(path_abilities_json)

        if len(abilities.keys()) == 0:
            print("In {}: Found empty dict".format(path_abilities_json))
            return {}

        for ability_name in abilities.keys():
            assert isinstance(ability_name, str), "In {}: Ability names must be of type str".format(path_abilities_json)
            assert isinstance(abilities[ability_name], str), "In {}: Ability descriptions must be of type str".format(path_abilities_json)

        return abilities


    def _load_faction_companies(self, faction_folder):
        path_companies = faction_folder + "/companies"
        if not os.path.exists(path_companies):
            print("In {}: Did not contain a folder 'companies'".format(faction_folder))
            return []

        companies = []
        company_jsons = os.listdir(path_companies)
        for company_json in company_jsons:
            path_company_json = os.path.join(path_companies, company_json)
            assert os.path.isfile(path_company_json), "Contents of {} must be json files".format(path_companies)
            
            company = {}
            with open(path_company_json, "r", encoding="utf8") as json_company:
                company = json.load(json_company)

            assert isinstance(company, dict), "In {}: Companies must be stored in dict".format(path_company_json)

            if len(company.keys()) == 0:
                print("In {}: Found empty json".format(path_company_json))
                continue

            assert "Name" in company.keys(),         "In {}: Cannot find key 'Name'".format(path_company_json)
            assert "Points" in company.keys(),       "In {}: Cannot find key 'Points'".format(path_company_json)
            assert "Requirements" in company.keys(), "In {}: Cannot find key 'Requirements'".format(path_company_json)
            assert "Effect" in company.keys(),       "In {}: Cannot find key 'Effect'".format(path_company_json)

            assert len(company.keys()) == 4, "In {}: Contains one or more unrecognized keys".format(path_company_json)

            assert isinstance(company["Name"], str),          "In {}: 'Name' must be of type string".format(path_company_json)
            assert isinstance(company["Points"], int),        "In {}: 'Points' must be of type int".format(path_company_json)
            assert isinstance(company["Requirements"], list), "In {}: 'Requirements' must be of type list".format(path_company_json)
            assert isinstance(company["Effect"], str),        "In {}: 'Effect' must be of type string".format(path_company_json)
            
            for requirement in company["Requirements"]:
                assert isinstance(requirement, str), "In {}: Each element of 'Requirements' must be of type string".format(path_company_json)

            companies.append(company)

        return companies


    def _load_faction_units(self, faction_folder):
        path_datacards = faction_folder + "/datacards"
        if not os.path.exists(path_datacards):
            print("In {}: Did not contain a folder 'datacards'".format(faction_folder))
            return []

        units = []
        unit_jsons = os.listdir(path_datacards)
        for unit_json in unit_jsons:
            path_unit_json = os.path.join(path_datacards, unit_json)
            assert os.path.isfile(path_unit_json), "Contents of {} must be json files".format(path_datacards)
            
            unit = {}
            with open(path_unit_json, "r", encoding="utf8") as json_unit:
                unit = json.load(json_unit)

            assert isinstance(unit, dict), "In {}: Units must be stored in dict".format(path_unit_json)

            if len(unit.keys()) == 0:
                print("In {}: Found empty json".format(path_unit_json))
                continue  
            
            # TODO add content type checks
            UNIT_KEYS = [
                "Name", 
                "Keywords", 
                "Points", 
                "Unit_Size", 
                "Move", 
                "Dash", 
                "Weapons", 
                "Faction_Abilities",
                "Unit_Abilities",
                "Caster",
                "Spells"]

            assert all_keywords_shared(UNIT_KEYS, unit.keys()), "In {}: Includes unknown dictionary keyowrds".format(path_unit_json)

            assert isinstance(unit["Name"], str), "In {}: Unit name must be string".format(path_unit_json)
            assert isinstance(unit["Keywords"], list), "In {}: Unit Keywords must be in a list".format(path_unit_json)
            assert isinstance(unit["Points"], int), "In {}: Unit points must be int".format(path_unit_json)
            assert isinstance(unit["Unit_Size"], dict), "In {}: Unit size must be dict".format(path_unit_json)

            # TODO add check for keywords being in DATACARD_TAGS
            # TODO add check for each weapon_ability being in WEAPON_ABILITIES 
            units.append(unit)

        return units


    def _load_faction_traits(self, faction_folder):
        return {}


    def _load_faction_primary(self, faction_folder):
        return {}


def rules_parser(rules):
    # given string from json doc containing ToD rules
    pass


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
