import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.sprite import Sprite
from Classes.tiro import Tiro

class Inimigo(Sprite):
    def __init__(self, x , y):
        super().__init__('Imagens/Sprites/inimigo/inimigo1.png', x, y)  #cria sprite do player
        self.image = pygame.transform.scale(self.image, (162/2, 160/2))
        self.rect.x = x
        self.rect.y = y
        self.vivo = True
        self.tiros = []
        self.atual = 0
        self.explodindo = False
        self.conjunto = []
        self.rect = self.image.get_rect(center=(x, y))
        self.som = pygame.mixer.Sound('Música e Sons/explosão-3.mp3')
        self.som2 = pygame.mixer.Sound('Música e Sons/explosão-1.mp3')

    def printar(self, tela):
        if self.vivo or self.explodindo:
            tela.blit(self.image, self.rect)
    
    def atirar(self, lado):
        if self.vivo and not self.explodindo:
            tiro = Tiro(2, self.rect.x + 35, self.rect.y + 35, lado)
            self.tiros.append(tiro)
            tiro.barulho()
            return tiro
        
    def colisão(self, tirosPlAtivos, som):
        for tiro in tirosPlAtivos[:]:
            if tiro and tiro.ativo and self.rect.colliderect(tiro.rect):
                self.explosão()
                if som / 2 ==0:
                    self.som.play()
                else:
                    self.som2.play()
                tiro.ativo = False  # Destrói o tiro
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
                return True  # <-- explosão terminou, pode deletar
        return False



