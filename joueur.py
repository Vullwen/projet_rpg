import pygame, sys, os, random,time
pygame.init()

class joueur:
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
        self.animation_frames = {} #je le met dans un dico
        self.player_rect = pygame.Rect(0,0,5,13) #je créé un rectangle qui me permettera de modifier la position du joueur ainsi que de tester si il entre en collision avec quelque chose
        self.true_scroll = [0,0]
        self.animation_database = {} #la je créé la database des animations dans un dico
        self.animation_database['run'] = load_animation('Data/player_animations/run',[7,7]) #la database 'run' contien donc le return de load_animation
        self.animation_database['idle'] = load_animation('Data/player_animations/idle',[7,7,40]) #pareil pour la database de 'idle'
        self.player_movement = [0,0] #la liste comprenant les mouvements du joueur

def test_mouvement(self)
        if self.moving_right == True: #si il bouge vers la droite
            self.player_movement[0] += 2 #j'joute 2pixels à la première case
        if self.moving_left == True:
            self.player_movement[0] -= 2 #si il va vers la gauche j'en enlève 2
        if self.moving_up == True: #pareil pour l'axe y mais avec la deuxième case du tableau
            self.player_movement[1] -= 2
        if self.moving_down == True:
            self.player_movement[1] += 2

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


    def load_animation(self,path,frame_durations):
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

    def move(rect,movement,tiles): #rect = joueur, #tiles = la liste de tuiles avec une présence physique
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
