# -*- coding: iso-8859-1 -*-

import interface_modele as im
import interface_vue as iv

class Controleur():
    def __init__(self):
        self.jeu=im.Jeu(self)
        self.vue=iv.Vue(self)
        self.vue.disposerEcran(self.jeu.partie.niveau.sentier)
        self.animer()
#        self.dessinerAiresConstruction()
#        self.dessinerTours()
#        self.dessinerIconesTours()

    def animer(self):
        self.vue.effacerAnimationPrecedente()
        self.jeu.faireAction()
        self.vue.afficherCreeps(self.jeu.partie.niveau.vague)
        self.vue.afficherTour(self.jeu.partie.niveau.tour)
        self.vue.afficherProjectiles(self.jeu)
        self.vue.root.after(50,self.animer)

    #TODO: J'ai fait en sorte que dans modèle le jeu génère lui même ses parties qui elles génèrent automatiquement
    #ses niveaux. Il faudra discuter si on veut passer par le contrôleur pour ces éléments.

    def dessinerAiresConstruction(self):
        self.vue.dessinerAires(self.jeu.partie.niveau.listAires)

    def dessinerTours(self):
        self.vue.dessinerTours(self.jeu.partie.niveau.listTours)

    def dessinerIconesTours(self):
        self.vue.dessinerIconesTours(self.jeu.partie.niveau.listIconesTours)

if __name__ == '__main__':
    c=Controleur()
    c.vue.root.mainloop()
    print ("Fin interface")
