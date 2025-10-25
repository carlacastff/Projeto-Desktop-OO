import pygame
from pygame.locals import*
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.inimigo import Inimigo

#inicia pygame
pygame.init() 

tela = pygame.display.set_mode((1280, 720))               #cria tela com tamanho 1280, 720
background = pygame.image.load('Imagens/backgrounds/6.png')     #cria background

inimigo1 = Inimigo(1280/2, 150)

clock = pygame.time.Clock()             #cria um temporizador para o laço while

while True:                 
    for event in pygame.event.get():
        if event.type == QUIT:          #fecha o jogo
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()
    tela.blit(background, (0,0))        #atualiza background
    inimigo1.printar(tela)

    if teclas[pygame.K_SPACE]:
        inimigo1.explosão()

    inimigo1.update()
    pygame.display.flip()           #atualiza tela
    clock.tick(60)                  #60 FPS
pygame.quit()