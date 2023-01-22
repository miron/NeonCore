# Change to singleton
import uuid 
from typing import List, Dict, Any
from character import Character


class CharactersManager:
    def __init__(self, characters_list: List[Dict[str, Any]]):
        for character in characters_list:
            character["char_id"] = uuid.uuid4()
        self.characters = {char["char_id"]: Character(**char) for char in 
                  characters_list}
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
        #with open("characters.json") as f:
        #    characters_data - json.load(f)
        characters_data = self.characters 
        for char in characters_data:
            self.characters_list.append(Character(**char))

    def roles(self, text=''):
        return [
            c.role.lower() for c in 
            self.characters.values()] if not text else [
                c.role.lower() for c in 
                self.characters.values()  if 
                c.role.lower().startswith(text)]

    def register_command(self, action_manager):
        setattr(action_manager, 'do_choose_character', 
                self.do_choose_character)
        setattr(action_manager, 'complete_choose_character', 
                self.complete_choose_character)
        setattr(action_manager, 'roles', self.roles)


    def get_available_commands(self):
        return [name[3:] for name in dir(self) if name.startswith("do_")]

    def do_choose_character(self, arg):
        """Allows the player to choose a character role."""
        if arg not in self.roles():
            characters_list = [
                f"{character.handle} ({character.role})" for  character in 
                self.characters.values()]
            self.columnize(characters_list, displaywidth=80)
            wprint(f"To pick yo' ride chummer, type in {self.roles()}.")
            return
        self.prompt = f"{arg} >>> "
        self.player = next(
            c for c in self.characters.values()  if 
            c.role.lower() == arg)
        self.npcs = [
            c for c in self.characters.values() if 
            c.role.lower() != arg]

    def complete_choose_character(self, text, line, begidx, endidx):
        return self.roles(text)

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

