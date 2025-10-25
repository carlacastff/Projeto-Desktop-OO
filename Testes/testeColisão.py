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

#função cria inimigos
def criação(qtd, y, espaçamento):
    inimigos = []
    for i in range(qtd):
        x = (i * espaçamento) + 300
        inimigos.append(Inimigo(x, y))     
    return inimigos

#cria player e inimigos
qtdIn = 5
inimigos = criação(qtdIn, 150, 180)
player = Player()

#tiros
tUltimoTiroIn = 0
tUltimoTiroPl = 0
intervaloIn = 1000
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
    
    if not player.vivo and not player.explodindo:
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

    # Atualiza explosão
    player.update()
    for inimigo in inimigos:
        inimigo.update()

    # Printar na tela
    for inimigo in inimigos:
        inimigo.printar(tela)
    for tiro in tirosPlAtivos + tirosInAtivos:
        tiro.printar(tela)
    player.printar(tela)

    RemoverIn = []
    for inimigo in inimigos[:]:
        inimigo.colisão(tirosPlAtivos)
        terminou = inimigo.update()
        if terminou:
            RemoverIn.append(inimigo)

    # Remove os inimigos depois do loop
    for inimigo in RemoverIn:
        inimigos.remove(inimigo)

    if player.vivo:                 
        player.colisão(tirosInAtivos)

    # Tiro inimigo
    if tempoAtual - tUltimoTiroIn > intervaloIn and inimigos:
        randomIn = random.randint(0, len(inimigos)-1)
        novoTiroIn = inimigos[randomIn].atirar(random.randint(1,10))
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