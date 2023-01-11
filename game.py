"""A Role Playing Game in the Cyberpunk RED Universe"""
import random
import shelve
import time
import cmd
import sys
from character import Character
from sheet import characters

DIFFICULTY_VALUE = {
    "Everyday": 13,
    "Difficult": 15,
    "Professional": 17,
    "Heroic": 21,
    "Incredible": 24
}

class ActionManager(cmd.Cmd):
    """cli, displays character stats/skills, quits the game"""
    intro = """--- RPG Cyberpunk RED Universe ---
    (stats)  View character stats
    (skills) View character skills
    (roll)   Roll skill check
    (help)   Available commands
    (quit)   Exit game"""
    prompt = '(CP) '

    def __init__(self, character):
        self.skill_check = SkillCheck(character)
        self.character = character
        # Call the __init__ method of the cmd.Cmd
        super().__init__()

    def do_quit(self, arg):
        """Exits Cyberpunk RED"""
        print('Thank you for playing')
        # Open database, create if it doesn't already exist
        with shelve.open('timestamp') as dbase:
            # Save data to the database>
            dbase['timestamp'] = time.time()
        sys.exit()

    def do_choose_character(self, arg):
        """Prompts the player to choose a character and assigns the selected character to self.character"""
        self.character = choose_character()

    def choose_character():
        print("Select a character:")
        for i, character in enumerate(characters_list):
            print(f"{i+1}. {character.handle}")

        while True:
            try:
                choice = int(input())
                if 1 <= choice <= len(characters_list):
                    return characters_list[choice-1]
            except ValueError:
                pass
            print("Invalid choice. Please choose a number between 1 and", len(characters_list))

    def do_stats(self, arg):
        """Displays the character's stats."""
        for stat, value in self.character.stats.items():
            print(f"{stat:.<26}{value:>2}")
            
    def do_skills(self, arg):
        """Displays the character's skills."""
        skill_keys = list(self.character.skills.keys())
        skill_values = list(self.character.skills.values())
        print(skill_keys)
        print(skill_values)
        skill_list = [(f'{key:.<26}{value[0]:>2}')
                        for key, value in zip(skill_keys,skill_values)]
        self.columnize(skill_list, displaywidth=80)

    def do_use_luck(self, arg):
        """Spends luck points on a skill check."""
        # parse the input to determine the number of luck points to spend
        luck_points = int(input(f'Use LUCK x/{self.character.lucky_pool}: '))
        if self.skill_check.use_luck(luck_points):
            self.skill_check.perform_check('Acting', 'Professional', luck_points)
        print(f"Lucky Pool: {self.character.lucky_pool}")

class SkillCheck:
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
    
    def __init__(self, character):
        self.character = character

    def use_luck(self, luck_points):
        """
        Spends a specified number of luck points on a skill check.

        Parameters:
        luck_points (int): The number of luck points to spend on the skill check.

        Returns:
        None
        """
        if luck_points > self.character.lucky_pool:
            print("Not enough luck points!")
            return False
        else:
            # subtract the luck points from the lucky pool
            self.character.lucky_pool -= luck_points
            return True

    def perform_check(self, skill_name, difficulty_value, luck_points):
        """
        Perform a skill check using a specified skill and difficulty level.

        Args:
        skill_name (str): The name of the skill to use for the check.
        difficulty_value (str): The difficulty level of the check.
        luck_points (int): The number of luck points to use for the check.

        Returns:
        None
        """

        # Generate a random number from 1 to 10
        d10_roll = random.randint(1, 10)
        # Add d10 roll to total skill level
        skill_check_total = self.character.skill_total(skill_name) + d10_roll + luck_points
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            # Generate another random number from 1 to 10
            skill_check_total += random.randint(1,10)
        elif d10_roll == 1:
            print("Critical Failure! Rolling another one")
            # Generate another random number from 1 to 10
            skill_check_total -= random.randint(1,10)

        # Get the DV for the specified difficulty level
        difficulty_value = DIFFICULTY_VALUE[difficulty_value]
        if skill_check_total > difficulty_value:
            print(f"Success! Attacker roll: {skill_check_total}, Defender DV: {difficulty_value}")
        elif skill_check_total < difficulty_value:
            print(f"Failure! Attacker roll: {skill_check_total}, Defender DV: {difficulty_value}")
        else:
            print(f"Tie! Attacker roll: {skill_check_total}, Defender DV: {difficulty_value}")
            print("Attacker loses.")


# Open a shelve in read mode
#with shelve.open('timestamp', 'r') as db:
    # Load the timestamp
    #timestamp = dbase['timestamp']
#print(timestamp)

if __name__ == "__main__":
    characters_list = [Character(**char) for char in characters]
    ActionManager(characters_list).cmdloop()
   # instances = locals().copy()
   # for name, value in instances.items():
   #     if isinstance(value, Character):
   #         print(name)
