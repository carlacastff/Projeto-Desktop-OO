import pygame
from pygame.locals import*
from Classes.inimigo import Inimigo
from Classes.player import Player
from Classes.tiro import Tiro
import random

#inicia pygame
pygame.init() 
pygame.font.init()
pygame.mixer.init()

tela = pygame.display.set_mode((1280, 720)) #cria tela com tamanho 1280, 720
pygame.display.set_caption('Space Invaders: Star Wars') #define nome da janela
pygame.mixer.music.load('Música e Sons/musicas-_Mandalorian-e-Andor.mp3') #musica
somTeclas = pygame.mixer.Sound('Música e Sons/som-typing.mp3')
pygame.mixer.music.play(-1) #música toca infinitamente

#variáveis tela
imagensBackground = ['Imagens/backgrounds/0.png', 'Imagens/backgrounds/1.png', 'Imagens/backgrounds/2.png', 'Imagens/backgrounds/3.png', 'Imagens/backgrounds/4.png', 
'Imagens/backgrounds/5.png', 'Imagens/backgrounds/6.png', 'Imagens/backgrounds/7.png', 'Imagens/backgrounds/Sega-Kamerr.png']
telaInicio = True
telaMenu = False
telaJogo = False
telaScore = False
backTipo = 0
cuts = True

#tiros
tUltimoTiroIn = 0
tUltimoTiroPl = 0
intervaloIn = 1000
intervaloPl = 500
tempoAtual = 0
tirosInAtivos = []
tirosPlAtivos = []

#player e fases
player = Player()
fases = [
    {"qtd_inimigos": 3, "y": 150, "espacamento": 180, "cut": True, "pos": 510, "cutscene": "Utilize as setas para se movimentar.\n Aperte espaço para atirar\n Aperte 'ESC' para pular as cutscenes", "back": 5, "t": 20, "yy": 300},
    {"qtd_inimigos": 4, "y": 150, "espacamento": 170, "cut": False, "pos": 400, "back": 5},
    {"qtd_inimigos": 5, "y": 120, "espacamento": 150, "cut": True, "pos": 300, "cutscene": "Mais Tie-Figthers a  frente!\n Cuidado!\n", "back": 6,  "t": 20, "yy": 300},
    {"qtd_inimigos": 4, "y": 150, "espacamento": 170, "cut": False, "pos": 400, "back": 6},
    {"qtd_inimigos": 6, "y": 110, "espacamento": 150, "cut": True,  "pos": 300, "cutscene": "Você observa a grande e imponente:\n Estrela da Morte\n A estrela destruídora de Planetas"
    "\n Seu esquadrão está todo destruído, só sobrou você\n e Luke.\n Não descanse, até a luta acabar!", "back": 7, "t": 15, "yy": 100},
    {"qtd_inimigos": 4, "y": 150, "espacamento": 170, "cut": False, "pos": 400, "back": 7},
    {"qtd_inimigos": 7, "y": 100, "espacamento": 130, "cut": True, "pos": 250, "cutscene": "A batalha atingiu seu clímax.\n Luke Skywalker, guiado pela Força, " 
"inicia seu \n ataque final.\n A Estrela da Morte está prestes a disparar \n em Yavin 4 e Darth Vader " 
"lidera o ataque \nfinal para acabar com Skywalker. \n Wedge, você é o único que pode se interpor!", "back": 7, "t": 15, "yy": 100},
    {"qtd_inimigos": 6, "y": 110, "espacamento": 150, "cut": False, "pos": 300, "back": 7},
]
fasesIntervalo = 100
fasesTempoAtual = 0

faseAtual = 0
inimigos = []
faseConcluida = False

clock = pygame.time.Clock()

def criação(qtd, y, espaçamento, pos):
    inimigos = []
    for i in range(qtd):
        x = (i * espaçamento) + pos
        inimigos.append(Inimigo(x, y))     
    return inimigos

def cutscene(tela, texto, cor, y, t, largura = 850, velocidade = 15):
    fonte = pygame.font.Font('Imagens/fonte/DIGITALPIXELV80-REGULAR.ttf', t)
    palavras = texto.split('\n')
    linhas = []
    linhaAtual = ''

    for palavra in palavras:
        teste = linhaAtual + palavra + ' '
        if fonte.size(teste)[0] < largura:
            linhaAtual = teste
        else:
            linhas.append(linhaAtual)
            linhaAtual = palavra + ' '
    
    linhas.append(linhaAtual)
    clock = pygame.time.Clock()

    for i, linha in enumerate(linhas):
        textoParcial = ''
        for letra in linha:
            somTeclas.play()
            textoParcial += letra
            tela.blit(background, (0,0))
            posY = y

            for j, k in enumerate(linhas):
                render = fonte.render(k if j < i else (textoParcial if j == i else ''), True, cor)
                x = (tela.get_width() - render.get_width())// 2
                tela.blit(render, (x,posY))
                posY = posY + 50

            pygame.display.flip()
            clock.tick(velocidade)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:           # primeiro verifica se é uma tecla
                    if event.key == pygame.K_ESCAPE:        # depois verifica qual tecla
                        esperando = False
                        somTeclas.stop()
                        return 0
        somTeclas.stop()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:           # primeiro verifica se é uma tecla
                if event.key == pygame.K_SPACE:        # depois verifica qual tecla
                    esperando = False

        # redesenha a cutscene continuamente
        tela.blit(background, (0,0))
        posY = y
        for l in linhas:
            render = fonte.render(l, True, cor)
            x = (tela.get_width() - render.get_width())//2
            tela.blit(render, (x, posY))
            posY += 50
            

        pygame.display.flip()
        clock.tick(60)  # evita travar

