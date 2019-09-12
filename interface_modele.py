# -*- coding: iso-8859-1 -*-
import random


class Sentier():
    def __init__(self,parent):
        self.parent=parent
        self.coord1 = [0,200]
        self.coord2 = [200,200]
        self.coord3 = [200,400]
        self.coord4 = [350,400]
        self.coord5 = [350,150]
        self.coord6 = [500, 150]
        self.coord7 = [500, 500]
        self.coord8 = [700, 500]
        self.coord9 = [700, 0]
        self.largeur = 30
        
        self.trace = [self.coord1, self.coord2, self.coord3, self.coord4, self.coord5, self.coord6, 
                      self.coord7, self.coord8, self.coord9]

class Pion():
    def __init__(self, parent, x, y):
        self.parent=parent
        self.taille=random.randrange(5) + 3
        self.x=x
        self.y=y
        self.cible=[]
        self.vitesse = 3
        
    def deplacer(self): #on met cette methode ici pour etre proche de l'objet
        self.x+=self.taille/2
    
    def suivreSentier(self, sentier):
        if self.x <  sentier.coord2[0]:
            self.x += self.vitesse
        elif self.y < sentier.coord3[1] and self.x < sentier.coord5[0]:
            self.y += self.vitesse
        elif self.x < sentier.coord4[0]:
            self.x += self.vitesse
        elif self.y > sentier.coord5[1] and self.x > sentier.coord2[0] and self.x <= sentier.coord6[0]:
            self.y -= self.vitesse
        elif self.x < sentier.coord6[0]:
            self.x += self.vitesse
        elif self.y < sentier.coord7[1] and self.x > sentier.coord6[0] and self.x <= sentier.coord8[0]:
            self.y += self.vitesse
        elif self.x < sentier.coord8[0]:
            self.x += self.vitesse
        elif self.y > sentier.coord9[1] and self.x > sentier.coord8[0]:
            self.y -= self.vitesse
            

class Jeu():
    def __init__(self, parent, largeur=800,hauteur=600):
        self.parent=parent
        self.largeur=largeur
        self.hauteur=hauteur
        self.pions=[]
        self.creerSentier()
    
    def creationpions(self,n):
        for i in range(n):
            #x=random.randrange(self.largeur)
            #y=random.randrange(self.hauteur)
            x, y = self.sentier.coord1
            p=Pion(self,x,y)
            self.pions.append(p)
    
    def faireaction(self):
        for i in self.pions:
            #i.deplacer()
            i.suivreSentier(self.sentier)
    
    def creerSentier(self):
        self.sentier = Sentier(self)
           
