from ivy.std_api import * #type: ignore
import math
import time

def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass

def on_msg(agent, *larg):
    print("Msg with arg %s received" % larg[0])  

app_name = "PA_LAT_test"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
time.sleep(1.0)
x1 = 10
y1 = 10
x2 = 100
y2 = 100
x=0
y=0
z=0
Vp= 154.33
fpa= 0
psi= 0
Dec_Magnetique = 13.69*(math.pi/180)
V_Wind = 0
Wind_Comp = 90*(math.pi/180)
Fcu_Mode="Managed"
Fcu_Value=1

for i in range(0,5):
    time.sleep(1.0)
    IvySendMsg('FM_Active_leg x1={}, x2={}, y1={}, y2={}'.format(x1,x2,y1,y2))
    IvySendMsg('StateVector x={} y={} z={} Vp={} fpa={} psi{}'.format(x,y,z,Vp,fpa,psi))
    IvySendMsg('MagneticDeclination={}'.format(Dec_Magnetique))
    IvySendMsg('WindComponent VWind={} dirWind={}'.format(V_Wind,Wind_Comp))
    IvySendMsg('FCULateral Mode={} Val={}'.format(Fcu_Mode,Fcu_Value))
   
IvyStop()