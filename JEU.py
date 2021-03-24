import pygame, sys, os, random, time, game#les imports
pygame.init() # j'initialyse pygame

while True: #la boucle de jeu

    for event in pygame.event.get(): #la boucle d'évenements, me permet de savoir tous les évenements possibles
        if event.type == KEYDOWN: #si une touche est en position basse (pressée)
            if event.key == K_w: #si c'est la touche 'w'
                if music_playing == True: #si la musique est en train d'etre jouée
                    music_playing = False #on change la variable car on veut couper la musique
                    pygame.mixer.music.fadeout(1000) #pendant 1000 millisecondes le volume de la musique baisse avant de s'éteindre
                else:
                    music_playing = True #on met la variable de la jouabilité de la musique ON
                    pygame.mixer.music.play() #on joue la musique
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
            if event.key == K_SPACE and event.mod and KMOD_LCTRL and event.mod and KMOD_LSHIFT: #si la combinaison de touche : 'CTRL' + 'MAJ' + 'ESPACE'
                if noclip: #si noclip est à True
                    noclip = False #on le change en False et donc le noclip s'arrete
                else:
                    noclip = True #sinon on change la variable en True et le noclip commence
            if event.key == K_e: #si la touche est 'e'
                 action_button_pressed = True #alors le bouton d'action est activée
            if event.key == K_e:
                 action_button_pressed = False
