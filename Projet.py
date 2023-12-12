from casadi import *
import numpy as np
import math
import time

import matplotlib.pyplot as plt
from   matplotlib.figure import Figure
from   matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

##Classe des résultats d'optimisation
class Results():
    def __init__(soc,ta,td):
        self.soc_init = soc_init
        self.soc_final = soc_final
        self.ta = ta
        self.td = td
        


#temporaire
kwh=50
soc_init=50
soc_final=100
kwh_init=kwh*soc_init/100
kwh_final=kwh*soc_final/100
Xmax=kwh
ta=0
td=24

##paramètres (tiré d'un autre fichier, directement ici dans un premier temps):
Ck_temp=np.array([100,1,1,1,1,100,1,1,1,1,1,1,1,100,1,1,1,1,1,1,1,1,1,1]) #prix 
Pmax=140 #puissance max borne
N=24 #intervalle de temps heures
#beta=N/(ta-td)
Dt=(td-ta)

opti = Opti() # Optimization problem

#Variables :
P = opti.variable(1,Dt) 
X = opti.variable(1,Dt) 
Ck = opti.parameter(1,N)

opti.set_value(Ck,Ck_temp)

#Formule a minimiser
J=0 
for k in range(Dt):
    J =  J + P[:,k] * Ck[k+ta] 
J = Dt*J
opti.minimize(J)

for k in range(Dt-1):
    opti.subject_to(X[:,k+1]==X[:,k]+P[:,k]) # close the gaps    

# ---- states constraints -----------
opti.subject_to(opti.bounded(0,X[:,:],Xmax))
opti.subject_to(opti.bounded(0,P[:,:],Pmax))
opti.subject_to(opti.bounded(kwh_final,X[:,Dt-1],Xmax))

opti.subject_to(X[:,0]== kwh_init)
#opti.subject_to(P[:,0]== 0)

    # ---- initial values for solver ---
#opti.set_initial(X[:,0], kwh_init)
#opti.set_initial(P[:,:], 0)


# ---- solve NLP              ------
opti.solver("ipopt") # set numerical backend

tic = time.process_time()
sol = opti.solve()   # actual solve
toc = time.process_time()

print(sol.value(Ck))
print(sol.value(P))
print(sol.value(J))
print(sol.value(X))

#Figure()
#plt.plot(N,P)
#plt.xlabel('Temps [min]')
#plt.ylabel('P')
#plt.title('Puissance vs time')
#plt.grid()

#Figure()
#plt.plot(N,X)
#plt.xlabel('Temps [min]')
#plt.ylabel('X')
#plt.title('Soc vs time')
#plt.grid()


# put optimization results in a class
#res = Results(sol.value(P)
#              )
    
