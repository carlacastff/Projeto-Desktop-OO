import pygame
from pygame.locals import*
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.sprite import Sprite


#inicia pygame
pygame.init() 

tela = pygame.display.set_mode((1280, 720)) #cria janela com tamanho 1280, 720

#cria sprite
sprite1 = Sprite('Imagens/Sprites/player/x-wing.png', 1280/2, 550)

while True:                 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    sprite1.printar(tela)

    pygame.display.flip()

pygame.quit()