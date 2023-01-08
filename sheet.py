characters = [
    {
        "handle": "Forty",
        "role": "Rockerboy",
        "stats": {
            "int": 5,
            "ref": 6,
            "dex": 7,
            "tech": 5,
            "cool": 7,
            "will": 8,
            "luck": 5,
            "move": 7,
            "body": 3,
            "emp": 6
        },
        "combat": {
            "hp": 15,
            "seriously_wounded": 10,
            "death_save": 3
        }, 
        "skills": {
            "accounting": [0, 0],
            "acting": [0, 0],
            "athletics": [7, 2],
            "brawling": [7, 6, 1],
            "bribery": [0, 0],
            "bureaucracy": [0, 0],
            "business": [0, 0],
            "composition": [5, 6],
            "conceal_reveal_object": [0, 0],
            "concentration": [8, 2],
            "conversation": [6, 2],
            "criminology": [0, 0],
            "cryptography": [0, 0],
            "deduction": [0, 0],
            "drive_land_vehicle": (0, 0),
            "education": [5, 2],
            "electronics_security_tech": [0, 0],
            "evasion": [7, 6],
            "first_aid": [5, 6],
            "forgery": [0, 0],
            "handgun": [6, 6],
            "human_perception": [6, 6],
            "interrogation": [0, 0],
            "library_search": [0, 0],
            "local_expert": [5, 4],
            "melee_weapon": [7, 6],
            "paramedic": [0, 0],
            "perception": [5, 2],
            "persuation": [7, 6],
            "photography_film": [0, 0],
            "pick_lock": [0, 0],
            "pick_pocket": [0, 0],
            "play_instrument": [5, 6],
            "resist_torture_drugs": [0, 0],
            "shoulder_arms": [0, 0],
            "stealth": [7, 2],
            "streetwise": [7, 6],
            "tactics": [0, 0],
            "tracking": [0, 0],
            "trading": [0, 0],
            "wardrobe_and_style": [7, 4]
        },
        "armor": {
            "name": "Light Armorjack",
            "sp": 11
        },
        "weapon": [
            {
                "name": "Very Heavy Pistol",
                "dmg": 4,
                "ammo": 8,
                "rof": 1,
                "notes": 16
            },
            {   "name": "Heavy Melee Weapon",
                "dmg": 3,
                "ammo": None,
                "rof": 2
                "notes": "sword/basball bat"
            }, 
        ],
        "role_ability": {
            "name": "Charismatic Impact",
            "notes": """You know when someone is a fan and
            receive a +2 to any EMP or COOL
            based Skill Check made against them,
            including Facedowns."""
        },
        "cyberware": [
            {
                "name": "Internal Agent",
                "notes": """You have a self-adaptive AI-powered Smart Phone in your head, 
                 controlled entirely by voice command"""
            },
            {  
                "name": "Pain Editor Chipware",
                "notes": """You can shut off your pain receptors, ignoring you to ignore the -2 to all
                 Checks granted by the Seriously Wounded Wound State."""
            }
        ],
        "gear": [
            {   
                "name": "Musical Instrument",
                "note": "Player's choice"
            },
            {
                "name": "Pocket Amp",
                "note": "Amplifies musical instrument"
            },
            {
                "name": "Glow Paint",
                "note": "Glow in the dark spraypaint"
            },
            {
                "name": "Video Camera",
                "note": "Records up to 12 hours"
            }
        ],
        "ascii_art": """
                    /\_/\
                   ( o.o )
                     >^<
                     """
    },
    # Add more character dictionaries here
]

    ("Mover", "Solo",
    (7, 0, 0, 0, 0, 8, 0, 0, 0, 2, 0, 2, 8, 6, 0),
    (7, 0, 6, 6),
    (6, 2, (2, 3), 6, 0, 6),
    (5, 0, 6, 0, 0, 0, 0, 0, 0),                         
    (7, 0, 0, 6, 2, 0, 0, 0),
    (6, 2, 6),
    6, 7, 7,
    (3, 2, 2),
    45, 23, 7,
    ("Light Armorjack", 11),
    ("Shotgun", 5, 4, 1, 8),
    ("Assault Rifle", 5, 25, 1, 25),
    "Combat Awareness",
    "Image Enhance Cybereyes", "Teleoptic Cybereye",
    "Burner Phone",
    "Ascii Portrait", "Notes"),
    
    ("Torch", "Tech",
    (8, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 2, 2, 0, 0),
    (7, 0, 6, 6),
    (5, 2, (2, 2), 6, 0, 6),
    (6, 10, 6, 6, 0, 0, 6, 6, 0),
    (3, 0, 0, 0, 2, 0, 0, 0),
    (3, 2, 0),
    7, 6, 6,
    (5, 2, 2),
    35, 18, 6,
    ("Light Armorjack", 11),
    ("Heavy Pistol", 3, 8, 2, 16),
    ("Shotgun", 5, 4, 1, 8),
    "Maker",
    "Tool Hand", "Internal Agent",
    ("Duct Tape", "Flashlight", "Road Flare"),
    "ASCII Portrait", "Notes"),
    
    ("Redtail", "Medtech",
    (8, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 2, 6, 0, 0),
    (5, 0, 0, 6),
    (5, 2, (2, 2), 6, 0, 6),
    (8, 4, 2, 0, 6, 0, 0, 0, 0),
    (5, 0, 0, 0, 5, 0, 0, 0),
    (5, 2, 4),
    6, 6, 5,
    (4, 6, 6),
    35, 18, 5,
    ("Light Armorjack", 11),
    ("Shotgun", 5, 4, 1, 8),
    ("Light Melee Weapon", 1, None, 2, "Small Knife"),
    "Medicine",
    "Tool Hand", "Pain Editor Chipware",
    ("Agent", "Medtech Bag", "Glow Paint", "Flashlight"),
    "ASCII Portrait", "Notes"),
    
    ("24/7", "Media",
    (7, 0, 0, 0, 6, 8, 0, 0, 0, 2, 4, 6, 8, 0, 0),
    (5, 0, 6, 0),
    (5, 2, (2, 2), 6, 6, 6),
    (4, 0, 2, 6, 0, 0, 0, 0, 0),
    (8, 0, 0, 0, 6, 0, 0, 0),
    (7, 2, 0),
    6, 7, 5,
    (7, 6, 6),
    40, 20, 5,
    ("Light Armorjack", 11),
    ("Heavy Pistol", 3, 8, 2, 16),
    ("Heavy Melee Weapon", 3, None, 2, ("Sword", "Folded Tripod")),
    "Credibility",
    "Internal Agent", "Image Enhance Cybereyes",
    ("Video Camera", "Audio Recorder"),
    "ASCII Portrait", "Notes"))
