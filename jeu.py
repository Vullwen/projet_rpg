from Map import *
from upemtk import *
from Tkinter import *
import pygame

map = ChangementDeMap(0)
class Joueur:
    """
    Je défini toutes les intéractions clavier ici
    """
    map = ChangementDeMap(0)
    def __init__(self):
        """
        Les informations sur le joueur
        """
        self.pseudo = input("Quel est votre pseudo ? >")
        self.x = 1
        self.y = 1
        #self.origine = ChoixOrigine() #Il faut définir cette fonction et donc les origines

    def déplacer(self, direction):
        """
        Permet de déplacer le joueur en regardant si il le peu
        """
        global map
        for i in range(0,14):
            for k in range(0,25):
                if map[i][k] == "J":#Je regarde ou le joueur est
                    y = i
                    x = k
        map[y][x] = 0                                       #Je supprime l'ancien emplacement du joueur
        if direction == "up":                               #Je regarde si il n'y a pas quelque chose la ou le joueur veut aller
            if map[y - 1][x] == 0 or map[y - 1][x] == "P":  #Si il n'y a rien c'est qu'il y a un 0 ou si il y a un piège P
                y -= 1
        elif direction == "down":
            if map[y + 1][x] == 0 or map[y - 1][x] == "P":
                print("hey")
                y += 1
        elif direction == "left":
            if map[y][x - 1] == 0 or map[y - 1][x] == "P":
                x -= 1
        elif direction == "right":
            if map[y][x + 1] == 0 or map[y - 1][x] == "P":
                x += 1
        map[y][x] = "J"             #Je met la gaumette joueur à la nouvelle position
