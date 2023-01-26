from .managers import ActionManager
from .managers import CharacterManager
from .managers import CommandManager

if __name__ == "__main__":
    char_mngr = CharacterManager()
    cmd_mngr = CommandManager
   #cyberpunk_manager = CyberpunkManager(character_manager)
    act_mngr = ActionManager(char_mngr, cmd_mngr)
    act_mngr.start_game()
    

