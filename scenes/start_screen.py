import blessed
import numpy as np
from numpy import cos, pi, sin

from assets import load_asset
from scenes.utils import Scene


class Square:
    vertices: np.array
    center: np.array
    rotation: float
    velocity: np.array
    angular_velocity: float

    def __init__(self, vertices: np.array, velocity: np.array, angular_velocity: float):
        self.vertices = vertices
        self.center = np.array(
            [
                sum(point[0] for point in vertices) / len(vertices),
                sum(point[1] for point in vertices) / len(vertices),
            ]
        )
        self.rotation = 0
        self.velocity = velocity
        self.angular_velocity = angular_velocity

    def rotate(self, delta_theta: float) -> None:
        self.rotation = (self.rotation + delta_theta) % (2 * pi)
        rotation_matrix = np.array(
            [
                [cos(delta_theta), -sin(delta_theta)],
                [sin(delta_theta), cos(delta_theta)],
            ]
        )
        local_positions = self.vertices - self.center
        self.vertices = (rotation_matrix @ local_positions.T).T + self.center

    def translate(self, delta_pos: np.array) -> None:
        self.center += delta_pos
        self.vertices += delta_pos

    def contains(self, points: np.array) -> np.array:
        """https://math.stackexchange.com/a/190373"""
        a_coordinates, b_coordinates, _, d_coordinates = self.vertices
        ab_vector = a_coordinates - b_coordinates
        ad_vector = a_coordinates - d_coordinates
        am_vector = ((-points).T + a_coordinates).T
        return (
            (np.dot(am_vector.T, ab_vector) > 0)
            & (np.dot(am_vector.T, ab_vector) < np.dot(ab_vector, ab_vector))
            & (np.dot(am_vector.T, ad_vector) > 0)
            & (np.dot(am_vector.T, ad_vector) < np.dot(ad_vector, ad_vector))
        ).T

    def update(self, screen_dimensions: tuple[tuple[float, float], tuple[float, float]]) -> None:
        (lower_x, lower_y), (upper_x, upper_y) = screen_dimensions
        self.translate(self.velocity)
        self.rotate(self.angular_velocity)
        for vertex in self.vertices:
            if vertex[1] < lower_x:
                self.velocity[1] = abs(self.velocity[1])
            if vertex[1] > upper_x:
                self.velocity[1] = -abs(self.velocity[1])
            if vertex[0] < lower_y:
                self.velocity[0] = abs(self.velocity[0])
            if vertex[0] > upper_y:
                self.velocity[0] = -abs(self.velocity[0])

    def to_be_painted(self, row: np.array, col: np.array) -> set[tuple[int, int]]:
        return set((int(x), int(y)) for x, y in np.transpose(self.contains(np.array([row, col])).nonzero()))


def make_title(term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
    """Draws the title in the terminal, returning the coordinates where it printed."""
    title_lines = load_asset("title.txt")
    title_width = max(term.length(title_line) for title_line in title_lines)
    title_height = len(title_lines)
    title_start_col = (cols - title_width) // 2
    title_start_row = (rows - title_height) // 4
    print(term.move_xy(title_start_col, title_start_row), end="")
    for title_line in title_lines:
        print(title_line + term.move_down + term.move_left(len(title_line)), end="")

    return {(y + title_start_row, x + title_start_col) for x in range(title_width) for y in range(title_height)}


def make_menu(term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
    """Draws the menu in the terminal, returning the coordinates where it printed."""
    menu_items = [
        "New Game [n]",
        "Continue [c]",
        "Help [h]",
        "About [a]",
        "Version [v]",
        "Quit [q]",
    ]
    menu_width = len((" " * 5).join(menu_items))
    menu_start_col = (cols - menu_width) // 2
    menu_row = rows - 3
    print(term.move_xy(menu_start_col, menu_row), end="")
    for menu_item in menu_items:
        print(menu_item + term.move_right(5), end="")

    return {(menu_row, x + menu_start_col) for x in range(menu_width)}


class StartScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        num_squares = 6
        self.squares = [
            Square(
                np.array(
                    [
                        [-2.0, 1.0],
                        [-2.0, 5.0],
                        [2.0, 5.0],
                        [2.0, 1.0],
                    ]
                ),
                np.array(
                    [
                        np.random.uniform(0.2, 0.3) * np.random.choice([-1, 1]),
                        np.random.uniform(0.2, 0.3) * np.random.choice([-1, 1]),
                    ]
                ),
                np.random.uniform(0.02, 0.05) * np.random.choice([-1, 1]),
            )
            for _ in range(num_squares)
        ]

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height
        rows -= 2
        cols -= 2

        with term.cbreak(), term.hidden_cursor():
            row, col = np.indices((rows, cols))
            row = row[::-1]
            row = (row - rows // 2) * 1 / 2
            col = (col - cols // 2) / 3 * 1 / 2

            old_indices = set()

            print(term.home + term.clear)

            title_indices = make_title(term, rows, cols)
            menu_indices = make_menu(term, rows, cols)

            while term.inkey(timeout=0.02) != "q":

                indices_to_be_painted = set()
                for square in self.squares:
                    square.update(((col[0, 0], row[-1, 0]), (col[0, -1], row[0, 0])))
                    indices_to_be_painted |= square.to_be_painted(row, col)
                for y_index, x_index in indices_to_be_painted - old_indices - title_indices - menu_indices:
                    print(term.move_xy(x_index, y_index) + chr(8226), end="", flush=True)
                for y_index, x_index in old_indices - indices_to_be_painted - title_indices - menu_indices:
                    print(term.move_xy(x_index, y_index) + " ", end="", flush=True)
                old_indices = indices_to_be_painted
