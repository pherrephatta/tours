# -*- coding: iso-8859-1 -*-
import threading
import helper

#TODO: projectiles trajectoire
#TODO: sprites temporaires sur les icones de tours
#TODO: delai de creeps
#           - after -> timer
#           - global thread
#           - relative positions
#           - event threads
#TODO: integrer julie vue, modele


class Timer():
    def __init__(self, jeu):
        self.thread = Thread(None, self.jeu.niveau[0])
        self.prtJeu = jeu
        self.time = 0
        self.incrTime()

    def incrTime(self):
        threading.Timer(1.0, self.incrTime).start
        self.time = self.time + 1
        print(self.time)

class Jeu():
    def __init__(self, controleur, largeur=800, hauteur=600):
        self.prtControleur = controleur
        self.largeur = largeur
        self.hauteur = hauteur
        self.partie = Partie(self) #le jeu génère ses parties
        self.listProjectiles=[] #TODO: mettre a un endroit plus approprier (Tour)

    def faireAction(self):
        for i in self.partie.niveau.vagues[0].listCreeps:
            i.suivreSentier()
            self.verifierCreepDansRangeTour(i, self.partie.niveau.tour) #voir comment on passe les tours en référence, ici c'est test
        for j in self.listProjectiles:
            j.deplacerProjectile(j.creep)
            if (j.verifierAtteinteCible(j.creep)):
                self.listProjectiles.remove(j)

    def verifierCreepDansRangeTour(self, creep, tour):
        if abs(tour.posX - creep.positionX) < tour.range:
            if abs(tour.posY - creep.positionY) < tour.range:
                #TODO: discuter frequence de creation des projectiles (timer?)
                if (creep.positionX % tour.freqAttaque) == 0 and (creep.positionY % tour.freqAttaque == 0):
                    tour.attaqueDeTour(creep)

class Partie():
    def __init__(self, jeu):
        self.prtJeu = jeu
        self.niveauCourant = 1
        #normalement tous ces tableaux seraient dans une base de donnée. Par manque de temps ils sont définis ici.
        self.listAiresN1 = ([100,100],[200,100],[300,100]) #positions des tours sur l'aire de jeu
        self.listToursN1 = ('Tour', 'None', 'Tour') #TODO: ce tableau sera rempli lors des phases de construction
        self.listIconesToursN1 = ([100,500],[200,500]) #Positions de icones de construction des tours sur l'aire de jeu
        self.niveau = Niveau(self) #TODO: la partie génère ses niveaux

class Niveau():
    def __init__(self, partie):
        self.prtPartie = partie
        self.listAires = [] # Stock les aires de constructions
        self.listTours = [] # Stock les tours construies
        self.listIconesTours = [] # Les icones pour chaque tour
        self.sentier = Sentier(self)
        self.vagues = [Vague(self, 5)] #TODO: Determiner nombre de creeps, types, etc.
        self.tour = Tour(self, 300, 100) #TODO: Position temporaire, pref. une liste
#        self.nbCreepsDansUneVague = 1 #TODO: A determiner
        self.creationAiresConstruction()
        self.creationTours()
        self.creationIconesTours()

        #Création des aires de construction selon le tableau défini dans la classe Partie
    def creationAiresConstruction(self):
        if self.prtPartie.niveauCourant==1: #On n'a pas besoin de créer un objet "partie" dans niveau pour accès à ces attributs
            for x,y in self.prtPartie.listAiresN1:
                aire=AireDeConstruction(self,x,y)
                self.listAires.append(aire)

    #Création des tours selon le tableau défini dans la classe Partie
    def creationTours(self):
        index=0
        if self.prtPartie.niveauCourant==1:
            for i in self.prtPartie.listToursN1: #
                if i=="Tour":  #Éventuellement il va y avoir un if par type de tour
                    x,y=self.prtPartie.listAiresN1[index]
                    tour=Tour(self,x,y)
                    tour.posY=tour.posY-tour.hauteur #Pour que ce soit la base de la tour qui soit au centre de l'aire de construction
                    self.listTours.append(tour)
                index=index+1

    #Création des icones de tour selon le tableau défini dans la classe Partie
    def creationIconesTours(self):
        if self.prtPartie.niveauCourant==1:
            for x,y in self.prtPartie.listIconesToursN1:
                iconeTour=IconeTour(self,x,y)
                self.listIconesTours.append(iconeTour)

