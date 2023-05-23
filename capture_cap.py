def selected_mode(): #cap magnetique en entree
    cap_actuel_vrai=input('') #cap actuel de l'avion (vrai)
    cav=float(cap_actuel_vrai)

    deviation= -13.69
    cap_actuel_magnetique= cav + deviation #calcul cap magnetique fct(cap actuel)
    if cap_actuel_magnetique<0: #evite d'avoir des cap negatifs
        cap_actuel_magnetique+=360
    
    cap_fcu_sm=input('Cap FCU :')  #objectif de cap a capturer (magnetique)
    cfcusm=float(cap_fcu_sm)

    cap_vrai=cfcusm-deviation #calcul cap vrai objectif fct(entree fcu)
    if cap_vrai<0: #evite d'avoir des cap negatifs
        cap_vrai+=360

    """
    print(cav)
    print(cap_actuel_magnetique)
    print(cfcusm)
    print(cap_vrai)
    """

def managed_mode(): #cap vrai en entree
    return 1


selected_mode()