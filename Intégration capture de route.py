#C:/msys64/mingw64/bin/python.exe c:/Users/louis/OneDrive/Bureau/PA-LAT/PA-LAT-RECEPTEUR.py


from ivy.std_api import * #type: ignore
from cmath import asin, sin, cos
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
# x1=-10000
# x2=40000
# y1=20000
# y2=70000

x1=0
x2=-15000
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
    global phi
    Vector_X = float(larg[0])
    Vector_Y = float(larg[1])
    Vp = float(larg[3])
    fpa = float(larg[4])
    psi = float(larg[5])
    phi = float(larg[6])
    #############Pour Test################
    if Fcu_Mode == "Managed" :
        print("AXE")
        capture_daxe()
    elif  Fcu_Mode == "SelectedTrack" :
        print("ROUTE")
        calcul_route_sélecté(Fcu_Value)
    elif Fcu_Mode == "SelectedHeading" :
        #Capture_Cap(Fcu_Value)
        heading_capture(Fcu_Value)
    #############Pour Test################


def on_WindComponent (agent, *larg):
    global V_Wind
    global Dir_Wind
    print("x={}, y={}".format(larg[0],larg[1]))
    V_Wind = float(larg[0])
    Dir_Wind = float(larg[1])

def on_MagnticDeclination(agent, *larg) :
    global Dec_Magnetique
    Dec_Magnetique = float(larg[0])
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
    #T_ey = 1
    T_ey = 37 # 10*TauPsi

    xdot = Vp*cos(fpa) * cos(psi) + V_Wind * cos(Wind_Comp+math.pi)
    ydot = Vp*cos(fpa) * sin(psi) + V_Wind * sin(Wind_Comp+math.pi) 

    
    Gs = math.sqrt((math.pow(ydot.real,2)) + (math.pow(xdot.real,2))) #ground speed

    if y2-y1 != 0 and x2-x1 != 0:
        if y2-y1 <0 and x2-x1 < 0:
            khi_a = math.atan((x2-x1)/(y2-y1))+180*(math.pi/180) #route avion
            print(khi_a*(180/math.pi))
        else : 
            khi_a = math.atan((x2-x1)/(y2-y1))
    if y2-y1 == 0:
        if x2-x1 > 0 :
            khi_a =  1.5708
        elif x2-x1 < 0 :
            khi_a = 4.71239
    if x2-x1 == 0 :
        if y2-y1 > 0 :
            khi_a = 0
        if y2-y1 < 0 :
            khi_a = 3.14159
 

    ey= -sin(khi_a)*(Vector_X- x1) + cos(khi_a) * (Vector_Y- y1) #cross_track
    print(ey.real)
    print(Gs)
    print(T_ey)
    
    # Test=ey.real/(Gs*T_ey)
    # if Test<= -math.sin(45) :
    #     khi_c=-math.asin(-math.sin(45)+khi_a)
    
    # if Test>= math.sin(45) :
    #     khi_c=-math.asin(math.sin(45)+khi_a)

    if ey.real/(Gs*T_ey) > 1 :
        khi_c = khi_a - math.asin(1)
    elif ey.real/(Gs*T_ey) < -1 :
        khi_c = khi_a - math.asin(-1)
    else :
        khi_c = khi_a - math.asin(ey.real/(Gs*T_ey))


    if khi_c*(180/math.pi) <0 :
        khi_c=khi_c+360*(math.pi/180)
    elif khi_c*(180/math.pi) > 360 :
        khi_c= khi_c - 360*(math.pi/180)

    print('Envoie cap (fct axe) :', khi_c.real*(180/math.pi))

    #Capture_Cap(calcul_route_managé(khi_c.real))
    heading_capture(calcul_route_managé(khi_c.real))

def calcul_route_sélecté(obj): 
    
    global Dec_Magnetique
    global V_Wind
    global Vp
    global fpa
    global Wind_Comp

# conversion de la diretion du vent vrai en magnétique
    direction_vent_magnetique = Wind_Comp + 180* (math.pi/180) - Dec_Magnetique 

#calcul de la dérive et du cap magnétique

    d = asin((V_Wind*sin(obj* (math.pi/180) - direction_vent_magnetique))/Vp*cos(fpa))
    d=d.real
    cap_magnetique = 0
    if d > 0 :
        cap_magnetique = obj* (math.pi/180) - d
        if cap_magnetique < 0 :
            cap_magnetique +=360* (math.pi/180)
    elif d < 0 :
        cap_magnetique = obj*(math.pi/180) + d #cap en rad
        if cap_magnetique > 360* (math.pi/180) :
            cap_magnetique-=360* (math.pi/180) 
    elif d == 0 :
        cap_magnetique=obj* (math.pi/180)
    print('Envoie cap (fct route) :', cap_magnetique)
    #Capture_Cap(cap_magnetique)
    heading_capture(cap_magnetique)

def calcul_route_managé(khi_c): 
    global V_Wind
    global Vp
    global fpa
    global Wind_Comp

#calcul de la direction du vent à partir de sa provenance 
    direction_vent_vrai = Wind_Comp + 180* (math.pi/180)

 #calcul de la dérive et du cap vrai 
    d=asin((V_Wind*sin(khi_c- direction_vent_vrai))/Vp*cos(fpa))
    d=d.real
    cap_vrai = 0
    if d > 0 :
        cap_vrai = khi_c - d
        if cap_vrai < 0 :
            cap_vrai +=360* (math.pi/180)
    elif d < 0 :
        cap_vrai = khi_c + d #cap en rad
        if cap_vrai > 360* (math.pi/180) :
            cap_vrai-=360* (math.pi/180) 
    elif d == 0 :
        cap_vrai=khi_c
    print("CAP VRAI fct route managed", cap_vrai * (180/math.pi))
    return cap_vrai


