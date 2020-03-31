import numpy as np
import random
import heapq
import Astar

def strategie_aleatoire_uniforme(nbRestau):
	return random.randint(0,nbRestau-1)

def strategie_tetue(numPlayer, nbRestau):
	return numPlayer%nbRestau

def strategie_restau_dans_lordre(numRestau, nbRestau):
	if numRestau > -2 :
		return (numRestau+1)%nbRestau
	else:
		print("ERREUR : INITIALISER numRestau > -2 SVP")

def strategie_le_plus_proche(posJoueur,goalStates,nbRestau):
	restau_tries = []
	for r in range(nbRestau):
		d = Astar.distManhattan(posJoueur,goalStates[r])
		heapq.heappush(restau_tries, (d, r))

	d_min, restau = heapq.heappop(restau_tries)
	return restau

def strategie_min_taux_rempli(tauxRemplissage, nbRestau):
	ind_min = 0
	for r in range(1,nbRestau):
		if tauxRemplissage[ind_min] > tauxRemplissage[r]:
			ind_min = r
	return r

def strategie_max_taux_rempli(tauxRemplissage, nbRestau):
	ind_min = 0
	for r in range(1,nbRestau):
		if tauxRemplissage[ind_min] < tauxRemplissage[r]:
			ind_min = r
	return r
