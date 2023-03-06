"""Character Movement on ASCII Map"""
import random
import curses
from ..game_mechanics import SkillCheckCommand
   

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
        "### ####  ###   ")
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.curs_set(False) # hide the cursor
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.player_color = curses.color_pair(1)
        self.npc_color = curses.color_pair(2)
        # Spawn the player and NPCs randomly on the map
        self.empty_positions = [
            (x,y) for y, row in enumerate(self.map_data) for 
            x, cell in enumerate(row) if cell == " "]
        random.shuffle(self.empty_positions)
        self.player_x, self.player_y = self.empty_positions.pop()
        self.npc_positions = self.empty_positions[:len(self.npcs)]
        for npc in self.npcs:
            npc.x, npc.y  = self.empty_positions.pop()

    def do_move(self, args):
        """Move player in the specified direction"""
        my_map = Map(self.char_mngr.get_player(), 
                     self.char_mngr.get_npcs())
        my_map.move()

    def move(self):
        while True:
            self.draw_map()
            self.draw_player()
            self.draw_npcs()
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            new_x, new_y = self.get_new_player_position(key)
            if not (self.is_within_map_bounds(new_x, new_y) and 
                    self.is_valid_move(new_x, new_y)):
                continue
            self.player_x, self.player_y = new_x, new_y
            # Check for collision with NPCs
            for npc in self.npcs:
                if (npc.x, npc.y) == (new_x, new_y):
                    self.encountered_npc = True
                    SkillCheckCommand(self.player, npc=npc)
                    # TODO: set game_state to 'npc_encountered'
                    # show ascii art, instance should be created 
                    # in do_use_skill, only pass npc
                    curses.endwin()
                    break
            if self.encountered_npc:
                break
        curses.endwin()

    def draw_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                self.stdscr.addch(y, x, cell)

    def draw_player(self):
        self.stdscr.addch(self.player_y, self.player_x, '@', self.player_color)

    def draw_npcs(self):
        for npc in self.npcs:
            self.stdscr.addch(npc.y, npc.x, 'N', self.npc_color)

    def get_new_player_position(self, key):
        new_x, new_y = self.player_x, self.player_y
        if key == ord('w'):
            new_y -= 1
        elif key == ord('s'):
            new_y += 1
        elif key == ord('a'):
            new_x -= 1
        elif key == ord('d'):
            new_x += 1
        return new_x, new_y

    def is_within_map_bounds(self, x, y):
        return (x >= 0 and x < len(self.map_data[0]) and 
                y >= 0 and y < len(self.map_data))

    def is_valid_move(self, x, y):
        return self.map_data[y][x] == ' '
