"""A Role Playing Game in the Cyberpunk RED Universe"""
import cmd
import os
import sys
import shelve
import time
from skill_check import SkillCheckCommand
import map 
from utils import wprint
from managers.cyberpunk_manager  import CyberpunkManager
from map import Map


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
    prompt = 'ᐸ/> '
    ruler = '⌁'
    doc_header = "Recorded jive (type help <jargon>):"

    def __init__(self, characters_manager):
        super().__init__()
        self.characters_manager = characters_manager
        self.player = None
        self.npcs = None
        self.game_state = None

    def start_game(self):
        os.system('clear')
        #self.characters_manager.register_command(self)
        self.prompt = '(choose_character) '
        self.cmdloop()

    def completenames(self, text, *ignored):
        cmds = super().completenames(text, *ignored)
        check_cmd = self.get_check_command()
        if check_cmd:
            cmds += [c for c in check_cmd.get_available_commands() if 
                     c.startswith(text)]
        return cmds

    def get_check_command(self):
        if self.game_state == 'character_chosen':
           pass
        if self.game_state == 'before_perception_check':
            use_skill = SkillCheckCommand(self.player)
            use_skill.register_command(self)
            return use_skill 
        elif self.game_state == 'heywood_industrial':
            pass
        elif self.game_state == 'before_ranged_combat':
            return RangedCombatCommand(self.player, self.npcs)
        else:
            self.characters_manager.register_command(self)
            return self.characters_manager

    def do_shell(self, arg):
        """ Shell commands can be added here prefixed with !"""
        os.system('clear')

   # def postcmd(self, stop, line):
   #    # Get the number of rows in the output
   #    rows, _ = os.popen('stty size', 'r').read().split()
   #    # Move the cursor to the correct position
   #    print(f'\033[{int(rows)}H')
   #    return stop

   # def postcmd(self, stop, line):
   #     # Get the size of the terminal window
   #     rows, cols = self.stdscr.getmaxyx()
   #     # Move the cursor to the 24th row (0-indexed)
   #     self.stdscr.move(24, 0)
   #     # Refresh the terminal window
   #     self.stdscr.refresh()
   #     return cmd.Cmd.postcmd(self, stop, line)

    def default(self, line):
        print("WTF dat mean, ain't no command like dat")

    def do_quit(self, arg):
        """Exits Cyberpunk RED"""
        wprint("Catch you on the flip side, choombatta. Keep your chrome "
               "polished and your guns loaded, "
               "the neon jungle ain't no walk in the park.")
        # Open database, create if it doesn't already exist
        with shelve.open('timestamp') as dbase:
            # Save data to the database>
            dbase['timestamp'] = time.time()
        sys.exit()

    def do_move(self, args):
        """Move player in the specified direction"""
        my_map = Map(self.characters_manager.player, 
                     self.characters_manager.npcs)
        my_map.move()

# Open a shelve in read mode
#with shelve.open('timestamp', 'r') as db:
    # Load the timestamp
    #timestamp = dbase['timestamp']
#print(timestamp)

