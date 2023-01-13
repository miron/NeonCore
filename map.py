"""Character Movement on ASCII Map"""
import random
from game import SkillCheck

def main(stdscr, curses, player, npcs):
    """wrapped for debugging, will be replaced by curses.endwin()"""
    curses.curs_set(False)  # hide the cursor
    curses.init_color(0, 0, 0, 0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    player_color = curses.color_pair(1)
    npc_color = curses.color_pair(2)


    # Set up the map
    map_data= (
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

    # Spawn the player and NPCs randomly on the map
    empty_positions = []
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == " ":
                empty_positions.append((x,y))

    random.shuffle(empty_positions)
    player_x, player_y = empty_positions.pop()
    npc_positions = empty_positions[:len(npcs)]
    for npc in npcs:
        npc.x, npc.y  = empty_positions.pop()

    # Wait for user input to move the player character
    while True:
        # Redraw the map and update the player position
        for y_axis, row in enumerate(map_data):
            for x_axis, cell in enumerate(row):
                stdscr.addch(y_axis, x_axis, cell)
        stdscr.addch(player_y, player_x, '@', player_color)
        for npc in npcs:
        # Draw the NPCs on the map
            stdscr.addch(npc.y, npc.x, 'N', npc_color)

        key = stdscr.getch()
        new_x = player_x
        new_y = player_y
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
        if (new_x >= 0 and new_x < len(map_data[0]) and new_y >= 0 and new_y < len(map_data)):
            # Check for collision with walls
            if map_data[new_y][new_x] !='#':
                if type(map_data[new_y][new_x]) == npc: # npc encountered 
                    skill_check = SkillCheck(npc)
                player_x = new_x
                player_y = new_y


