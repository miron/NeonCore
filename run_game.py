import asyncio
from NeonCore.core.dependencies import GameDependencies


async def main():
    action_manager = GameDependencies.initialize_game()
    await action_manager.start_game()
    return 0


if __name__ == "__main__":
    asyncio.run(main())
