from typing import Protocol
from . import common
from . import ActionManager


class AbstractCommandManager(Protocol):
    def get_check_command(self): ...


class CommandManager:
    def __init__(self):
        self.commands = {}

    def check_state(self):
        """Check current game state and return commands that should be
        registered"""
        return self.commands

    def register_command(self, game_state, command):
        if game_state not in self.commands:
            self.commands[game_state] = []
        self.commands[game_state].append(command)

    def get_check_command(self, game_state):
        if game_state in common.commands:
            commands = common.commands[game_state]
            for command in commands:
                class_name, method_name = command.split(".")
                class_ = getattr(common, class_name)
                method = getattr(class_, method_name)
                setattr(ActionManager, method_name, method)
        return method_name[0][10:]

        # if game_state == 'heywood_industrial':
        #    pass
        # elif game_state == 'before_ranged_combat':
        #    return RangedCombatCommand(self.player, self.npcs)


# future expansion following
class CombatCommandManager:
    def get_check_command(self):
        """Combat related commands"""


class ItemCommandManager:
    def get_check_command(self):
        """Item related commands"""
