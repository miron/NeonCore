from abc import ABC, abstractmethod

class StoryManager(ABC):
    """Singleton class that manages the different story modules in the 
       game.
    """

    _instance = None

    def __init__(self):
        self.current_story = None

   # instances = locals().copy()
   # for name, value in instances.items():
   #     if isinstance(value, Character):
   #         print(name)

    @classmethod
    def instance(cls):
        """Returns the singleton instance of the StoryManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_story(self, story_name: str):
        """Starts the specified story."""
        if story_name == "phone_call":
            self.current_story = PhoneCall()
        elif story_name == "heywood_industrial":
            self.current_story = HeywoodIndustrialStory()
        else:
            raise ValueError(f"Invalid story name: {story_name}")

    def end_story(self):
        """Ends the current story."""
        self.current_story = None

    @abstractmethod
    def update(self):
        """Updates the current story."""


