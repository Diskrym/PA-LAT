from ivy.std_api import *

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
x = 0
y = 0
for i in range(0,5):
    time.sleep(1.0)
    IvySendMsg('StateVector x={} y={}'.format(x,y))
    x = x+1
    y = y - 1
    if i == 3:
        IvySendMsg('FGS_Msg xWpt=8 yWpt=10')
IvyStop()