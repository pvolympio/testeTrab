import random
from OpenGL.GL import *
from OpenGL.GLU import *

from Rendering.Elements.Square import draw_square
from Rendering.Elements.Tree import draw_tree
from Rendering.Elements.Cloud import draw_cloud
from Rendering.Elements.Sun import draw_sun

MATRIX_SIZE = 20
MATRIX_CENTER = (0, -2, 0)

SQUARE_SIZE = 1

cloud_matrix = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
tree_matrix = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
lake_matrix = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
grass_matrix = [[1 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

def initialize_scene():
    global cloud_matrix, tree_matrix, lake_matrix
    
    random_i = random.randint(3, MATRIX_SIZE - 4)
    random_j = random.randint(3, MATRIX_SIZE - 4)
    
    for x in range(random_i - 3, random_i + 4):
        for y in range(random_j - 3, random_j + 4):
            if x > random_i - 1 and x < random_i + 2 or y > random_j - 1 and y < random_j + 2:
                lake_matrix[x][y] = 1
            elif random.random() <= 0.3:
                lake_matrix[x][y] = 1

    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            if random.random() <= 0.1:
                cloud_matrix[i][j] = 1
            else:
                cloud_matrix[i][j] = 0

            if lake_matrix[i][j] == 0 and random.random() <= 0.1:
                tree_matrix[i][j] = 1
                grass_matrix[i][j] = 0
            else:
                tree_matrix[i][j] = 0

                if random.random() <= 0.1:
                    grass_matrix[i][j] = 0

def draw_scene():
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            #Desenha os elementos terrestres (chão, lago)
            pos = (
                MATRIX_CENTER[0] + (-i * (SQUARE_SIZE + 1)),
                MATRIX_CENTER[1],
                MATRIX_CENTER[2] + (-j * (SQUARE_SIZE + 1))
            )
            if lake_matrix[i][j] == 1:
                draw_square(pos, (0, 0, 0.9))
            elif grass_matrix[i][j] == 0:
                draw_square(pos, (0.5, 0.35, 0.2))
            else:
                draw_square(pos, (0, 0.5, 0))

            #Desenha as árvores
            if tree_matrix[i][j] == 1:
                pos = (
                    MATRIX_CENTER[0] + (-i * (SQUARE_SIZE + 1)),
                    MATRIX_CENTER[1] + 1,
                    MATRIX_CENTER[2] + (-j * (SQUARE_SIZE + 1))
                )
                draw_tree(pos)

            #Desenha as nuvens
            if cloud_matrix[i][j] == 1:
                pos = (
                    (MATRIX_CENTER[0] + (i * 10)) - MATRIX_SIZE/2 * 10,
                    60,
                    (MATRIX_CENTER[2] + (j * 10)) - MATRIX_SIZE/2 * 10
                )
                draw_cloud(pos, MATRIX_SIZE * 10)            

    #Desenha o sol
    sunPos = (0, 70, 60)
    draw_sun(sunPos)