def load_datacard_json():
    # I need to create something like this from saved JSON
    datacards = {
        'Greeks': {
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
                    'Dash': 7
                    # etc...
                },
                {
                    'Name': 'Hoplites',
                    'Keywords': ['Infantry', 'Line Troop'],
                    'Points': 20,
                    'Unit_Size': {'min': 10, 'max': 20},
                    'Move': 5,
                    'Dash': 4
                    # etc...
                }
            ]
        },
        'Romans': {
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
                    'Dash': 6
                    # etc...
                },
                {
                    'Name': 'Centurion',
                    'Keywords': ['Infantry', 'Character', 'Magistro Malitiae'],
                    'Points': 240,
                    'Unit_Size': {'min': 1, 'max': 2},
                    'Move': 6,
                    'Dash': 4
                    # etc...
                }
            ]
        }
    }
    return datacards

def load_changelog_json():
    # I need to create something like this from saved JSON
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