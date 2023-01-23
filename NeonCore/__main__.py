if __name__ == "__main__":
    game_map = Map()
    character = Character()
    character_manager = CharacterManager(characters)
    command_manager = CommandManager(game_map, character_manager)
   #cyberpunk_manager = CyberpunkManager(character_manager)
    action_manager = ActionManager(character_manager, 
                                   command_manager, game_map)
    action_manager.start_game()
    

