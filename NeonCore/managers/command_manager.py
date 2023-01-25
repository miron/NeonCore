from NeonCore.managers.character_manager import CharacterManager
from NeonCore.game_maps.game_map import Map


class CommandManager:
    commands = {
            'choose_character': ['do_choose_character',
                                 'complete_choose_character',
                                 'roles']}

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
        #print(self.game_state)
        #print(self.cmd_mngr.commands)
        if self.game_state in self.cmd_mngr.commands:
            commands = self.cmd_mngr.commands[self.game_state]
            for command in commands:
                command_method = getattr(self.cmd_mngr, command)
                #print(command)
                setattr(self, command, command_method) 
            #print((commands[0][3:]))
            return commands[0][3:]

        #if self.game_state == 'before_perception_check':
        #    use_skill = SkillCheckCommand(self.player)
        #    use_skill.register_command(self)
        #    return use_skill 
        #elif self.game_state == 'heywood_industrial':
        #    pass
        #elif self.game_state == 'before_ranged_combat':
        #    return RangedCombatCommand(self.player, self.npcs)
        return 

    def roles(self, text=''):
        return [
            c.role.lower() for c in 
            self.characters.values()] if not text else [
                c.role.lower() for c in 
                self.characters.values()  if 
                c.role.lower().startswith(text)]

    def do_choose_character(self, arg):
        """Allows the player to choose a character role."""
        if arg not in self.roles():
            characters_list = [
                f"{character.handle} ({character.role})" for  character in 
                self.characters.values()]
            self.columnize(characters_list, displaywidth=80)
            wprint(f"To pick yo' ride chummer, type in {self.roles()}.")
            return
        self.prompt = f"{arg} >>> "
        self.player = next(
            c for c in self.characters.values()  if 
            c.role.lower() == arg)
        self.npcs = [
            c for c in self.characters.values() if 
            c.role.lower() != arg]
        self.gamestat = 'character_chosen'

    def complete_choose_character(self, text, line, begidx, endidx):
        breakpoint()
        return self.roles(text)


if __name__ == '__main__':
    cmd_manager = CommandManager()
    print(cmd_manager.commands)
