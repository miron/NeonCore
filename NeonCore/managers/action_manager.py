"""A Role Playing Game in the Cyberpunk Universe"""

# Standard library imports
import sys
import os
import logging
import json
import random
from ..core.async_cmd import AsyncCmd
from argparse import Action

# third party imports
import logging

# Patch pyreadline3 for Python 3.14 compatibility
try:
    import readline

    if not hasattr(readline, "backend"):
        # Add missing backend attribute for Python 3.14+ compatibility
        readline.backend = "pyreadline3"
except ImportError:
    pass  # readline not available (fine on non-Windows or without pyreadline3)

# Local imports
from ..utils import wprint
from ..ai_backends.ollama import OllamaBackend
from ..ai_backends.gemini import GeminiBackend
from ..game_mechanics.combat_system import CombatEncounter


class ActionManager(AsyncCmd):
    """cli, displays character stats/skills, quits the game"""

    intro = r"""     ᐸ ソ ╱> /Ξ /≥ /> // /𐑘/ /ᐸ
                      ‾
   …   ˛⁄⁔       ˛⁔     ⁔    _  ¸¸
  (˙}  \(∞l   ,, {˚)/ ¸{=}˛ |\\(˚}
 /(\)╲  `••\˛_ \/(⎔◊𐑘 (\+/)  \∏(p)]
 \ᢘ╦╤═÷- Y¸∆     ¸U˛   \Ξ˛\   ´¸v˛|
  7˘ 𐑘 ¸⁄∫𐑘      [][]  7 𐑘 `   [ ]´
  ]  ]  / |      [ [   ] ]     { }
  l  L ∫  l      ɺ[ɺ]  l L     ɺ L
    ⌁help⌁   give me the 411
"""

    prompt = "ᐸ/> "
    ruler = "⌁"
    doc_header = "Recorded jive (type help <jargon>):"

    def __init__(self, dependencies):
        super().__init__(dependencies.io)
        self.dependencies = dependencies
        self.char_mngr = dependencies.char_mngr
        self.cmd_mngr = dependencies.cmd_mngr
        self.skill_check = dependencies.skill_check
        self.game_state = "choose_character"

        # Initialize help system
        from ..utils.utils import HelpSystem

        self.help_system = HelpSystem()

        # Initialize AI backend
        self.ai_backends = {"gemini": GeminiBackend(), "ollama": OllamaBackend()}
        self.ai_backend = self.select_available_backend()

    def get_names(self):
        """Override to filter commands based on game state"""
        if self.game_state == "grappling":
            # Only allow specific commands in grapple mode
            return ["do_choke", "do_throw", "do_go", "do_look", "do_release", "do_help", "do_quit", "do_say"]
            
        if self.game_state == "choose_character":
             # Initial State: Restrict to basics
             return ["do_choose", "do_load", "do_reset", "do_help", "do_quit", "do_protocol", "do_shell"]
            # Added do_say for talking.
        
        # Default behavior: return all available commands
        return dir(self)

    async def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        await self.dependencies.story_manager.update()
        return stop

    def select_available_backend(self):
        """Auto-select the first available backend"""
        try:
            name, backend = next(
                (name, backend)
                for name, backend in self.ai_backends.items()
                if backend.is_available()
            )
            logging.info(f"Using {name} AI backend")
            return backend
        except StopIteration:
            raise RuntimeError("No AI backend available")

    async def do_protocol(self, arg):
        """Switch between available AI backends (gemini/ollama) or config."""
        if arg not in self.ai_backends:
            await self.io.send(f"Available backends: {', '.join(self.ai_backends.keys())}")
            return

        backend = self.ai_backends[arg]
        if not backend.is_available():
            await self.io.send(f"{arg} backend is not available")
            return

        self.ai_backend = backend
        await self.io.send(f"Switched to {arg} backend")

    def complete_protocol(self, text, line, begidx, endidx):
        """Complete AI backend options"""
        available_backends = list(self.ai_backends.keys())  # ['gemini', 'ollama']
        logging.debug(f"Available AI backends: {available_backends}")
        return [
            backend + " " for backend in available_backends if backend.startswith(text)
        ]

    async def do_talk(self, arg):
        "Start a conversation with an NPC"
        if not self.char_mngr.player:
            await self.io.send("You are a disembodied soul. You have no voice to speak with.")
            return

        player_name = self.char_mngr.player.handle
        npc_name = "Judy"
        # Construct Player Profile for the AI
        player = self.char_mngr.player
        soul = player.digital_soul

        # Format Big 5 for context
        b5 = soul.big5
        personality_profile = (
            f"Openness: {b5.openness}/100, "
            f"Conscientiousness: {b5.conscientiousness}/100, "
            f"Extraversion: {b5.extraversion}/100, "
            f"Agreeableness: {b5.agreeableness}/100, "
            f"Neuroticism: {b5.neuroticism}/100"
        )

        traits_str = ", ".join(soul.traits) if soul.traits else "None"

        # Check if NPC is in current location
        current_location = self.dependencies.world.player_position
        present_npcs = [
            npc.handle.lower()
            for npc in self.dependencies.npc_manager.get_npcs_in_location(
                current_location
            )
        ]

        target_npc = None
        # Handle "talk lazlo" vs "talk" (ambiguous)
        if not arg and len(present_npcs) == 1:
            target_name = present_npcs[0]
            target_npc = self.dependencies.npc_manager.get_npc(target_name)
        elif arg:
            target_name = arg.lower()
            target_npc = self.dependencies.npc_manager.get_npc(target_name)
            if target_npc and target_npc.location != current_location:
                await self.io.send(f"You don't see {target_npc.handle} here.")
                return
            if not target_npc:
                # Check if it's a generic NPC provided by the world description?
                # For now, only support named NPCs
                await self.io.send(f"Who is '{arg}'? You're talking to ghosts, choom.")
                return
        else:
            if not present_npcs:
                await self.io.send("There's no one here to talk to.")
            else:
                await self.io.send(
                    f"Who do you want to talk to? (Visible: {', '.join(present_npcs)})"
                )
            return

        npc_name = target_npc.handle
        npc_role = target_npc.role
        npc_context = target_npc.dialogue_context

        npc_context = target_npc.dialogue_context

        # Switch to Conversation State
        if self.game_state != "conversation":
            self.original_prompt = self.prompt

        self.game_state = "conversation"
        self.conversing_npc = target_npc
        self.prompt = f"\033[1;32mYou -> {npc_name} > \033[0m"

        # Fan Check for Header
        rel_tag = ""
        status = target_npc.relationships.get(player_name)
        if status and status.lower() == "fan":
             rel_tag = " \033[1;36m[ FAN ]\033[0m"

        print(
            f"\n\033[1;35m[ Entering conversation with {npc_name}{rel_tag}\033[1;35m. Type 'bye' to exit. ]\033[0m"
        )

        # If user provided an argument (e.g. "talk lazlo hello"), treat it as the first message
        if arg and arg.lower() != target_name.lower():
            # If arg is just 'lazlo', we do nothing.
            if not arg.lower().startswith(target_name.lower()):
                self.do_say(arg)
            elif len(arg) > len(target_name):
                msg = arg[len(target_name) :].strip()
                if msg:
                    self.do_say(msg)
        return



    def complete_look(self, text, line, begidx, endidx):
        """Complete look command with visible NPC names"""
        current_location = self.dependencies.world.player_position
        visible_npcs = self.dependencies.npc_manager.get_npcs_in_location(
            current_location
        )
        # Deduplicate by name
        present_names = list({npc.handle for npc in visible_npcs})

        if not text:
            return [name + " " for name in present_names]
        return [
            name + " " for name in present_names if name.lower().startswith(text.lower())
        ]



    async def do_go(self, arg):
        """Move to a new location. If grappling, drags the target."""
        if self.game_state == "grappling" and hasattr(self, "grapple_shell"):
             await self.grapple_shell.do_go(arg)
             return

        # Normal Movement
        await self.dependencies.world.do_go(arg)

    def complete_go(self, text, line, begidx, endidx):
        """Complete go command with available exits"""
        current_location = self.dependencies.world.locations[
            self.dependencies.world.player_position
        ]
        exits = list(current_location.get("exits", {}).keys())
        if not text:
            return [e + " " for e in exits]
        return [direction + " " for direction in exits if direction.startswith(text)]

    def complete_talk(self, text, line, begidx, endidx):
        """Complete talk command with visible NPC names"""
        current_location = self.dependencies.world.player_position
        present_npcs = [
            npc.handle
            for npc in self.dependencies.npc_manager.get_npcs_in_location(
                current_location
            )
        ]
        if not text:
            return [n + " " for n in present_npcs]
        return [
            name + " " for name in present_npcs if name.lower().startswith(text.lower())
        ]


    async def do_reset(self, arg):
        """
        Delete your save file to start fresh.
        Usage: reset <handle>
        """
        if not arg:
            await self.io.send("Reset whom? (Usage: reset <handle>)")
            return
            
        db = self.dependencies.world.db
        if db.delete_player(arg):
             await self.io.send(f"\033[1;33m[SYSTEM] Save file for '{arg}' deleted. You are now a blank slate.\033[0m")
        else:
             await self.io.send(f"No active save file found for '{arg}'.")

    async def do_choose(self, arg=None):
        """Allows the player to choose a character by Handle."""
        allowed_names = self.char_mngr.character_names()

        # Parse Handle if input is "Handle (Role)"
        if "(" in arg:
            arg_handle = arg.split("(")[0].strip()
        else:
            arg_handle = arg.strip()

        arg_lower = arg_handle.lower() if arg_handle else ""

        # Use partial name matching for the input check if strict match fails?
        # But we want strict matching for the final selection.
        # Let's extract handles from the allowed_names which are now "Handle (Role)"
        allowed_handles = [name.split(" (")[0].lower() for name in allowed_names]

        if arg_lower not in allowed_handles:
            # Fallback or help
            characters_list = self.char_mngr.character_names()
            self.columnize(characters_list, displaywidth=80)
            await self.io.send(f"To pick yo' ride chummer, type 'choose <handle>'.")
            return

        self.prompt = f"{arg_handle} {ActionManager.prompt}"

        # Set player character (Match Handle)
        selected_char = next(
            c
            for c in self.char_mngr.characters.values()
            if c.handle.lower() == arg_lower
        )

        if selected_char:
             # --- 3. Save/Load Check ---
             db = self.dependencies.world.db
             saved_state = db.load_player(selected_char.handle)
             
             if saved_state:
                 # RESUME GAME
                 await self.io.send(f"\n\033[1;32m[SYSTEM] Signal re-acquired. Resuming session for {selected_char.handle}...\033[0m")
                 
                 # Restore Location
                 if saved_state['location_id']:
                     self.dependencies.world.player_position = saved_state['location_id']
                 
                 # Restore Items (Resolve IDs -> Dicts/Objects)
                 # Note: Currently Items are Dicts in Inventory. DatabaseManager.get_item returns Dict.
                 inv_ids = json.loads(saved_state['inventory_ids']) if saved_state['inventory_ids'] else []
                 equip_ids = json.loads(saved_state['equipped_ids']) if saved_state['equipped_ids'] else []
                 
                 inv_items = []
                 for i_id in inv_ids:
                     item = db.get_item(i_id)
                     if item: inv_items.append(item)
                     
                 equip_items = []
                 for i_id in equip_ids:
                     item = db.get_item(i_id)
                     if item: equip_items.append(item)
                 
                 # PARSE STATS
                 # Handle the new "attributes" + "combat" structure
                 stats_payload = {}
                 raw_stats = saved_state['stats']
                 if isinstance(raw_stats, str):
                     try:
                        stats_payload = json.loads(raw_stats)
                     except:
                        pass
                 elif isinstance(raw_stats, dict):
                     stats_payload = raw_stats
                     
                 # Pass the Full Payload to restore_state
                 selected_char.restore_state(stats_payload, inv_items, equip_items)
                 
                 self.char_mngr.set_player(selected_char)
                 self.game_state = "active_game" # Skip Intro
                 
                 # Show Look immediately
                 await self.do_look("")
                 
             else:
                 # NEW GAME (Intro)
                 self.char_mngr.set_player(selected_char)
                 await self.io.send(f"\nLocked and loaded. You are now {selected_char.handle}.")
                 
                 # Initialize NPCs
                 # Append unselected PCs to the NPC list so they exist in the world (Future Multiplayer)
                 unselected_pcs = [
                    c
                    for c in self.char_mngr.characters.values()
                    if c.char_id != selected_char.char_id
                 ]
                 self.char_mngr.npcs.extend(unselected_pcs)
                 
                 # Spawn Intro Item (The Glitching Burner)
                 # We need to guarantee it exists for the "Take" interaction
                 db = self.dependencies.world.db
                 start_loc = self.dependencies.world.player_position
                 
                 # 1. Spawn Intro Burner (Ensure ALL characters have one in INVENTORY)
                 # Check if they already have it (loadout)
                 has_burner = False
                 for item in selected_char.inventory:
                     name = item.get('name') if isinstance(item, dict) else item
                     if "glitching burner" in name.lower():
                         has_burner = True
                         break
                 
                 if not has_burner:
                      # Create and Add to Inventory
                      burner_tid = db.get_template_id_by_name("Glitching Burner")
                      if not burner_tid:
                          burner_tid = db.create_template("Glitching Burner", "gear", "A cheap burner phone, screen cracked and glitching.")
                      
                      if burner_tid:
                          # Create instance owned by player
                          iid = db.create_instance(burner_tid, owner_id=selected_char.handle)
                          # Add to inventory list so it's usable immediately
                          selected_char.inventory.append({"name": "Glitching Burner", "id": iid})
                 
                 # 2. Persist Player Starting Gear
                 new_inv = []
                 for item in selected_char.inventory:
                     name = item.get('name') if isinstance(item, dict) else item
                     # Check/Create Template
                     tid = db.get_template_id_by_name(name)
                     if not tid:
                         desc = item.get('notes', 'Standard gear.')
                         tid = db.create_template(name, "gear", desc)
                     
                     iid = db.create_instance(tid, owner_id=selected_char.handle)
                     
                     if isinstance(item, dict):
                         item['id'] = iid
                     else:
                         item = {"name": item, "id": iid}
                     new_inv.append(item)
                 selected_char.inventory = new_inv

                 new_weapons = []
                 for item in selected_char.weapons:
                     name = item.get('name') if isinstance(item, dict) else item
                     tid = db.get_template_id_by_name(name)
                     if not tid:
                         desc = item.get('notes', 'Weapon.')
                         desc = item.get('notes', 'Weapon.')
                         # Try to parse stats from json if possible or default
                         # CAPTURE ALL STATS (Ammo, ROF, Dmg)
                         stats = {}
                         # specific keys to migrate to base_stats
                         for key in ['dmg', 'damage', 'ammo', 'rof', 'range', 'cost']:
                             if key in item: stats[key] = item[key]
                             
                         tid = db.create_template(name, "weapon", desc, base_stats=json.dumps(stats))
                     
                     iid = db.create_instance(tid, owner_id=selected_char.handle)
                     if isinstance(item, dict):
                         item['id'] = iid
                     else:
                         item = {"name": item, "id": iid}
                     new_weapons.append(item)
                 selected_char.weapons = new_weapons

                 
                 # Set State to 'character_chosen' 
                 # This state is special: Logic in 'do_look' used to trap it, but we removed that trap.
                 # We simply want normal game behavior with an intro flavor.
                 self.game_state = "character_chosen" 
                 
                 # 1. Trigger the first look (Intro Visuals + System Msg)
                 await self.do_look("")

                 # 2. Trigger Story (Phone Call - Prints AFTER Visuals)
                 await self.dependencies.story_manager.start_story("phone_call")


    async def do_save(self, arg):
        """Manually save your progress."""
        player = self.char_mngr.player
        if not player:
            await self.io.send("No character loaded to save.")
            return
            
        # Serialize - NOW SAVING FULL STATS (Attributes + Combat)
        data = player.to_dict()
        
        # Old Format (Buggy): data['stats'] (just attributes)
        # New Format: { "attributes": {...}, "combat": {...} }
        full_stats = {
            "attributes": data['stats'], # Strength, Ref, etc.
            "combat": data['combat']     # HP, SP, etc.
        }
        
        loc = self.dependencies.world.player_position
        
        success = self.dependencies.world.db.save_player(
            player.handle,
            loc,
            full_stats, # Pass Dict, DatabaseManager.save_player handles json.dumps in this project version
            data['inventory_ids'],
            data['equipped_ids']
        )
        
        # 2. Persist Item States (Mutable Stats like Ammo)
        # We must iterate over the player's actual item objects and update the DB instances
        all_items = player.inventory + player.weapons
        for item in all_items:
            if isinstance(item, dict) and 'id' in item:
                # Filter out non-stat keys for the stats payload if we want cleanliness, 
                # or just dump the difference.
                # Ideally, we save everything that isn't ID/Name/Desc?
                # For simplicity, we save the whole dict as current_stats, 
                # or just specific mutable fields.
                # Let's save the whole mutable dict to ensure we capture ammo/notes changes.
                # But we should exclude ID/Name if they are redundant? No, JSON is flexible.
                self.dependencies.world.db.update_instance_stats(item['id'], item)
        
        if success:
            await self.io.send("\033[1;32m[SYSTEM] Progress Saved.\033[0m")
        else:
            await self.io.send("\033[1;31m[ERROR] Save Failed.\033[0m")

    async def do_load(self, arg):
        """
        Load a saved game.
        Usage: load <handle>
        """
        if not arg:
            await self.io.send("Load which character? (Use 'load <handle>')")
            return
            
        # Strict Check: Must exist in DB
        db = self.dependencies.world.db
        if not db.load_player(arg):
             await self.io.send(f"No save file found for '{arg}'. Use 'choose {arg}' to start a new game.")
             return

        await self.do_choose(arg)


    def complete_choose(self, text, line, begidx, endidx):
        """Complete character handles after 'choose' command"""
        # Ensure we call character_names without args if it doesn't support them
        # And filter manually + append space
        names = self.char_mngr.character_names()
        return [n + " " for n in names if n.lower().startswith(text.lower())]

    def complete_load(self, text, line, begidx, endidx):
        """Complete ONLY saved handles"""
        saved = self.dependencies.world.db.get_all_saved_handles()
        return [n + " " for n in saved if n.lower().startswith(text.lower())]

    async def start_game(self):
        """
        Clears the terminal screen and starts the Cyberpunk RPG game.
        This method clears the terminal screen using the `os.system("clear")`
        command, sets the command prompt for the game to the value of the
        `prompt` class variable, and starts the command-line interface using
        the `cmdloop()` method of the `cmd.Cmd()` class.

        Returns:
            None
        """
        # Clear screen
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        self.prompt = (
            f"What's the deal, choomba? Give me the word:\n" f"{ActionManager.prompt}"
        )

        # Start the loop
        await self.cmdloop()

    def completenames(self, text, *ignored):
        """Handle command completion including character roles"""
        logging.debug(
            f"completenames called with: text='{text}', state={self.game_state}"
        )

        # 1. Get ALL valid completions from parent (already filtered by text matching)
        #    These come with trailing spaces e.g. "choose ", "help "
        candidates = super().completenames(text, *ignored)

        # 2. Define whitelist of allowed commands based on state
        allowed = {"help", "quit"} # Always allowed

        if self.game_state == "choose_character":
            allowed.add("choose")

        if self.game_state in ["character_chosen", "active_game", "before_perception_check"]:
            allowed.update({"use_object", "look", "gear", "whoami", "take", "drop", "save", "load", "reset", "quit", "help", "talk", "inventory"})

        # elif self.game_state == "grappling" and hasattr(self, "grappled_target"):
        #     pass # Incorrectly returning string here caused tab completion bug
        elif self.game_state == "conversation":
            allowed.update({"say", "bye", "take", "inventory", "look", "talk"})

        elif self.game_state == "grappling":
            allowed.update({"choke", "throw", "look", "release"})
            # Hide move, go, take, etc.

        filtered_cmds = [c for c in candidates if c.strip() in allowed]
        
        logging.debug(f"Filtered commands for state {self.game_state}: {filtered_cmds}")
        return filtered_cmds


    def complete_take(self, text, line, begidx, endidx):
        """Autocomplete for take command (Inventory + Ground)"""
        if not self.char_mngr.player:
            return []
        
        items = []
        # 1. Inventory items (for Draw)
        for item in self.char_mngr.player.inventory:
            name = item.get('name') if isinstance(item, dict) else item
            items.append(name)

        # 2. Ground Items (for Pickup)
        if self.dependencies and self.dependencies.world:
            loc = self.dependencies.world.player_position
            ground_items = self.dependencies.world.get_items_in_location(loc)
            for item in ground_items:
                 name = item.get('name') if isinstance(item, dict) else item
                 items.append(name)
            
            # Special Case: Intro Item (Virtual)
            if self.game_state == "character_chosen":
                items.append("Glitching Burner")

        return [i for i in items if i.lower().startswith(text.lower())]

    def complete_drop(self, text, line, begidx, endidx):
        """Autocomplete for drop command (Inventory + Hand)"""
        if not self.char_mngr.player:
            return []
            
        items = []
        # Hand
        for w in self.char_mngr.player.weapons:
            items.append(w.get('name'))
        # Inventory
        for item in self.char_mngr.player.inventory:
             name = item.get('name') if isinstance(item, dict) else item
             items.append(name)
             
        return [i for i in items if i.lower().startswith(text.lower())]

    def complete_use_object(self, text, line, begidx, endidx):
        """Autocomplete for use_object (Equipped weapons to stow AND items to interact with)"""
        items = []

        # 1. Contextual Items (State-Specific)
        if self.game_state == "character_chosen":
            items.extend(["Glitching Burner"])

        if not self.char_mngr.player:
             return [i for i in items if i.lower().startswith(text.lower())]
            
        # 2. Equipped Weapons (to stow)
        for w in self.char_mngr.player.weapons:
            items.append(w['name'])

        # 3. Inventory Items (to equip/hold)
        if self.char_mngr.player.inventory:
            for item in self.char_mngr.player.inventory:
                name = item.get('name') if isinstance(item, dict) else item
                items.append(name)
            
        return [i for i in items if i.lower().startswith(text.lower())]

    def complete_grab(self, text, line, begidx, endidx):
        """Autocomplete for grab (NPCs or Items)"""
        # Suggest NPCs primarily
        if not self.dependencies or not self.dependencies.npc_manager:
            return []
            
        # Get NPCs in current location
        loc = self.dependencies.world.player_position
        npcs = [n.handle for n in self.dependencies.npc_manager.get_npcs_in_location(loc)]
        candidates = list(npcs)
        
        # Add Contextual Quest Items (Hardcoded for hint visibility)
        if "lenard" in [n.lower() for n in candidates]:
            candidates.extend(["Briefcase"])
            
        return [c for c in candidates if c.lower().startswith(text.lower())]

    async def _display_rap_sheet(self, arg):
        """Internal method to display rap sheet"""
        # data = self.char_mngr.do_rap_sheet(arg) # Calling do_rap_sheet which is sync but now returns string
        # We can just call it directly as it's just data processing + return string
        rap_sheet = self.char_mngr.do_rap_sheet(arg)
        await self.io.send(rap_sheet)

    async def _display_player_sheet(self, arg):
        """Internal method to display character sheet"""
        data = self.char_mngr.get_character_sheet_data()
        await self.io.display(data, view_type="character_sheet")





    async def do_use_skill(self, arg):
        """Perform a skill check or a combat action."""
        # Check if command is allowed in current game state
        allowed_states = ["before_perception_check", "conversation"]
        if self.game_state not in allowed_states:
            await self.io.send("That command isn't available right now, choomba.")
            return

        if not self.skill_check:
            await self.io.send("Skill check system not initialized!")
            return

        # Parse argument: skill_name [target_name]
        parts = arg.strip().split(maxsplit=1)
        skill_name = parts[0].lower() if parts else ""
        target_name = parts[1] if len(parts) > 1 else None

        if skill_name == "brawling":
            if not target_name:
                await self.io.send("Brawl with who? yourself? Provide a target.")
                return
            
            # Resolve target to NPC object
            if self.dependencies.npc_manager:
                 target_npc = self.dependencies.npc_manager.get_npc(target_name)
                 
                 # Fallback: Check CharacterManager's NPCs
                 if not target_npc:
                     target_npc = self.char_mngr.get_npc(target_name)

                 if not target_npc:
                     await self.io.send(f"You don't see '{target_name}' here to brawl with.")
                     return
            else:
                 await self.io.send("Error: NPC Manager not available.")
                 return

            # Execute 2 Attacks (ROF 2) immediately
            player = self.char_mngr.player
            await self.io.send(f"\n\033[1;31m[COMBAT] {player.handle} attempts to BRAWL (ROF 2) with {target_npc.handle}!\033[0m")
            
            for i in range(2):
                await self.io.send(f"\033[1;33m--- Attack {i+1} ---\033[0m")
                # Suppress internal prints of roll_check
                check_data = player.roll_check(target_npc, "brawling", "evasion", verbose=False)
                
                # Manually Print Summary
                att_total = check_data["att_total"]
                def_total = check_data["def_total"]
                details = check_data.get("details", {})
                att_roll = details.get("att_roll", "?")
                att_crit = details.get("att_crit")
                def_crit = details.get("def_crit")
                
                roll_msg = f"Roll: {att_total} (Dice: {att_roll}"
                if att_crit:
                    roll_msg += f" [{att_crit}]"
                roll_msg += f") vs Def: {def_total}"
                if def_crit:
                    roll_msg += f" [{def_crit}]"
                
                await self.io.send(roll_msg)
                
                if check_data["result"] == "success":
                     # Apply Damage based on Body Stat
                     # Body 0-4: 1d6, 5-6: 2d6, 7-10: 3d6, 11+: 4d6
                     body = player.stats.get("body", 5)
                     dmg_dice = 1
                     if body >= 11: dmg_dice = 4
                     elif body >= 7: dmg_dice = 3
                     elif body >= 5: dmg_dice = 2
                     
                     dmg = 0
                     dice_rolls = []
                     for _ in range(dmg_dice):
                         r = random.randint(1, 6)
                         dmg += r
                         dice_rolls.append(r)
                         
                     # Suppress internal prints of take_damage, we handle output
                     taken = target_npc.take_damage(dmg, ignore_armor=False, verbose=False)
                     
                     dmg_str = f"{dmg} (Rolls: {dice_rolls})" if len(dice_rolls) > 1 else f"{dmg} (Roll: {dice_rolls[0]})"

                     if taken == 0:
                         await self.io.send(f"\033[1;32mHIT! Damage: {dmg_str} -> Absorbed by Armor (SP {target_npc.defence.get('sp', 0)})\033[0m")
                     else:
                         await self.io.send(f"\033[1;32mHIT! Damage: {dmg_str} -> Taken: {taken}\033[0m")
                else:
                     await self.io.send("\033[1;30mMISS!\033[0m")
                     
            return

        # Fallback to standard skill check for other skills
        # NOTE: self.skill_check.do_use_skill might use print(). We haven't refactored SkillCheckCommand yet.
        # This is a risk. SkillCheckCommand needs refactor or I/O injection.
        # Assuming for now it's okay or we'll wrap output capability later.
        # But 'result' is just return value.
        result = self.skill_check.do_use_skill(skill_name, target_name)
        
        # Handle Quest Trigger
        if result == "ambush_trigger":
            self._trigger_ambush()



    def complete_use_skill(self, text, line, begidx, endidx):
        """Complete skill names AND targets for use_skill command"""
        # Update allowed states to match do_use_skill
        if (
            self.game_state not in ["before_perception_check", "conversation"]
            or not self.char_mngr.player
        ):
            return []

        args = line.split()

        # Determine completion context
        completing_target = False
        if len(args) > 2:
            completing_target = True
        elif len(args) == 2 and line.endswith(" "):
            completing_target = True

        if completing_target:
            # Completing Target (NPCs in location)
            loc = self.dependencies.world.player_position
            npcs = self.dependencies.npc_manager.get_npcs_in_location(loc)
            candidates = [npc.handle for npc in npcs]
            return [
                name + " "
                for name in candidates
                if name.lower().startswith(text.lower())
            ]
        else:
            # Completing Skill
            skills = self.char_mngr.player.get_skills()
            return [skill + " " for skill in skills if skill.startswith(text)]

    def do_shell(self, arg):
        """Shell commands can be added here prefixed with !"""
        os.system("cls" if os.name == "nt" else "clear")

    async def default(self, line):
        # Command doesn't exist at all
        if self.game_state == "conversation":
            await self.do_say(line)
            return

        if line.startswith("go "):
            # Handle 'go' command directly
            direction = line.split(" ")[1]
            await self.do_go(direction)
        else:
            await self.io.send(
                "WTF dat mean, ain't no command like dat. Jack in 'help or '?' for the 411 on the specs, omae"
            )

    async def do_look(self, arg):
        """Look around at your current location"""
        if self.game_state == "grappling" and hasattr(self, "grapple_shell"):
             await self.grapple_shell.do_look(arg)
             return

        if self.game_state == "choose_character":
             # "Soul View" - Idea A (The Network)
             await self.io.send(
                 "\n\033[1;36m[ SIGNAL TRACE: ACTIVE ]\033[0m"
                 "\nYou are adrift in the Dark Fiber. Streams of data rush past like neon highways."
                 "\nThree distinct signal signatures pulse nearby... (The Hosts)."
                 "\nRipples of 'V' (Valerie/Vincent) echo in the static, but you need a solid connection."
             )
             return

        if self.game_state == "character_chosen":
             # Intro Sequence Visuals (One Time Only)
             await self.io.send("\n[SYSTEM]: Connection Established.")
             
             # Fall through to standard World Look to show ASCII art and items
             await self.dependencies.world.do_look(arg)
             
             # Transition state so this doesn't repeat
             self.game_state = "active_game"
             return

        # General "Active Game" Look (includes "before_perception_check")
        # We fall through for any state that just needs standard world looking.
        
        # Standard World Look
        await self.dependencies.world.do_look(arg)
        
        # Post-Look Hooks (Reminders)
        if self.dependencies.story_manager.current_story and self.dependencies.story_manager.current_story.name == "phone_call":
             if getattr(self.dependencies.story_manager.current_story, "state") == "ringing":
                 # Check where the phone is
                 has_burner = False
                 for item in self.char_mngr.player.inventory:
                     name = item.get('name', '') if isinstance(item, dict) else item
                     if "glitching burner" in name.lower(): has_burner = True
                 
                 # Also checks weapons/equipped?
                 
                 if has_burner:
                     await self.io.send("\n\033[1;33m[!] REMINDER:\033[0m Your pocket vibrates violently. (Type 'use burner' to answer)")
                 else:
                     # Check ground
                     ground_burner = False
                     loc = self.dependencies.world.player_position
                     items = self.dependencies.world.get_items_in_location(loc)
                     for item in items:
                         name = item.get('name', '') if isinstance(item, dict) else item
                         if "glitching burner" in name.lower(): ground_burner = True
                     
                     if ground_burner:
                         await self.io.send("\n\033[1;33m[!] REMINDER:\033[0m A \033[1;31mGlitching Burner\033[0m on the ground vibrates violently. (Type 'take burner' then 'use burner')")
                     else:
                         # Far away? Or lost?
                         await self.io.send("\n\033[1;33m[!] REMINDER:\033[0m You hear a faint electronic buzzing from somewhere nearby...")
        return




    async def log_event(self, event):
        """Log an event to the player's recent_events buffer and trigger passive thoughts"""
        if self.char_mngr.player and self.char_mngr.player.digital_soul:
            self.char_mngr.player.digital_soul.recent_events.append(event)
            # Add some stress for any event (placeholder mechanic)
            self.char_mngr.player.digital_soul.stress = min(
                100, self.char_mngr.player.digital_soul.stress + 5
            )
            # Notify User
            await self.io.send(f"\033[3;90m[!] Event Recorded: {event} (Drafted for Reflection)\033[0m")

            # Passive "Intrusive Thoughts" (Chance to trigger)
            # Only trigger random thoughts if stress is building up or event is significant
            if random.random() < 0.4:  # 40% chance
                await self._trigger_intrusive_thought(event) # Await it!

    async def _trigger_intrusive_thought(self, event):
        """Generates and displays a passive intrusive thought"""
        try:
            player = self.char_mngr.player
            soul = player.digital_soul

            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are the inner consciousness of {player.handle} ({player.role}). "
                        f"Current Stress: {soul.stress}%. Traits: {soul.traits}. "
                        "Generate a SINGLE, short, gritty intrusive thought about the recent event. "
                        "It should reflect your internal conflict or reaction. "
                        "Max 15 words. No quotes."
                    ),
                },
                {"role": "user", "content": f"Event: {event}"},
            ]
            # Use a quick call if possible, or just standard
            # NOTE: get_chat_completion is sync blocking call.
            response = self.ai_backend.get_chat_completion(messages)
            thought = response["message"]["content"]

            # Print in grey italics
            await self.io.send(f"\033[3;90m{thought}\033[0m")

        except Exception:
            pass  # Fail silently for passive flavor

    async def do_reflect(self, arg):
        """
        Reflect on your recent actions to process stress and evolve your soul.
        Usage: reflect
        """
        player = self.char_mngr.player
        soul = player.digital_soul

        if not soul.recent_events:
            await self.io.send("\n\033[3mYour mind is clear. Nothing pressing to reflect on.\033[0m")
            return

        await self.io.send(f"\n\033[1;30m[ INTERNAL MONOLOGUE INITIATED ]\033[0m")
        await self.io.send(f"\033[3mProcessing {len(soul.recent_events)} recent events...\033[0m")

        # 1. Ask Gemini to generate a probe
        events_str = "; ".join(soul.recent_events)
        probe_messages = [
            {
                "role": "system",
                "content": f"You are the internal monologue of a Cyberpunk Edgerunner ({player.role}). Traits: {soul.traits}.",
            },
            {
                "role": "user",
                "content": (
                    f"Recent Events: {events_str}.\n"
                    "GOAL: Ask the user a Single, Deep, Gritty question about these events to help them process the psychological weight. "
                    "Do not be nice. Be introspective and noir-style."
                ),
            },
        ]

        try:
            probe_response = self.ai_backend.get_chat_completion(probe_messages)
            question = probe_response["message"]["content"]
            await self.io.send(f"\n\033[1;36mSOUL > {question}\033[0m")

            # 2. Get User Reflection (Critical Input Replacement)
            answer = await self.io.prompt("\n\033[1;30mYOU > \033[0m")

            # 3. Analyze and Update
            analyze_messages = [
                {
                    "role": "system",
                    "content": "You are a psychological analyzer for a game character.",
                },
                {
                    "role": "user",
                    "content": (
                        f"User ({player.role}) reflected on events: {events_str}. "
                        f"Their internal monologue asked: {question}. "
                        f"They answered: {answer}. "
                        "GOAL: Analyze this to update their character. "
                        "1. CLASSIFY the connection between User's Nature (Traits/Triads) and Action:"
                        "   - ALIGNMENT: Acting according to nature. EFFECT: Heals Stress."
                        "   - DISSONANCE: Acting against nature. EFFECT: Increases Stress."
                        "2. CLASSIFY the Motivation (The Soul Trilemma):"
                        "   - SENTIMENT (Humanity): Genuine care. Effect: Heals Stress, Light Triad +."
                        "   - NECESSITY (Survival): 'No choice'. Effect: NO stress heal (Numb), LOSS of Agreeableness."
                        "   - TRANSACTIONAL/CYNIC (Masking): 'Fake kindness', 'Used them', 'Annoyed'. Effect: INCREASES Stress (Masking Cost), Dark Triad +, Agreeableness -."
                        "   - RUTHLESSNESS (Power): Cruelty enjoyed. Effect: Heals stress, Dark Triad +."
                        "3. LIGHT TRIAD: Did they show Kantianism (Principles), Humanism (Dignity), or Faith (Hope)? "
                        "Return ONLY a JSON object with keys: "
                        "'stress_change' (int), "
                        "'new_traits' (list[str]), "
                        "'memory_summary' (str), "
                        "'big5_drift' (dict: keys openness, conscientiousness, extraversion, agreeableness, neuroticism. Values +/- int), "
                        "'dark_triad_drift' (dict: keys machiavellianism, narcissism, psychopathy. Values + int), "
                        "'light_triad_drift' (dict: keys kantianism, humanism, faith. Values + int)."
                    ),
                },
            ]

            await self.io.send("\n\033[3m(Re-integrating psyche...)\033[0m")
            try:
                analysis_response = self.ai_backend.get_chat_completion(analyze_messages)
                analysis_text = analysis_response["message"]["content"]
            except Exception as e:
                await self.io.send(f"\n\033[1;31m[ ERROR: Connection to Soul Severed ({e}) ]\033[0m")
                await self.io.send("\033[31mYour thoughts scatter before they can form a coherent pattern.\033[0m")
                self.char_mngr.player.digital_soul.recent_events.clear() # Clear events to unblock queue?
                return

            # Robust JSON extraction
            import re
            json_match = re.search(r"\{.*\}", analysis_text, re.DOTALL)
            if json_match:
                analysis_text = json_match.group(0)
            
            # SANITIZE JSON: Limit AI's creativity with "+" signs (e.g., +1 -> 1) which breaks JSON
            # NOTE: Specific fix for Qwen 32b which tends to output non-compliant JSON integers (e.g. +1)
            analysis_text = re.sub(r':\s*\+(\d+)', r': \1', analysis_text)

            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError as e:
                await self.io.send(f"\033[1;31m(Neural Glitch: {e})\033[0m")
                return

            # Apply Changes
            soul.stress = max(
                0, min(100, soul.stress + analysis.get("stress_change", -10))
            )
            new_traits = analysis.get("new_traits", [])
            for t in new_traits:
                if t not in soul.traits:
                    soul.traits.append(t)
                    await self.io.send(f"\033[1;32m[+] NEW TRAIT ACQUIRED: {t}\033[0m")

            # Apply Big 5 Drift
            b5_drift = analysis.get("big5_drift", {})
            for trait, delta in b5_drift.items():
                if hasattr(soul.big5, trait):
                    current = getattr(soul.big5, trait)
                    new_val = max(0, min(100, current + delta))
                    setattr(soul.big5, trait, new_val)
                    if delta != 0:
                        sign = "+" if delta > 0 else ""
                        await self.io.send(f"\033[3m(Big 5 Shift: {trait.capitalize()} {sign}{delta})\033[0m")

            # Apply Dark Triad Drift
            dt_drift = analysis.get("dark_triad_drift", {})
            # Ensure dark_triad exists (migration handle)
            if not hasattr(soul, 'dark_triad'):
                from .trait_manager import DarkTriad
                soul.dark_triad = DarkTriad()

            for trait, delta in dt_drift.items():
                if hasattr(soul.dark_triad, trait) and delta > 0:
                    current = getattr(soul.dark_triad, trait)
                    new_val = max(0, min(100, current + delta))
                    setattr(soul.dark_triad, trait, new_val)
                    await self.io.send(f"\033[31m(Dark Triad Rise: {trait.capitalize()} +{delta})\033[0m")

            # Apply Light Triad Drift
            lt_drift = analysis.get("light_triad_drift", {})
            if not hasattr(soul, 'light_triad'):
                 from .trait_manager import LightTriad
                 soul.light_triad = LightTriad()

            for trait, delta in lt_drift.items():
                if hasattr(soul.light_triad, trait) and delta > 0:
                     current = getattr(soul.light_triad, trait)
                     new_val = max(0, min(100, current + delta))
                     setattr(soul.light_triad, trait, new_val)
                     await self.io.send(f"\033[1;36m(Light Triad Rise: {trait.capitalize()} +{delta})\033[0m")

            memory = analysis.get("memory_summary")
            if memory:
                soul.memories.append(f"{events_str} -> {memory}")

            # Clear buffer
            soul.recent_events = []
            await self.io.send(f"\033[1;36m[ REFLECTION COMPLETE. STRESS: {soul.stress}% ]\033[0m")

        except Exception as e:
            await self.io.send(f"\nReflection failed: {e}")

    async def do_dev_fan(self, arg):
        """[DEBUG] Make an NPC a Fan of the player. Usage: dev_fan <npc_handle>"""
        npc = self.dependencies.npc_manager.get_npc(arg)
        if npc:
            player_handle = self.char_mngr.player.handle
            npc.relationships[player_handle] = "Fan"
            await self.io.send(f"\033[1;36m[DEBUG] {npc.handle} is now a FAN of {player_handle}!\033[0m")
            await self.io.send(f"Try: 'look {arg}' or 'talk {arg}'")
        else:
             await self.io.send(f"NPC '{arg}' not found.")

    async def do_help(self, arg):
        """Get help for commands - context-sensitive based on game state."""
        if not arg:
            # Show general help introduction based on current state
            help_intro = self.help_system.get_help(state=self.game_state)
            await self.io.send(help_intro)

            # Show available commands
            # Show available commands
            await self.io.send("\nAvailable commands in your current state:")
            commands = self.help_system.get_available_commands(state=self.game_state)
            await self.async_columnize(commands, displaywidth=80)
        else:
            # Show specific command help
            help_text = self.help_system.get_help(arg, self.game_state)
            await self.io.send(help_text)

            # If it's a skill command, show available skills
            if (
                arg == "use_skill"
                and self.game_state == "before_perception_check"
                and self.char_mngr.player
            ):
                await self.io.send("\nAvailable skills:")
                skills = self.char_mngr.player.get_skills()
                await self.async_columnize(skills, displaywidth=80)

    async def do_quit(self, arg):
        """Exits Cyberpunk"""
        await self.io.send(
            "Catch you on the flip side, choombatta. Keep your chrome "
            "polished and your guns loaded, "
            "the neon jungle ain't no walk in the park."
        )
        return True

    def complete_whoami(self, text, line, begidx, endidx):
        """Complete whoami subcommands"""
        subcommands = ["stats", "bio", "soul"]
        return [s + " " for s in subcommands if s.startswith(text)]


    async def do_whoami(self, arg):
        """
        Displays your identity dashboard.
        Usage:
            whoami          -> Dashboard Summary
            whoami stats    -> Full Character Sheet
            whoami bio      -> Rap Sheet (Backstory)
            whoami soul     -> Digital Soul (Traits & Memories)
        """
        if self.game_state == "choose_character":
            await self.io.send("You have no identity yet. Choose a character first.")
            return

        arg = arg.strip().lower()
        player = self.char_mngr.player

        # Default Dashboard View
        if not arg or arg == "dashboard":
            # Header
            await self.io.send(
                f"\n\033[1;36mHID:\033[0m {player.handle} \033[1;36mROLE:\033[0m {player.role}"
            )
            stats = player.stats
            await self.io.send(
                f"\033[1;36mINT:\033[0m {stats.get('int', 0)} | \033[1;36mREF:\033[0m {stats.get('ref', 0)} | \033[1;36mEMP:\033[0m {stats.get('emp', 0)}"
            )
            await self.io.send(f"{'⌁'*60}")

            # Cyber Stress Bar + Brain Icon
            current_stress = player.digital_soul.stress
            max_stress = 100
            fill_len = int(30 * (current_stress / max_stress))
            bar = "█" * fill_len + "░" * (30 - fill_len)
            color = (
                "\033[1;32m"
                if current_stress < 50
                else "\033[1;33m" if current_stress < 80 else "\033[1;31m"
            )
            await self.io.send(f"CYBER STRESS: 🧠 {color}[{bar}] {current_stress}%\033[0m")

            # PENDING REFLECTIONS INDICATOR
            pending = len(player.digital_soul.recent_events)
            if pending > 0:
                await self.io.send(f"\033[1;33m[!] PENDING REFLECTIONS: {pending} (Type 'reflect')\033[0m")
            else:
                await self.io.send(f"\033[1;30m(Mind Clear - No pending reflections)\033[0m")

            # HOST INSTINCT (The fixed trait of the body)
            await self.io.send(f"\n\033[1;35m[ HOST INSTINCT ]\033[0m")
            await self.io.send(f"{player.trait if player.trait else 'Survival'}")

            # DIGITAL SOUL (Your True Self)
            await self.io.send(f"\n\033[1;36m[ TRUE SELF ]\033[0m")
            if player.digital_soul.traits:
                await self.io.send(f"{', '.join(player.digital_soul.traits)}")
            else:
                await self.io.send("(No traits developed yet)")

            # Gear Summary
            inv_count = len(player.inventory)
            await self.io.send(
                f"\n\033[1;33mGEAR:\033[0m {inv_count} item(s) carried. (Use 'gear' to view)"
            )
            return

        if arg == "stats":
            await self._display_player_sheet(None)
            return
        elif arg == "bio":
            await self._display_rap_sheet(None)
            return
        elif arg in ["soul", "mind", "traits"]:
            # Deep Dive into Digital Soul
            soul = player.digital_soul
            await self.io.send(
                f"\n🧠 \033[1;36mDIGITAL SOUL INTERFACE\033[0m: {player.handle} [{player.role}]"
            )
            await self.io.send(f"{'⌁'*60}")

            if hasattr(self, "_ascii_bar_visual"):
                 pass # Use helper if available
            else:
                 # Define helper locally or bind it
                 def _ascii_bar_visual(val):
                     if val == 50: return "\033[1;30m=\033[0m" # Neutral (was '?', changed to '=' for clarity)
                     if val < 30: return "\033[1;31m--\033[0m"
                     if val < 45: return "\033[1;33m-\033[0m"
                     if val <= 55: return "\033[1;30m=\033[0m"
                     if val < 70: return "\033[1;32m+\033[0m"
                     return "\033[1;36m++\033[0m"
                 self._ascii_bar_visual = _ascii_bar_visual

            await self.io.send(f"\n\033[1;35m[ BIG 5 PERSONALITY ]\033[0m")
            b5 = soul.big5
            await self.io.send(f"Openness:          {self._ascii_bar_visual(b5.openness)}")
            await self.io.send(f"Conscientiousness: {self._ascii_bar_visual(b5.conscientiousness)}")
            await self.io.send(f"Extraversion:      {self._ascii_bar_visual(b5.extraversion)}")
            await self.io.send(f"Agreeableness:     {self._ascii_bar_visual(b5.agreeableness)}")
            await self.io.send(f"Neuroticism:       {self._ascii_bar_visual(b5.neuroticism)}")

            # Dark Triad Display
            if hasattr(soul, 'dark_triad') and (soul.dark_triad.machiavellianism > 0 or soul.dark_triad.narcissism > 0 or soul.dark_triad.psychopathy > 0):
                await self.io.send(f"\n\033[1;31m[ DARK TRIAD ]\033[0m")
                dt = soul.dark_triad
                def _dt_visual(val):
                    if val == 0: return "\033[1;30m?\033[0m"
                    if val < 30: return "\033[1;33m+\033[0m"
                    if val < 70: return "\033[1;31m++\033[0m"
                    return "\033[1;31m+++\033[0m" # Extreme
                
                if dt.machiavellianism > 0: await self.io.send(f"Machiavellianism:  {_dt_visual(dt.machiavellianism)}")
                if dt.narcissism > 0:       await self.io.send(f"Narcissism:        {_dt_visual(dt.narcissism)}")
                if dt.psychopathy > 0:      await self.io.send(f"Psychopathy:       {_dt_visual(dt.psychopathy)}")

            # Light Triad Display
            if hasattr(soul, 'light_triad') and (soul.light_triad.kantianism > 0 or soul.light_triad.humanism > 0 or soul.light_triad.faith > 0):
                await self.io.send(f"\n\033[1;36m[ LIGHT TRIAD ]\033[0m")
                lt = soul.light_triad
                def _lt_visual(val):
                     if val == 0: return "\033[1;30m?\033[0m"
                     if val < 30: return "\033[1;34m+\033[0m"
                     if val < 70: return "\033[1;36m++\033[0m"
                     return "\033[1;37m+++\033[0m" # Radiant
                
                if lt.kantianism > 0: await self.io.send(f"Kantianism:        {_lt_visual(lt.kantianism)}")
                if lt.humanism > 0:   await self.io.send(f"Humanism:          {_lt_visual(lt.humanism)}")
                if lt.faith > 0:      await self.io.send(f"Faith in Humanity: {_lt_visual(lt.faith)}")


            await self.io.send(f"\n\033[1;35m[ TRUE SELF ]\033[0m")
            if soul.traits:
                await self.io.send(
                    f"\033[1;35mTRAITS > {', '.join(player.digital_soul.traits)}\033[0m"
                )
            else:
                await self.io.send("(No traits developed yet)")

            await self.io.send(f"\n\033[1;35m[ MEMORY STREAM ]\033[0m")
            if player.digital_soul.memories:
                await self.io.send("\n".join(player.digital_soul.memories) + "\033[0m")
            else:
                await self.io.send("(No memories recorded yet)")
            return

    # Conversation Methods (Re-added)
    async def do_bye(self, arg):
        """End the conversation."""
        if self.game_state == "conversation":
            await self.io.send(f"\033[1;35m[ You step away from the conversation. ]\033[0m")
            self.game_state = "before_perception_check"  # Revert specific state
            if hasattr(self, "original_prompt"):
                self.prompt = self.original_prompt
            if hasattr(self, "conversing_npc"):
                del self.conversing_npc
        else:
            await self.io.send("You aren't talking to anyone.")

    async def do_say(self, arg):
        """Speak to the NPC in conversation"""
        if self.game_state != "conversation" or not self.conversing_npc:
            await self.io.send("You're not talking to anyone.")
            return

        if not arg:
            await self.io.send("Say what?")
            return

        # Player inputs message
        await self.io.send(f"\033[1;32mYou: {arg}\033[0m")

        # Story Hook: Check if current story wants to handle dialogue
        if self.dependencies.story_manager.current_story and hasattr(self.dependencies.story_manager.current_story, 'handle_say'):
             handled = await self.dependencies.story_manager.current_story.handle_say(self.dependencies, arg)
             if handled:
                 return

        # 1. Update Dialogue Context for NPC
        # We need to construct the prompt for the AI
        npc = self.conversing_npc
        player = self.char_mngr.player

        # Basic context construction
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are {npc.handle}, a {npc.role}. "
                    f"Description: {npc.description}. "
                    f"Context: {npc.dialogue_context}. "
                    f"You are talking to {player.handle} ({player.role}). "
                    "Keep responses short (under 2 sentences) and in-character (Cyberpunk slang). "
                    "Do not use quotes."
                ),
            },
            # Role Ability Context Injection
            {
                "role": "system",
                "content": player.role_ability.get_social_context(npc.relationships.get(player.handle))
            },
            # We should ideally keep a history buffer, but for now simple 1-turn
            {"role": "user", "content": arg},
        ]

        try:
            # AI Call
            # NOTE: Sync call!
            response = self.ai_backend.get_chat_completion(messages)
            response_content = response["message"]["content"]

            await self.io.send(f"\033[1;35m{npc.handle}: {response_content}\033[0m")

            # Update stress slightly if conversation is intense? (Simplification)
            # Triggers: Profanity OR Strong Emotion words
            triggers = ["fuck", "kill", "shit", "damn", "love", "help", "sorry", "thanks", "promise", "betray"]
            if any(t in arg.lower() for t in triggers):
                await self.log_event(f"Significant conversation with {npc.handle}: '{arg}'")

        except Exception as e:
            await self.io.send(f"[{npc.handle} glitches out... (AI Error: {e})]")

    # do_take removed as per user request (replaced by skill interactions)



    async def do_take(self, arg):
        """
        Smart Action:
        1. Pick Up: Take an item from the environment (Ground/Container).
        2. Draw: Equip a weapon/item from your inventory.
        Usage: take <item_name>
        """
        if not arg:
            await self.io.send("Take what?")
            return

        player = self.char_mngr.player
        current_loc = self.dependencies.world.player_position
        arg_lower = arg.lower()

        # --- 0. Intro Special: The Burner Phone ---
        # Pick up ONLY (Does not answer)
        if self.game_state == "character_chosen" and ("glitching" in arg_lower or "burner" in arg_lower):
              # Check if already has it (Hand or Inventory) or if it's on the ground
              has_it = False
              for w in player.weapons:
                  if "burner" in w.get('name', '').lower(): has_it = True
              for i in player.inventory:
                  if "burner" in i.get('name', '').lower(): has_it = True
              
              if not has_it:
                   loc = self.dependencies.world.player_position
                   ground_items = self.dependencies.world.get_items_in_location(loc)
                   for i in ground_items:
                       name = i.get('name') if isinstance(i, dict) else i
                       if "burner" in name.lower(): has_it = True

              if has_it:
                   # Fall through to normal Pickup/Draw logic
                   pass
              else:
                  # Intro Pickup: Use DB logic but with custom flavor text
                  # Try to pick it up from the world
                  current_loc = self.dependencies.world.player_position
                  # We use 'glitching burner' as keyword
                  world_item = self.dependencies.world.remove_item(current_loc, "glitching burner")
                  
                  if world_item:
                      player.weapons.append(world_item)
                      await self.io.send("\033[1;32m[+ITEM] You snatch the vibrating Burner Phone.\033[0m")
                      await self.io.send("(It continues to buzz in your hand. Use it to answer.)")
                      return
                  else:
                      # If for some reason it's not there (bug?), fall through
                      pass

        # --- 1. Environment Check (Pick Up) ---
        # Specific Quest Logic: Briefcase
        if "case" in arg_lower:
             present_npcs = [n.handle.lower() for n in self.dependencies.npc_manager.get_npcs_in_location(current_loc)]
             if "lenard" in present_npcs:
                 await self.io.send("\033[1;33mYou reach for the case, but Lenard holds it tight.\033[0m")
                 await self.io.send("(Hint: He's holding it. You assume you'll have to \033[1mgrab\033[0m it from him.)")
                 return

        # Generic Pickup from World
        world_item = self.dependencies.world.remove_item(current_loc, arg)
        if world_item:
            player.inventory.append(world_item)
            name = world_item.get('name') if isinstance(world_item, dict) else world_item
            await self.io.send(f"You pick up the \033[1m{name}\033[0m.")
            return

        # --- 2. Inventory Check (Draw/Equip - Permissive) ---
        found_item = None
        for item in player.inventory:
            name = item.get('name') if isinstance(item, dict) else item
            if arg_lower in name.lower():
                found_item = item
                break
        
        if found_item:
             player.inventory.remove(found_item)
             player.weapons.append(found_item)
             # Verb
             verb = "equip"
             if isinstance(found_item, dict) and 'dmg' not in found_item:
                 verb = "hold"
             await self.io.send(f"You {verb} your \033[1m{found_item.get('name', found_item)}\033[0m.")
             return

        await self.io.send("You don't see that here or in your pack.")

    async def do_answer(self, arg):
        """Answer a ringing phone."""
        # Story Hook for answering phone
        if self.dependencies.story_manager.current_story and self.dependencies.story_manager.current_story.name == "phone_call":
            if getattr(self.dependencies.story_manager.current_story, "state") == "ringing":
                await self.dependencies.story_manager.current_story.handle_answer(self.dependencies)
                # Ensure we reset dialogue context immediately so 'say' works cleanly after
                return
        
        await self.io.send("There is no phone ringing right now.")

    async def do_drop(self, arg):
        """
        Action: Drop an item from your hand or inventory.
        Usage: drop <item_name>
        """
        if not arg:
            await self.io.send("Drop what?")
            return

        arg_lower = arg.lower()
        player = self.char_mngr.player
        dropped_item = None
        source = None

        # 1. Check Weapons (Hand) first
        for w in player.weapons:
            if arg_lower in w.get('name', '').lower():
                dropped_item = w
                source = player.weapons
                break

        # 2. Check Inventory second
        if not dropped_item:
            for item in player.inventory:
                name = item.get('name') if isinstance(item, dict) else item
                if arg_lower in name.lower():
                    dropped_item = item
                    source = player.inventory
                    break
        
        if dropped_item:
            source.remove(dropped_item)
            name = dropped_item.get('name') if isinstance(dropped_item, dict) else dropped_item
            
            # Add to World
            current_loc = self.dependencies.world.player_position
            self.dependencies.world.add_item(current_loc, dropped_item)
            
            await self.io.send(f"You drop the \033[1m{name}\033[0m onto the concrete.")
        else:
            await self.io.send("You don't have that.")

    async def do_stow(self, arg):
        """
        Action: Stow a held item/weapon into your inventory.
        Usage: stow <item_name>
        """
        if not arg:
            await self.io.send("Stow what?")
            return
            
        arg_lower = arg.lower()
        player = self.char_mngr.player
        
        found_weapon = None
        for w in player.weapons:
            if arg_lower in w.get('name', '').lower():
                found_weapon = w
                break
                
        if found_weapon:
            player.weapons.remove(found_weapon)
            player.inventory.append(found_weapon)
            await self.io.send(f"You stow your \033[1m{found_weapon.get('name')}\033[0m back in your gear.")
        else:
             await self.io.send("You aren't holding that.")

    async def do_use_object(self, arg):
        """
        Action: Use/Interact with an object.
        Usage: use_object <target>
        Examples:
            use_object potion   -> Consumes potion.
            use_object switch   -> Flips switch.
        """
        if not arg:
             await self.io.send("Use what object?")
             return
             
        player = self.char_mngr.player
        arg_lower = arg.lower()

        # --- Specific Quest: The Burner Phone ---
        if self.game_state == "character_chosen" and ("glitching" in arg_lower or "burner" in arg_lower or "phone" in arg_lower):
            current_story = self.dependencies.story_manager.current_story
            if current_story and current_story.name == "phone_call":
                 # If we don't have it, take it first (Auto-Take for convenience on Use?)
                 # Or just allow using it from ground.
                 # Let's simple allow Answer.
                 if hasattr(current_story, "handle_answer"):
                     result = await current_story.handle_answer(self.dependencies)
                     if result == "success":
                          self.game_state = "before_perception_check"
                          # Ensure we have it if we used it from ground
                          has_it = False
                          for w in player.weapons:
                              if "burner" in w.get('name','').lower(): has_it = True
                          
                          if not has_it:
                               phone_item = {"name": "Glitching Burner", "type": "tool", "description": "A cheap, vibrating burner phone."}
                               player.weapons.append(phone_item)
                               await self.io.send("(You press the answer key.)")
                     elif result == "already_answered":
                          await self.io.send("You're already on the line.")
                 else:
                     await self.io.send("You pick up the phone.")
            else:
                await self.io.send("The phone isn't ringing right now.")
            return
        
        # --- 1. Hand Check (Use) ---
        found_weapon = None
        for w in player.weapons:
            if arg_lower in w.get('name', '').lower():
                found_weapon = w
                break
                
        if found_weapon:
            # Always Attempt Use (No Stow)
            if "burner" in found_weapon.get('name','').lower():
                 await self.io.send("\033[1;32m[PHONE]\033[0m Signal erratic. No new messages.")
                 return
            
            if isinstance(found_weapon, dict) and found_weapon.get('type') == 'consumable':
                  player.weapons.remove(found_weapon)
                  effect = found_weapon.get('effect', 'refreshing')
                  await self.io.send(f"You use the {found_weapon.get('name')}. It is {effect}.")
                  return
            
            await self.io.send(f"You wave the {found_weapon.get('name')} around.")
            return

        # --- 2. Inventory Check (Use) ---
        found_item = None
        for item in player.inventory:
            name = item.get('name') if isinstance(item, dict) else item
            if arg_lower in name.lower():
                found_item = item
                break
        
        if found_item:
             if isinstance(found_item, dict) and found_item.get('type') == 'consumable':
                 player.inventory.remove(found_item)
                 effect = found_item.get('effect', 'refreshing')
                 await self.io.send(f"You use the {found_item.get('name')}. It is {effect}.")
                 return
             
             # If weapon in inv, use -> equip? 
             # User said "take is take, use is use". 
             # So use_object gun (in inv) -> "You need to take/equip it first."
             await self.io.send(f"You need to take (equip) the {found_item.get('name')} first.")
             return

        # --- 3. Environment Interact ---
        
        # Quest Specific: Briefcase Check
        if "case" in arg_lower or "suitcase" in arg_lower:
             current_loc = self.dependencies.world.player_position
             present_npcs = [n.handle.lower() for n in self.dependencies.npc_manager.get_npcs_in_location(current_loc)]
             if "lenard" in present_npcs:
                 await self.io.send("(Hint: Lenard is holding it. use 'grab'.)")
                 return

        await self.io.send(f"You try to use the {arg}, but nothing happens.")

    async def do_grab(self, arg):
        """
        Action: Grab a target to initiate a Grapple.
        Usage: grab <target>
        """
        if not arg:
            await self.io.send("Grab who?")
            return

        # Parse 'grab item target' vs 'grab target'
        # Heuristic: If 2+ words, check if last word is a valid NPC.
        args = arg.split()
        target_name = arg.strip()
        item_name = None
        
        if len(args) > 1:
            potential_npc = args[-1]
            npc_obj = self.dependencies.npc_manager.get_npc(potential_npc)
            if npc_obj:
                target_name = potential_npc # "Lenard"
                item_name = " ".join(args[:-1]) # "Suitcase" relative to Lenard

        player = self.char_mngr.player

        # --- 0. Item Grab Logic (Briefcase) ---
        # If specifically grabbing 'case' or 'suitcase' (with or without target specified)
        check_item = item_name if item_name else target_name
        if "case" in check_item.lower() or "suitcase" in check_item.lower():
             # Check if Lenard is here map-wise
             current_loc = self.dependencies.world.player_position
             present_npcs = [n.handle.lower() for n in self.dependencies.npc_manager.get_npcs_in_location(current_loc)]
             
             if "lenard" in present_npcs:
                 await self.io.send(f"\033[1;33m[!] You lunge for the briefcase! Lenard shouts!\033[0m")
                 # Trigger Ambush
                 self._trigger_ambush()
                 # Add Briefcase (if successful? _trigger_ambush handles success flow text, but adding item?)
                 # _trigger_ambush text says "The briefcase is yours". So we should add it?
                 # Actually, _trigger_ambush runs combat. If we win, we get it. 
                 # We can add it in _trigger_ambush cleanup or here. 
                 # Let's add it here assuming the flow continues or handled by combat result.
                 # BUT, _trigger_ambush executes combat loop.
                 # We will add it safely.
                 player.inventory.append("Briefcase (Locked)")
                 return
             else:
                 await self.io.send("There's no briefcase to grab here.")
                 return
        
        # 1. Find Target (NPC)
        target_npc = self.dependencies.npc_manager.get_npc(target_name)
        if not target_npc:
             target_npc = self.char_mngr.get_npc(target_name)
        
        if not target_npc or target_npc.location != self.dependencies.world.player_position:
            await self.io.send(f"You don't see '{target_name}' here.")
            return

        # 2. Perform Opposed Check
        await self.io.send(f"\n\033[33mAttempting to GRAB {target_npc.handle}...\033[0m")
        # Rule: Grab uses Brawling vs Brawling (if Defender has it) or Evasion?
        # CP Red: Attacker(DEX+Brawling) vs Defender(DEX+Brawling). If invalid/no brawling, use Evasion?
        # We will check 'brawling' first.
        result = player.roll_check(target_npc, "brawling", "brawling")

        if result["result"] == "success":
            await self.io.send(f"\033[1;32m[SUCCESS] You wrap your arms around {target_npc.handle}! You are now Grappling.\033[0m")
            
            # 3. Enter Grapple State / Shell
            self.game_state = "grappling"
            self.grappled_target = target_npc
            
            # Initialize Grapple Shell
            from ..game_mechanics.combat_shells import GrappleShell
            self.grapple_shell = GrappleShell(self.io, player, target_npc, self)
            
            # Switch Prompt
            self.original_prompt = self.prompt
            self.prompt = self.grapple_shell.prompt
            
            # Note: We don't enter a loop like cmdloop(). We just change state and let ActionManager handle commands.
            # BUT the implementation_plan implies using the Shell class to handle logic.
            # If we want commands like 'choke' to be handled by GrappleShell, we should probably forward them.
            # OR we implement do_choke here and delegate to shell? 
        else:
            await self.io.send(f"\033[1;31m[FAILURE] {target_npc.handle} fends off your grab attempt!\033[0m")
            
    async def do_choke(self, arg):
        if self.game_state == "grappling" and hasattr(self, "grapple_shell"):
             await self.grapple_shell.do_choke(arg)
        else:
             await self.io.send("You aren't grappling anyone.")

    async def do_throw(self, arg):
        if self.game_state == "grappling" and hasattr(self, "grapple_shell"):
             await self.grapple_shell.do_throw(arg)
             # If throw ends grapple, shell should update state or return indicator
             # But shell logic runs commands. We need to sync state.
             # Ideally GrappleShell has a callback or we check state after.
             if self.grapple_shell.grapple_ended:
                  self.game_state = "before_perception_check"
                  if hasattr(self, "original_prompt"):
                      self.prompt = self.original_prompt
                  del self.grappled_target
                  del self.grapple_shell
        else:
             await self.io.send("You aren't grappling anyone.")

    async def do_release(self, arg):
         if self.game_state == "grappling":
             await self.io.send("You release the grapple.")
             self.game_state = "before_perception_check"
             if hasattr(self, "original_prompt"):
                 self.prompt = self.original_prompt
             if hasattr(self, "grappled_target"): del self.grappled_target
             if hasattr(self, "grapple_shell"): del self.grapple_shell
         else:
             await self.io.send("You aren't grappling anyone.")

    def _trigger_ambush(self):
        """Triggers the scripted ambush event."""
        # === TRIGGER AMBUSH ===
        from ..game_mechanics.combat_system import CombatEncounter

        squad = self.dependencies.npc_manager.create_dirty_cop_squad()
        combat = CombatEncounter(self.char_mngr.player, squad)

        # CombatEncounter.start_combat() runs its own loop.
        combat_result = combat.start_combat()

        if combat_result == "dead":
            sys.exit()  # Game Over
        else:
            # Post-Combat Cleanup
            self.game_state = "before_perception_check"
            if hasattr(self, "original_prompt"):
                self.prompt = self.original_prompt
            if hasattr(self, "conversing_npc"):
                del self.conversing_npc

            wprint(
                "\nThe adrenaline fades. The briefcase is yours. Now get it to the Drop Point at the Street Corner."
            )

    def do_deposit(self, arg):
        """Deposit the mission item at the drop point."""
        # 1. Check Location
        if self.dependencies.world.player_position != "street_corner":
            print("To a Drop Box? There isn't one here, choom.")
            return

        # 2. Check Inventory
        player = self.char_mngr.player
        briefcase = "Briefcase (Locked)"
        if briefcase not in player.inventory:
            print("You have nothing to deposit for the contract.")
            return

        # 3. Mission Success Sequence
        player.inventory.remove(briefcase)
        print("\n\033[1;32m[ PROCESSING TRANSACTION... ]\033[0m")
        print(
            "You slide the heavy briefcase into the slot. The machine whirs, scans the biometrics, and chimes."
        )
        print(f"\033[1;33m[ CRITICAL SUCCESS ]\033[0m Contract Fulfilled.")
        print(
            f"\033[1;36m[+] 5000 EDDIES TRANSFERRED TO {player.handle.upper()}'S ACCOUNT\033[0m"
        )
        print(f"\033[1;35m[+] LEGEND REPUTATION INCREASED\033[0m")

        print("\n" + "=" * 50)
        print("       M I S S I O N   C O M P L E T E       ")
        print("=" * 50)

        # End or Continue?
        print("\nYou've survived another night in Night City.")
        print("The game loop is complete. Feel free to explore, or type 'quit'.")
        self.log_event(f"COMPLETED MISSION: Delivered the briefcase. Got Paid.")

    async def do_gear(self, arg):
        """Check your gear and inventory."""
        if not self.char_mngr.player:
            await self.io.send("You have no physical form to carry gear.")
            return
        inv = self.char_mngr.player.inventory
        if not inv:
            await self.io.send("You pockets are empty, choom.")
        else:
            await self.io.send(f"\n\033[1;36m[ GEAR & INVENTORY ]\033[0m")
            for item in inv:
                # Handle both dicts (new format) and strings (legacy/simple items)
                if isinstance(item, dict):
                    display = item.get('name', 'Unknown Item')
                    if 'notes' in item and item['notes']:
                        display += f" ({item['notes']})"
                    # Show stats if it's a weapon (optional, but helpful)
                    if 'dmg' in item:
                         display += f" [DMG: {item['dmg']}]"
                    if 'ammo' in item and item['ammo'] is not None:
                         display += f" [Ammo: {item['ammo']}]"
                    if 'rof' in item:
                         display += f" [ROF: {item['rof']}]"
                    await self.io.send(f"- {display}")
                else:
                    await self.io.send(f"- {item}")
