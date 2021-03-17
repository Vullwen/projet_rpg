import pygame, sys, os, random, time, ennemis#les imports
clock = pygame.time.Clock() #C'est pour déterminer le nombre d'image par seconde qui seront affichées

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512) #j'initialyse tous les sons sinon il y a un décalage audio
pygame.init() # j'initialyse pygame
pygame.mixer.set_num_channels(64) #je choisi le nombre de channels audio, le nombre de sons qui peuvent etres jouée en meme temps

pygame.display.set_caption('Tests de générations de Maps') #c'est le nom de la fenetre
window_size_x = 1280 #la taille x de la fenetre (en pixels), si la taille est celle de l'écran alors la fenetre sera en mode pleine écran
window_size_y = 800 #la taille y
WINDOW_SIZE = (window_size_x,window_size_y) #et je mets ces deux valeurs dans un tuple


screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # créé la fenetre

display = pygame.Surface((300,200)) #je crée une Surface afin de rezise la taille des objects affichées ainsi meme si les images sont en 16pixels elles auront une taille convenable

moving_right = False #me sert à savoir si le joueur bouge vers la droite
moving_left = False #me sert à savoir si le joueur bouge vers la gauche
moving_up = False #me sert à savoir si le joueur bouge vers le haut
moving_down = False #me sert à savoir si le joueur bouge vers le bas
vertical_momentum = 0 #me sert à savoir si le joueur bouge sur l'axe des ordonnées
music_playing = True #me sert à savoir si la music est en train d'etre jouée
life = 120 #me sert à savoir combien de points de vie a le joueur
vie_pallier = 100 #le pallier de points vie avant que l'image de la vie ne s'actualise
path_vie = 0 #afin d'obtenir le chemin d'accès à l'image vie
noclip = False #me sert à savoir si le joueur peut traverser les murs
oneshot = True #me sert à savoir plus tard
nb_map = len(os.listdir('Data/Maps')) - 1 #me sert à savoir combien il y a de map, je fait -1 car il y a un fichier de renseignement sur les maps
nbr_map = 1 #me sert à savoir nous sommes à quel map (la 1, la 2,...)
no_physics_tile = ["0","4","2","+","-","*","/","5"] #la liste des tuiles non physiques
action_button_pressed = False #si la touche d'action est pressée
truc_exist = False

true_scroll = [0,0]

player_rect = pygame.Rect(0,0,5,13) #je créé un rectangle qui me permettera de modifier la position du joueur ainsi que de tester si il entre en collision avec quelque chose

def load_map(path): #pour loader la map dans une variable 'game_map'
    f = open(path + '.txt','r') #j'ouvre l'un des fichiers map
    data = f.read() #je met le contenu du fichier dans une variable 'data'
    f.close() #je ferme le fichier (!!! IMPORTANT !!!)
    data = data.split('\n') #je coupe les retours à la ligne
    game_map = [] #je créé la fameuse variable 'game_map'
    for row in data: #pour chaque ligne dans data,
        game_map.append(list(row)) #, j'ajoute cette ligne dans data
    return game_map #je retourne la valeur

global animation_frames #pour savoir le nombre de frame que restera l'image
animation_frames = {} #je le met dans un dico

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1] #me permet d'avoir juste le nom de l'animation
    animation_frame_data = [] #je créé une base de donnée des frames
    n = 0 #me permet d'obtenir le numéro de l'animation (mon fichier est enregistré avec un numéro à la fin (ex : 'run_1'))
    for frame in frame_durations: #les 'frames_durations' sont de 7 soit toutes les 7 ticks dans frame_duration
        animation_frame_id = animation_name + '_' + str(n) #me premet d'obtenir le fameux nom de cette
        img_loc = path + '/' + animation_frame_id + '.png' #la, je reconstitu le chemni d'accès au fichier
        #un exemple de chemin d'accès : 'player_animations/idle/idle_0.png'
        animation_image = pygame.image.load(img_loc).convert() #permet de charger l'image de l'animation
        animation_image.set_colorkey((255,255,255)) #j'efface la couleur blanc (code RGB)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value): #pour ne pas changer constament les images, ca pourrait faire laguer
    if action_var != new_value: #on regarde si l'actuel image est différente de la nouvelle
        action_var = new_value #si oui, alors l'actuel devient la nouvelle
        frame = 0 #et les frames sont remisent à 0
    return action_var,frame #et on return tout ca


animation_database = {} #la je créé la database des animations dans un dico

animation_database['run'] = load_animation('Data/player_animations/run',[7,7]) #la database 'run' contien donc le return de load_animation
animation_database['idle'] = load_animation('Data/player_animations/idle',[7,7,40]) #pareil pour la database de 'idle'

map_path = 'Data/Maps/map_5' #le chemin d'accès aux maps
game_map = load_map(map_path) #le fichier ou est stocké la map recois le return de load_map

