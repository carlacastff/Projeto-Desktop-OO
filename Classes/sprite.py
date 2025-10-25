import pygame

class Sprite(pygame.sprite.Sprite):        #pygame.sprite.Sprite é uma classe do pygame para Sprites
    def __init__(self, localização, x,y):
        super().__init__()
        self.image = pygame.image.load(localização).convert_alpha()   #inicializa imagem
        self.rect = self.image.get_rect(center=(x,y))    #onde a sprite aparece
    
    def printar(self, tela):
        tela.blit(self.image, self.rect)
    
    def update(self):
        pass

    def entradaDoUsuário(self):
        pass