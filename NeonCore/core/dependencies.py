import logging

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)
from dataclasses import dataclass
from ..managers.character_manager import CharacterManager
from ..managers.command_manager import CommandManager
from ..managers.action_manager import ActionManager
from ..world.world import World
from ..managers import common
from ..game_mechanics.skill_check import SkillCheckCommand
from ..managers.npc_manager import NPCManager
from .game_io import GameIO


@dataclass
class GameDependencies:
    char_mngr: CharacterManager
    cmd_mngr: CommandManager
    world: World
    npc_manager: NPCManager
    io: GameIO
    skill_check: SkillCheckCommand = None

    @classmethod
    def initialize_game(cls, io: GameIO = None) -> ActionManager:
        # Initialize IO
        if io is None:
            from .game_io import ConsoleIO
            io = ConsoleIO()

        char_mngr = CharacterManager()
        cmd_mngr = CommandManager()
        npc_manager = NPCManager()
        world = World(char_mngr, npc_manager, io)

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
            npc_manager=npc_manager,
            skill_check=skill_check,
            io=io,
        )

        return ActionManager(dependencies)
