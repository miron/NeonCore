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



