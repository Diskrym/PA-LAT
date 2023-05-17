def selected_mode(): #cap magnetique
    deviation= -13.69
    cap_fcu_sm=input('Cap FCU :')
    cfcusm=float(cap_fcu_sm)

    cap_vrai=cfcusm+deviation
    if cap_vrai<0:
        cap_vrai+=360
    
    print(cap_vrai)


def managed_mode(): #cap vrai en entree
    return 1


selected_mode()