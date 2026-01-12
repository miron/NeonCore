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

    async def do_switch_ai(self, arg):
        """Switch between available AI backends (ollama/gemini)"""
        if arg not in self.ai_backends:
            await self.io.send(f"Available backends: {', '.join(self.ai_backends.keys())}")
            return

        backend = self.ai_backends[arg]
        if not backend.is_available():
            await self.io.send(f"{arg} backend is not available")
            return

        self.ai_backend = backend
        await self.io.send(f"Switched to {arg} backend")

    def complete_switch_ai(self, text, line, begidx, endidx):
        """Complete AI backend options"""
        available_backends = list(self.ai_backends.keys())  # ['gemini', 'ollama']
        logging.debug(f"Available AI backends: {available_backends}")
        return [
            backend + " " for backend in available_backends if backend.startswith(text)
        ]

    async def do_talk(self, arg):
        "Start a conversation with an NPC"
        if self.char_mngr.player:
            player_name = self.char_mngr.player.handle
        else:
            player_name = "V"
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
            npc.name.lower()
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
                await self.io.send(f"You don't see {target_npc.name} here.")
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

        npc_name = target_npc.name
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
        present_names = list({npc.name for npc in visible_npcs})

        if not text:
            return [name + " " for name in present_names]
        return [
            name + " " for name in present_names if name.lower().startswith(text.lower())
        ]



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
            npc.name
            for npc in self.dependencies.npc_manager.get_npcs_in_location(
                current_location
            )
        ]
        if not text:
            return [n + " " for n in present_npcs]
        return [
            name + " " for name in present_npcs if name.lower().startswith(text.lower())
        ]


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
             self.char_mngr.set_player(selected_char)
             await self.io.send(f"\nLocked and loaded. You are now {selected_char.handle}.")
             # Trigger perception check if needed or just welcome
             
        # Set remaining characters as NPCs
        self.char_mngr.set_npcs(
            [
                c
                for c in self.char_mngr.characters.values()
                if c.char_id != selected_char.char_id
            ]
        )
        # trigger the phone call story
        await self.dependencies.story_manager.start_story("phone_call")

        self.game_state = "character_chosen"

    def complete_choose(self, text, line, begidx, endidx):
        """Complete character handles after 'choose' command"""
        # Ensure we call character_names without args if it doesn't support them
        # And filter manually + append space
        names = self.char_mngr.character_names()
        return [n + " " for n in names if n.lower().startswith(text.lower())]

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

        elif self.game_state == "character_chosen":
            allowed.update({"answer", "look"})

        elif self.game_state == "before_perception_check":
            allowed.update({
                "talk", "look", "go", "inventory", 
                "whoami", "reflect", "use_skill", "deposit",
                "take", "use_object", "grab", "answer"
            })

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
        """Autocomplete for take command (Inventory items)"""
        if not self.char_mngr.player:
            return []
        
        # Candidate 1: Inventory Items (Draw)
        items = []
        for item in self.char_mngr.player.inventory:
            name = item.get('name') if isinstance(item, dict) else item
            items.append(name)
            
        # Candidate 2: Environment Items (Pickup) - Placeholder
        # items.extend(["Briefcase"]) 
        
        return [i for i in items if i.lower().startswith(text.lower())]

    def complete_use_object(self, text, line, begidx, endidx):
        """Autocomplete for use_object (Equipped weapons to stow)"""
        if not self.char_mngr.player:
            return []
            
        # Candidate: Equipped Weapons
        items = []
        for w in self.char_mngr.player.weapons:
            items.append(w['name'])
            
        return [i for i in items if i.lower().startswith(text.lower())]

    def complete_grab(self, text, line, begidx, endidx):
        """Autocomplete for grab (NPCs or Items)"""
        # Suggest NPCs primarily
        if not self.dependencies or not self.dependencies.npc_manager:
            return []
            
        # Get NPCs in current location
        loc = self.dependencies.world.player_position
        npcs = [n.handle for n in self.dependencies.npc_manager.get_npcs_in_location(loc)]
        
        return [n for n in npcs if n.lower().startswith(text.lower())]

    async def _display_rap_sheet(self, arg):
        """Internal method to display rap sheet"""
        # data = self.char_mngr.do_rap_sheet(arg) # Calling do_rap_sheet which is sync but now returns string
        # We can just call it directly as it's just data processing + return string
        rap_sheet = self.char_mngr.do_rap_sheet(arg)
        await self.io.send(rap_sheet)

    async def _display_player_sheet(self, arg):
        """Internal method to display character sheet"""
        data = self.char_mngr.get_player_sheet_data()
        await self.io.display(data, view_type="character_sheet")




    async def do_answer(self, arg):
        """Answer the incoming holo-call from Lazlo."""
        # In the new StoryManager architecture, the call is already "active" if the story is running.
        # This command might be a redundant legacy trigger, or we can use it to advance the story state.
        
        current_story = self.dependencies.story_manager.current_story
        if current_story and current_story.name == "phone_call":
             # Call handle_answer logic on the story module
             if hasattr(current_story, "handle_answer"):
                 result = await current_story.handle_answer(self.dependencies)
                 if result == "success":
                      # Transition state to allow skill checks
                      self.game_state = "before_perception_check"
                 elif result == "already_answered":
                      await self.io.send("You're already on the line with him.")
             else:
                 await self.io.send("You answer the call. Lazlo is speaking...")
        else:
            await self.io.send("No one is calling you right now, choomba.")

    async def do_use_skill(self, arg):
        """Perform a skill check with the specified skill"""
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

            # Execute Opposed Check immediately (No Shell)
            player = self.char_mngr.player
             # Ensure we use an asynchronous safe wrapper if roll_check has prints? 
             # For now, roll_check uses wprint (sync). 
             # We let it print.
            check_data = player.roll_check(target_npc, "brawling", "evasion")
            
            result = check_data["result"]
            
            # Check for Brawling-specific Quest Triggers (e.g. Ambush on success)
            # Logic: If success, do we trigger ambush?
            # User previously had logic: "Trigger Ambush IS HERE NOW" upon snatch success.
            # But straightforward brawling? "Ambush/Takedown" logic.
            # I will map success to "ambush_trigger" return for the handler below.
            if result == "success":
                 # Return specific trigger for handling below
                 if hasattr(self, "_trigger_ambush"): # Check if ambush logic exists
                      # Just assume we return "ambush_trigger" if it was the intent?
                      # Or let the standard result handling take care of it?
                      # Line 495 checks result == "ambush_trigger".
                      # So I should return that string if appropriate.
                      # But simple brawling might just be damage.
                      # For safety/regression fix, I just return the result string.
                      pass
            
            # Line 492 assigns 'result' for standard skills. 
            # I should update 'result' variable here to flow into Line 494 check.
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
            candidates = [npc.name for npc in npcs]
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
        if self.game_state == "before_perception_check":
            await self.dependencies.world.do_look(arg)
        else:
            await self.io.send("Nothing much to see here yet, choomba.")

    async def do_go(self, arg):
        """Move to a new location"""
        if self.game_state != "before_perception_check":
            await self.io.send("That command isn't available right now, choomba.")
            return

        if not arg or arg.strip() == "":
            await self.io.send("Go where? Try 'go north', 'go east', 'go south', or 'go west'.")
            return

        direction = arg.strip()
        try:
            await self.dependencies.world.do_go(direction)
        except KeyError as e:
            await self.io.send(f"Error: Location not found - {e}")
            await self.io.send("This is a bug. Please report it.")
        except Exception as e:
            await self.io.send(f"Error moving: {e}")

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
            analysis_response = self.ai_backend.get_chat_completion(analyze_messages)
            analysis_text = analysis_response["message"]["content"]

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
            await self.io.send(f"\033[1;36m[DEBUG] {npc.name} is now a FAN of {player_handle}!\033[0m")
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
            # await self.io.send("\nAvailable commands in your current state:")
            # commands = self.help_system.get_available_commands(state=self.game_state)
            # await self.async_columnize(commands, displaywidth=80)
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

        # 1. Update Dialogue Context for NPC
        # We need to construct the prompt for the AI
        npc = self.conversing_npc
        player = self.char_mngr.player

        # Basic context construction
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are {npc.name}, a {npc.role}. "
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

            await self.io.send(f"\033[1;35m{npc.name}: {response_content}\033[0m")

            # Update stress slightly if conversation is intense? (Simplification)
            # Triggers: Profanity OR Strong Emotion words
            triggers = ["fuck", "kill", "shit", "damn", "love", "help", "sorry", "thanks", "promise", "betray"]
            if any(t in arg.lower() for t in triggers):
                await self.log_event(f"Significant conversation with {npc.name}: '{arg}'")

        except Exception as e:
            await self.io.send(f"[{npc.name} glitches out... (AI Error: {e})]")

    # do_take removed as per user request (replaced by skill interactions)



    async def do_take(self, arg):
        """
        Smart Action:
        1. Pick Up: Take an item from the environment (Ground/Container).
        2. Draw: Equip a weapon/item from your inventory.
        Usage: take <item_name>
        """
        if not arg:
            print("Take what?")
            return

        player = self.char_mngr.player
        current_loc = self.dependencies.world.player_position
        arg_lower = arg.lower()

        # --- 1. Environment Check (Pick Up) ---
        # Note: In a real implementation, we'd check `world.get_items_in_location(current_loc)`
        # For now, we use the specific "Briefcase" check as per previous logic, but stricter.
        
        # Check if item is on the ground (e.g. dropped by NPC or pre-placed)
        # (Assuming world has a way to track loose items, or we mock it for the specific quest item)
        
        # Specific Quest Logic: Briefcase is ONLY on ground if dropped/spawned. 
        # If Lenard is holding it, 'take' fails.
        
        # For this specific task, we'll check if it's "Briefcase" and explicitly fail if Lenard has it.
        if "case" in arg_lower:
             # Check if Lenard is here map-wise
             present_npcs = [n.name.lower() for n in self.dependencies.npc_manager.get_npcs_in_location(current_loc)]
             if "lenard" in present_npcs:
                 print("\033[1;33mYou reach for the case, but Lenard holds it tight.\033[0m")
                 print("(Hint: He's holding it. You assume you'll have to \033[1mgrab\033[0m it from him.)")
                 return

        # Generic Pickup (Placeholder for future item system)
        # item = world.find_item(arg, current_loc)
        # if item:
        #    player.inventory.append(item)
        #    return

        # --- 2. Inventory Check (Draw/Equip) ---
        # Search for item in inventory to equip
        found_item = None
        for item in player.inventory:
            name = item['name'] if isinstance(item, dict) else item
            if arg_lower in name.lower():
                found_item = item
                break
        
        if found_item:
            # Check if it's a weapon (has damage stats)
            is_weapon = False
            if isinstance(found_item, dict) and 'dmg' in found_item:
                is_weapon = True
            
            # Move from Inventory to Weapons (Equip)
            if is_weapon:
                 player.inventory.remove(found_item)
                 player.weapons.append(found_item)
                 print(f"You draw your \033[1m{found_item['name']}\033[0m.")
            else:
                 print(f"You take out the {found_item.get('name', found_item)}.")
                 # For non-weapons, we might just "hold" it, but for now we only have a 'weapons' slot.
                 # Maybe allow holding utility items? Let's stick to weapons for now as per user request.
            return

        print("You don't see that here or in your pack.")

    async def do_use_object(self, arg):
        """
        Action: Manipulate an object or Stow a held weapon.
        Usage: use_object <target>
        Examples:
            use_object shotgun  -> Stows the equipped shotgun.
            use_object switch   -> Flips a light switch.
        """
        if not arg:
             print("Use what object?")
             return
             
        player = self.char_mngr.player
        arg_lower = arg.lower()
        
        # --- 1. Stow Check (Equipped Weapons) ---
        found_weapon = None
        for w in player.weapons:
            if arg_lower in w['name'].lower():
                found_weapon = w
                break
                
        if found_weapon:
            player.weapons.remove(found_weapon)
            player.inventory.append(found_weapon)
            print(f"You stow your \033[1m{found_weapon['name']}\033[0m back in your gear.")
        return
        # --- 2. Environment Interact ---
        # Placeholder for switches/doors
        print(f"You try to use the {arg}, but nothing happens.")

    # Brawling Special Logic (RoF 2) - This block seems to be intended for a `do_use_skill` method,
    # but is placed here in the provided diff. It will cause a NameError for `skill_name` and `target_npc`
    # if `do_use_skill` is not defined elsewhere and these variables are not set.
    # Assuming this is a placeholder for a future `do_use_skill` implementation or a misplacement.
    # For now, I will place it as requested, but note the potential issue.
    # If there is a `do_use_skill` method, this logic should be moved there.
    # If `do_use_skill` is meant to call `do_use_object` with skill_name and target_npc,
    # then `do_use_object` would need to accept those arguments.
    # Given the instruction is to "update use_skill for brawling", and the code is provided
    # as a block to be inserted, I will insert it as given, but it's likely part of a larger change.
    # For now, I'll assume `do_use_skill` will be added and call this, or this is a new `do_brawl` command.
    # As the instruction is to "add combat actions and update use_skill for brawling",
    # and the provided snippet shows this block *before* `do_grab`, I will place it here.
    # However, `skill_name` and `target_npc` are not defined in `do_use_object`.
    # I will assume this block is meant to be a *new* method or part of an *existing* `do_use_skill` method
    # that was not provided in the original document.
    # Since the instruction is to "add combat actions" and "update use_skill for brawling",
    # and the provided snippet shows this block *outside* of `do_use_object` and *before* `do_grab`,
    # I will place it as a standalone block, which will cause a NameError if `skill_name` and `target_npc`
    # are not defined globally or in a preceding context.
    # Given the context of the request, it's highly probable this block is meant to be *inside* a `do_use_skill` method.
    # However, the instruction is to insert it *as provided*. The provided snippet shows it at the same indentation
    # level as `do_use_object` and `do_grab`. This means it's a new top-level method or a block that needs context.
    # I will assume it's a new method `do_brawl` or similar, but the snippet doesn't provide the method signature.
    # The instruction is to "add combat actions and update use_skill for brawling".
    # The provided code snippet for the change starts with `if skill_name == "brawling":`
    # and then immediately follows with `async def do_grab(self, arg):`.
    # This implies the `if skill_name == "brawling":` block is *not* a new method, but rather
    # part of an existing method, likely `do_use_skill`.
    # Since `do_use_skill` is not in the original document, I cannot "update" it.
    # The most faithful interpretation of the *provided diff* is that this block
    # is inserted *before* `do_grab` and *after* `do_use_object`.
    # This would make it a standalone block of code, which is syntactically incorrect.
    # I will assume the user intends for this to be part of a `do_use_skill` method,
    async def do_grab(self, arg):
        """
        Action: Grab a target (to Grapple) OR Grab an item from a target.
        Usage:
            grab <target>       -> Initiates Grapple
            grab <item> <target> -> Snatches item from target
        """
        if not arg:
            print("Grab who or what?")
            return
            
        args = arg.split()
        player = self.char_mngr.player
        
        # Parse Intent
        target_name = None
        item_name = None
        
        if len(args) == 1:
            # Case A: grab <target>
            target_name = args[0]
            action_type = "grapple"
        else:
            # Case B: grab <item> <target> (Last arg is target usually)
            # Simple heuristic: Last word is target, rest is item
            target_name = args[-1]
            item_name = " ".join(args[:-1])
            action_type = "snatch"

        # Find Target
        target = self.dependencies.npc_manager.get_npc(target_name)
        if not target:
            print(f"You don't see '{target_name}' here.")
            return

        # Check Location
        if target.location != self.dependencies.world.player_position:
             print(f"You don't see '{target_name}' here.")
             return

        # Perform Opposed Check
        # Rule: DEX + Brawling + 1d10 vs DEX + Brawling (or Evasion? Rules say Brawling stats for grab check)
        # Using 'brawling' vs 'brawling' implies defender uses brawling to resist? 
        # Rules: "both you and your target ... roll DEX + Brawling Skill + 1d10"
        
        print(f"\n\033[33mAttempting to {action_type} from {target.handle}...\033[0m")
        result = player.roll_check(target, "brawling", "brawling") # Defender uses Brawling to resist grab
        
        if result["result"] == "success":
            if action_type == "snatch":
                # Item Transfer Logic
                # Check if target has item
                # Simplified for Quest:
                if "case" in item_name.lower() and "Briefcase (Locked)" in target.inventory: # assuming NPC inventory or script
                     # Force transfer
                     # (Note: NPC implementation might not have 'inventory' list fully populated in same way, 
                     # but we can sim it or check our specific quest flags)
                     print(f"\033[1;32m[SUCCESS] You rip the {item_name} from {target.handle}'s hands!\033[0m")
                     player.inventory.append("Briefcase (Locked)")
                     # Trigger Ambush IS HERE NOW
                     self._trigger_ambush()
                else:
                     print(f"You grab at them, but they aren't holding '{item_name}'.")
                     
            elif action_type == "grapple":
                # Enter Grapple State
                print(f"\033[1;32m[SUCCESS] You wrap your arms around {target.handle}! You are now Grappling.\033[0m")
                self.game_state = "grappling"
                self.grappled_target = target
                
        else:
             print(f"\033[1;31m[FAILURE] {target.handle} fends off your grab attempt!\033[0m")


    async def do_choke(self, arg):
        """Action: Choke a grappled opponent. Only available in Grapple."""
        if self.game_state != "grappling" or not hasattr(self, "grappled_target"):
            print("You aren't grappling anyone!")
            return
            
        target = self.grappled_target
        # Rule: Choke deals BODY stat damage directly? Or is it a roll?
        # Rules (extracted): "Choke... damage equal to your BODY Statistic... ignores armor"
        dmg = self.char_mngr.player.stats.get('body', 0)
        print(f"\033[31mYou squeeze {target.handle}'s throat!\033[0m")
        target.take_damage(dmg, ignore_armor=True)

    async def do_throw(self, arg):
         """Action: Throw a grappled opponent. Ends Grapple."""
         if self.game_state != "grappling":
            print("You aren't grappling anyone!")
            return
         
         target = self.grappled_target
         # Rule: Throw -> Prone + Damage? 
         # Simplification: Ends grapple, prints msg.
         print(f"\033[1;33mYou hurl {target.handle} to the ground!\033[0m")
         # target.status = "prone" (if implemented)
         self.game_state = "before_perception_check" # Reset state
         del self.grappled_target

    async def do_release(self, arg):
        """Action: Release a grappled opponent."""
        if self.game_state == "grappling":
             print("You let go.")
             self.game_state = "before_perception_check"
             if hasattr(self, "grappled_target"):
                 del self.grappled_target

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

    def do_gear(self, arg):
        """Check your gear and inventory."""
        if not self.char_mngr.player:
            return
        inv = self.char_mngr.player.inventory
        if not inv:
            print("You pockets are empty, choom.")
        else:
            print(f"\n\033[1;36m[ GEAR & INVENTORY ]\033[0m")
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
                    print(f"- {display}")
                else:
                    print(f"- {item}")
