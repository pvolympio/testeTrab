import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from teste.Camera import handle_camera, initialize_camera
from teste.Rendering.Scene import draw_scene

WIDTH, HEIGHT = 1024, 768
TITLE = "Trabalho CMCO05"
        
FPS = 60
clock = 0

def main():
    initialize_app()
    run_app()

def initialize_app():
    #Configurações iniciais da aplicação
    pygame.init

    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(TITLE)

    global clock
    clock = pygame.time.Clock()

    initialize_camera(WIDTH, HEIGHT)

def run_app():
    #Loop principal da aplicação
    running = True;

    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        handle_camera(pressed_keys)

        draw_scene()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()