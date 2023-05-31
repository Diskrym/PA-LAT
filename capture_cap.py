import math
from ivy.std_api import * #type: ignore

Vector_X=None
Vector_Y=None
Wind_Comp=None
V_Wind=None
Fcu_Mode=None
Fcu_Value=None
Heading=0.00
Dec_Magnetique=0.00

def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass

def get_AircraftSetPosition(agent, *larg):
    Heading=float(larg[0])
    print("Heading={}".format(larg[0]))
    return Heading

def get_MagneticDeclination(agent, *larg) :
    Dec_Magnetique = float(larg[0])
    print("DEC={}".format(larg[0]))
    return Dec_Magnetique

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
        print("vd")
    else:
        print("vg")

def managed_mode(): #cap vrai en entree
    return 1

def main():
    get_MagneticDeclination()
    get_AircraftSetPosition()
    selected_mode()

main()


app_name = "PA_LAT"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(get_AircraftSetPosition, r'^AircraftSetPosition Heading=(\S+)')
IvyBindMsg(get_MagneticDeclination, r'^MagneticDeclination=(\S+)')