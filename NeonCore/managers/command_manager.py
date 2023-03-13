from typing import Protocol
from . import common
from . import ActionManager


class AbstractCommandManager(Protocol):
    def get_check_command(self):
        ... 


class CommandManager:
    def check_state(self):
        """Check current game state and return commands that should be 
        registered"""
        return self.commands

    def get_check_command(self):
        if self.game_state in common.commands:
            commands = common.commands[self.game_state]
        for command in commands:
            class_name, method_name = command.split('.')
            class_ = getattr(common, class_name)
            method = getattr(class_,  method_name)
            setattr(ActionManager, method_name, method) 
        return method_name[0][3:]
        #if self.game_state == 'heywood_industrial':
        #    pass
        #elif self.game_state == 'before_ranged_combat':
        #    return RangedCombatCommand(self.player, self.npcs)


# future expansion following
class CombatCommandManager:
    def get_check_command(self):
        """Combat related commands"""


class ItemCommandManager:
    def get_check_command(self):
        """Item related commands """
