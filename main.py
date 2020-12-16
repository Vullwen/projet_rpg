import pygame
from Joueur import *
from Mobs import *
from Map import *
import time
from main_class import Game, collision

pygame.init()
pygame.display.set_caption("RPG de ouf", "images/icon.png")
screen = pygame.display.set_mode((1080,720))
background = pygame.image.load("images/background_test 1.jpg")
game = Game()

running = True
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
    screen.blit(game.porte1.image, game.porte1.rect)
    screen.blit(game.porte2.image, game.porte2.rect)
    screen.blit(game.Epouvantail.image, game.Epouvantail.rect)
    screen.blit(game.murs1.image, game.murs1.rect)
def quel_pressee():
    if game.pressed.get(pygame.K_z) and game.player.rect.y > 0: #and main_class.game.player.rect.colliderect(main_class.game.murs.rect) == False:
        game.player.move("up")
    elif game.pressed.get(pygame.K_s) and game.player.rect.y < 688:
        game.player.move("down")
    elif game.pressed.get(pygame.K_q) and game.player.rect.x > 0:
        game.player.move("left")
    elif game.pressed.get(pygame.K_d) and game.player.rect.x < 1050:
        game.player.move("right")
def pressee():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
while running:
    affiche()
    quel_pressee()
    pressee()
    pygame.display.flip()
    game.porte1.use()
    game.porte2.use()
    collision()
