# -*- coding: iso-8859-1 -*-
import interface_modele as im #alias !
import interface_vue as iv #alias !


class Controleur():
    def __init__(self):
        self.jeu=im.Jeu(self)
        self.vue=iv.Vue(self)
        self.jeu.creationpions(1)
        self.vue.disposerEcran(self.jeu.sentier)
        self.animer()
    
    def animer(self):
        self.vue.effacerpions(self.vue.elementAEffacer)
        self.jeu.faireaction()
        self.vue.afficherpions(self.jeu.pions)
        self.vue.root.after(50,self.animer) #2 parametres : combien de temps en ms + rappel sans () car je ne veux pas l'exécuter tout de suite

    def creerpion(self):
        self.jeu.creationpions(1)

if __name__ == '__main__':
    c=Controleur()
    c.vue.root.mainloop()  #boucle de l'engin de jeu
    # tout ce qui vient apres le mainloop sera execute a la fermeture de la fenetre
    print("FIN INTERFACE")
