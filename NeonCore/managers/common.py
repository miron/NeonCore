from . import CharacterManager
from ..game_mechanics import SkillCheckCommand
from ..story_modules import PhoneCall
from ..world import World

commands = {
    "choose_character": ["CharacterManager.do_choose_character"],
    "character_chosen": [
        "PhoneCall.do_answer",
    ],
    "before_perception_check": [
        "World.do_go",  # For movement between locations
        "World.do_look",  # For examining locations
        "SkillCheckCommand.do_use_skill",  # For when encountering NPCs
        "ActionManager.do_inventory",  # Check gear
    ],
    "conversation": [
        "ActionManager.do_say",
        "ActionManager.do_bye",
        "ActionManager.do_take",  # For intent actions
        "ActionManager.do_inventory",
        "World.do_look",  # Allow looking during conversation
    ],
}
