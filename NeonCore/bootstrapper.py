
from .managers import ActionManager
from .managers import CharacterManager
from .managers import CommandManager
from .game_mechanics import SkillCheckCommand

class Bootstrapper:
    def __init__(self):
        self.char_mngr = CharacterManager()
        # TODO: Make completion work with instance of CommandManager, not class
        self.cmd_mngr = CommandManager
        self.skcc = SkillCheckCommand(self.char_mngr)

    def create_action_manager(self):
        act_mngr = ActionManager(self.char_mngr, self.cmd_mngr, self.skcc)
        return act_mngr

