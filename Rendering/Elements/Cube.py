from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)
edges = (
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,7), (7,6), (6,4),
    (0,4), (1,5), (2,7), (3,6)
)
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (0,1,1),
)

def draw_cube(position):
    x, y, z = position[0], position[1], position[2]

    glPushMatrix()
    glTranslatef(x, y, z)

    #Desenha as faces do cubo
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()