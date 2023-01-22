from managers.action_manager  import ActionManager
from managers.cyberpunk_manager import CyberpunkManager
from managers.characters_manager import CharactersManager
from sheets import characters

if __name__ == "__main__":
    characters_manager = CharactersManager(characters)
    cyberpunk_manager = CyberpunkManager(characters_manager)
    action_manager = ActionManager(characters_manager)
    action_manager.start_game()
    

