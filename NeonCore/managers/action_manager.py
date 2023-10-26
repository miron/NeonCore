"""A Role Playing Game in the Cyberpunk Universe"""
from argparse import Action
import cmd
import os
import sys

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
            f"What's the deal, choomba? Give me the word:\n"
            f"{ActionManager.prompt}"
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
