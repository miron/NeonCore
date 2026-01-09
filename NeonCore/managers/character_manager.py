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

    def get_player_sheet_data(self):
        """Prepares character sheet data without formatting"""
        header = (
            f"HANDLE \033[1;3;35m{self.player.handle:^33}"
            "\033[0m ROLE "
            f"\033[1;3;35m{self.player.role:^33}\033[0m"
        )
        stat_list = [
            (
                f"{key:<12}{self.player.lucky_pool}/{value}"
                if key == "luck"
                else f"{key:<12}{value:>2}"
            )
            for key, value in self.player.stats.items()
        ]
        combat_list = [
            (f"{key:<23}{value:>2}") for key, value in self.player.combat.items()
        ]
        skill_keys = list(self.player.skills.keys())
        skill_values = list(self.player.skills.values())
        skill_list_raw = [
            (f"{key:<25} {value['lvl']:>2}")
            for key, value in zip(skill_keys, skill_values)
            if value.get('lvl', 0) != 0
        ]
        
        # Merge Skills and ASCII Art side-by-side
        art_lines = self.player.ascii_art.splitlines()
        skills_and_art = []
        for skill, art in zip_longest(skill_list_raw, art_lines, fillvalue=""):
            # Pad skill to fixed width if it exists, else empty space
            skill_part = f"{skill:<30}" if skill else " " * 30
            art_part = art if art else ""
            skills_and_art.append(f"{skill_part}   {art_part}")

        defence_list = (
            [f"WEAPONS & ARMOR{' '*19:<10} "]
            + [" ".join(self.player.defence.keys())]
            + [" ".join([str(row) for row in self.player.defence.values()])]
        )
        weapons_list = [" ".join(self.player.weapons[0].keys())] + [
            " ".join([str(val) for val in row.values()]) for row in self.player.weapons
        ]
        
        # Helper for wrapping text fields
        def wrap_field(items):
            wrapped = []
            for item in items:
                if isinstance(item, dict): # Handle dicts like cyberware/gear
                    name = item.get("name", "Unknown")
                    notes = item.get("notes", "")
                    wrapped.append(f"\033[1m{name}\033[0m")
                    if notes:
                         wrapped.extend(textwrap.wrap(notes, width=60, initial_indent="  ", subsequent_indent="  "))
                elif isinstance(item, str): # Handle raw strings if any
                     wrapped.extend(textwrap.wrap(item, width=60))
            return wrapped

        # Process lists with wrapping
        ability_vals = list(self.player.role_ability.values())
        # Role ability is a dict {name:..., notes:...} usually? Check json structure.
        # Structure in json: "role_ability": {"name": "...", "notes": "..."}
        # In code: ability_list = list(self.player.role_ability.values()) which gives [name, notes]
        # Let's fix this to treat it properly:
        ability_list = []
        ra = self.player.role_ability
        if ra:
             ability_list.append(f"\033[1m{ra.get('name', 'Ability')}\033[0m")
             if "notes" in ra:
                 ability_list.extend(textwrap.wrap(ra["notes"], width=60, initial_indent="  ", subsequent_indent="  "))

        ware_list = wrap_field(self.player.cyberware)

        return {
            "header": header,
            "stats": stat_list,
            "stats": stat_list,
            "combat": combat_list,
            "skills": skills_and_art,
            # "ascii_art": self.player.ascii_art, # Integrated into skills now
            "defence": defence_list,
            "weapons": weapons_list,
            "abilities": ability_list,
            "cyberware": ware_list,
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
