# Change to singleton
import uuid 
from typing import List, Dict, Any
import json
from .character import Character
from pathlib import Path

class CharacterManager:
    def __init__(self):
        self.characters = {}
        self.load_characters()
        #for character in characters_list:
        #    character["char_id"] = uuid.uuid4()
        #self.characters = {char["char_id"]: Character(**char) for char in 
        #          characters_list}
    def get_character_by_id(self, character_id: int) -> Character:
        return self.characters.get(character_id)
        
    def add_character(self, character: dict):
        self.characters_list.append(Character(**character))

    def get_characters_list(self):
        return self.characters_list
    
    def get_npc_characters(self):
        return [character for character in self.characters_list if not 
            character.is_player]
    
    def get_player_character(self):
        return next(character for character in self.characters_list if 
            character.is_player)

    def load_characters(self):
        file_path = Path(
            __file__).parent.parent /  'character_assets/characters.json'
        with open(file_path) as f:
            characters_data = json.load(f)
        for char in characters_data:
            char["char_id"] = uuid.uuid4()
            self.characters[char["char_id"]] = Character(**char)

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
            print(ability.ljust(28) + ware.ljust(28) + gear.ljust(24))
            #if ability == ability_list[0]:
            #    ability = "\033[1m" + ability + "\033[0m"
            #if ware == ware_list[0]:
            #    ware = "\033[1m" + ware + "\033[0m"
            #if gear == gear_list[0]:
            #    gear = "\033[1m" + gear + "\033[0m"

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



