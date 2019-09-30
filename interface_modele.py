# -*- coding: iso-8859-1 -*-

import helper
#import winsound #TODO: winsound

# Trello?
#TODO: Changer le choix de tour meme avec une tour deja selectionner
#TODO: Sprites
#TODO: Animation des sprites
#TODO: Ecran proportionnel (frame de construction?)
#TODO: --Indicateur du curseur(?)

class Jeu():
    def __init__(self, controleur, largeur=800, hauteur=600):
        self.prtControleur = controleur
        self.largeur = largeur # largeur de fenetre
        self.hauteur = hauteur
        self.typeAconstruire = "None" # Joueur - selection de tour 
        self.partie = Partie(self)

    # Recoit appel du controlleur a interval regulier
    def faireAction(self):
        if self.partie.niveau.vague.nbCreepsActif < self.partie.niveau.vague.nbCreepsTotal:
            if self.prtControleur.msTime % 1000 == 0: #TODO: delai de creation
                self.partie.niveau.vague.listCreeps.append(CreepDifficile(self.partie.niveau.vague))
                self.partie.niveau.vague.nbCreepsActif += 1;
        # Faire bouger les creeps
        for i in self.partie.niveau.vague.listCreeps:
            if self.prtControleur.msTime > (i.lastMouvmt + i.vitesse) or self.prtControleur.msTime < i.lastMouvmt:
                i.suivreSentier()
                i.verifierFinSentier()
                i.lastMouvmt = self.prtControleur.msTime
            # Attaquer avec tours
            self.partie.niveau.attaquerCreeps(i)
        # Avancer projectiles
        for i in self.partie.niveau.listTours:
            # Creation de nouveau projectiles
            if i.cible is not None:
                if not i.siCreepDansRange(i.cible):
                    i.cible = None 
                elif (self.prtControleur.msTime % i.freqAttaque) == 0:
                    i.creerProjectile()
                    #winsound.PlaySound(i.son, winsound.SND_FILENAME | winsound.SND_ASYNC)
            for j in i.listProjectiles:
                j.bougerProjectile()

    # Fonction appelée par le contrôleur lorsque la vue détecte un click gauche de la souris.
    # position = position du curseur de la souris lors du click.
    def event_click(self, position):
        print("Click à", position.x, position.y)
        if (self.typeAconstruire == "None"):
            for t in self.partie.niveau.listIconesTours:
                if t.rect.isInside(position.x, position.y):
                    if(t.tour.cout<=self.partie.argentJoueur):
                        self.typeAconstruire = t.typeTour
                        self.prtControleur.afficherDescriptionTour(t)
                        print("Dans icone")
                    else:
                        self.prtControleur.manqueDargent()
                        print("Pas d'argent")
                else:
                    print("Pas dans icone")
        else:
            emplacementLibre=True
            for i in self.partie.niveau.listAires:
                if i.rect.isInside(position.x, position.y): #Vérifie si le joueur click sur une aire de construction
                    for t in self.partie.niveau.listTours: #Véfifie si l'aire de construction est libre
                        if t.posX == i.posX and t.posY == (i.posY - t.hauteur):
                            print("Emplacement non libre")
                            emplacementLibre = False
                    if emplacementLibre is True:
                        self.partie.niveau.construireTour(self.typeAconstruire, i.posX, i.posY)
                        self.typeAconstruire = "None"
                        self.prtControleur.effacerDescriptionTour()
                        
    def event_click_droit(self, event): 
        if(self.typeAconstruire!="None"):
            self.typeAconstruire="None"
            self.prtControleur.constructionAnnulee()

class Partie():
    def __init__(self, jeu):
        self.prtJeu = jeu
        self.niveauCourant = 1
        #normalement tous ces tableaux seraient dans une base de donnée. Par manque de temps ils sont définis ici.
        self.listAiresN1 = ([100,100],[200,100],[300,100],[400,250],[60,280]) #positions des tours sur l'aire de jeu
        self.listIconesToursN1 = ([40,490],[100,490],[40,560],[100,560]) #Positions de icones de construction des tours sur l'aire de jeu
        self.listTypeIconeN1 = ("TourRoche","TourFeu","TourCanon","TourGoo")
        self.argentJoueur = 500 #valeur à déterminer
        self.ptsVieJoueur = 2
        self.niveau = Niveau(self)

    def verifierGameOver(self):
        if self.ptsVieJoueur <= 0:
            self.prtJeu.prtControleur.annulerClicks()
            return True
        return False

    def verifierFinNiveau(self):
        if not self.niveau.vague.listCreeps:
            self.prtJeu.prtControleur.annulerClicks()
            return True
        return False

