import blessed

from scenes import StartScene


def main():
    term = blessed.Terminal()
    StartScene().render(term)


main()
