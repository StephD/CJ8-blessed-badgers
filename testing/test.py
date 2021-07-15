from blessed import Terminal

"""
Pros
Easy to render no need to use subtractable dict.

Cons
hard code every position
"""

PLAYER = "@"
MSG_POS = (2, 26)

# Don't create object for every wall maintain a different sets.
wall_pos = set()
# Entities Dictionary for now -> convert it to objects.
entity = {}
# Player position (x, y)
player_pos = (0, 0)

# For Now
message = {
    "M": "I have left the key somewhere. find the ✕ mark",
    "X": "The door seem to be closed.",
    "P": "Beware of this poisonous block. This might decrease your life.",
    "✕": "Hurray! You have found the key.",
    "completed": "You have completed the tutorial",
}

# For Now
found_key = False

log_fd = open("log", "w")


def log(s):
    """
    Simple log function.
    """
    log_fd.write(s)


def _print(s):
    """
    Do we need this ?
    """
    print(s, end="", flush=True)


def global_frame(term):
    """
    This will render global frame from gframe.txt
    """
    with open("gframe.txt", encoding="utf-8") as fd:
        data = fd.read()
    _print(data)


def get_neighbour(x, y):
    """
    Get neighbour position of an entity.
    Note: change the height and width if gframe or map is changed.
    """
    neighbours = set()
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i == x and j == y) or not (1 < i < 25 and 1 < j < 57):
                continue
            neighbours.add((i, j))
    return neighbours


def game_layout(term, level=0, pos=(2, 1)):
    """
    Assuming level is int.
    """
    with open(f"{level}.txt", encoding="utf-8") as fd:
        data = fd.readlines()
    x, y = pos
    for i, line in enumerate(data):
        # For rendering inside the global frame.
        data[i] = term.move_xy(x, y) + data[i]
        y += 1
        for j, char in enumerate(line):
            if char == " ":
                continue
            # Note it is a cross(U+2715).
            elif char in "MPX✕":
                entity[char] = get_neighbour(i + 1, j + 2)
            # why j + 2?
            wall_pos.add((i + 1, j + 2))
    # Let the player be at the center of the game.
    global player_pos
    player_pos = len(data[0]) // 2, len(data) // 2

    # Show level.
    sidebar(term, 0, str(level))

    data = "".join(data)
    _print(data + term.move_xy(*player_pos) + PLAYER)


def put_msg(term, msg):
    # Is it okay to call this
    clr_msg(term)
    # Position of message box
    x, y = MSG_POS
    max_width = 72
    # Check if it can fit in first line
    if len(msg) < max_width:
        _print(term.move_xy(x, y) + msg)
    else:
        # Break and print and keep it under 6 lines
        pass
    x, y = 5, 26


def clr_msg(term):
    # Position of message box
    max_width = 72
    x, y = MSG_POS
    # Message height
    for i in range(6):
        _print(term.move_xy(x, y) + " " * max_width)
        x += 1


def sidebar(term, field_id, msg):
    # Move the level to somewhere else
    # max_with maybe 10
    max_width = 10
    if field_id == 0:
        # update Level
        x, y = 68, 2
        _print(term.move_xy(x, y) + msg)
    if field_id == 1:
        # update key
        x, y = 67, 3
    elif field_id == 2:
        # update lives
        pass
    if len(msg) < max_width:
        _print(term.move_xy(x, y) + msg)
    else:
        log("msg too long from sidebar.")


def mov_player(term, mov):
    """
    Update the player position
    """
    global player_pos, found_key
    x, y = player_pos

    prev_pos = term.move_xy(x, y) + " "

    if mov == "j" or mov == "KEY_DOWN":
        y += 1
    if mov == "k" or mov == "KEY_UP":
        y -= 1
    if mov == "h" or mov == "KEY_LEFT":
        x -= 1
    if mov == "l" or mov == "KEY_RIGHT":
        x += 1

    # Check what player has encountered.
    if (char := [i for i in entity if (y, x) in entity[i]]) != []:
        put_msg(term, message[char[0]])
        if char[0] == "✕":
            found_key = True
            # Update key
            sidebar(term, 1, "1")
        if found_key and char[0] == "X":
            put_msg(term, message["completed"])
            # clear the current state and then start a new level
            game_layout(term, level=1)
    if (y, x) not in wall_pos:
        _print(prev_pos + term.move_xy(x, y) + PLAYER)
        player_pos = x, y


def main():
    """
    Just testing out an idea.
    """
    term = Terminal()
    # clear screen.
    with term.cbreak(), term.hidden_cursor():
        _print(term.clear + term.home)
        # print global frame.
        global_frame(term)
        # print global frame at given pos.
        game_layout(term, level=0, pos=(2, 1))
        # Fix this
        put_msg(term, "Hey ... Wake up.(press any key to continue)")
        inp = term.inkey()
        put_msg(term, "Welcome to the tutorial, we need to find a way to get out, now ...")
        inp = term.inkey()
        put_msg(term, "May be have a look around with your arrow-keys or hjkl.")
        inp = term.inkey()
        put_msg(term, "Hey, what's there? A door. May be have a look?")
        inp = term.inkey()
        sidebar(term, 1, "0")
        inp = ""
        while inp.lower() != "q":
            # get input key
            inp = term.inkey()
            # update the player position
            mov_player(term, inp.lower())
            # How to do message ? queue in async and then print ?
    print(term.clear + "BYE!")
    # Fix this
    global log_fd
    log_fd.close()


if __name__ == "__main__":
    main()
