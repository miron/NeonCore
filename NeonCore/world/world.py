from typing import Dict
import random
from ..game_mechanics import SkillCheckCommand


class World:
    def __init__(self, char_mngr): # Add character manager as parameter
        self.char_mngr = char_mngr # Store reference to character manager
        self.locations: Dict[str, Dict] = self._init_locations()
        self.player_position = "start_square"
        self.inventory = []

    def _init_locations(self) -> Dict[str, Dict]:
        # Example structure
        return {
            "start_square": {
                "description": "You stand in the heart of Neon City, surrounded by towering skyscrapers and flickering holographic ads.",
                "exits": {"north": "market_street", "east": "dark_alley"},
                "ascii_art": None,  # No special art for this common place
                "npcs": [],  # No NPCs in starting area
                "encounter_chance": 0
            },
            "market_street": {
                "description": "Vendors hawk everything from black market tech to street food. The air buzzes with the hum of drones.",
                "exits": {"south": "start_square", "west": "corporate_plaza"},
                "ascii_art": """
                +----------------+
                |   MARKET ST.   |
                |  [ ] [ ] [ ]   |
                |  [ ] [X] [ ]   |
                |  [ ] [ ] [ ]   |
                +----------------+
                """,
                "npcs": ["street_thug", "gang_member", "street_vendor", "netrunner"],  # Potential NPCs to encounter
                "encounter_chance": 0.4  # 40% chance of encounter
            },
            "dark_alley": {
                "description": "A narrow passage between buildings, shrouded in shadow. Graffiti covers the walls and the air smells of chemicals and decay.",
                "exits": {"west": "start_square", "north": "industrial_zone"},
                "ascii_art": """
                +----------------+
                |   DARK ALLEY   |
                |  [\\] [|] [/]   |
                |  [\\] [|] [/]   |
                |  [\\] [|] [/]   |
                +----------------+
                """,
                "npcs": ["street_thug", "cyberjunkie", "black_market_dealer"],
                "encounter_chance": 0.6  # 60% chance of encounter
            },
            "corporate_plaza": {
                "description": "Clean and sterile, the corporate plaza gleams with polished surfaces and armed guards. Corporate logos dominate the skyline.",
                "exits": {"east": "market_street"},
                "ascii_art": """
                +----------------+
                |    CORP PLAZA  |
                |  [█] [█] [█]   |
                |  [█] [X] [█]   |
                |  [█] [█] [█]   |
                +----------------+
                """,
                "npcs": ["corpo_exec", "security_guard", "office_worker"],
                "encounter_chance": 0.3
            },
            "industrial_zone": {
                "description": "Massive factories and warehouses dominate this area. The air is thick with smog and the sound of machinery never stops.",
                "exits": {"south": "dark_alley"},
                "ascii_art": """
                +----------------+
                | INDUSTRIAL ZN  |
                |  [▮] [▮] [▮]   |
                |  [▮] [X] [▮]   |
                |  [▮] [▮] [▮]   |
                +----------------+
                """,
                "npcs": ["factory_worker", "gang_member", "corpo_security"],
                "encounter_chance": 0.5
            }
        }

    def do_look(self, arg):
        """Look around your current location."""
        location = self.locations[self.player_position]
        print(location["description"])
        if location["ascii_art"]:
            print(location["ascii_art"])
            
        # Show available exits
        exits = location["exits"]
        if exits:
            exit_list = ", ".join(exits.keys())
            print(f"Exits: {exit_list}")
        else:
            print("There are no obvious exits.")

    def do_go(self, direction):
        """Move to another location. Usage: go [direction]"""
        direction = direction.lower()
        current_location = self.locations[self.player_position]
        if direction in current_location["exits"]:
            self.player_position = current_location["exits"][direction]

            # NPC encounter logics
            if 'npcs' in current_location:
                # Random chance for encounter
                if random.random() < current_location.get('encounter_chance', 0.3):
                    npc_name = random.choice(current_location['npcs'])
                    # Get actual NPC object from character manager
                    try:
                        npc = next((npc for npc in self.char_mngr.npcs
                              if npc.handle.lower() == npc_name.lower()), None)
                        if npc:
                            print(f"You've encountered {npc.handle}!")
                            SkillCheckCommand(self.char_mngr.player, npc=npc)
                    except Exception as e:
                        print(f"Error finding NPC: {e}")
            self.do_look(None)  # Automatically look after moving
        else:
            print(f"You can't go {direction} from here.")

    def do_quit(self, arg):
        """Quit the game."""
        print("Thanks for playing!")
        return True

    def default(self, line):
        """Called on an input line when the command prefix is not recognized."""
        print("Unknown command. Type 'help' for available commands.")

class Map:
    def __init__(self, player, npcs):
        self.player = player
        self.npcs = npcs
        self.encountered_npc = False
        self.map_data = (
            "### ####  ######",
            "###   ##  ######",
            "                ",
            " ##            #",
            " ## ###        #",
            " ## ###   ###  #",
            "    ###   ###  #",
            "          ###  #",
            "###       ###  #",
            "### ####  ###   ",
            "### ####  ###   ",
        )

def check_for_npc_encounter(self) -> bool:
    """Check if player encounters an NPC in current location"""
    location = self.locations[self.player_position]
    if 'npcs' in location and random.random() < location.get('encounter_chance', 0):
        return True
    return False

def get_location_npc(self):
    """Get a random NPC from current location"""
    location = self.locations[self.player_position]
    if 'npcs' in location:
        npc_id = random.choice(location['npcs'])
        return self.char_mngr.get_npc(npc_id)  # assuming this exists
    return None
