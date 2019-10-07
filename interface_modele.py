# -*- coding: iso-8859-1 -*-

import helper
import winsound #TODO: winsound

# Trello?
#TODO: Animation des sprites
#TODO: Ecran proportionnel (frame de construction?)
#TODO: --Indicateur du curseur(?)
#TODO: Le timer est a changer... un index du nombre de fois que la fonction a ete appeller serait mieux
#TODO: Projectiles Canon et Feu: Attaque plus d'une seule fois la meme cible (a chaque fois qu'on anime)
#TODO: Le niveau 2 va beaucoup plus vite que le niveau 1

class Jeu():
    def __init__(self, controleur, largeur=800, hauteur=600):
        self.prtControleur = controleur
        self.largeur = largeur # largeur de fenetre
        self.hauteur = hauteur
        self.typeAconstruire = "None" # Joueur - selection de tour 
        self.partie = Partie(self)

    # Recoit appel du controlleur a interval regulier
    def faireAction(self):
        if len(self.partie.niveau.vague.listCreeps)==0 and self.prtControleur.msTime == 1:
            self.partie.niveau.vague.genererCreep()
        elif self.prtControleur.msTime % 1000 == 0: #TODO: delai de creation
            self.partie.niveau.vague.genererCreep()
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
        #normalement les tableaux suivants seraient dans une base de donnée. Par manque de temps ils sont définis ici
        self.listCreepsN1 = ("facile","facile","facile","facile","facile","difficile","difficile","difficile","boss")
        self.listCreepsN2 = ("facile","facile","difficile","difficile","difficile","boss","boss","boss")
        self.listAiresN1 = ([100,150],[275,350],[425,100],[600,350],[275,200],[600,200],[425,275]) #positions des tours sur l'aire de jeu
        self.listAiresN2 = ([100,100],[250,100],[400,100],[550,100],[250,250],[400,250],[550,250],[75,350],[725,225])
        self.listIconesTours = ([40,490],[100,490],[40,560],[100,560]) #Positions des icones de construction de tour
        self.listTypeIcone = ("TourRoche","TourFeu","TourCanon","TourGoo")

        self.niveauCourant = 1
        self.compteurCreep = 0
        self.argentJoueur = 200 #valeur à déterminer
        self.ptsVieJoueur = 5
        self.score = 0
        self.niveau = Niveau(self)

    def verifierGameOver(self):
        if self.ptsVieJoueur <= 0:
            self.prtJeu.prtControleur.annulerClicks()
            return True
        return False

    def verifierFinNiveau(self):
        if self.niveauCourant==1 and not self.niveau.vague.listCreeps and self.compteurCreep==len(self.listCreepsN1):
            self.prtJeu.prtControleur.annulerClicks()
            return True
        elif self.niveauCourant==2 and not self.niveau.vague.listCreeps and self.compteurCreep==len(self.listCreepsN2):
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
        self.genererSentier() #TODO: Implementation de vagues

        self.vague = Vague(self)
        self.genererAiresConstruction()
        self.genererIconesTours()
        self.interfaceJeu = Interface_jeu()
        self.zoneDescription = Zone_description()
        
    def genererSentier(self):
        if(self.prtPartie.niveauCourant==1):
            self.sentier = SentierN1(self)
        elif(self.prtPartie.niveauCourant==2):
            self.sentier = SentierN2(self) 
        else:
            print("Fin de partie") 

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
        winsound.PlaySound(tour.sonConstruction, winsound.SND_FILENAME | winsound.SND_ASYNC) #TODO: winsound
        
    #Création des aires de construction selon le tableau défini dans la classe Partie
    def genererAiresConstruction(self):
        self.listAires=[]
        if self.prtPartie.niveauCourant == 1:
            listAiresNiv=self.prtPartie.listAiresN1
        elif self.prtPartie.niveauCourant == 2:
            listAiresNiv=self.prtPartie.listAiresN2
        
        for x,y in listAiresNiv:
            aire=AireDeConstruction(self,x,y)
            self.listAires.append(aire)                 

    #Création des icones de tour selon le tableau défini dans la classe Partie
    def genererIconesTours(self):
        index = 0
        for x,y in self.prtPartie.listIconesTours:
            iconeTour = IconeTour(self,x,y,self.prtPartie.listTypeIcone[index])
            self.listIconesTours.append(iconeTour)
            index = index + 1

    def attaquerCreeps(self, creep):
        for i in self.listTours:
            if i.cible is None:
                if i.siCreepDansRange(creep):
                    i.cible = creep

#TODO: passer un dictionaire de creeps?
class Vague():
    def __init__(self, niveau):
        self.prtNiveau = niveau
        self.listCreeps = []
        self.nbCreepsActif = 0
        self.vagueCree = False

    def genererCreep(self):
        if(self.prtNiveau.prtPartie.niveauCourant==1):
            if self.nbCreepsActif < len(self.prtNiveau.prtPartie.listCreepsN1):
                if(self.prtNiveau.prtPartie.listCreepsN1[self.nbCreepsActif]=="facile"):
                    creep=CreepFacile(self);
                elif(self.prtNiveau.prtPartie.listCreepsN1[self.nbCreepsActif]=="difficile"):
                    creep=CreepDifficile(self);
                elif(self.prtNiveau.prtPartie.listCreepsN1[self.nbCreepsActif]=="boss"):
                    creep=CreepBoss(self);
                self.listCreeps.append(creep)
                self.prtNiveau.prtPartie.compteurCreep=self.prtNiveau.prtPartie.compteurCreep+1
        elif(self.prtNiveau.prtPartie.niveauCourant==2):
            if self.nbCreepsActif < len(self.prtNiveau.prtPartie.listCreepsN2):
                if(self.prtNiveau.prtPartie.listCreepsN2[self.nbCreepsActif]=="facile"):
                    creep=CreepFacile(self);
                elif(self.prtNiveau.prtPartie.listCreepsN2[self.nbCreepsActif]=="difficile"):
                    creep=CreepDifficile(self);
                elif(self.prtNiveau.prtPartie.listCreepsN2[self.nbCreepsActif]=="boss"):
                    creep=CreepBoss(self);
                self.listCreeps.append(creep)
                self.prtNiveau.prtPartie.compteurCreep=self.prtNiveau.prtPartie.compteurCreep+1
        self.nbCreepsActif += 1 
        
