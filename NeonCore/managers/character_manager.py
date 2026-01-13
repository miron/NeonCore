# Change to singleton
import json
import uuid
from pathlib import Path
import logging


from .character import Character
from .trait_manager import TraitManager
from ..utils import DiceRoller, wprint
import textwrap
from itertools import zip_longest


class CharacterManager:
    def __init__(self):
        self.trait_manager = TraitManager()
        self.characters = {}
        self.npcs = []
        self.load_characters()
        self.player = None

    def get_character_by_id(self, character_id: int) -> Character:
        return self.characters.get(character_id)

    def set_player(self, character: Character):
        self.player = character

    def set_npcs(self, characters: list[Character]):
        self.npcs = characters

    def get_npc(self, handle: str) -> Character:
        for npc in self.npcs:
            if npc.handle.lower() == handle.lower():
                return npc
        return None

    def load_characters(self):
        # Load Playable Characters
        char_path = Path(__file__).parent.parent / "character_assets/characters.json"
        
        # Load NPCs
        npc_path = Path(__file__).parent.parent / "character_assets/npcs.json"


        with open(char_path) as f:
            characters_data = json.load(f)
        
        # Helper to process character data list into Character objects
        def process_chars(data_list, target_dict=None, target_list=None):
            for char in data_list:
                char["char_id"] = uuid.uuid4()
                # Check if Ascii art exists, otherwise placeholder or skip
                # Assuming ascii art files for NPCs exist or are managed similarly
                if "ascii_art" in char:
                   ascii_path = (
                       Path(__file__).parent.parent / f'character_assets/{char["ascii_art"]}'
                   )
                   if ascii_path.exists():
                       with open(ascii_path, "r", encoding="utf-8") as f:
                            char["ascii_art"] = f.read()
                   else:
                       char["ascii_art"] = "No Art"
                
                soul = self.trait_manager.generate_random_soul()
                character_obj = Character(**char, digital_soul=soul)
                
                if target_dict is not None:
                    target_dict[character_obj.char_id] = character_obj
                
                if target_list is not None:
                    target_list.append(character_obj)

        process_chars(characters_data, target_dict=self.characters)

        if npc_path.exists():
            with open(npc_path) as f:
                npcs_data = json.load(f)
            process_chars(npcs_data, target_list=self.npcs)


    def roles(self, text=""):
        """Return list of available character roles"""
        text_lower = text.lower()  # Hoist method call outside loop
        roles = [
            c.role.lower()
            for c in self.characters.values()
            if c.role.lower().startswith(text_lower)
        ]
        logging.debug(f"Available roles: {roles}")
        return roles

    def character_names(self, text=""):
        """Return list of available character handles with roles"""
        text_lower = text.lower()
        # Return format: "Handle (Role)"
        names = [
            f"{c.handle} ({c.role})"
            for c in self.characters.values()
            if c.handle.lower().startswith(text_lower)
        ]
        return names

    def get_character_sheet_data(self, character=None):
        """Prepares raw character sheet data for rendering"""
        from copy import deepcopy
        
        target = character if character else self.player
        if not target:
            return {}
            
        # Calculate Brawling Damage
        body = target.stats.get('body', 5)
        if body <= 4: dice = 1
        elif body <= 6: dice = 2
        elif body <= 10: dice = 3
        else: dice = 4
        
        brawling_entry = {
            "name": "Brawling",
            "dmg": f"{dice}d6",
            "ammo": "-",
            "rof": 2,
            "notes": "Unarmed"
        }
        
        # Deep copy weapons to avoid mutating the actual character object when adding Brawling
        weapons_list = deepcopy(target.weapons)
        weapons_list.insert(0, brawling_entry)

        display_ability = {}
        if target.role_ability:
             # handle case where it might be a dict or object
             if hasattr(target.role_ability, "get_display_data"):
                 data = target.role_ability.get_display_data()
                 display_ability = {"name": data.name, "notes": data.description}
             elif isinstance(target.role_ability, dict):
                 display_ability = target.role_ability
        
        return {
            "handle": target.handle,
            "role": target.role,
            "stats": target.stats,
            "combat": target.combat,
            "skills": target.skills,
            "ascii_art": target.ascii_art,
            "defence": target.defence,
            "weapons": weapons_list,
            "role_ability": display_ability,
            "cyberware": target.cyberware,
            "inventory": target.inventory
        }

    def do_rap_sheet(self, arg):
        """Yo, dis here's rap_sheet, it's gonna show ya all the deetz on
        ya character's backstory, where they came from, who they know, and what
        they're all about.
        It's like peepin' into they mind, know what I'm sayin'? Gotta know ya
        homies before ya start runnin' with em, ya feel me?"""
        rap_sheet = f"""Lifepath:
Cultural Region: {self.player.cultural_region}
Personality: {self.player.personality}
Clothing Style: {self.player.clothing_style}
Hairstyle: {self.player.hairstyle}
Affectation: {self.player.affectation}
Value: {self.player.value}
Trait: {self.player.trait}
Most Valued Person in Your Life: {self.player.valued_person}
Most Valued Possession You Own: {self.player.valued_possession}
Original Background: {self.player.original_background}
Childhood Environment: {self.player.childhood_environment}
Family Crisis: {self.player.family_crisis}
Friends: {self.player.friends}
Enemies: {self.player.enemies}
Lovers: {self.player.lovers}
Life Goals: {self.player.life_goal}"""
        return rap_sheet
