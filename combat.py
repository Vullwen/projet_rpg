import math
import random
import robot
import time



x,y = 100, 100  #position joueur
pv = 100
monstre_pv = 50
attaque = 25
game = 0


inventaire_joueur = []


position_arme= 250, 150
def recup():
    global x, y, arme
    if x == 250 and y == 150:
        inventaire_joueur.append(arme)


def arme():
    global attaque
    attaque = attaque + 25
    inventaire_joueur.append(attaque)


def armure():
    global pv
    pv = pv + 50
    inventaire_joueur.append(pv)


def mort():
    global pv, game
    if pv <= 0:
        game = 1


def chest():
    r=random.randint(0,1)
    if r == 0:
        chest=arme
    if r == 1:
        chest=armure

while True:
    if game == 0:
        armure()
        arme()
        chest()
        recup()
    if game == 1:
        attente_clic()
        ferme_fenetre()


