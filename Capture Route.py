from cmath import asin, sin, cos
import math 

def calcul_route(V_Wind , Vp, route,fpa, Wind_Comp, Fcu_Mode, Fcu_Value, Declinaison_Magnetique=13.69*(math.pi/180)): 

    # mode MANAGE sélectioné 
    if Fcu_Mode =="Managed":
        direction_vent_vrai = Wind_Comp +180 #calcul de la direction du vent à partir de sa provenance

    #calcul de la dérive vrai 
        d=asin((V_Wind*sin(route- direction_vent_vrai))/Vp*cos(fpa))
    
    #calcul du cap vrai
        cap_vrai = route - d
        return cap_vrai

 
# mode SELECT sélectioné 

    if Fcu_Mode =="SelectedHeading" :
        direction_vent_magnetique = Wind_Comp + 180 - Declinaison_Magnetique # conversion de la diretion du vent vrai en magnétique

    #calcul de la dérive magnétique
        d=asin((V_Wind*sin(Fcu_Value- direction_vent_magnetique))/Vp*cos(fpa))

    #calcul du cap magnétique
        cap_magnetique = Fcu_Value - d #cap en rad 
        return cap_magnetique
