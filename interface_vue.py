
# -*- coding: iso-8859-1 -*-

from tkinter import *
from PIL import Image, ImageTk
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

        ###### PORTAIL #######
        indiceCheminSentier = len(sentier.chemin) - 1
        largeurPortail = 70
        hauteurPortail = 70
        #Calcul coordonnées portail
        pX1 = sentier.chemin[indiceCheminSentier][0] - (largeurPortail/2)
        pX2 = sentier.chemin[indiceCheminSentier][0] + (largeurPortail/2)
        pY1 = sentier.chemin[indiceCheminSentier][1] - (hauteurPortail/2)
        pY2 = sentier.chemin[indiceCheminSentier][1] + (hauteurPortail/2)
        #print(pX1)
        #input("test")
        self.canevasDessin.create_rectangle(pX1, pY1, pX2, pY2, fill="blue", tags=("portail"))

    def afficherCreeps(self, vague):
        for i in vague.listCreeps:
            imgCreep = Image.open(i.sprite)
            imgCreep = imgCreep.resize((int(i.largeur), int(i.hauteur)))
            imgCreep = ImageTk.PhotoImage(imgCreep)
            # l'allocation a un label empeche l'image d'etre effacer par le garbage collector
            label = Label()
            label.image = imgCreep 
            creep = self.canevasDessin.create_image((i.positionX, i.positionY), image=imgCreep, anchor=CENTER, tags=("creep"))
            self.creepsAEffacer.append(creep)

            #TODO: generaliser
#            if i.nom == "creepFacile":
#                creep = self.canevasDessin.create_oval(i.positionX, i.positionY, i.positionX+i.largeur, i.positionY+i.hauteur, fill = "pink", tags = ("creep"))
#            elif i.nom == "creepDifficile":
#                creep = self.canevasDessin.create_oval(i.positionX, i.positionY, i.positionX+i.largeur, i.positionY+i.hauteur, fill = "yellow", tags = ("creep"))
#            elif i.nom == "creepBoss":
#                creep = self.canevasDessin.create_oval(i.positionX, i.positionY, i.positionX+i.largeur, i.positionY+i.hauteur, fill = "red", tags = ("creep"))
#            self.creepsAEffacer.append(creep)

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
                if j.type == "pCirculaire":
                    projectile=self.canevasDessin.create_oval(j.x0, j.y0, j.x1, j.y1, fil="red", tags=("projectile"))
                else:
                    projectile=self.canevasDessin.create_rectangle(j.posX, j.posY, j.posX+5, j.posY+5, fill=j.couleur, tags=("projectile"))
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
        imgTour = Image.open(tour.sprite)
        imgTour = imgTour.resize((int(tour.largeur), int(tour.hauteur)))
        imgTour = ImageTk.PhotoImage(imgTour)
        # l'allocation a un label empeche l'image d'etre effacer par le garbage collector
        label = Label()
        label.image = imgTour
        self.canevasDessin.create_image(tour.posX, tour.posY, image=imgTour, anchor=CENTER)
#        self.canevasDessin.create_rectangle(tour.posX-tour.largeur,tour.posY-tour.hauteur,tour.posX+tour.largeur,
 #                                         tour.posY+tour.hauteur,fill=tour.couleur, tags=('IconeTour'))

    #Dessine toutes les tours d'un aire de jeu. Éventuellement ce sera selon le type choisi.
    def dessinerTour(self, tour):
        self.dessinerUneTour(tour)

    #TODO: Pour l'instant il n'y a qu'un seul type d'icone de tour. Éventuellement chaque type de tour aura sa fonction dessiner
    #TODO: Pour l'instant c'est un rectangle mais on pourra facilement importer des sprites
    def dessinerUneIconeTour(self,iconeTour):
        self.canevasDessin.create_rectangle(iconeTour.posX-iconeTour.largeur,iconeTour.posY-iconeTour.hauteur,
                                      iconeTour.posX+iconeTour.largeur, iconeTour.posY+iconeTour.hauteur,
                                      fill="grey")
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
        
    def detecterClickDroit(self):
        self.canevasDessin.bind("<Button-3>", self.prtControleur.event_click_droit)
        
    def annulerClicks(self): #En cas de gameOver si on annule pas le bind on peut continuer à construire
        self.canevasDessin.unbind("<Button-1>")
        self.canevasDessin.unbind("<Button-3>")

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

    def afficherPasDargent(self):
        texte="Fond insuffisant"
        self.canevasDessin.create_text(400, 525, justify="left", text=texte, font=("Courier 14 bold"), fill="red", tags = ('PasDargent'))
        self.root.after(1000, self.canevasDessin.delete,"PasDargent")

    def afficherDescriptionTour(self, tour):
        self.canevasDessin.create_text(400, 525, justify="left", text=tour.description, font=("Courier 9"), fill="white", tags = ('DescriptionTour'))
    
    def effacerDescriptionTour(self):
        self.canevasDessin.delete("DescriptionTour")
    
    def afficherConstructionAnnulee(self):
        texte="Construction annulée"
        self.effacerDescriptionTour()
        self.canevasDessin.create_text(400, 525, justify="left", text=texte, font=("Courier 14 bold"), fill="white", tags = ('ConstructionAnnulee'))
        self.root.after(1000, self.canevasDessin.delete,"ConstructionAnnulee")
    
    def reJouer(self):
        self.prtControleur.restart = 1
    
    def quitter(self):
        self.root.quit        

    def afficherMenuFinDePartie(self):
        texte = "Fin de partie"
        largeurMenu = 200
        hauteurMeu = 100
        coordX1 = (self.largeur - largeurMenu)/2
        coordY1 = (self.hauteur - hauteurMeu)/2
        coordX2 = coordX1 + largeurMenu
        coordY2 = coordY1 + hauteurMeu
        self.canevasDessin.create_rectangle(coordX1, coordY1, coordX2, coordY2, fill="red", tags = ('gameOver'))
        coordTextX = coordX1 + ((coordX2 - coordX1) /2)
        coordTextY = coordY1 + 20
        self.canevasDessin.create_text(coordTextX, coordTextY, justify="center", text=texte, font=("Helvetica"), fill="black", tags = ('gameOver'))
        coordBoutonX = coordX1 + 73
        self.boutonRejouer=Button(self.cadreDessin,text="Rejouer",bg="grey", command=self.reJouer)
        self.boutonRejouer.place(x=coordBoutonX, y=coordTextY +20)
        self.boutonQuitter=Button(self.cadreDessin,text="Quitter",bg="grey", command=self.quitter)
        self.boutonQuitter.place(x=coordBoutonX, y=coordTextY +50)

    def effacerNiveau(self):
        self.canevasDessin.pack_forget()
        self.boutonMenu.pack_forget()
        self.boutonQuitter.pack_forget()
        self.cadreMenu.pack_forget()
        self.cadreDessin.pack_forget()
