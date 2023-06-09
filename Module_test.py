#C:/Users/louis/AppData/Local/Programs/Python/Python39/python.exe "c:/Users/louis/OneDrive/Bureau/PA-LAT/Module_test.py"

from ivy.std_api import * #type: ignore
import math
import time
Fcu_Mode = ""


def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass

def on_msg(agent, *larg):
    print("Msg with arg %s received" % larg[0])  

app_name = "PA_LAT_test"
ivy_bus = "127.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
time.sleep(1.0)
x1 = 0
y1 = 0
x2 = 10000
y2 = 0
magnetic_declination = math.radians(13.69)
Dec_Magnetique = str(13.69*(math.pi/180))
V_Wind = str(30)
Wind_Comp = math.radians(90) + magnetic_declination
Fcu_Mode="Managed"
#Fcu_Mode="SelectedTrack"
#Fcu_Mode="SelectedHeading"
Fcu_Value=str(0)
roulisMax=str(0.575959)
rollrateMax=str(0.261799)
IvySendMsg('WindComponent VWind={} dirWind={}'.format(V_Wind,Wind_Comp))
IvySendMsg('MagneticDeclination={}'.format(Dec_Magnetique))
IvySendMsg('FCULateral Mode={} Val={}'.format(Fcu_Mode,Fcu_Value))

for i in range(0,30):
    time.sleep(1.0)
    IvySendMsg('FM_Active_leg x1={} x2={} y1={} y2={} h_contrainte={}'.format(x1,x2,y1,y2,0))
    IvySendMsg('Perfo ViManage={} ViMin={} ViMax={} nxMin={} nxMax={} nzMin={} nzMax={} fpaMin={} fpaMax={} roulisMax={} rollrateMax={}'.format(0,0,0,0,0,0,0,0,0,roulisMax,rollrateMax))

x1 = 10000
y1 = 0
x2 = 10000
y2 = 10000

for i in range (0,100000) :
    time.sleep(1.0)
    print(x2,",",y2)
    IvySendMsg('FM_Active_leg x1={} x2={} y1={} y2={} h_contrainte={}'.format(x1,x2,y1,y2,0))
    IvySendMsg('Perfo ViManage={} ViMin={} ViMax={} nxMin={} nxMax={} nzMin={} nzMax={} fpaMin={} fpaMax={} roulisMax={} rollrateMax={}'.format(0,0,0,0,0,0,0,0,0,roulisMax,rollrateMax))

x1 = 10000
y1 = 10000
x2 = -10000
y2 = 10000

for i in range (0,60000) :
    time.sleep(1.0)
    IvySendMsg('FM_Active_leg x1={} x2={} y1={} y2={} h_contrainte={}'.format(x1,x2,y1,y2,0))
    IvySendMsg('Perfo ViManage={} ViMin={} ViMax={} nxMin={} nxMax={} nzMin={} nzMax={} fpaMin={} fpaMax={} roulisMax={} rollrateMax={}'.format(0,0,0,0,0,0,0,0,0,roulisMax,rollrateMax))

x1 = -10000
y1 = 10000
x2 = -10000
y2 = 0


for i in range (0,60) :
    time.sleep(1.0)
    print(x2,",",y2)
    IvySendMsg('FM_Active_leg x1={} x2={} y1={} y2={} h_contrainte={}'.format(x1,x2,y1,y2,0))
    IvySendMsg('Perfo ViManage={} ViMin={} ViMax={} nxMin={} nxMax={} nzMin={} nzMax={} fpaMin={} fpaMax={} roulisMax={} rollrateMax={}'.format(0,0,0,0,0,0,0,0,0,roulisMax,rollrateMax))

x1 = -10000
y1 = 0
x2 = 0 
y2 =0

for i in range (0,60) :
    time.sleep(1.0)
    IvySendMsg('FM_Active_leg x1={} x2={} y1={} y2={} h_contrainte={}'.format(x1,x2,y1,y2,0))
    IvySendMsg('Perfo ViManage={} ViMin={} ViMax={} nxMin={} nxMax={} nzMin={} nzMax={} fpaMin={} fpaMax={} roulisMax={} rollrateMax={}'.format(0,0,0,0,0,0,0,0,0,roulisMax,rollrateMax))

IvyStop()