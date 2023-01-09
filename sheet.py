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
            "accounting": [5, 0],
            "acting": [7, 0],
            "athletics": [7, 2],
            "brawling": [7, 6, 1],
            "bribery": [7, 0],
            "bureaucracy": [5, 0],
            "business": [5, 0],
            "composition": [5, 6],
            "conceal_reveal_object": [5, 0],
            "concentration": [8, 2],
            "conversation": [6, 2],
            "criminology": [5, 0],
            "cryptography": [5, 0],
            "deduction": [5, 0],
            "drive_land_vehicle": (6, 0),
            "education": [5, 2],
            "electronics_security_tech": [5, 0],
            "evasion": [7, 6],
            "first_aid": [5, 6],
            "forgery": [5, 0],
            "handgun": [6, 6],
            "human_perception": [6, 6],
            "interrogation": [7, 0],
            "library_search": [5, 0],
            "local_expert": [5, 4],
            "melee_weapon": [7, 6],
            "paramedic": [5, 0],
            "perception": [5, 2],
            "persuation": [7, 6],
            "photography_film": [5, 0],
            "pick_lock": [5, 0],
            "pick_pocket": [5, 0],
            "play_instrument": [5, 6],
            "resist_torture_drugs": [8, 0],
            "shoulder_arms": [6, 0],
            "stealth": [7, 2],
            "streetwise": [7, 6],
            "tactics": [5, 0],
            "tracking": [5, 0],
            "trading": [7, 0],
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
                "rof": 2,
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
         ˛⁄_
         \(∞l 
          `••\˛_  
            Y¸∆
          ¸⁄∫\ 
           / |   
          ∫  l """
    },
    {
        "handle": "Mover",
        "role": "Solo",
        "stats": {
            "int": 7,
            "ref": 7,
            "dex": 6,
            "tech": 5,
            "cool": 7,
            "will": 6,
            "luck": 6,
            "move": 7,
            "body": 7,
            "emp": 3
        },
        "combat": {
            "hp": 45,
            "seriously_wounded": 23,
            "death_save": 7
        }, 
        "skills": {
            "accounting": [7, 0],
            "acting": [7, 0],
            "athletics": [6, 2],
            "brawling": [6, 6, 2],
            "bribery": [7, 0],
            "bureaucracy": [7, 0],
            "business": [7, 0],
            "composition": [7, 0],
            "conceal_reveal_object": [7, 8],
            "concentration": [6, 2],
            "conversation": [3, 2],
            "criminology": [7, 0],
            "cryptography": [7, 0],
            "deduction": [7, 0],
            "drive_land_vehicle": (7, 0),
            "education": [7, 2],
            "electronics_security_tech": [5, 0],
            "evasion": [6, 6],
            "first_aid": [5, 6],
            "forgery": [5, 0],
            "handgun": [7, 6],
            "human_perception": [3, 2],
            "interrogation": [7, 6],
            "library_search": [7, 0],
            "local_expert": [7, 2],
            "melee_weapon": [6, 0],
            "paramedic": [5, 0],
            "perception": [7, 8],
            "persuation": [7, 2],
            "photography_film": [5, 0],
            "pick_lock": [5, 0],
            "pick_pocket": [5, 0],
            "play_instrument": [5, 0],
            "resist_torture_drugs": [6, 6],
            "shoulder_arms": [7, 6],
            "stealth": [6, 6],
            "streetwise": [7, 0],
            "tactics": [7, 6],
            "tracking": [7, 0],
            "trading": [7, 0],
            "wardrobe_and_style": [7, 0]
        },
        "armor": {
            "name": "Light Armorjack",
            "sp": 11
        },
        "weapon": [
            {
                "name": "Shotgun",
                "dmg": 5,
                "ammo": 4,
                "rof": 1,
                "notes": 8
            },
            {   "name": "Assault Rifle",
                "dmg": 5,
                "ammo": 25,
                "rof": 1,
                "notes": 25
            }, 
        ],
        "role_ability": {
            "name": "Combat Awarness",
            "notes": "Add +4 to any Initiative roll you make."
        },
        "cyberware": [
            {
                "name": "Image Enhance Cybereyes",
                "notes": """Your eyes are better than human, giving you +2 to Perception and
                 Conceal/Reveal Object Skills (already included above)."""
            },
            {  
                "name": "Teleoptic Cybereye",
                "notes": "You can see detail up to 800 m/yds away."
            }
        ],
        "gear": [
            {   
                "name": "Burner Phone",
                "note": "A disposable phone"
            }
        ],
        "ascii_art": "︻デ┳═ー"
    },
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
            "accounting": [5, 0],
            "acting": [7, 0],
            "athletics": [7, 2],
            "brawling": [7, 6, 1],
            "bribery": [7, 0],
            "bureaucracy": [5, 0],
            "business": [5, 0],
            "composition": [5, 6],
            "conceal_reveal_object": [5, 0],
            "concentration": [8, 2],
            "conversation": [6, 2],
            "criminology": [5, 0],
            "cryptography": [5, 0],
            "deduction": [5, 0],
            "drive_land_vehicle": (6, 0),
            "education": [5, 2],
            "electronics_security_tech": [5, 0],
            "evasion": [7, 6],
            "first_aid": [5, 6],
            "forgery": [5, 0],
            "handgun": [6, 6],
            "human_perception": [6, 6],
            "interrogation": [7, 0],
            "library_search": [5, 0],
            "local_expert": [5, 4],
            "melee_weapon": [7, 6],
            "paramedic": [5, 0],
            "perception": [5, 2],
            "persuation": [7, 6],
            "photography_film": [5, 0],
            "pick_lock": [5, 0],
            "pick_pocket": [5, 0],
            "play_instrument": [5, 6],
            "resist_torture_drugs": [8, 0],
            "shoulder_arms": [6, 0],
            "stealth": [7, 2],
            "streetwise": [7, 6],
            "tactics": [5, 0],
            "tracking": [5, 0],
            "trading": [7, 0],
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
                "rof": 2,
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
]

Media:
"[●▪▪●]" Casette
"[¯ↂ■■ↂ¯]" Casette
'[◉"]' Camera
Solo:
"︻╦̵̵͇̿̿̿̿══╤─

"╾━╤デ╦︻"
"︻┳デ═—"
"▄︻̷̿┻̿═━一"
"▄︻┻═━一"
Medtech:
"|==|iiii|>-----" Needle
"┣▇▇▇═─" Needle
"(:̲̅:̲̅:̲̅[̲̅ ̲̅]̲̅:̲̅:̲̅:̲̅)" Bandaid
Rockerboy:
"{ o }===(:::)" Guitar
"c====(=#O|)" Guitar
"d[o_0]b" Robot 
"<|º감º|>" Robot
"c[○┬●]כ" Robot
Tech: 🔋[👨‍🔧]🔋
Medtech: 💊[👨‍⚕️]💊️  
Rockerboy: 🎸[👨‍🎤]🎸 
Solo:  🦾[🥷]🦾
Media: 📰[👨‍💼]📰