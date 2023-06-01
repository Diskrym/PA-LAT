import math

Heading=0*(math.pi/180) #Cap_magnetique actuel de l'avion [rad]
Dec_Magnetique=0 #declinaison magentique [rad]
Fcu_Value=175 #Cap_magnetique objectif [deg]

def selected_mode(): #mode selecte, on entre un cap au fcu
    global Heading
    global Dec_Magnetique
    global Fcu_Value

    Fcu_Value*=(math.pi/180) #conversion en [rad] du cap objectif
    """PASSAGE DE CAP MAGNETIQUE A CAP VRAI"""

    Heading_v=Heading+Dec_Magnetique #Cap_vrai actuel [rad]
    Fcu_Value_v=Fcu_Value+Dec_Magnetique #Cap_vrai objectif [rad]

    if Heading_v<0: #evite cap negatifs
        Heading_v+=360*(math.pi/180)
    if Fcu_Value_v<0: #evite cap negatifs
        Fcu_Value_v+=360*(math.pi/180)
    
    """CALCUL DU SENS DU VIRAGE"""

    #d_objectif_v=Fcu_Value_v-Heading_v #Valeur de l'angle à parcourir

    """if d_objectif_v>180*(math.pi/180):
        d_objectif_v=360*(math.pi/180)-d_objectif_v"""
    
    if Heading_v<Fcu_Value_v<Heading_v+180*(math.pi/180):
        d_objectif_v=Fcu_Value_v-Heading_v
    else:
        if 0<=Heading_v<Fcu_Value_v:
            d_objectif_v=Heading_v+(360*(math.pi/180))-Fcu_Value_v
        else:
            d_objectif_v=Heading_v-Fcu_Value_v
    
    
    print("delta objectif:{}".format(d_objectif_v*(180/math.pi)))

    if Heading_v<=Fcu_Value_v and Fcu_Value_v<=Heading_v+180*(math.pi/180):
        print("vd")
    else:
        print("vg")

selected_mode()