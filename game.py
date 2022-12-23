"""A Role Playing Game in the Cyberpunk RED Universe"""
import random
import shelve
import time

# Character stats
stats = {
    "INT":   0, #intelligence
    "REF":   0, #reflexes
    "DEX":   0, #dexterity
    "TECH":  0, #technique
    "COOL":  0, #cool
    "WILL":  0, #will
    "LUCK": 20, #luck
    "MOVE":  0, #movement
    "BODY":  0, #body
    "EMP":   0  #empathy
}

lucky_pool = stats['LUCK']

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
    "Wardrobe & Style":         [0, stats["COOL"]]
}

DIFFICULTY_VALUE = {
    "Everyday": 13,
    "Difficult": 15,
    "Professional": 17,
    "Heroic": 21,
    "Incredible": 24
}

def skill_check(skill_name, difficulty_value):
    """
    Attacker vs Defender
    Trying Again:
      only if chances of success have improved
      - you took longer
      - used better tool
      - you or friends made Complementary Skill Check
    Complementary Skill Check
      Single +1 bonus for subsequent similar skill
    Taking Extra Time
      Single +1 bonus when taking four times longer
    """
    global lucky_pool
    # Get the skill level and stat value for the specified skill
    skill_level, stat_value = skills[skill_name]
    # Generate a random number from 1 to 10
    d10_roll = random.randint(1, 10)
    # Add d10 roll to total skill level
    total_skill_level = skill_level + stat_value + d10_roll
    if d10_roll == 10:
        print("Critical Success! Rolling another one")
        # Generate another random number from 1 to 10
        total_skill_level += random.randint(1,10)
    elif d10_roll == 1:
        print("Critical Failure! Rolling another one")
        # Generate another random number from 1 to 10
        total_skill_level -= random.randint(1,10)
    # Prompt the player to enter the number
    # of lucky points they want to spend
    lucky_points = input("How many Lucky points)")
    # Convert the input to an integer
    lucky_points = int(lucky_points)
    # Add lucky points to total skill level
    total_skill_level += lucky_points
    # Deduct lucky points from lucky pool
    lucky_pool -= lucky_points

    # Get the DV for the specified difficulty level
    d_v = DIFFICULTY_VALUE[difficulty_value]
    if total_skill_level > d_v:
        print(f"Success! Attacker roll: {total_skill_level}, Defender DV: {d_v}")
    elif total_skill_level < d_v:
        print(f"Failure! Attacker roll: {total_skill_level}, Defender DV: {d_v}")
    else:
        print(f"Tie! Attacker roll: {total_skill_level}, Defender DV: {d_v}")
        print("Attacker loses.")

for skill, skill_info in skills.items():
    print(f"{skill:<25} {sum(skill_info):>2}")
# Open the database, creating it if it doesn't already exist
with shelve.open('timestamp', 'c') as db:
    # Save data to the database
    db['timestamp'] = time.time()
# The database is automatically closed and saved when the `with` block is exited

skill_check("Acting", "Professional")
# Open a shelve in read mode
with shelve.open('timestamp', 'r') as db:
    # Load the timestamp
    timestamp = db['timestamp']
print(timestamp)
print(f"Lucky Pool: {lucky_pool}")
