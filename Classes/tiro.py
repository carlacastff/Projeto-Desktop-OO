import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.sprite import Sprite

pygame.mixer.init()

class Tiro(Sprite):
    def __init__(self, tipo, x, y, lado):
        self.ativo = True
        self.Colidiu = False

        if tipo == 1:
            self.pos = 5     #velocidade do tiro
            if lado == 1:
                super().__init__('Imagens/Sprites/explosão/tiro player.jpg', x, y)               #cria sprite do tiro do player
                self.image = pygame.transform.scale(self.image, (79/7, 355/7))                   #deixa sprite com tamanho redimensionado
                self.rect = self.image.get_rect()  # Recria o rect com as novas dimensões
                self.som = pygame.mixer.Sound('Música e Sons/x-wing - audio tiro 1.mp3')
                self.rect.x = x                                                                     #onde inicia horizontalmente
            else:
                super().__init__('Imagens/Sprites/explosão/tiro player.jpg', x + 85, y)             #cria sprite do tiro do player
                self.image = pygame.transform.scale(self.image, (79/7, 355/7))                      #deixa sprite com tamanho redimensionado
                self.rect = self.image.get_rect()  # Recria o rect com as novas dimensões
                self.som = pygame.mixer.Sound('Música e Sons/x-wing - audio tiro 2.mp3')
                self.rect.x = x + 85                                                                #onde inicia horizontalmente
            self.rect.y = y                                                                         #onde inicia veticalmente
            self.tipo = tipo
        else:
            self.pos = 2     #velocidade do tiro
            if lado < 5:
                self.som = pygame.mixer.Sound('Música e Sons/tie-fighter-audio-1.mp3')
            else:
                self.som = pygame.mixer.Sound('Música e Sons/tie-fighter-audio-2.mp3')

            super().__init__('Imagens/Sprites/explosão/tiro inimigo.jpg', x, y)                   #cria sprite do tiro do inimigo
            self.image = pygame.transform.scale(self.image, (79/7, 355/7))                          #deixa sprite com tamanho redimensionado
            self.rect = self.image.get_rect()  # Recria o rect com as novas dimensões
            self.rect.x = x                                                                         #onde inicia horizontalmente
            self.rect.y = y                                                                         #onde inicia veticalmente
            self.tipo = tipo


    def update(self):                                                                    #rect.y move o tiro na vertical
        max = 100
        min = 600
        if not self.ativo:
            return False
        
        if self.tipo == 1:
            self.rect.y = self.rect.y - self.pos

            if self.rect.y - self.pos < max:
                self.ativo = False
        else:
            self.rect.y = self.rect.y + self.pos

            if self.rect.y + self.pos > min:
                self.ativo = False
        return self.ativo
    
    def printar(self, tela):
        if self.ativo:
            tela.blit(self.image, self.rect)
    
    def barulho(self):
        if self.tipo == 1:
            self.som.play()
        if self.tipo == 2:
            self.som.play()


    