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




   

