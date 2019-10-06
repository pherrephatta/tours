# -*- coding: iso-8859-1 -*-

from tkinter import *

class Vue():
    def __init__(self, controleur, largeur, hauteur):
        self.prtControleur = controleur
        self.root = Tk()
        self.largeur = largeur
        self.hauteur = hauteur
        self.creepsAEffacer = []
        self.projectilesAEffacer = []
        
        self.choixMenuFinal="none"
        self.restart=False
        self.quit=False
        self.niveauSuivant=False
        self.menuInterAffiche=False
        self.menuGameOverAffiche=False
        self.rejouer=False

        self.imgCreep1 = PhotoImage(file="./assets/sprites/creep1.gif")
        self.imgCreep2 = PhotoImage(file="./assets/sprites/creep2.gif")
        self.imgCreep3 = PhotoImage(file="./assets/sprites/creep3.gif")

        self.imgTourRoche = PhotoImage(file="./assets/sprites/tour_roche.gif")
        self.imgTourFeu = PhotoImage(file="./assets/sprites/tour_feu.gif")
        self.imgTourGoo = PhotoImage(file="./assets/sprites/tour_goo.gif")
        self.imgTourCanon = PhotoImage(file="./assets/sprites/tour_canon.gif")

        self.icoTourRoche = PhotoImage(file="./assets/sprites/ico_tour_roche.gif")
        self.icoTourFeu = PhotoImage(file="./assets/sprites/ico_tour_feu.gif")
        self.icoTourGoo = PhotoImage(file="./assets/sprites/ico_tour_goo.gif")
        self.icoTourCanon = PhotoImage(file="./assets/sprites/ico_tour_canon.gif")

        self.imgPortail = PhotoImage(file="./assets/sprites/portail_citrouille.gif")
        self.imgBackground = PhotoImage(file="./assets/sprites/bg_grass.gif")
        self.imageMenuInter=PhotoImage(file="./assets/sprites/InterNiveauBknd.gif")
        self.imageMenuGameOver=PhotoImage(file="./assets/sprites/chenille.gif")
        self.imageMenuEnd=PhotoImage(file="./assets/sprites/pumpkinEnd.gif")

    #TODO: Placer les elements dans __init__ (faire reference au meme canevas/cadre)
    def disposerEcran(self, sentier):
        self.cadreMenu = Frame(self.root, bg="grey",width=self.largeur, height=self.hauteur)
        self.cadreMenu.pack()

        self.cadreDessin = Frame(self.root, bg="black", width=self.largeur, height=self.hauteur)
        self.cadreDessin.pack()

        self.canevasDessin = Canvas(self.cadreDessin,width=self.largeur, height=self.hauteur, bg="green")
        self.canevasDessin.create_image((0,0), image=self.imgBackground, anchor=NW)
        self.canevasDessin.create_line(sentier.chemin, width=sentier.largeur, fill=sentier.couleur)
        self.canevasDessin.pack()

        self.boutonMenu=Button(self.cadreMenu,text="menu",bg="grey")
        self.boutonMenu.pack(side=LEFT)

        self.boutonQuitter=Button(self.cadreMenu,text="Quitter",command=self.root.quit,bg="grey",fg="red")
        self.boutonQuitter.pack(side=RIGHT)

        # Portail
        indiceCheminSentier = len(sentier.chemin) - 1
        largeurPortail = 75
        hauteurPortail = 75
        pX1 = sentier.chemin[indiceCheminSentier][0]
        pY1 = sentier.chemin[indiceCheminSentier][1]
        #Calcul coordonnées portail
        if sentier.axe == 'Y':
            pY1 += hauteurPortail/3
        else:
            pX1 -= largeurPortail/3
        self.canevasDessin.create_image((pX1, pY1), image=self.imgPortail, anchor=CENTER, tags=("portail"))

    def afficherCreeps(self, vague):
        for c in vague.listCreeps:
            if c.type == "creepFacile":
                imgCreep = self.imgCreep1
            elif c.type == "creepDifficile":
                imgCreep = self.imgCreep2
            elif c.type == "creepBoss":
                imgCreep = self.imgCreep3
            else:
                imgCreep = self.imgCreep1

            creep = self.canevasDessin.create_image((c.positionX, c.positionY), image=imgCreep, anchor=CENTER, tags=("creep"))
            self.creepsAEffacer.append(creep)
            self.afficherDommageCreep(c)

    def afficherDommageCreep(self, creep):
        couleur = None
        if creep.ptsVie > (creep.ptsVieInit / 2):
            couleur = "green"
        elif creep.ptsVie <= (creep.ptsVieInit / 2) and creep.ptsVie > 1:
            couleur = "yellow"
        else:
            couleur = "red"
        dommage=self.canevasDessin.create_rectangle(creep.positionX - creep.largeur/2, creep.positionY-10, creep.positionX + creep.largeur, creep.positionY-15, fill=couleur, tags=("dommage"))

    def effacerAnimationPrecedente(self):
        for i in self.creepsAEffacer:
            self.canevasDessin.delete(i)
        self.creepsAEffacer.clear()
        for j in self.projectilesAEffacer:
            self.canevasDessin.delete(j)
        self.projectilesAEffacer.clear()
        self.canevasDessin.delete("argent", "ptsVie", "score", "dommage")

    def afficherProjectiles(self, jeu):
        for i in jeu.partie.niveau.listTours:
            for j in i.listProjectiles:
                if j.type == "pCirculaire":
                    projectile=self.canevasDessin.create_oval(j.x0, j.y0, j.x1, j.y1, fil="red", stipple="gray25", tags=("projectile"))
                else:
                    projectile=self.canevasDessin.create_rectangle(j.posX, j.posY, j.posX+5, j.posY+5, fill=j.couleur, tags=("projectile"))
                self.projectilesAEffacer.append(projectile)

    def dessinerUneAire(self, aire):
        self.canevasDessin.create_rectangle(aire.posX-aire.largeur,aire.posY-aire.hauteur,aire.posX+aire.largeur,
                                          aire.posY+aire.hauteur,fill=aire.couleur)

    #Dessine toutes les aires de construction d'un aire de jeu.
    def dessinerAires(self, listAires):
        for i in listAires:
            self.dessinerUneAire(i)

    def dessinerUneTour(self, tour):
        if tour.type == "TourFeu":
            imgTour = self.imgTourFeu
        elif tour.type == "TourRoche":
            imgTour = self.imgTourRoche
        elif tour.type == "TourGoo":
            imgTour = self.imgTourGoo
        elif tour.type == "TourCanon":
            imgTour = self.imgTourCanon
        else:
            imgTour = self.imgTourRoche

        self.canevasDessin.create_image(tour.posX, tour.posY, image=imgTour, anchor=CENTER)

    #Dessine toutes les tours d'un aire de jeu. Éventuellement ce sera selon le type choisi.
    def dessinerTour(self, tour):
        self.dessinerUneTour(tour)

    def dessinerUneIconeTour(self,iconeTour):
        self.canevasDessin.create_rectangle(iconeTour.posX-iconeTour.largeur,iconeTour.posY-iconeTour.hauteur,
                                      iconeTour.posX+iconeTour.largeur, iconeTour.posY+iconeTour.hauteur,
                                      fill="grey")

        if iconeTour.tour.type == "TourFeu":
            imgTour = self.icoTourFeu
        elif iconeTour.tour.type == "TourRoche":
            imgTour = self.icoTourRoche
        elif iconeTour.tour.type == "TourGoo":
            imgTour = self.icoTourGoo
        elif iconeTour.tour.type == "TourCanon":
            imgTour = self.icoTourCanon
        else:
            imgTour = self.icoTourRoche

        self.canevasDessin.create_image(iconeTour.posX, iconeTour.posY, image=imgTour, anchor=CENTER)

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

    def afficherStats(self, argent, ptsVie, score):
        self.afficherArgent(argent, 700, 475)
        self.afficherPtsVie(ptsVie, 700, 500)
        self.afficherScore(score, 700, 525)
        
    def afficherArgent(self, argent, x, y):
        money = str(argent)
        texte="Argent: " + money
        texte += " $"
        self.canevasDessin.create_text(x, y, justify="right", text=texte, font="Helvetica", fill="white", tags = ('argent'))
    
    def afficherPtsVie(self, ptsVie, x, y):
        vie = str(ptsVie)
        texte = "Il vous reste " + vie
        texte += " vies"
        self.canevasDessin.create_text(x, y, justify="right", text=texte, font="Helvetica", fill="white", tags = ('ptsVie'))
       
    def afficherScore(self, score, x, y):
        s = str(score)
        texte = "Score : " + s
        self.canevasDessin.create_text(x, y, justify="right", text=texte, font="Helvetica", fill="white", tags = ('score'))

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


    def effacerNiveau(self):
        self.canevasDessin.pack_forget()
        self.boutonMenu.pack_forget()
        self.boutonQuitter.pack_forget()
        self.cadreMenu.pack_forget()
        self.cadreDessin.pack_forget()
        
    def afficherMenuInterNiveau(self):
        boutonSuivantX=400
        boutonSuivantY=530
        boutonSuivantLarg=60
        boutonSuivantHaut=30
        boutonSuivantTexte="Niveau\nSuivant"
        boutonSuivantCouleur="dark green"

        cadreScoreX=400
        cadreScoreY=320
        cadreScoreLarg=75
        cadreScoreHaut=50
        cadreScoreCouleur="dark green"

        self.cadreMenu = Frame(self.root, bg="grey",width=self.largeur, height=self.hauteur)
        self.cadreMenu.pack()

        self.cadreDessin = Frame(self.root, bg="black", width=self.largeur, height=self.hauteur)
        self.cadreDessin.pack()

        self.canevasDessin = Canvas(self.cadreDessin,width=self.largeur, height=self.hauteur, bg="green")
        self.canevasDessin.create_image((0,0),image=self.imageMenuInter, anchor=NW)
        self.canevasDessin.pack()

        self.boutonMenu=Button(self.cadreMenu,text="niveau suivant",bg="grey")
        self.boutonMenu.pack(side=LEFT)

        self.boutonQuitter=Button(self.cadreMenu,text="Quitter",command=self.root.quit,bg="grey",fg="red")
        self.boutonQuitter.pack(side=RIGHT)
        
        self.canevasDessin.create_rectangle(cadreScoreX-cadreScoreLarg,cadreScoreY-cadreScoreHaut,cadreScoreX+cadreScoreLarg,
                                  cadreScoreY+cadreScoreHaut,fill=cadreScoreCouleur, tags=('cadreScore'))
        
        self.canevasDessin.create_rectangle(boutonSuivantX-boutonSuivantLarg,boutonSuivantY-boutonSuivantHaut,boutonSuivantX+boutonSuivantLarg,
                                          boutonSuivantY+boutonSuivantHaut,fill=boutonSuivantCouleur, tags=('BoutonSuivant'))
        
        self.canevasDessin.create_text(boutonSuivantX, boutonSuivantY, justify="center", text=boutonSuivantTexte, font=("Courier 12 bold"), fill="black", tags = ('TextSuivant'))
        
        self.canevasDessin.tag_bind("BoutonSuivant", "<Button-1>", self.passerNiveauSuivant)
        self.canevasDessin.tag_bind("TextSuivant", "<Button-1>", self.passerNiveauSuivant)


    def passerNiveauSuivant(self,a):
        print("dans icone")
        self.niveauSuivant=True 
        
        
    def afficherMenuGameOver(self):
        boutonQuitterX=400
        boutonQuitterY=530
        boutonQuitterLarg=60
        boutonQuitterHaut=30
        boutonQuitterTexte="Quitter"
        boutonQuitterCouleur="dark green"
        texteGameOver="Game Over!"
        texteGameOverX=400
        texteGameOverY=100
        textGameOverFont="Comic Sans MS"
        self.cadreMenu = Frame(self.root, bg="grey",width=self.largeur, height=self.hauteur)
        self.cadreMenu.pack()

        self.cadreDessin = Frame(self.root, bg="black", width=self.largeur, height=self.hauteur)
        self.cadreDessin.pack()

        self.canevasDessin = Canvas(self.cadreDessin,width=self.largeur, height=self.hauteur, bg="green")
        self.canevasDessin.create_image((0,0),image=self.imageMenuGameOver, anchor=NW)
        self.canevasDessin.pack()

        self.boutonMenu=Button(self.cadreMenu,text="niveau suivant",bg="grey")
        self.boutonMenu.pack(side=LEFT)

        self.boutonQuitter=Button(self.cadreMenu,text="Quitter",command=self.root.quit,bg="grey",fg="red")
        self.boutonQuitter.pack(side=RIGHT)
        
        
        self.canevasDessin.create_rectangle(boutonQuitterX-boutonQuitterLarg,boutonQuitterY-boutonQuitterHaut,boutonQuitterX+boutonQuitterLarg,
                                          boutonQuitterY+boutonQuitterHaut,fill=boutonQuitterCouleur, tags=('BoutonQuitter'))
        
        self.canevasDessin.create_text(boutonQuitterX, boutonQuitterY, justify="center", text=boutonQuitterTexte, font=("Courier 12 bold"), fill="black", tags = ('TextQuitter'))
        
        self.canevasDessin.create_text(texteGameOverX, texteGameOverY, justify="center", text=texteGameOver, font=("Comic Sans MS", 50, "bold"), fill="red4", tags = ('TextGameOver'))

        
        self.canevasDessin.tag_bind("BoutonQuitter", "<Button-1>", self.quitter)
        self.canevasDessin.tag_bind("TextQuitter", "<Button-1>", self.quitter)
        
    def afficherMenuEnd(self):
        boutonQuitterX=400
        boutonQuitterY=530
        boutonQuitterLarg=60
        boutonQuitterHaut=30
        boutonQuitterTexte="Quitter"
        boutonQuitterCouleur="Orange"
        texteEnd="Victoire!"
        texteEnd2="Vous aurez vos citrouilles pour l'halloween."
        
        
        texteEndX=400
        texteEndY=50
        texteEnd2X=400
        texteEnd2Y=100
        textEndFont="Comic Sans MS"
        self.cadreMenu = Frame(self.root, bg="grey",width=self.largeur, height=self.hauteur)
        self.cadreMenu.pack()

        self.cadreDessin = Frame(self.root, bg="black", width=self.largeur, height=self.hauteur)
        self.cadreDessin.pack()

        self.canevasDessin = Canvas(self.cadreDessin,width=self.largeur, height=self.hauteur, bg="green")
        self.canevasDessin.create_image((0,0),image=self.imageMenuEnd, anchor=NW)
        self.canevasDessin.pack()

        self.boutonMenu=Button(self.cadreMenu,text="niveau suivant",bg="grey")
        self.boutonMenu.pack(side=LEFT)

        self.boutonQuitter=Button(self.cadreMenu,text="Quitter",command=self.root.quit,bg="grey",fg="red")
        self.boutonQuitter.pack(side=RIGHT)
        
        
        self.canevasDessin.create_rectangle(boutonQuitterX-boutonQuitterLarg,boutonQuitterY-boutonQuitterHaut,boutonQuitterX+boutonQuitterLarg,
                                          boutonQuitterY+boutonQuitterHaut,fill=boutonQuitterCouleur, tags=('BoutonQuitter'))
        
        self.canevasDessin.create_text(boutonQuitterX, boutonQuitterY, justify="center", text=boutonQuitterTexte, font=("Courier 12 bold"), fill="black", tags = ('TextQuitter'))
        
        self.canevasDessin.create_text(texteEndX, texteEndY, justify="center", text=texteEnd, font=("Comic Sans MS", 50, "bold"), fill="red3", tags = ('TextEnd'))
        self.canevasDessin.create_text(texteEnd2X, texteEnd2Y, justify="center", text=texteEnd2, font=("Comic Sans MS", 20, "bold"), fill="red3", tags = ('TextEnd2'))

        
        self.canevasDessin.tag_bind("BoutonQuitter", "<Button-1>", self.quitter)
        self.canevasDessin.tag_bind("TextQuitter", "<Button-1>", self.quitter)




    def quitter(self,a):
        print("dans icone")
        sys.exit()



        



        
        

