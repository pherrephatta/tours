# -*- coding: iso-8859-1 -*-

import helper

# Modifications (17/09/2019):
# Projectile.verifierAtteinteCible()
# Creep.hitBox
# Creep.largeur
# Interaction projectile et creep
#TODO: changer % de 25 de creation de projectile pour un after()
#TODO: Individualiser l'attaque des tours

class Jeu():
    def __init__(self, controleur, largeur=800, hauteur=600):
        self.prtControleur = controleur
        self.largeur = largeur
        self.hauteur = hauteur
        self.partie = Partie(self) # le jeu génère ses parties
        self.listProjectiles=[] #TODO: mettre a un endroit plus approprier (Tour?)
        self.typeAconstruire = "None" # tour a construire, selectionne par le joueur

    def faireAction(self):
        # Faire bouger les creeps et attaquer avec tours
        for i in self.partie.niveau.vague.listCreeps:
            self.prtControleur.syncMoveCreep(i)
        # Animer projectiles et effet sur les creeps
        for j in self.listProjectiles:
            self.prtControleur.syncMoveProjectile(j)
        if self.partie.niveau.vague.vagueCree == False:
            self.prtControleur.syncCreerCreep()
            self.partie.niveau.vague.vagueCree = True

    def bougerCreep(self, creep):
        creep.suivreSentier()
        for j in self.partie.niveau.listTours:
            self.siCreepDansRangeTour(creep, j) #voir comment on passe les tours en référence, ici c'est test
    
    def bougerProjectile(self, projectile):
        projectile.deplacerProjectile()
        if (projectile.verifierAtteinteCible()):
            self.listProjectiles.remove(projectile)
            projectile.cible.soustrairePtsVieCreep(projectile)
            if (projectile.cible.verifierSiCreepEstMort()):
                self.partie.niveau.vague.listCreeps.remove(projectile.cible)
                projectile.cible.transfererValeurCreep()

    def siCreepDansRangeTour(self, creep, tour):
        if abs(tour.posX - creep.positionX) < tour.range:
            if abs(tour.posY - creep.positionY) < tour.range:
                #TODO: discuter frequence de creation des projectiles (timer?)
                if (creep.positionX % tour.freqAttaque) == 0 and (creep.positionY % tour.freqAttaque == 0):
                    tour.attaqueDeTour(creep)

    # Fonction appelée par le contrôleur lorsque la vue détecte un click gauche de la souris.
    # position = position du curseur de la souris lors du click.
    def event_click(self,position):
        print("Click à",position.x,position.y)
        if(self.typeAconstruire=="None"):
            for t in self.partie.niveau.listIconesTours:
                if(t.rect.isInside(position.x,position.y)):
                    self.typeAconstruire=t.type
                    print("Dans icone")
                else:
                    print("Pas dans icone")
        else:
            emplacementLibre=True
            for i in self.partie.niveau.listAires:
                if(i.rect.isInside(position.x,position.y)): #Vérifie si le joueur click sur une aire de construction
                    for t in self.partie.niveau.listTours: #Véfifie si l'aire de construction est libre
                        if((t.posX==i.posX) and (t.posY ==(i.posY-t.hauteur))):
                           print("emplacement non libre")
                           emplacementLibre=False
                    if(emplacementLibre==True):
                        self.partie.niveau.construireTour(self.typeAconstruire, i.posX, i.posY) #
                        self.typeAconstruire="None"

class Partie():
    def __init__(self, jeu):
        self.prtJeu = jeu
        self.niveauCourant = 1
        #normalement tous ces tableaux seraient dans une base de donnée. Par manque de temps ils sont définis ici.
        self.listAiresN1 = ([100,100],[200,100],[300,100],[400,250],[60,280]) #positions des tours sur l'aire de jeu
        self.listIconesToursN1 = ([100,500],[200,500]) #Positions de icones de construction des tours sur l'aire de jeu
        self.niveau = Niveau(self) #TODO: la partie génère DES niveaux?
        self.argentJoueur = 500 #valeur à déterminer

