import pygame
from Joueur import *
from Mobs import *
import time

class Game:
    def __init__(self):
        self.player = Joueur(self)
        self.Epouvantail = Epouvantail()
        self.porte = porte()
        self.murs = Murs1()
        self.pressed = {}
class Murs1(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('images/murs/murs 1.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = 206
        self.rect.y = 314
    def collision(self):
        if self.rect.colliderect(game.player.rect):
            if game.pressed.get(pygame.K_z):
                for i in range(0,5):
                    game.player.move("down")
            elif game.pressed.get(pygame.K_s):
                for i in range(0,5):
                    game.player.move("up")
            elif game.pressed.get(pygame.K_q):
                for i in range(0,5):
                    game.player.move("right")
            elif game.pressed.get(pygame.K_d):
                for i in range(0,5):
                    game.player.move("left")
class porte(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('images/porte 1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 686
        self.rect.y = 312
    def use(self):
        if self.rect.colliderect(game.player.rect):
            for i in range(0,200):
                screen.blit(background, (0,0))
                game.player.rect.y -= game.player.velocity
                screen.blit(game.player.image, game.player.rect)
                pygame.display.flip()
                time.sleep(0.001)

pygame.init()
pygame.display.set_caption("RPG de ouf", "images/icon.png")
screen = pygame.display.set_mode((1080,720))
background = pygame.image.load("images/background_test 1.jpg")
game = Game()

running = True
game.player.rect.x = 352
game.player.rect.y = 720
screen.blit(background, (0,0))
for i in range(0,153):
    screen.blit(background, (0,0))
    game.player.rect.y -= game.player.velocity
    screen.blit(game.player.image, game.player.rect)
    pygame.display.flip()
    time.sleep(0.001)
def affiche():
    screen.blit(background, (0,0))
    screen.blit(game.player.image, game.player.rect)
    screen.blit(game.porte.image, game.porte.rect)
    screen.blit(game.Epouvantail.image, game.Epouvantail.rect)
    screen.blit(game.murs.image, game.murs.rect)
#686;312
while running:
    affiche()
    if game.pressed.get(pygame.K_z) and game.player.rect.y > 0: #and game.player.rect.colliderect(game.murs.rect) == False:
        game.player.move("up")
    elif game.pressed.get(pygame.K_s) and game.player.rect.y < 688:
        game.player.move("down")
    elif game.pressed.get(pygame.K_q) and game.player.rect.x > 0:
        game.player.move("left")
    elif game.pressed.get(pygame.K_d) and game.player.rect.x < 1050:
        game.player.move("right")
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
    game.porte.use()
    game.murs.collision()
