from ivy.std_api import * #type: ignore
import math 
from bus_address import bus_address

Vector_X = 0
Vector_Y = 0
Wind_Comp = V_Wind = 0
Dec_Magnetique = 0
Fcu_Mode = ""
Fcu_Value = 0
fpa = psi = phi = 0
Max_Roll_Rate = Max_Roll = 0
x1=x2=y1=y2=0
Vp=100

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
    global phi
    Vector_X = float(larg[0])
    Vector_Y = float(larg[1])
    Vp = float(larg[3])
    fpa = float(larg[4])
    psi = float(larg[5])
    phi = float(larg[6])
    
def on_FCU_Mod(agent, *larg) :
    global Fcu_Mode
    global Fcu_Value
    Fcu_Mode = larg[0]
    Fcu_Value = float(larg[1])

def on_FGS_Msg(agent, *larg): 
    global x1,x2
    global y1,y2
    
    x1 = float(larg[0])
    x2 = float(larg[1])
    y1 = float(larg[2])
    y2 = float(larg[3])
    #lancement du code au message du FM
    if Fcu_Mode == "Managed" :
        Capture_AXE()
    elif  Fcu_Mode == "SelectedTrack" :
        Capture_ROUTE(Fcu_Value)
    elif Fcu_Mode == "SelectedHeading" :
        Capture_CAP(Fcu_Value)

def on_Perfo_Msg(agent, *larg) :
    global Max_Roll
    global Max_Roll_Rate
    Max_Roll = float(larg[9])
    Max_Roll_Rate = float(larg[10])

def on_WindComponent (agent, *larg):
    global V_Wind
    global Wind_Comp
    V_Wind = float(larg[0]) 
    Wind_Comp = float(larg[1]) 

def on_MagnticDeclination(agent, *larg) :
    global Dec_Magnetique
    Dec_Magnetique = float(larg[0])

def Capture_AXE():

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
    T_ey = 37 # 10*TauPsi

    xdot = Vp*math.cos(fpa) * math.cos(psi) + V_Wind * math.cos(Wind_Comp+math.pi)
    ydot = Vp*math.cos(fpa) * math.sin(psi) + V_Wind * math.sin(Wind_Comp+math.pi) 
    
    Gs = math.sqrt((math.pow(ydot,2)) + (math.pow(xdot,2))) #ground speed

    if y2-y1 != 0 and x2-x1 != 0:
        if y2-y1 <0 and x2-x1 < 0:
            khi_a = math.atan((y2-y1)/(x2-x1))+180*(math.pi/180) #route avion
        else : 
            khi_a = math.atan((y2-y1)/(x2-x1))
    if x2-x1 == 0:
        if y2-y1 > 0 :
            khi_a =  90 * (math.pi/180)
        elif y2-y1 < 0 :
            khi_a = 270 * (math.pi/180)
    if y2-y1 == 0 :
        if x2-x1 > 0 :
            khi_a = 0
        if x2-x1 < 0 :
            khi_a = 180 * (math.pi/180)
    ey= -math.sin(khi_a)*(Vector_X- x1) + math.cos(khi_a) * (Vector_Y- y1) #cross_track
    if ey/(Gs*T_ey) > 1 :
        khi_c = khi_a - math.asin(1)
    elif ey/(Gs*T_ey) < -1 :
        khi_c = khi_a - math.asin(-1)
    else :
        khi_c = khi_a - math.asin(ey/(Gs*T_ey))

    if khi_c*(180/math.pi) <0 :
        khi_c=khi_c+360*(math.pi/180)
    elif khi_c*(180/math.pi) > 360 :
        khi_c= khi_c - 360*(math.pi/180)
    Capture_ROUTE(khi_c)

def Capture_ROUTE(khi_c): 
    global V_Wind
    global Vp
    global fpa
    global Wind_Comp

    if Fcu_Mode == "Managed" :
        #calcul de la direction du vent à partir de sa provenance 
        if Wind_Comp > 180 :
            direction_vent_vrai = Wind_Comp - 180 * (math.pi/180)
        else:
            direction_vent_vrai = Wind_Comp + 180 * (math.pi/180) 
         #calcul de la dérive et du cap vrai
        d = math.asin((V_Wind*math.sin(khi_c - direction_vent_vrai))/Vp*math.cos(fpa))
    else : #Pour calcul en mode select
        khi_c = khi_c * (math.pi/180)
        #calcul de la direction du vent à partir de sa provenance 
        direction_vent_magnetique = Wind_Comp + 180* (math.pi/180) - Dec_Magnetique 
         #calcul de la dérive et du cap vrai
        d = math.asin((V_Wind * math.sin(khi_c - direction_vent_magnetique))/Vp * math.cos(fpa))
    cap = 0

    #Evite cap <0 et >360 
    if d > 0 :
        cap = khi_c + d
        if cap < 0 :
            cap +=360* (math.pi/180)
    elif d < 0 :
        cap = khi_c - d #cap en rad
        if cap > 360* (math.pi/180) :
            cap-=360* (math.pi/180) 
    elif d == 0 :
        cap = khi_c
    Capture_CAP(cap)
    
def Capture_CAP (target):

    global Vp
    global psi  #psi
    global phi  #phi
    global Fcu_Value

    global Max_Roll
    global Max_Roll_Rate 
    global Dec_Magnetique
    global Fcu_Mode

    TauPhi= 1.7
    TauPsi = 5.1 #3*TauPhi
    gravity = 9.81
    Delta_CAP = 0.0
    p=0


    if Fcu_Mode == "SelectedHeading" :
        target = target*(math.pi/180) - Dec_Magnetique
    elif Fcu_Mode == "SelectedTrack" :
        target = target - Dec_Magnetique
    
    
    Delta_CAP = (target-psi)
    while Delta_CAP > math.pi:
        Delta_CAP = Delta_CAP - 2*math.pi
    while Delta_CAP <= -math.pi:
        Delta_CAP = Delta_CAP + 2*math.pi

    #Capture de cap
    phic = Delta_CAP*(Vp/(gravity*TauPsi))

    if phic > Max_Roll:
        phic = Max_Roll
        
    if phic < -Max_Roll:
        phic = -Max_Roll

    p = (phic-phi)/TauPhi

    if (p>=Max_Roll_Rate):
        p =Max_Roll_Rate
    if (p<=(-Max_Roll_Rate)):
        p = -Max_Roll_Rate
    
    IvySendMsg("APLatControl rollRate={}".format(str(p)))
bus_address = "127.255.255:2010"
app_name = "PA_LAT"
ivy_bus = bus_address
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_FCU_Mod, r'^FCULateral Mode=(\S+) Val=(\S+)')
IvyBindMsg(on_StateVector, r'^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)')
IvyBindMsg(on_FGS_Msg, r'^FM_Active_leg x1=(\S+) x2=(\S+) y1=(\S+) y2=(\S+) h_contrainte=(\S+)')
IvyBindMsg(on_MagnticDeclination, r'^MagneticDeclination=(\S+)')
IvyBindMsg(on_WindComponent, r'^WindComponent VWind=(\S+) dirWind=(\S+)')
IvyBindMsg(on_Perfo_Msg, r'^Perfo ViManage=(\S+) ViMin=(\S+) ViMax=(\S+) nxMin=(\S+) nxMax=(\S+) nzMin=(\S+) nzMax=(\S+) fpaMin=(\S+) fpaMax=(\S+) roulisMax=(\S+) rollrateMax=(\S+)')

IvyMainLoop()