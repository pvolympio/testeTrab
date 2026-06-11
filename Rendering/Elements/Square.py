from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (-1, 0, -1),
    (1, 0, -1),
    (1, 0, 1),
    (-1, 0, 1)
)
surfaces = (
    (0,1,2,3),
)
colors = (
    (1,0,0),
)

def draw_square(position):
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