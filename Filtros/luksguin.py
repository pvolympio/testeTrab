import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

import random

import cv2
import numpy as np

seedRandom = random.randint(0, 1000)
display = (1000, 800)

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

def cubo(x, y, z):
    vertices = (
        (-x, -y, z), # 0: Frente-Baixo-Esquerda
        (x, -y, z), # 1: Frente-Baixo-Direita
        (x, y, z), # 2: Frente-Cima-Direita
        (-x, y, z), # 3: Frente-Cima-Esquerda
        (-x, -y, -z), # 4: Trás-Baixo-Esquerda
        (x, -y, -z), # 5: Trás-Baixo-Direita
        (x, y, -z), # 6: Trás-Cima-Direita
        (-x, y, -z)  # 7: Trás-Cima-Esquerda
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

def sphere(raio, stacks, slices):
    glColor3f(1, 0, 0)

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
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(raio * x * zr0, raio * y * zr0, raio * z0)

            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(raio * x * zr1, raio * y * zr1, raio * z1)
        glEnd()

def borramento(largura, altura, intensidade):
    matrizMedia = np.ones((intensidade, intensidade)) / intensidade ** 2

    buffer = glReadPixels(0, 0, largura, altura, GL_RGB, GL_UNSIGNED_BYTE) # Captura a tela;
    imagem = np.frombuffer(buffer, dtype=np.uint8).reshape((altura, largura, 3)) # Conversão;
    
    imagem_filtrada = cv2.filter2D(imagem, -1, matrizMedia) # Aplica o filtro;

    glDrawPixels(largura, altura, GL_RGB, GL_UNSIGNED_BYTE, imagem_filtrada.tobytes()) # Cola a imagem filtrada;

def alterarBrilho(largura, altura, intensidade):
    # Captura a tela
    buffer = glReadPixels(0, 0, largura, altura, GL_RGB, GL_UNSIGNED_BYTE) 
    imagem = np.frombuffer(buffer, dtype=np.uint8).reshape((altura, largura, 3)) 
    
    # 1. Converte pra int16 e soma o brilho no mesmo instante (Sem chance de dar a volta)
    # 2. Já aplica o clip na resposta do cálculo
    # 3. Devolve como uint8 para a placa de vídeo
    imagemAlterada = np.clip(imagem.astype(np.int16) + intensidade, 0, 255).astype(np.uint8)

    # Cola a imagem
    glDrawPixels(largura, altura, GL_RGB, GL_UNSIGNED_BYTE, imagemAlterada.tobytes())

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
    sphereTest = Objeto3D(sphere, (0,0,0), (45,12,0), 1, 1, 30, 30)

    brilho = 0
    borrado = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    borrado = not borrado

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o and brilho >= -260:
                    brilho -= 10
                    print(brilho)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and brilho <= 260:
                    brilho += 10
                    print(brilho)

        glEnable(GL_DEPTH_TEST) # Profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpar a cena
        
        background.spawn()
        #cuboObj.spawn()
        sphereTest.spawn()

        if(borrado): borramento(display[0], display[1])
        alterarBrilho(display[0], display[1], brilho)

        # Troca os buffers para atualizar o quadro
        pygame.display.flip()
        
        # Limita os frames
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
