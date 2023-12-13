from casadi import *
import numpy as np
import math
import time

import matplotlib.pyplot as plt
from pylab  import step, figure, show, spy

##Classe des résultats d'optimisation
class Results():
    def __init__(soc,ta,td):
        self.soc_init = soc_init
        self.soc_final = soc_final
        self.ta = ta
        self.td = td
        self.capa = Xmax

#temporaire (plus tard sera recupéré)
Xmax=50 #Capa batterrie
soc_init=0 #% capa init
soc_final=100 #% capa finale
ta=0 # temps d'arrivé h
td=10# temps final h

kwh_init=Xmax*soc_init/100 
kwh_final=Xmax*soc_final/100

##paramètres (tiré d'un autre fichier, directement ici dans un premier temps):
Ck=np.array([100,1,1,1,1,100,1,1,1,1,1,1,1,100,1,1,1,1,1000,1,1,1,1,1]) #vecteur de prix selon l'heure
Pmax=140 #puissance max borne
Dt=(td-ta) #différence de temps (utile pour le pas d'opti)

t = np.linspace(ta,td,Dt+1) #vecteur temps pour le plot

opti = Opti() # Optimization problem

#Variables :
P = opti.variable(1,Dt+1) 
X = opti.variable(1,Dt+1) 

#Formule a minimiser

J=0 
for k in range(Dt+1):
    J =  J + P[:,k] * Ck[k+ta] 
J = Dt*J

opti.minimize(J)

for k in range(Dt):
    opti.subject_to(X[:,k+1]==X[:,k]+P[:,k]) # close the gaps    

# ---- states constraints -----------
opti.subject_to(opti.bounded(0,X[:,:],Xmax))
opti.subject_to(opti.bounded(0,P[:,:],Pmax))
opti.subject_to(opti.bounded(kwh_final,X[:,Dt],Xmax))



    # ---- initial values for solver ---
#opti.set_initial(X[:,0], kwh_init)
opti.set_initial(P[:,:], 0)

opti.subject_to(X[:,0]== kwh_init)
#opti.subject_to(P[:,0]== 0)

# ---- solve NLP              ------
opti.solver("ipopt") # set numerical backend

tic = time.process_time()
sol = opti.solve()   # actual solve
toc = time.process_time()

print(sol.value(P))
print(sol.value(X))


figure()
plt.plot(t,sol.value(P))
plt.xlabel('Temps [heures]')
plt.ylabel('P (kW)')
plt.title('Puissance vs time')
plt.grid()

figure()
plt.plot(t,sol.value(X))
plt.xlabel('Temps [heures]')
plt.ylabel('X (kWh)')
plt.title('Soc vs time')
plt.grid()

plt.show()

# put optimization results in a class
#res = Results(sol.value(P)
#              )
    
