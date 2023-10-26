from . import CharacterManager
from ..game_mechanics import SkillCheckCommand
from ..story_modules import PhoneCall
from ..game_maps import Map

commands = {
    "choose_character": [
        "CharacterManager.do_choose_character",
        "CharacterManager.complete_choose_character",
        "CharacterManager.roles",
    ],
    "character_chosen": [
        "CharacterManager.do_player_sheet",
        "CharacterManager.do_rap_sheet",
        "PhoneCall.do_phone_call",
    ],
    "before_perception_check": [
        "SkillCheckCommand.do_use_skill",
        "SkillCheckCommand.complete_use_skill",
        "Map.do_move",
    ],
}