#TODO: Determiner nombre de creeps, types, etc.
class Niveau():
    def __init__(self, partie):
        self.prtPartie = partie
        self.listAires = [] # Stock les aires de constructions
        self.listTours = [] # Stock les tours construies
        self.listIconesTours = [] # Les icones pour chaque tour
        #self.sentier = Sentier(self)
        self.sentier = Sentier2(self) #TODO: Implementation de vagues

        self.vague = Vague(self, 5)
        self.genererAiresConstruction()
        self.genererIconesTours()
        self.interfaceJeu = Interface_jeu()
        self.zoneDescription = Zone_description()

    #Création d'une tour
    def construireTour(self, typeTour, x,y): #x et y sont les coordonnées de l'aire de construction
        if typeTour == "TourRoche":
            tour = Tour_Roche(self,x,y)
        elif typeTour == "TourFeu":
            tour = Tour_Feu(self,x,y)
        elif typeTour == "TourCanon":
            tour = Tour_Canon(self,x,y)
        elif typeTour == "TourGoo":
            tour = Tour_Goo(self,x,y)
        #on charge le joueur le coût de la tour
        self.prtPartie.argentJoueur -= tour.cout
        # On ne veut pas que le centre de la tour soit au centre de l'aire de construction. 
        tour.posY = tour.posY - tour.hauteur/2
        # ^-- pour que ce soit la base de la tour qui est sur l'aire.
        self.listTours.append(tour)
        self.prtPartie.prtJeu.prtControleur.nouvelleTour(tour)
#        winsound.PlaySound(tour.sonConstruction, winsound.SND_FILENAME | winsound.SND_ASYNC) #TODO: winsound
        
    #Création des aires de construction selon le tableau défini dans la classe Partie
    def genererAiresConstruction(self):
        if self.prtPartie.niveauCourant == 1: #On n'a pas besoin de créer un objet "partie" dans niveau pour accès à ces attributs
            for x,y in self.prtPartie.listAiresN1:
                aire=AireDeConstruction(self,x,y)
                self.listAires.append(aire)

    #Création des icones de tour selon le tableau défini dans la classe Partie
    def genererIconesTours(self):
        index = 0
        if self.prtPartie.niveauCourant == 1:
            for x,y in self.prtPartie.listIconesToursN1:
                iconeTour = IconeTour(self,x,y,self.prtPartie.listTypeIconeN1[index])
                self.listIconesTours.append(iconeTour)
                index = index + 1

    def attaquerCreeps(self, creep):
        for i in self.listTours:
            if i.cible is None:
                if i.siCreepDansRange(creep):
                    i.cible = creep

#TODO: passer un dictionaire de creeps?
class Vague():
    def __init__(self, niveau, nbCreeps):
        self.prtNiveau = niveau
        self.listCreeps = []
        self.nbCreepsTotal = nbCreeps
        self.nbCreepsActif = 0
        self.vagueCree = False

class Sentier():
    def __init__(self, niveau):  # parent = niveau
        self.prtNiveau = niveau
        self.largeur = 30
        self.couleur = "black"
        self.chemin = [[0,200],[200,200],[200,400],[350,400],[350,150],[500,150],[500,400],[700,400],[700,0]]
#        self.chemin = [[700,0],[700,500],[500,500],[500,150],[350,150],[350,400],[200,400],[200,200],[0,200]] # meme chemin mais inverse

class Sentier2():
    def __init__(self, niveau):
        self.prtNiveau = niveau
        self.largeur = 60
        self.couleur = "#1A1A50"
        self.chemin = [[0,150],[650,150],[650,300],[150,300],[150,400],[800,400]] 

class AireDeConstruction():
    def __init__(self, parent,x,y):
        self.parent = parent
        self.largeur = 25
        self.hauteur = 5
        self.posX = x
        self.posY = y
        self.couleur = "darkolivegreen"
        self.rect = Rect(self.posX, self.posY, self.largeur,self.hauteur)