def on_FCU_Mod(agent, *larg) :
    global Fcu_Mode
    global Fcu_Value
    Fcu_Mode = larg[0]
    ########Debug###########
    if Fcu_Mode == '0' :
        Fcu_Mode = 'Managed'

    Fcu_Value = float(larg[1])
    #print("Mode={}, Value={}".format(larg[0],larg[1]))


# def Capture_Cap(cap): #mode selecte, on entre un cap au fcu
#     """VARIABLE D'IVY"""
#     global psi
#     global Dec_Magnetique
#     global Fcu_Value
#     global phi

    
#     """PASSAGE DE CAP MAGNETIQUE A CAP VRAI"""
#     if Fcu_Mode != "Managed" :
#         Heading_v=psi+Dec_Magnetique #Cap_vrai actuel [rad]
#         Fcu_Value_v=Fcu_Value*(math.pi/180)+Dec_Magnetique #Cap_vrai objectif [rad]
#     else :
#         Heading_v=psi
#         Fcu_Value_v = cap

#     if Heading_v<0: #evite cap negatifs
#         Heading_v+=360*(math.pi/180)
#     if Fcu_Value_v<0: #evite cap negatifs
#         Fcu_Value_v+=360*(math.pi/180)
        
#     """CALCUL ANGLE A PARCOURIR"""
#     if Heading_v<Fcu_Value_v<Heading_v+180*(math.pi/180): #calcul de l'angle a parcourir
#         d_objectif_v=Fcu_Value_v-Heading_v
#     else:
#         if 0<=Heading_v<Fcu_Value_v:
#             d_objectif_v=Heading_v+(360*(math.pi/180))-Fcu_Value_v
#         else:
#             d_objectif_v=Heading_v-Fcu_Value_v
#     #print("delta objectif:{}".format(d_objectif_v*(180/math.pi))) #print test de controle angle à parcourir

#     """BOUCLE INSTRUCTION MISE EN VIRAGE"""

#     tphi=1.7
#     tpsi=3*tphi
#     p=(((1/tpsi)-psi)*(1/tphi))*d_objectif_v


#     while d_objectif_v!=0:

#         if Heading_v<=Fcu_Value_v and Fcu_Value_v<=Heading_v+180*(math.pi/180):
#             p=1*p
#             #print("vd p:{}".format(p)) #p>0
#         else:
#             p=(-1)*p
#             #print("vg p:{}".format(p)) #p<0
        
#     print("ENVOIE   ")
#     print(p)
#     IvySendMsg('Roll_Rate:{}'.format(str(p)))

def heading_capture (obj):

    global Vp
    global recorded_fpa
    global psi  #psi
    global phi  #phi
    global Fcu_Value

    #global rollAngleLimit
    #global rollRateLimit 
    global Dec_Magnetique
    global Fcu_Mode

    #TauPhi = 1.2 #A modifier 
    #TauPsi = 5*TauPhi
    TauPhi= 1.7
    TauPsi = 5.1 #3*TauPhi
    gravity = 9.81
    p=0


    if Fcu_Mode == "SelectedHeading" :
        Dec_Magnetique = 0.23893557
        obj = obj*(math.pi/180) - Dec_Magnetique
    elif Fcu_Mode == "SelectedTrack" :
        obj = obj - Dec_Magnetique
   
    #recorded_heading = recorded_heading%(2*math.pi)
    diff_heading = (obj-psi)
    while diff_heading > math.pi:
        diff_heading = diff_heading - 2*math.pi
    while diff_heading <= -math.pi:
        diff_heading = diff_heading + 2*math.pi

    #if ((diff_heading) >= math.pi):
    #    diff_heading = diff_heading-(2*math.pi)
    

    #Capture de cap
    phic = diff_heading*(Vp/(gravity*TauPsi))


    rollAngleLimit=0.575959
    rollRateLimit=0.261799
    print("phic = ", phic, "en deg")
    print("rollangle limite ", rollAngleLimit*(180/math.pi), "en deg")

    if phic > rollAngleLimit:
        phic = rollAngleLimit
        
    if phic < -rollAngleLimit:
        phic = -rollAngleLimit

    p = (phic-phi)/TauPhi

    if (p>=rollRateLimit):
        p =rollRateLimit
    if (p<=(-rollRateLimit)):
        p = -rollRateLimit
    

    #if ((recorded_rollangle >= rollAngleLimit and p >0) or (recorded_rollangle <= (-rollAngleLimit) and p<0 )):
    #    p = 0

    #print("p est saturé =",p*(180/math.pi)," deg/sec" )
    print("p envoyé", p*(180/math.pi), " en deg")
    print("diff heading ",diff_heading )

    p_string = str(p)
    print('ANGLE :', phi*(180/math.pi))
    IvySendMsg("APLatControl rollRate="+p_string)



def on_FGS_Msg(agent, *larg): 
    global x1,x2
    global y1,y2
    
    x1 = float(larg[0])
    x2 = float(larg[1])
    y1 = float(larg[2])
    y2 = float(larg[3])
    print(Fcu_Mode)

    #lancement du code au message du FM
    if Fcu_Mode == "Managed" :
        print("AXE")
        capture_daxe()
    elif  Fcu_Mode == "SelectedTrack" :
        print("ROUTE")
        calcul_route_sélecté(Fcu_Value)
    elif Fcu_Mode == "SelectedHeading" :
        print("CAP")
        #Capture_Cap(Fcu_Value)
        heading_capture(Fcu_Value)
        


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
IvyMainLoop()