import asyncio
from NeonCore.core.dependencies import GameDependencies


async def main():
    # Explicitly init IO so we can set the handler for tab completion
    from NeonCore.core.game_io import ConsoleIO
    io = ConsoleIO()
    
    action_manager = GameDependencies.initialize_game(io=io)
    io.set_cmd_handler(action_manager) # Enable tab completion
    
    await action_manager.start_game()
    return 0


if __name__ == "__main__":
    asyncio.run(main())
