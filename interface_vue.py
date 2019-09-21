
# -*- coding: iso-8859-1 -*-

from tkinter import *
from test.test_importlib.namespace_pkgs.project1 import parent

class Vue():
    def __init__(self, controleur, largeur, hauteur):
        self.prtControleur = controleur
        self.root = Tk()
        self.largeur = largeur
        self.hauteur = hauteur
        self.creepsAEffacer = []
        self.projectilesAEffacer = []

    #TODO: Placer les elements dans __init__ (faire reference au meme canevas/cadre)
    def disposerEcran(self, sentier):
        self.cadreMenu = Frame(self.root, bg="grey",width=self.largeur, height=self.hauteur)
        self.cadreMenu.pack()

        self.cadreDessin = Frame(self.root, bg="black", width=self.largeur, height=self.hauteur)
        self.cadreDessin.pack()

        self.canevasDessin = Canvas(self.cadreDessin,width=self.largeur, height=self.hauteur, bg="green")
        self.canevasDessin.create_line(sentier.chemin, width=sentier.largeur, fill=sentier.couleur)
        self.canevasDessin.pack()

        self.boutonMenu=Button(self.cadreMenu,text="menu",bg="grey")
        self.boutonMenu.pack(side=LEFT)

        self.boutonQuitter=Button(self.cadreMenu,text="Quitter",command=self.root.quit,bg="grey",fg="red")
        self.boutonQuitter.pack(side=RIGHT)

    def afficherCreeps(self, vague):
        for i in vague.listCreeps:
            #TODO: generaliser
            creep = self.canevasDessin.create_oval(i.positionX, i.positionY, i.positionX+i.largeur, i.positionY+i.hauteur, fill = "yellow", tags = ("creep"))
            self.creepsAEffacer.append(creep)

    def effacerAnimationPrecedente(self):
        for i in self.creepsAEffacer:
            self.canevasDessin.delete(i)
        self.creepsAEffacer.clear()
        for j in self.projectilesAEffacer:
            self.canevasDessin.delete(j)
        self.projectilesAEffacer.clear()
        self.canevasDessin.delete("argent", "ptsVie")

    def afficherProjectiles(self, jeu):
        for i in jeu.partie.niveau.listTours:
            for j in i.listProjectiles:
                projectile=self.canevasDessin.create_rectangle(j.posX, j.posY, j.posX+5, j.posY+5, fill="red", tags=("projectile"))
                self.projectilesAEffacer.append(projectile)

    #TODO: Pour l'instant c'est un rectangle mais on pourra facilement importer des sprites
    def dessinerUneAire(self, aire):
        self.canevasDessin.create_rectangle(aire.posX-aire.largeur,aire.posY-aire.hauteur,aire.posX+aire.largeur,
                                          aire.posY+aire.hauteur,fill=aire.couleur)

    #Dessine toutes les aires de construction d'un aire de jeu.
    def dessinerAires(self, listAires):
        for i in listAires:
            self.dessinerUneAire(i)

    #TODO: Pour l'instant il n'y a qu'un seul type de tour. Éventuellement chaque type de tour aura sa fonction dessiner
    #TODO: Pour l'instan c'est un rectangle mais on pourra facilement importer des sprites
    def dessinerUneTour(self,tour):
        self.canevasDessin.create_rectangle(tour.posX-tour.largeur,tour.posY-tour.hauteur,tour.posX+tour.largeur,
                                          tour.posY+tour.hauteur,fill=tour.couleur, tags=('IconeTour'))

    #Dessine toutes les tours d'un aire de jeu. Éventuellement ce sera selon le type choisi.
    def dessinerTour(self, tour):
        self.dessinerUneTour(tour)

    #TODO: Pour l'instant il n'y a qu'un seul type d'icone de tour. Éventuellement chaque type de tour aura sa fonction dessiner
    #TODO: Pour l'instant c'est un rectangle mais on pourra facilement importer des sprites
    def dessinerUneIconeTour(self,iconeTour):
        self.canevasDessin.create_rectangle(iconeTour.posX-iconeTour.largeur,iconeTour.posY-iconeTour.hauteur,
                                      iconeTour.posX+iconeTour.largeur, iconeTour.posY+iconeTour.hauteur,
                                      fill=iconeTour.couleur)
        self.dessinerUneTour(iconeTour.tour)

    #Dessine toutes les icones de tour d'un aire de jeu. Éventuellement ce sera selon le type choisi.
    def dessinerIconesTours(self, listIconesTours):
        for i in listIconesTours:
            self.dessinerUneIconeTour(i)
   
    def dessinerInterfaceJeu(self,interfaceJeu,zoneDescription):
        self.canevasDessin.create_rectangle(interfaceJeu.posX-interfaceJeu.largeur,interfaceJeu.posY-interfaceJeu.hauteur,interfaceJeu.posX+interfaceJeu.largeur,
                                          interfaceJeu.posY+interfaceJeu.hauteur,fill=interfaceJeu.couleur)
        self.canevasDessin.create_rectangle(zoneDescription.posX-zoneDescription.largeur,zoneDescription.posY-zoneDescription.hauteur,zoneDescription.posX+zoneDescription.largeur,
                                          zoneDescription.posY+zoneDescription.hauteur,fill=zoneDescription.couleur)

    # Détecte un événement "click bouton gauche de la souris"
    def detecterClick(self):
        self.canevasDessin.bind("<Button-1>", self.prtControleur.event_click)

    def afficherStats(self, argent, ptsVie):
        self.afficherArgent(argent)
        self.afficherPtsVie(ptsVie)
        
    def afficherArgent(self, argent):
        money = str(argent)
        texte="Argent: " + money
        texte += " $"
        self.canevasDessin.create_text(700, 475, justify="right", text=texte, font="Helvetica", fill="white", tags = ('argent'))
    
    def afficherPtsVie(self, ptsVie):
        vie = str(ptsVie)
        texte = "Il vous reste " + vie
        texte += " vies"
        self.canevasDessin.create_text(700, 500, justify="right", text=texte, font="Helvetica", fill="white", tags = ('ptsVie'))
        
    def afficherGameOver(self):
        texte = "GAME OVER"
        self.canevasDessin.create_text(400, 525, justify="center", text=texte, font=("Helvetica"), fill="red", tags = ('game over'))
    
    def afficherDescriptionTour(self, tour):
        self.canevasDessin.create_text(400, 525, justify="left", text=tour.description, font=("Courier 9"), fill="white", tags = ('DescriptionTour'))
    
    def effacerDescriptionTour(self):
        self.canevasDessin.delete("DescriptionTour")

if __name__ == '__main__':
    v=Vue(None, 800, 600)
    v.root.mainloop()
    print ("Fin Vue")
