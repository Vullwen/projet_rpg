import pygame, sys, os, random,time
pygame.init()

def load_map(path): #pour loader la map dans une variable 'game_map'
    f = open(path + '.txt','r') #j'ouvre l'un des fichiers map
    data = f.read() #je met le contenu du fichier dans une variable 'data'
    f.close() #je ferme le fichier (!!! IMPORTANT !!!)
    data = data.split('\n') #je coupe les retours à la ligne
    game_map = [] #je créé la fameuse variable 'game_map'
    for row in data: #pour chaque ligne dans data,
        game_map.append(list(row)) #, j'ajoute cette ligne dans data
    return game_map #je retourne la valeur

map_path = 'Data/Maps/map_1' #le chemin d'accès aux maps
game_map = load_map(map_path) #le fichier ou est stocké la map recois le return de load_map
nb_map = len(os.listdir('Data/Maps')) - 1 #me sert à savoir combien il y a de map, je fait -1 car il y a un fichier de renseignement sur les maps
nbr_map = 1 #me sert à savoir nous sommes à quel map (la 1, la 2,...)

no_physics_tile = ["s","j","e","1","9","2","8"] #la liste des tuiles non physiques

tile_rects = [] #la liste de tuiles qui ont une existance physique

def update_tile_map(game_map,):
    y = 0 #je met à 0 le y, soit la première 'ligne' de la map (en partant du haut)
    for layer in game_map: #je regarde ligne par ligne dans le fichier texte ou se trouve la map
        x = 0 #je met à 0 le x, soit le premier 'bloc' de la map (en partant de la droite)
        for tile in layer: #je regarde du coup 'bloc' par 'bloc' dans chacune des lignes
            if tile == 'm': #si le 'bloc' (appelée tile pour tuile) vaut 1 alors c'est un mur
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1])) #j'affiche son image correspondante ("dirt_img")
            if tile == 's': #si la tuile est 0 alors c'est un sol normal
                display.blit(sol_img_1,(x*16-scroll[0],y*16-scroll[1])) #le -scroll c'est pour enlever le scroll de la CAM
            if tile == 'j': #si la tuile vaut 4 alors c'est le point de spawn du joueur
                display.blit(sol_img_1,(x*16-scroll[0],y*16-scroll[1])) #tu peut essayer sans (le scroll) mais tu verra que c'est pas bien
            if tile == 'e':
                display.blit(sol_img_1,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '1': #la c'est une des deux portes
                display.blit(porte_img_2,(x*16-scroll[0],y*16-scroll[1]))
                porte_2_rect = pygame.Rect(x*16,y*16,16,16) #je fais un rectangle qui me permettera de faire des tests de collisions (au meme endroit que la porte)
            if tile == '9': #la c'est la deuxième porte, dans notre code les portes ont une genre de 'jumelle' et les jumelles téléporte le joueur entre elles
                display.blit(porte_img_1,(x*16-scroll[0],y*16-scroll[1]))
                porte_1_rect = pygame.Rect(x*16,y*16,16,16)
            if tile == '2':
                display.blit(porte_img_1,(x*16-scroll[0],y*16-scroll[1]))
                porte_3_rect = pygame.Rect(x*16,y*16,16,16)
            if tile == '8':
                display.blit(porte_img_2,(x*16-scroll[0],y*16-scroll[1]))
                porte_4_rect = pygame.Rect(x*16,y*16,16,16)
            if tile in no_physics_tile: #la je teste si la tuile fait partie des tuiles qui ne doivent pas avoirs de collisions
                pass #si c'est le cas je ne fais rien
            else:
                tile_rects.append(pygame.Rect(x*16,y*16,16,16)) #là, je fait un rectangle au coordonées de la tuile qui aura une présence physique et j'ajoute ce rectangle dans une liste
            x += 1 #j'ajoute 1 au x pour vérifier la tuile suivante
        y += 1 # j'ajoute 1 au y pour vérifier la ligne suivante
