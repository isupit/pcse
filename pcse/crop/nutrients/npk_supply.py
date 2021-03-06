#!/usr/bin/env python

from ...decorators import prepare_rates, prepare_states
from ...base_classes import StatesTemplate, ParamTemplate, SimulationObject
from ...traitlets import Float

class npk_supply_storage_organs(SimulationObject):
    
    class Parameters(ParamTemplate):
        TCNT  = Float(-99.) # time coefficient for N translocation to storage organs [days]
        TCPT  = Float(-99.) # time coefficient for P translocation to storage organs [days]
        TCKT  = Float(-99.) # time coefficient for K translocation to storage organs [days]
        DVSNT = Float(-99.) # development stage above which N-P-K translocation to storage organs does occur 
    
    class StateVariables(StatesTemplate):
        NUPSO = Float(-99.) # N amount that can be translocated to the storage organs [kg N ha-1]
        PUPSO = Float(-99.) # P amount that can be translocated to the storage organs [kg P ha-1]
        KUPSO = Float(-99.) # K amount that can be translocated to the storage organs [kg K ha-1]
       
    def initialize(self, day, kiosk, cropdata):
        """
        :param day: start date of the simulation
        :param kiosk: variable kiosk of this PyWOFOST instance
        :param cropdata: dictionary with WOFOST cropdata key/value pairs
        :returns: nutrient supply to storage organs __call__()
        """

        self.params = self.Parameters(cropdata)
        self.states  = self.StateVariables(kiosk,publish=["NUPSO","PUPSO","KUPSO"],
                                           NUPSO=0.,PUPSO=0.,KUPSO=0.)
    
    @prepare_states
    def integrate(self, day):
        states = self.states
        params = self.params
        
#       published rates from the kiosk
#       total amount of translocatable NPK
        ATNLV  = self.kiosk["ATNLV"]
        ATNST  = self.kiosk["ATNST"]
        ATNRT  = self.kiosk["ATNRT"]
        
        ATPLV  = self.kiosk["ATPLV"]
        ATPST  = self.kiosk["ATPST"]
        ATPRT  = self.kiosk["ATPRT"]
        
        ATKLV  = self.kiosk["ATKLV"]
        ATKST  = self.kiosk["ATKST"]
        ATKRT  = self.kiosk["ATKRT"]

        DVS = self.kiosk["DVS"] 
        
#       total translocatable NPK amount in the organs [kg N ha-1]
        ATN   = ATNLV + ATNST + ATNRT
        ATP   = ATPLV + ATPST + ATPRT
        ATK   = ATKLV + ATKST + ATKRT
        
        # NPK amount that can be translocated to the storage organs [kg N ha-1]
        # translocation occurs after DVSNT
        if DVS > params.DVSNT:
            states.NUPSO = ATN/params.TCNT
            states.PUPSO = ATP/params.TCPT
            states.KUPSO = ATK/params.TCKT
        else:
            states.NUPSO = states.PUPSO= states.KUPSO = 0.
        
        
        

