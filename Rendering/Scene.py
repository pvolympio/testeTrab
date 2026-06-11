import random

from teste.Rendering.Elements.Cube import draw_cube
from teste.Rendering.Elements.Square import draw_square

MATRIX_SIZE = 20
MATRIX_CENTER = (0, -2, 0)

SQUARE_SIZE = 1

def draw_scene():
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            pos = (
                MATRIX_CENTER[0] + (-i * (SQUARE_SIZE + 1)),
                MATRIX_CENTER[1],
                MATRIX_CENTER[2] + (-j * (SQUARE_SIZE + 1))
            )
            draw_square(pos)

            random = random.random()
            print(random)