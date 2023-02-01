from .character_manager  import CharacterManager
from ..story_modules.phone_call import PhoneCall
from .action_manager  import ActionManager
from ..game_maps.game_map import Map
from ..utils.utils import wprint


class CommandManager:
    #commands = {
    #    'phone_call': ['do_phone_call']}

    def check_state(self):
        """Check current game state and return commands that should be 
        registered"""
        # check game state and return appropriate commands
        return self.commands

    #def register_commands(self):
    #    """ Register commands in the appropriate class"""
    #    for command, value in self.check_state().items():
    #        for method in value['commands']:
    #            setattr(value['class'], method, 
    #            getattr(value['class'], method))

    def get_check_command(self):
        if self.game_state in CharacterManager.commands:
            commands = CharacterManager.commands[self.game_state]
        elif self.game_state in PhoneCall.commands:
            commands = PhoneCall.commands[self.game_state]
        for command in commands:
            command_method = getattr(CharacterManager, command)
            setattr(ActionManager, command, command_method) 
        return [commands[0][3:]]
        #if self.game_state == 'before_perception_check':
        #    use_skill = SkillCheckCommand(self.player)
        #    use_skill.register_command(self)
        #    return use_skill 
        #elif self.game_state == 'heywood_industrial':
        #    pass
        #elif self.game_state == 'before_ranged_combat':
        #    return RangedCombatCommand(self.player, self.npcs)


if __name__ == '__main__':
    cmd_manager = CommandManager()
    print(cmd_manager.commands)
