import math

def selected_mode(): #cap magnetique en entree
    cap_actuel_vrai=input('Cap actuel :') #cap actuel de l'avion (vrai)
    cap_adeg=float(cap_actuel_vrai)
    cap_a=cap_adeg*(math.pi/180)

    deviation= -13.69
    cap_actuel_magnetique= cap_a + deviation #calcul cap magnetique fct(cap actuel)
    if cap_actuel_magnetique<0: #evite d'avoir des cap negatifs
        cap_actuel_magnetique+=360
    
    cap_fcu_sm=input('Cap FCU :')  #objectif de cap a capturer (magnetique)
    cfcusm=float(cap_fcu_sm)

    cap_odeg=cfcusm-deviation #calcul cap vrai objectif fct(entree fcu)
    if cap_odeg<0: #evite d'avoir des cap negatifs
        cap_odeg+=360
    cap_o=cap_odeg*(math.pi/180)

    if cap_a<=cap_o and cap_o<=cap_a+(180*(math.pi/180)): #calcul sens virage
        print("vd")
    else:
        print("vg")

    
    
    """ #sens virage // variation du cap
    while deltaCapOut!=deltaCapIn: 
        while deltaCapOut> (math.pi):
            deltaCapOut=deltaCapIn-2*(math.pi)
            print(deltaCapOut)
            deltaCapIn=deltaCapOut #probleme quand deltaCapOut arrive < pi : retour vers deltaCapOut > pi -> boucle infini
        while deltaCapOut<= (math.pi):
            deltaCapOut+=2*(math.pi)
            print(deltaCapOut)
            deltaCapOut=deltaCapIn
    """
    
    """ #sens virage // variation du cap
    if deltaCapOut!=deltaCapIn: 
        if deltaCapOut> 180:
            print('vg')
            
        if deltaCapOut>= -180:
            print('vd')
    #sens_virage(deltaCapOut,deltaCapIn)
    """
    

     #test de cap
    print(cap_adeg)
    print(cap_a)
    print(cap_actuel_magnetique)
    print(cfcusm)
    print(cap_odeg)
    print(cap_o)
    

def managed_mode(): #cap vrai en entree
    return 1

"""def sens_virage(deltaCapOut, deltaCapIn):
    while deltaCapOut> (math.pi):
        deltaCapOut=deltaCapIn-2*(math.pi)
        print(deltaCapOut)
        
    while deltaCapOut>= -(math.pi):
        deltaCapOut+=2*(math.pi)
        print(deltaCapOut)
"""
selected_mode()