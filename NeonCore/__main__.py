from NeonCore.managers.action_manager import ActionManager
from NeonCore.managers.character_manager import CharacterManager
from NeonCore.managers.command_manager import CommandManager

if __name__ == "__main__":
    char_mngr = CharacterManager()
    cmd_mngr = CommandManager
   #cyberpunk_manager = CyberpunkManager(character_manager)
    act_mngr = ActionManager(char_mngr, cmd_mngr)
    act_mngr.start_game()
    

