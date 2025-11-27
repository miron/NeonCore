# Change to singleton
import json
import uuid
from pathlib import Path
import logging

from NeonCore.managers.action_manager import ActionManager

from .character import Character


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
        file_path = Path(__file__).parent.parent / "character_assets/characters.json"
        with open(file_path) as f:
            characters_data = json.load(f)
        for char in characters_data:
            char["char_id"] = uuid.uuid4()
            ascii_art_path = (
                Path(__file__).parent.parent / f'character_assets/{char["ascii_art"]}'
            )
            with open(ascii_art_path, "r", encoding="utf-8") as f:
                char["ascii_art"] = f.read()
            self.characters[char["char_id"]] = Character(**char)

    def roles(self, text=""):
        """Return list of available character roles"""
        text_lower = text.lower()  # Hoist method call outside loop
        roles = [c.role.lower() for c in self.characters.values() if c.role.lower().startswith(text_lower)]
        logging.debug(f"Available roles: {roles}")
        return roles

    def get_player_sheet_data(self):
        """Prepares character sheet data without formatting"""
        header = (
            f"HANDLE \033[1;3;35m{self.player.handle:⌁^33}"
            "\033[0m ROLE "
            f"\033[1;3;35m{self.player.role:⌁^33}\033[0m"
        )
        stat_list = [
            (
                f"{key:⌁<12}{self.player.lucky_pool}/{value}"
                if key == "luck"
                else f"{key:⌁<12}{value:>2}"
            )
            for key, value in self.player.stats.items()
        ]
        combat_list = [
            (f"{key:⌁<23}{value:>2}")
            for key, value in self.player.combat.items()
        ]
        skill_keys = list(self.player.skills.keys())
        skill_values = list(self.player.skills.values())
        skill_list = [
            (f"{key:⌁<30}{value[0]:>2}")
            for key, value in zip(skill_keys, skill_values)
            if value[1 != 0]
        ]
        skill_list += self.player.ascii_art.splitlines()

        defence_list = (
            [f"WEAPONS & ARMOR{'⌁'*19:<10} "]
            + [" ".join(self.player.defence.keys())]
            + [" ".join([str(row) for row in self.player.defence.values()])]
        )
        weapons_list = [" ".join(self.player.weapons[0].keys())] + [
            " ".join([str(val) for val in row.values()])
            for row in self.player.weapons
        ]
        ability_list = list(self.player.role_ability.values())
        ability_list = [row.splitlines() for row in ability_list]
        ability_list = [item for sublist in ability_list for item in sublist]
        ware_list = [
            value
            for row in self.player.cyberware
            for key, value in row.items()
        ]
        ware_list = [row.splitlines() for row in ware_list]
        ware_list = [item for sublist in ware_list for item in sublist]
        gear_list = (
            [" ".join(self.player.gear[0].keys())]
            + [" ".join(row.values()) for row in self.player.gear]
            + [""]
        )

        return {
            'header': header,
            'stats': stat_list,
            'combat': combat_list,
            'skills': skill_list,
            'defence': defence_list,
            'weapons': weapons_list,
            'abilities': ability_list,
            'cyberware': ware_list,
            'gear': gear_list
        }
            # if ability == ability_list[0]:
            #    ability = "\033[1m" + ability + "\033[0m"
            # if ware == ware_list[0]:
            #    ware = "\033[1m" + ware + "\033[0m"
            # if gear == gear_list[0]:
            #    gear = "\033[1m" + gear + "\033[0m"

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
        print(rap_sheet)
