import time
# Define the stick figure as a list of strings
stick_figure = [
    "   O   ",
    "   |   ",
    "  / \\  ",
    " /   \\ ",
    "/     \\",
]

# Define the number of steps to take
num_steps = 10

# Animate the stick figure
for i in range(num_steps):
    # Clear the console
    print("\033[H\033[J")

    # Print the stick figure, shifting the position by one character to the right each time
    for line in stick_figure:
        print(line[i % len(line):] + line[:i % len(line)])

    # Wait for a short time before printing the next frame
    time.sleep(0.1)
