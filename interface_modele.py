# -*- coding: iso-8859-1 -*-

#****Temporaire: j'ai mis dans les classes seulement les éléments dont j'avais besoin. Elles sont à compléter.****
#****TODO: remplacer tous les "tab" (ex tabTours) par "list"

class Jeu():
    def __init__(self, controleur, largeur=800, hauteur=600):
        self.prtControleur = controleur
        self.largeur = largeur
        self.hauteur = hauteur
        self.partie = Partie(self) #le jeu génère ses parties
        self.listProjectiles=[] #TODO: mettre a un endroit plus approprier

    def faireAction(self):
        for i in self.partie.niveau.vague.listCreeps:
            i.suivreSentier()
            self.verifierCreepDansRangeTour(i, self.partie.niveau.tour) #TODO: revoir comment on passe les tours en référence
        for j in self.listProjectiles:
            j.deplacerProjectiles()

    def verifierCreepDansRangeTour(self, creep, tour):
        if abs(tour.posX - creep.positionX) < tour.range:
            if abs(tour.posY - creep.positionY) < tour.range:
                print("FEU !!")
                #TODO: discuter frequence de creation des projectiles (timer?)
                if (creep.positionX % tour.freqAttaque) == 0 and (creep.positionY % tour.freqAttaque == 0):
                    tour.attaqueDeTour(creep)

class Partie():
    def __init__(self, jeu):
        self.prtJeu = jeu
        self.niveauCourant = 1
        #normalement tous ces tableaux seraient dans une base de donnée. Par manque de temps ils sont définis ici.
        self.tabAiresN1 = ([100,100],[200,100],[300,100]) #positions des tours sur l'aire de jeu
        self.tabToursN1 = ('Tour', 'None', 'Tour') #TODO: ce tableau sera rempli lors des phases de construction
        self.tabIconesToursN1 = ([100,500],[200,500]) #Positions de icones de construction des tours sur l'aire de jeu
        self.niveau = Niveau(self) #la partie génère ses niveaux

class Niveau():
    def __init__(self, partie):
        self.prtPartie = partie
        self.listAires = [] # Stock les aires de constructions
        self.listTours = [] # Stock les tours construies
        self.listIconesTours = [] # Les icones pour chaque tour
        self.sentier = Sentier(self)
        self.vague = Vague(self)
        self.tour = Tour(self, 300, 100) #TODO: Position temporaire, pref. une liste
#        self.nbCreepsDansUneVague = 1 #TODO: nombre de creeps dans une vague
        self.creationAiresConstruction()
        self.creationTours()
        self.creationIconesTours()

        #Création des aires de construction selon le tableau défini dans la classe Partie
    def creationAiresConstruction(self):
        if self.prtPartie.niveauCourant==1: #On n'a pas besoin de créer un objet "partie" dans niveau pour accès à ces attributs
            for x,y in self.prtPartie.tabAiresN1:
                aire=AireDeConstruction(self,x,y)
                self.listAires.append(aire)

    #Création des tours selon le tableau défini dans la classe Partie
    def creationTours(self):
        index=0
        if self.prtPartie.niveauCourant==1:
            for i in self.prtPartie.tabToursN1: #
                if i=="Tour":  #Éventuellement il va y avoir un if par type de tour
                    x,y=self.prtPartie.tabAiresN1[index]
                    tour=Tour(self,x,y)
                    tour.posY=tour.posY-tour.hauteur #Pour que ce soit la base de la tour qui soit au centre de l'aire de construction
                    self.listTours.append(tour)
                index=index+1

    #Création des icones de tour selon le tableau défini dans la classe Partie
    def creationIconesTours(self):
        if self.prtPartie.niveauCourant==1:
            for x,y in self.prtPartie.tabIconesToursN1:
                iconeTour=IconeTour(self,x,y)
                self.listIconesTours.append(iconeTour)

class Vague():
    def __init__(self, niveau):
        self.prtNiveau = niveau
        self.listCreeps = []
#        self.nbCreep = self.prtNiveau.nbCreepsDansUneVague #TODO: Creeps dans une vague
        self.creerCreep()

    def creerCreep(self):
        creep = Creep(self)
        self.listCreeps.append(creep)
        print("objet creep init : un Creep créé") #TODO: A enlever -- juste pour test

