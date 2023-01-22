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

