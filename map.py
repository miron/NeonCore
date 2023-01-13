"""Character Movement on ASCII Map"""
import curses
import random

def main(stdscr):
    """wrapped for debugging, will be replaced by curses.endwin()"""
    curses.curs_set(False)  # hide the cursor
    curses.init_color(0, 0, 0, 0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    player_color = curses.color_pair(1)


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
    "### ####  ###   "
)

    # Spawn the player randomly on the map
    while True:
        player_x = random.randint(0, len(map_data[0]) - 1)
        player_y = random.randint(0, len(map_data) - 1)
        if map_data[player_y][player_x] != "#":
            #player.x =  player_x
            #player.y =  player_y
            break

    # Wait for user input to move the player character
    while True:
        # Redraw the map and update the player position
        for y_axis, row in enumerate(map_data):
            for x_axis, cell in enumerate(row):
                stdscr.addch(y_axis, x_axis, cell)
        stdscr.addch(player_y, player_x, '@', player_color)
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
                # Update the player position
                player_x = new_x
                player_y = new_y

curses.wrapper(main)
