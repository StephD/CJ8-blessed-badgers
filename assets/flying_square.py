import numpy as np
from numpy import cos, pi, sin


class Square:
    """Square class will display a rotating square for the start menu"""

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
