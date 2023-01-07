"""
Handle, Role
INT, Accounting, Bureaucracy, Business, Composition,
     Conceal/Reveal Object, Criminology, Cryptography, Deduction, 
     Education, Library Search, Local Expert, Perception, Tactics, 
     Tracking
REF, Drive Land Vehicle, Handgun, Shoulder Arms
DEX, Athletics, (Brawling, xd6), Evasion, Melee Weapon, Stealth
TECH, Electronics/Security Tech, First Aid, Forgery, Paramedic, 
      Photography/Film, Pick Lock, Pick Pocket, Play Instrument
COOL, Acting, Bribery, Interrogation, Persuation, Streetwise, Trading,
      Wardrobe & Style
WILL, Concentration, Resist Torture/Drugs
LUCK, MOVE, BODY
EMP, Conversation, Human Perception
HP, seriously_wounded, death_save
Armor, SP
Weapon 1, DMG xd6, Ammo, ROF, Notes
Weapon 2, DMG xd6, Ammo, ROF, Notes
Role Ability
Cyberware 1, Cyberware 2
Gear
Portrait, Notes
"""

characters_sheet = (
    ("Forty", "Rockerboy",
    (5, 0, 0, 0, 6, 0, 0, 0, 0, 2, 0, 4, 2, 0, 0),
    (6, 0, 6, 0),
    (7, 2, (6, 1), 6, 6, 2),
    (5, 0, 6, 0, 0, 0, 0, 0, 6),
    (7, 0, 0, 0, 6, 6, 0, 4),
    (8, 2, 0),
    5, 7, 3,
    (6, 2, 6),
    40, 20, 3,
    ("Light Armorjack", 11),
    ("Very Heavy Pistol", 4, 8, 1, 6),
    ("Heavy Melee Weapon", 3, None, 2, ("Sword", "Baseball Bat")),
    ("Charismatic Impact", 2),
    "Internal Agent", "Paint Editor Chipware",
    ("Musical Instrument", "Pocket Amp", "Glow Paint", "Video Camera"),
    "Ascii Portrait", "Notes"),

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
    ("Light Armorjack", 11),
    ("Heavy Pistol", 3, 8, 2, 16),
    ("Heavy Melee Weapon", 3, None, 2, ("Sword", "Folded Tripod")),
    "Credibility",
    "Internal Agent", "Image Enhance Cybereyes",
    ("Video Camera", "Audio Recorder"),
    "ASCII Portrait", "Notes"))