#TODO: passer un dictionaire de creeps?
class Vague():
    def __init__(self, niveau, nbCreeps):
        self.prtNiveau = niveau
        self.listCreeps = []
        self.activeCreeps = []
        self.nbCreeps = nbCreeps
        self.nbCreepsActif = 0
#        self.nbCreep = self.prtNiveau.nbCreepsDansUneVague #TODO: Creeps dans une vague
        self.creerCreep()

    def creerCreep(self):
        #TODO: ajouter differents type de creep, etc.
        creep = Creep(self)
        self.listCreeps.append(creep)

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

class Creep():
    def __init__(self, vague):
        self.prtVague = vague
        self.positionX = self.prtVague.prtNiveau.sentier.coord0[0]
        self.positionY = self.prtVague.prtNiveau.sentier.coord0[1]
        self.ptsVie = 3 #TODO: cette variable devra être passée en argument par la vague
        self.vitesse = 5 #TODO: cette variable devra être passée en argument par la vague
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

class Tour():
    def __init__(self, niveau,x,y):
        self.prtNiveau = niveau
        self.largeur = 15 #TODO: dimensions en pixels?
        self.hauteur = 25 #TODO: dimensions en pixels?
        self.posX = x
        self.posY = y
        self.couleur = "dim grey"
        self.type = "Tour" #TODO: plusieurs types de tour seront implantés
        self.range = 200
        self.freqAttaque = 25
        #TODO: Ajuster trajectoire, etc.
#        self.trajectoireX = 0
#        self.trajectoireY= 0
#        self.cible

    def calculerAngleVersCible(self, creep):
        angle = helper.Helper.calcAngle(self.posXtour,self.posYtour,creep.positionX,creep.positionY)
        return angle

    def calculerDistanceTourCible(self,creep):
        distance = helper.Helper.calcDistance(self.posXtour,self.posYtour,creep.positionX,creep.positionY)
        return distance

    def calculerPointAttaque(self, angle, distance, x,y):
        ptAttaque = helper.Helper.getAngledPoint(angle,distance,x,y)
        return ptAttaque

    def attaqueDeTour(self, creep):
        #self.calculerTrajectoire(creep)
        #cibleAvecDepAnticipe=[cible[0]+creep.vitesse, cible[1]+creep.vitesse] #voir pour raffiner selon deplacement et position tour
        #angle = self.calculerAngleVersCible(creep)
        #distance = self.calculerDistanceTourCible(creep)
        #ptAttaque = self.calculerPointAttaque(angle, distance, self.posXtour, self.posYtour)
        #print("angle de tir: ", angle)
        #print("distance de tir: ", distance)
        #print("ptAttaque: ", ptAttaque)
        #print ("position creep: ", creep.positionX, creep.positionY)
        #input ("stop test")
        projectile = Projectile(self, creep)
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
    def __init__(self, tour, creep): # parent = tour
        self.prtTour = tour
        self.posX=self.prtTour.posX
        self.posY=self.prtTour.posY
        self.puissance = 1
        self.vitesse = 50
        self.creep = creep
        self.trajectoireX = 0
        self.trajectoireY = 0
        self.calculerTrajectoire(self.creep)

    def deplacerProjectile(self, creep):
        self.posX += (self.vitesse * self.trajectoireX)
        self.posY += (self.vitesse * self.trajectoireY)

    def verifierAtteinteCible(self, creep):
        buffer = 50 #eventuellement sera hit box du creep
        if ( abs(self.posX - creep.positionX) <= buffer):
            if ( abs(self.posY - creep.positionY) <= buffer):
                print("cible touchée! ")
                return True
        return False

    #TODO: Pas bon -- modifier trajectoire
    def calculerTrajectoire(self, creep):
        # creep = self.parent.vague.tabCreeps[indCreep] #Je ne suis pas décidée de comment on déclenche les attaques... en fonction des creeps qui se déplacent ?
        cible=[creep.positionX, creep.positionY]
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



class Cercle():
    def __init__(self, x, y, rayon):
        self.x = x
        self.y = y
        self.r = rayon

    def siDansCercle(self, x, y):
        delta = pow((x - self.x), 2) + pow((x - self.x), 2)
        if delta > pow(self.r, 2):
            return False
        return True

class Rect():
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def siDansRect(self, x, y):
        if x > self.x and x < self.x + self.largeur:
            if y > self.y and y < self.y + self.hauteur:
                return True
        else:
            return False

if __name__ == '__main__':
    print ("Fin Modele")
