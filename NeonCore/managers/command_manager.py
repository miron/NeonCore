from typing import Protocol
from . import CharacterManager
from . import ActionManager
from ..game_mechanics import SkillCheckCommand
from ..story_modules import PhoneCall
from ..game_maps import  Map




class AbstractCommandManager(Protocol):
    def get_check_command(self):
        ... 


class CommandManager:
    def check_state(self):
        """Check current game state and return commands that should be 
        registered"""
        # check game state and return appropriate commands
        return self.commands

    def get_check_command(self):
        if self.game_state in CharacterManager.commands:
            commands = CharacterManager.commands[self.game_state]
        elif self.game_state in PhoneCall.commands:
            commands = PhoneCall.commands[self.game_state]
        for command in commands:
            class_name, method_name = command.split('.')
            class_ = globals()[class_name]
            method = getattr(class_, method_name)
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
