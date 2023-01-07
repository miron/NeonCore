characters_sheet = {
    "Forty": (                  # Handle  
    "Rockerboy",                # Role
 
    (5,                         # INT
    0,                          # Accounting
    0,                          # Bureaucracy
    0,                          # Business
    6,                          # Composition
    0,                          # Conceal/Reveal Object
    0,                          # Criminology
    0,                          # Cryptography
    0,                          # Deduction
    2,                          # Education
    0,                          # Library Search
    4,                          # Local Expert
    2,                          # Perception
    0,                          # Tactics
    0),                         # Tracking

    (6,                         # REF
    0,                          # Drive Land Vehicle
    6,                          # Handgun
    0),                         # Shoulder Arms

    (7,                         # DEX
    2,                          # Athletics
    (6, 1),                     # Brawling, 1d6
    6,                          # Evasion
    6,                          # Melee Weapon
    2),                         # Stealth

    (5,                         # TECH
    0,                          # Electronics/Security Tech
    6,                          # First Aid
    0,                          # Forgery
    0,                          # Paramedic
    0,                          # Photography/Film
    0,                          # Pick Lock
    0,                          # Pick Pocket
    6),                         # Play Instrument

    (7,                         # COOL
    0,                          # Acting
    0,                          # Bribery
    0,                          # Interrogation
    6,                          # Persuation
    6,                          # Streetwise
    0,                          # Trading
    4),                         # Wardrobe & Style

    (8,                         # WILL
    2,                          # Concentration
    0),                         # Resist Torture/Drugs

    5,                          # LUCK
    7,                          # MOVE
    3,                          # BODY

    (6,                         # EMP
    2,                          # Conversation
    6),                         # Human Perception

    40,                         # HP
    20,                         # seriously_wounded
    3,                          # death_save

    ("Light Armorjack", 11),    # Armor, SP

    ("Very Heavy Pistol",       # Weapon 1
    4,                          # DMG 4d6
    8,                          # Ammo
    1,                          # ROF
    16),                        # extra ammo 
    
    ("Heavy Melee Weapon",      # Weapon 2
    3,                          # DMG 3d6
    None,                       # Ammo
    2,                          # ROF
    ("Sword", "Baseball Bat")), # 1 Melee Weapon
    ("Charismatic Impact", 2),  # Role Ability, EMP/COOL 
    "Internal Agent",           # Cyberware 1
    "Paint Editor Chipware",    # Cyberware 2
    (("Guitar", "Synthesizer", 
    "Sampler", "Sequencer"),
    "Pocket Amp", "Glow Paint",
    "Video Camera"),            # Gear
    "Ascii Portrait",           # Portrait 
    "Notes"                     # Notes
    ),

    "Mover": (                  # Handle  
    "Solo",                     # Role

    (7,                         # INT
    0,                          # Accounting
    0,                          # Bureaucracy
    0,                          # Business
    0,                          # Composition
    8,                          # Conceal/Reveal Object
    0,                          # Criminology
    0,                          # Cryptography
    0,                          # Deduction
    2,                          # Education
    0,                          # Library Search
    2,                          # Local Expert
    8,                          # Perception
    6,                          # Tactics
    0),                         # Tracking

    (7,                         # REF
    0,                          # Drive Land Vehicle
    6,                          # Handgun
    6),                         # Shoulder Arms

    (6,                         # DEX
    2,                          # Athletics
    (2, 3),                      # Brawling, 3d6
    6,                          # Evasion
    0,                          # Melee Weapon
    6),                         # Stealth

    (5,                         # TECH
    0,                          # Electronics/Security Tech
    6,                          # First Aid
    0,                          # Forgery
    0,                          # Paramedic
    0,                          # Photography/Film
    0,                          # Pick Lock
    0,                          # Pick Pocket
    0),                         # Play Instrument

    (7,                         # COOL
    0,                          # Acting
    0,                          # Bribery
    6,                          # Interrogation
    2,                          # Persuation
    0,                          # Streetwise
    0,                          # Trading
    0),                         # Wardrobe & Style

    (6,                         # WILL
    2,                          # Concentration
    6),                         # Resist Torture/Drugs

    6,                          # LUCK
    7,                          # MOVE
    7,                          # BODY

    (3,                         # EMP
    2,                          # Conversation
    2),                         # Human Perception

    45,                         # HP
    23,                         # seriously_wounded
    7,                          # death_save

    ("Light Armorjack", 11),    # Armor, SP
    ("Shotgun",                 # Weapon 1
    5,                          # DMG 5d6
    4,                          # Ammo
    1,                          # ROF
    8),                         # extra ammo
    ("Assault Rifle",           # Weapon 2
    5,                          # DMG 5d6
    25,                         # Ammo
    1,                          # ROF
    25),                        # extra ammo
    "Combat Awareness",         # Role Ability
    "Image Enhance Cybereyes",  # Cyberware 1
    "Teleoptic Cybereye",       # Cyberware 2
    "Burner Phone",             # Gear
    "Ascii Portrait",           # Portrait 
    "Notes")                                  # Notes
}
