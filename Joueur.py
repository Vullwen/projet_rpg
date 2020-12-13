import pygame
import time

class Joueur(pygame.sprite.Sprite):
    """
    Je défini toutes les intéractions clavier ici
    """
    def __init__(self, game):
        """
        Les informations sur le joueur
        """
        super().__init__()
        #l'image des entités doit etre MAX de 45*45pixels et donc respecter ses proportions
        self.image = pygame.image.load('images/perso dot.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = 352
        self.rect.y = 567
        self.velocity = 1

    def move(self, direction):
        """
        Permet de déplacer le joueur en regardant si il le peu
        """
        if direction == "up":
            self.rect.y -= self.velocity
            self.image = pygame.image.load('images/perso dot.jpg')
        elif direction == "down":
            self.rect.y += self.velocity
            self.image = pygame.image.load('images/perso face.jpg')
        elif direction == "left":
            self.rect.x -= self.velocity
            self.image = pygame.image.load('images/perso gauche.jpg')
        elif direction == "right":
            self.rect.x += self.velocity
            self.image = pygame.image.load('images/perso droite.jpg')