class Creep():
    def __init__(self, vague):
        self.prtVague = vague
        self.positionX = self.prtVague.prtNiveau.sentier.coord0[0]
        self.positionY = self.prtVague.prtNiveau.sentier.coord0[1]
        self.ptsVie = 3 #TODO: cette variable devra être passée en argument par la vague
        self.vitesse = 2 #TODO: cette variable devra être passée en argument par la vague
        self.valeur = 10 #TODO: cette variable devra être passée en argument par la vague
        self.puissanceDommage = 1 #TODO: cette variable devra être passée en argument par la vague

        # print("coordonnées X de départ du Creep: ", self.positionX)
        # print("coordonnées Y de départ du Creep: ", self.positionY)

        #TODO: collison box ? ou calcul d'un range p/r à sa position pour l'éliminer


    def suivreSentier(self):
        if self.positionX <  self.prtVague.prtNiveau.sentier.coord1[0]:
            self.positionX += self.vitesse
            #print("c1")
        elif self.positionY < self.prtVague.prtNiveau.sentier.coord2[1] and self.positionX < self.prtVague.prtNiveau.sentier.coord4[0]:
            self.positionY += self.vitesse
            #print("c2")
        elif self.positionX < self.prtVague.prtNiveau.sentier.coord3[0]:
            self.positionX += self.vitesse
            #print("c3")
        elif self.positionY > self.prtVague.prtNiveau.sentier.coord4[1] and self.positionX > self.prtVague.prtNiveau.sentier.coord1[0] and self.positionX <= self.prtVague.prtNiveau.sentier.coord5[0]:
            self.positionY -= self.vitesse
            #print("c4")
        elif self.positionX < self.prtVague.prtNiveau.sentier.coord5[0]:
            self.positionX += self.vitesse
            #print("c5")
        elif self.positionY < self.prtVague.prtNiveau.sentier.coord6[1] and self.positionX > self.prtVague.prtNiveau.sentier.coord5[0] and self.positionX < self.prtVague.prtNiveau.sentier.coord7[0]:
            self.positionY += self.vitesse
            #print("c6")
        elif self.positionX < self.prtVague.prtNiveau.sentier.coord7[0]:
            self.positionX += self.vitesse
            #print("c7")
        elif self.positionX >= self.prtVague.prtNiveau.sentier.coord7[0]:
            self.positionY -= self.vitesse
            #print("c8")


#TODO: generaliser la creation de sentier?
class Sentier():
    def __init__(self, niveau):  # parent = niveau
        self.prtNiveau = niveau
        self.coord0 = [0,200]
        self.coord1 = [200,200]
        self.coord2 = [200,400]
        self.coord3 = [350,400]
        self.coord4 = [350,150]
        self.coord5 = [500, 150]
        self.coord6 = [500, 500]
        self.coord7 = [700, 500]
        self.coord8 = [700, 0]
        self.largeur = 30
        self.couleur = "black"

        self.trace = [self.coord0, self.coord1, self.coord2, self.coord3, self.coord4, self.coord5,
                      self.coord6, self.coord7, self.coord8]

class AireDeConstruction():
    def __init__(self, parent,x,y):
        self.parent=parent #TODO: parent -> ?
        self.largeur=25
        self.hauteur=5
        self.posX=x
        self.posY=y
        self.couleur="brown"

class Tour():
    def __init__(self, niveau,x,y):
        self.prtNiveau = niveau
        self.largeur = 15 #TODO: dimensions en pixels?
        self.hauteur = 25 #TODO: dimensions en pixels?
        self.posX = x
        self.posY = y
        self.couleur = "dim grey"
        self.type = "Tour" #TODO: plusieurs types de tour seront implantés
        self.range=130
        self.freqAttaque = 25
        self.trajectoireX = 0
        self.trajectoireY= 0

    def calculerTrajectoire(self, creep):
        # creep = self.parent.vague.tabCreeps[indCreep] #Je ne suis pas décidée de comment on déclenche les attaques... en fonction des creeps qui se déplacent ?
        cible=[creep.positionX, creep.positionY]
        print("La cible est ", cible)
        if cible[0] < self.posX:
            self.trajectoireX = -1
        elif cible[0] > self.posX:
            self.trajectoireX = +1
        else:
            trajectoireX = 0
        if cible[1] < self.posY:
            self.trajectoireY = -1
        elif cible[1] > self.posY:
            self.trajectoireY = +1
        else:
            self.trajectoireY = 0

    def attaqueDeTour(self, creep):
        self.calculerTrajectoire(creep)
        #cibleAvecDepAnticipe=[cible[0]+creep.vitesse, cible[1]+creep.vitesse] #voir pour raffiner selon deplacement et position tour
        projectile=Projectile(self)
        print("Projectile créé")
        self.prtNiveau.prtPartie.prtJeu.listProjectiles.append(projectile)

class IconeTour():
    def __init__(self, parent,x,y):
        self.parent=parent #TODO: parent -> ?
        self.largeur=30
        self.hauteur=30
        self.posX=x
        self.posY=y
        self.couleur="light grey"
        self.type="Tour" #TODO: plusieurs types de tour seront implantés
        self.tour=Tour(self,x,y)
        #Prend une image de tour et la réduit de moitié. C'est cette image qui apparait à l'intérieur de l'icone
        self.tour.largeur=self.tour.largeur/2
        self.tour.hauteur=self.tour.hauteur/2

class Projectile():
    def __init__(self, tour): # parent = tour
        self.parent=tour
        self.posX=self.parent.posX
        self.posY=self.parent.posY
        self.puissance=1
        self.vitesse = 50

    def deplacerProjectiles(self):
        self.posX += (self.vitesse * self.parent.trajectoireX)
        self.posY += (self.vitesse * self.parent.trajectoireY)

if __name__ == '__main__':
    print ("Fin Modele")
