import random
class Bartram:
    """
    Toutes les actions de Bartram
    """
    def __init__(self):
        """
        Son nom, prénom, age, lore, toutes les infos de l'alliee
        """
        self.nom = "Raolin"
        self.prenom = "Bartram"
        self.age = 33
        self.lore = "Je crois qu'il est capitaine"
        #self.vie =
        #self.pointsDegats =
        #self.

    def dit(self, message):
        """
        permet d'envoyer un message
        """
        print("Bartram dit : {}".format(message))
        self.dit = message
class Gobelin:
    """
    Toutes les actions des gobelins
    """
    def __init__(self):
        """
        Toutes les infos sur les gobelins
        """
        prenoms = ["Taard","Trard","Preegs","Cikz","Xalb","Vrikelb","Pazlyld","Cegherm","Bruisoik","Frazmuzz","Vres",
                "Slarx","Wakx","Preek","Criang","Elberd","Igtycs","Drehic","Ceastalk","Kleatoisb", "Klogs","Zrebs",
                "Crak","Turd","Fralb","Dievneg","Bliavong","Coitiq","Priarkard","Xiegibs"]
        self.nom = "Hemo"
        self.prenom = liste[random.randint(0,len(prenoms))]
        #self.vie =
        #self.pointsDegats =
