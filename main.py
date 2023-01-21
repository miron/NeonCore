from managers.story_manager import StoryManager
from managers.action_manager import ActionManager

if __name__ == "__main__":
    story_manager = StoryManager()
    action_manager = ActionManager(story_manager.characters_list())
    action_manager.start_game()

