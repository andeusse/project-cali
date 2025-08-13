from math import gcd
from functools import reduce
from fractions import Fraction
import numpy as np
from scipy.integrate import odeint
from simulation_models.Biogas import ThermoProperties as TP


class BMPModelOffline:
    def __init__ (self, MeasureMethod, ReactorVolume, InitialFreeVolume,
                  SubstrateNumber, MixRule, 
                  Fraction1, Fraction2, Fraction3, Fraction4, WaterFraction,
                  Volume1, Volume2, Volume3, Volume4, WaterVolume,
                  Weight1, Weight2, Weight3, Weight4, WaterWeight,
                  ST1, SV1, rho1, Cc1, Ch1, Co1, Cn1, Cs1,
                  ST2, SV2, rho2, Cc2, Ch2, Co2, Cn2, Cs2,
                  ST3, SV3, rho3, Cc3, Ch3, Co3, Cn3, Cs3,
                  ST4, SV4, rho4, Cc4, Ch4, Co4, Cn4, Cs4,
                  OperationMethod, tp):
        
        self.Thermo = TP.ThermoProperties()
        
        #construction of the plant
        self.MeasureMethod = MeasureMethod
        self.ReactorVolume = ReactorVolume
        self.InitialFreeVolume = InitialFreeVolume
        self.InitialFreeVolumei = self.InitialFreeVolume
        #Substrate information
        self.MixRule = MixRule
        self.SubstrateNumber = SubstrateNumber
        #Estimation by fraction
        self.Fraction1 = Fraction1
        self.Fraction2 = Fraction2
        self.Fraction3 = Fraction3
        self.Fraction4 = Fraction4
        self.WaterFraction = WaterFraction
        #Estimation by Volume
        self.Volume1 = Volume1
        self.Volume2 = Volume2
        self.Volume3 = Volume3
        self.Volume4 = Volume4
        self.WaterVolume = WaterVolume
        #Estimation by weight
        self.Weight1 = Weight1
        self.Weight2 = Weight2
        self.Weight3 = Weight3
        self.Weight4 = Weight4
        self.WaterWeight = WaterWeight
        #Substrate conditions
        #Substrate1
        self.ST1 = ST1/100
        self.SV1 = SV1/100
        self.rho1 = rho1
        self.Cc1 = Cc1
        self.Ch1 = Ch1
        self.Co1 = Co1
        self.Cn1 = Cn1
        self.Cs1 = Cs1
        #Substrate2
        self.ST2 = ST2/100
        self.SV2 = SV2/100
        self.rho2 = rho2
        self.Cc2 = Cc2
        self.Ch2 = Ch2
        self.Co2 = Co2
        self.Cn2 = Cn2
        self.Cs2 = Cs2
        #Substrate3
        self.ST3 = ST3/100
        self.SV3 = SV3/100
        self.rho3 = rho3
        self.Cc3 = Cc3
        self.Ch3 = Ch3
        self.Co3 = Co3
        self.Cn3 = Cn3
        self.Cs3 = Cs3
        #Substrate4
        self.ST4 = ST4/100
        self.SV4 = SV4/100
        self.rho4 = rho4
        self.Cc4 = Cc4
        self.Ch4 = Ch4
        self.Co4 = Co4
        self.Cn4 = Cn4
        self.Cs4 = Cs4
        #Operation Mode
        self.OperationMethod = OperationMethod

        if self.MixRule == "Fraction":
            self.Fraction1 = self.Fraction1
            self.Fraction2 = self.Fraction2
            self.Fraction3 = self.Fraction3
            self.Fraction4 = self.Fraction4
            self.WaterFraction = self.WaterFraction
        
        elif self.MixRule == "Volume":
            Mass1 = self.Volume1 * self.rho1/1000
            Mass2 = self.Volume2 * self.rho2/1000
            Mass3 = self.Volume3 * self.rho3/1000
            Mass4 = self.Volume4 * self.rho4/1000
            MassWater = self.WaterVolume
            
            if self.SubstrateNumber == 1:
                self.Fraction1 = Mass1/(Mass1 + MassWater) * 100 
                self.WaterFraction = MassWater/(Mass1 + MassWater) * 100
            elif self.SubstrateNumber == 2:
                self.Fraction1 = Mass1/(Mass1 + Mass2 + MassWater) * 100 
                self.Fraction2 = Mass2/(Mass1 + Mass2 + MassWater) * 100 
                self.WaterFraction = MassWater/(Mass1 + Mass2 + MassWater) * 100
            elif self.SubstrateNumber == 3:
                self.Fraction1 = Mass1/(Mass1 + Mass2 + Mass3 + MassWater) * 100 
                self.Fraction2 = Mass2/(Mass1 + Mass2 + Mass3 + MassWater) * 100
                self.Fraction3 = Mass3/(Mass1 + Mass2 + Mass3 + MassWater) * 100 
                self.WaterFraction = MassWater/(Mass1 + Mass2 + Mass3 + MassWater) * 100
            elif self.SubstrateNumber == 4:
                self.Fraction1 = Mass1/(Mass1 + Mass2 + Mass3 + Mass4 + MassWater) * 100 
                self.Fraction2 = Mass2/(Mass1 + Mass2 + Mass3 + Mass4 + MassWater) * 100 
                self.Fraction3 = Mass3/(Mass1 + Mass2 + Mass3 + Mass4 + MassWater) * 100
                self.Fraction4 = Mass4/(Mass1 + Mass2 + Mass3 + Mass4 + MassWater) * 100 
                self.WaterFraction = MassWater/(Mass1 + Mass2 + Mass3 + Mass4 + MassWater) * 100
        
        elif self.MixRule == "Weight":
            self.Weight1 = self.Weight1
            self.Weight2 = self.Weight2
            self.Weight3 = self.Weight3
            self.Weight4 = self.Weight4
            self.WaterWeight = self.WaterWeight

            if self.SubstrateNumber == 1:
                self.Fraction1 = self.Weight1/(self.Weight1 + self.WaterFraction) * 100 
                self.WaterFraction = self.WaterWeight/(self.Weight1 + self.WaterWeight) * 100
            elif self.SubstrateNumber == 2:
                self.Fraction1 = self.Weight1/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100 
                self.Fraction2 = self.Weight2/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100 
                self.WaterFraction = self.WaterWeight/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
            elif self.SubstrateNumber == 3:
                self.Fraction1 = self.Weight1/(self.Weight1 + self.Weight2 + self.Weight3 + self.WaterWeight) * 100 
                self.Fraction2 = self.Weight2/(self.Weight1 + self.Weight2 + self.Weight3 + self.WaterWeight) * 100 
                self.Fraction3 = self.Weight3/(self.Weight1 + self.Weight2 + self.Weight3 + self.WaterWeight) * 100 
                self.WaterFraction = self.WaterWeight/(self.Weight1 + self.Weight2 + self.Weight3 + self.WaterWeight) * 100
            elif self.SubstrateNumber == 4:
                self.Fraction1 = self.Weight1/(self.Weight1 + self.Weight2 + self.Weight3 + self.Weight4 + self.WaterWeight) * 100 
                self.Fraction2 = self.Weight2/(self.Weight1 + self.Weight2 + self.Weight3 + self.Weight4 + self.WaterWeight) * 100 
                self.Fraction3 = self.Weight3/(self.Weight1 + self.Weight2 + self.Weight3 + self.Weight4 + self.WaterWeight) * 100 
                self.Fraction4 = self.Weight4/(self.Weight1 + self.Weight2 + self.Weight3 + self.Weight4 + self.WaterWeight) * 100 
                self.WaterFraction = self.WaterWeight/(self.Weight1 + self.Weight2 + self.Weight3 + self.Weight4 + self.WaterWeight) * 100

        #Mixture without dosification
        if self.OperationMethod == "NoDosing":
            if self.SubstrateNumber == 1:
                self.ST_ini = (self.ST1 * self.Fraction1/100)                                       #Total solids decimal 1 substrate diluted
                self.SV_ini = (self.SV1 * self.Fraction1/100)                                       #Total volatile solids decimal 1 substrate diluted
                self.rho_ini = (self.rho1 * self.Fraction1/100 + 1000 * self.WaterFraction/100)     #density of the mixture
                self.Cc = Cc1
                self.Ch = Ch1
                self.Co = Co1
                self.Cn = Cn1
                self.Cs = Cs1
            
            elif self.SubstrateNumber == 2:
                self.ST_ini = (self.ST1 * self.Fraction1/100) + (self.ST2 * self.Fraction2/100)
                self.SV_ini = (self.SV1 * self.Fraction1/100) + (self.SV2 * self.Fraction2/100)
                self.rho_ini = (self.rho1 * self.Fraction1/100) + (self.rho2 * self.Fraction2/100) + (1000 * self.WaterFraction/100)
                gc1 = (Fraction1/100) * Cc1 * (self.ST1); gc2 = (Fraction2/100) * Cc2 * (self.ST2)
                gh1 = (Fraction1/100) * Ch1 * (self.ST1); gh2 = (Fraction2/100) * Ch2 * (self.ST2)
                go1 = (Fraction1/100) * Co1 * (self.ST1); go2 = (Fraction2/100) * Co2 * (self.ST2)
                gn1 = (Fraction1/100) * Cn1 * (self.ST1); gn2 = (Fraction2/100) * Cn2 * (self.ST2)
                gs1 = (Fraction1/100) * Cs1 * (self.ST1); gs2 = (Fraction2/100) * Cs2 * (self.ST2)
                self.Cc = (gc1 + gc2)/self.ST_ini
                self.Ch = (gh1 + gh2)/self.ST_ini
                self.Co = (go1 + go2)/self.ST_ini
                self.Cn = (gn1 + gn2)/self.ST_ini
                self.Cs = (gs1 + gs2)/self.ST_ini
            
            elif self.SubstrateNumber == 3:
                self.ST_ini = (self.ST1 * self.Fraction1/100) + (self.ST2 * self.Fraction2/100) + (self.ST3 * self.Fraction3/100)
                self.SV_ini = (self.SV1 * self.Fraction1/100) + (self.SV2 * self.Fraction2/100) + (self.SV3 * self.Fraction3/100)
                self.rho_ini = (self.rho1 * self.Fraction1/100) + (self.rho2 * self.Fraction2/100) + (self.rho3 * self.Fraction3/100)
                gc1 = (Fraction1/100) * Cc1 * (self.ST1); gc2 = (Fraction2/100) * Cc2 * (self.ST2); gc3 = (Fraction3/100) * Cc3 * (self.ST3)
                gh1 = (Fraction1/100) * Ch1 * (self.ST1); gh2 = (Fraction2/100) * Ch2 * (self.ST2); gh3 = (Fraction3/100) * Ch3 * (self.ST3)
                go1 = (Fraction1/100) * Co1 * (self.ST1); go2 = (Fraction2/100) * Co2 * (self.ST2); go3 = (Fraction3/100) * Co3 * (self.ST3)
                gn1 = (Fraction1/100) * Cn1 * (self.ST1); gn2 = (Fraction2/100) * Cn2 * (self.ST2); gn3 = (Fraction3/100) * Cn3 * (self.ST3)
                gs1 = (Fraction1/100) * Cs1 * (self.ST1); gs2 = (Fraction2/100) * Cs2 * (self.ST2); gs3 = (Fraction3/100) * Cs3 * (self.ST3)
                self.Cc = (gc1 + gc2 + gc3)/self.ST_ini
                self.Ch = (gh1 + gh2 + gh3)/self.ST_ini
                self.Co = (go1 + go2 + go3)/self.ST_ini
                self.Cn = (gn1 + gn2 + gn3)/self.ST_ini
                self.Cs = (gs1 + gs2 + gs3)/self.ST_ini
            
            elif self.SubstrateNumber == 4:
                self.ST_ini = (self.ST1 * self.Fraction1/100) + (self.ST2 * self.Fraction2/100) + (self.ST3 * self.Fraction3/100) + (self.ST4 * self.Fraction4/100)
                self.SV_ini = (self.SV1 * self.Fraction1/100) + (self.SV2 * self.Fraction2/100) + (self.SV3 * self.Fraction3/100) + (self.SV4 * self.Fraction4/100)
                self.rho_ini = (self.rho1 * self.Fraction1/100) + (self.rho2 * self.Fraction2/100) + (self.rho3 * self.Fraction3/100) + (self.rho4 * self.Fraction4/100)
                gc1 = (Fraction1/100) * Cc1 * (self.ST1); gc2 = (Fraction2/100) * Cc2 * (self.ST2); gc3 = (Fraction3/100) * Cc3 * (self.ST3); gc4 = (Fraction4/100) * Cc4 * (self.ST4)
                gh1 = (Fraction1/100) * Ch1 * (self.ST1); gh2 = (Fraction2/100) * Ch2 * (self.ST2); gh3 = (Fraction3/100) * Ch3 * (self.ST3); gh4 = (Fraction4/100) * Ch4 * (self.ST4)
                go1 = (Fraction1/100) * Co1 * (self.ST1); go2 = (Fraction2/100) * Co2 * (self.ST2); go3 = (Fraction3/100) * Co3 * (self.ST3); go4 = (Fraction4/100) * Co4 * (self.ST4)
                gn1 = (Fraction1/100) * Cn1 * (self.ST1); gn2 = (Fraction2/100) * Cn2 * (self.ST2); gn3 = (Fraction3/100) * Cn3 * (self.ST3); gn4 = (Fraction4/100) * Cn4 * (self.ST4)
                gs1 = (Fraction1/100) * Cs1 * (self.ST1); gs2 = (Fraction2/100) * Cs2 * (self.ST2); gs3 = (Fraction3/100) * Cs3 * (self.ST3); gs4 = (Fraction4/100) * Cs4 * (self.ST4)
                self.Cc = (gc1 + gc2 + gc3 + gc4)/self.ST_ini
                self.Ch = (gh1 + gh2 + gh3 + gh4)/self.ST_ini
                self.Co = (go1 + go2 + go3 + go4)/self.ST_ini
                self.Cn = (gn1 + gn2 + gn3 + gn4)/self.ST_ini
                self.Cs = (gs1 + gs2 + gs3 + gs4)/self.ST_ini
            
        elif self.OperationMethod in ["Time", "Injection"]:
            if self.SubstrateNumber == 1:
                self.ST_ini = (self.ST1 * self.Fraction1/100)                                       #Total solids decimal 1 substrate diluted
                self.SV_ini = (self.SV1 * self.Fraction1/100)                                       #Total volatile solids decimal 1 substrate diluted
                self.rho_ini = (self.rho1 * self.Fraction1/100 + 1000 * self.WaterFraction/100)     #density of the mixture
                self.Cc = Cc1
                self.Ch = Ch1
                self.Co = Co1
                self.Cn = Cn1
                self.Cs = Cs1
            
            elif self.SubstrateNumber == 2:
                self.ST_ini = self.ST2
                self.SV_ini = self.SV2
                self.rho_ini = self.rho2
                self.Cc = Cc2
                self.Ch = Ch2
                self.Co = Co2
                self.Cn = Cn2
                self.Cs = Cs2
            
            elif self.SubstrateNumber == 3:
                self.ST_ini = self.ST3
                self.SV_ini = self.SV3
                self.rho_ini = self.rho3
                self.Cc = Cc3
                self.Ch = Ch3
                self.Co = Co3
                self.Cn = Cn3
                self.Cs = Cs3
            
            elif self.SubstrateNumber == 4:
                self.ST_ini = self.ST4
                self.SV_ini = self.SV4
                self.rho_ini = self.rho4
                self.Cc = Cc4
                self.Ch = Ch4
                self.Co = Co4   
                self.Cn = Cn4
                self.Cs = Cs4
            
        self.molC = self.Cc*(1/12.01)
        self.molH = self.Ch*(1/1.01)
        self.molO = self.Co*(1/16)
        self.molN = self.Cn*(1/14)
        self.molS = self.Cs*(1/32)

        def lcm(a,b):
            return a * b // gcd(a, b)
        
        numbers = [self.molC, self.molH, self.molO, self.molN, self.molS]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        self.subindex = [int(num * common_denominator) for num in numbers]

        self.n_ini = self.subindex[0]
        self.a_ini = self.subindex[1]
        self.b_ini = self.subindex[2]
        self.c_ini = self.subindex[3]
        self.d_ini = self.subindex[4]

        self.s_H2O = self.n_ini-(self.a_ini/4)-(self.b_ini/2)+(3/4)*self.c_ini+(self.d_ini/2)
        self.s_CH4 = (self.n_ini/2)+(self.a_ini/8)-(self.b_ini/4)-(3/8)*self.c_ini-(self.d_ini/4)
        self.s_CO2 = (self.n_ini/2)-(self.a_ini/8)+(self.b_ini/4)+(3/8)*self.c_ini-(self.d_ini/4)
        self.s_NH3 = self.c_ini
        self.s_H2S = self.d_ini

        self.MW_sustrato = self.n_ini*12.01+self.a_ini*1.01+self.b_ini*16+self.c_ini*14+self.d_ini*32
        self.Csus_ini_ST_g = (self.rho_ini*self.ST_ini)
        self.Csus_ini_SV_g = (self.rho_ini*self.SV_ini)
        self.Csus_ini_ST_mol = (self.rho_ini*(self.ST_ini))/self.MW_sustrato            #mol/L
        self.Csus_ini_SV_mol = (self.rho_ini*self.SV_ini)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST_mol - self.Csus_ini_SV_mol

        #time for simulation
        self.Globaltime = 0
        self.tp = tp      #seconds

        #Inyections parameters
        self.counterfeed = 0
        self.TotalVolFeed = 0

        #Biogas production reactor
        self.nbiogastotal = 0
        self.nCH4 = 0
        self.nCO2 = 0
        self.nO2 = 0
        self.nH2S = 0
        self.nNH3 = 0
        self.nH2 = 0
        self.C_ini_convertion = self.Csus_ini_SV_mol

        #Pressure methid measurement
        self.nbiogasi=0

        #Mixer variable
        self.countermixing = 0

    def MixtureCalculationFeeding (self):
        if self.SubstrateNumber == 1:
            self.ST = (self.ST1 * self.Fraction1/100)                                       #Total solids decimal 1 substrate diluted
            self.SV = (self.SV1 * self.Fraction1/100)                                       #Total volatile solids decimal 1 substrate diluted
            self.rho = (self.rho1 * self.Fraction1/100 + 1000 * self.WaterFraction/100)     #density of the mixture
            self.Cc = self.Cc1
            self.Ch = self.Ch1
            self.Co = self.Co1
            self.Cn = self.Cn1
            self.Cs = self.Cs1
        
        elif self.SubstrateNumber == 2:
            if self.MixRule == "Fraction":
                self.Fraction1 = self.Fraction1
                self.WaterFraction = 100 - self.Fraction1
            elif self.MixRule == "Volume":
                Mass1 = self.Volume1 * self.rho1/1000
                MassWater = self.WaterVolume
                self.Fraction1 = Mass1/(Mass1 + MassWater) * 100
                self.WaterFraction = 100 - self.Fraction1
            elif self.MixRule == "Weight":
                self.Fraction1 = self.Weight1/(self.Weight1 + self.WaterWeight) * 100
                self.WaterFraction = 100 - self.Fraction1

            self.ST = (self.ST1 * self.Fraction1/100)
            self.SV = (self.SV1 * self.Fraction1/100)
            self.rho = (self.Fraction1/100 * self.rho1 + self.WaterFraction/100 * 1000)
            self.Cc = self.Cc1
            self.Ch = self.Ch1
            self.Co = self.Co1
            self.Cn = self.Cn1
            self.Cs = self.Cs1
        
        elif self.SubstrateNumber ==3:
            if self.MixRule == "Fraction":
                self.Fraction1 = self.Fraction1
                self.Fraction2 = self.Fraction2
                self.WaterFraction = 100 - self.Fraction1 - self.Fraction2
            elif self.MixRule == "Volume":
                Mass1 = self.Volume1 * self.rho1/1000
                Mass2 = self.Volume2 * self.rho2/1000
                MassWater = self.WaterVolume
                self.Fraction1 = Mass1/(Mass1 + Mass2 + MassWater) * 100
                self.Fraction2 = Mass2/(Mass1 + Mass2 + MassWater) * 100
                self.WaterFraction = MassWater/(Mass1 + Mass2 + MassWater) * 100
            elif self.MixRule == "Weight":
                self.Weight1 = self.Weight1
                self.Weight2 = self.Weight2
                self.WaterWeight = self.WaterWeight
                self.Fraction1 = self.Weight1/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
                self.Fraction2 = self.Weight2/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
                self.WaterFraction = self.WaterWeight/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
            
            self.ST = self.ST1 * (self.Fraction1/100) + self.ST2 * (self.Fraction2/100)
            self.SV = self.SV1 * (self.Fraction1/100) + self.SV2 * (self.Fraction2/100)
            self.rho = self.rho1 * (self.Fraction1/100) + self.rho2 * (self.Fraction2/100) + 1000 * (self.WaterFraction/100)
            
            gc1 = (self.Fraction1/100) * self.Cc1 * (self.ST1); gc2 = (self.Fraction2/100) * self.Cc2 * (self.ST2)
            gh1 = (self.Fraction1/100) * self.Ch1 * (self.ST1); gh2 = (self.Fraction2/100) * self.Ch2 * (self.ST2)
            go1 = (self.Fraction1/100) * self.Co1 * (self.ST1); go2 = (self.Fraction2/100) * self.Co2 * (self.ST2)
            gn1 = (self.Fraction1/100) * self.Cn1 * (self.ST1); gn2 = (self.Fraction2/100) * self.Cn2 * (self.ST2)
            gs1 = (self.Fraction1/100) * self.Cs1 * (self.ST1); gs2 = (self.Fraction2/100) * self.Cs2 * (self.ST2)

            self.Cc = (gc1 + gc2)/self.ST
            self.Ch = (gh1 + gh2)/self.ST
            self.Co = (go1 + go2)/self.ST
            self.Cn = (gn1 + gn2)/self.ST
            self.Cs = (gs1 + gs2)/self.ST
        
        elif self.SubstrateNumber == 4:
            if self.MixRule == "Fraction":
                self.Fraction1 = self.Fraction1
                self.Fraction2 = self.Fraction2
                self.Fraction3 = self.Fraction3
                self.WaterFraction = 100 - self.Fraction1 - self.Fraction2 - self.Fraction3
            elif self.MixRule == "Volume":
                Mass1 = self.Volume1 * self.rho1/1000
                Mass2 = self.Volume2 * self.rho2/1000
                Mass3 = self.Volume3 * self.rho3/1000
                MassWater = self.WaterVolume
                self.Fraction1 = Mass1/(Mass1 + Mass2 + Mass3 + MassWater) * 100
                self.Fraction2 = Mass2/(Mass1 + Mass2 + Mass3 + MassWater) * 100
                self.Fraction3 = Mass3/(Mass1 + Mass2 + Mass3 + MassWater) * 100
                self.WaterFraction = MassWater/(Mass1 + Mass2 + Mass3 + MassWater) * 100
            elif self.MixRule == "Weight":
                self.Weight1 = self.Weight1
                self.Weight2 = self.Weight2
                self.Weight3 = self.Weight3
                self.WaterWeight = self.WaterWeight
                self.Fraction1 = self.Weight1/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
                self.Fraction2 = self.Weight2/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
                self.Fraction3 = self.Weight3/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
                self.WaterFraction = self.WaterWeight/(self.Weight1 + self.Weight2 + self.WaterWeight) * 100
            
            self.ST = self.ST1 * (self.Fraction1/100) + self.ST2 * (self.Fraction2/100) + self.ST3 * (self.Fraction3/100)
            self.SV = self.SV1 * (self.Fraction1/100) + self.SV2 * (self.Fraction2/100) + self.SV3 * (self.Fraction3/100)
            self.rho = self.rho1 * (self.Fraction1/100) + self.rho2 * (self.Fraction2/100) + self.rho3 * (self.Fraction3/100) + 1000 * (self.WaterFraction/100)

            gc1 = (self.Fraction1/100) * self.Cc1 * (self.ST1); gc2 = (self.Fraction2/100) * self.Cc2 * (self.ST2); gc3 = (self.Fraction3/100) * self.Cc3 * (self.ST3)
            gh1 = (self.Fraction1/100) * self.Ch1 * (self.ST1); gh2 = (self.Fraction2/100) * self.Ch2 * (self.ST2); gh3 = (self.Fraction3/100) * self.Ch3 * (self.ST3)
            go1 = (self.Fraction1/100) * self.Co1 * (self.ST1); go2 = (self.Fraction2/100) * self.Co2 * (self.ST2); go3 = (self.Fraction3/100) * self.Co3 * (self.ST3)
            gn1 = (self.Fraction1/100) * self.Cn1 * (self.ST1); gn2 = (self.Fraction2/100) * self.Cn2 * (self.ST2); gn3 = (self.Fraction3/100) * self.Cn3 * (self.ST3)
            gs1 = (self.Fraction1/100) * self.Cs1 * (self.ST1); gs2 = (self.Fraction2/100) * self.Cs2 * (self.ST2); gs3 = (self.Fraction3/100) * self.Cs3 * (self.ST3)

            self.Cc = (gc1 + gc2 + gc3)/self.ST
            self.Ch = (gh1 + gh2 + gh3)/self.ST
            self.Co = (go1 + go2 + go3)/self.ST
            self.Cn = (gn1 + gn2 + gn3)/self.ST
            self.Cs = (gs1 + gs2 + gs3)/self.ST

        self.molC = self.Cc*(1/12.01)
        self.molH = self.Ch*(1/1.01)
        self.molO = self.Co*(1/16)
        self.molN = self.Cn*(1/14)
        self.molS = self.Cs*(1/32)

        def lcm(a,b):
            return a * b // gcd(a, b)
        
        numbers = [self.molC, self.molH, self.molO, self.molN, self.molS]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        self.subindex = [int(num * common_denominator) for num in numbers]

        self.n = self.subindex[0]
        self.a = self.subindex[1]
        self.b = self.subindex[2]
        self.c = self.subindex[3]
        self.d = self.subindex[4]

        self.s_H2O = self.n-(self.a/4)-(self.b/2)+(3/4)*self.c+(self.d/2)
        self.s_CH4 = (self.n/2)+(self.a/8)-(self.b/4)-(3/8)*self.c-(self.d/4)
        self.s_CO2 = (self.n/2)-(self.a/8)+(self.b/4)+(3/8)*self.c-(self.d/4)
        self.s_NH3 = self.c
        self.s_H2S = self.d

        self.MW_sustrato = self.n*12.01+self.a*1.01+self.b*16+self.c*14+self.d*32
        self.Csus_ST_g = (self.rho*self.ST)
        self.Csus_SV_g = (self.rho*self.SV)
        self.Csus_ST_mol = (self.rho*(self.ST))/self.MW_sustrato            #mol/L
        self.Csus_SV_mol = (self.rho*self.SV_ini)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ST_mol - self.Csus_SV_mol
    
    
    def SubstrateFeed (self, Mode = "Time", Volume = 50, Time = 4, Inyections = 4, Q=1, speed_time = 1):  #from frontend requieres add entrance vble for sideA and SideB
        self.Volume_feed = Volume  #mL
        self.speed_time = speed_time
        if Mode == "Time":
            TimeFeed = (Volume/Q)*60
            self.TimeFeed = TimeFeed
            if self.counterfeed < TimeFeed:
                self.Qr = Q
                self.TotalVolFeed = self.TotalVolFeed + self.Qr*((TimeFeed)/60)  
            else:
                self.Qr = 0
                self.TotalVolFeed = self.TotalVolFeed
            self.counterfeed = self.counterfeed + (self.tp*speed_time)
            if self.counterfeed > Time*3600:
                self.counterfeed = 0
            

        elif Mode == "Injection":
            IntervalTimeInyection = 24/Inyections
            TimeFeed = (Volume/Q)*60
            self.TimeFeed = TimeFeed
            if self.counterfeed < TimeFeed:
                self.Qr = Q
                self.TotalVolFeed = self.TotalVolFeed + self.Qr*(TimeFeed/60) 
            else:
                self.Qr = 0
                self.TotalVolFeed = self.TotalVolFeed 
            self.counterfeed = self.counterfeed + (self.tp * speed_time)
            if self.counterfeed > IntervalTimeInyection*3600:
                self.counterfeed = 0 
             
            
        elif Mode == "NoDosing":
            self.Qr = 0
            self.TotalVolFeed = 0
            self.TotalVolFeed = 0
            self.TimeFeed = 0

    def MixControl (self, MixVelocity, MixTime, DailyMixing, speed_time):
        self.MixTime = MixTime*60
        TimeInterval = 24/DailyMixing
        self.speed_time = speed_time

        if self.countermixing < self.MixTime:
            self.MixVelocity = MixVelocity
        else:
            self.MixVelocity = 0
        
        if self.countermixing > TimeInterval*3600:
            self.countermixing = 0

        self.countermixing = self.countermixing + (self.tp*self.speed_time)
        
    def Reactor (self, model, OperationMethod, T, K1, K2=1, K3=1, speed_time = 1):
        self.speed_time = speed_time
        def model_Arrhenius(C, t, K, Ea, VR, T_func, Csus_in_func_1 = 0, Q_func_1 = 0, Operation = 1):
            R = 8.314
            T=T_func
            Csus_in_1 = Csus_in_func_1
            Q_1 = Q_func_1
                    
            if Operation == 1:         #One entrance without recirculation
                dCsus_dt = - (C * K * np.exp(-(Ea)/(R*T))) / VR
            elif Operation == 2:       #Two entrances with differents concentrations
                dCsus_dt = ((Q_1 / VR) * (Csus_in_1 - C)) - (C * K * np.exp(-(Ea)/(R*T))) / VR
            return dCsus_dt

        def model_ADM1(C, t, K, VR, Csus_in_func_1 = 0, Q_func_1 = 0, Operation = 1):
            Csus_in_1 = Csus_in_func_1
            Q_1 = Q_func_1
                    
            if Operation == 1:         #One entrance without recirculation
                dCsus_dt = - (C * K) / VR
            elif Operation == 2:       #Two entrances with differents concentrations
                dCsus_dt = ((Q_1 / VR) * (Csus_in_1 - C)) - (C * K) / VR
            return dCsus_dt

        def model_Gompertz(t, ym, U, L):
            t = np.array(t, dtype = float)
            y_t = ym * np.exp(-np.exp(((U*np.e)/ym)*(L-t)+1))
            return y_t
        
        Pstd = 100000                                              #Pa
        Tstd = 273.15                                              #K
        time_sim = [self.Globaltime, self.Globaltime + self.tp*self.speed_time]
        if model == "Arrhenius":
            if OperationMethod in ["Time", "Injection"]:
                self.Csus_ini_SV_molv = odeint(model_Arrhenius, y0 = self.Csus_ini_SV_mol, t=time_sim, args=(K1, K2, self.ReactorVolume/1000, T, self.Csus_SV_mol, self.Qr/60, 2))
                self.Csus_ini_SV_mol = self.Csus_ini_SV_molv[-1]
                if self.Globaltime == 0:
                    self.DCsus_ini_SV_mol = 0
                else:
                    self.DCsus_ini_SV_mol  = self.Csus_ini_SV_molv[-1] - self.Csus_ini_SV_molv[0]
                self.SV_int = (self.Csus_ini_SV_mol/self.rho)*self.MW_sustrato
                self.ST_int = ((self.Csus_ini_SV_mol+self.Csus_fixed)/self.rho)*self.MW_sustrato
                self.OC = self.Csus_ini_SV_mol/(self.Globaltime/86400)
            else:
                self.Csus_ini_SV_molv = odeint(model_Arrhenius, y0 = self.Csus_ini_SV_mol, t=time_sim, args=(K1, K2, self.ReactorVolume/1000, T, 0, 0, 1))
                self.Csus_ini_SV_mol = self.Csus_ini_SV_molv[-1]
                if self.Globaltime == 0:
                    self.DCsus_ini_SV_mol = 0
                else:
                    self.DCsus_ini_SV_mol  = self.Csus_ini_SV_molv[-1] - self.Csus_ini_SV_molv[0]
                
                self.SV_int = (self.Csus_ini_SV_mol/self.rho_ini)*self.MW_sustrato
                self.ST_int = ((self.Csus_ini_SV_mol+self.Csus_fixed)/self.rho_ini)*self.MW_sustrato
                self.OC = self.Csus_ini_SV_mol/(self.Globaltime/86400)

        elif model == "ADM1":
            if OperationMethod in ["Time", "Injection"]:
                self.Csus_ini_SV_molv = odeint(model_ADM1, y0 = self.Csus_ini_SV_mol, t=time_sim, args=(K1, self.ReactorVolume/1000, self.Csus_SV_mol, self.Qr/60, 2))
                self.Csus_ini_SV_mol = self.Csus_ini_SV_molv[-1]
                if self.Globaltime == 0:
                    self.DCsus_ini_SV_mol = 0
                else:
                    self.DCsus_ini_SV_mol  = self.Csus_ini_SV_molv[-1] - self.Csus_ini_SV_molv[0]
                self.SV_int = (self.Csus_ini_SV_mol/self.rho)*self.MW_sustrato
                self.ST_int = ((self.Csus_ini_SV_mol+self.Csus_fixed)/self.rho)*self.MW_sustrato
                self.OC = self.Csus_ini_SV_mol/(self.Globaltime/86400)
                
            else:
                self.Csus_ini_SV_molv = odeint(model_ADM1, y0 = self.Csus_ini_SV_mol, t=time_sim, args=(K1, self.ReactorVolume/1000, 0, 0, 1))
                self.Csus_ini_SV_mol = self.Csus_ini_SV_molv[-1]
                if self.Globaltime == 0:
                    self.DCsus_ini_SV_mol = 0
                else:
                    self.DCsus_ini_SV_mol  = self.Csus_ini_SV_molv[-1] - self.Csus_ini_SV_molv[0]
                self.SV_int = (self.Csus_ini_SV_mol/self.rho_ini)*self.MW_sustrato
                self.ST_int = ((self.Csus_ini_SV_mol+self.Csus_fixed)/self.rho_ini)*self.MW_sustrato
                self.OC = self.Csus_ini_SV_mol/(self.Globaltime/86400)
        
        elif model == "Gompertz":
            time_sim = [self.Globaltime/86400, (self.Globaltime + self.tp*self.speed_time)/86400]
            y_tv = model_Gompertz(time_sim, K1, K2, K3)
            y_t = float(y_tv[0])
            
            self.gSV = self.Csus_ini_SV_g * self.ReactorVolume/1000    #grams of volatile solids 
            
            self.Vnormalbiogasv = y_tv * self.gSV
            self.Vnormalbiogas = y_t * self.gSV

            self.nbiogasv =  (Pstd * self.Vnormalbiogasv/1000000)/(8.314 * Tstd)
            self.nbiogas = (Pstd * self.Vnormalbiogas/1000000)/(8.314 * Tstd)
            
            self.s_O2 = self.s_CH4 * np.random.uniform(0.001, 0.0015)
            self.s_H2 = self.s_CH4 * np.random.uniform(0.0000001, 0.00000015)
            self.s_biogas = self.s_CH4 + self.s_CO2 + self.s_H2S + self.s_O2 + self.s_H2
            
            self.xCH4 = self.s_CH4/self.s_biogas
            self.xCO2 = self.s_CO2/self.s_biogas
            self.xH2S = self.s_H2S/self.s_biogas
            self.xO2 = self.s_O2/self.s_biogas
            self.xH2 = self.s_H2/self.s_biogas
            
            self.nCH4v = self.nbiogasv * self.xCH4
            self.nCO2v = self.nbiogasv * self.xCO2
            self.nH2Sv = self.nbiogasv * self.xH2S
            self.nO2v = self.nbiogasv * self.xO2
            self.nH2v = self.nbiogasv * self.xH2
            
            self.DnCH4 = abs(self.nCH4v[-1] - self.nCH4v[0])
            self.DnCO2 = abs(self.nCO2v[-1] - self.nCO2v[0])
            self.DnH2S = abs(self.nH2Sv[-1] - self.nH2Sv[0])
            self.DnO2 = abs(self.nO2v[-1] - self.nO2v[0])
            self.DnH2 = abs(self.nH2v[-1] - self.nH2v[0])

            self.nCH4 = self.nbiogas * self.xCH4
            self.nCO2 = self.nbiogas * self.xCO2
            self.nH2S = self.nbiogas * self.xH2S
            self.nO2 = self.nbiogas * self.xO2
            self.nH2 = self.nbiogas * self.xH2
            self.nbiogas = self.nCH4 + self.nCO2 + self.nH2S + self.nO2 + self.nH2

            self.DCsus_ini_SV_mol = self.DnCH4 * (1/self.s_CH4)
            self.Csus_ini_SV_mol = self.Csus_ini_SV_mol - self.DnCH4 * (1/self.s_CH4)
            self.Csus_ini_ST_mol = self.Csus_ini_ST_mol - self.DnCH4 * (1/self.s_CH4)
            self.x = (self.C_ini_convertion - self.Csus_ini_SV_mol)/self.C_ini_convertion

            self.PBM = (self.Vnormalbiogas * self.xCH4)/self.gSV  

            self.SV_int = (self.Csus_ini_SV_mol/self.rho_ini)*self.MW_sustrato  
            self.ST_int = (self.Csus_ini_ST_mol/self.rho_ini)*self.MW_sustrato  
            self.OC = self.Csus_ini_SV_mol/(self.Globaltime/86400)     

        if model in ["Arrhenius", "ADM1"]:
            if OperationMethod == "NoDosing":
                
                self.gSV = self.C_ini_convertion * self.ReactorVolume/1000    #grams of volatile solids

                self.x = (self.C_ini_convertion - self.Csus_ini_SV_mol)/self.C_ini_convertion
                self.nCH4 = self.nCH4 + abs(self.DCsus_ini_SV_mol)*(self.s_CH4)*(self.ReactorVolume/1000)
                self.nCO2 = self.nCO2 + abs(self.DCsus_ini_SV_mol)*(self.s_CO2)*(self.ReactorVolume/1000)
                self.nH2S = self.nH2S + abs(self.DCsus_ini_SV_mol)*(self.s_H2S)*(self.ReactorVolume/1000)
                self.nNH3 = self.nNH3 + abs(self.DCsus_ini_SV_mol)*(self.s_NH3)*(self.ReactorVolume/1000)
                self.nO2 = self.nCH4 * np.random.uniform(0.001, 0.0015)
                self.nH2 = self.nCH4 * np.random.uniform(0.0000001, 0.00000015)
                self.nbiogas = self.nCH4 + self.nCO2 + self.nH2S + self.nO2 + self.nH2
                
                try:
                    self.xCH4 = self.nCH4/self.nbiogas
                except ZeroDivisionError:
                    self.xCH4 = 0
                try:
                    self.xCO2 = self.nCO2/self.nbiogas
                except ZeroDivisionError:
                    self.xCO2 = 0
                try:
                    self.xH2S = self.nH2S/self.nbiogas
                except ZeroDivisionError:
                    self.xH2S = 0
                try:
                    self.xO2 = self.nO2/self.nbiogas
                except ZeroDivisionError:
                    self.xO2 = 0
                try:
                    self.xH2 = self.nH2/self.nbiogas
                except ZeroDivisionError:
                    self.xH2 = 0

                self.Vnormalbiogas_m3 = (self.nbiogas * 8.314 * Tstd)/Pstd
                self.Vnormalbiogas = self.Vnormalbiogas_m3*1000000

                self.PBM = (self.Vnormalbiogas * self.xCH4)/self.gSV

            else:

                self.gSV = self.Csus_ini_SV_mol * self.ReactorVolume/1000 
                self.x = (self.Csus_SV_mol - self.Csus_ini_SV_mol)/self.Csus_SV_mol
                self.nCH4 = self.nCH4 + abs(self.DCsus_ini_SV_mol)*(self.s_CH4)*(self.ReactorVolume/1000)
                self.nCO2 = self.nCO2 + abs(self.DCsus_ini_SV_mol)*(self.s_CO2)*(self.ReactorVolume/1000)
                self.nH2S = self.nH2S + abs(self.DCsus_ini_SV_mol)*(self.s_H2S)*(self.ReactorVolume/1000)
                self.nNH3 = self.nNH3 + abs(self.DCsus_ini_SV_mol)*(self.s_NH3)*(self.ReactorVolume/1000)
                self.nO2 = self.nCH4 * np.random.uniform(0.001, 0.0015)
                self.nH2 = self.nCH4 * np.random.uniform(0.0000001, 0.00000015)
                self.nbiogas = self.nCH4 + self.nCO2 + self.nH2S + self.nO2 + self.nH2

                try:
                    self.xCH4 = self.nCH4/self.nbiogas
                except ZeroDivisionError:
                    self.xCH4 = 0
                try:
                    self.xCO2 = self.nCO2/self.nbiogas
                except ZeroDivisionError:
                    self.xCO2 = 0
                try:
                    self.xH2S = self.nH2S/self.nbiogas
                except ZeroDivisionError:
                    self.xH2S = 0
                try:
                    self.xO2 = self.nO2/self.nbiogas
                except ZeroDivisionError:
                    self.xO2 = 0
                try:
                    self.xH2 = self.nH2/self.nbiogas
                except ZeroDivisionError:
                    self.xH2 = 0

                self.Vnormalbiogas_m3 = (self.nbiogas * 8.314 * Tstd)/Pstd
                self.Vnormalbiogas = self.Vnormalbiogas_m3*1000000

                self.PBM = (self.Vnormalbiogas * self.xCH4)/self.gSV

        
    def Measurement_by_pressure(self, T, Pset):   #Temperature in Celsius        
        self.InitialFreeVolume = self.InitialFreeVolume - self.Qr*(self.TimeFeed/60)
        if self.InitialFreeVolume < self.ReactorVolume:
            self.InitialFreeVolume = self.InitialFreeVolumei
        
        #Storage pressure
        self.nbiogasp = self.nbiogas - self.nbiogasi
        self.P_pascal = self.nbiogasp*8.314*(T+273.15)/(self.InitialFreeVolume/1000000)
        self.P_psi = self.P_pascal/6894.76
        
        #Accumulated pressure
        self.P_acum_pa = self.nbiogas*8.314*(T+273.15)/(self.InitialFreeVolume/1000000)
        self.P_acum_psi = self.P_acum_pa/6894.76

        if self.P_psi>Pset:
            self.nbiogasi = self.nbiogas
        
        self.hpool_mm = 0
    
    def Measument_by_volume(self, T, hmax, hmin, Apool):   #Temperature in Celsius
        self.InitialFreeVolume = self.InitialFreeVolume - self.Qr*(self.TimeFeed/60)
        if self.InitialFreeVolume < self.ReactorVolume:
            self.InitialFreeVolume = self.InitialFreeVolumei
        
        #Storage pressure
        self.nbiogasp = self.nbiogas - self.nbiogasi
        self.P_pascal = self.nbiogasp*8.314*(T+273.15)/(self.InitialFreeVolume/1000000)
        self.P_psi = self.P_pascal/6894.76
        self.hpool = self.P_pascal/(1000*9.81)   #m
        self.hpool_mm = self.hpool*1000          #mm

        #Accumulated pressure
        self.P_acum_pa = self.nbiogas*8.314*(T+273.15)/(self.InitialFreeVolume/1000000)
        self.P_acum_psi = self.P_acum_pa/6894.76
        
        if self.hpool_mm > hmax:
            self.nbiogasi = self.nbiogas


    def GlobaltimeCounter(self):
        self.Globaltime = self.Globaltime + (self.tp * self.speed_time) 