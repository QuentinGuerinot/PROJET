from casadi import *
import numpy as np
import math
import time

##Classe des résultats d'optimisation
class Results():
    def __init__(soc,ta,tb):
        self.soc = soc
        self.ta = ta
        self.td= tb
        
def run_opti(config):

    ##paramètres (tiré d'un autre fichier, directement ici dans un premier temps):


    opti = Opti() # Optimization problem


    #Variables :
    P = opti.variable(1,N) 
    X = opti.variable(1,N) 

    #Formule a minimiser 
    J = Ck
    opti.minimize(J)

    # ---- states constraints -----------
    opti.subject_to(opti.bounded(soc_final,soc,xmax))

        # ---- initial values for solver ---
    opti.set_initial(tf, 20*60)
    
    # ---- solve NLP              ------
    opti.solver("ipopt") # set numerical backend

    tic = time.process_time()
    sol = opti.solve()   # actual solve
    toc = time.process_time()

        # put optimization results in a class
    res = Results(sol.value(soc)
                  )
    