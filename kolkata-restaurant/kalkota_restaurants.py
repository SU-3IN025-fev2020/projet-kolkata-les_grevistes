# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys

import Astar
import heapq
import Strategies


    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 20 # default
    if len(sys.argv) == 2:         
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    #-------------------------------
    # Liste des stratégies dans Strategies.py
    #-------------------------------

    """
    - def strategie_aleatoire_uniforme(nbRestau)
    - def strategie_tetue(numPlayer, nbRestau)
    - def strategie_restau_dans_lordre(numRestau, nbRestau)
    - def strategie_le_plus_proche(posJoueur,goalStates,nbRestau)
    - def strategie_min_taux_rempli(tauxRemplissage, nbRestau)
    - def strategie_max_taux_rempli(tauxRemplissage, nbRestau)


    """

    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)

    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates and (x,y) not in goalStates]    
    #print ("allowed states:",len(allowedStates), allowedStates)

    #initialisation pour avoir le numéro des clients dans chaque restaurant
    clientsRestau = {r:[] for r in range(nbRestaus)}

    #taux remplissage de chaque restau
    tauxRestau = [0 for i in range(nbRestaus)]

    #gains des joueurs
    gainsJoueur = [0 for i in range(nbPlayers)]

    #nom de la stratégie utilisée par chaque joueur
    nomJoueurStrategie = []

    posPlayers = initStates
    restau=[0]*nbPlayers
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    #vitesse d'execution : voir frameskip de gameclass.py (ligne 66)

    for i in range(iterations):

        #--------------------------------------------------------------
        # Placement aleatoire des joueurs sur la carte, en évitant les obstacles
        #--------------------------------------------------------------
        #posPlayers = initStates
   
        for j in range(nbPlayers):
            x,y = random.choice(allowedStates)
            players[j].set_rowcol(x,y)
            game.mainiteration()
            posPlayers[j]=(x,y)

        #--------------------------------------------------------------
        # Chaque joueur choisit un restaurant
        #--------------------------------------------------------------
        nomJoueurStrategie = []
        #restau=[0]*nbPlayers
        for j in range(nbPlayers):
            s = ""
            if j == 0 :
                c = Strategies.strategie_aleatoire_uniforme(nbRestaus)
                s = "Strategie aleatoire uniforme"
            elif j == 1 :
                c = Strategies.strategie_aleatoire_uniforme(nbRestaus)
                s = "Strategie aleatoire uniforme"
            elif j == 2 :
                c = Strategies.strategie_tetue(j, nbRestaus)
                s = "Strategie tetue"
            elif j == 3 :
                c = Strategies.strategie_tetue(j, nbRestaus)
                s = "Strategie tetue"
            elif j == 4 :
                c = Strategies.strategie_restau_dans_lordre(restau[j], nbRestaus)
                s = "Strategie restau dans l'ordre"
            elif j == 5 :
                c = Strategies.strategie_restau_dans_lordre(restau[j], nbRestaus)
                s = "Strategie restau dans l'ordre"
            elif j == 6 :
                c = Strategies.strategie_le_plus_proche(posPlayers[j],goalStates,nbRestaus)
                s = "Strategie restau le plus proche"
            elif j == 7 :
                c = Strategies.strategie_le_plus_proche(posPlayers[j],goalStates,nbRestaus)
                s = "Strategie restau le plus proche"
            elif j == 8 :
                c = Strategies.strategie_min_taux_rempli(tauxRestau, nbRestaus)
                s = "Strategie restau le moins rempli"
            elif j == 9 :
                c = Strategies.strategie_min_taux_rempli(tauxRestau, nbRestaus)
                s = "Strategie restau le moins rempli"

            #print(c)
            nomJoueurStrategie.append(s)
            restau[j]=c
            clientsRestau[c].append(j)


        #--------------------------------------------------------------
        # Chaque joueur se rend au restaurant de son choix avec l'algorithme A*
        #--------------------------------------------------------------

        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            pos_restau = goalStates[restau[j]]
            chemin_le_plus_court = Astar.aStar(posPlayers[j], pos_restau, wallStates, 19)

            while posPlayers[j] != pos_restau:
                min_g, min_pos = heapq.heappop(chemin_le_plus_court)
                row, col = min_pos

                players[j].set_rowcol(row, col)
                print ("pos :", j, row, col)
                game.mainiteration()
    
                posPlayers[j]=(row,col)
            
                # si on est à l'emplacement d'un restaurant, on s'arrête
                if (row,col) == pos_restau:
                    #o = players[j].ramasse(game.layers)
                    game.mainiteration()
                    print ("Le joueur ", j, " est à son restaurant.")
                    # goalStates.remove((row,col)) # on enlève ce goalState de la liste            
                    break

        #--------------------------------------------------------------
        # Les joueurs obtiennent leur gain, et prennent connaissance des taux de remplissage de chaque restaurant
        #--------------------------------------------------------------

        #un joueur est choisi au hasard parmis ceux dans le restau si plusieurs joueurs se trouvent dans un même restaurant
        for r in range(nbRestaus):
            if len(clientsRestau[r]) == 1 :
                num_j = clientsRestau[r][0]
                gainsJoueur[num_j] += 1

            elif len(clientsRestau[r]) > 1 :
                num_j = random.choice(clientsRestau[r])
                gainsJoueur[num_j] += 1

        #taux de remplissage de chaque restaurant
            tauxRestau[r] = len(clientsRestau[r])/nbPlayers
            print("Taux remplissage Restau",r," :", tauxRestau[r])

        #réinitialisation des clients par restau à chaque itération
        clientsRestau = {r:[] for r in range(nbRestaus)}


    #affichage des gains
    for g in range(len(gainsJoueur)):
        print("Le joueur",g," a une moyenne de gains de :",gainsJoueur[g]/iterations)




    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


