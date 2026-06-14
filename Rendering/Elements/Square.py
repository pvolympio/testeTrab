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

def draw_square(position, color, size_multiplier = 1):
    x, y, z = position[0], position[1], position[2]

    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size_multiplier, size_multiplier, size_multiplier)

    #Desenha as faces do cubo
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(color)
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()