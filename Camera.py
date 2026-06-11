import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#Movimento da câmera
CENTER_DISTANCE = 10
MOVE_SPEED = 0.1
eye = [0, 0, 0]
center = [0, 0, CENTER_DISTANCE]
up = [0, 1, 0]

#Rotação da câmera
ROTATE_SPEED = 2
x_rotation = 0
y_rotation = 0

def initialize_camera(width: int, height: int):
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(60, width / height, 0.1, 50)

    glMatrixMode(GL_MODELVIEW)

def handle_camera(pressed_keys):
    rotate_camera(pressed_keys)
    move_camera(pressed_keys)
    
    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])

def rotate_camera(pressed_keys):
    global x_rotation, y_rotation

    angular_speed = math.radians(ROTATE_SPEED)

    if pressed_keys[pygame.K_LEFT]:
        x_rotation -= angular_speed
    if pressed_keys[pygame.K_RIGHT]:
        x_rotation += angular_speed
    if pressed_keys[pygame.K_UP]:
        y_rotation += angular_speed
    if pressed_keys[pygame.K_DOWN]:
        y_rotation -= angular_speed

    dx = CENTER_DISTANCE * math.cos(y_rotation) * math.sin(x_rotation)
    dy = CENTER_DISTANCE * math.sin(y_rotation)
    dz = -CENTER_DISTANCE * math.cos(y_rotation) * math.cos(x_rotation)

    center[0] = eye[0] + dx
    center[1] = eye[1] + dy
    center[2] = eye[2] + dz

def move_camera(pressed_keys):
    forward_x = center[0] - eye[0]
    forward_z = center[2] - eye[2]

    forward_x /= CENTER_DISTANCE
    forward_z /= CENTER_DISTANCE

    right_x = -forward_z
    right_z = forward_x

    #Move a posição da câmera
    if pressed_keys[pygame.K_a]:
        eye[0] -= right_x * MOVE_SPEED
        eye[2] -= right_z * MOVE_SPEED
        center[0] -= right_x * MOVE_SPEED
        center[2] -= right_z * MOVE_SPEED

    if pressed_keys[pygame.K_d]:
        eye[0] += right_x * MOVE_SPEED
        eye[2] += right_z * MOVE_SPEED
        center[0] += right_x * MOVE_SPEED
        center[2] += right_z * MOVE_SPEED

    if pressed_keys[pygame.K_w]:
        eye[0] += forward_x * MOVE_SPEED
        eye[2] += forward_z * MOVE_SPEED
        center[0] += forward_x * MOVE_SPEED
        center[2] += forward_z * MOVE_SPEED

    if pressed_keys[pygame.K_s]:
        eye[0] -= forward_x * MOVE_SPEED
        eye[2] -= forward_z * MOVE_SPEED
        center[0] -= forward_x * MOVE_SPEED
        center[2] -= forward_z * MOVE_SPEED