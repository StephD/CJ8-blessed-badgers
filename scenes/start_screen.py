import blessed
import numpy as np
from numpy import sin, cos, pi

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
        a, b, _, d = self.vertices
        ab = a - b
        ad = a - d
        am = ((-points).T + a).T
        return (
            (0 < np.dot(am.T, ab))
            & (np.dot(am.T, ab) < np.dot(ab, ab))
            & (0 < np.dot(am.T, ad))
            & (np.dot(am.T, ad) < np.dot(ad, ad))
        ).T

    def update(
        self, screen_dimensions: tuple[tuple[float, float], tuple[float, float]]
    ) -> None:
        (lower_x, lower_y), (upper_x, upper_y) = screen_dimensions
        self.translate(self.velocity)
        self.rotate(self.angular_velocity)
        for vertex in self.vertices:
            """if not lower_x < vertex[1] < upper_x:
                self.velocity[1] *= -1
                break
            if not lower_y < vertex[0] < upper_y:
                self.velocity[0] *= -1
                break"""
            if vertex[1] < lower_x:
                self.velocity[1] = abs(self.velocity[1])
            if vertex[1] > upper_x:
                self.velocity[1] = -abs(self.velocity[1])
            if vertex[0] < lower_y:
                self.velocity[0] = abs(self.velocity[0])
            if vertex[0] > upper_y:
                self.velocity[0] = -abs(self.velocity[0])

    def to_be_painted(self, row: np.array, col: np.array) -> set[tuple[int, int]]:
        return set(
            (int(x), int(y))
            for x, y in np.transpose(self.contains(np.array([row, col])).nonzero())
        )


class StartScene(Scene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_lines = load_asset("title.txt")

        self.menu_items = [
            "New Game [n]",
            "Continue [c]",
            "Help [h]",
            "About [a]",
            "Version [v]",
            "Quit [q]",
        ]

    def render(self, term: blessed.Terminal) -> None:
        cols, rows = term.width, term.height
        rows -= 2
        cols -= 2

        num_squares = 6
        squares = [
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

        with term.cbreak(), term.hidden_cursor():
            row, col = np.indices((rows, cols))
            row = row[::-1]
            y_scale = 1 / 2
            x_scale = 1 / 2
            row = (row - rows // 2) * y_scale
            col = (col - cols // 2) / 3 * x_scale

            old_indices = set()

            print(term.home + term.clear)

            title_width = max(term.length(title_line) for title_line in self.title_lines)
            title_height = len(self.title_lines)
            title_start_col = (cols - title_width) // 2
            title_start_row = (rows - title_height) // 4
            print(term.move_xy(title_start_col, title_start_row), end="")
            for title_line in self.title_lines:
                print(title_line + term.move_down + term.move_left(len(title_line)), end="")

            title_indices = {
                (y + title_start_row, x + title_start_col)
                for x in range(title_width)
                for y in range(title_height)
            }

            menu_width = len((" " * 5).join(self.menu_items))
            menu_start_col = (cols - menu_width) // 2
            menu_row = rows - 3
            print(term.move_xy(menu_start_col, menu_row), end="")
            for menu_item in self.menu_items:
                print(menu_item + term.move_right(5), end="")

            menu_indices = {(menu_row, x + menu_start_col) for x in range(menu_width)}

            while term.inkey(timeout=0.02) != "q":

                indices_to_be_painted = set()
                for square in squares:
                    square.update(((col[0, 0], row[-1, 0]), (col[0, -1], row[0, 0])))
                    indices_to_be_painted |= square.to_be_painted(row, col)
                for y, x in (
                    indices_to_be_painted - old_indices - title_indices - menu_indices
                ):
                    print(term.move_xy(x, y) + chr(8226), end="", flush=True)
                for y, x in (
                    old_indices - indices_to_be_painted - title_indices - menu_indices
                ):
                    print(term.move_xy(x, y) + " ", end="", flush=True)
                old_indices = indices_to_be_painted

