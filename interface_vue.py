# -*- coding: iso-8859-1 -*-

from tkinter import *
from test.test_importlib.namespace_pkgs.project1 import parent

class Vue():
    def __init__(self, controleur):
        self.prtControleur = controleur
        self.root = Tk()
        self.hauteur = 600
        self.largeur = 800

        self.creepsAEffacer = []
        self.projectilesAEffacer = []

    #TODO: Placer les elements dans __init__ (faire reference au meme canevas/cadre)
    def disposerEcran(self, sentier):
        self.cadreMenu = Frame(self.root, bg="grey",width=800, height=600)
        self.cadreMenu.pack()

        self.cadreDessin = Frame(self.root, bg="black", width=800, height=600)
        self.cadreDessin.pack()

        self.canevasDessin = Canvas(self.cadreDessin,width=self.largeur, height=self.hauteur, bg="green")
        self.canevasDessin.create_line(sentier.trace, width=sentier.largeur, fill=sentier.couleur)
        self.canevasDessin.pack()

        self.boutonMenu=Button(self.cadreMenu,text="menu",bg="grey")
        self.boutonMenu.pack(side=LEFT)

        self.boutonQuitter=Button(self.cadreMenu,text="Quitter",command=self.root.quit,bg="grey",fg="red")
        self.boutonQuitter.pack(side=RIGHT)

    def afficherCreeps(self, vague):
        for i in vague.listCreeps:
            creep=self.canevasDessin.create_oval(i.positionX, i.positionY, i.positionX+10, i.positionY+10, fill="yellow", tags=("creep"))
            self.creepsAEffacer.append(creep)

    def effacerAnimationPrecedente(self):
        for i in self.creepsAEffacer:
            self.canevasDessin.delete(i)
        self.creepsAEffacer.clear()
        for j in self.projectilesAEffacer:
            self.canevasDessin.delete(j)
        self.projectilesAEffacer.clear()

    def afficherProjectiles(self, jeu):
        for i in jeu.listProjectiles:
            projectile=self.canevasDessin.create_rectangle(i.posX, i.posY, i.posX+5, i.posY+5, fill="red", tags=("projectile"))
            self.projectilesAEffacer.append(projectile)

    #TODO: Pour l'instant c'est un rectangle mais on pourra facilement importer des sprites
    def dessinerUneAire(self, aire):
        self.canevasDessin.create_rectangle(aire.posX-aire.largeur,aire.posY-aire.hauteur,aire.posX+aire.largeur,
                                          aire.posY+aire.hauteur,fill=aire.couleur)

    #TODO: Logique?
    #Dessine toutes les aires de construction d'un aire de jeu.
    def dessinerAires(self, listAires):
        for i in listAires:
            self.dessinerUneAire(i)

    #TODO: Pour l'instant il n'y a qu'un seul type de tour. Éventuellement chaque type de tour aura sa fonction dessiner
    #TODO: Pour l'instan c'est un rectangle mais on pourra facilement importer des sprites
    def dessinerUneTour(self,tour):
        self.canevasDessin.create_rectangle(tour.posX-tour.largeur,tour.posY-tour.hauteur,tour.posX+tour.largeur,
                                          tour.posY+tour.hauteur,fill=tour.couleur)

    #Dessine toutes les tours d'un aire de jeu. Éventuellement ce sera selon le type choisi.
    def dessinerTour(self, tour):
        if (tour.type=="Tour"):
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
            if i.type=="Tour":
                self.dessinerUneIconeTour(i)

    # Détecte un événement "click bouton gauche de la souris"
    def detecterClick(self):
        self.canevasDessin.bind("<Button-1>", self.prtControleur.event_click)

if __name__ == '__main__':
    v=Vue(None)
#    v.detecterClick() TODO: Detecter un clique a l'interieur d'un triangle
    v.root.mainloop()
    print ("Fin Vue")
