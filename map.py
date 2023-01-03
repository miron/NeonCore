import curses

# Initialize curses
stdscr = curses.initscr()
curses.curs_set(False)  # hide the cursor

# Set up the map
map_matrix = [
    ['#', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', ' ', ' ', ' ', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    [' ', '#', '#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    [' ', '#', '#', ' ', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', '#'],
    [' ', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', '#'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', '#'],
    ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', '#'],
    ['#', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', ' ', ' '],
    ['#', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', ' ', ' ', ' '],
]


# Set the initial position of the player character
player_x = 3
player_y = 0

# Wait for user input to move the player character
while True:
    # Redraw the map and update the player position
    for y, row in enumerate(map_matrix):
        for x, cell in enumerate(row):
            stdscr.addch(y, x, cell)
    stdscr.addstr(player_y, player_x, '\N{singer}')
    stdscr.refresh()
    
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
    else:
        continue
    
    # Check for collision with walls
    if map_matrix[new_y][new_x] == '#':
        continue
    
    # Update the player position
    player_x = new_x
    player_y = new_y
