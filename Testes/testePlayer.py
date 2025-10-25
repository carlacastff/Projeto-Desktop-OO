import pygame
from pygame.locals import*
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.player import Player


#inicia pygame
pygame.init() 

tela = pygame.display.set_mode((1280, 720))                     #cria tela com tamanho 1280, 720
background = pygame.image.load('Imagens/backgrounds/6.png')     #cria background
player = Player()                                               #cria um player

clock = pygame.time.Clock()  #cria um temporizador para o laço while

while True:                 
    for event in pygame.event.get():
        if event.type == QUIT:  #fecha o jogo
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()   #teclas pressionadas
    
    player.entradaDoUsuário(teclas) #movimentação
    if teclas[pygame.K_SPACE]:      #explosão!
        player.explosão()

    tela.blit(background, (0,0))    #atualiza background
    player.printar(tela)            #printa sprite do player
    player.update()                 #atualiza sprite do player explodindo
    pygame.display.flip()           #atualiza tela
    clock.tick(60)  #60 FPS
pygame.quit()