#TODO: Evaluer les variables a passer en argument
#TODO: largeur change avec le type?
class Creep():
    def __init__(self, vague):
        self.prtVague = vague
        self.chIndex = 0
        self.chVelosite = [0,0]
        self.positionX = self.prtVague.prtNiveau.sentier.chemin[0][0]
        self.positionY = self.prtVague.prtNiveau.sentier.chemin[0][1]
        self.ptsVie = 3
        self.pas = 1
        self.vitesse = 20 
        self.valeur = 10
        self.puissanceDommage = 1
        self.largeur = 30 
        self.hauteur = 15
        self.hitBox = Rect(self.positionX - self.largeur / 2, self.positionY + self.largeur / 2, self.largeur, self.hauteur) 
        self.lastMouvmt = 0
        self.son = "./assets/sounds/creep_coin.wav"

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
            if self.positionX + self.pas >= destinationX:
                self.chVelosite[0] = destinationX - self.positionX
            else:
                self.chVelosite[0] = self.pas
        # Creep va vers la gauche 
        elif self.positionX > destinationX:
            if self.positionX - self.pas <= destinationX:
                self.chVelosite[0] = destinationX - self.positionX
            else:
                self.chVelosite[0] = -self.pas
        # Creep est a la fin du Noeud en X
        else:
            finX = True
            self.chVelosite[0] = 0

        # Creep va vers le bas
        if self.positionY < destinationY:
            if self.positionY + self.pas >= destinationY:
                self.chVelosite[1] = destinationY - self.positionY
            else:
                self.chVelosite[1] = self.pas
        # Creep va vers le haut
        elif self.positionY > destinationY:
            if self.positionY - self.pas <= destinationY:
                self.chVelosite[1] = destinationY - self.positionY
            else:
                self.chVelosite[1] = -self.pas
        # Creep est a la fin du Noeud en Y
        else:
            finY = True
            self.chVelosite[1] = 0

        # Changer le noeud
        if finX is True and finY is True:
            if self.chIndex < len(self.prtVague.prtNiveau.sentier.chemin) - 1:
                self.chIndex += 1
                finX = False
                finY = False

    def soustrairePtsVieCreep(self, projectile):
        self.ptsVie -= projectile.puissance

    def verifierSiCreepEstMort(self):
        if self.ptsVie <= 0:
            return True
        return False

    def transfererValeurCreep(self):
        self.prtVague.prtNiveau.prtPartie.argentJoueur += self.valeur
#        winsound.PlaySound(self.son, winsound.SND_FILENAME | winsound.SND_ASYNC) #TODO: winsound

    def verifierFinSentier(self):
        chemin = self.prtVague.prtNiveau.sentier.chemin
        fin = chemin[len(chemin) - 1]
        if self.positionX >= fin[0]:
            if self.positionY <= fin[1]:
                self.prtVague.prtNiveau.prtPartie.ptsVieJoueur -= self.puissanceDommage
                self.prtVague.listCreeps.remove(self)
                return True
        return False

    def effacerCreep(self, projectile):
        self.soustrairePtsVieCreep(projectile)
        if self.verifierSiCreepEstMort():
            self.transfererValeurCreep()
            self.prtVague.listCreeps.remove(self)
            for t in self.prtVague.prtNiveau.listTours:
                if t.cible == self:
                    t.cible = None
        
class CreepFacile(Creep):
     def __init__(self,vague):
        Creep.__init__(self, vague)
        self.type = "creepFacile"
        self.ptsVie = 3 
        self.pas = 2 
        self.vitesse = 5
        self.valeur = 10 
        self.puissanceDommage = 1 
        
class CreepDifficile(Creep):
     def __init__(self,vague):
        Creep.__init__(self, vague)
        self.type = "creepDifficile"
        self.ptsVie = 10 
        self.pas = 1 
        self.vitesse = 20
        self.valeur = 20 
        self.puissanceDommage = 5 

class CreepBoss(Creep):
    def __init__(self, vague):
        Creep.__init__(self, vague)
        self.type = "creepBoss"
        self.ptsVie = 50
        self.pas = 1
        self.vitesse = 30
        self.valeur = 100
        self.puissanceDommage = 25