dirt_img = pygame.image.load("Data/images/dirt.PNG") #je load les images des 'blocs' dans des variables
sol_img_1 = pygame.image.load("Data/images/sol_1.PNG")
sol_img_2 = pygame.image.load("Data/images/sol_2.PNG")
porte_img_1 = pygame.image.load("Data/images/porte_1.PNG")
porte_img_2 = pygame.image.load("Data/images/porte_2.PNG")
vie = pygame.image.load("Data/images/vie_0.PNG")

jump_sound = pygame.mixer.Sound('Data/Sound/jump.wav') #je télécharge le son dans une variable
grass_sounds = [pygame.mixer.Sound('Data/Sound/grass_0.wav'),pygame.mixer.Sound('Data/Sound/grass_1.wav')] #j'ai deux sons d'herbes donc je met le tous dans la variable
grass_sounds[0].set_volume(0.2) #je réduis leur volume (1 = normal; <1 = plus fort; >1 = moins fort)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('Data/Sound/music.wav') #"j'initialise" la musique de fond
pygame.mixer.music.play(-1) #je la joue

player_action = 'idle' #l'action du joueur (uniquement pour les animations)
player_frame = 0 #de base la frame du joueur est à 0
player_flip = False #me permettera de retourener l'image du joueur

grass_sound_timer = 0 #un timer pour savoir au bout de combien de ticks un son d'herbe se jouera

def collision_test(rect,tiles):
    hit_list = [] #la liste des collisions avec les 'blocs'
    for tile in tiles: #je regarde chaque tuile qui a une présence physique
        if rect.colliderect(tile): #je regarde si elle est en collision avec quelque chose
            hit_list.append(tile) #si oui je l'ajoute à la liste de collion
    return hit_list #je retourne cette liste

