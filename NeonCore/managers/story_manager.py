from abc import ABC, abstractmethod
import logging

class Story(ABC):
    """Abstract base class for all story modules."""
    
    def __init__(self, name: str):
        self.name = name
        self.state = "start"
    
    @abstractmethod
    async def start(self, game_context):
        """Called when the story begins."""
        pass
        
    @abstractmethod
    async def update(self, game_context):
        """Called every game loop iteration to check triggers."""
        pass
        
    @abstractmethod
    async def end(self, game_context):
        """Called when the story ends."""
        pass

    async def handle_use_skill(self, game_context, skill_name, target):
        """
        Optional: Handle skill checks specific to this story step.
        Returns True if handled, False/None if default logic should proceed.
        """
        return False

    async def handle_use_object(self, game_context, object_name):
        """
        Optional: Handle object usage specific to this story.
        """
        return False


class StoryManager:
    """Singleton class that manages the active story and transition logic."""

    _instance = None
    _dependencies = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StoryManager, cls).__new__(cls)
            cls._instance.current_story = None
            cls._instance.available_stories = {}
            cls._instance.scene_triggered = False
        return cls._instance

    def set_dependencies(self, dependencies):
        """Inject game dependencies (ActionManager, etc.)"""
        self._dependencies = dependencies

    def register_story(self, story_class):
        """Register a story class to be available for starting."""
        story_instance = story_class()
        self.available_stories[story_instance.name] = story_instance
        logging.info(f"Registered story: {story_instance.name}")

    async def start_story(self, story_name: str):
        """Starts the specified story by name."""
        if story_name not in self.available_stories:
             logging.error(f"Story '{story_name}' not found.")
             print(f"Story '{story_name}' is not available.")
             return

        if self.current_story:
            await self.current_story.end(self._dependencies)

        self.current_story = self.available_stories[story_name]
        await self.current_story.start(self._dependencies)
        logging.info(f"Started story: {story_name}")

    async def end_story(self):
        """Ends the current story safely."""
        if self.current_story:
            await self.current_story.end(self._dependencies)
            print(f"Story '{self.current_story.name}' ended.")
            self.current_story = None

    async def update(self):
        """Updates the current story. Called from the main game loop."""
        self.scene_triggered = False
        if self.current_story:
            return await self.current_story.update(self._dependencies)
        return False
