import time
import math
from ivy.std_api import *

class Waypoint:
    def __init__(self, name, x, y, z, type) :
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.type = type

    def __str__(self):
        return f"Waypoint: {self.name}\nCoordinates: ({self.x}, {self.y})\nz: {self.z}\nType: {self.type}"

class Leg :
    def __init__(self, start_wpt, end_wpt, start_x, start_y, end_x, end_y, z_constraint, type):
        self.start_wpt = start_wpt
        self.end_wpt = end_wpt
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y
        self.z_constraint = z_constraint
        self.type = type
    
    def __str__(self):
        return f"Waypoint Départ {self.start_wpt} : ({self.start_x}, {self.start_y}) \nWaypoint Arrivée {self.end_wpt} : ({self.end_x}, {self.end_y})\nz: {self.z_constraint}\nType: {self.type}"

# ----- Function create_waypoints -----
# Create waypoints from a text file
# Parameters:
#   - file: The path to the text file containing the waypoints
# Returns:
#   - waypoints: A list of Waypoint objects created from the file

def create_waypoints(file):
    waypoints = []
    with open(file, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Delete spaces at the beginning and at the end
            if line.startswith("[") and line.endswith("]"):
                # Extract values between brackets
                values = line[1:-1].split(",")
                if len(values) == 5:
                    # Create Waypoint object with values
                    waypoint = Waypoint(values[0], int(values[1]), int(values[2]), int(values[3]), values[4].strip())
                    waypoints.append(waypoint)
    return waypoints

# -------------------------------

# ----- Function create_legs -----
# Create a list of legs between every waypoint
# Parameters:
#   - waypoints: A list of waypoint objects representing the flight plan
# Returns:
#   - legs: A list of Leg objects representing the legs between each waypoint

def create_legs(waypoints):
    legs = []  # List to store the legs
    i = 1  # Index variable for the starting waypoint
    j = i  # Index variable for searching the next non-negative z value

    # Iterate through the waypoints
    while i < len(waypoints):
        # Find the next non-negative z value
        while j < len(waypoints) and waypoints[j].z < 0:
            j += 1

        # Determine the value of z based on whether a non-negative z value was found
        if j == len(waypoints):
            z = -1
        else:
            z = waypoints[j].z

        # Create a leg object using the waypoint information and add it to the list
        leg = Leg(waypoints[i-1].name, waypoints[i].name, waypoints[i-1].x, waypoints[i-1].y, waypoints[i].x, waypoints[i].y, z, waypoints[i].type)
        legs.append(leg)

        # Update the index variables for the next iteration
        i += 1
        j = i

    return legs

# -------------------------------

# ----- Function angle -----
# Calculates the angle between the current position of the plane and the end waypoint
# of the next leg, taking into account the next waypoint.
# Parameters:
#   - x_start/y_start: The beginning of the leg
#   - x_intermediate/y_intermediate: The next waypoint in the flight plan
#   - x_arrival/y_arrival: The end waypoint of the next leg
# Returns:
#   - The angle between the current position and the end waypoint, in radians.

def angle(x_start, y_start, x_intermediate, y_intermediate, x_arrival, y_arrival):

    # Vectors calulation between points
    v1 = (x_start - x_intermediate, y_start - y_intermediate)
    v2 = (x_arrival - x_intermediate, y_arrival - y_intermediate)

    # Norms calculation of vectors
    norm_v1 = math.sqrt(math.pow(v1[0], 2) + math.pow(v1[1], 2))
    norm_v2 = math.sqrt(math.pow(v2[0], 2) + math.pow(v2[1], 2))

    # Scalar product of vectors
    scalar_product = v1[0] * v2[0] + v1[1] * v2[1]

    # Angle calculation in radians
    return math.acos(scalar_product / (norm_v1 * norm_v2))

# -------------------------------

# ----- Function DIRTO -----
# Seek for the leg located just before the waypoint of the DIRTO
# Parameters:
#   - new_waypoint: The waypoint chosen for the new leg
#   - legs: A list of Leg objects representing the legs between waypoints
#   - active_leg: The index of the currently active leg
# Returns:
#   - active_leg: The updated index of the active leg

def DIRTO(new_waypoint, legs, active_leg):
    i = 0
    while i < len(legs):
    # Check if the new waypoint matches the end waypoint of the current leg
        if new_waypoint != legs[i].end_wpt:
            i += 1  # If not, move to the next leg
        else:
            active_leg = i  # Set the active leg index to the current leg
            i = len(legs)  # Exit the loop by setting i to the length of legs
    return active_leg 

# -------------------------------

# ----- Function check_change_leg -----
# Check if we pass the waypoint and change the current leg once the waypoint is passed
# Note: The last waypoint cannot be a flyby
# Parameters:
#   - legs: A list of Leg objects representing the legs between waypoints
#   - active_leg: The index of the currently active leg
#   - x_plane/y_plane: The current plane's position
#   - radius_circle: The specified radius to determine if the waypoint is passed
#   - check_dirto : Boolean to check if we are in DIRTO mode
# Returns:
#   - active_leg: The updated index of the active leg

def check_change_leg(legs, active_leg, x_plane, y_plane, radius_circle, check_dirto):
    # Calculate the distance between the plane and the waypoint of the active leg
    distance_plane = math.sqrt((math.pow(x_plane - legs[active_leg].end_x, 2) + math.pow(y_plane - legs[active_leg].end_y, 2)))

    # Check if the distance is less than the specified radius_circle
    if distance_plane < radius_circle:
        active_leg += 1  # Increment the active_leg index if the condition is met
    return active_leg

# -------------------------------

# ----- Function radius -----
# Calculate the radius of the circle around the waypoints
# Parameters:
#   - legs: A list of Leg objects representing the legs between waypoints
#   - active_leg: The index of the currently active leg
#   - x/y: Starting coordinates
#   - ground_speed: Speed of the plane 
#   - phi_max: Roll gradient in radian
# Returns:
#   - The radius of the circle, in meters

def radius(legs, active_leg, x, y, ground_speed, phi_max):
    g = 9.80665 # m.s-2
    if legs[active_leg].type == "flyBy" and active_leg + 1 < len(legs):
        alpha = angle(x, y, legs[active_leg + 1].start_x, legs[active_leg + 1].start_y, legs[active_leg + 1].end_x, legs[active_leg + 1].end_y)
    else:
        return 2 * ground_speed # m

    if phi_max == 0 or alpha == 0:
        return 4630 # m
    else:
        distance = math.pow(ground_speed, 2) / (g * math.tan(alpha/2) * math.tan(phi_max))
        return min(max(distance, 2 * ground_speed), 4630)
    
# -------------------------------

# ----- Functions to convert -----

def feet_to_meters(feet):
    return feet / 3.28084

def knots_to_mps(knots):
    return knots * 0.514444

# -------------------------------

# Ivy functions
def on_cx_proc (agent, connected):
    pass
def on_die_proc (agent, _id):
    pass

def on_dirto (agent, *larg):
    global dirto 
    global legs
    global active_leg
    global x_plane
    global y_plane
    global x_leg_dirto
    global y_leg_dirto
    global check_dirto
    
    dirto = larg[0]
    check_dirto = True
    x_leg_dirto = x_plane
    y_leg_dirto = y_plane
    
    print("DIRTO " + dirto)
    active_leg = DIRTO(dirto, legs, active_leg)
    

def on_state_vector(agent, *larg):
    global x_plane
    global y_plane
    global z_plane
    global Vp
    global flight_path_angle
    global psi
    global phi
        
    x_plane = float(larg[0])
    y_plane = float(larg[1])
    z_plane = float(larg[2])
    Vp = float(larg[3]) 
    flight_path_angle = float(larg[4]) 
    psi = float(larg[5]) 
    phi = float(larg[6])
    print("StateVector x =", x_plane, "y =", y_plane, "z =", z_plane, "VP =", Vp, "fpa =", flight_path_angle, "psi =", psi, "phi =", phi)

def on_perf(agent, *larg):

    global phi_max
    global legs
    global active_leg
    global x_plane
    global y_plane
    global Vp
    global flight_path_angle
    global phi
    global v_wind
    global dir_wind
    global ground_speed
    global check_dirto

    phi_max = float(larg[9])
    print("Perfo roulisMax =", phi_max)
    x_dot = Vp * math.cos(flight_path_angle) * math.cos(phi) + v_wind * math.cos(dir_wind + math.pi)
    y_dot = Vp * math.cos(flight_path_angle) * math.sin(phi) + v_wind * math.sin(dir_wind + math.pi)
    ground_speed = math.sqrt(math.pow(x_dot, 2) + math.pow(y_dot, 2))

    old_active_leg = active_leg

    if check_dirto:
        radius_circle = radius(legs, active_leg, x_leg_dirto, y_leg_dirto, ground_speed, phi_max)
    else:
        radius_circle = radius(legs, active_leg, legs[active_leg].start_x, legs[active_leg].start_y, ground_speed, phi_max)

    active_leg = check_change_leg(legs, active_leg, x_plane, y_plane, radius_circle, check_dirto)
    if old_active_leg < active_leg:
        check_dirto = False
    if (active_leg == len(legs)):
        active_leg = len(legs) - 1
    if check_dirto:
        print("FM_Active_leg x1=" + str(x_leg_dirto) + " x2=" + str(legs[active_leg].start_x) + " y1=" + str(y_leg_dirto) + " y2=" + str(legs[active_leg].start_y) + " h_contrainte=" + str(legs[active_leg].z_constraint))
        IvySendMsg("FM_Active_leg x1=" + str(x_leg_dirto) + " x2=" + str(legs[active_leg].start_x) + " y1=" + str(y_leg_dirto) + " y2=" + str(legs[active_leg].start_y) + " h_contrainte=" + str(legs[active_leg].z_constraint))
    else:
        print("FM_Active_leg x1=" + str(legs[active_leg].start_x) + " x2=" + str(legs[active_leg].end_x) + " y1=" + str(legs[active_leg].start_y) + " y2=" + str(legs[active_leg].end_y) + " h_contrainte=" + str(legs[active_leg].z_constraint))
        IvySendMsg("FM_Active_leg x1=" + str(legs[active_leg].start_x) + " x2=" + str(legs[active_leg].end_x) + " y1=" + str(legs[active_leg].start_y) + " y2=" + str(legs[active_leg].end_y) + " h_contrainte=" + str(legs[active_leg].z_constraint))

def on_time_1(agent, *larg):
    
    global x_plane
    global y_plane
    global z_plane
    global Vp 
    global flight_path_angle
    global psi
    global phi
    
    if float(larg[0]) == 1.0:
        print("InitStateVector x=" + str(x_plane) + " y=" + str(y_plane) + " z=" + str(z_plane) + " Vp=" + str(Vp) + " fpa=" + str(flight_path_angle) +  " psi=" + str(psi) + " phi=" + str(phi))
        print("WindComponent VWind=" + str(v_wind) + " dirWind=" + str(dir_wind))
        print("MagneticDeclination=" + str(magnetic_declination))
        IvySendMsg("InitStateVector x=" + str(x_plane) + " y=" + str(y_plane) + " z=" + str(z_plane) + " Vp=" + str(Vp) + " fpa=" + str(flight_path_angle) +  " psi=" + str(psi) + " phi=" + str(phi))
        IvySendMsg("WindComponent VWind=" + str(v_wind) + " dirWind=" + str(dir_wind))
        IvySendMsg("MagneticDeclination=" + str(magnetic_declination))

# Internal datas
magnetic_declination = math.radians(13.69) # rad
khi = math.radians(14) + magnetic_declination # rad

v_wind = knots_to_mps(0) # m.s-1
dir_wind = math.radians(20) + magnetic_declination  # rad

x_plane = 0 # m
y_plane = 0 # m
z_plane = feet_to_meters(25) # m
Vp = knots_to_mps(20) # m.s-1
flight_path_angle = math.radians(0) # rad
d = math.asin((v_wind * math.sin(khi - dir_wind))/(Vp * math.cos(flight_path_angle))) # rad / drift angle
phi = math.radians(0) # rad / roll
psi = khi - d # rad / heading
check_dirto = False
x_leg_dirto = 0
y_leg_dirto = 0

active_leg = 0
i = 0

file = "FPL.txt"
waypoints = create_waypoints(file)

legs = create_legs(waypoints)
for leg in legs:
    print("Leg number", i)
    print(leg)
    print("-------------")
    i += 1


app_name="FMGS"
# Local
ivy_bus="127.0.0.1:2010" 
# Broadcast
# ivy_bus="10.3.63.255:2022"

IvyInit(app_name,"[%s ready]", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
time.sleep(1.0)

# ----- BUS reception -----

IvyBindMsg(on_state_vector, '^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)')
IvyBindMsg(on_dirto, '^DIRTO (\S+)')
IvyBindMsg(on_perf, '^Perfo ViManage=(\S+) ViMin=(\S+) ViMax=(\S+) nxMin=(\S+) nxMax=(\S+) nzMin=(\S+) nzMax=(\S+) fpaMin=(\S+) fpaMax=(\S+) roulisMax=(\S+) rollrateMax=(\S+)')
IvyBindMsg(on_time_1, '^Time t=(\S+)')

IvyMainLoop()


# ----------