import textwrap


def wprint(text, width=80):
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)


class HelpSystem:
    """Dynamic help system for NeonCore that provides context-aware help based on game state."""
    
    def __init__(self):
        self.help_texts = {
            # General help texts available in all states
            "general": {
                "help": "Displays help information for available commands. Usage: help [command]",
                "quit": "Exits the game. Usage: quit",
                "talk": "Talk to NPCs using AI-generated responses. Usage: talk [your message]",
                "look": "Examine your surroundings. Usage: look"
            },
            
            # State-specific help texts
            "choose_character": {
                "choose_character": "Select your character from available roles. Usage: choose_character [role]",
                "switch_ai": "Switch between available AI backends (grok/ollama). Usage: switch_ai [backend_name]",
                "_intro": "Welcome to NeonCore! You need to choose a character to begin. Type 'help choose_character' for details."
            },
            
            "character_chosen": {
                "player_sheet": "Displays your character stats and abilities. Usage: player_sheet",
                "rap_sheet": "Displays your character's background and life story. Usage: rap_sheet",
                "phone_call": "Answer the incoming call to start your adventure. Usage: phone_call",
                "_intro": "Character selected! Check your stats with player_sheet, view your background with rap_sheet, or start the game with phone_call."
            },
            
            "before_perception_check": {
                "use_skill": "Use one of your character's skills. Usage: use_skill [skill_name]",
                "go": "Move in a direction. Usage: go [north/east/south/west]",
                "_intro": "You're now in the game world. Use 'look' to see your surroundings, 'go' to move around, and 'use_skill' to perform actions."
            }
        }
    
    def get_help(self, command=None, state="general"):
        """Get help text for a specific command in the current game state."""
        if command is None:
            # Return intro text for current state if available
            if "_intro" in self.help_texts.get(state, {}):
                return self.help_texts[state]["_intro"]
            else:
                return "Type 'help [command]' for information on specific commands."
        
        # First try state-specific help
        if state in self.help_texts and command in self.help_texts[state]:
            return self.help_texts[state][command]
        
        # Fall back to general help
        if command in self.help_texts["general"]:
            return self.help_texts["general"][command]
        
        return f"No help available for '{command}'."
    
    def get_available_commands(self, state="general"):
        """Get list of commands available in the current state."""
        commands = list(self.help_texts["general"].keys())
        
        # Add state-specific commands
        if state in self.help_texts:
            for cmd in self.help_texts[state]:
                if not cmd.startswith('_'):  # Skip intro/meta entries
                    commands.append(cmd)
        
        return sorted(list(set(commands)))
