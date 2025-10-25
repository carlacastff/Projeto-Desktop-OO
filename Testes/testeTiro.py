import pygame
from pygame.locals import*
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.inimigo import Inimigo
from Classes.player import Player
from Classes.tiro import Tiro

#inicializa pygame
pygame.init() 

#cria tela e imagem de fundo (background)
tela = pygame.display.set_mode((1280, 720))
background = pygame.image.load('Imagens/backgrounds/6.png')


inimigo = Inimigo(650, 180)
player = Player()

#tiros
tUltimoTiroIn = 0
tUltimoTiroPl = 0
intervaloIn = 3000
intervaloPl = 500
tempoAtual = 0
tirosInAtivos = []
tirosPlAtivos = []

#temporizador para o laço while
clock = pygame.time.Clock()

while True:
    # Fecha o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    teclas = pygame.key.get_pressed()       # Pega teclas
    tela.blit(background, (0,0))            # atualiza background


    player.entradaDoUsuário(teclas)     #movimentação

    tempoAtual = pygame.time.get_ticks()
    if teclas[pygame.K_SPACE] and tempoAtual - tUltimoTiroPl > intervaloPl:     #cria tiros do player
        novoTiro = player.atirar()
        if novoTiro:
            tirosPlAtivos.append(novoTiro)
        tUltimoTiroPl = tempoAtual

    #printar todos os objetos na tela
    inimigo.printar(tela)
    player.printar(tela)
    for tiro in tirosPlAtivos + tirosInAtivos:
        tiro.printar(tela)


    if tempoAtual - tUltimoTiroIn > intervaloIn:           #cria tiros do inimigo
        novoTiroIn = inimigo.atirar(random.randint(1,10))
        if novoTiroIn:
            tirosInAtivos.append(novoTiroIn)
        tUltimoTiroIn = tempoAtual

    for tiro in tirosPlAtivos[:]:             #remove tiros inativos do player
        if not tiro.update():
            tirosPlAtivos.remove(tiro)
    for tiro in tirosInAtivos[:]:             #remove tiros inativos do inimigo
        if not tiro.update():
            tirosInAtivos.remove(tiro)

    pygame.display.flip()
    clock.tick(60)