import time

# Define the stick figure as a list of strings
stick_figure = [
    "   O   ",
    "   |   ",
    "   |   ",
    "   |   ",
    "   |_  ",
]

# Define the number of steps to take
num_steps = 10

# Animate the stick figure
for i in range(num_steps):
    # Clear the console
    print("\033[H\033[J")

    # Print the stick figure, shifting the position by one character to the right each time
    for j, line in enumerate(stick_figure):
        if j == 0:
            # Head
            print(line[i % len(line):] + line[:i % len(line)])
        elif j == 1:
            # Torso
            print(line)
        elif j == 2:
            # Left arm
            if i % 2 == 0:
                print(line[:2] + "\\" + line[3:])
            else:
                print(line[:2] + "/" + line[3:])
        elif j == 3:
            # Right leg
            if i % 2 == 0:
                print(line[:2] + "\\" + line[3:])
            else:
                print(line[:2] + "/" + line[3:])
        elif j == 4:
            # Left leg
            if i % 2 == 0:
                print(line[:2] + "/" + line[3:])
            else:
                print(line[:2] + "\\" + line[3:])

    # Wait for a short time before printing the next frame
        time.sleep(0.1)

