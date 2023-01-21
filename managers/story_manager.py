import abc
from character import Character

class StoryManager(metaclass=abc.ABCMeta):
    """
    Singleton class that manages the different story modules in the game.
    """

    _instance = None

    def __init__(self):
        from sheets import characters
        self.characters = characters
        self.characters_list = []
        self.load_characters() 
        
    def load_characters(self):
        #with open("characters.json") as f:
        #    characters_data - json.load(f)
        characters_data = self.characters 
        for char in characters_data:
            self.characters_list.append(Character(**char))

    def start_game(self):
        ActionManager(self.characters_list).cmdloop()

   # instances = locals().copy()
   # for name, value in instances.items():
   #     if isinstance(value, Character):
   #         print(name)

    @classmethod
    def instance(cls):
        """
        Returns the singleton instance of the StoryManager.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.current_story = None

    def start_story(self, story_name: str):
        """
        Starts the specified story.
        """
        if story_name == "heywood_industrial":
            self.current_story = HeywoodIndustrialStory()
        elif story_name == "phone_call":
            self.current_story = PhoneCall()
        else:
            raise ValueError(f"Invalid story name: {story_name}")

    def end_story(self):
        """
        Ends the current story.
        """
        self.current_story = None

    @abc.abstractmethod
    def update(self):
        """
        Updates the current story.
        """
        pass


