# -*- coding: iso-8859-1 -*-

import interface_modele as im
import interface_vue as iv

class Controleur():
    def __init__(self):
        self.fntLargeur = 800
        self.fntHauteur = 600
        self.vue = iv.Vue(self, self.fntLargeur, self.fntHauteur)
        self.jeu = im.Jeu(self, self.fntLargeur, self.fntHauteur)
        self.vue.disposerEcran(self.jeu.partie.niveau.sentier)
        self.animer()
        self.dessinerAiresConstruction()
        self.dessinerInterfaceJeu()
        self.dessinerIconesTours()
        self.vue.detecterClick()
        self.vue.detecterClickDroit()
        self.gameOver=False

    def animer(self):
        gameOver=self.jeu.partie.verifierGameOver()
        if (gameOver == True):
            self.vue.afficherGameOver()
        self.vue.effacerAnimationPrecedente()
        self.jeu.faireAction()
        self.vue.afficherCreeps(self.jeu.partie.niveau.vague)
        self.vue.afficherProjectiles(self.jeu) #TODO: projectiles dans jeu
        self.vue.afficherStats(self.jeu.partie.argentJoueur, self.jeu.partie.ptsVieJoueur)
        self.vue.root.after(50, self.animer)

    def syncMoveCreep(self, creep):
        self.vue.root.after(creep.vitesse, self.jeu.bougerCreep, creep)
        
    def syncMoveProjectile(self, projectile):
        self.vue.root.after(projectile.vitesse, self.jeu.bougerProjectile, projectile)

    def syncCreerCreep(self):
        if self.jeu.partie.niveau.vague.nbCreepsActif < self.jeu.partie.niveau.vague.nbCreepsTotal:
            self.jeu.partie.niveau.vague.listCreeps.append(im.Creep(self.jeu.partie.niveau.vague))
            self.jeu.partie.niveau.vague.nbCreepsActif += 1
            #TODO: generaliser le delai de creation des creeps
            self.vue.root.after(1000, self.syncCreerCreep)

    def syncCreerProjectile(self, tour):
        tour.pretTir = False
        tour.listProjectiles.append(im.Projectile(tour))
        self.vue.root.after(tour.freqAttaque * 10, tour.attaquerCible)

    #Lorsque la vue détecte un "click gauche de la souris" elle appelle cette fonction afin que le contrôleur
    #transmette l'événement au modèle. position = position du curseur de la souris lors du click.
    def event_click(self,position):
        self.jeu.event_click(position);
    
    def event_click_droit(self,event): #event au lieu de position car la position n'est pas utilisée
        self.jeu.event_click_droit(event)

    #TODO: J'ai fait en sorte que dans modèle le jeu génère lui même ses parties qui elles génèrent automatiquement
    # ses niveaux. Il faudra discuter si on veut passer par le contrôleur pour ces éléments.
    def dessinerAiresConstruction(self):
        self.vue.dessinerAires(self.jeu.partie.niveau.listAires)

    #Appelée par le jeu lorsqu'une nouvelle tour est générée
    def nouvelleTour(self, tour):
        self.vue.dessinerTour(tour)

    def dessinerIconesTours(self):
        self.vue.dessinerIconesTours(self.jeu.partie.niveau.listIconesTours)
    
    def dessinerInterfaceJeu(self):
        self.vue.dessinerInterfaceJeu(self.jeu.partie.niveau.interfaceJeu,self.jeu.partie.niveau.zoneDescription)
        
    def afficherDescriptionTour(self,tour):
        self.vue.afficherDescriptionTour(tour)
    
    def effacerDescriptionTour(self):
        self.vue.effacerDescriptionTour()
    
    def manqueDargent(self):
        self.vue.afficherPasDargent()
    
    def constructionAnnulee(self):
        self.vue.afficherConstructionAnnulee()

if __name__ == '__main__':
    c=Controleur()
    c.vue.root.mainloop()
    print ("Fin interface")

