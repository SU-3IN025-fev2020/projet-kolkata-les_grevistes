import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod
import functools
import time

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2) 


@functools.total_ordering # to provide comparison of nodes
class Noeud:
    def __init__(self, position, g, pere=None):
        self.pos = position
        self.g = g
        self.pere = pere
        
    def expand(self,taille, walls):
        nouveaux_fils = []
        x, y = self.pos
        
        if y+1<=taille and (x,y+1) not in walls:
            nouveaux_fils.append(Noeud((x, y+1), self.g+1, self))
        if x-1>=0 and (x-1,y) not in walls:
            nouveaux_fils.append(Noeud((x-1, y), self.g+1, self))
        if y-1>=0 and (x,y-1) not in walls:
            nouveaux_fils.append(Noeud((x, y-1), self.g+1, self))
        if x+1<=taille and (x+1,y) not in walls:
            nouveaux_fils.append(Noeud((x+1, y), self.g+1, self))

        return nouveaux_fils
    
    def h_value(self, position, but):
        return distManhattan(position, but)

    def f_value(self, position, but):
        return self.g+self.h_value(position, but)

    def chemin(self, chemin):
        if self.pere == None:
            return chemin
        else:
            chemin.append(self)
            return self.pere.chemin(chemin)


    def __str__(self):
        return str(self.pos)
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __lt__(self, other):
        return str(self) < str(other)
            
    def trace(self,p):
        """ affiche tous les ancetres du noeud
            """
        n = self
        c=0    
        while n!=None :
            print (n)
            n = n.pere
            c+=1
        print ("Nombre d'étapes de la solution:", c-1)
        return            


def aStar(initState,goalState,wallStates,taille):
    row,col = initState

    nodeInit = Noeud((row,col),0,None)
    frontiere = [(nodeInit.f_value((row,col),goalState),nodeInit)] 

    reserve = {}        
    bestNoeud = nodeInit
    chemin = []
    
    while frontiere != [] and bestNoeud.pos != goalState:    
        
        (min_f,bestNoeud) = heapq.heappop(frontiere)

        if bestNoeud.pos not in reserve:
            reserve[bestNoeud.pos] = bestNoeud.g 
            nouveauxNoeuds = bestNoeud.expand(taille, wallStates)
            for n in nouveauxNoeuds:
                f = n.f_value(n.pos, goalState)
                heapq.heappush(frontiere, (f,n))

        if bestNoeud.pos==goalState:
            #print("CHEMIN TROUVE")
            ch = bestNoeud.chemin([])
            for c in ch :
                heapq.heappush(chemin, (c.g, c.pos))

        if(frontiere == []):
            print("ERREUR : FRONTIERE VIDE")

    return chemin