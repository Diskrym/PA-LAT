import math
from ivy.std_api import * #type: ignore

Vector_X=0
Vector_Y=0
Wind_Comp=0
V_Wind=0
Fcu_Mode=0
Fcu_Value=0  #Cap_magnetique objectif [deg]
Heading=0   #Cap_magnetique actuel de l'avion [rad]
Dec_Magnetique=0 #declinaison magentique [rad]

def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass

def on_AircraftSetPosition(agent, *larg):
    Heading=float(larg[0])
    print("Heading={}".format(larg[0]))
    return Heading

def on_MagneticDeclination(agent, *larg) :
    Dec_Magnetique = float(larg[0])
    print("DEC={}".format(larg[0]))
    return Dec_Magnetique

def on_FCU_Mod(agent, *larg) :
    global Fcu_Mode
    global Fcu_Value
    Fcu_Mode = larg[0]
    Fcu_Value = larg[1]
    print("Mode={}, Value={}".format(larg[0],larg[1]))


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

    if Heading_v<=Fcu_Value_v and Fcu_Value_v<=Heading_v+180*(math.pi/180):
        print("vd")
    else:
        print("vg")

    """BOUCLE INSTRUCTION MISE EN VIRAGE"""

    if Heading_v<Fcu_Value_v<Heading_v+180*(math.pi/180):
        d_objectif_v=Fcu_Value_v-Heading_v
    else:
        if 0<=Heading_v<Fcu_Value_v:
            d_objectif_v=Heading_v+(360*(math.pi/180))-Fcu_Value_v
        else:
            d_objectif_v=Heading_v-Fcu_Value_v
    print("delta objectif:{}".format(d_objectif_v*(180/math.pi))) #print test de controle angle a parcourir

    if Heading_v<=Fcu_Value_v and Fcu_Value_v<=Heading_v+180*(math.pi/180):
        print("vd")
    else:
        print("vg")

    pass

def managed_mode(): #cap vrai en entree
    pass

def main():
    selected_mode()
    pass

# main()

app_name = "PA_LAT"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_AircraftSetPosition, r'^AircraftSetPosition Heading=(\S+)')
IvyBindMsg(on_MagneticDeclination, r'^MagneticDeclination=(\S+)')