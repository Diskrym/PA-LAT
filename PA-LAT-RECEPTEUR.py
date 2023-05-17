from ivy.std_api import *

xGlobal = None

def on_cx_proc(agent, connected) :
    pass
def on_die_proc(agent, _id) :
    pass
def on_msg(agent, *larg):
    print("Msg with arg %s received" % larg[0])

def on_StateVector(agent, *larg):
    global xGlobal
    print("x={}, y={}".format(larg[0],larg[1]))
    xGlobal = float(larg[0])

def on_FGS_Msg(agent, *larg):
    global xGlobal
    print("x+5={}".format(xGlobal+5))


app_name = "PA_LAT"
ivy_bus = "127.255.255.255:2010"
IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_StateVector, '^StateVector x=(\S+) y=(\S+)')
IvyBindMsg(on_FGS_Msg, '^FGS_Msg xWpt=(\S+) yWpt=(\S+)')
IvyMainLoop()