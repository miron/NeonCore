"""A Role Playing Game in the Cyberpunk Universe"""

# Standard library imports
import sys
import os
import logging
import json
import random
from cmd import Cmd
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


class ActionManager(Cmd):
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
        super().__init__()
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

    def select_available_backend(self):
        """Auto-select the first available backend"""
        try:
            name, backend = next(
                (name, backend)
                for name, backend in self.ai_backends.items()
                if backend.is_available()
            )
            print(f"Using {name} AI backend")
            return backend
        except StopIteration:
            raise RuntimeError("No AI backend available")

    def do_switch_ai(self, arg):
        """Switch between available AI backends (ollama/gemini)"""
        if arg not in self.ai_backends:
            print(f"Available backends: {', '.join(self.ai_backends.keys())}")
            return

        backend = self.ai_backends[arg]
        if not backend.is_available():
            print(f"{arg} backend is not available")
            return

        self.ai_backend = backend
        print(f"Switched to {arg} backend")

    def complete_switch_ai(self, text, line, begidx, endidx):
        """Complete AI backend options"""
        available_backends = list(self.ai_backends.keys())  # ['gemini', 'ollama']
        logging.debug(f"Available AI backends: {available_backends}")
        return [
            backend + " " for backend in available_backends if backend.startswith(text)
        ]

    def do_talk(self, arg):
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
                print(f"You don't see {target_npc.name} here.")
                return
            if not target_npc:
                # Check if it's a generic NPC provided by the world description?
                # For now, only support named NPCs
                print(f"Who is '{arg}'? You're talking to ghosts, choom.")
                return
        else:
            if not present_npcs:
                print("There's no one here to talk to.")
            else:
                print(
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

        print(
            f"\n\033[1;35m[ Entering conversation with {npc_name}. Type 'bye' to exit. ]\033[0m"
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

    def do_choose(self, arg=None):
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
            print(f"To pick yo' ride chummer, type 'choose <handle>'.")
            return

        self.prompt = f"{arg_handle} {ActionManager.prompt}"

        # Set player character (Match Handle)
        selected_char = next(
            c
            for c in self.char_mngr.characters.values()
            if c.handle.lower() == arg_lower
        )

        self.char_mngr.set_player(selected_char)

        # Set remaining characters as NPCs
        self.char_mngr.set_npcs(
            [
                c
                for c in self.char_mngr.characters.values()
                if c.char_id != selected_char.char_id
            ]
        )
        print(f"\n\033[1;33m[!] INCOMING HOLO-CALL: Unknown Number (Lazlo)\033[0m")
        print(f"\033[3mType 'answer' to accept the connection...\033[0m")

        self.game_state = "character_chosen"

    def complete_choose(self, text, line, begidx, endidx):
        """Complete character handles after 'choose' command"""
        return [n + " " for n in self.char_mngr.character_names(text)]

    def start_game(self):
        """
        Clears the terminal screen and starts the Cyberpunk RPG game.
        This method clears the terminal screen using the `os.system("clear")`
        command, sets the command prompt for the game to the value of the
        `prompt` class variable, and starts the command-line interface using
        the `cmdloop()` method of the `cmd.Cmd()` class.

        Returns:
            None
        """
        os.system("cls" if os.name == "nt" else "clear")
        self.prompt = (
            f"What's the deal, choomba? Give me the word:\n" f"{ActionManager.prompt}"
        )
        self.cmdloop()

    def completenames(self, text, *ignored):
        """Handle command completion including character roles"""
        logging.debug(
            f"completenames called with: text='{text}', state={self.game_state}"
        )

        # Get base commands that should always be available
        always_available = ["help", "quit"]
        base_cmds = [
            cmd
            for cmd in super().completenames(text, *ignored)
            if cmd in always_available
        ]

        # Add commands based on specific game state
        if self.game_state == "choose_character":
            if "choose" in super().completenames(text, *ignored):
                base_cmds.append("choose")

        elif self.game_state == "character_chosen":
            if "answer" in super().completenames(text, *ignored):
                base_cmds.append("answer")
            if "look" in super().completenames(text, *ignored):
                base_cmds.append("look")

        elif self.game_state == "before_perception_check":
            allowed = [
                "talk",
                "look",
                "go",
                "inventory",
                "whoami",
                "reflect",
                "use_skill",
                "deposit",
            ]
            for cmd in allowed:
                if cmd in super().completenames(text, *ignored):
                    base_cmds.append(cmd)

        elif self.game_state == "conversation":
            # say is visible here, as per user request
            allowed = ["say", "bye", "take", "inventory", "look", "talk"]
            for cmd in allowed:
                if cmd in super().completenames(text, *ignored):
                    base_cmds.append(cmd)

        logging.debug(f"Always available commands: {base_cmds}")

        # Get state-specific commands
        state_cmds = []
        # if self.cmd_mngr:
        #    state_cmds = self.cmd_mngr.get_check_command(self.game_state)
        # Note: cmd_mngr logic might be redundant now that we put everything in base_cmds,
        # but ignoring for now.
        logging.debug(f"State commands: {state_cmds}")

        # Combine all commands
        all_cmds = base_cmds + state_cmds
        logging.debug(f"Combined commands: {all_cmds}")

        # Filter by text prefix and append space
        matching = [cmd + " " for cmd in all_cmds if cmd.startswith(text)]
        logging.debug(f"Final matching commands: {matching}")

        return matching

    def _display_player_sheet(self, arg):
        """Internal method to display character sheet"""
        # No game state check needed as this is called by whoami which checks

        data = self.char_mngr.get_player_sheet_data()
        # Print header
        print(data["header"])

        # Print stats
        self.columnize(data["stats"], displaywidth=80)

        # Print combat info
        self.columnize(data["combat"], displaywidth=80)

        # Print skills
        self.columnize(data["skills"], displaywidth=80)

        # Print defense and weapons
        for defence, weapon in zip(data["defence"], data["weapons"]):
            print(f"{defence:<35}{weapon:<45}")

        # Print abilities, cyberware (Gear moved to separate command)
        print(f"ROLE ABILITY {'⌁'*14} CYBERWARE {'⌁'*17}")
        for ability, ware in zip(data["abilities"], data["cyberware"]):
            print(f"{ability:<28}{ware:<28}")

    def _display_rap_sheet(self, arg):
        """Internal method to display character background"""
        return self.char_mngr.do_rap_sheet(arg)



    def do_answer(self, arg):
        """Answer the incoming holo-call from Lazlo."""
        # Only allowed when phone is actually ringing (character_chosen state)
        if self.game_state != "character_chosen":
            print("No one is calling you right now, choomba.")
            return

        # Create the PhoneCall instance with char_mngr
        from ..story_modules import PhoneCall

        phone = PhoneCall(self.char_mngr)
        # Note: PhoneCall.do_phone_call might need renaming too, but for now we wrap it
        result = phone.do_phone_call(arg)

        # Update the ActionManager's state based on PhoneCall's result
        if isinstance(result, dict):
            if "prompt" in result:
                self.prompt = result["prompt"]
            if "game_state" in result:
                self.game_state = result["game_state"]
                logging.debug(f"Game state changed to: {self.game_state}")

        # Don't return anything - this prevented further commands

    def do_use_skill(self, arg):
        """Perform a skill check with the specified skill"""
        # Check if command is allowed in current game state
        allowed_states = ["before_perception_check", "conversation"]
        if self.game_state not in allowed_states:
            print("That command isn't available right now, choomba.")
            return

        if not self.skill_check:
            print("Skill check system not initialized!")
            return

        # Parse argument: skill_name [target_name]
        parts = arg.strip().split(maxsplit=1)
        skill_name = parts[0].lower() if parts else ""
        target_name = parts[1] if len(parts) > 1 else None

        if skill_name == "brawling":
            from ..game_mechanics.combat_shells import BrawlingShell
            if not target_name:
                print("Brawl with who? yourself? Provide a target.")
                return
            
            # Create and launch the shell
            shell = BrawlingShell(self.char_mngr.player, target_name)
            shell.cmdloop()
            return

        # Fallback to standard skill check for other skills
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

    def default(self, line):
        # Command doesn't exist at all
        if self.game_state == "conversation":
            self.do_say(line)
            return

        if line.startswith("go "):
            # Handle 'go' command directly
            direction = line.split(" ")[1]
            self.do_go(direction)
        else:
            print(
                "WTF dat mean, ain't no command like dat. Jack in 'help or '?' for the 411 on the specs, omae"
            )

    def do_look(self, arg):
        """Look around at your current location"""
        if self.game_state == "before_perception_check":
            self.dependencies.world.do_look(arg)
        else:
            print("Nothing much to see here yet, choomba.")

    def do_go(self, arg):
        """Move to a new location"""
        if self.game_state != "before_perception_check":
            print("That command isn't available right now, choomba.")
            return

        if not arg or arg.strip() == "":
            print("Go where? Try 'go north', 'go east', 'go south', or 'go west'.")
            return

        direction = arg.strip()
        try:
            self.dependencies.world.do_go(direction)
        except KeyError as e:
            print(f"Error: Location not found - {e}")
            print("This is a bug. Please report it.")
        except Exception as e:
            print(f"Error moving: {e}")

    def log_event(self, event):
        """Log an event to the player's recent_events buffer and trigger passive thoughts"""
        if self.char_mngr.player and self.char_mngr.player.digital_soul:
            self.char_mngr.player.digital_soul.recent_events.append(event)
            # Add some stress for any event (placeholder mechanic)
            self.char_mngr.player.digital_soul.stress = min(
                100, self.char_mngr.player.digital_soul.stress + 5
            )

            # Passive "Intrusive Thoughts" (Chance to trigger)
            # Only trigger random thoughts if stress is building up or event is significant
            if random.random() < 0.4:  # 40% chance
                self._trigger_intrusive_thought(event)

    def _trigger_intrusive_thought(self, event):
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
            response = self.ai_backend.get_chat_completion(messages)
            thought = response["message"]["content"]

            # Print in grey italics
            print(f"\033[3;90m{thought}\033[0m")

        except Exception:
            pass  # Fail silently for passive flavor

    def do_reflect(self, arg):
        """
        Reflect on your recent actions to process stress and evolve your soul.
        Usage: reflect
        """
        player = self.char_mngr.player
        soul = player.digital_soul

        if not soul.recent_events:
            print("\n\033[3mYour mind is clear. Nothing pressing to reflect on.\033[0m")
            return

        print(f"\n\033[1;30m[ INTERNAL MONOLOGUE INITIATED ]\033[0m")
        print(f"\033[3mProcessing {len(soul.recent_events)} recent events...\033[0m")

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
            print(f"\n\033[1;36mSOUL > {question}\033[0m")

            # 2. Get User Reflection
            answer = input("\n\033[1;30mYOU > \033[0m")

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
                        "Return ONLY a JSON object with keys: "
                        "'stress_change' (integer, usually negative to heal), "
                        "'new_traits' (list of strings, strictly new discovered traits based on answer), "
                        "'memory_summary' (string, summary of this memory)."
                    ),
                },
            ]

            print("\n\033[3m(Re-integrating psyche...)\033[0m")
            analysis_response = self.ai_backend.get_chat_completion(analyze_messages)
            analysis_text = analysis_response["message"]["content"]

            # Clean generic markdown if present
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0]
            elif "```" in analysis_text:
                analysis_text = analysis_text.split("```")[1].split("```")[0]

            analysis = json.loads(analysis_text)

            # Apply Changes
            soul.stress = max(
                0, min(100, soul.stress + analysis.get("stress_change", -10))
            )
            new_traits = analysis.get("new_traits", [])
            for t in new_traits:
                if t not in soul.traits:
                    soul.traits.append(t)
                    print(f"\033[1;32m[+] NEW TRAIT ACQUIRED: {t}\033[0m")

            memory = analysis.get("memory_summary")
            if memory:
                soul.memories.append(f"{events_str} -> {memory}")

            # Clear buffer
            soul.recent_events = []
            print(f"\033[1;36m[ REFLECTION COMPLETE. STRESS: {soul.stress}% ]\033[0m")

        except Exception as e:
            print(f"\nReflection failed: {e}")

    def do_help(self, arg):
        """Get help for commands - context-sensitive based on game state."""
        if not arg:
            # Show general help introduction based on current state
            help_intro = self.help_system.get_help(state=self.game_state)
            wprint(help_intro)

            # Show available commands
            # print("\nAvailable commands in your current state:")
            # commands = self.help_system.get_available_commands(state=self.game_state)
            # self.columnize(commands, displaywidth=80)
        else:
            # Show specific command help
            help_text = self.help_system.get_help(arg, self.game_state)
            wprint(help_text)

            # If it's a skill command, show available skills
            if (
                arg == "use_skill"
                and self.game_state == "before_perception_check"
                and self.char_mngr.player
            ):
                print("\nAvailable skills:")
                skills = self.char_mngr.player.get_skills()
                self.columnize(skills, displaywidth=80)

    def do_quit(self, arg):
        """Exits Cyberpunk"""
        wprint(
            "Catch you on the flip side, choombatta. Keep your chrome "
            "polished and your guns loaded, "
            "the neon jungle ain't no walk in the park."
        )
        sys.exit()

    def complete_whoami(self, text, line, begidx, endidx):
        """Complete whoami subcommands"""
        subcommands = ["stats", "bio", "soul"]
        return [s + " " for s in subcommands if s.startswith(text)]

    def do_whoami(self, arg):
        """
        Displays your identity dashboard.
        Usage:
            whoami          -> Dashboard Summary
            whoami stats    -> Full Character Sheet
            whoami bio      -> Rap Sheet (Backstory)
            whoami soul     -> Digital Soul (Traits & Memories)
        """
        if self.game_state == "choose_character":
            print("You have no identity yet. Choose a character first.")
            return

        arg = arg.strip().lower()
        player = self.char_mngr.player

        # Default Dashboard View
        if not arg or arg == "dashboard":
            # Header
            print(
                f"\n\033[1;36mHID:\033[0m {player.handle} \033[1;36mROLE:\033[0m {player.role}"
            )
            stats = player.stats
            print(
                f"\033[1;36mINT:\033[0m {stats.get('int', 0)} | \033[1;36mREF:\033[0m {stats.get('ref', 0)} | \033[1;36mEMP:\033[0m {stats.get('emp', 0)}"
            )
            print(f"{'⌁'*60}")

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
            print(f"CYBER STRESS: 🧠 {color}[{bar}] {current_stress}%\033[0m")

            # HOST INSTINCT (The fixed trait of the body)
            print(f"\n\033[1;35m[ HOST INSTINCT ]\033[0m")
            print(f"{player.trait if player.trait else 'Survival'}")

            # DIGITAL SOUL (Your True Self)
            print(f"\n\033[1;36m[ TRUE SELF ]\033[0m")
            if player.digital_soul.traits:
                print(f"{', '.join(player.digital_soul.traits)}")
            else:
                print("(No traits developed yet)")

            # Gear Summary
            inv_count = len(player.inventory)
            print(
                f"\n\033[1;33mGEAR:\033[0m {inv_count} item(s) carried. (Use 'gear' to view)"
            )
            return

        if arg == "stats":
            self._display_player_sheet(None)
            return
        elif arg == "bio":
            self._display_rap_sheet(None)
            return
        elif arg in ["soul", "mind", "traits"]:
            # Deep Dive into Digital Soul
            soul = player.digital_soul
            print(
                f"\n🧠 \033[1;36mDIGITAL SOUL INTERFACE\033[0m: {player.handle} [{player.role}]"
            )
            print(f"{'⌁'*60}")

            print(f"\n\033[1;35m[ BIG 5 PERSONALITY ]\033[0m")
            b5 = soul.big5
            print(f"Openness:          {b5.openness:>3}%")
            print(f"Conscientiousness: {b5.conscientiousness:>3}%")
            print(f"Extraversion:      {b5.extraversion:>3}%")
            print(f"Agreeableness:     {b5.agreeableness:>3}%")
            print(f"Neuroticism:       {b5.neuroticism:>3}%")

            print(f"\n\033[1;35m[ TRUE SELF ]\033[0m")
            if soul.traits:
                print(
                    f"\033[1;35mTRAITS > {', '.join(player.digital_soul.traits)}\033[0m"
                )
            else:
                print("(No traits developed yet)")

            print(f"\n\033[1;35m[ MEMORY STREAM ]\033[0m")
            if player.digital_soul.memories:
                print("\n".join(player.digital_soul.memories) + "\033[0m")
            else:
                print("(No memories recorded yet)")
            return

    # Conversation Methods (Re-added)
    def do_bye(self, arg):
        """End the conversation."""
        if self.game_state == "conversation":
            print(f"\033[1;35m[ You step away from the conversation. ]\033[0m")
            self.game_state = "before_perception_check"  # Revert specific state
            if hasattr(self, "original_prompt"):
                self.prompt = self.original_prompt
            if hasattr(self, "conversing_npc"):
                del self.conversing_npc
        else:
            print("You aren't talking to anyone.")

    def do_say(self, arg):
        """Say something to the NPC."""
        if not hasattr(self, "conversing_npc"):
            print("You're talking to yourself.")
            return

        npc = self.conversing_npc
        player = self.char_mngr.player

        # AI Interaction
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are {npc.name} ({npc.role}).\n"
                    f"CONTEXT: {npc.dialogue_context}\n"
                    f"You are talking to {player.handle} ({player.role}).\n"
                    "GOAL: Reply to the user's input. Keep it short and in character."
                ),
            },
            {"role": "user", "content": arg},
        ]

        if self.ai_backend:
            try:
                response = self.ai_backend.get_chat_completion(messages)
                print(
                    f"\n\033[1;32m{npc.name}: {response['message']['content']}\033[0m"
                )
                self.log_event(f"Said to {npc.name}: {arg}")
            except Exception as e:
                print(f"Error: {e}")

    # do_take removed as per user request (replaced by skill interactions)



    def do_take(self, arg):
        """Take an object from the environment."""
        # Determine if we are in conversation or before_perception_check
        # (Both allow 'take' now)
        
        # Check argument
        arg_lower = arg.lower()
        if "case" in arg_lower: # Matches briefcase, case, suitcase
             # Check Context: Is Lenard present?
            current_location = self.dependencies.world.player_position
            # We can check via npc_manager or just assume if prompt logic led here.
            # Ideally verification:
            present_npcs = [n.name.lower() for n in self.dependencies.npc_manager.get_npcs_in_location(current_location)]
            
            if "lenard" in present_npcs:
                 player = self.char_mngr.player
                 # Add to inventory
                 if "Briefcase (Locked)" not in player.inventory:
                     player.inventory.append("Briefcase (Locked)")
                     print(f"\n\033[1;32m[SUCCESS] You snatch the Briefcase from Lenard's grasp!\033[0m")
                     self._trigger_ambush()
                 else:
                     print("You already have the briefcase, choom.")
            else:
                 print("There's no briefcase here to take.")
        else:
             print("You can't take that.")

    def _trigger_ambush(self):
        """Triggers the scripted ambush event."""
        # === TRIGGER AMBUSH ===
        from ..game_mechanics.combat_system import CombatEncounter

        print("\n\033[1;31m[!] SUDDENLY, TIRES SCREECH! A BLACK VAN SLIDES AROUND THE CORNER!\033[0m")

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
                print(f"- {item}")
