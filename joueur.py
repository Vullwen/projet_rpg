import pygame, sys, os, random,time
pygame.init()

animation_frames = {}

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

def collision_test(rect,tiles):
    hit_list = [] #la liste des collisions avec les 'blocs'
    for tile in tiles: #je regarde chaque tuile qui a une présence physique
        if rect.colliderect(tile): #je regarde si elle est en collision avec quelque chose
            hit_list.append(tile) #si oui je l'ajoute à la liste de collion
    return hit_list #je retourne cette liste

def change_action(action_var,frame,new_value): #pour ne pas changer constament les images, ca pourrait faire laguer
    if action_var != new_value: #on regarde si l'actuel image est différente de la nouvelle
        action_var = new_value #si oui, alors l'actuel devient la nouvelle
        frame = 0 #et les frames sont remisent à 0
    return action_var,frame #et on return tout ca

class joueur_class:
    def __init__(self):
        self.moving_right = False #me sert à savoir si le joueur bouge vers la droite
        self.moving_left = False #me sert à savoir si le joueur bouge vers la gauche
        self.moving_up = False #me sert à savoir si le joueur bouge vers le haut
        self.moving_down = False #me sert à savoir si le joueur bouge vers le bas
        self.vertical_momentum = 0 #me sert à savoir si le joueur bouge sur l'axe des ordonnées
        self.life = 120 #me sert à savoir combien de points de vie a le joueur
        self.vie_pallier = 100 #le pallier de points vie avant que l'image de la vie ne s'actualise
        self.path_vie = 0 #afin d'obtenir le chemin d'accès à l'image vie
        self.noclip = False #me sert à savoir si le joueur peut traverser les murs
        self.action_button_pressed = False #si la touche d'action est pressée
        self.animation_frames = animation_frames #je le met dans un dico
        self.player_rect = pygame.Rect(0,0,5,13) #je créé un rectangle qui me permettera de modifier la position du joueur ainsi que de tester si il entre en collision avec quelque chose
        self.animation_database = {} #la je créé la database des animations dans un dico
        self.animation_database['run'] = load_animation('Data/player_animations/run',[7,7]) #la database 'run' contien donc le return de load_animation
        self.animation_database['idle'] = load_animation('Data/player_animations/idle',[7,7,40]) #pareil pour la database de 'idle'
        self.player_movement = [0,0] #la liste comprenant les mouvements du joueur
        self.player_action = 'idle' #l'action du joueur (uniquement pour les animations)
        self.player_frame = 0 #de base la frame du joueur est à 0
        self.player_flip = False #me permettera de retourener l'image du joueur

    def test_movement(self):
        if self.moving_right == True: #si il bouge vers la droite
            self.player_movement[0] += 2 #j'ajoute 2pixels à la première case
        if self.moving_left == True:
            self.player_movement[0] -= 2 #si il va vers la gauche j'en enlève 2
        if self.moving_up == True: #pareil pour l'axe y mais avec la deuxième case du tableau
            self.player_movement[1] -= 2
        if self.moving_down == True:
            self.player_movement[1] += 2

        if self.player_movement[0] == 0: #si le joueur ne bouge pas alors je change son animation
            self.player_action,self.player_frame = change_action(self.player_action,self.player_frame,'idle')
        if self.player_movement[0] > 0: #si le joueur cours à droite alors je change avec l'animation de course
            self.player_flip = False
            self.player_action,self.player_frame = change_action(self.player_action,self.player_frame,'run')
        if self.player_movement[0] < 0: #pareil qu'au dessus
            self.player_flip = True #me permet de retourner l'image pour que le joueur regarde de l'autre coté
            self.player_action,self.player_frame = change_action(self.player_action,self.player_frame,'run')

    def animation(self):
        if self.player_frame >= len(self.animation_database[self.player_action]): #si les frames d'action sont plus grandes que celles qui sont possible
            self.player_frame = 0 #on met les frames à 0
        self.player_img_id = self.animation_database[self.player_action][self.player_frame]
        self.player_img = self.animation_frames[self.player_img_id]

    def lose_life(self,dammage,life,life_img,vie_pallier,path_vie): #si on perd de la vie
        self.life -= dammage #on retire les dommages subit à la vie
        if self.life <= self.vie_pallier: #si la vie est en dessous du palier
            self.path_vie += 1 #on ajoute 1 au chemin d'accès
            self.vie_pallier -= 20 #on baisse jusqu'au prochain palier de 20
        if self.life <= 0:
            print("GAME OVER")
            exit()
        self.life_img = pygame.image.load("Data/images/vie_" + str(path_vie) + ".PNG") #on reload l'image

    def move(self,rect,movement,tiles): #rect = joueur, #tiles = la liste de tuiles avec une présence physique
        #movement = liste. movement[0] = mouvement en x par pixels, movement[1] =  mouvement en y par pixels
        collision_types = {'top':False,'bottom':False,'right':False,'left':False} #les différents moyen de rentrer en collision
        rect.x += movement[0] #je déplace le joueur en x par le mouvement par pixels inscrits
        hit_list = collision_test(rect,tiles) #je teste si le joueur est en collision avec une tuile
        for tile in hit_list: #je regarde tuile par tuile dans la liste des tuiles physique
            if movement[0] > 0: #si le mouvement x est superieur à 0 alors le joueur veut aller à droite
                rect.right = tile.left #honnetement, allez sur internet pour ça, flemme d'expliquer mdr
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
