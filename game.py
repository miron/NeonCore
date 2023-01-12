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
    prompt = 'ᐸ/> '

    def __init__(self, characters_list):
        self.characters_list = characters_list
        self.player = None
        self.npcs = None

        # Call the __init__ method of the cmd.Cmd
        super().__init__()

    def do_quit(self, arg):
        """Exits Cyberpunk RED"""
        print("""
        Catch you on the flip side, choombatta.
        Keep your chrome polished and your guns loaded,
        the neon jungle ain't no walk in the park.""")
        # Open database, create if it doesn't already exist
        with shelve.open('timestamp') as dbase:
            # Save data to the database>
            dbase['timestamp'] = time.time()
        sys.exit()

    def choose_character(self):
        while True:
            print("Select a character:")
            characters_list = [f"{i+1}. {character.handle}" for i, character in enumerate(self.characters_list)]
            self.columnize(characters_list, displaywidth=80)
            choice = input("Enter the number of your choice or 'q' to quit: ")
            if choice.lower() == 'q':
                break
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(characters_list):
                    self.player = self.characters_list.pop(choice)
                    #character_summary(self.player)
                    self.npcs = self.characters_list
                    confirm = input("Confirm? y/n: ")
                    if confirm.lower() == 'y':
                        break
            except ValueError:
                pass
            print("Invalid choice. Please choose a number between 1 and", len(characters_list))

    def do_choose_character(self, arg):
        """Prompts the player to choose a character and assigns the selected character to self.character"""
        self.character = self.choose_character()
        self.skill_check = SkillCheck(self.player)

    def spawn_npcs(self, area):
        """Randomly spawn NPCs in the specified area"""
        # Determine the number of NPCs to spawn
        num_npcs = random.randint(1, 5)
        for i in range(num_npcs):
            x, y = random.randint(1, area.width), random.randint(1, area.height)
            if area.grid[x][y] == ".":
                npc = self.npcs[random.randint(0, len(self.npcs)-1)]
                area.grid[x][y] = npc
                self.npcs.remove(npc)

    def do_move(self, args):
        """Move player in the specified direction"""
        x, y = self.player.x, self.player.y
        if args.lower() == 'up':
            y -= 1
        elif args.lower() == 'down':
            y += 1
        elif args.lower() == 'left':
            x -= 1
        elif args.lower() == 'right':
            x += 1
        # Check if the player can move in the specified direction
        if (1 <= x <= self.area.width and 1 <= y <= self.area.height and
                self.area.grid[x][y] != "#"):
            # Update player's position
            self.area.grid[self.player.x][self.player.y] = "."
            self.player.x, self.player.y = x, y
            self.area.grid[x][y] = self.player
            if type(self.area.grid[x][y]) == Character: # npc encountered 
                self.current_npc = self.area.grid[x][y]
                self.skill_check = SkillCheck(self.current_npc)
            print(self.area)
        else:
            print("Can't move in that direction")

    def do_encounter_npc(self, arg):
        """Encounter an NPC and assign the selected NPC to self.current_npc"""
        print("Select an NPC:")
        for i, npc in enumerate(self.npcs):
            print(f"{i+1}. {npc.handle}")
        while True:
            try:
                npc_index = int(input()) - 1
                if 0 <= npc_index < len(self.npcs):
                    self.current_npc = self.npcs[npc_index]
                    self.skill_check = SkillCheck(self.current_npc)
                    return
            except ValueError:
                pass
            print("Invalid choice. Please choose a number between 0 and", len(self.npcs)-1)
    
    def do_player_sheet(self, arg):
        """Displays the character sheet"""
        print(f'HANDLE {self.player.handle} ROLE {self.player.role}')
        # Display stats
        stat_list = [(f'{key:.<10}{value:>2}')
                        for key, value in self.player.stats.items()]
        self.columnize(stat_list, displaywidth=80)
        # Display combat
        combat_list = [(f'{key:.<20}{value:>2}')
                        for key, value in self.player.combat.items()]
        self.columnize(combat_list, displaywidth=80)
        print('SKILLS  ' + '/' * 72)
        skill_keys = list(self.player.skills.keys())
        skill_values = list(self.player.skills.values())
        skill_list = [(f'{key:.<26}{value[0]:>2}')
                        for key, value in zip(skill_keys,skill_values) if value[1!=0]]
        
        self.columnize(skill_list, displaywidth=80)
        # Display armor & weapons
        print("WEAPONS & ARMOR  //")
        for key, value in zip(self.player.defence.keys(), self.player.defence.values()):
                print(key, value)
        weapons_list = [' '.join(self.player.weapons[0].keys())] + [' '.join(str(row.values())) for row in self.player.weapons]
        self.columnize(weapons_list, displaywidth=80)
        print("ROLE ABILITY  " + "/" * 24 + "  CYBERWARE  " + "/" * 24 + "  GEAR")
        for key, value in self.player.role_ability.items():
            print(f'{key:.<26}{value}')
        ware_list = [(f'{ware["name"]:.<20}{ware["notes"]}')
                        for ware in self.player.cyberware]
        self.columnize(ware_list, displaywidth=40)
        gear_list = [' '.join(self.player.gear[0].keys())] + [' '.join(row.values()) for row in self.player.gear]
        #gear_list = [(f'{item["name"]:.<20} {item["notes"]:>20}')
                        #for item in self.player.gear]
        self.columnize(gear_list, displaywidth=40)
        # Display ascii_art
        print(self.player.ascii_art)



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
