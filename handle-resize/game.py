import os
import sys

from blessed import Terminal

class GameException(Exception):
    """Base class for exceptions in this module."""
    pass

class Game():
    '''
    Test game class implementing all necessary methods.
    '''
    PLAYER = "@"
    def __init__(self, term=Terminal()) -> None:
        self.term = term
        self.obstacles = set()
        self.message_pos = set()
        # Main message: Look around in the game.
        self.message =  {"X": "Syntax to print in python is print('Hello, World')",
                    "M": "To solve the current challenge understand the syntax", 
                    "A": "Whats the code to print Hello in python ?"}
        self.current_map = None
        self.pos_x = 2
        self.pos_y = 2

    def get_neighbour(self, i, j) -> set:
        '''
        Small helper function
        '''
        pos = set()
        for i in range(i-1, i+1):
            for j in range(j-1, j+1):
                # Specify max width and max height
                if i != j and (0 < j < 21 and 0 < i < 21):
                    continue
                else:
                    pos.add((i, j))
        return pos

    def load_map(self, level=0) -> str:
        '''
        Load map from the directory according to the specified level.
        Note: Assuming level is safe and has the type integer.
        '''
        with open(f"maps/{level}.txt") as map_fd:
            map_data = map_fd.read()

        if len(map_data) < 0:
            raise GameException("map loading")
            sys.exit(1)

        self.current_map = map_data
        map_data = map_data.split("\n")
        obstacles = set()
        for i in range(len(map_data)):
            for j in range(len(map_data[i])):
                if map_data[i][j] == " ":
                    continue
                elif map_data[i][j] in ["M", "A", "X"]:
                    pos = self.get_neighbour(i, j)
                    self.message_pos.update(pos)
                obstacles.add((i, j))

        # Update obstacles
        self.obstacles = obstacles

    def render(self):
        '''
        Render the game.
        '''
        if not self.current_map:
            raise GameException("Map is not loaded")

        player = self.term.move_xy(self.pos_x, self.pos_y) + self.PLAYER
        print(self.term.home + self.term.clear + self.current_map + player, end="", flush=True)

    def move_player(self, mov):
        '''
        Move player.
        '''
        # Make a copy of the position of the player.
        pos_x, pos_y = self.pos_x, self.pos_y

        # Erase the current position.
        term_erase = self.term.move_xy(pos_x, pos_y) + " "

        # Update the position.
        if mov == "j":
            pos_y += 1
        if mov == "k":
            pos_y -= 1
        if mov == "h":
            pos_x -= 1
        if mov == "l":
            pos_x += 1

        # Check the orientation what is x and y ?
        if (pos_y, pos_x) not in self.obstacles:
            term_player = self.term.move_xy(pos_x, pos_y) + self.PLAYER
            print(term_erase + term_player, end="", flush=True)
            # Update the position of the player.
            self.pos_x, self.pos_y = pos_x, pos_y
        elif (pos_y, pos_x) in self.message_pos:
            term_player = self.term.move_xy(self.pos_x, self.pos_y) + self.PLAYER
            msg = "┌" + "─" * 21 + "┐\n"
            for i in range(10):
                msg +=  "│" + " " * 21 + "│\n" 
            msg += "└" + "─" * 21 + "┘\n"
            print(self.term.clear + self.current_map + msg, end="", flush=True)
        
    def display_msg(self) -> None:
        pass


if __name__ == "__main__":
    '''
    Main
    '''
    game = Game()
    game.load_map()
    game.render()
    inp = ""
    with game.term.cbreak(), game.term.hidden_cursor():
        while inp != "q":
            inp = game.term.inkey().lower()
            game.move_player(inp)
        print(game.term.clear, "BYE!")
