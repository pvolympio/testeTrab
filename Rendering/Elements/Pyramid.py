import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    ( 1, -1,  1), 
    ( 1, -1, -1),
    (-1, -1, -1),
    (-1, -1,  1), 
    ( 0,  1,  0)  
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
colors = (
    (1, 0.5, 0),  
    (1, 0, 0),    
    (0, 1, 0),    
    (0, 0, 1),    
    (0.5, 0.5, 0),
    (0.5, 0.5, 0) 
)

def draw_pyramid(position):
    x, y, z = position[0], position[1], position[2]

    glPushMatrix()
    glTranslatef(x, y, z)

    glBegin(GL_TRIANGLES)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3f(1, 1, 1)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()