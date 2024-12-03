"""A Role Playing Game in the Cyberpunk Universe"""

from cmd import Cmd
import os
import sys
from argparse import Action
from ..utils import wprint
from ..ai_backends.ollama import OllamaBackend
from ..ai_backends.grok import GrokBackend
import logging # Added


class ActionManager(Cmd):
    """cli, displays character stats/skills, quits the game"""

    intro = r"""     ᐸ ソ ╱> /Ξ /≥ /> // /𐑘/ /ᐸ
                      ‾
   …   ˛⁄⁔      ˛⁔     ⁔   _  ¸¸
  (˙}  \(∞l   ,, {˚)/ ¸{=}˛ |\\(˚}
 /(\)╲  `••\˛_ \/(⎔◊𐑘 (\+/)  \∏(p)]
 \ᢘ╦╤═÷- Y¸∆     ¸U˛   \Ξ˛\   ´¸v˛|
  7˘ 𐑘 ¸⁄∫𐑘      [][]   7 𐑘 `   [ ]´
  ]  ]  / |      [ [   ]  ]    { }
  l  L ∫  l      ɺ[ɺ]  l  L    ɺ L
    ⌁help⌁   give me the 411
"""

    prompt = "ᐸ/> "
    ruler = "⌁"
    doc_header = "Recorded jive (type help <jargon>):"

    def __init__(self, dependencies):
        super().__init__()
        self.char_mngr = dependencies.char_mngr
        self.cmd_mngr = dependencies.cmd_mngr
        self.game_state = "choose_character"

        # Initialize AI backend
        self.ai_backends = {"grok": GrokBackend(), "ollama": OllamaBackend()}
        self.current_backend = self.select_available_backend()

    def select_available_backend(self):
        """Auto-select the first available backend"""
        for name, backend in self.ai_backends.items():
            if backend.is_available():
                print(f"Using {name} AI backend")
                return backend
        raise RuntimeError("No AI backend available")

    def do_switch_ai(self, arg):
        """Switch between available AI backends (ollama/grok)"""
        if arg not in self.ai_backends:
            print(f"Available backends: {', '.join(self.ai_backends.keys())}")
            return

        backend = self.ai_backends[arg]
        if not backend.is_available():
            print(f"{arg} backend is not available")
            return

        self.current_backend = backend
        print(f"Switched to {arg} backend")

    def do_talk(self, arg):
        "Start a conversation with an NPC"
        player_name = "V"
        npc_name = "Judy"
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are {npc_name}, a female hacker with streetwise savvy and a penchant for Night City street slang."
                    f" You are known for your sharp wit and cyber skills. You are now indterfacing with {player_name}."
                    " The conversation should be casual, using the colorful and gritty slang of Night City's streets."
                ),
            },
            {"role": "user", "content": arg},
        ]

        try:
            completion = self.current_backend.get_chat_completion(messages)
            response = completion["message"]["content"]
            print(f"{npc_name}: {response}")
        except Exception as e:
            print(f"AI communication error: {e}")

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
        os.system("clear")
        self.prompt = (
            f"What's the deal, choomba? Give me the word:\n" f"{ActionManager.prompt}"
        )
        self.cmdloop()

    def do_choose_character(self, arg=None):
        """Allows the player to choose a character role."""
        if arg not in self.char_mngr.roles():
            characters_list = [
                f"{character.handle} ({character.role})"
                for character in self.char_mngr.characters.values()
            ]
            self.columnize(characters_list, displaywidth=80)
            print(f"To pick yo' ride chummer, type in {self.char_mngr.roles()}.")
            return

        self.prompt = f"{arg} {ActionManager.prompt}"
        # Set player character
        self.char_mngr.set_player(
            next(c for c in self.char_mngr.characters.values()
                if c.role.lower() == arg)
        )
        # Set remaining characters as NPCs
        self.char_mngr.set_npcs(
            [c for c in self.char_mngr.characters.values()
            if c.role.lower() != arg]
        )
        self.game_state = "character_chosen"

    def complete_choose_character(self, text, line, begidx, endidx):
        """Complete character roles after 'choose_character' command"""
        logging.debug(f"Role completion: text='{text}', line='{line}'")
        return [role for role in self.char_mngr.roles(text)]
    def completenames(self, text, *ignored):
        """Handle command completion including character roles"""
        logging.debug(f"completenames called with: text='{text}', state={self.game_state}")

        # Get base commands
        base_cmds = super().completenames(text, *ignored)
        logging.debug(f"Base commands from super(): {base_cmds}")

        # Get state commands
        state_cmds = []
        if self.cmd_mngr:
            state_cmds = self.cmd_mngr.get_check_command(self.game_state)
        logging.debug(f"State commands: {state_cmds}")

        # Combine all commands
        all_cmds = base_cmds + state_cmds
        logging.debug(f"Combined commands: {all_cmds}")

        # Filter by text prefix
        matching = [cmd for cmd in all_cmds if cmd.startswith(text)]
        logging.debug(f"Final matching commands: {matching}")

        return matching

    def do_player_sheet(self, arg):
        """Displays the character sheet"""
        data = self.char_mngr.get_player_sheet_data()
        # Print header
        print(data['header'])

        # Print stats
        self.columnize(data['stats'], displaywidth=80)

        # Print combat info
        self.columnize(data['combat'], displaywidth=80)

        # Print skills
        self.columnize(data['skills'], displaywidth=80)

        # Print defense and weapons
        for defence, weapon in zip(data['defence'], data['weapons']):
            print(defence.ljust(35) + weapon.ljust(45))

        # Print abilities, cyberware, and gear
        print(f"ROLE ABILITY {'⌁'*14} CYBERWARE {'⌁'*17} GEAR {'⌁'*19}")
        for ability, ware, gear in zip(data['abilities'], data['cyberware'], data['gear']):
            print(ability.ljust(28) + ware.ljust(28) + gear.ljust(24))

        # Print abilities, cyberware, and gear
        print(f"ROLE ABILITY {'⌁'*14} CYBERWARE {'⌁'*17} GEAR {'⌁'*19}")
        for ability, ware, gear in zip(data['abilities'], data['cyberware'], data['gear']):
            print(ability.ljust(28) + ware.ljust(28) + gear.ljust(24))

    def do_rap_sheet(self, arg):
        """Display character background"""
        return self.char_mngr.do_rap_sheet(arg)

    def do_phone_call(self, arg):
        """Start the phone call story element"""
        # Assuming PhoneCall class has this method
        from ..story_modules import PhoneCall
        phone = PhoneCall(self.char_mngr)
        return phone.do_phone_call(arg)

    def do_shell(self, arg):
        """Shell commands can be added here prefixed with !"""
        os.system("clear")

    def default(self, line):
        print(
            "WTF dat mean, ain't no command like dat. Jack in 'help or '?' for the 411 on the specs, omae"
        )

    def do_quit(self, arg):
        """Exits Cyberpunk"""
        wprint(
            "Catch you on the flip side, choombatta. Keep your chrome "
            "polished and your guns loaded, "
            "the neon jungle ain't no walk in the park."
        )
        sys.exit()