class Niveau():
    def __init__(self, partie):
        self.prtPartie = partie
        self.listAires = [] # Stock les aires de constructions
        self.listTours = [] # Stock les tours construies
        self.listIconesTours = [] # Les icones pour chaque tour
        self.sentier = Sentier(self)
        self.vague = Vague(self, 1) #TODO: Determiner nombre de creeps, types, etc.
        self.genererAiresConstruction()
        self.genererIconesTours()

    #Création d'une tour
    def construireTour(self, type, x,y): #x et y sont les coordonnées de l'aire de construction
        if (type=="Tour"):
            tour=Tour(self,x,y)
            tour.posY=tour.posY-tour.hauteur#On ne veut pas que le centre de la tour soit au centre de l'aire de construction. y-tour.hauteur -> pour que ce soit la base de la tour qui est sur l'aire.
            self.listTours.append(tour)
            self.prtPartie.prtJeu.prtControleur.nouvelleTour(tour)

    #Création des aires de construction selon le tableau défini dans la classe Partie
    def genererAiresConstruction(self):
        if self.prtPartie.niveauCourant==1: #On n'a pas besoin de créer un objet "partie" dans niveau pour accès à ces attributs
            for x,y in self.prtPartie.listAiresN1:
                aire=AireDeConstruction(self,x,y)
                self.listAires.append(aire)

    #Création des icones de tour selon le tableau défini dans la classe Partie
    def genererIconesTours(self):
        if self.prtPartie.niveauCourant==1:
            for x,y in self.prtPartie.listIconesToursN1:
                iconeTour=IconeTour(self,x,y)
                self.listIconesTours.append(iconeTour)

#TODO: passer un dictionaire de creeps?
class Vague():
    def __init__(self, niveau, nbCreeps):
        self.prtNiveau = niveau
        self.listCreeps = []
        self.nbCreepsTotal = nbCreeps
        self.nbCreepsActif = 0
        self.vagueCree = False

#TODO: generaliser la creation de sentier?
class Sentier():
    def __init__(self, niveau):  # parent = niveau
        self.prtNiveau = niveau
        self.largeur = 30
        self.couleur = "black"
        self.chemin = [[0,200],[200,200],[200,400],[350,400],[350,400],[350,150],[500,150],[500,500],[700,500],[700,0]]
#        self.chemin = [[700,0],[700,500],[500,500],[500,150],[350,150],[350,400],[200,400],[200,200],[0,200]] # meme chemin mais inverse

class AireDeConstruction():
    def __init__(self, parent,x,y):
        self.parent=parent
        self.largeur=25
        self.hauteur=5
        self.posX=x
        self.posY=y
        self.couleur="brown"
        self.rect = Rect(self.posX, self.posY, self.largeur,self.hauteur)

class Creep():
    def __init__(self, vague):
        self.prtVague = vague
        self.chIndex = 0
        self.chVelosite = [0,0]
        self.positionX = self.prtVague.prtNiveau.sentier.chemin[0][0]
        self.positionY = self.prtVague.prtNiveau.sentier.chemin[0][1]
        self.ptsVie = 3 #TODO: cette variable devra être passée en argument par la vague
        self.pas = 4 #TODO: cette variable devra être passée en argument par la vague
        self.vitesse = 50
        self.valeur = 10 #TODO: cette variable devra être passée en argument par la vague
        self.puissanceDommage = 1 #TODO: cette variable devra être passée en argument par la vague
        self.largeur = 10
        self.hauteur = 10
        self.hitBox = Rect(self.positionX - self.largeur / 2, self.positionY + self.largeur / 2, self.largeur, self.hauteur) #TODO: largeur change avec le type?

    def suivreSentier(self):
        self.positionX += self.chVelosite[0]
        self.positionY += self.chVelosite[1]
        self.hitBox = Rect(self.positionX - self.largeur / 2, self.positionY - self.hauteur / 2, self.largeur, self.hauteur)
        self.definirVecteur()

    def definirVecteur(self):
        # definit position X
        # verifie si le creep a atteint la fin
        destinationX = self.prtVague.prtNiveau.sentier.chemin[self.chIndex + 1][0]
        destinationY = self.prtVague.prtNiveau.sentier.chemin[self.chIndex + 1][1]
        finX = False
        finY = False
        
        # Creep va vers la droite 
        if self.positionX < destinationX:
            print("droite")
            if self.positionX + self.pas >= destinationX:
                self.chVelosite[0] = destinationX - self.positionX
            else:
                self.chVelosite[0] = self.pas
        # Creep va vers la gauche 
        elif self.positionX > destinationX:
            print("gauche")
            if self.positionX - self.pas <= destinationX:
                self.chVelosite[0] = destinationX - self.positionX
            else:
                self.chVelosite[0] = -self.pas
        # Creep est a la fin du Noeud
        else:
            finX = True
            self.chVelosite[0] = 0

        # Creep va vers le bas
        if self.positionY < destinationY:
            print("bas")
            if self.positionY + self.pas >= destinationY:
                self.chVelosite[1] = destinationY - self.positionY
            else:
                self.chVelosite[1] = self.pas
        # Creep va vers le haut
        elif self.positionY > destinationY:
            print("haut")
            if self.positionY - self.pas <= destinationY:
                self.chVelosite[1] = destinationY - self.positionY
            else:
                self.chVelosite[1] = -self.pas
        # Creep est a la fin du Noeud
        else:
            finY = True
            self.chVelosite[1] = 0
        # Changer le noeud
        if finX == True and finY == True:
            if self.chIndex < len(self.prtVague.prtNiveau.sentier.chemin):
                   self.chIndex += 1
                   finX = False
                   finY = False

    def soustrairePtsVieCreep(self, projectile):
        self.ptsVie -= projectile.puissance

    def verifierSiCreepEstMort(self):
        if self.ptsVie <= 0:
            return True

    def transfererValeurCreep(self):
        self.prtVague.prtNiveau.prtPartie.argentJoueur += self.valeur

