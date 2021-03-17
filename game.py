import pygame, sys, os, random, time, Map, son, ennemis
clock = pygame.time.Clock() #C'est pour déterminer le nombre d'image par seconde qui seront affichées
from pygame.locals import *
pygame.init()

pygame.display.set_caption('Le jeu') #c'est le nom de la fenetre
window_size_x = 888 #la taille x de la fenetre (en pixels), si la taille est celle de l'écran alors la fenetre sera en mode pleine écran
window_size_y = 500 #la taille y
WINDOW_SIZE = (window_size_x,window_size_y) #et je mets ces deux valeurs dans un tuple

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # créé la fenetre
display = pygame.Surface((300,200)) #je crée une Surface afin de rezise la taille des objects affichées ainsi meme si les images sont en 16pixels elles auront une taille convenable
display.fill((46,32,55)) # remplir le fond avec du violet, car c'est assez cool

class game:
    def __init__(self):
        self.player = joueur.init()


while True:

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0)) #j'affiche toutes les choses que j'ai mises sur 'display' sur 'screen' qui est la chose affiché à l'écran
    pygame.display.update() #j'update l'image

    for event in pygame.event.get(): #la boucle d'évenements, me permet de savoir tous les évenements possibles
        if event.type == QUIT: #si on quit le jeu, par ALT + F4 ou par le bouton quitter
            pygame.quit() #quit le jeu
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player.moving_up = True

    clock.tick(60) #le nombre FPS (Frame Per Second = Images par secondes)