class Tour():
    def __init__(self, niveau,x,y):
        self.prtNiveau = niveau
        self.largeur = 70
        self.hauteur = 100
        self.posX = x
        self.posY = y
        self.typeTour = "Tour"
        self.range = 200
        self.freqAttaque = 100
        self.cible = None
        self.listProjectiles=[]
        self.pretTir = True
        self.puissance = 1
        self.cout = 100
        self.sonConstruction = "./assets/sounds/tour_construction.wav"

    def siCreepDansRange(self, creep):
        if abs(self.posX - creep.positionX) < self.range:
            if abs(self.posY - creep.positionY) < self.range:
                return True
        return False

    def calculerDistanceTourCible(self, creep):
        distance = helper.Helper.calcDistance(self.posX, self.posY, creep.positionX, creep.positionY)
        return distance

    def attaquerCible(self):
        self.pretTir = True

class Tour_Roche(Tour):
    def __init__(self, niveau,x,y):
        Tour.__init__(self, niveau,x,y)
        self.type = "TourRoche"
        self.couleur = "dim grey"
        self.cout = 100
        self.description = "Une tour qui lance des pierres à l'unité." \
                            + "\nDommage: " + str(self.puissance) + "\nFréquence: " + str(self.freqAttaque) + "\nCout: " + str(self.cout)
        self.son = "./assets/sounds/tour_roche.wav" 

    def creerProjectile(self):                
        self.listProjectiles.append(Projectile_Roche(self))

class Tour_Feu(Tour):
    def __init__(self, niveau,x,y):
        Tour.__init__(self, niveau,x,y)
        self.type = "TourFeu"
        self.couleur = "red"
        self.cout = 150
        self.description = "Une tour qui lance des boules de feu qui\nsuivent leurs cibles." \
                            + "\nDommage: " + str(self.puissance) + "\nFréquence: " + str(self.freqAttaque) + "\nCout: " + str(self.cout)
        self.son = "./assets/sounds/tour_feu.wav" 
        self.freqAttaque = 500
        self.range = 150
        self.puissance = 4

    def creerProjectile(self):                
        self.listProjectiles.append(Projectile_Circulaire(self))
       
class Tour_Canon(Tour):
    def __init__(self, niveau,x,y):
        Tour.__init__(self, niveau,x,y)
        self.type = "TourCanon"
        self.couleur = "blue"
        self.cout = 200
        self.description = "Une tour qui lance des boules de canon\nen lignes droites" \
                            + "\nDommage: " + str(self.puissance) + "\nFréquence: " + str(self.freqAttaque) + "\nCout: " + str(self.cout)
        self.son = "./assets/sounds/tour_cannon.wav" 

    def creerProjectile(self):                
        self.listProjectiles.append(Projectile_Canon(self))

class Tour_Goo(Tour):
    def __init__(self, niveau,x,y):
        Tour.__init__(self, niveau,x,y)
        self.type="TourGoo"
        self.couleur="dark green"
        self.cout=120
        self.description = "Une tour qui lance des projectiles gluants\nqui ralentissent leurs cibles" \
                            + "\nDommage: " + str(self.puissance) + "\nFréquence: " + str(self.freqAttaque) + "\nCout: " + str(self.cout)
        self.son = "./assets/sounds/tour_goo.wav" 

    def creerProjectile(self):                
        self.listProjectiles.append(Projectile_Goo(self))

class IconeTour():
    def __init__(self, niveau, x, y, typeTour):
        self.prtNiveau = niveau
        self.largeur = 25
        self.hauteur = 25
        self.posX = x
        self.posY = y
        self.couleur="light grey"
        self.typeTour = typeTour
        self.definirTypeTour()
        # Prend une image de tour et la réduit de moitié. 
        # C'est cette image qui apparait à l'intérieur de l'icone.
        self.description = self.tour.description
        self.tour.largeur = self.tour.largeur / 2
        self.tour.hauteur = self.tour.hauteur / 2
        self.rect = Rect(self.posX, self.posY, self.largeur, self.hauteur)

    def definirTypeTour(self):
        if self.typeTour == "TourRoche":
            self.tour = Tour_Roche(self,self.posX,self.posY)
        elif self.typeTour == "TourFeu":
            self.tour = Tour_Feu(self,self.posX,self.posY)
        elif self.typeTour == "TourCanon":
            self.tour = Tour_Canon(self,self.posX,self.posY)
        elif self.typeTour == "TourGoo":
            self.tour = Tour_Goo(self,self.posX,self.posY)

