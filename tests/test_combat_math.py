import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NeonCore.managers.character import Character

def test_combat_math():
    print("Initializing Test Characters...")
    
    # Mock data based on characters.json structure
    char_stats = {
        "int": 5, "ref": 6, "dex": 7, "tech": 5, "cool": 7, 
        "will": 8, "luck": 5, "move": 7, "body": 10, "emp": 6
    }
    
    # Skills format: [Stat+Skill, Rank] -> sum is total
    attacker_skills = {
        "brawling": [5, 4], # Total 9
        "evasion": [4, 3]   # Total 7
    }
    
    defender_skills = {
        "brawling": [4, 2], # Total 6
        "evasion": [5, 5]   # Total 10
    }

    attacker = Character(
        char_id="att1", handle="Attacker", role="Solo", stats=char_stats,
        combat={"hp": 20}, skills=attacker_skills, defence={"sp": 5},
        weapons=[], role_ability={}, cyberware=[], gear=[], ascii_art=""
    )

    defender = Character(
        char_id="def1", handle="Defender", role="Solo", stats=char_stats,
        combat={"hp": 20}, skills=defender_skills, defence={"sp": 5}, 
        weapons=[], role_ability={}, cyberware=[], gear=[], ascii_art=""
    )
    
    print("\n--- Testing Skill Check ---")
    # Attacker tries to hit Defender
    # Attacker Brawling (9) vs Defender Evasion (10)
    # Random die rolls will affect this, but we verify method runs and output format
    result = attacker.roll_check(defender, "brawling", "evasion")
    print(f"Check Result: {result}")

    print("\n--- Testing Damage ---")
    print(f"Initial Defender HP: {defender.combat['hp']}")
    
    # Damage < SP (SP is 5)
    print("Applying 4 damage (should be absorbed)...")
    defender.take_damage(4)
    # HP should remain 20
    
    # Damage > SP
    print("Applying 10 damage (should take 5)...")
    defender.take_damage(10)
    # HP should be 15
    
    # Ignore Armor
    print("Applying 10 damage ignoring armor (should take 10)...")
    defender.take_damage(10, ignore_armor=True)
    # HP should be 5
    
    print(f"Final Defender HP: {defender.combat['hp']}")

if __name__ == "__main__":
    test_combat_math()
