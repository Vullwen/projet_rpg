from robot import *

cree_fenetre(500,280)

for x in range(20,500,40):
    for y in range(10, 280, 20):
        image(x, y, "images/sols_dongeon 2.png",ancrage="center", tag="")
clic()
