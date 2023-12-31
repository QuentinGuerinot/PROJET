from casadi import *
import numpy as np
import math
import time

import matplotlib.pyplot as plt
from pylab  import step, figure, show, spy


#Variables du problème
Xmax=50 #Capa batterie kWh
soc_init=0 #capa init %
soc_final=100 # capa finale %
ta=0 # temps d'arrivé h
td=19# temps final h
Pmax=140 #puissance max borne

kwh_init=Xmax*soc_init/100 
kwh_final=Xmax*soc_final/100

##paramètres (tiré d'un autre fichier, directement ici dans un premier temps):
Ck=np.array([0.045,0.042,0.035,0.035,0.035,0.041,0.045,0.05,0.052,0.052,0.06,0.1,0.06,0.095,0.1,0.098,0.095,0.05,0.06,0.095,0.05,0.05,0.048,0.045]) #vecteur de prix selon l'heure
Dt=(int(td*60)-int(ta*60)) #différence de temps (utile pour le pas d'opti)
Ck_temp = np.linspace(0,Dt,Dt+1)

for k in range(Dt+1):
    Ck_temp[k]=Ck[int((k+int(ta*60))/60)]

t = np.linspace(ta,td,Dt+1) #vecteur temps pour le plot

opti = Opti() # Optimization problem

#Variables :
P = opti.variable(1,Dt+1) 
X = opti.variable(1,Dt+1) 

#Formule a minimiser

J=0 
for k in range(Dt+1):
    J =  J + P[:,k] * Ck_temp[k]

J = Dt*J

opti.minimize(J)

for k in range(Dt):
    opti.subject_to(X[:,k+1]==X[:,k]+1/60*P[:,k]) 

# ---- states constraints -----------
opti.subject_to(opti.bounded(0,X[:,:],Xmax))
opti.subject_to(opti.bounded(0,P[:,:],Pmax))
opti.subject_to(opti.bounded(kwh_final,X[:,Dt],Xmax))


# ---- initial values for solver ---
opti.set_initial(X[:,0], kwh_init)
opti.set_initial(P[:,:], 0)

opti.subject_to(X[:,0]== kwh_init)
#opti.subject_to(P[:,0]== 0)

# ---- solve NLP ------
opti.solver("ipopt") # set numerical backend

tic = time.process_time()
sol = opti.solve()   # actual solve
toc = time.process_time()

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

figure()
plt.plot(t,Ck_temp)
plt.xlabel('Temps [heures]')
plt.ylabel('Prix (€)')
plt.title('Prix du kWh')
plt.grid()

plt.show()
