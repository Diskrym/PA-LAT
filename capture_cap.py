import math
from ivy.std_api import * #type: ignore

Vector_X=0
Vector_Y=0
Wind_Comp=0
V_Wind=0
Fcu_Mode=0
Fcu_Value=0
Heading=0
Dec_Magnetique=0

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


def selected_mode(): #cap magnetique en entree
    global Heading
    global Dec_Magnetique

    cap_a=Heading*(math.pi/180) #cap en rad

    cap_actuel_magnetique= cap_a + Dec_Magnetique #calcul cap magnetique fct(cap actuel)
    if cap_actuel_magnetique<0: #evite d'avoir des cap negatifs
        cap_actuel_magnetique+=360

    cap_odeg=Heading-Dec_Magnetique #calcul cap vrai objectif fct(entree fcu)
    if cap_odeg<0: #evite d'avoir des cap negatifs
        cap_odeg+=360
    cap_o=cap_odeg*(math.pi/180)

    if cap_a<=cap_o and cap_o<=cap_a+(180*(math.pi/180)): #calcul sens virage
        print("vd") #établir les taux de roulis
    else:
        print("vg")

def managed_mode(): #cap vrai en entree
    pass

def main():
    """if selected_mod
        selected_mode()
    else 
        managed_mode()"""

main()


app_name = "PA_LAT"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_AircraftSetPosition, r'^AircraftSetPosition Heading=(\S+)')
IvyBindMsg(on_MagneticDeclination, r'^MagneticDeclination=(\S+)')