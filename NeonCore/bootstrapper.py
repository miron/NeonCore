from NeonCore.managers import common

# TODO: Instantiate SkillCheckCommand object
from .game_mechanics import SkillCheckCommand
from .managers import ActionManager, CharacterManager, CommandManager


class Bootstrapper:
    def __init__(self):
        self.char_mngr = CharacterManager()
        self.cmd_mngr = CommandManager()
        for state, command in common.commands.items():
            self.cmd_mngr.register_command(state, command)

    def create_action_manager(self):
        # TODO: Pass SkillCheckCommand object to ActionManager constructor
        act_mngr = ActionManager(self.char_mngr, self.cmd_mngr)
        return act_mngr
