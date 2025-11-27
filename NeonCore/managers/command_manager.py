from typing import Protocol
from . import common
from . import ActionManager
import logging # Added


class AbstractCommandManager(Protocol):
    def get_check_command(self): ...


class CommandManager:
    def __init__(self):
        self.commands = {}
        self.completions = {} # Added

    def check_state(self):
        """Check current game state and return commands that should be
        registered"""
        return self.commands

    def register_command(self, game_state, commands):
        """Register commands and their completions for a game state"""
        self.commands[game_state] = [cmd for cmd in commands if 'do_' in cmd]
        self.completions[game_state] = [cmd for cmd in commands if 'complete_' in cmd]

    def get_check_command(self, game_state):
        """Return list of command names for current game state"""
        logging.debug(f"Getting commands for state: {game_state}")
        try:
            commands = self.commands[game_state]
            # Strip class name and 'do_' prefix
            command_names = [cmd.split('.')[-1].replace('do_', '') for cmd in commands]
            logging.debug(f"Returning commands: {command_names}")
            return command_names
        except KeyError:
            return []

    def get_completion(self, game_state, command):
        """Get completion method for a command in current state"""
        try:
            return [comp for comp in self.completions[game_state]
                   if command in comp]
        except KeyError:
            return []


    def completenames(self, text, line, begidx, endidx):
        """Handle command completion including character roles"""
        if line.startswith('choose_character'):
            # If completing arguments for choose_character, use roles
            return self.char_mngr.roles(text)

        # Get base commands
        cmds = super().completenames(text, line, begidx, endidx)

        # Add commands from current game state
        if self.cmd_mngr:
            state_commands = self.cmd_mngr.get_check_command(self.game_state)
            cmds.extend(state_commands)

        return sorted(set(cmds))

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
