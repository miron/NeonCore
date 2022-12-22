import random

# Character stats
stats = {
    "INT": 0,  #intelligence
    "REF": 0,  #reflexes
    "DEX": 0,  #dexterity
    "TECH": 0, #technique
    "COOL": 0, #cool
    "WILL": 0, #will
    "LUCK": 0, #luck
    "MOVE": 0, #movement
    "BODY": 0, #body
    "EMP": 0   #empathy
}

# Character skills
skills = {
    "Accounting":               [0, stats["INT"]],
    "Acting":                   [0, stats["COOL"]],
    "Athletics":                [0, stats["DEX"]],
    "Brawling":                 [0, stats["DEX"]],
    "Bribery":                  [0, stats["COOL"]],
    "Bureaucracy":              [0, stats["INT"]],
    "Business":                 [0, stats["INT"]],
    "Composition":              [0, stats["INT"]],
    "Conceal/Reveal Object":    [0, stats["INT"]],
    "Concentration":            [0, stats["WILL"]],
    "Conversation":             [0, stats["EMP"]],
    "Criminology":              [0, stats["INT"]],
    "Cryptography":             [0, stats["INT"]],
    "Deduction":                [0, stats["INT"]],
    "Drive Land Vehicle":       [0, stats["REF"]],
    "Education":                [0, stats["INT"]],
    "Electronics/Security Tech":[0, stats["TECH"]],
    "Evasion":                  [0, stats["DEX"]],
    "First Aid":                [0, stats["TECH"]],
    "Forgery":                  [0, stats["TECH"]],
    "Handgun":                  [0, stats["REF"]],
    "Human Perception":         [0, stats["EMP"]],
    "Interrogation":            [0, stats["COOL"]],
    "Library Search":           [0, stats["INT"]],
    "Local Expert":             [0, stats["INT"]],
    "Melee Weapon":             [0, stats["DEX"]],
    "Paramedic":                [0, stats["TECH"]],
    "Perception":               [0, stats["INT"]],
    "Persuation":               [0, stats["COOL"]],
    "Photography/Film":         [0, stats["TECH"]],
    "Pick Lock":                [0, stats["TECH"]],
    "Pick Pocket":              [0, stats["TECH"]],
    "Play Instrument":          [0, stats["TECH"]],
    "Resist Torture/Drugs":     [0, stats["WILL"]],
    "Shoulder Arms":            [0, stats["REF"]],
    "Stealth":                  [0, stats["DEX"]],
    "Streetwise":               [0, stats["COOL"]],
    "Tactics":                  [0, stats["INT"]],
    "Tracking":                 [0, stats["INT"]],
    "Trading":                  [0, stats["COOL"]],
    "Wardrobe & Style":           [0, stats["COOL"]]
}

for skill, skill_info in skills.items():
    skill_level, stat_value = skill_info
    # Generate a random number from 1 to 10
    d10_roll = random.randint(1, 10)
    # Add d10 roll to total skill level
    # in case of a tie, the Defender always wins
    print(f"{skill:<25} {skill_level+stat_value+d10_roll:>2}")
