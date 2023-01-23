from managers import CharacterManager
from game_maps import Map
class CommandManager:
    def __init__(self, action_manager):
        self.commands = {
            'choose_character': {
                'class': CharacterManager, 
                'commands': ['do_choose_character']},
            'player_sheet': {
                'class': CharacterManager, 
                'commands': ['do_player_sheet']},
            'move': {
                'class': Map, 
                'commands': ['do_move']}
            }

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

    def register_command(self, action_manager):
        setattr(action_manager, 'do_choose_character', 
                self.do_choose_character)
        setattr(action_manager, 'complete_choose_character', 
                self.complete_choose_character)
        setattr(action_manager, 'roles', self.roles)

    def get_available_commands(self):
        return [name[3:] for name in dir(self) if name.startswith("do_")]

    def get_check_command(self):
        #if self.game_state == 'character_chosen':
        #   pass
        #if self.game_state == 'before_perception_check':
        #    use_skill = SkillCheckCommand(self.player)
        #    use_skill.register_command(self)
        #    return use_skill 
        #elif self.game_state == 'heywood_industrial':
        #    pass
        #elif self.game_state == 'before_ranged_combat':
        #    return RangedCombatCommand(self.player, self.npcs)
        return 
