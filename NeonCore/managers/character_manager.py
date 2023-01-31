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
            ascii_art_path = (
                Path(__file__).parent.parent / 
                f'character_assets/{char["ascii_art"]}')
            with open(ascii_art_path, 'r') as f:
                char['ascii_art'] = f.read()
            self.characters[char["char_id"]] = Character(**char)

