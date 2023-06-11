#C:/msys64/mingw64/bin/python.exe c:/Users/louis/OneDrive/Bureau/PA-LAT/PA-LAT-RECEPTEUR.py


from ivy.std_api import * #type: ignore
import math 

Vector_X = 0
Vector_Y = 0
Wind_Comp = 0
V_Wind = 0
Dec_Magnetique = 0
Fcu_Mode = ""
Fcu_Value = 0
Vp = 0
fpa = 0
psi=0
phi = 0
route=0
Max_Roll = 0
Max_Roll_Rate = 0



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

    #############Pour Test################
    if Fcu_Mode == "Managed" :
        Capture_AXE()
    elif  Fcu_Mode == "SelectedTrack" :
        Capture_ROUTE(Fcu_Value)
    elif Fcu_Mode == "SelectedHeading" :
        #Capture_Cap(Fcu_Value)
        Capture_CAP(Fcu_Value)
    #############Pour Test################


def on_WindComponent (agent, *larg):
    global V_Wind
    global Dir_Wind
    V_Wind = float(larg[0])
    Dir_Wind = float(larg[1])

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

    Gs = math.sqrt((math.pow(ydot.real,2)) + (math.pow(xdot.real,2))) #ground speed

    if y2-y1 != 0 and x2-x1 != 0:
        if y2-y1 <0 and x2-x1 < 0:
            khi_a = math.atan((x2-x1)/(y2-y1))+180*(math.pi/180) #route avion si 2 négatifs
        else :                                                   #Evite les / par 0 et séléctionne le sens du leg
            khi_a = math.atan((x2-x1)/(y2-y1))

    if y2-y1 == 0:

        if x2-x1 > 0 :
            khi_a =  45*(180/math.pi)
        elif x2-x1 < 0 :
            khi_a = 270*(180/math.pi)
    if x2-x1 == 0 :
        if y2-y1 > 0 :
            khi_a = 0
        if y2-y1 < 0 :
            khi_a = 180*(180/math.pi)
 

    ey= -math.sin(khi_a)*(Vector_X- x1) + math.cos(khi_a) * (Vector_Y- y1) #cross_track
    
    if ey.real/(Gs*T_ey) > 1 :                                             #Angle nord géo et le leg
        khi_c = khi_a - math.asin(1)                                       #Route consigne (Khi_c)
    elif ey.real/(Gs*T_ey) < -1 :
        khi_c = khi_a - math.asin(-1)
    else :
        khi_c = khi_a - math.asin(ey/(Gs*T_ey))


    if khi_c*(180/math.pi) <0 :                                            # Evite les cap <0 ou >360
        khi_c=khi_c+360*(math.pi/180)
    elif khi_c*(180/math.pi) > 360 :
        khi_c= khi_c - 360*(math.pi/180)

    print('Envoie route (fct axe) :', khi_c*(180/math.pi))
    Capture_CAP(Capture_ROUTE(khi_c))

def Capture_ROUTE(khi_c): 
    global V_Wind
    global Vp
    global fpa
    global Wind_Comp

    if Fcu_Mode == "Managed" :
        #calcul de la direction du vent à partir de sa provenance 
        direction_vent_vrai = Wind_Comp + 180* (math.pi/180)
         #calcul de la dérive et du cap vrai
        d=math.asin((V_Wind*math.sin(khi_c- direction_vent_vrai))/Vp*math.cos(fpa))
    else : #Pour calcul en mode select
        khi_c = khi_c * (math.pi/180)
        #calcul de la direction du vent à partir de sa provenance 
        direction_vent_magnetique = Wind_Comp + 180* (math.pi/180) - Dec_Magnetique 
         #calcul de la dérive et du cap vrai
        d = math.asin((V_Wind * math.sin(khi_c * (math.pi/180) - direction_vent_magnetique))/Vp * math.cos(fpa))
    cap_vrai = 0

    #Evite cap <0 et >360 
    if d > 0 :
        cap_vrai = khi_c - d
        if cap_vrai < 0 :
            cap_vrai +=360* (math.pi/180)
    elif d < 0 :
        cap_vrai = khi_c + d #cap en rad
        if cap_vrai > 360* (math.pi/180) :
            cap_vrai-=360* (math.pi/180) 
    elif d == 0 :
        cap_vrai = khi_c

    #print("CAP VRAI fct route managed", cap_vrai * (180/math.pi))
    return cap_vrai

