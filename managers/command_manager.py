class CommandRegistrar:
    def __init__(self):
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

    def register_commands(self):
        """ Register commands in the appropriate class"""
        for command, value in self.check_state().items():
            for method in value['commands']:
                setattr(value['class'], method, getattr(value['class'], method))