class Tour():
    def __init__(self, niveau,x,y):
        self.prtNiveau = niveau
        self.largeur = 15
        self.hauteur = 25
        self.posX = x
        self.posY = y
        self.couleur = "dim grey"
        self.type = "Tour" #TODO: plusieurs types de tour seront implemantes
        self.range = 200
        self.freqAttaque = 25

    def attaqueDeTour(self, creep):
        projectile = Projectile(self, creep)
        print("Projectile créé")
        self.prtNiveau.prtPartie.prtJeu.listProjectiles.append(projectile)

    def calculerDistanceTourCible(self, creep):
        distance = helper.Helper.calcDistance(self.posX, self.posY, creep.positionX, creep.positionY)
        return distance

class IconeTour():
    def __init__(self, niveau, x, y):
        self.prtNiveau = niveau
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
        self.rect = Rect(self.posX, self.posY, self.largeur,self.hauteur)

class Projectile():
    def __init__(self, tour, creep):
        self.prtTour = tour
        self.cible = creep
        self.posX = self.prtTour.posX
        self.posY = self.prtTour.posY
        self.trajectoireX = 0
        self.trajectoireY = 0
        self.vitesse = 50        
        self.puissance = 1
        self.pas = 10

    def deplacerProjectile(self):
        self.calculerTrajectoire()
        self.posX += (self.pas * self.trajectoireX)
        self.posY += (self.pas * self.trajectoireY)

    def verifierAtteinteCible(self):
        if self.cible.hitBox.isInside(self.posX, self.posY):
            print("cible touchée! ")
            return True
        else:
            return False

    def calculerDistanceCible(self):
        distance = helper.Helper.calcDistance(self.posX, self.posY, self.cible.positionX, self.cible.positionY)
        return distance

    def calculerTrajectoire2(self, creep):
            cible=[creep.positionX, creep.positionY]
            distance = self.prtTour.calculerDistanceTourCible(creep)
            incrementX = abs(self.posX - creep.positionX)/distance
            incrementY = abs(self.posY - creep.positionY)/distance
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
            
            self.trajectoireX *= incrementX
            self.trajectoireY *= incrementY

    def calculerTrajectoire(self):
        distance = self.calculerDistanceCible()
        deltaX = abs(self.cible.positionX + self.cible.pas - self.posX) / distance
        deltaY = abs(self.cible.positionY + self.cible.pas - self.posY) / distance
 
        if self.cible.positionX < self.posX:
            self.trajectoireX = (-1 * deltaX) 
        elif self.cible.positionX > self.posX:
            self.trajectoireX = (+1 * deltaX) 
        else:
            self.trajectoireX = 0
 
        if self.cible.positionY < self.posY:
            self.trajectoireY = (-1 * deltaY) 
        elif self.cible.positionY > self.posY:
            self.trajectoireY = (+1 * deltaY) 
        else:
            self.trajectoireY = 0

class Cercle():
    def __init__(self, x, y, rayon):
        self.x = x
        self.y = y
        self.r = rayon

    def isInside(self, x, y):
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

    def isInside(self, x,y):
        if (x > self.x-self.largeur) and (x< self.x+self.largeur) and (y > self.y-self.hauteur) and (y < self.y + self.hauteur):
            return True
        else:
            return False

if __name__ == '__main__':
    print ("Fin Modele")