def on_FCU_Mod(agent, *larg) :
    global Fcu_Mode
    global Fcu_Value
    Fcu_Mode = larg[0]
    Fcu_Value = float(larg[1])

def Capture_CAP (target):

    global Vp
    global psi  #psi
    global phi  #phi
    global Fcu_Value
    global Max_Roll_Rate
    global Max_Roll
    global Dec_Magnetique
    global Fcu_Mode
    print('ok')
    TPhi= 1.7
    TPsi = 5.1 #3*TauPhi
    g = 9.81
    p=0
    Max_Roll=0.575959
    Max_Roll_Rate=0.261799

    if Fcu_Mode == "SelectedHeading" :
        target = target*(math.pi/180) - Dec_Magnetique
    elif Fcu_Mode == "SelectedTrack" :
        target = target - Dec_Magnetique
   
    Delat_Cap = (target-psi)

    while Delat_Cap > math.pi:
        Delat_Cap = Delat_Cap - 2*math.pi
    while Delat_Cap <= -math.pi:
        Delat_Cap = Delat_Cap + 2*math.pi


    #Capture de cap
    phic = Delat_Cap*(Vp/(g*TPsi))
    if phic > Max_Roll:
        phic = Max_Roll 
    if phic < -Max_Roll:
        phic = -Max_Roll

    p = (phic-phi)/TPhi

    if (p>=Max_Roll_Rate):
        p =Max_Roll_Rate
    if (p<=(-Max_Roll_Rate)):
        p = -Max_Roll_Rate
    
    print("p pour Ivy", p*(180/math.pi), " en deg")
    #print("Delta axe ",diff_heading )
    print(p)
    #p_string = str(p)
    print('ANGLE :', phi*(180/math.pi))
    #IvySendMsg("APLatControl rollRate="+p_string)
    IvySendMsg("APLatControl rollRate=".format(str(p)))

def on_Perfo_Msg(agent, *larg) :
    global Max_Roll
    global Max_Roll_Rate
    Max_Roll = float(larg[9])
    Max_Roll_Rate = float(larg[10])
    print(Max_Roll)
    print(Max_Roll_Rate)

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
        #Capture_Cap(Fcu_Value)
        Capture_CAP(Fcu_Value)
        


#10.1.127.255:3010
app_name = "PA_LAT"
ivy_bus = "127.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_FCU_Mod, r'^FCULateral Mode=(\S+) Val=(\S+)')
IvyBindMsg(on_StateVector, r'^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)')
IvyBindMsg(on_FGS_Msg, r'^FM_Active_leg x1=(\S+) x2=(\S+) y1=(\S+) y2=(\S+) h_contrainte=(\S+)')
IvyBindMsg(on_MagnticDeclination, r'^MagneticDeclination=(\S+)')
IvyBindMsg(on_WindComponent, r'^WindComponent VWind=(\S+) dirWind=(\S+)')
IvyBindMsg(on_Perfo_Msg, r'^Perfo ViManage=(\S+) ViMin=(\S+) ViMax=(\S+) nxMin=(\S+) nxMax=(\S+) nzMin=(\S+) nzMax=(\S+) fpaMin=(\S+) fpaMax=(\S+) roulisMax=(\S+) rollrateMax=(\S+)')
IvyMainLoop()


# FCULateral Mode=Managed Val=0
# Perfo ViManage=0 ViMin=0 ViMax=0 nxMin=0 nxMax=0 nzMin=0 nzMax=0 fpaMin=0 fpaMax=0 roulisMax=0.575959 rollrateMax=0.261799
# FM_Active_leg x1=0 x2=10 y1=34 y2=56 h_contrainte=24