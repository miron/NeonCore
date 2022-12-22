import time

# Define the stick figure frames as a list of lists of strings
stick_figure_frames = [
    [
        "   O   ",
        "   |   ",
        "  / \\  ",
        " /   \\ ",
        "/     \\",
    ],
    [
        "    O   ",
        "    |   ",
        "   / \\  ",
        "  /   \\ ",
        " /     \\",
    ],
    [
        "     O   ",
        "     |   ",
        "    / \\  ",
        "   /   \\ ",
        "  /     \\",
    ],
    [
        "      O   ",
        "      |   ",
        "     / \\  ",
        "    /   \\ ",
        "   /     \\",
    ],
]

# Define the number of steps to take
num_steps = 10

# Animate the stick figure
for i in range(num_steps):
    # Clear the console
    print("\033[H\033[J")

    # Print the current frame
    for line in stick_figure_frames[i % len(stick_figure_frames)]:
        print(line)

    # Wait for a short time before printing the next frame
    time.sleep(0.25)
