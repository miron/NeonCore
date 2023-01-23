class CyberpunkManager(StoryManager):
    def __init__(self, character_manager: CharacterManager):
        self.character_manager = character_manager
        self.heywood_industrial = HeywoodIndustrial(self.characters_manager)
        self.story_modules = {
            'heywood_industrial': self.heywood_industrial,
            #'phone_call': PhoneCall
        }

    def update(self):
        # Provide an implementation for the update method here
        pass

    def load_story_module(self, module_name: str):
        """
        Loads the specified story module and returns an instance of it
        """
        if module_name in self.story_modules:
            return self.story_modules[module_name]()
        else:
            raise ValueError(f"Invalid story module name: {module_name}")



