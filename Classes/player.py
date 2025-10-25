import pygame
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.sprite import Sprite
from Classes.tiro import Tiro

class Player(Sprite):
    def __init__(self):
        super().__init__('Imagens/Sprites/player/x-wing.png', 1280/2, 550)  #cria sprite do player
        self.pos = 5
        self.tiros = []
        self.explodindo = False
        self.vivo = True
        self.conjunto = []
        self.atual = 0
        self.som = pygame.mixer.Sound('Música e Sons/explosão-2.mp3')

    def entradaDoUsuário(self, teclas):
        if self.vivo:
            if teclas[pygame.K_RIGHT]:
                self.moverDireita()
            if teclas[pygame.K_LEFT]:
                self.moverEsquerda()

    def moverDireita(self): #rect.x move o personagem na horizontal
        if self.vivo:
            if self.rect.x + self.pos >= 960:
                self.rect.x = 957
            else:
                self.rect.x = self.rect.x + self.pos

    def moverEsquerda(self):
        if self.vivo:
            if self.rect.x + self.pos <= 220:
                self.rect.x = 225
            else:
                self.rect.x = self.rect.x - self.pos
    
    def printar(self, tela):
        if self.vivo or self.explodindo: 
            tela.blit(self.image, self.rect)
    
    def atirar(self):
        if self.vivo:
            lado = random.randint(1, 2)
            tiro = Tiro(1, self.rect.x, self.rect.y - 25, lado)
            self.tiros.append(tiro)
            tiro.barulho()
            return tiro
    
    def colisão(self, tirosInAtivos):
        if self.vivo:
            for tiro in tirosInAtivos[:]:
                if tiro and tiro.ativo and self.rect.colliderect(tiro.rect):
                    self.explosão()
                    self.som.play()
                    return True
            return False

    
    def explosão(self):
        if self.vivo:
            self.vivo = False
            self.explodindo = True
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 1.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 2.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 3.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 4.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 5.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 6.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 7.png', self.rect.x, self.rect.y))
            self.conjunto.append(Sprite('Imagens/Sprites/explosão/explosão 8.png', self.rect.x, self.rect.y))
            self.image = self.conjunto[int(self.atual)].image
            for sprite in self.conjunto:
                sprite.image = pygame.transform.scale(sprite.image, (162//2, 160//2))
        return not self.vivo
    
    def update(self):
        if self.explodindo and self.conjunto:
            if int(self.atual) < len(self.conjunto):
                self.image = self.conjunto[int(self.atual)].image
                self.atual += 0.2
            else:
                self.explodindo = False
                self.conjunto = []
                self.atual = 0
