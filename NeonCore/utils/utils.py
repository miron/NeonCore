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
                "quit": "Jack out. Exit the game.",
                "talk": "Initiate conversation with an NPC. Usage: talk [name]",
                "look": "Examine your surroundings or specific targets. Usage: look [target]",
                "gear": "Check your inventory and equipment. Usage: gear",
            },
            
            # State-specific help texts
            "choose_character": {
                "choose": "Select your character by Handle. Usage: choose [handle] (e.g. choose mover)",
                "switch_ai": "Switch between available AI backends (grok/ollama). Usage: switch_ai [backend_name]",
                "_intro": "Welcome to NeonCore! Choose a character to begin. Hit TAB to see available commands."
            },
            
            "character_chosen": {
                "whoami": "View Identity Dashboard (Stats, Bio, Soul). Usage: whoami [stats|bio|soul]",
                "reflect": "Process events and evolve your Digital Soul. Usage: reflect",
                "answer": "Answer the incoming holo-call from Lazlo. Usage: answer",
                "_intro": "Character selected! Incoming Holo-Call... Type 'answer' to pick up."
            },
            
            "before_perception_check": {
                "use_skill": "Use one of your character's skills. Usage: use_skill [skill_name]",
                "go": "Move in a direction. Usage: go [north/east/south/west]",
                "_intro": "You're in the game world. Explore and survive. Hit TAB to see available commands."
            },
            
            "conversation": {
                "say": "Speak to the character. Usage: say [message] (or just type the message)",
                "take": "Attempt to take an object. Usage: take [item]",
                "bye": "End the conversation. Usage: bye",
                "_intro": "Conversation Mode. Type your message or use commands. Hit TAB for options."
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
