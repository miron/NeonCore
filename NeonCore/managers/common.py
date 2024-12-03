from . import CharacterManager
from ..game_mechanics import SkillCheckCommand
from ..story_modules import PhoneCall
from ..world import World

commands = {
    "choose_character": [
        "CharacterManager.do_choose_character"
    ],
    "character_chosen": [
        "CharacterManager.do_player_sheet",
        "CharacterManager.do_rap_sheet",
        "PhoneCall.do_phone_call",
    ],
    "before_perception_check": [
        "World.do_go", # For movement between locations
        "SkillCheckCommand.do_use_skill", # For when encountering NPCs
    ],
}
