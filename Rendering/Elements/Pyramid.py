import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    ( 1, -1,  1), 
    ( 1, -1, -1),
    (-1, -1, -1),
    (-1, -1,  1), 
    ( 0,  4,  0)  
)
edges = (
    (0,1), (1,2), (2,3), (3,0), 
    (0,4), (1,4), (2,4), (3,4)
)
surfaces = (
    (0,1,4),  
    (1,2,4),  
    (2,3,4),  
    (3,0,4),  
    (0,2,1),  
    (0,3,2)  
)

def draw_pyramid(position, color):
    x, y, z = position[0], position[1], position[2]

    glPushMatrix()
    glTranslatef(x, y, z)

    glBegin(GL_TRIANGLES)
    for i, surface in enumerate(surfaces):
        glColor3fv(color)
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()