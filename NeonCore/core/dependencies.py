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
from ..game_mechanics.skill_check import SkillCheckCommand

@dataclass
class GameDependencies:
    char_mngr: CharacterManager
    cmd_mngr: CommandManager
    world: World
    skill_check: SkillCheckCommand = None

    @classmethod
    def initialize_game(cls) -> ActionManager:
        char_mngr = CharacterManager()
        cmd_mngr = CommandManager()
        world = World(char_mngr)
        
        # Initialize the skill check command
        skill_check = SkillCheckCommand()
        skill_check.char_mngr = char_mngr

        # Register commands
        for state, command in common.commands.items():
            cmd_mngr.register_command(state, command)

        dependencies = cls(
            char_mngr=char_mngr,
            cmd_mngr=cmd_mngr,
            world=world,
            skill_check=skill_check
        )

        return ActionManager(dependencies)