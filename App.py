import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Camera import handle_camera, initialize_camera
from Rendering.Scene import draw_scene, initialize_scene

from Filtros.luksguin import borramento
from Filtros.luksguin import Objeto3D
from Filtros.luksguin import cubo
from Filtros.luksguin import sphere
from Filtros.luksguin import alterarBrilho

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
    initialize_scene()

def run_app():
    #Loop principal da aplicação
    running = True

    borrado = False
    brilho = 0

    canoArma = Objeto3D(cubo, (.809,-.6,-2.2), (1,0,0), 0, .15,.7,.15)
    gatilhoArma = Objeto3D(cubo, (.8,-.8,-1.7), (1,1,0), 0, .15,.3,.15)
    mira = Objeto3D(sphere, (0,0,-1), (45,12,0), 0, .005, 30, 30)

    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    borrado = not borrado

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o and brilho >= -260:
                    brilho -= 10
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and brilho <= 260:
                    brilho += 10

        pressed_keys = pygame.key.get_pressed()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        canoArma.angulo = 95
        canoArma.spawn()

        gatilhoArma.angulo = 10
        gatilhoArma.spawn()

        mira.spawn()

        handle_camera(pressed_keys)

        draw_scene()
        
        if borrado: borramento(WIDTH, HEIGHT, 3)
        alterarBrilho(WIDTH, HEIGHT, brilho)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()