class SentierN1():
    def __init__(self, niveau):  # parent = niveau
        self.prtNiveau = niveau
        self.largeur = 30
        self.couleur = "lightGoldenrod1"
        self.chemin = [[0,200],[200,200],[200,400],[350,400],[350,150],[500,150],[500,400],[700,400],[700,0]]
        self.axe = 'Y'

class SentierN2():
    def __init__(self, niveau):
        self.prtNiveau = niveau
        self.largeur = 60
        self.couleur = "lightGoldenrod2"
        self.chemin = [[0,150],[650,150],[650,300],[150,300],[150,400],[800,400]] 
        self.axe = 'X'

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
        self.ptsVieInit = self.ptsVie

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
        self.prtVague.prtNiveau.prtPartie.score += self.valeur
        winsound.PlaySound(self.son, winsound.SND_FILENAME | winsound.SND_ASYNC) #TODO: winsound

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
        self.ptsVieInit = self.ptsVie
        self.pas = 1 
        self.vitesse = 10
        self.valeur = 10 
        self.puissanceDommage = 1 
        
class CreepDifficile(Creep):
     def __init__(self,vague):
        Creep.__init__(self, vague)
        self.type = "creepDifficile"
        self.ptsVie = 10 
        self.ptsVieInit = self.ptsVie
        self.pas = 1 
        self.vitesse = 7
        self.valeur = 20 
        self.puissanceDommage = 2 

class CreepBoss(Creep):
    def __init__(self, vague):
        Creep.__init__(self, vague)
        self.type = "creepBoss"
        self.ptsVie = 50
        self.ptsVieInit = self.ptsVie
        self.pas = 1
        self.vitesse = 15
        self.valeur = 100
        self.puissanceDommage = 3
        self.largeur = 30 
        self.hauteur = 20

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
        self.freqAttaque = 200
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
        self.cout = 200
        self.description = "Une tour qui crache du feu \ndans un mouvement circulaire." \
                            + "\nDommage: " + str(self.puissance) + "\nFréquence: " + str(self.freqAttaque) + "\nCout: " + str(self.cout)
        self.son = "./assets/sounds/tour_feu.wav" 
        self.freqAttaque = 1000
        self.range = 150
        self.puissance = 1

    def creerProjectile(self):                
        self.listProjectiles.append(Projectile_Circulaire(self))
       
class Tour_Canon(Tour):
    def __init__(self, niveau,x,y):
        Tour.__init__(self, niveau,x,y)
        self.type = "TourCanon"
        self.couleur = "blue"
        self.cout = 200
        self.freqAttaque = 1000
        self.puissance = 1
        self.description = "Une tour qui lance des boulets de canon\npuissants mais lents." \
                            + "\nDommage: " + str(self.puissance) + "\nFréquence: " + str(self.freqAttaque) + "\nCout: " + str(self.cout)
        self.son = "./assets/sounds/tour_cannon.wav" 

    def creerProjectile(self):                
        self.listProjectiles.append(Projectile_Canon(self))

class Tour_Goo(Tour):
    def __init__(self, niveau,x,y):
        Tour.__init__(self, niveau,x,y)
        self.type="TourGoo"
        self.couleur="dark green"
        self.cout=80
        self.puissance = 0
        self.freqAttaque = 1500
        self.description = "Une tour qui lance des projectiles gluants\nqui ralentissent leurs cibles." \
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
        self.type = None

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
                if self.type != "pCirculaire" and self.type != "pCanon":
                    if self in self.prtTour.listProjectiles:
                        self.prtTour.listProjectiles.remove(self)
                creep.effacerCreep(self)
        if (self.posX > self.prtTour.prtNiveau.prtPartie.prtJeu.largeur or self.posX < 0 or self.posY > self.prtTour.prtNiveau.prtPartie.prtJeu.hauteur or self.posY < 0):
            self.prtTour.listProjectiles.remove(self)

class Projectile_Roche(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.couleur = "dim grey"
        self.type = "pRoche"
        self.calculerTrajectoire()
    
class Projectile_Canon(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.couleur = "black"
        self.type = "pCanon"
        self.rayon = 30
        self.pas = 1
        self.calculerTrajectoire()

class Projectile_Goo(Projectile):
    def __init__(self, tour):
        Projectile.__init__(self, tour)
        self.couleur="red"
        self.type = "pGoo"
        self.vitesse = 5
        self.calculerTrajectoire()

    def verifierAtteinteDesCibles(self, creep):
        if creep.hitBox.isInside(self.posX, self.posY):
            if creep.vitesse <= 30:
                creep.vitesse *= 2
            return True
        return False

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
        self.couleur="gray31"

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
