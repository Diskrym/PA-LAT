from perfovalues import *

class FlightPhase:
    def __init__(self, name, flightPhaseType, canConfigureFlaps, canConfigureLandingGear, altitudeRange, vTable, vTargets, nxTable, nzTable, fpaTable, rollTable, rollRateTable):
        self.name=name
        self.flightPhaseType=flightPhaseType # 1 : climb - 0 : cruize - -1 : descent
        self.canConfigureFlaps=canConfigureFlaps
        self.canConfigureLandingGear=canConfigureLandingGear
        self.altitudeRanges=altitudeRange
        self.vTable=vTable
        self.vTargets=vTargets
        self.nxTable=nxTable
        self.nzTable=nzTable
        self.fpaTable=fpaTable
        self.rollTable=rollTable
        self.rollRateTable=rollRateTable
        
class FlightEnvelope:
    def __init__(self, flightPhases):
        self.flightPhases = flightPhases
        self.lastFlightPhaseType = None
        
    def getMatchingFlightPhases(self,currentAltiude):
        altitudeRanges = ()
        for key in self.flightPhases:
            if key[0] <= currentAltiude <= key[1] or key[0] >= currentAltiude >= key[1]:
                altitudeRanges += (key,)
        return altitudeRanges
        
    def getFlightPhase(self,previousAltitude,currentAltiude):
        altitudeRanges = self.getMatchingFlightPhases(currentAltiude)
        print("altitudeRanges : ", altitudeRanges)
        print("len(altitudeRanges) : ", len(altitudeRanges))
        if len(altitudeRanges) == 1:
            print("1 altitudeRanges")
            print("altitudeRange[0] : ", self.flightPhases[altitudeRanges[0]].flightPhaseType)
            print(f"getflightPhaseType({previousAltitude},{currentAltiude}) : {self.getflightPhaseType(previousAltitude,currentAltiude)}")
            
            if self.flightPhases[altitudeRanges[0]].flightPhaseType == self.getflightPhaseType(previousAltitude,currentAltiude):
                print("1st")
                return self.flightPhases[altitudeRanges[0]]
        elif len(altitudeRanges) == 2:
            print("2 altitudeRanges")
            print("altitudeRange[0] : ", self.flightPhases[altitudeRanges[0]].flightPhaseType)
            print("altitudeRange[1] : ",self.flightPhases[altitudeRanges[1]].flightPhaseType)
            print(f"getflightPhaseType({previousAltitude},{currentAltiude}) : {self.getflightPhaseType(previousAltitude,currentAltiude)}")
            
            for altitudeRange in altitudeRanges:
                if self.flightPhases[altitudeRange].flightPhaseType == self.getflightPhaseType(previousAltitude,currentAltiude):
                    print("2nd")
                    return self.flightPhases[altitudeRange] 
        print("none found")
        return None
    
    def getflightPhaseType(self,previousAltitude,currentAltiude):
        if currentAltiude == previousAltitude and 5001 <= currentAltiude <= 41000: 
            self.lastFlightPhaseType=0 
            return 0 #croisière
        elif currentAltiude > previousAltitude and 0 <= currentAltiude <= 5000:
            self.lastFlightPhaseType=1
            return 1 #montée
        elif currentAltiude < previousAltitude and 0 <= currentAltiude <= 4999 :
            self.lastFlightPhaseType=-1
            return -1 #descente
        else : 
            return self.lastFlightPhaseType
        
        

