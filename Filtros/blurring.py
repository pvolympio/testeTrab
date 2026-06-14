import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random

import cv2
import numpy as np

seedRandom = random.randint(0, 1000)
display = (1000, 800)

intensidadeBlur = 7
kernel_media = np.ones((intensidadeBlur, intensidadeBlur)) / intensidadeBlur ** 2

# def ponto(size, r, g, b, x, y, z):
#     glPointSize(size) # Tamanho
        
#     glBegin(GL_POINTS)

#     glColor3f(r, g, b) # Cor
#     glVertex3f(x, y, z) # Coordenadas
        
#     glEnd()

def aresta(modo, r, g, b, vertex):
    glPointSize(1) # Tamanho
    
    if(modo == 'Pares'): glBegin(GL_LINES)
    elif(modo == 'Sequencia'): glBegin(GL_LINE_STRIP)
    elif(modo == 'Loop'): glBegin(GL_LINE_LOOP)

    glColor3f(r, g, b) # Cor

    for v in vertex:
        glVertex3f(v[0], v[1], v[2])
    
    glEnd()

def poligono(modo, vertex):
    glShadeModel(GL_FLAT)

    if modo == 'TIsolados': glBegin(GL_TRIANGLES)
    elif modo == 'TConectados': glBegin(GL_TRIANGLE_STRIP)
    elif modo == 'TVentilador': glBegin(GL_TRIANGLE_FAN)
    elif modo == 'QIsolados': glBegin(GL_QUADS)
    elif modo == 'QConectados': glBegin(GL_QUAD_STRIP)
    elif modo == 'Poligonos': glBegin(GL_POLYGON)

    random.seed(seedRandom)

    for v in vertex:
        glColor3f(random.random(), random.random(), random.random())
        glVertex3f(v[0], v[1], v[2])

    glEnd()

def cubo(tamanho):
    vertices = (
        (-tamanho, -tamanho, tamanho), # 0: Frente-Baixo-Esquerda
        (tamanho, -tamanho, tamanho), # 1: Frente-Baixo-Direita
        (tamanho, tamanho, tamanho), # 2: Frente-Cima-Direita
        (-tamanho, tamanho, tamanho), # 3: Frente-Cima-Esquerda
        (-tamanho, -tamanho, -tamanho), # 4: Trás-Baixo-Esquerda
        (tamanho, -tamanho, -tamanho), # 5: Trás-Baixo-Direita
        (tamanho, tamanho, -tamanho), # 6: Trás-Cima-Direita
        (-tamanho, tamanho, -tamanho)  # 7: Trás-Cima-Esquerda
    )

    #Ligando os pontos
    faces = (
        (0, 1, 2, 3), # Frente
        (5, 4, 7, 6), # Trás
        (3, 2, 6, 7), # Topo
        (4, 5, 1, 0), # Fundo
        (1, 5, 6, 2), # Direita
        (4, 0, 3, 7)  # Esquerda
    )

    glBegin(GL_QUADS)
    random.seed(seedRandom + 1)

    for face in faces:
        glColor3f(random.random(), random.random(), random.random()) 
        
        for v in face:
            glVertex3fv(vertices[v])
            
    glEnd()

def borramento():
    # Captura a tela;
    buffer = glReadPixels(0, 0, display[0], display[1], GL_RGB, GL_UNSIGNED_BYTE) #Lê os pixeis da tela;
    imagem = np.frombuffer(buffer, dtype=np.uint8).reshape((display[1], display[0], 3)) #Transforma em uma imagem;
    
    imagem_filtrada = cv2.filter2D(imagem, -1, kernel_media) # Aplica o filtro;

    #Coloca a lente 3D em segundo plano e vira 2D;
    # glMatrixMode(GL_PROJECTION)
    # glPushMatrix()
    # glLoadIdentity()
    
    #Colocas as posições e rotações 3D em segundo plano e vira 2D;
    # glMatrixMode(GL_MODELVIEW)
    # glPushMatrix()
    # glLoadIdentity()

    # Posiciona o "carimbo" no canto inferior esquerdo (-1, -1)
    #glRasterPos2f(-1.5, -1.0)
    
    glDrawPixels(display[0], display[1], GL_RGB, GL_UNSIGNED_BYTE, imagem_filtrada.tobytes()) #Cola a imagem filtrada por cima de tudo;

    #Devolve as configurações 3D;
    # glPopMatrix()
    # glMatrixMode(GL_PROJECTION)
    # glPopMatrix()
    # glMatrixMode(GL_MODELVIEW)

class Objeto3D:
    def __init__(self, tipoObjeto, posicao, rotacao, velocidadeRotacao, *args):
        self.tipoObjeto = tipoObjeto
        self.posicao = posicao
        self.rotacao = rotacao
        self.velocidadeRotacao = velocidadeRotacao
        self.argumentos = args
        
        self.angulo = 0

    def spawn(self):
        self.angulo += self.velocidadeRotacao
        
        glPushMatrix()
        glTranslatef(self.posicao[0], self.posicao[1], self.posicao[2])

        glRotatef(self.angulo, self.rotacao[0], self.rotacao[1], self.rotacao[2])
            
        self.tipoObjeto(*self.argumentos)
        glPopMatrix()

def main():
    pygame.init()

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Trabalinho")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    
    # Gap entre o desenho e a visão;
    glTranslatef(0.0, 0.0, -5.0)

    background = Objeto3D(poligono, (0,0,0), (0,0,0), 0, 'QConectados', [[-10, -10, -10], [10, -10, -10], [-10, 0, -10], [10, 0, -10], [-10, 10, -10], [10, 10, -10]])
    cuboObj = Objeto3D(cubo, (0,0,0), (-56,23,-76), .5, 1)

    borrado = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    borrado = not borrado

        glEnable(GL_DEPTH_TEST) # Profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpar a cena
        #glRotatef(1, 1, 1, 0) # Rotaciona o mundo todo;
        
        background.spawn()
        cuboObj.spawn()

        if(borrado): borramento()

        # Troca os buffers para atualizar o quadro
        pygame.display.flip()
        
        # Limita os frames
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
