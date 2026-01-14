from typing import Dict
import random
from ..game_mechanics import SkillCheckCommand
from ..utils import wprint


from ..managers.database_manager import DatabaseManager

class World:
    def __init__(self, char_mngr, npc_manager, io):
        self.char_mngr = char_mngr
        self.npc_manager = npc_manager
        self.io = io
        self.locations: Dict[str, Dict] = self._init_locations()
        self.player_position = "start_square"
        self.inventory = []
        self.db = DatabaseManager()

    def _init_locations(self) -> Dict[str, Dict]:
        # Example structure
        return {
            "start_square": {
                "description": "You stand in the heart of Neon City, surrounded by towering skyscrapers and flickering holographic ads.",
                "exits": {"north": "market_street", "east": "dark_alley"},
                "ascii_art": """
   | |      .      | |
   | |      |      | |
   | |  |¯| | |¯|  | |
   | |  | | | | |  | |
___|_|__|_|_|_|_|__|_|___
""",
                "encounter_chance": 0,
            },
            "market_street": {
                "description": "Vendors hawk everything from black market tech to street food. The air buzzes with the hum of drones.",
                "exits": {"south": "start_square", "west": "corporate_plaza"},
                "ascii_art": """
      _______       _______
     |  ___  |     |  ___  |
     | |___| |     | |___| | [Shop]
     |_______|     |_______|
_____|_______|_____|_______|_____
""",
                "npcs": [
                    "street_thug",
                    "gang_member",
                    "street_vendor",
                    "netrunner",
                ],  # Potential NPCs to encounter
                "encounter_chance": 0.4,  # 40% chance of encounter
                "items": [],
            },
            "dark_alley": {
                "description": "A narrow passage between buildings, shrouded in shadow. Graffiti covers the walls and the air smells of chemicals and decay.",
                "exits": {"west": "start_square", "north": "industrial_zone"},
                "ascii_art": """
      _______
     |   |   | [Gener8r]
     |   |   |   _____
     |   |___|  [_____]
_____|___________________
""",
                "npcs": ["street_thug", "cyberjunkie", "black_market_dealer"],
                "encounter_chance": 0.6,  # 60% chance of encounter
                "items": [],
            },
            "corporate_plaza": {
                "description": "Clean and sterile, the corporate plaza gleams with polished surfaces and armed guards. Corporate logos dominate the skyline.",
                "exits": {"east": "market_street"},
                "ascii_art": """
      .___________.
      |           |
      |   ( $ )   |
      |___________|
______|___________|______
""",
                "npcs": ["corpo_exec", "security_guard", "office_worker"],
                "encounter_chance": 0.3,
                "items": [],
            },
            "industrial_zone": {
                "description": "Massive factories and warehouses dominate this area. The air is thick with smog and the sound of machinery never stops.",
                "exits": {"south": "dark_alley", "east": "street_corner", "north": "heywood_industrial"},
                "ascii_art": """
    /\\      /\\      /\\
   |  |    |  |    |  |
   |__|____|__|____|__|
   |  |    |  |    |  |
___|__|____|__|____|__|___
""",
                "npcs": [
                    "factory_worker",
                    "corpo_security",
                ],
                "encounter_chance": 0.5,
                "items": [],
            },
            "heywood_industrial": {
                "description": "An industrial park in Heywood. The alleyway looks perfect for a shady deal. Or an ambush.",
                "exits": {"south": "industrial_zone", "north": "heywood_alley"},
                "ascii_art": """
       _______
      |       |
      |Factory|      OPEN
      |_______|      AREA
______|_______|_________________
""",
                "npcs": [],
                "encounter_chance": 0,
                "items": [],
            },
            "heywood_alley": {
                "description": "A dead-end alleyway between massive industrial structures. A hooded man stands here waiting.",
                "exits": {"south": "heywood_industrial", "north": "warehouse_entrance"},
                "ascii_art": """
      | |
      | |    (Hooded Man)
      | |        O
      | |       /|\\
______| |_______/ \\_____
""",
                "npcs": [],  # Hooked Man (Lenard) is spawned by script, not random encounter
                "encounter_chance": 0,
                "items": [],
            },
            "warehouse_entrance": {
                "description": "The entrance to a large warehouse. It looks quiet. Too quiet.",
                "exits": {"south": "heywood_alley", "enter": "warehouse_interior"},
                "ascii_art": """
    _________________
   |    WAREHOUSE    |
   |   ___________   |
   |  |   |   |   |  |
___|__|_^_|_^_|_^_|__|___
""",
                "npcs": [],
                "encounter_chance": 0,
                "items": [],
            },
            "warehouse_interior": {
                "description": "Inside the warehouse. Rows of crates and conveyor belts fill the space.",
                "exits": {"exit": "warehouse_entrance"},
                "ascii_art": """
 || [BOX] | [BOX] ||
 || [BOX] | [BOX] ||
 ||_______|_______||
 || [===] | [===] ||
_||_______|_______||_
""",
                "npcs": [], # Ambush cops spawn here
                "encounter_chance": 0,
                "items": [],
            },
            "street_corner": {
                "description": "A rain-slicked intersection under a flickering streetlight. A yellow 'NC Express' drop box stands against a graffiti-stained wall.",
                "exits": {"west": "industrial_zone"},
                "ascii_art": """
      |   |         .       |   |
      |   |       .   .     |   |
      |   |       |___|     |   |
______|___|_______|___|_____|___|______
     /   /       [BOX]     /   /
____/___/_________________/___/________
""",
                "npcs": [],
                "encounter_chance": 0.1,
                "items": [],
            },
        }

    def add_item(self, location_id, item):
        """Add an item to a location (Persist to DB)."""
        item_name = item.get('name') if isinstance(item, dict) else item
        
        # 1. Check if it's already an existing DB instance (Has ID)
        if isinstance(item, dict) and "id" in item:
            self.db.update_item_state(item["id"], location_id=location_id, owner_id=None)
            return

        # 2. Legacy/New Item: Create a fresh instance from Template
        # Try to find template by name (Simple lookup map for now, or query DB by name?)
        # For prototype, we hardcode the mapping or rely on name matching
        # In a real app, 'item' should ALWAYS have a template_id ref.
        
        # Look up template ID (Hack for now: Seeding assumed known IDs or Names)
        # We'll just try to create an instance for "Glitching Burner"
        template_id = None
        conn = self.db._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM item_templates WHERE name LIKE ?", (item_name,))
        row = cursor.fetchone()
        
        if row:
            template_id = row[0]
            self.db.create_instance(template_id, location_id=location_id)
        else:
            # Fallback: Create ad-hoc template so item is not lost
            # Check for description in item dict if available
            desc = "A dropped item."
            if isinstance(item, dict):
                 desc = item.get("notes", desc)
                 
            template_id = self.db.create_template(item_name, "gear", desc)
            self.db.create_instance(template_id, location_id=location_id)

    def remove_item(self, location_id, item_name):
        """Pick up an item (Remove from Location in DB, return Instance)."""
        # Find item in DB at this location
        items = self.db.get_items_in_location(location_id)
        for item in items:
            if item["name"].lower() == item_name.lower():
                # Found it.
                # Update State: Remove from location (Conceptually). 
                # Caller (ActionManager) will assign Owner, so we just return it.
                # But to prevent 'look' from finding it before Owner assignment, we set loc=None.
                self.db.update_item_state(item["id"], location_id=None, owner_id=None)
                return item
        return None

    def get_items_in_location(self, location_id):
        """Get list of items in a location (From DB)."""
        return self.db.get_items_in_location(location_id)

    async def do_look(self, arg):
        """Look around your current location or at a specific character. Usage: look [target]"""
        # Specific target lookup
        if arg:
            # Check NPCs
            target_npc = self.npc_manager.get_npc(arg)
            if target_npc and target_npc.location == self.player_position:
                rel_tag = ""
                player_handle = self.char_mngr.player.handle
                status = target_npc.relationships.get(player_handle)
                if status and status.lower() == "fan":
                    rel_tag = " \033[1;36m[ FAN ]\033[0m"

                await self.io.send(
                    f"\n\033[1;36m=== {target_npc.handle.upper()} ({target_npc.role}){rel_tag}\033[1;36m ===\033[0m"
                )
                # Use Standard Character Sheet Display
                sheet_data = self.char_mngr.get_character_sheet_data(target_npc)
                
                # Check Description First (Flavor Text)
                await self.io.send(target_npc.description)
                
                # Display Sheet
                await self.io.display(sheet_data, view_type="character_sheet")

                return
            else:
                await self.io.send(f"You don't see '{arg}' here.")
                return

        # Location lookup
        location = self.locations[self.player_position]
        await self.io.send(location["description"])
        if location["ascii_art"]:
            await self.io.send(location["ascii_art"])

        # Story Check Hook (Safety Net)
        if self.player_position == "heywood_alley":
             # If we are here, dirty cops should NOT be visible unless the ambush started.
             # If the script failed to trigger in 'update', we might trigger it here manually?
             # No, better to trust the StoryManager loop, but we can verify visibility.
             pass

        # List NPCs currently in this location
        visible_npcs = self.npc_manager.get_npcs_in_location(self.player_position)
        if visible_npcs:
            # unique list to avoid duplicates from aliases
            unique_npcs = {npc.handle: npc for npc in visible_npcs}.values()
            npc_names = []
            player_handle = self.char_mngr.player.handle
            for npc in unique_npcs:
                # Check for Relationship Status (e.g. Fan)
                rel_tag = ""
                status = npc.relationships.get(player_handle)
                if status and status.lower() == "fan":
                    rel_tag = " \033[1;36m[ FAN ]\033[0m" # Cyan tag for positive

                npc_names.append(f"\033[1;35m{npc.handle} ({npc.role}){rel_tag}\033[0m")
            await self.io.send(f"\nVisible Characters: {', '.join(npc_names)}")

        # List Items on the ground
        items = self.locations[self.player_position].get("items", [])
        if items:
            item_names = []
            for item in items:
                name = item.get('name') if isinstance(item, dict) else item
                item_names.append(f"\033[1;33m{name}\033[0m")
            await self.io.send(f"\nItems on ground: {', '.join(item_names)}")

        # Show available exits
        exits = location["exits"]
        if exits:
            exit_list = ", ".join(exits.keys())
            await self.io.send(f"\nExits: {exit_list}")
        else:
            await self.io.send("\nThere are no obvious exits.")

    async def do_go(self, direction):
        """Move to another location. Usage: go [direction]"""
        direction = direction.lower()
        current_location = self.locations[self.player_position]
        try:
            self.player_position = current_location["exits"][direction]
        except KeyError:
            await self.io.send(f"You can't go {direction} from here.")
            return

        # NPC encounter logic using EAFP
        try:
            npcs = current_location["npcs"]
            # Random chance for  encounter
            if random.random() < current_location.get("encounter_chance", 0.3):
                npc_name = random.choice(npcs)
                # Get actual NPC object from character manager
                npc = next(
                    (
                        npc
                        for npc in self.char_mngr.npcs
                        if npc.handle.lower() == npc_name.lower()
                    ),
                    None,
                )
                if npc:
                    await self.io.send(f"You've encountered {npc.handle}!")
                    SkillCheckCommand(self.char_mngr.player, npc=npc)
        except KeyError:
            pass  # No NPCs in this location
        except Exception as e:
            await self.io.send(f"Error during NPC encounter: {e}")

        await self.do_look(None)  # Automatically look after moving

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
    try:
        return random.random() < location.get("encounter_chance", 0) and bool(
            location["npcs"]
        )
    except KeyError:
        return False


def get_location_npc(self):
    """Get a random NPC from current location"""
    location = self.locations[self.player_position]
    try:
        npc_id = random.choice(location["npcs"])
        return self.char_mngr.get_npc(npc_id)  # assuming this exists
    except KeyError:
        return None
