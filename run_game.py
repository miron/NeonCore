# miron/NeonCore/run_game.py
from NeonCore.core.dependencies import GameDependencies

def main():
    action_manager = GameDependencies.initialize_game()
    action_manager.start_game()
    return 0

if __name__ == "__main__":
    main()