def iniciarFase(numFase):
    config = fases[numFase]
    inimigos = criação(config["qtd_inimigos"], config["y"], config["espacamento"], config["pos"])
    backTipo = config["back"]
    
    pygame.image.load(imagensBackground[backTipo])

    if config["cut"]:
        cutscene(tela, config["cutscene"], '#d69b3d', config["yy"], config["t"])
    
    return inimigos, numFase, backTipo

while True:

    teclas = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if telaMenu:
            if teclas[pygame.K_DOWN]:
                if backTipo == 1 or backTipo == 2:
                    backTipo = backTipo + 1
                else:
                    backTipo = backTipo - 2
            if teclas[pygame.K_UP]:
                if backTipo == 1:
                    backTipo = backTipo + 2
                else:
                    backTipo = backTipo - 1
            if teclas[pygame.K_RETURN]:
                if backTipo == 1:
                    telaJogo = True
                    backTipo = 4
                    cuts = True
                elif backTipo == 2:
                    telaScore = True
                    cuts = True
                    pass
                else:
                    pygame.quit()
                    exit()   
                telaMenu = False

    background = pygame.image.load(imagensBackground[backTipo])
    tela.blit(background, (0,0))

    if telaScore:
        backTipo = 0
        background = pygame.image.load(imagensBackground[backTipo])
        if cuts:
            cutscene(tela, "Aqui serão inseridos os \nscores dos jogadores\n Aperte espaço para sair...", '#5d84db', 100, 20)
            cuts = False
            telaScore = False
            telaMenu = True
            backTipo = 1
            
    if telaInicio and cuts:
        cutscene(tela, "Aperte espaço para começar...", '#d69b3d', 300, 20)
        cuts = False
        backTipo = 1
        telaMenu = True
        telaInicio = False

    if telaJogo:
        if cuts:
            backTipo = 5
            cutscene(tela, "É um período de guerra civil.\nA Aliança Rebelde conseguiu roubar os planos da\n Estrela da Morte.\n "
"Como parte do Red Squadron, você é Wedge Antilles,\n um piloto de elite da Aliança Rebelde, sua missão\n é atacar os Tie-Fighters "
"e abrir caminho\n para destruir a arma mais poderosa do Império.\n A batalha de Yavin começa agora!\n "
"\n Aperte espaço para continuar...", '#d69b3d', 100, 15)
            inimigos, faseAtual, backtipo = iniciarFase(0)
            cuts = False
            print(backTipo)
        
        # Verifica se a fase atual foi concluída
        if not inimigos and not faseConcluida:  # Todos inimigos destruídos
            fasesTempoAtual += 1
            if fasesTempoAtual > fasesIntervalo:
                faseConcluida = True
                fasesTempoAtual = 0
                faseAtual += 1
                if faseAtual < len(fases):
                        #Próxima fase
                        inimigos, faseAtual, backTipo = iniciarFase(faseAtual)
                        faseConcluida = False
                else:
                    #finalizou game
                    background = pygame.image.load(imagensBackground[0])
                    cutscene(tela, "A Estrela da Morte explode...\n A Aliança Rebelde sobreviveu e\n a esperança renasce na galáxia.\n Red Squadron cumpriu sua missão.\n", '#d69b3d', 200, 20)
                    cutscene(tela, "Aperte ESPAÇO para voltar ao menu.", '#d69b3d', 300, 20)
                    telaJogo = False
                    telaMenu = True
                    faseAtual = 0
                    backTipo = 1
                    faseConcluida = False
                    background = pygame.image.load(imagensBackground[backTipo])
                    tela.blit(background, (0,0))

        player.entradaDoUsuário(teclas)

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
            inimigo.colisão(tirosPlAtivos, random.randint(1,10))
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

        if not player.vivo and not player.explodindo:
            faseConcluida = False
            cutscene(tela, "Você foi derrotado!\n", '#d69b3d', 300, 20)
            telaMenu = True
            telaJogo = False
            faseAtual = 0
            backTipo = 1
            background = pygame.image.load(imagensBackground[backTipo])
            player = Player()
            tirosInAtivos = []
            tela.blit(background, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
