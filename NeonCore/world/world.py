from typing import Dict
import random
from ..game_mechanics import SkillCheckCommand


class World:
    def __init__(self, char_mngr): # Add character manager as parameter
        super().__init__()
        self.char_mgr = char_mngr # Store reference to character manager
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
            # More locations...
        }

    def do_look(self, arg):
        """Look around your current location."""
        location = self.locations[self.player_position]
        print(location["description"])
        if location["ascii_art"]:
            print(location["ascii_art"])

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
                    npc = next((npc for npc in self.char_mngr.get_npcs()
                              if npc.handle.lower() == npc_name.lower()), None)
                    if npc:
                        print(f"You've encountered {npc.handle}!")
                        SkillCheckCommand(self.char_mngr.get_player(), npc=npc)
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
