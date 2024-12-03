import logging

logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
from dataclasses import dataclass
from ..managers.character_manager import CharacterManager
from ..managers.command_manager import CommandManager
from ..managers.action_manager import ActionManager
from ..world.world import World
from ..managers import common

@dataclass
class GameDependencies:
    char_mngr: CharacterManager
    cmd_mngr: CommandManager
    world: World

    @classmethod
    def initialize_game(cls) -> ActionManager:
        char_mngr = CharacterManager()
        cmd_mngr = CommandManager()
        world = World(char_mngr)

        # Register commands
        for state, command in common.commands.items():
            cmd_mngr.register_command(state, command)

        dependencies = cls(
            char_mngr=char_mngr,
            cmd_mngr=cmd_mngr,
            world=world
        )

        return ActionManager(dependencies)
