from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, sys, os, random, time, Map, son, ennemis, joueur
from pygame.locals import *
def launch():
    clock = pygame.time.Clock() #C'est pour déterminer le nombre d'image par seconde qui seront affichées
    pygame.init()

    pygame.display.set_caption('Le jeu') #c'est le nom de la fenetre
    window_size_x = 1280 #la taille x de la fenetre (en pixels), si la taille est celle de l'écran alors la fenetre sera en mode pleine écran
    window_size_y = 800 #la taille y
    WINDOW_SIZE = (window_size_x,window_size_y) #et je mets ces deux valeurs dans un tuple

    screen = pygame.display.set_mode(WINDOW_SIZE, 0,32) # créé la fenetre
    display = pygame.Surface((300,200)) #je crée une Surface afin de rezise la taille des objects affichées ainsi meme si les images sont en 16pixels elles auront une taille convenable
    pygame.display.set_icon(pygame.image.load("Data/images/icon.PNG"))

    class game:
        def __init__(self):
            self.true_scroll = [0,0]
            self.action_button = False
            self.scroll = self.true_scroll.copy()
            self.player = joueur.joueur_class()
            self.map = Map.map_class()
            self.ennemi = ennemis.Mob()
            self.img_size = 16
            self.god_mod = 0
    JEU = game()

    def spawnpoint(game_map, player_rect):
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == 'j':
                    player_rect.x = x*JEU.img_size
                    player_rect.y = y*JEU.img_size
                x += 1
            y += 1
        return player_rect

    JEU.ennemi.mob_rect.x, JEU.ennemi.mob_rect.y = JEU.ennemi.create_mob(JEU.player.player_rect.x,JEU.player.player_rect.y, JEU.map.game_map)
    JEU.player.player_rect = spawnpoint(JEU.map.game_map, JEU.player.player_rect)
    while True:
        display.fill((46,32,55)) # remplir le fond avec du violet, car c'est assez cool

        #---Joueur---#
        JEU.true_scroll[0] += (JEU.player.player_rect.x-JEU.true_scroll[0]-156)/20
        JEU.true_scroll[1] += (JEU.player.player_rect.y-JEU.true_scroll[1]-106)/20
        JEU.scroll = JEU.true_scroll.copy()
        JEU.scroll[0] = int(JEU.scroll[0])
        JEU.scroll[1] = int(JEU.scroll[1])
        JEU.player.player_movement = [0,0] #la liste comprenant les mouvements du joueur
        JEU.player.player_frame += 1 #j'ajoute une frame au joueur
        JEU.player.animation()
        JEU.player.test_movement()
        JEU.player.player_rect,JEU.player.collisions = JEU.player.move(JEU.player.player_rect,JEU.player.player_movement,JEU.map.tile_rects) #regarde les commentaires de cette fonction tu comprendra surement
        #---Joueur---#
        #---Map---#
        JEU.map.game_map = Map.load_map(JEU.map.map_path)
        JEU.map.meta_map = Map.load_map(JEU.map.meta_map_path)
        JEU.map.tile_rects = []
        JEU.map.meta_tile = []
        y = 0 #je met à 0 le y, soit la première 'ligne' de la map (en partant du haut)
        for layer in JEU.map.game_map: #je regarde ligne par ligne dans le fichier texte ou se trouve la map
            x = 0 #je met à 0 le x, soit le premier 'bloc' de la map (en partant de la droite)
            for tile in layer: #je regarde du coup 'bloc' par 'bloc' dans chacune des lignes
                if tile == 'm': #si le 'bloc' (appelée tile pour tuile) vaut 1 alors c'est un mur
                    display.blit(JEU.map.dirt_img,(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1])) #j'affiche son image correspondante ("dirt_img")
                if tile == 's': #si la tuile est 0 alors c'est un sol normal
                    display.blit(JEU.map.sol_img_1,(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1])) #le -scroll c'est pour enlever le scroll de la CAM
                if tile == 'j': #si la tuile vaut 4 alors c'est le point de spawn du joueur
                    display.blit(JEU.map.sol_img_1,(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1])) #tu peut essayer sans (le scroll) mais tu verra que c'est pas bien
                if tile == 'e':
                    display.blit(JEU.map.sol_img_1,(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1]))
                if tile == 'p': #la c'est une des deux portes
                    display.blit(JEU.map.porte_img_1,(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1]))
                    JEU.map.meta_tile.append(pygame.Rect(x*JEU.img_size,y*JEU.img_size,JEU.img_size,JEU.img_size))
                    for nb_meta_tile in range(len(JEU.map.meta_tile)):
                        if JEU.player.player_rect.colliderect(JEU.map.meta_tile[nb_meta_tile]) and JEU.action_button:
                            JEU.action_button = False
                            print(JEU.map.meta_tile)
                            JEU.player.player_rect.x, JEU.player.player_rect.y = Map.look_at_meta(JEU.map.meta_map, JEU.player.player_rect, JEU.map.meta_tile, 'p')
                            JEU.player.player_rect.x = JEU.player.player_rect.x*JEU.img_size
                            JEU.player.player_rect.y = JEU.player.player_rect.y*JEU.img_size
                if tile in JEU.map.no_physics_tile: #la je teste si la tuile fait partie des tuiles qui ne doivent pas avoirs de collisions
                    pass #si c'est le cas je ne fais rien
                else:
                    JEU.map.tile_rects.append(pygame.Rect(x*JEU.img_size,y*JEU.img_size,JEU.img_size,JEU.img_size)) #là, je fait un rectangle au coordonées de la tuile qui aura une présence physique et j'ajoute ce rectangle dans une liste
                x += 1 #j'ajoute 1 au x pour vérifier la tuile suivante
            y += 1 # j'ajoute 1 au y pour vérifier la ligne suivante

        if JEU.god_mod == 1:
            JEU.map.tile_rects = []
        #---Map---#
        #---Mob---#

        JEU.ennemi.move_to_player(JEU.player.player_rect)
        JEU.ennemi.collision_test(JEU.map.tile_rects)
        JEU.ennemi.movement = [0,0] #la liste comprenant les mouvements du joueur
        JEU.ennemi.move_to_player(JEU.player.player_rect)
        JEU.ennemi.mob_rect,JEU.ennemi.collision = JEU.ennemi.move(JEU.ennemi.movement,JEU.map.tile_rects)
        if JEU.ennemi.test_hit_player(JEU.player.player_rect):
            print("Touche")
        #---Mob---#

        for event in pygame.event.get(): #la boucle d'évenements, me permet de savoir tous les évenements possibles
            if event.type == QUIT: #si on quit le jeu, par ALT + F4 ou par le bouton quitter
                pygame.quit() #quit le jeu
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT: #si la touche est la flèche de droite
                    JEU.player.moving_right = True #je change la valeur de mouvement
                if event.key == K_LEFT: #si la touche est la flèche de gauche
                    JEU.player.moving_left = True
                if event.key == K_UP: #si la touche est la flèche du haut
                    JEU.player.moving_up = True
                if event.key == K_DOWN: #si la touche est la flèche du bas
                    JEU.player.moving_down = True
                if event.key == K_e:
                    JEU.action_button = True
                if event.key == K_LCTRL and event.key == K_LSHIFT and event.key == K_SPACE:
                    JEU.god_mod = 1
                if event.key == K_m: #si le touche est 'm'
                    print(JEU.map.nbr_map, JEU.map.nb_map - 1)
                    if (JEU.map.nbr_map + 1) > (JEU.map.nb_map - 1): #je regarde si la futur map est supérieur au nombre de map
                        JEU.map.nbr_map = 1 #si oui alors on a fait le tour des maps et on retourne à la map 0
                        JEU.player.player_rect = spawnpoint(JEU.map.game_map, JEU.player.player_rect)
                    else:
                        JEU.map.nbr_map += 1 #sinon on ajoute 1 et on passe à la map suivante
                        JEU.map.map_path = 'Data/Maps/map_' + str(JEU.map.nbr_map) #le chemin d'accès à la map est modifier pour correspondre au nouveau
                        JEU.map.meta_map_path = 'Data/Maps/Meta/map_' + str(JEU.map.nbr_map)
                        JEU.player.player_rect = spawnpoint(JEU.map.game_map, JEU.player.player_rect)
            if event.type == KEYUP: #si la touche n'est plus pressée
                if event.key == K_RIGHT:
                    JEU.player.moving_right = False #je les mets donc à false
                if event.key == K_LEFT:
                    JEU.player.moving_left = False
                if event.key == K_UP:
                    JEU.player.moving_up = False
                if event.key == K_DOWN:
                    JEU.player.moving_down = False
                if event.key == K_e:
                    JEU.action_button = False

        display.blit(JEU.ennemi.image,(JEU.ennemi.mob_rect.x-JEU.scroll[0],JEU.ennemi.mob_rect.y-JEU.scroll[1]))
        display.blit(pygame.transform.flip(JEU.player.player_img,JEU.player.player_flip,False),(JEU.player.player_rect.x-JEU.scroll[0],JEU.player.player_rect.y-JEU.scroll[1])) #affiche l'image du joueur
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0)) #j'affiche toutes les choses que j'ai mises sur 'display' sur 'screen' qui est la chose affiché à l'écran
        pygame.display.update() #j'update l'image
        clock.tick(60) #le nombre FPS (Frame Per Second = Images par secondes)
