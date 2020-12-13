import pygame
from Joueur import *
from Mobs import *
from Map import *

class Game:
    def __init__(self):
        self.player = Joueur(self)
        self.pressed = {}

pygame.init()
pygame.display.set_caption("RPG de ouf", "icon.png")
screen = pygame.display.set_mode((1080,720))
background = pygame.image.load("images/background_test 1.jpg")
game = Game()

running = True

while running:
    screen.blit(background, (0,0))
    screen.blit(game.player.image, game.player.rect)
    if game.pressed.get(pygame.K_z) and game.player.rect.y > 0:
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
