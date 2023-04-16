# Change to singleton
import uuid 
import json
from .character import Character 
from pathlib import Path


class CharacterManager:
    def __init__(self):
        self.characters = {}
        self.load_characters()
        self.player = None
        self.npcs = []

    def get_character_by_id(self, character_id: int) -> Character:
        return self.characters.get(character_id)
    
    def set_player(self, character: Character):
        self.player = character

    def set_npcs(self, characters: list[Character]):
        self.npcs = characters
        
    def get_player(self):
        return self.player
    
    def get_npcs(self):
        return self.npcs
    

    def load_characters(self):
        file_path = Path(
            __file__).parent.parent /  'character_assets/characters.json'
        with open(file_path) as f:
            characters_data = json.load(f)
        for char in characters_data:
            char["char_id"] = uuid.uuid4()
            ascii_art_path = (
                Path(__file__).parent.parent / 
                f'character_assets/{char["ascii_art"]}')
            with open(ascii_art_path, 'r') as f:
                char['ascii_art'] = f.read()
            self.characters[char["char_id"]] = Character(**char)

    def roles(self, text=''): 
        return [
            c.role.lower() for c in 
            self.char_mngr.characters.values() if 
            c.role.lower().startswith(text)]

    def do_choose_character(self, arg=None):
        """Allows the player to choose a character role."""
        if arg not in self.roles():
            characters_list = [
                f"{character.handle} ({character.role})" for  character in 
                self.char_mngr.characters.values()]
            self.columnize(characters_list, displaywidth=80)
            print(f"To pick yo' ride chummer, type in {self.roles()}.")
            return
        self.prompt = f"{arg} ᐸ/> "
        self.char_mngr.set_player(
            next(c for c in self.char_mngr.characters.values() if 
                 c.role.lower() == arg))
        self.char_mngr.set_npcs(
            [c for c in self.char_mngr.characters.values() if 
             c.role.lower() != arg])
        self.game_state = 'character_chosen'

    def complete_choose_character(self, text, line, begidx, endidx):
        return self.roles(text)

    def do_player_sheet(self, arg):
        """Displays the character sheet"""
        print(f"HANDLE \033[1;3;35m{self.char_mngr.player.handle:⌁^33}"
              "\033[0m ROLE "
              f"\033[1;3;35m{self.char_mngr.player.role:⌁^33}\033[0m")
        stat_list = [(f'{key:⌁<12}{self.char_mngr.player.lucky_pool}/{value}' 
                      if key == 'luck' else f'{key:⌁<12}{value:>2}')
                     for key, value in self.char_mngr.player.stats.items()]
        self.columnize(stat_list, displaywidth=80)
        combat_list = [(f'{key:⌁<23}{value:>2}')
                        for key, value in self.char_mngr.player.combat.items()]
        self.columnize(combat_list, displaywidth=80)
        skill_keys = list(self.char_mngr.player.skills.keys())
        skill_values = list(self.char_mngr.player.skills.values())
        skill_list = [(f'{key:⌁<30}{value[0]:>2}')
                      for key, value in zip(skill_keys,skill_values)
                      if value[1!=0]]
        skill_list += self.char_mngr.player.ascii_art.splitlines()
        self.columnize(skill_list, displaywidth=80)
        # Display armor & weapons
        defence_list = (
            [f"WEAPONS & ARMOR{'⌁'*19:<10} "] 
            + [' '.join(self.char_mngr.player.defence.keys())] 
            + [' '.join([str(row) for row in 
               self.char_mngr.player.defence.values()])])
        weapons_list = (
            [' '.join(self.char_mngr.player.weapons[0].keys())] 
            + [' '.join([str(val) for val in row.values()]
                        ) for row in self.char_mngr.player.weapons])
        for defence, weapon in zip(defence_list, weapons_list):
            print(defence.ljust(35) + weapon.ljust(45))
        print(f"ROLE ABILITY {'⌁'*14} CYBERWARE {'⌁'*17} GEAR {'⌁'*19}")
        ability_list = list(self.char_mngr.player.role_ability.values())
        ability_list = [row.splitlines() for row in ability_list]
        ability_list = [item for sublist in ability_list for item in sublist]
        ware_list = [
            value for row in self.char_mngr.player.cyberware for key, value in 
            row.items()]
        ware_list = [row.splitlines() for row in ware_list]
        ware_list = [item for sublist in ware_list for item in sublist]
        gear_list = (
            [' '.join(self.char_mngr.player.gear[0].keys())]
            + [' '.join(row.values()) for row in self.char_mngr.player.gear]
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
        print("Cultural Region:", self.char_mngr.player.cultural_region)
        print("Personality:", self.char_mngr.player.personality)
        print("Clothing Style:", self.char_mngr.player.clothing_style)
        print("Hairstyle:", self.char_mngr.player.hairstyle)
        print('Affectation:', self.char_mngr.player.affectation)
        print("Value:", self.char_mngr.player.value)
        print("Trait:", self.char_mngr.player.trait)
        print('Most Valued Person in Your Life:', 
              self.char_mngr.player.valued_person)
        print('Most Valued Possession You Own:', 
              self.char_mngr.player.valued_possession)
        print("Original Background:",
            self.char_mngr.player.original_background)
        print("Childhood Environment:",
            self.char_mngr.player.childhood_environment)
        print("Family Crisis:", self.char_mngr.player.family_crisis)
        print("Friends:", self.char_mngr.player.friends)
        print("Enemies:", self.char_mngr.player.enemies)
        print("Lovers:", self.char_mngr.player.lovers)
        print("Life Goals:", self.char_mngr.player.life_goal)
