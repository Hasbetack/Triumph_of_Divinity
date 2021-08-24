def load_datacard_json():
    # Create something like this from saved JSON
    # Return the datastructure, a list of all factions in it, a list of all keywords
    datacards = {
        'Greeks': {
            'Abilities': {
            },
            'Companies': [
                {
                    'Name': 'The Gates of the Underworld',
                    'Points': 600,
                    'Requirements': ['Requirement 1', 'Requirement 2', 'Requirement 3'],
                    'Effect': 'Effect description'
                },
                {
                    'Name': 'The Gift of Greed',
                    'Points': 200,
                    'Requirements': ['Requirement 1', 'Requirement 2'],
                    'Effect': 'Effect description 2'
                }
            ],
            'Units': [
                {
                    'Name': 'Poseidon',
                    'Keywords': ['Character', 'Legendary'],
                    'Points': 2700,
                    'Unit_Size': {'min': 1, 'max': 1},
                    'Move': 12,
                    'Dash': 7,
                    'Faction_Abilities': [],
                    'Unit_Abilities': [],
                    # etc...
                    'Caster': 3,
                    'Spells': [
                        {
                            'Name': 'Rage of the Ocean (35)',
                            'Effect': 'Select D3 enemy formations within 18” of the caster. Then roll 2D6 for each model in each formation (to a maximum of 15 D6). For each 4+ that model’s formation suffers 1 ethereal damage.'
                        }   
                    ]                   
                },
                {
                    'Name': 'Hoplites',
                    'Keywords': ['Infantry', 'Line Troop'],
                    'Points': 20,
                    'Unit_Size': {'min': 10, 'max': 20},
                    'Move': 5,
                    'Dash': 4,
                    'Faction_Abilities': [],
                    'Unit_Abilities': []
                    # etc...
                }
            ]
        },
        'Romans': {
            'Abilities': {
                'Servants of the Emperor': 'While a friendly <span class="datacard-keyword">MAGISTRO MALITAE CHARACTER</span> is within 6" of this formation, then models in this formation cannot fail Will tests.'
            },
            'Companies': [
                {
                    'Name': 'The Chosen Sons',
                    'Points': 500,
                    'Requirements': ['Requirement 1', 'Requirement 2', 'Requirement 3'],
                    'Effect': 'Effect description'
                },
                {
                    'Name': 'The Eternal Wall',
                    'Points': 200,
                    'Requirements': ['Requirement 1', 'Requirement 2'],
                    'Effect': 'Effect description 2'
                }
            ],
            'Units': [
                {
                    'Name': 'Scholae Palatine',
                    'Keywords': ['Cavalry', 'Elite', 'Magistro Malitiae'],
                    'Points': 90,
                    'Unit_Size': {'min': 3, 'max': 6},
                    'Move': 12,
                    'Dash': 6,
                    # etc...
                    'Weapons': [
                        {
                            'Cost': 0,
                            'Name': 'blah',
                            'Type': 'blah',
                            'Range': 'blah',
                            'Wound': 'blah',
                            'Rend': 'blah',
                            'D': 'blah',
                            'Abilities': 'blah'
                        },
                        {
                            'Cost': 0,
                            'Name': 'blah',
                            'Type': 'blah',
                            'Range': 'blah',
                            'Wound': 'blah',
                            'Rend': 'blah',
                            'D': 'blah',
                            'Abilities': 'blah'
                        }
                    ],
                    'Faction_Abilities': ['Servants of the Emperor'],
                    'Unit_Abilities': [
                        {
                            'Ability_Name': "The Emperor's Bodyguard",
                            'Ability_Effect': 'While a friendly <span class="datacard-keyword">MAGISTRO MALITIAE CHARACTER</span> is within 3" of this formation then that character cannot be selected as the target of ranged attacks.'
                        },
                        {
                            'Ability_Name': 'Militiae Battle Shield',
                            'Ability_Effect': 'Improve the Armour of models in this formation by 1.'
                        }
                    ],
                    'Caster': False,
                    'Spells': []
                },
                {
                    'Name': 'Centurion',
                    'Keywords': ['Infantry', 'Character', 'Magistro Malitiae'],
                    'Points': 240,
                    'Unit_Size': {'min': 1, 'max': 1},
                    'Move': 6,
                    'Dash': 4,
                    'Faction_Abilities': [],
                    'Unit_Abilities': []
                    # etc...
                }
            ]
        }
    }
    return datacards, datacards.keys(), ["Infantry", "Cavalry", "Character", 'Magistro Malitiae', "Elite", "Legendary", "Line Troop"]

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
    assert type(searched_factions) == list, "seached_factions must be a list"
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
    assert type(searched_keywords) == list, "seached_keywords must be a list"
    for faction in datacards.keys():
        if strict:
            datacards[faction]["Units"] = [unit for unit in datacards[faction]["Units"] if all_keywords_shared(unit["Keywords"], searched_keywords)]
        else:
            datacards[faction]["Units"] = [unit for unit in datacards[faction]["Units"] if any_keywords_shared(unit["Keywords"], searched_keywords)]
    return datacards
