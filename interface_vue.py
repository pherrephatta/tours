# -*- coding: iso-8859-1 -*-

from tkinter import *  # seule exception pour cette librairie on importe l'entierete
import random
import interface_modele as im


class Vue():
    def __init__(self, parent):
        self.parent=parent
        self.root=Tk()  #fenetre principale de l'environnement graphique, objet de type top level
        self.largeur=800
        self.hauteur=600
        self.elementAEffacer = []
    # quelques widgets
    
    def disposerEcran(self, sentier):
        self.cadremenu=Frame(self.root, bg="red", width=600, height=200)
        self.cadredessin=Frame(self.root, bg="blue",width=600, height=200) #On doit maintenant les disposer (demander au gestionnaire)
        
        
        self.monetiquette=Label(self.cadremenu, text="Hello world")  #1er argument en tkinter est parent dans la hierarchie
        self.monetiquette.pack(side=LEFT)
        #self.monetiquette.pack_forget() # enleve mais existe tjrs en memoire, le gestionnaire ne le considere plus
        self.monentree=Entry(self.cadremenu) #champ de texte
        self.monentree.insert(0, "Ecrivez ici")
        self.monentree.pack(side=LEFT)
        
        self.monaction=Button(self.cadremenu, text="clic moi", command=self.reagit) #reagit pas de parentheses
        self.monaction.pack(side=LEFT)
        
        self.canevas=Canvas(self.cadredessin,width=self.largeur, height=self.hauteur, bg="green")
        
        # test sentier
        self.canevas.create_line(sentier.trace, width=sentier.largeur);
        
        self.canevas.pack()
        
        self.cadremenu.pack()
        self.cadredessin.pack()
    
    def reagit(self): 
        self.parent.creerpion()
    
    # copie de ma fonction originale
    def reagit1(self): #La fonction est un objet Python. Retourne none par defaut, on ne veut pas son resultat mais son execution
        x=random.randrange(self.largeur)
        y=random.randrange(self.hauteur)
        taille=5
        self.canevas.create_rectangle(x-taille, y-taille,
                                      x+taille, y+taille,
                                      fill="yellow")  #donne un point, et un autre point, et trace rectangle entre les 2
        #donnee=self.monentree.get()
        #print(donnee)
        print(x,y)
        
    def afficherpions(self,pions):  #efface tout ce que le canevas contenait
       # self.effacerpions(self.elementAEffacer)
        for i in pions:
            p=self.canevas.create_rectangle(i.x-i.taille, i.y-i.taille,
                                      i.x+i.taille, i.y+i.taille,
                                      fill="yellow")
            self.elementAEffacer.append(p)
    
    def effacerpions(self, elementAEffacer):
        for i in self.elementAEffacer:
            self.canevas.delete(i)
            
if __name__ == '__main__':
    v=Vue(None)
    v.root.mainloop()
    print("DANS VUE")