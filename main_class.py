import pygame
from Joueur import *
from Mobs import *

pygame.init()
class Game:
    def __init__(self):
        self.player = Joueur()
        self.Epouvantail = Epouvantail()
        self.porte1 = porte1(self)
        self.porte2 = porte2(self)
        self.murs1 = murs1()
        self.pressed = {}
class porte1(pygame.sprite.Sprite):
    def __init__(self, game):
        self.image = pygame.image.load('images/porte 1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 352
        self.rect.y = 200
    def use(self):
        if self.rect.colliderect(game.player.rect):
            for i in range(0,200):
                screen = pygame.display.set_mode((1080,720))
                game.player.rect.y -= game.player.velocity
                screen.blit(game.player.image, game.player.rect)
                pygame.display.flip()
                time.sleep(0.001)
class porte2(pygame.sprite.Sprite):
    def __init__(self, game):
        self.image = pygame.image.load('images/porte 2.png')
        self.rect = self.image.get_rect()
        self.rect.x = 688
        self.rect.y = 229
    def use(self):
        if self.rect.colliderect(game.player.rect):
            for i in range(0,200):
                screen.blit(background, (0,0))
                game.player.rect.y += game.player.velocity
                screen.blit(game.player.image, game.player.rect)
                pygame.display.flip()
                time.sleep(0.001)
class murs1(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('images/murs/Layer 1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 208
        self.rect.y = 233
game = Game()
def collision():
    if game.murs1.rect.colliderect(game.player.rect):
        if game.pressed.get(pygame.K_z):
            game.player.rect.y += 5
        elif game.pressed.get(pygame.K_s):
            game.player.rect.y -= 5
        elif game.pressed.get(pygame.K_q):
            game.player.rect.x += 5
        elif game.pressed.get(pygame.K_d):
            game.player.rect.y -= 5
