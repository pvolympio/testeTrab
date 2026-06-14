import math
from OpenGL.GL import *

def draw_circle(position):
    x, y, z = position

    glPushMatrix()
    glTranslatef(x, y, z)

    glColor3f(1.0, 1.0, 0.0)

    glBegin(GL_TRIANGLE_FAN)

    glVertex3f(0.0, 0.0, 0.0)

    radius = 5
    segments = 100

    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        px = radius * math.cos(angle)
        py = radius * math.sin(angle)

        glVertex3f(px, py, 0.0)
    glEnd()

    glPopMatrix()