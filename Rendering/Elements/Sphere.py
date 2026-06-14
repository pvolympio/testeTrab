import math
from OpenGL.GL import *

def draw_sphere(position, radius=5, stacks=10, slices=10):
    x, y, z = position

    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 1.0, 0.0)

    for i in range(stacks):
        lat0 = math.pi * (-0.5 + i / stacks)
        lat1 = math.pi * (-0.5 + (i + 1) / stacks)

        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * j / slices
            x_val = math.cos(lng)
            y_val = math.sin(lng)

            glNormal3f(x_val * zr0, y_val * zr0, z0)
            glVertex3f(radius * x_val * zr0, radius * y_val * zr0, radius * z0)

            glNormal3f(x_val * zr1, y_val * zr1, z1)
            glVertex3f(radius * x_val * zr1, radius * y_val * zr1, radius * z1)
        glEnd()

    glPopMatrix()