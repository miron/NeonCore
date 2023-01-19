"""A Role Playing Game in the Cyberpunk RED Universe"""

import cmd
import os
import sys
import shelve
import time
from character import Character
from sheet import characters
import map 
import textwrap 

def wprint(text, width=80):
    wrapped_text = textwrap.wrap(text, width=width)
    for line in wrapped_text:
        print(line)


class ActionManager(cmd.Cmd):
    """cli, displays character stats/skills, quits the game"""
    intro = r"""     ᐸ ソ ╱> /Ξ /≥ /> // /𐑘/ /ᐸ
                      ‾
   …   ˛⁄⁔      ˛⁔     ⁔   _  ¸¸
  (˙}  \(∞l   ,, {˚)/ ¸{=}˛ |\\(˚}
 /(\)╲  `••\˛_ \/(⎔◊𐑘 (\+/)  \∏(p)]
 \ᢘ╦╤═÷- Y¸∆     ¸U˛   \Ξ˛\   ´¸v˛|
  7˘ 𐑘 ¸⁄∫𐑘      [][]   7 𐑘 `   [ ]´
  ]  ]  / |      [ [   ]  ]    { }
  l  L ∫  l      ɺ[ɺ]  l  L    ɺ L 
    ⌁help⌁   give me the 411
"""
    prompt = 'ᐸ/> '
    ruler = '⌁'
    doc_header = "Recorded jive (type help <jargon>):"

    def __init__(self, characters_list):
        super().__init__()
        self.characters_list = characters_list
        self.player = None
        self.npcs = None
        self.game_state = None

    def do_shell(self, arg):
        """ Shell commands can be added here prefixed with !"""
        os.system('clear')

   # def postcmd(self, stop, line):
   #    # Get the number of rows in the output
   #    rows, _ = os.popen('stty size', 'r').read().split()
   #    # Move the cursor to the correct position
   #    print(f'\033[{int(rows)}H')
   #    return stop

   # def postcmd(self, stop, line):
   #     # Get the size of the terminal window
   #     rows, cols = self.stdscr.getmaxyx()
   #     # Move the cursor to the 24th row (0-indexed)
   #     self.stdscr.move(24, 0)
   #     # Refresh the terminal window
   #     self.stdscr.refresh()
   #     return cmd.Cmd.postcmd(self, stop, line)

    def default(self, line):
        print("WTF dat mean, ain't no command like dat")

    def do_quit(self, arg):
        """Exits Cyberpunk RED"""
        wprint("Catch you on the flip side, choombatta. Keep your chrome "
               "polished and your guns loaded, "
               "the neon jungle ain't no walk in the park.")
        # Open database, create if it doesn't already exist
        with shelve.open('timestamp') as dbase:
            # Save data to the database>
            dbase['timestamp'] = time.time()
        sys.exit()

    def do_choose_character(self, arg):
        """Allows the player to choose a character role."""
        self.prompt = ("Pick yo' ride, rockerboy, solo, tech, medtech, "
                       "or media:")
        characters_list = [
            f"{character.handle} ({character.role})" 
            for i, character in enumerate(self.characters_list)
            ]
        self.columnize(characters_list, displaywidth=80)
        valid_roles = ['rockerboy', 'solo', 'tech', 'medtech', 'media']
        if arg in valid_roles:
            self.character_role = arg
            self.prompt = f"{arg} >>> "
        else:
            print(f"Invalid role. Valid roles: {valid_roles}")

    def choose_character(self):
        while True:
            print("Yo, roll a homie, chummer:")
            characters_list = [
                f"{i+1}. {character.handle}"
                for i, character in enumerate(self.characters_list)
                ]
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
            print("Invalid choice. Please choose a number between 1 and",
                  len(characters_list))

    def do_move(self, args):
        """Move player in the specified direction"""
        map.main(self.player, self.npcs)

    def do_player_sheet(self, arg):
        """Displays the character sheet"""
        print(f"HANDLE \033[1;3;35m{self.player.handle:⌁^33}\033[0m ROLE "
              f"\033[1;3;35m{self.player.role:⌁^33}\033[0m")
        stat_list = [(f'{key:⌁<12}{self.player.lucky_pool}/{value}' 
                      if key == 'luck' else f'{key:⌁<12}{value:>2}')
                     for key, value in self.player.stats.items()]
        self.columnize(stat_list, displaywidth=80)
        combat_list = [(f'{key:⌁<23}{value:>2}')
                        for key, value in self.player.combat.items()]
        self.columnize(combat_list, displaywidth=80)
        skill_keys = list(self.player.skills.keys())
        skill_values = list(self.player.skills.values())
        skill_list = [(f'{key:⌁<30}{value[0]:>2}')
                      for key, value in zip(skill_keys,skill_values)
                      if value[1!=0]]
        skill_list += self.player.ascii_art.splitlines()
        self.columnize(skill_list, displaywidth=80)
        # Display armor & weapons
        defence_list = (
            [f"WEAPONS & ARMOR{'⌁'*19:<10} "] 
            + [' '.join(self.player.defence.keys())] 
            + [' '.join([str(row) for row in 
               self.player.defence.values()])])
        weapons_list = (
            [' '.join(self.player.weapons[0].keys())] 
            + [' '.join([str(val) for val in row.values()]
                        ) for row in self.player.weapons])
        for defence, weapon in zip(defence_list, weapons_list):
            print(defence.ljust(35) + weapon.ljust(45))
        print("ROLE ABILITY " + "⌁"*14 + " CYBERWARE " + "⌁"*17 + " GEAR "
              + "⌁"*19)
        ability_list = list(self.player.role_ability.values())
        ability_list = [row.splitlines() for row in ability_list]
        ability_list = [item for sublist in ability_list for item in sublist]
        ware_list = [value for row in self.player.cyberware for key, value in 
                     row.items()]
        ware_list = [row.splitlines() for row in ware_list]
        ware_list = [item for sublist in ware_list for item in sublist]
        gear_list = ([' '.join(self.player.gear[0].keys())]
                     + [' '.join(row.values()) for row in self.player.gear]
                     + [''])
        for ability, ware, gear in zip(ability_list, ware_list, gear_list):
            #if ability == ability_list[0]:
            #    ability = "\033[1m" + ability + "\033[0m"
            #if ware == ware_list[0]:
            #    ware = "\033[1m" + ware + "\033[0m"
            #if gear == gear_list[0]:
            #    gear = "\033[1m" + gear + "\033[0m"
            print(ability.ljust(28) + ware.ljust(28) + gear.ljust(24))

    def do_rap_sheet(self, arg):
        """Yo, dis here's rap_sheet, it's gonna show ya all the deetz on
ya character's backstory, where they came from, who they know, and what
they're all about.
It's like peepin' into they mind, know what I'm sayin'? Gotta know ya 
homies before ya start runnin' with em, ya feel me?
"""
        print("Lifepath:")
        print("Cultural Region:", self.player.cultural_region)
        print("Personality:", self.player.personality)
        print("Clothing Style:", self.player.clothing_style)
        print("Hairstyle:", self.player.hairstyle)
        print("Value:", self.player.value)
        print("Trait:", self.player.trait)
        print("Original Background:", self.player.original_background)
        print("Childhood Environment:", self.player.childhood_environment)
        print("Family Crisis:", self.player.family_crisis)
        print("Friends:", self.player.friends)
        print("Enemies:", self.player.enemies)
        print("Lovers:", self.player.lovers)
        print("Life Goals:", self.player.life_goal)

    def do_jack_in(self, args):
        """Yo, chummer! You wanna make some eddies and climb the ranks? 
You wanna be a player in Night City? Type 'jack_in' and let's get this 
show on the road. Gotta choose your character first, make sure you roll 
'em up tight and make the right choice. Remember, in Night City, you 
gotta be quick on your feet and make the right moves, or you'll end up 
as another memory on the streets. So, you in or what?
"""
        self.character = self.choose_character()
        wprint("Yo, listen up. You and your crew just hit the South Night City"
               " docks and now you're chillin' with a burner phone call from "
               "Lazlo, your fixer.")
        wprint("He's all like, 'Yo, we gotta change the spot for the payout. "
               "Meet me at the industrial park in Heywood.")
        wprint("But something ain't right, 'cause Lazlo ain't telling you why."
               " He's just saying it's all good, but you can tell "
               "he's sweatin'.")
        print("You got a bad feeling about this. Like, real bad.")
        self.game_state = 'before_perception_check'
        self.prompt = "ε(๏_๏)з】 "

    def completenames(self, text, *ignored):
        cmds = super().completenames(text, *ignored)
        check_cmd = self.get_check_command()
        if check_cmd:
            cmds = check_cmd.completenames(text)
        return cmds
        #if self.game_state == 'before_perception_check':
        #    cmds = [cmd for cmd in cmds if cmd in ['perception_check']]
        #return cmds

    def get_check_command(self):
        if self.game_state == 'before_perception_check':
            return PerceptionCheckCommand(...)
        elif self.game_state == 'before_ranged_combat':
            return RangedCombatCommand(...)


    def do_heywood_industrial(self):
        """This method handles the Heywood Industrial story mode."""
        wprint("You arrive at Heywood Industrial. "
               "How do you want to approach the situation?")
        approach = input("Enter your choice: ")
        # Check if the player's approach includes a skill check of 17 or higher
        if self.character.skill_check(17):
            print("Your approach leads to a beneficial situation!")
            # Adjudicate the beneficial situation
            self.beneficial_situation()
        else:
            wprint("Your approach does not lead to a beneficial situation."
                   "At the center of some alleys is a hooded man handcuffed to"
                   " a briefcase. He offers it to you, but fumbles with the "
                   "key before handing it over.")
        choice = input("Do you take the briefcase? (yes/no) ")
        if choice == "yes":
            print("You take the briefcase.")
            character = self.choose_character()
            # Check if the briefcase contains counterfeit money
            if character.forgery_check(17):
                print("The briefcase contains 10,000eb, but it's counterfeit.")
            else:
                print("The briefcase contains 10,000eb.")
            # Trigger the ambush
            self.ambush()
        else:
            print("You don't take the briefcase.")
            # Continues the story without trigger the ambush
            self.continue_story()


# Open a shelve in read mode
#with shelve.open('timestamp', 'r') as db:
    # Load the timestamp
    #timestamp = dbase['timestamp']
#print(timestamp)


if __name__ == "__main__":
    characters_list = [Character(**char) for char in characters]
    os.system('clear')
    ActionManager(characters_list).cmdloop()
   # instances = locals().copy()
   # for name, value in instances.items():
   #     if isinstance(value, Character):
   #         print(name)
