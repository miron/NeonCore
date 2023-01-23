from managers import CommandManager
from managers import CharacterManager
from managers import ActionManager

if __name__ == "__main__":
    character_manager = CharacterManager()
   #cyberpunk_manager = CyberpunkManager(character_manager)
    action_manager = ActionManager(character_manager)
    command_manager = CommandManager(action_manager)
    action_manager.start_game()
    

