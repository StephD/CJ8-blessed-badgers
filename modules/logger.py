FILENAME = "game_log.log"


def log(message: str, title: str = "") -> None:
    """
    Write a message with/without title in a log file

    read the file : tail -f game_log.log
    """
    if title != "":
        title = title.title() + " : "
    message = message or "*None"
    try:
        with open(FILENAME, "a") as file:
            file.write(title + message + "\n")
    except FileExistsError:
        with open(FILENAME, "w") as file:
            file.write(title + message + "\n")
