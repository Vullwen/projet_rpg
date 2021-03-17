import pygame, sys, os, random, time, game#les imports
pygame.init() # j'initialyse pygame

dirt_img = pygame.image.load("Data/images/dirt.PNG") #je load les images des 'blocs' dans des variables
sol_img_1 = pygame.image.load("Data/images/sol_1.PNG")
sol_img_2 = pygame.image.load("Data/images/sol_2.PNG")
porte_img_1 = pygame.image.load("Data/images/porte_1.PNG")
porte_img_2 = pygame.image.load("Data/images/porte_2.PNG")
vie = pygame.image.load("Data/images/vie_0.PNG")

player_action = 'idle' #l'action du joueur (uniquement pour les animations)
player_frame = 0 #de base la frame du joueur est à 0
player_flip = False #me permettera de retourener l'image du joueur

def collision_test(rect,tiles):
    hit_list = [] #la liste des collisions avec les 'blocs'
    for tile in tiles: #je regarde chaque tuile qui a une présence physique
        if rect.colliderect(tile): #je regarde si elle est en collision avec quelque chose
            hit_list.append(tile) #si oui je l'ajoute à la liste de collion
    return hit_list #je retourne cette liste

def lose_life(dammage): #si on perd de la vie
    global life,vie,vie_pallier,path_vie
    life -= dammage #on retire les dommages subit à la vie
    if life <= vie_pallier: #si la vie est en dessous du palier
        path_vie += 1 #on ajoute 1 au chemin d'accès
        vie_pallier -= 20 #on baisse jusqu'au prochain palier de 20
    if life <= 0:
        print("GAME OVER")
        exit()
    vie = pygame.image.load("Data/images/vie_" + str(path_vie) + ".PNG") #on reload l'image

while True: #la boucle de jeu

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1])) #affiche l'image du joueur
    #flip permet de retourner l'image en fonction de 'player_flip', le reste c'est les coordonnées

    for event in pygame.event.get(): #la boucle d'évenements, me permet de savoir tous les évenements possibles
        if event.type == KEYDOWN: #si une touche est en position basse (pressée)
            if event.key == K_w: #si c'est la touche 'w'
                if music_playing == True: #si la musique est en train d'etre jouée
                    music_playing = False #on change la variable car on veut couper la musique
                    pygame.mixer.music.fadeout(1000) #pendant 1000 millisecondes le volume de la musique baisse avant de s'éteindre
                else:
                    music_playing = True #on met la variable de la jouabilité de la musique ON
                    pygame.mixer.music.play() #on joue la musique
            if event.key == K_RIGHT: #si la touche est la flèche de droite
                moving_right = True #je change la valeur de mouvement
            if event.key == K_LEFT: #si la touche est la flèche de gauche
                moving_left = True
            if event.key == K_UP: #si la touche est la flèche du haut
                moving_up = True
            if event.key == K_DOWN: #si la touche est la flèche du bas
                moving_down = True
            if event.key == K_v:
                lose_life(20)
            if event.key == K_m: #si le touche est 'm'
                if (nbr_map + 1) > nb_map: #je regarde si la futur map est supérieur au nombre de map
                    nbr_map = 1 #si oui alors on a fait le tour des maps et on retourne à la map 0
                else:
                    nbr_map += 1 #sinon on ajoute 1 et on passe à la map suivante
                map_path = 'Data/Maps/map_' + str(nbr_map) #le chemin d'accès à la map est modifier pour correspondre au nouveau
                game_map = load_map(map_path) #la nouvelle map est enregistrée dans 'game_map'
                y = 0                                   #
                for layer in game_map:                  #
                    x = 0                               #
                    for tile in layer:                  #Tous ca pour remettre le joueur
                        if tile == '4':                 #a son point de spawn
                            player_rect.x = x*16        #
                            player_rect.y = y*16        #
                        x += 1                          #
                    y += 1                              #
                truc_exist = False
            if event.key == K_SPACE and event.mod and KMOD_LCTRL and event.mod and KMOD_LSHIFT: #si la combinaison de touche : 'CTRL' + 'MAJ' + 'ESPACE'
                if noclip: #si noclip est à True
                    noclip = False #on le change en False et donc le noclip s'arrete
                else:
                    noclip = True #sinon on change la variable en True et le noclip commence
            if event.key == K_e: #si la touche est 'e'
                 action_button_pressed = True #alors le bouton d'action est activée
        if event.type == KEYUP: #si la touche n'est plus pressée
            if event.key == K_RIGHT:
                moving_right = False #je les mets donc à false
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False
            if event.key == K_e:
                 action_button_pressed = False
