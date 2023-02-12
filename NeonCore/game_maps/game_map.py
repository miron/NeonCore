"""Character Movement on ASCII Map"""
import random
import curses
from ..game_mechanics import NPCEncounterCommand
   

class Map:
    def __init__(self, player, npcs):
        self.player = player
        self.npcs = npcs
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
        curses.curs_set(False)  # hide the cursor
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.player_color = curses.color_pair(1)
        self.npc_color = curses.color_pair(2)
        # Spawn the player and NPCs randomly on the map
        self.empty_positions = []
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == " ":
                    self.empty_positions.append((x,y))
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
        try:
            while True:
                # Redraw the map and update the player position
                for y_axis, row in enumerate(self.map_data):
                    for x_axis, cell in enumerate(row):
                        self.stdscr.addch(y_axis, x_axis, cell)
                self.stdscr.addch(
                    self.player_y, self.player_x, '@', self.player_color)
                for npc in self.npcs:
                # Draw the NPCs on the map
                    self.stdscr.addch(npc.y, npc.x, 'N', self.npc_color)

                key = self.stdscr.getch()
                new_x = self.player_x
                new_y = self.player_y
                if key == ord('w'):
                    new_y -= 1
                elif key == ord('s'):
                    new_y += 1
                elif key == ord('a'):
                    new_x -= 1
                elif key == ord('d'):
                    new_x += 1
                elif key == ord('q'):
                    break
                # Check if the new position is within the bounds of the map
                if (new_x >= 0 and new_x < len(self.map_data[0]) and 
                    new_y >= 0 and new_y < len(self.map_data)):
                    # Check for collision with walls
                    if self.map_data[new_y][new_x] == ' ':
                        for npc in self.npcs:
                            # npc encountered
                            if (npc.x, npc.y) == (new_x, new_y): 
                                # TODO: set game_state to 'npc_encountered'
                                # show ascii art, drop to cmd
                                # pass npc object
                                npc_encounter = NPCEncounterCommand(self.player)
                                curses.endwin()
                                npc_encounter.handle_npc_encounter(npc)
                        self.player_x = new_x
                        self.player_y = new_y
        except StopIteration:
            pass
        curses.endwin()