class Projectile():
    def __init__(self, tour):
        self.prtTour = tour
        self.posX = self.prtTour.posX
        self.posY = self.prtTour.posY
        self.trajectoireX = 0
        self.trajectoireY = 0
        self.vitesse = 1
        self.couleur = "yellow"    
        self.puissance = self.prtTour.puissance
        self.pas = 3
        self.cible = self.prtTour.cible
        self.rayon = 5
        self.hitBox = Cercle(self.posX - self.rayon / 2, self.posY + self.rayon / 2, self.rayon) 

    def calculerDistanceCible(self):
        distance = helper.Helper.calcDistance(self.posX, self.posY, self.cible.positionX, self.cible.positionY)
        return distance

    def deplacerProjectile(self):
        self.posX += (self.pas * self.trajectoireX)
        self.posY += (self.pas * self.trajectoireY)

    # Trajectoire semi-lineaire
    def calculerTrajectoire(self):
        distance = self.calculerDistanceCible()
        if distance == 0:
            distance = 1
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

    def verifierAtteinteDesCibles(self, creep):
        if creep.hitBox.isInside(self.posX, self.posY):
            return True
        return False

    def bougerProjectile(self):
        self.deplacerProjectile()
        for creep in self.prtTour.prtNiveau.vague.listCreeps:
            if self.verifierAtteinteDesCibles(creep):
                if self.type != "pCirculaire":
                    self.prtTour.listProjectiles.remove(self)
                creep.effacerCreep(self)
        if (self.posX > self.prtTour.prtNiveau.prtPartie.prtJeu.largeur or self.posX < 0 or self.posY > self.prtTour.prtNiveau.prtPartie.prtJeu.hauteur or self.posY < 0):
            self.prtTour.listProjectiles.remove(self)

class Projectile_Roche(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.couleur = "dim grey"
        self.calculerTrajectoire()
        self.type = "pRoche"
    
class Projectile_Canon(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.couleur = "blue"
        self.type = "pCanon"

class Projectile_Goo(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.couleur="dark green"
        self.type = "pGoo"

class Projectile_Circulaire(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.type = "pCirculaire"
        self.departX = self.prtTour.posX
        self.departY = self.prtTour.posY
        self.rayon = self.prtTour.range
        self.etendueDommage = self.calculerEtendueDommage()
        self.x0 = self.departX
        self.x1=self.departX
        self.y0= self.departY
        self.y1=self.departY
        self.vitesseExplosion = 2
    
    def calculerEtendueDommage(self):
        xMax0 = self.departX - self.rayon
        yMax0 = self.departY - self.rayon
        xMax1 = self.departX + self.rayon
        yMax1 = self.departY + self.rayon
        coordOvale = [xMax0, yMax0, xMax1, yMax1]
        return coordOvale
    
    def deplacerProjectile(self):
        if self.x0 > self.etendueDommage[0]:
            self.x0 -= self.vitesseExplosion
        else:
            self.prtTour.listProjectiles.remove(self)
        if self.x1 < self.etendueDommage[2]:
            self.x1 += self.vitesseExplosion
        if self.y0 > self.etendueDommage[1]:
            self.y0 -= self.vitesseExplosion
        if self.y1 < self.etendueDommage[3]:
            self.y1 += self.vitesseExplosion

    def verifierAtteinteDesCibles(self, creep):
        if creep.positionX >= self.x0 and creep.positionX <= self.x1:
            if creep.positionY >= self.y0 and creep.positionY <= self.y1:
                return True
        return False

class Interface_jeu():
    def __init__(self):
        self.posX = 400
        self.posY = 525
        self.largeur = 400
        self.hauteur = 75
        self.couleur="gray21"

class Zone_description():
    def __init__(self):
        self.posX = 400
        self.posY = 525
        self.largeur = 175
        self.hauteur = 62
        self.couleur="gray21"

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

    def ifIntersectRect(self, rect):
        for i in range(rect.x, rect.x + rect.largeur):
            for j in range(rect.y, rect.y + rect.hauteur):
                if self.isInside(i, j):
                    return True
        return False

class Rect():
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def isInside(self, x,y):
        if x > (self.x - self.largeur) and x < (self.x + self.largeur):
            if y > (self.y -self.hauteur) and y < (self.y + self.hauteur):
                return True
        return False

if __name__ == '__main__':
    print ("Fin Modele")
