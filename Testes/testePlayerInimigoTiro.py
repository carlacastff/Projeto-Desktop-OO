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

# main.py (loop principal modificado)
while True:
    # Fecha o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    if not player.vivo and not player.explodindo:
            pygame.quit()
            exit()
    
    # Pega teclas e atualiza background
    teclas = pygame.key.get_pressed()
    tela.blit(background, (0,0))

    # POLIMORFISMO EM AÇÃO: Handle input apenas do Player
    player.entradaDoUsuário(teclas)

    # Controle de tiro player (mantido específico)
    tempoAtual = pygame.time.get_ticks()
    if teclas[pygame.K_SPACE] and tempoAtual - tUltimoTiroPl > intervaloPl:
        novoTiro = player.atirar()
        if novoTiro:
            tirosPlAtivos.append(novoTiro)
        tUltimoTiroPl = tempoAtual

    # Todos os objetos respondem ao mesmo método, mas cada um faz algo diferente
    player.update()
    for inimigo in inimigos:
        inimigo.update()
    for tiro in tirosPlAtivos + tirosInAtivos:
        tiro.update()

    # POLIMORFISMO: Draw de todos os objetos de forma uniforme
    for inimigo in inimigos:
        inimigo.printar(tela)
    for tiro in tirosPlAtivos + tirosInAtivos:
        tiro.printar(tela)
    player.printar(tela)

    inimigos_para_remover = []
    for inimigo in inimigos[:]:
        # Verifica colisão - isso inicia a explosão se houver colisão
        inimigo.colisão(tirosPlAtivos)
        terminou = inimigo.update()
        if terminou:
            inimigos_para_remover.append(inimigo)

    # Remove os inimigos depois do loop
    # Main loop - após a criação dos inimigos e antes do display.flip()

    # COLISÃO DO PLAYER - verifica a cada frame
    if player.vivo:
        player.colisão(tirosInAtivos)

    # Remove os inimigos depois do loop
    for inimigo in inimigos_para_remover:
        inimigos.remove(inimigo)

    # Tiro inimigo
    if tempoAtual - tUltimoTiroIn > intervaloIn and inimigos:
        randomIn = random.randint(0, len(inimigos)-1)
        novoTiroIn = inimigos[randomIn].atirar(random.randint(1,10))
        if novoTiroIn:
            tirosInAtivos.append(novoTiroIn)
        tUltimoTiroIn = tempoAtual

    # Remove tiros inativos
    tirosPlAtivos = [t for t in tirosPlAtivos if t.ativo]
    tirosInAtivos = [t for t in tirosInAtivos if t.ativo]

    pygame.display.flip()
    clock.tick(60)