def move(rect,movement,tiles): #rect = joueur, #tiles = la liste de tuiles avec une présence physique
    #movement = liste. movement[0] = mouvement en x par pixels, movement[1] =  mouvement en y par pixels
    collision_types = {'top':False,'bottom':False,'right':False,'left':False} #les différents moyen de rentrer en collision
    rect.x += movement[0] #je déplace le joueur en x par le mouvement par pixels inscrits
    hit_list = collision_test(rect,tiles) #je teste si le joueur est en collision avec une tuile
    for tile in hit_list: #je regarde tuile par tuile dans la liste des tuiles physique
        if movement[0] > 0: #si le mouvement x est superieur à 0 alors le joueur veut aller à droite
            rect.right = tile.left #honnetement, aller sur internet pour ca, flem d'expliquer
            collision_types['right'] = True #quelle type de collision a t-on
        elif movement[0] < 0: #tout le reste c'est la meme chose mais avec les 3 axes restants
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types #je renvoi la nouvelle position du joueur ainsi que les types de collisions, toujours utile au cas ou

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
    display.fill((46,32,55)) # remplir le fond avec du violet, car c'est assez cool

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = [] #la liste de tuiles qui ont une existance physique

    y = 0 #je met à 0 le y, soit la première 'ligne' de la map (en partant du haut)
    for layer in game_map: #je regarde ligne par ligne dans le fichier texte ou se trouve la map
        x = 0 #je met à 0 le x, soit le premier 'bloc' de la map (en partant de la droite)
        for tile in layer: #je regarde du coup 'bloc' par 'bloc' dans chacune des lignes
            if tile == '1': #si le 'bloc' (appelée tile pour tuile) vaut 1 alors c'est un mur
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1])) #j'affiche son image correspondante ("dirt_img")
            if tile == '2': #si la tuile est 2 alors c'est un sol craquelé
                display.blit(sol_img_2,(x*16-scroll[0],y*16-scroll[1])) #les coordonnées sont les x et y de la lecture du fichier game_map
            if tile == '0': #si la tuile est 0 alors c'est un sol normal
                display.blit(sol_img_1,(x*16-scroll[0],y*16-scroll[1])) #le -scroll c'est pour enlever le scroll de la CAM
            if tile == '4': #si la tuile vaut 4 alors c'est le point de spawn du joueur
                display.blit(sol_img_1,(x*16-scroll[0],y*16-scroll[1])) #tu peut essayer sans (le scroll) mais tu verra que c'est pas bien
                if oneshot: #je regarde si ma variable 'oneshot' est à TRUE
                    oneshot = False #si c'est le cas alors je la met a False, il n'y aura pas d'autre modification de cette variable
                    player_rect.x = x*16 #elle restera ainsi une variable qui me permet d'efectuer une action une seul fois mais dans une boucle
                    player_rect.y = y*16 #la je met les positions du joueur au point de spawn (c'est pour ca qu'il faut le faire UNE SEUL FOIS, pour pas que le joueur reste visé au sol)
            if tile == '5':
                display.blit(sol_img_1,(x*16-scroll[0],y*16-scroll[1]))
                if truc_exist == False:
                    truc = ennemis.Mob(x,y)
                    truc_exist = True
            if tile == '+': #la c'est une des deux portes
                display.blit(porte_img_2,(x*16-scroll[0],y*16-scroll[1]))
                porte_2_rect = pygame.Rect(x*16,y*16,16,16) #je fais un rectangle qui me permettera de faire des tests de collisions (au meme endroit que la porte)
                if player_rect.colliderect(porte_2_rect) and action_button_pressed: #je teste si il y a collision avec le rectangle du joueur et le rectangle de la porte
                    player_rect.x = porte_1_rect.x - 5 #le 'action_button_pressed' c'est pour voir si le bouton 'e' est pressée (le bouton d'action du joueur)
                    player_rect.y = porte_1_rect.y + 2
            if tile == '-': #la c'est la deuxième porte, dans notre code les portes ont une genre de 'jumelle' et les jumelles téléporte le joueur entre elles
                display.blit(porte_img_1,(x*16-scroll[0],y*16-scroll[1]))
                porte_1_rect = pygame.Rect(x*16,y*16,16,16)
                if player_rect.colliderect(porte_1_rect) and action_button_pressed:
                    player_rect.x = porte_2_rect.x + 16 #je remplace les positions x,y du joueur par celles des portes 'jumelles'
                    player_rect.y = porte_2_rect.y + 2
            if tile == '*':
                display.blit(porte_img_1,(x*16-scroll[0],y*16-scroll[1]))
                porte_3_rect = pygame.Rect(x*16,y*16,16,16)
                if player_rect.colliderect(porte_3_rect) and action_button_pressed:
                    player_rect.x = porte_4_rect.x + 16
                    player_rect.y = porte_4_rect.y + 2
            if tile == '/':
                display.blit(porte_img_2,(x*16-scroll[0],y*16-scroll[1]))
                porte_4_rect = pygame.Rect(x*16,y*16,16,16)
                if player_rect.colliderect(porte_4_rect) and action_button_pressed:
                    player_rect.x = porte_3_rect.x - 5
                    player_rect.y = porte_3_rect.y + 2
            if tile in no_physics_tile: #la je teste si la tuile fait partie des tuiles qui ne doivent pas avoirs de collisions
                pass #si c'est le cas je ne fais rien
            else:
                tile_rects.append(pygame.Rect(x*16,y*16,16,16)) #là, je fait un rectangle au coordonées de la tuile qui aura une présence physique et j'ajoute ce rectangle dans une liste
            x += 1 #j'ajoute 1 au x pour vérifier la tuile suivante
        y += 1 # j'ajoute 1 au y pour vérifier la ligne suivante

    if noclip: #si le noclip est activée
        tile_rects = [] #le fichier comprenant les tuiles qui ont une présence physique devient vide et le joueur peut traverser ses 'bloc'

    player_movement = [0,0] #la liste comprenant les mouvements du joueur
    if moving_right == True: #si il bouge vers la droite
        player_movement[0] += 2 #j'joute 2pixels à la première case
    if moving_left == True:
        player_movement[0] -= 2 #si il va vers la gauche j'en enlève 2
    if moving_up == True: #pareil pour l'axe y mais avec la deuxième case du tableau
        player_movement[1] -= 2
    if moving_down == True:
        player_movement[1] += 2

    if player_movement[0] == 0: #si le joueur ne bouge pas alors je change son animation
        player_action,player_frame = change_action(player_action,player_frame,'idle') #
    if player_movement[0] > 0: #si le joueur cours à droite alors je change avec l'animation de course
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0: #pareil qu'au dessus
        player_flip = True #me permet de retourner l'image pour que le joueur regarde de l'autre coté
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects) #regarde les commentaires de cette fonction tu comprendra surement

    player_frame += 1 #j'ajoute une frame au joueur
    if player_frame >= len(animation_database[player_action]): #si les frames d'action sont plus grandes que celles qui sont possible
        player_frame = 0 #on met les frames à 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1])) #affiche l'image du joueur
    #flip permet de retourner l'image en fonction de 'player_flip', le reste c'est les coordonnées

    for event in pygame.event.get(): #la boucle d'évenements, me permet de savoir tous les évenements possibles
        if event.type == QUIT: #si on quit le jeu, par ALT + F4 ou par le bouton quitter
            pygame.quit() #quit le jeu
            sys.exit()
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

    if truc_exist:
        truc.move_to_player(player_rect)
        display.blit(truc.image,(truc.rect.x - scroll[0],truc.rect.y - scroll[1]))
        if truc.test_hit_player(player_rect):
             lose_life(0.5)

    display.blit(vie,(0,0)) #j'affiche la vie

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0)) #j'affiche toutes les choses que j'ai mises sur 'display' sur 'screen' qui est la chose affiché à l'écran
    pygame.display.update() #j'update l'image
    clock.tick(60) #le nombre FPS (Frame Per Second = Images par secondes)
