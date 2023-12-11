from casadi import *
import numpy as np
import math
import time

##Classe des résultats d'optimisation
class Results():
    def __init__(soc,ta,tb):
        self.soc_init = soc_init
        self.soc_final = soc_final
        self.ta = ta
        self.td = tb 
        
def run_opti(config):

    ##paramètres (tiré d'un autre fichier, directement ici dans un premier temps):

    Ck=1 #prix 
    Pmax=140 #puissance max borne
    N=100 #intervalle de temps 



    opti = Opti() # Optimization problem


    #Variables :
    P = opti.variable(1,N) 
    X = opti.variable(1,N) 

    #Formule a minimiser 
    for k in range(N):
        J = Ck[:,k]*P[:,k]
    J = (ta-tb)*J
    opti.minimize(J)

    for k in range(N):
        opti.subject_to(X[:,k+1]==X[:,k]+(ta-tb)*P[:,k]) # close the gaps    

    # ---- states constraints -----------
    opti.subject_to(opti.bounded(0,Xk,Xmax))
    opti.subject_to(opti.bounded(0,Pi,Pmax))
    opti.subject_to(opti.bounded(soc_final,Xdj,Xmax))

        # ---- initial values for solver ---
    opti.set_initial(X, soc_init)
    
    
    # ---- solve NLP              ------
    opti.solver("ipopt") # set numerical backend

    tic = time.process_time()
    sol = opti.solve()   # actual solve
    toc = time.process_time()

        # put optimization results in a class
    res = Results(sol.value(soc)
                  )
    
