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

class map_class:
    def __init__(self):
        self.map_path = 'Data/Maps/map_1' #le chemin d'accès aux maps
        self.meta_map_path = 'Data/Maps/Meta/map_1'
        self.game_map = load_map(self.map_path)
        self.meta_map = load_map(self.meta_map_path)
        self.nb_map = len(os.listdir('Data/Maps')) - 1
        self.nbr_map = 1 #me sert à savoir nous sommes à quel map (la 1, la 2,...)
        self.no_physics_tile = ["s","j","e","p"] #la liste des tuiles non physiques
        self.meta_tile = []
        self.tile_rects = [] #la liste de tuiles qui ont une existance physique
        self.dirt_img = pygame.image.load("Data/images/dirt.PNG") #je load les images des 'blocs' dans des variables
        self.sol_img_1 = pygame.image.load("Data/images/sol_1.PNG")
        self.sol_img_2 = pygame.image.load("Data/images/sol_2.PNG")
        self.porte_img_1 = pygame.image.load("Data/images/porte_1.PNG")
        self.porte_img_2 = pygame.image.load("Data/images/porte_2.PNG")

def look_at_meta(meta_map, player_rect, meta_tile, type):
    indice = 0
    y = 0
    for b_layer in meta_map:
        x = 0
        for b_tile in b_layer:
            if type == 'p':
                for i in range(len(meta_tile)):
                    if b_tile == 'A' and player_rect.colliderect(meta_tile[indice]):
                        return (1,15)
                    indice += 1
                    if b_tile == 'B' and player_rect.colliderect(meta_tile[indice]):
                        return (13,2)
                    indice += 1
                    if b_tile == 'C' and player_rect.colliderect(meta_tile[indice]):
                        return (13,2)
                    indice += 1

                    indice = 0
            x += 1
        y += 1
