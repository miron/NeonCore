"""A Role Playing Game in the Cyberpunk Universe"""

import cmd
import os
import sys
from argparse import Action
from ..utils import wprint
from ..ai_backends.ollama import OllamaBackend
from ..ai_backends.grok import GrokBackend

class ActionManager(cmd.Cmd):
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

    def __init__(self, char_mngr, cmd_mngr):
        super().__init__()
        self.char_mngr = char_mngr
        self.cmd_mngr = cmd_mngr
        self.game_map = None
        self.game_state = "choose_character"

        # Initialize AI backend
        self.ai_backends = {
            "grok": GrokBackend(),
            "ollama": OllamaBackend()
        }
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


    # TODO needed to show up in help before hitting tab
    # but shows as Miscelaneous topic and doesn't use docstring of do_* for
    # help text.
    # def help_choose_character(self):
    #     wprint(
    #         "choose_character - Allows the player to choose a character role.")
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

    def completenames(self, text, *ignored):
        cmds = super().completenames(text, *ignored)
        if check_cmd := self.cmd_mngr.get_check_command(self.game_state):
            cmds += [c for c in check_cmd if c.startswith(text)]
        return cmds

    def do_shell(self, arg):
        """Shell commands can be added here prefixed with !"""
        os.system("clear")

    def default(self, line):
        print("WTF dat mean, ain't no command like dat")

    def do_quit(self, arg):
        """Exits Cyberpunk"""
        wprint(
            "Catch you on the flip side, choombatta. Keep your chrome "
            "polished and your guns loaded, "
            "the neon jungle ain't no walk in the park."
        )
        sys.exit()
