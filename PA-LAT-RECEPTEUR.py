#C:/msys64/mingw64/bin/python.exe c:/Users/louis/OneDrive/Bureau/PA-LAT/PA-LAT-RECEPTEUR.py

from ivy.std_api import * #type: ignore

Vector_X=None
Vector_Y=None
Wind_Comp=None
V_Wind=None
Dec_Magnetique=None
Fcu_Mode=None
Fcu_Value=None



#init
def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass

def on_msg(agent, *larg):
    print("Msg with arg %s received" % larg[0])

def on_StateVector(agent, *larg):
    global Vector_X
    global Vector_Y
    print("x={}, y={}".format(larg[0],larg[1]))
    Vector_X = float(larg[0])
    Vector_Y = float(larg[1])

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

def on_FCU_Mod(agent, *larg) :
    global Fcu_Mode
    global Fcu_Value
    Fcu_Mode = larg[0]
    Fcu_Value = larg[1]
    print("Mode={}, Value={}".format(larg[0],larg[1]))


def on_FGS_Msg(agent, *larg):
    global xGlobal
    

app_name = "PA_LAT"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_StateVector, r'^StateVector x=(\S+) y=(\S+)')
IvyBindMsg(on_FGS_Msg, r'^FGS_Msg xWpt=(\S+) yWpt=(\S+)')
IvyBindMsg(on_MagnticDeclination, r'^MagneticDeclination=(\S+)')
IvyBindMsg(on_WindComponent, r'^WindComponent VWind=(\S+) dirWind=(\S+)')
IvyBindMsg(on_FCU_Mod, r'^FCULateral Mode=(\S+) Val=(\S+)')

IvyMainLoop()