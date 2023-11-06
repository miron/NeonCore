"""A Role Playing Game in the Cyberpunk Universe"""
import cmd
import json
import os
import sys
import urllib.request
from argparse import Action

from ..utils import wprint


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

    def do_talk(self, arg):
        "Start a conversation with an NPC"
        npc_name = "Judy"
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a hacker in the dystopian city of Neo-Tokyo."
                    f"You are now interfacing with {npc_name}."
                ),
            },
            {"role": "user", "content": arg},
        ]
        completion = self.get_chat_completion(messages)
        response = completion["choices"][0]["message"]["content"]
        print(f"{npc_name}: {response}")

    def get_chat_completion(self, prompt):
        url = "http://localhost:8000/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {"prompt": prompt, "max_tokens": 100}
        req = urllib.request.Request(
            url, headers=headers, data=json.dumps(data).encode()
        )
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

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
