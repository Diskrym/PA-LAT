#C:/msys64/mingw64/bin/python.exe c:/Users/louis/OneDrive/Bureau/PA-LAT/PA-LAT-RECEPTEUR.py


from ivy.std_api import * #type: ignore
from cmath import asin, sin, cos
import math 

Vector_X = 0
Vector_Y = 0
Wind_Comp = 0
V_Wind = 0
Dec_Magnetique = 0
Fcu_Mode = 0
Fcu_Value = 0
Vp = 0
fpa = 0
psi=0
route=0
x1=0
x2=0
y1=0
y2=0

#init
def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass

def on_StateVector(agent, *larg):
    global Vector_X
    global Vector_Y
    global Vp
    global fpa
    global psi
    print("x={}, y={}".format(larg[0],larg[1]))
    Vector_X = float(larg[0])
    Vector_Y = float(larg[1])
    Vp = float(larg[3])
    fpa = float(larg[4])
    psi = float(larg[5])

def on_WindComponent (agent, *larg):
    global V_Wind
    global Dir_Wind
    print("x={}, y={}".format(larg[0],larg[1]))
    V_Wind = larg[0]
    Dir_Wind = larg[1]

def on_MagnticDeclination(agent, *larg) :
    global Dec_Magnetique
    Dec_Magnetique = larg[0]
    print("DEC={}".format(larg[0]))

def capture_daxe():

    global Vp
    global fpa
    global psi
    global V_Wind
    global Wind_Comp
    global x1
    global y1
    global x2
    global y2

    # calcul vecteur vitesse
    T_ey = 1

    xdot = Vp*cos(fpa) * cos(psi) + cos(V_Wind) * cos(Wind_Comp+math.pi)
    ydot = Vp*cos(fpa) * sin(psi) + sin(V_Wind) * sin(Wind_Comp+math.pi) 

    
    Gs = math.sqrt((math.pow(ydot.real,2)) + (math.pow(xdot.real,2))) #ground speed

    khi_a = math.atan((x2-x1)/(y2-y1)) #route avion

    ey= -sin(khi_a)*(Vector_X- x1) + cos(khi_a) * (Vector_Y- y1) #cross_track

    khi_c = khi_a - math.asin(ey.real/(Gs*T_ey))

    return khi_c.real

def calcul_route_sélecté(): 
    
    global Dec_Magnetique
    global V_Wind
    global Vp
    global fpa
    global Wind_Comp
    global Fcu_Value

# conversion de la diretion du vent vrai en magnétique
    direction_vent_magnetique = Wind_Comp + 180* (math.pi/180) - Dec_Magnetique 

#calcul de la dérive et du cap magnétique

    d = asin((V_Wind*sin(Fcu_Value* (math.pi/180) - direction_vent_magnetique))/Vp*cos(fpa))
    d=d.real
    cap_magnetique = 0
    if d > 0 :
        cap_magnetique = Fcu_Value* (math.pi/180) - d
        if cap_magnetique < 0 :
            cap_magnetique +=360* (math.pi/180)
    elif d < 0 :
        cap_magnetique = Fcu_Value*(math.pi/180) + d #cap en rad
        if cap_magnetique > 360* (math.pi/180) :
            cap_magnetique-=360* (math.pi/180) 
    elif d == 0 :
        cap_magnetique=Fcu_Value* (math.pi/180)
    return cap_magnetique

def calcul_route_managé(): 
    global V_Wind
    global Vp
    global fpa
    global Wind_Comp

#calcul de la direction du vent à partir de sa provenance 
    direction_vent_vrai = Wind_Comp + 180* (math.pi/180)

 #calcul de la dérive et du cap vrai 
    d=asin((V_Wind*sin(capture_daxe()- direction_vent_vrai))/Vp*cos(fpa))
    d=d.real
    cap_vrai = 0
    if d > 0 :
        cap_vrai = capture_daxe() - d
        if cap_vrai < 0 :
            cap_vrai +=360* (math.pi/180)
    elif d < 0 :
        cap_vrai = capture_daxe() + d #cap en rad
        if cap_vrai > 360* (math.pi/180) :
            cap_vrai-=360* (math.pi/180) 
    elif d == 0 :
        cap_vrai=capture_daxe()
        print(cap_vrai)
    return cap_vrai


def on_FCU_Mod(agent, *larg) :
    global Fcu_Mode
    global Fcu_Value
    Fcu_Mode = larg[0]
    Fcu_Value = float(larg[1])
    print("Mode={}, Value={}".format(larg[0],larg[1]))


def on_FGS_Msg(agent, *larg):
    print('a')
    global x1,x2
    global y1,y2

    x1 = float(larg[0])
    x2 = float(larg[1])
    y1 = float(larg[2])
    y2 = float(larg[3])

    #lancement du code au message du FM
    if Fcu_Mode == "Managed" :
        capture_daxe()
    elif  Fcu_Mode == "SelectedHeading" :
        calcul_route_sélecté()
     



app_name = "PA_LAT"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_StateVector, r'^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+)')
IvyBindMsg(on_FGS_Msg, r'^FM_Active_leg x1=(\S+), x2=(\S+), y1=(\S+), y2=(\S+)')
IvyBindMsg(on_MagnticDeclination, r'^MagneticDeclination=(\S+)')
IvyBindMsg(on_WindComponent, r'^WindComponent VWind=(\S+) dirWind=(\S+)')
IvyBindMsg(on_FCU_Mod, r'^FCULateral Mode=(\S+) Val=(\S+)')

IvyMainLoop()