from tools import DBManager
from math import gcd
from fractions import Fraction
from functools import reduce
import pandas as pd
import datetime
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st

class BMP_online:
    def __init__ (self, DB_IP, DB_Port, DB_Organization, DB_Bucket, DB_Token,
                  MeasureMethod, ReactorVolume, InitialFreeVolume,
                  SubstrateNumber, MixRule, 
                  Fraction1, Fraction2, Fraction3, Fraction4, WaterFraction,
                  Volume1, Volume2, Volume3, Volume4, WaterVolume,
                  Weight1, Weight2, Weight3, Weight4, WaterWeight,
                  ST1, SV1, rho1, Cc1, Ch1, Co1, Cn1, Cs1,
                  ST2, SV2, rho2, Cc2, Ch2, Co2, Cn2, Cs2,
                  ST3, SV3, rho3, Cc3, Ch3, Co3, Cn3, Cs3,
                  ST4, SV4, rho4, Cc4, Ch4, Co4, Cn4, Cs4,
                  OperationMethod, Model):
        
        self.influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
        self.connectionState = self.influxDB.InfluxDBconnection()
        if not self.connectionState:
            raise ConnectionError(f"Database connection failed: {self.influxDB.ERROR_MESSAGE}")
        
        #construction of the plant
        self.MeasureMethod = MeasureMethod
        self.ReactorVolume = ReactorVolume
        self.InitialFreeVolume = InitialFreeVolume
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

        #Initital values for optimization
        if Model == "Arrhenius":
            self.K_ini_R101 = 1
            self.Ea_ini_R101 = 1
            self.K_ini_R102 = 1
            self.Ea_ini_R102 = 1
            self.K_ini_R103 = 1
            self.Ea_ini_R103 = 1
            self.K_ini_R104 = 1
            self.Ea_ini_R104 = 1

    
    def SubstrateFeeding (self):
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
    
    def GetData(self, SideA, SideB, TrainTime):

        if SideA == True:
            attempts = 1
            while attempts <= 5:
                try:
                    self.query1 = self.influxDB.QueryCreator(measurement="Planta_PBM", train_time=TrainTime, type=12)
                    df_last = self.influxDB.InfluxDBreader(query = self.query1)
                    last_time = df_last["_time"].max()
                    t_end = last_time.to_pydatetime().astimezone(datetime.timezone.utc)
                    t_start = t_end - datetime.timedelta(minutes=TrainTime)

                    t_end_str = t_end.isoformat(timespec="milliseconds").replace('+00:00', 'Z') 
                    t_start_str = t_start.isoformat(timespec="milliseconds").replace('+00:00', 'Z')
                    self.query2 = self.influxDB.QueryCreator(measurement="Planta_PBM", t_start_str = t_start_str, t_end_str = t_end_str, type=13)
                    self.PlantSideA = self.influxDB.InfluxDBreader(query = self.query2)
                    self.PlantSideA.set_index("_field", inplace = True)
                    break
                except Exception as e:
                    print(f"Try {attempts} failed: {e}")
                    attempts += 1
                    print("Try", attempts)

        if SideB == True:
            attempts = 1
            while attempts <= 5:
                try:
                    self.query3 = self.influxDB.QueryCreator(measurement="Planta_PBM", train_time=TrainTime, type=14)
                    df_last = self.influxDB.InfluxDBreader(query = self.query3)
                    last_time = df_last["_time"].max()
                    t_end = last_time.to_pydatetime().astimezone(datetime.timezone.utc)
                    t_start = t_end - datetime.timedelta(minutes=TrainTime)

                    t_end_str = t_end.isoformat(timespec="milliseconds").replace('+00:00', 'Z') 
                    t_start_str = t_start.isoformat(timespec="milliseconds").replace('+00:00', 'Z')
                    self.query4 = self.influxDB.QueryCreator(measurement="Planta_PBM", t_start_str = t_start_str, t_end_str = t_end_str, type=15)
                    self.PlantSideB = self.influxDB.InfluxDBreader(query = self.query4)
                    self.PlantSideB.set_index("_field", inplace = True)
                    break
                except Exception as e:
                    print(f"Try {attempts} failed: {e}")
                    attempts += 1
                    print("Try", attempts)
        
        attempts = 1
        while attempts <= 5:
            try:
                self.query5 = self.influxDB.QueryCreator(measurement="Planta_PBM", train_time=TrainTime, type=16)
                df_last = self.influxDB.InfluxDBreader(query=self.query5)
                #df_last = pd.concat(self.influxDB.InfluxDBreader(query = self.query5), ignore_index=True)
                #df_last = pd.DataFrame(self.influxDB.InfluxDBreader(query = self.query5))
                last_time = df_last["_time"].max()
                t_end = last_time.to_pydatetime().astimezone(datetime.timezone.utc)
                t_start = t_end - datetime.timedelta(minutes=TrainTime)

                t_end_str = t_end.isoformat(timespec="milliseconds").replace('+00:00', 'Z') 
                t_start_str = t_start.isoformat(timespec="milliseconds").replace('+00:00', 'Z')
                self.query6 = self.influxDB.QueryCreator(measurement="Planta_PBM", t_start_str = t_start_str, t_end_str = t_end_str, type=17)
                self.PlantEstimation = self.influxDB.InfluxDBreader(query = self.query6)
                # self.PlantEstimation = pd.concat(self.influxDB.InfluxDBreader(query = self.query6), ignore_index=True)
                self.PlantEstimation.set_index("_field", inplace = True)
                break
            except Exception as e:
                print(f"Try {attempts} failed: {e}")
                attempts += 1
                print("Try", attempts)

        # self.PlantSideA.to_csv(r'.\DataTestPBM\TrainDataSideA.csv')
        # self.PlantSideB.to_csv(r'.\DataTestPBM\TrainDataSideB.csv')
        # self.PlantEstimation.to_csv(r'.\DataTestPBM\EstimatedValues.csv')
    
    def ProcessData(self, SideA, SideB, MeasureMethodSideA, MeasureMethodSideB, DataPlantSideA, DataPlantSideB,  DataEstimation,
                    OperationMethod): 
        
        #Function to normalice time
        def normaliceTime (time):
            #check the lenght of the vector
            try: 
                if len(time) > 1:
                    time_norm = []
                    for i in range (len(time)):
                        time_diff = time.iloc[i] - time.iloc[0]
                        time_diff = time_diff.total_seconds()/60
                        time_norm.append(time_diff)
                else: 
                    time_norm = []
                    time_norm.append(0)
            except TypeError as e:
                time_norm = []
                time_norm.append(0)
            return time_norm
        
        #Side A
        if SideA == True:
            #%%Reactor 101
            TempR101 = DataPlantSideA.loc["TE-101A", ["_time", "_value"]]
            pHR101 = DataPlantSideA.loc["AT-101", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-111", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R101
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR101 = DataEstimation.loc["PTotalR101", ["_time", "_value"]]
                    VolAcumR101 = DataEstimation.loc["Volumen_bioR101_Pressure", ["_time", "_value"]]
                    TempGasR101 = DataPlantSideA.loc["TE-101B", ["_time", "_value"]]
                    xCH4R101 = DataPlantSideA.loc["CH4-101", ["_time", "_value"]]
                    xCO2R101 = DataPlantSideA.loc["CO2-101", ["_time", "_value"]]
                    xO2R101 = DataPlantSideA.loc["O2-101", ["_time", "_value"]]
                    xH2SR101 = DataPlantSideA.loc["H2S-101", ["_time", "_value"]]
                    xH2R101 = DataPlantSideA.loc["H2-101", ["_time", "_value"]]
                    EnergiaR101 = DataEstimation.loc["Energia_mWhR101_Pressure", ["_time", "_value"]]
                    
                    DataR101 = [Inyections, AcumPressureR101, VolAcumR101, TempGasR101, xCH4R101, xCO2R101,
                                xO2R101, xH2SR101, xH2R101, EnergiaR101, TempR101, pHR101]
                    Columns_names = ["Inyections", "AcumPressureR101", "VolAcumR101", "TempGasR101", "xCH4R101", "xCO2R101",
                                "xO2R101", "xH2SR101", "xH2R101", "EnergiaR101", "TempR101", "pHR101"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR101 = DataEstimation.loc["VacumA", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR101 = DataEstimation.loc["TE-100A", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR101 = DataEstimation.loc["PT-100A", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R101 = DataPlantSideA.loc["CH4-101", ["_time", "_value"]]
                    xCO2R101 = DataPlantSideA.loc["CO2-101", ["_time", "_value"]]
                    xO2R101 = DataPlantSideA.loc["O2-101", ["_time", "_value"]]
                    xH2SR101 = DataPlantSideA.loc["H2S-101", ["_time", "_value"]]
                    xH2R101 = DataPlantSideA.loc["H2-101", ["_time", "_value"]]
                    EnergiaR101 = DataEstimation.loc["Energia_mWhR101_Pressure", ["_time", "_value"]]
                    
                    DataR101 = [Inyections, VolAcumR101, TempPoolR101, PressureR101, xCH4R101, xCO2R101,
                                xO2R101, xH2SR101, xH2R101, EnergiaR101, TempR101, pHR101]
                    
                    Columns_names = ["Inyections", "VolAcumR101", "TempGasR101", "xCH4R101", "xCO2R101",
                                "xO2R101", "xH2SR101", "xH2R101", "EnergiaR101", "TempR101", "pHR101"]
                
                R101_data = pd.concat(DataR101)
                R101_data = R101_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R101
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR101 = DataEstimation.loc["PTotalR101", ["_time", "_value"]]
                    VolAcumR101 = DataEstimation.loc["Volumen_bioR101_Pressure", ["_time", "_value"]]
                    TempGasR101 = DataPlantSideA.loc["TE-101B", ["_time", "_value"]]
                    xCH4R101 = DataPlantSideA.loc["CH4-101", ["_time", "_value"]]
                    xCO2R101 = DataPlantSideA.loc["CO2-101", ["_time", "_value"]]
                    xO2R101 = DataPlantSideA.loc["O2-101", ["_time", "_value"]]
                    xH2SR101 = DataPlantSideA.loc["H2S-101", ["_time", "_value"]]
                    xH2R101 = DataPlantSideA.loc["H2-101", ["_time", "_value"]]
                    EnergiaR101 = DataEstimation.loc["Energia_mWhR101_Pressure", ["_time", "_value"]]
                    
                    DataR101 = [AcumPressureR101, VolAcumR101, TempGasR101, xCH4R101, xCO2R101,
                                xO2R101, xH2SR101, xH2R101, EnergiaR101, TempR101, pHR101]
                    
                    Columns_names = ["AcumPressureR101", "VolAcumR101", "TempGasR101", "xCH4R101", "xCO2R101",
                                "xO2R101", "xH2SR101", "xH2R101", "EnergiaR101", "TempR101", "pHR101"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR101 = DataEstimation.loc["VacumA", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR101 = DataEstimation.loc["TE-100A", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR101 = DataEstimation.loc["PT-100A", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R101 = DataPlantSideA.loc["CH4-101", ["_time", "_value"]]
                    xCO2R101 = DataPlantSideA.loc["CO2-101", ["_time", "_value"]]
                    xO2R101 = DataPlantSideA.loc["O2-101", ["_time", "_value"]]
                    xH2SR101 = DataPlantSideA.loc["H2S-101", ["_time", "_value"]]
                    xH2R101 = DataPlantSideA.loc["H2-101", ["_time", "_value"]]
                    EnergiaR101 = DataEstimation.loc["Energia_mWhR101_Pressure", ["_time", "_value"]]
                    
                    DataR101 = [VolAcumR101, TempPoolR101, PressureR101, xCH4R101, xCO2R101,
                                xO2R101, xH2SR101, xH2R101, EnergiaR101, TempR101, pHR101]
                    
                    Columns_names = ["VolAcumR101", "TempGasR101", "xCH4R101", "xCO2R101",
                                "xO2R101", "xH2SR101", "xH2R101", "EnergiaR101", "TempR101", "pHR101"]
                
            R101_data = DataR101[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR101[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R101_data = pd.merge(R101_data, df_rename, on="_time", how="outer")
            
            R101_data = R101_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R101_data.columns = new_columns
            try:
                cols_to_fill = R101_data.columns.difference(["Inyections"])
                R101_data[cols_to_fill] = R101_data[cols_to_fill].bfill().ffill()
                R101_data["Inyections"] = R101_data["Inyections"].fillna(0)
            except:
                R101_data = R101_data.bfill()
                R101_data = R101_data.ffill()
            
            R101_data["normalice_time"] = normaliceTime(R101_data["_time"])
            
            if (R101_data["xCH4R101"] != 0).any():
                R101_data["xCH4R101"] = R101_data["xCH4R101"].replace(0, pd.NA).bfill()
            
            if (R101_data["xCO2R101"] != 0).any():
                R101_data["xCO2R101"] = R101_data["xCO2R101"].replace(0, pd.NA).bfill()
            
            if (R101_data["xO2R101"] != 0).any():
                R101_data["xO2R101"] = R101_data["xO2R101"].replace(0, pd.NA).bfill()
            
            if (R101_data["xH2SR101"] != 0).any():
                R101_data["xH2SR101"] = R101_data["xH2SR101"].replace(0, pd.NA).bfill()
            
            if (R101_data["xH2R101"] != 0).any():
                R101_data["xH2R101"] = R101_data["xH2R101"].replace(0, pd.NA).bfill()
            
            self.R101_data = R101_data
        
            #%% Reactor 102
            TempR102 = DataPlantSideA.loc["TE-102A", ["_time", "_value"]]
            pHR102 = DataPlantSideA.loc["AT-102", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-111", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R102
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR102 = DataEstimation.loc["PTotalR102", ["_time", "_value"]]
                    VolAcumR102 = DataEstimation.loc["Volumen_bioR102_Pressure", ["_time", "_value"]]
                    TempGasR102 = DataPlantSideA.loc["TE-102B", ["_time", "_value"]]
                    xCH4R102 = DataPlantSideA.loc["CH4-102", ["_time", "_value"]]
                    xCO2R102 = DataPlantSideA.loc["CO2-102", ["_time", "_value"]]
                    xO2R102 = DataPlantSideA.loc["O2-102", ["_time", "_value"]]
                    xH2SR102 = DataPlantSideA.loc["H2S-102", ["_time", "_value"]]
                    xH2R102 = DataPlantSideA.loc["H2-102", ["_time", "_value"]]
                    EnergiaR102 = DataEstimation.loc["Energia_mWhR102_Pressure", ["_time", "_value"]]
                    
                    DataR102 = [Inyections, AcumPressureR102, VolAcumR102, TempGasR102, xCH4R102, xCO2R102,
                                xO2R102, xH2SR102, xH2R102, EnergiaR102, TempR102, pHR102]
                    Columns_names = ["Inyections", "AcumPressureR102", "VolAcumR102", "TempGasR102", "xCH4R102", "xCO2R102",
                                "xO2R102", "xH2SR102", "xH2R102", "EnergiaR102", "TempR102", "pHR102"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR102 = DataEstimation.loc["VacumB", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR102 = DataEstimation.loc["TE-100B", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR102 = DataEstimation.loc["PT-100B", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R102 = DataPlantSideA.loc["CH4-102", ["_time", "_value"]]
                    xCO2R102 = DataPlantSideA.loc["CO2-102", ["_time", "_value"]]
                    xO2R102 = DataPlantSideA.loc["O2-102", ["_time", "_value"]]
                    xH2SR102 = DataPlantSideA.loc["H2S-102", ["_time", "_value"]]
                    xH2R102 = DataPlantSideA.loc["H2-102", ["_time", "_value"]]
                    EnergiaR102 = DataEstimation.loc["Energia_mWhR102_Pressure", ["_time", "_value"]]
                    
                    DataR102 = [Inyections, VolAcumR102, TempPoolR102, PressureR102, xCH4R102, xCO2R102,
                                xO2R102, xH2SR102, xH2R102, EnergiaR102, TempR102, pHR102]
                    
                    Columns_names = ["Inyections", "VolAcumR102", "TempGasR102", "xCH4R102", "xCO2R102",
                                "xO2R102", "xH2SR102", "xH2R102", "EnergiaR102", "TempR102", "pHR102"]
                
                R102_data = pd.concat(DataR102)
                R102_data = R102_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R102
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR102 = DataEstimation.loc["PTotalR102", ["_time", "_value"]]
                    VolAcumR102 = DataEstimation.loc["Volumen_bioR102_Pressure", ["_time", "_value"]]
                    TempGasR102 = DataPlantSideA.loc["TE-102B", ["_time", "_value"]]
                    xCH4R102 = DataPlantSideA.loc["CH4-102", ["_time", "_value"]]
                    xCO2R102 = DataPlantSideA.loc["CO2-102", ["_time", "_value"]]
                    xO2R102 = DataPlantSideA.loc["O2-102", ["_time", "_value"]]
                    xH2SR102 = DataPlantSideA.loc["H2S-102", ["_time", "_value"]]
                    xH2R102 = DataPlantSideA.loc["H2-102", ["_time", "_value"]]
                    EnergiaR102 = DataEstimation.loc["Energia_mWhR102_Pressure", ["_time", "_value"]]
                    
                    DataR102 = [AcumPressureR102, VolAcumR102, TempGasR102, xCH4R102, xCO2R102,
                                xO2R102, xH2SR102, xH2R102, EnergiaR102, TempR102, pHR102]
                    
                    Columns_names = ["AcumPressureR102", "VolAcumR102", "TempGasR102", "xCH4R102", "xCO2R102",
                                "xO2R102", "xH2SR102", "xH2R102", "EnergiaR102", "TempR102", "pHR102"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR102 = DataEstimation.loc["VacumB", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR102 = DataEstimation.loc["TE-100B", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR102 = DataEstimation.loc["PT-100B", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R102 = DataPlantSideA.loc["CH4-102", ["_time", "_value"]]
                    xCO2R102 = DataPlantSideA.loc["CO2-102", ["_time", "_value"]]
                    xO2R102 = DataPlantSideA.loc["O2-102", ["_time", "_value"]]
                    xH2SR102 = DataPlantSideA.loc["H2S-102", ["_time", "_value"]]
                    xH2R102 = DataPlantSideA.loc["H2-102", ["_time", "_value"]]
                    EnergiaR102 = DataEstimation.loc["Energia_mWhR102_Pressure", ["_time", "_value"]]
                    
                    DataR102 = [VolAcumR102, TempPoolR102, PressureR102, xCH4R102, xCO2R102,
                                xO2R102, xH2SR102, xH2R102, EnergiaR102, TempR102, pHR102]
                    
                    Columns_names = ["VolAcumR102", "TempGasR102", "xCH4R102", "xCO2R102",
                                "xO2R102", "xH2SR102", "xH2R102", "EnergiaR102", "TempR102", "pHR102"]
                
            R102_data = DataR102[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR102[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R102_data = pd.merge(R102_data, df_rename, on="_time", how="outer")
                
            R102_data = R102_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R102_data.columns = new_columns
            try:
                cols_to_fill = R102_data.columns.difference(["Inyections"])
                R102_data[cols_to_fill] = R102_data[cols_to_fill].bfill().ffill()
                R102_data["Inyections"] = R102_data["Inyections"].fillna(0)
            except:
                R102_data = R102_data.bfill()
                R102_data = R102_data.ffill()
            
            R102_data["normalice_time"] = normaliceTime(R102_data["_time"])

            if (R102_data["xCH4R102"] != 0).any():
                R102_data["xCH4R102"] = R102_data["xCH4R102"].replace(0, pd.NA).bfill()
            
            if (R102_data["xCO2R102"] != 0).any():
                R102_data["xCO2R102"] = R102_data["xCO2R102"].replace(0, pd.NA).bfill()
            
            if (R102_data["xO2R102"] != 0).any():
                R102_data["xO2R102"] = R102_data["xO2R102"].replace(0, pd.NA).bfill()
            
            if (R102_data["xH2SR102"] != 0).any():
                R102_data["xH2SR102"] = R102_data["xH2SR102"].replace(0, pd.NA).bfill()
            
            if (R102_data["xH2R102"] != 0).any():
                R102_data["xH2R102"] = R102_data["xH2R102"].replace(0, pd.NA).bfill()

            self.R102_data = R102_data
            
            #%% Reactor 103
            TempR103 = DataPlantSideA.loc["TE-103A", ["_time", "_value"]]
            pHR103 = DataPlantSideA.loc["AT-103", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-111", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R103
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR103 = DataEstimation.loc["PTotalR103", ["_time", "_value"]]
                    VolAcumR103 = DataEstimation.loc["Volumen_bioR103_Pressure", ["_time", "_value"]]
                    TempGasR103 = DataPlantSideA.loc["TE-103B", ["_time", "_value"]]
                    xCH4R103 = DataPlantSideA.loc["CH4-103", ["_time", "_value"]]
                    xCO2R103 = DataPlantSideA.loc["CO2-103", ["_time", "_value"]]
                    xO2R103 = DataPlantSideA.loc["O2-103", ["_time", "_value"]]
                    xH2SR103 = DataPlantSideA.loc["H2S-103", ["_time", "_value"]]
                    xH2R103 = DataPlantSideA.loc["H2-103", ["_time", "_value"]]
                    EnergiaR103 = DataEstimation.loc["Energia_mWhR103_Pressure", ["_time", "_value"]]
                    
                    DataR103 = [Inyections, AcumPressureR103, VolAcumR103, TempGasR103, xCH4R103, xCO2R103,
                                xO2R103, xH2SR103, xH2R103, EnergiaR103, TempR103, pHR103]
                    Columns_names = ["Inyections", "AcumPressureR103", "VolAcumR103", "TempGasR103", "xCH4R103", "xCO2R103",
                                "xO2R103", "xH2SR103", "xH2R103", "EnergiaR103", "TempR103", "pHR103"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR103 = DataEstimation.loc["VacumC", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR103 = DataEstimation.loc["TE-100C", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR103 = DataEstimation.loc["PT-100C", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R103 = DataPlantSideA.loc["CH4-103", ["_time", "_value"]]
                    xCO2R103 = DataPlantSideA.loc["CO2-103", ["_time", "_value"]]
                    xO2R103 = DataPlantSideA.loc["O2-103", ["_time", "_value"]]
                    xH2SR103 = DataPlantSideA.loc["H2S-103", ["_time", "_value"]]
                    xH2R103 = DataPlantSideA.loc["H2-103", ["_time", "_value"]]
                    EnergiaR103 = DataEstimation.loc["Energia_mWhR103_Pressure", ["_time", "_value"]]
                    
                    DataR103 = [Inyections, VolAcumR103, TempPoolR103, PressureR103, xCH4R103, xCO2R103,
                                xO2R103, xH2SR103, xH2R103, EnergiaR103, TempR103, pHR103]
                    
                    Columns_names = ["Inyections", "VolAcumR103", "TempGasR103", "xCH4R103", "xCO2R103",
                                "xO2R103", "xH2SR103", "xH2R103", "EnergiaR103", "TempR103", "pHR103"]
                
                R103_data = pd.concat(DataR103)
                R103_data = R103_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R103
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR103 = DataEstimation.loc["PTotalR103", ["_time", "_value"]]
                    VolAcumR103 = DataEstimation.loc["Volumen_bioR103_Pressure", ["_time", "_value"]]
                    TempGasR103 = DataPlantSideA.loc["TE-103B", ["_time", "_value"]]
                    xCH4R103 = DataPlantSideA.loc["CH4-103", ["_time", "_value"]]
                    xCO2R103 = DataPlantSideA.loc["CO2-103", ["_time", "_value"]]
                    xO2R103 = DataPlantSideA.loc["O2-103", ["_time", "_value"]]
                    xH2SR103 = DataPlantSideA.loc["H2S-103", ["_time", "_value"]]
                    xH2R103 = DataPlantSideA.loc["H2-103", ["_time", "_value"]]
                    EnergiaR103 = DataEstimation.loc["Energia_mWhR103_Pressure", ["_time", "_value"]]
                    
                    DataR103 = [AcumPressureR103, VolAcumR103, TempGasR103, xCH4R103, xCO2R103,
                                xO2R103, xH2SR103, xH2R103, EnergiaR103, TempR103, pHR103]
                    
                    Columns_names = ["AcumPressureR103", "VolAcumR103", "TempGasR103", "xCH4R103", "xCO2R103",
                                "xO2R103", "xH2SR103", "xH2R103", "EnergiaR103", "TempR103", "pHR103"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR103 = DataEstimation.loc["VacumC", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR103 = DataEstimation.loc["TE-100C", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR103 = DataEstimation.loc["PT-100C", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R103 = DataPlantSideA.loc["CH4-103", ["_time", "_value"]]
                    xCO2R103 = DataPlantSideA.loc["CO2-103", ["_time", "_value"]]
                    xO2R103 = DataPlantSideA.loc["O2-103", ["_time", "_value"]]
                    xH2SR103 = DataPlantSideA.loc["H2S-103", ["_time", "_value"]]
                    xH2R103 = DataPlantSideA.loc["H2-103", ["_time", "_value"]]
                    EnergiaR103 = DataEstimation.loc["Energia_mWhR103_Pressure", ["_time", "_value"]]
                    
                    DataR103 = [VolAcumR103, TempPoolR103, PressureR103, xCH4R103, xCO2R103,
                                xO2R103, xH2SR103, xH2R103, EnergiaR103, TempR103, pHR103]
                    
                    Columns_names = ["VolAcumR103", "TempGasR103", "xCH4R103", "xCO2R103",
                                "xO2R103", "xH2SR103", "xH2R103", "EnergiaR103", "TempR103", "pHR103"]
                
            R103_data = DataR103[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR103[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R103_data = pd.merge(R103_data, df_rename, on="_time", how="outer")
            
            R103_data = R103_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R103_data.columns = new_columns
            try:
                cols_to_fill = R103_data.columns.difference(["Inyections"])
                R103_data[cols_to_fill] = R103_data[cols_to_fill].bfill().ffill()
                R103_data["Inyections"] = R103_data["Inyections"].fillna(0)
            except:
                R103_data = R103_data.bfill()
                R103_data = R103_data.ffill()
            
            R103_data["normalice_time"] = normaliceTime(R103_data["_time"])
            
            if (R103_data["xCH4R103"] != 0).any():
                R103_data["xCH4R103"] = R103_data["xCH4R103"].replace(0, pd.NA).bfill()
            
            if (R103_data["xCO2R103"] != 0).any():
                R103_data["xCO2R103"] = R103_data["xCO2R103"].replace(0, pd.NA).bfill()
            
            if (R103_data["xO2R103"] != 0).any():
                R103_data["xO2R103"] = R103_data["xO2R103"].replace(0, pd.NA).bfill()
            
            if (R103_data["xH2SR103"] != 0).any():
                R103_data["xH2SR103"] = R103_data["xH2SR103"].replace(0, pd.NA).bfill()
            
            if (R103_data["xH2R103"] != 0).any():
                R103_data["xH2R103"] = R103_data["xH2R103"].replace(0, pd.NA).bfill()

            self.R103_data = R103_data
        
            #%% Reactor 104
            TempR104 = DataPlantSideA.loc["TE-104A", ["_time", "_value"]]
            pHR104 = DataPlantSideA.loc["AT-104", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-111", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R104
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR104 = DataEstimation.loc["PTotalR104", ["_time", "_value"]]
                    VolAcumR104 = DataEstimation.loc["Volumen_bioR104_Pressure", ["_time", "_value"]]
                    TempGasR104 = DataPlantSideA.loc["TE-104B", ["_time", "_value"]]
                    xCH4R104 = DataPlantSideA.loc["CH4-104", ["_time", "_value"]]
                    xCO2R104 = DataPlantSideA.loc["CO2-104", ["_time", "_value"]]
                    xO2R104 = DataPlantSideA.loc["O2-104", ["_time", "_value"]]
                    xH2SR104 = DataPlantSideA.loc["H2S-104", ["_time", "_value"]]
                    xH2R104 = DataPlantSideA.loc["H2-104", ["_time", "_value"]]
                    EnergiaR104 = DataEstimation.loc["Energia_mWhR104_Pressure", ["_time", "_value"]]
                    
                    DataR104 = [Inyections, AcumPressureR104, VolAcumR104, TempGasR104, xCH4R104, xCO2R104,
                                xO2R104, xH2SR104, xH2R104, EnergiaR104, TempR104, pHR104]
                    Columns_names = ["Inyections", "AcumPressureR104", "VolAcumR104", "TempGasR104", "xCH4R104", "xCO2R104",
                                "xO2R104", "xH2SR104", "xH2R104", "EnergiaR104", "TempR104", "pHR104"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR104 = DataEstimation.loc["VacumD", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR104 = DataEstimation.loc["TE-100D", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR104 = DataEstimation.loc["PT-100D", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R104 = DataPlantSideA.loc["CH4-104", ["_time", "_value"]]
                    xCO2R104 = DataPlantSideA.loc["CO2-104", ["_time", "_value"]]
                    xO2R104 = DataPlantSideA.loc["O2-104", ["_time", "_value"]]
                    xH2SR104 = DataPlantSideA.loc["H2S-104", ["_time", "_value"]]
                    xH2R104 = DataPlantSideA.loc["H2-104", ["_time", "_value"]]
                    EnergiaR104 = DataEstimation.loc["Energia_mWhR104_Pressure", ["_time", "_value"]]
                    
                    DataR104 = [Inyections, VolAcumR104, TempPoolR104, PressureR104, xCH4R104, xCO2R104,
                                xO2R104, xH2SR104, xH2R104, EnergiaR104, TempR104, pHR104]
                    
                    Columns_names = ["Inyections", "VolAcumR104", "TempGasR104", "xCH4R104", "xCO2R104",
                                "xO2R104", "xH2SR104", "xH2R104", "EnergiaR104", "TempR104", "pHR104"]
                
                R104_data = pd.concat(DataR104)
                R104_data = R104_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R104
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR104 = DataEstimation.loc["PTotalR104", ["_time", "_value"]]
                    VolAcumR104 = DataEstimation.loc["Volumen_bioR104_Pressure", ["_time", "_value"]]
                    TempGasR104 = DataPlantSideA.loc["TE-104B", ["_time", "_value"]]
                    xCH4R104 = DataPlantSideA.loc["CH4-104", ["_time", "_value"]]
                    xCO2R104 = DataPlantSideA.loc["CO2-104", ["_time", "_value"]]
                    xO2R104 = DataPlantSideA.loc["O2-104", ["_time", "_value"]]
                    xH2SR104 = DataPlantSideA.loc["H2S-104", ["_time", "_value"]]
                    xH2R104 = DataPlantSideA.loc["H2-104", ["_time", "_value"]]
                    EnergiaR104 = DataEstimation.loc["Energia_mWhR104_Pressure", ["_time", "_value"]]
                    
                    DataR104 = [AcumPressureR104, VolAcumR104, TempGasR104, xCH4R104, xCO2R104,
                                xO2R104, xH2SR104, xH2R104, EnergiaR104, TempR104, pHR104]
                    
                    Columns_names = ["AcumPressureR104", "VolAcumR104", "TempGasR104", "xCH4R104", "xCO2R104",
                                "xO2R104", "xH2SR104", "xH2R104", "EnergiaR104", "TempR104", "pHR104"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR104 = DataEstimation.loc["VacumD", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR104 = DataEstimation.loc["TE-100D", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR104 = DataEstimation.loc["PT-100D", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R104 = DataPlantSideA.loc["CH4-104", ["_time", "_value"]]
                    xCO2R104 = DataPlantSideA.loc["CO2-104", ["_time", "_value"]]
                    xO2R104 = DataPlantSideA.loc["O2-104", ["_time", "_value"]]
                    xH2SR104 = DataPlantSideA.loc["H2S-104", ["_time", "_value"]]
                    xH2R104 = DataPlantSideA.loc["H2-104", ["_time", "_value"]]
                    EnergiaR104 = DataEstimation.loc["Energia_mWhR104_Pressure", ["_time", "_value"]]
                    
                    DataR104 = [VolAcumR104, TempPoolR104, PressureR104, xCH4R104, xCO2R104,
                                xO2R104, xH2SR104, xH2R104, EnergiaR104, TempR104, pHR104]
                    
                    Columns_names = ["VolAcumR104", "TempGasR104", "xCH4R104", "xCO2R104",
                                "xO2R104", "xH2SR104", "xH2R104", "EnergiaR104", "TempR104", "pHR104"]
                
            R104_data = DataR104[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR104[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R104_data = pd.merge(R104_data, df_rename, on="_time", how="outer")
            
            R104_data = R104_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R104_data.columns = new_columns
            try:
                cols_to_fill = R104_data.columns.difference(["Inyections"])
                R104_data[cols_to_fill] = R104_data[cols_to_fill].bfill().ffill()
                R104_data["Inyections"] = R104_data["Inyections"].fillna(0)
            except:
                R104_data = R104_data.bfill()
                R104_data = R104_data.ffill()
            
            R104_data["normalice_time"] = normaliceTime(R104_data["_time"])
            
            if (R104_data["xCH4R104"] != 0).any():
                R104_data["xCH4R104"] = R104_data["xCH4R104"].replace(0, pd.NA).bfill()
            
            if (R104_data["xCO2R104"] != 0).any():
                R104_data["xCO2R104"] = R104_data["xCO2R104"].replace(0, pd.NA).bfill()
            
            if (R104_data["xO2R104"] != 0).any():
                R104_data["xO2R104"] = R104_data["xO2R104"].replace(0, pd.NA).bfill()
            
            if (R104_data["xH2SR104"] != 0).any():
                R104_data["xH2SR104"] = R104_data["xH2SR104"].replace(0, pd.NA).bfill()
            
            if (R104_data["xH2R104"] != 0).any():
                R104_data["xH2R104"] = R104_data["xH2R104"].replace(0, pd.NA).bfill()

            self.R104_data = R104_data

            #%% Reactor 105
            TempR105 = DataPlantSideA.loc["TE-105A", ["_time", "_value"]]
            pHR105 = DataPlantSideA.loc["AT-105", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-111", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R105
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR105 = DataEstimation.loc["PTotalR105", ["_time", "_value"]]
                    VolAcumR105 = DataEstimation.loc["Volumen_bioR105_Pressure", ["_time", "_value"]]
                    TempGasR105 = DataPlantSideA.loc["TE-105B", ["_time", "_value"]]
                    xCH4R105 = DataPlantSideA.loc["CH4-105", ["_time", "_value"]]
                    xCO2R105 = DataPlantSideA.loc["CO2-105", ["_time", "_value"]]
                    xO2R105 = DataPlantSideA.loc["O2-105", ["_time", "_value"]]
                    xH2SR105 = DataPlantSideA.loc["H2S-105", ["_time", "_value"]]
                    xH2R105 = DataPlantSideA.loc["H2-105", ["_time", "_value"]]
                    EnergiaR105 = DataEstimation.loc["Energia_mWhR105_Pressure", ["_time", "_value"]]
                    
                    DataR105 = [Inyections, AcumPressureR105, VolAcumR105, TempGasR105, xCH4R105, xCO2R105,
                                xO2R105, xH2SR105, xH2R105, EnergiaR105, TempR105, pHR105]
                    Columns_names = ["Inyections", "AcumPressureR105", "VolAcumR105", "TempGasR105", "xCH4R105", "xCO2R105",
                                "xO2R105", "xH2SR105", "xH2R105", "EnergiaR105", "TempR105", "pHR105"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR105 = DataEstimation.loc["VacumE", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR105 = DataEstimation.loc["TE-100E", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR105 = DataEstimation.loc["PT-100E", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R105 = DataPlantSideA.loc["CH4-105", ["_time", "_value"]]
                    xCO2R105 = DataPlantSideA.loc["CO2-105", ["_time", "_value"]]
                    xO2R105 = DataPlantSideA.loc["O2-105", ["_time", "_value"]]
                    xH2SR105 = DataPlantSideA.loc["H2S-105", ["_time", "_value"]]
                    xH2R105 = DataPlantSideA.loc["H2-105", ["_time", "_value"]]
                    EnergiaR105 = DataEstimation.loc["Energia_mWhR105_Pressure", ["_time", "_value"]]
                    
                    DataR105 = [Inyections, VolAcumR105, TempPoolR105, PressureR105, xCH4R105, xCO2R105,
                                xO2R105, xH2SR105, xH2R105, EnergiaR105, TempR105, pHR105]
                    
                    Columns_names = ["Inyections", "VolAcumR105", "TempGasR105", "xCH4R105", "xCO2R105",
                                "xO2R105", "xH2SR105", "xH2R105", "EnergiaR105", "TempR105", "pHR105"]
                
                R105_data = pd.concat(DataR105)
                R105_data = R105_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R105
                if MeasureMethodSideA == "Pressure":
                    #Biogas topcase
                    AcumPressureR105 = DataEstimation.loc["PTotalR105", ["_time", "_value"]]
                    VolAcumR105 = DataEstimation.loc["Volumen_bioR105_Pressure", ["_time", "_value"]]
                    TempGasR105 = DataPlantSideA.loc["TE-105B", ["_time", "_value"]]
                    xCH4R105 = DataPlantSideA.loc["CH4-105", ["_time", "_value"]]
                    xCO2R105 = DataPlantSideA.loc["CO2-105", ["_time", "_value"]]
                    xO2R105 = DataPlantSideA.loc["O2-105", ["_time", "_value"]]
                    xH2SR105 = DataPlantSideA.loc["H2S-105", ["_time", "_value"]]
                    xH2R105 = DataPlantSideA.loc["H2-105", ["_time", "_value"]]
                    EnergiaR105 = DataEstimation.loc["Energia_mWhR105_Pressure", ["_time", "_value"]]
                    
                    DataR105 = [AcumPressureR105, VolAcumR105, TempGasR105, xCH4R105, xCO2R105,
                                xO2R105, xH2SR105, xH2R105, EnergiaR105, TempR105, pHR105]
                    
                    Columns_names = ["AcumPressureR105", "VolAcumR105", "TempGasR105", "xCH4R105", "xCO2R105",
                                "xO2R105", "xH2SR105", "xH2R105", "EnergiaR105", "TempR105", "pHR105"]

                #Accumulated Volume
                elif MeasureMethodSideA == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR105 = DataEstimation.loc["VacumE", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR105 = DataEstimation.loc["TE-100E", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR105 = DataEstimation.loc["PT-100E", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R105 = DataPlantSideA.loc["CH4-105", ["_time", "_value"]]
                    xCO2R105 = DataPlantSideA.loc["CO2-105", ["_time", "_value"]]
                    xO2R105 = DataPlantSideA.loc["O2-105", ["_time", "_value"]]
                    xH2SR105 = DataPlantSideA.loc["H2S-105", ["_time", "_value"]]
                    xH2R105 = DataPlantSideA.loc["H2-105", ["_time", "_value"]]
                    EnergiaR105 = DataEstimation.loc["Energia_mWhR105_Pressure", ["_time", "_value"]]
                    
                    DataR105 = [VolAcumR105, TempPoolR105, PressureR105, xCH4R105, xCO2R105,
                                xO2R105, xH2SR105, xH2R105, EnergiaR105, TempR105, pHR105]
                    
                    Columns_names = ["VolAcumR105", "TempGasR105", "xCH4R105", "xCO2R105",
                                "xO2R105", "xH2SR105", "xH2R105", "EnergiaR105", "TempR105", "pHR105"]
                
            R105_data = DataR105[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR105[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R105_data = pd.merge(R105_data, df_rename, on="_time", how="outer")
            
            R105_data = R105_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R105_data.columns = new_columns
            try:
                cols_to_fill = R105_data.columns.difference(["Inyections"])
                R105_data[cols_to_fill] = R105_data[cols_to_fill].bfill().ffill()
                R105_data["Inyections"] = R105_data["Inyections"].fillna(0)
            except:
                R105_data = R105_data.bfill()
                R105_data = R105_data.ffill()
            
            R105_data["normalice_time"] = normaliceTime(R105_data["_time"])
            
            if (R105_data["xCH4R105"] != 0).any():
                R105_data["xCH4R105"] = R105_data["xCH4R105"].replace(0, pd.NA).bfill()
            
            if (R105_data["xCO2R105"] != 0).any():
                R105_data["xCO2R105"] = R105_data["xCO2R105"].replace(0, pd.NA).bfill()
            
            if (R105_data["xO2R105"] != 0).any():
                R105_data["xO2R105"] = R105_data["xO2R105"].replace(0, pd.NA).bfill()
            
            if (R105_data["xH2SR105"] != 0).any():
                R105_data["xH2SR105"] = R105_data["xH2SR105"].replace(0, pd.NA).bfill()
            
            if (R105_data["xH2R105"] != 0).any():
                R105_data["xH2R105"] = R105_data["xH2R105"].replace(0, pd.NA).bfill()

            self.R105_data = R105_data
        
         #Side B
        if SideB == True:
            #%%Reactor 106
            TempR106 = DataPlantSideB.loc["TE-106A", ["_time", "_value"]]
            pHR106 = DataPlantSideB.loc["AT-106", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-112", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R106
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR106 = DataEstimation.loc["PTotalR106", ["_time", "_value"]]
                    VolAcumR106 = DataEstimation.loc["Volumen_bioR106_Pressure", ["_time", "_value"]]
                    TempGasR106 = DataPlantSideB.loc["TE-106B", ["_time", "_value"]]
                    xCH4R106 = DataPlantSideB.loc["CH4-106", ["_time", "_value"]]
                    xCO2R106 = DataPlantSideB.loc["CO2-106", ["_time", "_value"]]
                    xO2R106 = DataPlantSideB.loc["O2-106", ["_time", "_value"]]
                    xH2SR106 = DataPlantSideB.loc["H2S-106", ["_time", "_value"]]
                    xH2R106 = DataPlantSideB.loc["H2-106", ["_time", "_value"]]
                    EnergiaR106 = DataEstimation.loc["Energia_mWhR106_Pressure", ["_time", "_value"]]
                    
                    DataR106 = [Inyections, AcumPressureR106, VolAcumR106, TempGasR106, xCH4R106, xCO2R106,
                                xO2R106, xH2SR106, xH2R106, EnergiaR106, TempR106, pHR106]
                    Columns_names = ["Inyections", "AcumPressureR106", "VolAcumR106", "TempGasR106", "xCH4R106", "xCO2R106",
                                "xO2R106", "xH2SR106", "xH2R106", "EnergiaR106", "TempR106", "pHR106"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR106 = DataEstimation.loc["VacumA", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR106 = DataEstimation.loc["TE-100A", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR106 = DataEstimation.loc["PT-100A", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R106 = DataPlantSideB.loc["CH4-106", ["_time", "_value"]]
                    xCO2R106 = DataPlantSideB.loc["CO2-106", ["_time", "_value"]]
                    xO2R106 = DataPlantSideB.loc["O2-106", ["_time", "_value"]]
                    xH2SR106 = DataPlantSideB.loc["H2S-106", ["_time", "_value"]]
                    xH2R106 = DataPlantSideB.loc["H2-106", ["_time", "_value"]]
                    EnergiaR106 = DataEstimation.loc["Energia_mWhR106_Pressure", ["_time", "_value"]]
                    
                    DataR106 = [Inyections, VolAcumR106, TempPoolR106, PressureR106, xCH4R106, xCO2R106,
                                xO2R106, xH2SR106, xH2R106, EnergiaR106, TempR106, pHR106]
                    
                    Columns_names = ["Inyections", "VolAcumR106", "TempGasR106", "xCH4R106", "xCO2R106",
                                "xO2R106", "xH2SR106", "xH2R106", "EnergiaR106", "TempR106", "pHR106"]
                
                R106_data = pd.concat(DataR106)
                R106_data = R106_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R106
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR106 = DataEstimation.loc["PTotalR106", ["_time", "_value"]]
                    VolAcumR106 = DataEstimation.loc["Volumen_bioR106_Pressure", ["_time", "_value"]]
                    TempGasR106 = DataPlantSideB.loc["TE-106B", ["_time", "_value"]]
                    xCH4R106 = DataPlantSideB.loc["CH4-106", ["_time", "_value"]]
                    xCO2R106 = DataPlantSideB.loc["CO2-106", ["_time", "_value"]]
                    xO2R106 = DataPlantSideB.loc["O2-106", ["_time", "_value"]]
                    xH2SR106 = DataPlantSideB.loc["H2S-106", ["_time", "_value"]]
                    xH2R106 = DataPlantSideB.loc["H2-106", ["_time", "_value"]]
                    EnergiaR106 = DataEstimation.loc["Energia_mWhR106_Pressure", ["_time", "_value"]]
                    
                    DataR106 = [AcumPressureR106, VolAcumR106, TempGasR106, xCH4R106, xCO2R106,
                                xO2R106, xH2SR106, xH2R106, EnergiaR106, TempR106, pHR106]
                    
                    Columns_names = ["AcumPressureR106", "VolAcumR106", "TempGasR106", "xCH4R106", "xCO2R106",
                                "xO2R106", "xH2SR106", "xH2R106", "EnergiaR106", "TempR106", "pHR106"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR106 = DataEstimation.loc["VacumA", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR106 = DataEstimation.loc["TE-100A", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR106 = DataEstimation.loc["PT-100A", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R106 = DataPlantSideB.loc["CH4-106", ["_time", "_value"]]
                    xCO2R106 = DataPlantSideB.loc["CO2-106", ["_time", "_value"]]
                    xO2R106 = DataPlantSideB.loc["O2-106", ["_time", "_value"]]
                    xH2SR106 = DataPlantSideB.loc["H2S-106", ["_time", "_value"]]
                    xH2R106 = DataPlantSideB.loc["H2-106", ["_time", "_value"]]
                    EnergiaR106 = DataEstimation.loc["Energia_mWhR106_Pressure", ["_time", "_value"]]
                    
                    DataR106 = [VolAcumR106, TempPoolR106, PressureR106, xCH4R106, xCO2R106,
                                xO2R106, xH2SR106, xH2R106, EnergiaR106, TempR106, pHR106]
                    
                    Columns_names = ["VolAcumR106", "TempGasR106", "xCH4R106", "xCO2R106",
                                "xO2R106", "xH2SR106", "xH2R106", "EnergiaR106", "TempR106", "pHR106"]
                
            R106_data = DataR106[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR106[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R106_data = pd.merge(R106_data, df_rename, on="_time", how="outer")
            
            R106_data = R106_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R106_data.columns = new_columns
            try:
                cols_to_fill = R106_data.columns.difference(["Inyections"])
                R106_data[cols_to_fill] = R106_data[cols_to_fill].bfill().ffill()
                R106_data["Inyections"] = R106_data["Inyections"].fillna(0)
            except:
                R106_data = R106_data.bfill()
                R106_data = R106_data.ffill()
            
            R106_data["normalice_time"] = normaliceTime(R106_data["_time"])
            
            if (R106_data["xCH4R106"] != 0).any():
                R106_data["xCH4R106"] = R106_data["xCH4R106"].replace(0, pd.NA).bfill()
            
            if (R106_data["xCO2R106"] != 0).any():
                R106_data["xCO2R106"] = R106_data["xCO2R106"].replace(0, pd.NA).bfill()
            
            if (R106_data["xO2R106"] != 0).any():
                R106_data["xO2R106"] = R106_data["xO2R106"].replace(0, pd.NA).bfill()
            
            if (R106_data["xH2SR106"] != 0).any():
                R106_data["xH2SR106"] = R106_data["xH2SR106"].replace(0, pd.NA).bfill()
            
            if (R106_data["xH2R106"] != 0).any():
                R106_data["xH2R106"] = R106_data["xH2R106"].replace(0, pd.NA).bfill()

            self.R106_data = R106_data

            #%%Reactor 107
            TempR107 = DataPlantSideB.loc["TE-107A", ["_time", "_value"]]
            pHR107 = DataPlantSideB.loc["AT-107", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-112", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R107
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR107 = DataEstimation.loc["PTotalR107", ["_time", "_value"]]
                    VolAcumR107 = DataEstimation.loc["Volumen_bioR107_Pressure", ["_time", "_value"]]
                    TempGasR107 = DataPlantSideB.loc["TE-107B", ["_time", "_value"]]
                    xCH4R107 = DataPlantSideB.loc["CH4-107", ["_time", "_value"]]
                    xCO2R107 = DataPlantSideB.loc["CO2-107", ["_time", "_value"]]
                    xO2R107 = DataPlantSideB.loc["O2-107", ["_time", "_value"]]
                    xH2SR107 = DataPlantSideB.loc["H2S-107", ["_time", "_value"]]
                    xH2R107 = DataPlantSideB.loc["H2-107", ["_time", "_value"]]
                    EnergiaR107 = DataEstimation.loc["Energia_mWhR107_Pressure", ["_time", "_value"]]
                    
                    DataR107 = [Inyections, AcumPressureR107, VolAcumR107, TempGasR107, xCH4R107, xCO2R107,
                                xO2R107, xH2SR107, xH2R107, EnergiaR107, TempR107, pHR107]
                    Columns_names = ["Inyections", "AcumPressureR107", "VolAcumR107", "TempGasR107", "xCH4R107", "xCO2R107",
                                "xO2R107", "xH2SR107", "xH2R107", "EnergiaR107", "TempR107", "pHR107"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR107 = DataEstimation.loc["VacumB", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR107 = DataEstimation.loc["TE-100B", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR107 = DataEstimation.loc["PT-100B", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R107 = DataPlantSideB.loc["CH4-107", ["_time", "_value"]]
                    xCO2R107 = DataPlantSideB.loc["CO2-107", ["_time", "_value"]]
                    xO2R107 = DataPlantSideB.loc["O2-107", ["_time", "_value"]]
                    xH2SR107 = DataPlantSideB.loc["H2S-107", ["_time", "_value"]]
                    xH2R107 = DataPlantSideB.loc["H2-107", ["_time", "_value"]]
                    EnergiaR107 = DataEstimation.loc["Energia_mWhR107_Pressure", ["_time", "_value"]]
                    
                    DataR107 = [Inyections, VolAcumR107, TempPoolR107, PressureR107, xCH4R107, xCO2R107,
                                xO2R107, xH2SR107, xH2R107, EnergiaR107, TempR107, pHR107]
                    
                    Columns_names = ["Inyections", "VolAcumR107", "TempGasR107", "xCH4R107", "xCO2R107",
                                "xO2R107", "xH2SR107", "xH2R107", "EnergiaR107", "TempR107", "pHR107"]
                
                R107_data = pd.concat(DataR107)
                R107_data = R107_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R107
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR107 = DataEstimation.loc["PTotalR107", ["_time", "_value"]]
                    VolAcumR107 = DataEstimation.loc["Volumen_bioR107_Pressure", ["_time", "_value"]]
                    TempGasR107 = DataPlantSideB.loc["TE-107B", ["_time", "_value"]]
                    xCH4R107 = DataPlantSideB.loc["CH4-107", ["_time", "_value"]]
                    xCO2R107 = DataPlantSideB.loc["CO2-107", ["_time", "_value"]]
                    xO2R107 = DataPlantSideB.loc["O2-107", ["_time", "_value"]]
                    xH2SR107 = DataPlantSideB.loc["H2S-107", ["_time", "_value"]]
                    xH2R107 = DataPlantSideB.loc["H2-107", ["_time", "_value"]]
                    EnergiaR107 = DataEstimation.loc["Energia_mWhR107_Pressure", ["_time", "_value"]]
                    
                    DataR107 = [AcumPressureR107, VolAcumR107, TempGasR107, xCH4R107, xCO2R107,
                                xO2R107, xH2SR107, xH2R107, EnergiaR107, TempR107, pHR107]
                    
                    Columns_names = ["AcumPressureR107", "VolAcumR107", "TempGasR107", "xCH4R107", "xCO2R107",
                                "xO2R107", "xH2SR107", "xH2R107", "EnergiaR107", "TempR107", "pHR107"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR107 = DataEstimation.loc["VacumB", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR107 = DataEstimation.loc["TE-100B", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR107 = DataEstimation.loc["PT-100B", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R107 = DataPlantSideB.loc["CH4-107", ["_time", "_value"]]
                    xCO2R107 = DataPlantSideB.loc["CO2-107", ["_time", "_value"]]
                    xO2R107 = DataPlantSideB.loc["O2-107", ["_time", "_value"]]
                    xH2SR107 = DataPlantSideB.loc["H2S-107", ["_time", "_value"]]
                    xH2R107 = DataPlantSideB.loc["H2-107", ["_time", "_value"]]
                    EnergiaR107 = DataEstimation.loc["Energia_mWhR107_Pressure", ["_time", "_value"]]
                    
                    DataR107 = [VolAcumR107, TempPoolR107, PressureR107, xCH4R107, xCO2R107,
                                xO2R107, xH2SR107, xH2R107, EnergiaR107, TempR107, pHR107]
                    
                    Columns_names = ["VolAcumR107", "TempGasR107", "xCH4R107", "xCO2R107",
                                "xO2R107", "xH2SR107", "xH2R107", "EnergiaR107", "TempR107", "pHR107"]
                
            R107_data = DataR107[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR107[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R107_data = pd.merge(R107_data, df_rename, on="_time", how="outer")
            
            R107_data = R107_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R107_data.columns = new_columns
            try:
                cols_to_fill = R107_data.columns.difference(["Inyections"])
                R107_data[cols_to_fill] = R107_data[cols_to_fill].bfill().ffill()
                R107_data["Inyections"] = R107_data["Inyections"].fillna(0)
            except:
                R107_data = R107_data.bfill()
                R107_data = R107_data.ffill()
            
            R107_data["normalice_time"] = normaliceTime(R107_data["_time"])

            if (R107_data["xCH4R107"] != 0).any():
                R107_data["xCH4R107"] = R107_data["xCH4R107"].replace(0, pd.NA).bfill()
            
            if (R107_data["xCO2R107"] != 0).any():
                R107_data["xCO2R107"] = R107_data["xCO2R107"].replace(0, pd.NA).bfill()
            
            if (R107_data["xO2R107"] != 0).any():
                R107_data["xO2R107"] = R107_data["xO2R107"].replace(0, pd.NA).bfill()
            
            if (R107_data["xH2SR107"] != 0).any():
                R107_data["xH2SR107"] = R107_data["xH2SR107"].replace(0, pd.NA).bfill()
            
            if (R107_data["xH2R107"] != 0).any():
                R107_data["xH2R107"] = R107_data["xH2R107"].replace(0, pd.NA).bfill()

            self.R107_data = R107_data

            #%%Reactor 108
            TempR108 = DataPlantSideB.loc["TE-108A", ["_time", "_value"]]
            pHR108 = DataPlantSideB.loc["AT-108", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-112", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R108
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR108 = DataEstimation.loc["PTotalR108", ["_time", "_value"]]
                    VolAcumR108 = DataEstimation.loc["Volumen_bioR108_Pressure", ["_time", "_value"]]
                    TempGasR108 = DataPlantSideB.loc["TE-108B", ["_time", "_value"]]
                    xCH4R108 = DataPlantSideB.loc["CH4-108", ["_time", "_value"]]
                    xCO2R108 = DataPlantSideB.loc["CO2-108", ["_time", "_value"]]
                    xO2R108 = DataPlantSideB.loc["O2-108", ["_time", "_value"]]
                    xH2SR108 = DataPlantSideB.loc["H2S-108", ["_time", "_value"]]
                    xH2R108 = DataPlantSideB.loc["H2-108", ["_time", "_value"]]
                    EnergiaR108 = DataEstimation.loc["Energia_mWhR108_Pressure", ["_time", "_value"]]
                    
                    DataR108 = [Inyections, AcumPressureR108, VolAcumR108, TempGasR108, xCH4R108, xCO2R108,
                                xO2R108, xH2SR108, xH2R108, EnergiaR108, TempR108, pHR108]
                    Columns_names = ["Inyections", "AcumPressureR108", "VolAcumR108", "TempGasR108", "xCH4R108", "xCO2R108",
                                "xO2R108", "xH2SR108", "xH2R108", "EnergiaR108", "TempR108", "pHR108"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR108 = DataEstimation.loc["VacumC", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR108 = DataEstimation.loc["TE-100C", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR108 = DataEstimation.loc["PT-100C", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R108 = DataPlantSideB.loc["CH4-108", ["_time", "_value"]]
                    xCO2R108 = DataPlantSideB.loc["CO2-108", ["_time", "_value"]]
                    xO2R108 = DataPlantSideB.loc["O2-108", ["_time", "_value"]]
                    xH2SR108 = DataPlantSideB.loc["H2S-108", ["_time", "_value"]]
                    xH2R108 = DataPlantSideB.loc["H2-108", ["_time", "_value"]]
                    EnergiaR108 = DataEstimation.loc["Energia_mWhR108_Pressure", ["_time", "_value"]]
                    
                    DataR108 = [Inyections, VolAcumR108, TempPoolR108, PressureR108, xCH4R108, xCO2R108,
                                xO2R108, xH2SR108, xH2R108, EnergiaR108, TempR108, pHR108]
                    
                    Columns_names = ["Inyections", "VolAcumR108", "TempGasR108", "xCH4R108", "xCO2R108",
                                "xO2R108", "xH2SR108", "xH2R108", "EnergiaR108", "TempR108", "pHR108"]
                
                R108_data = pd.concat(DataR108)
                R108_data = R108_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R108
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR108 = DataEstimation.loc["PTotalR108", ["_time", "_value"]]
                    VolAcumR108 = DataEstimation.loc["Volumen_bioR108_Pressure", ["_time", "_value"]]
                    TempGasR108 = DataPlantSideB.loc["TE-108B", ["_time", "_value"]]
                    xCH4R108 = DataPlantSideB.loc["CH4-108", ["_time", "_value"]]
                    xCO2R108 = DataPlantSideB.loc["CO2-108", ["_time", "_value"]]
                    xO2R108 = DataPlantSideB.loc["O2-108", ["_time", "_value"]]
                    xH2SR108 = DataPlantSideB.loc["H2S-108", ["_time", "_value"]]
                    xH2R108 = DataPlantSideB.loc["H2-108", ["_time", "_value"]]
                    EnergiaR108 = DataEstimation.loc["Energia_mWhR108_Pressure", ["_time", "_value"]]
                    
                    DataR108 = [AcumPressureR108, VolAcumR108, TempGasR108, xCH4R108, xCO2R108,
                                xO2R108, xH2SR108, xH2R108, EnergiaR108, TempR108, pHR108]
                    
                    Columns_names = ["AcumPressureR108", "VolAcumR108", "TempGasR108", "xCH4R108", "xCO2R108",
                                "xO2R108", "xH2SR108", "xH2R108", "EnergiaR108", "TempR108", "pHR108"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR108 = DataEstimation.loc["VacumC", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR108 = DataEstimation.loc["TE-100C", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR108 = DataEstimation.loc["PT-100C", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R108 = DataPlantSideB.loc["CH4-108", ["_time", "_value"]]
                    xCO2R108 = DataPlantSideB.loc["CO2-108", ["_time", "_value"]]
                    xO2R108 = DataPlantSideB.loc["O2-108", ["_time", "_value"]]
                    xH2SR108 = DataPlantSideB.loc["H2S-108", ["_time", "_value"]]
                    xH2R108 = DataPlantSideB.loc["H2-108", ["_time", "_value"]]
                    EnergiaR108 = DataEstimation.loc["Energia_mWhR108_Pressure", ["_time", "_value"]]
                    
                    DataR108 = [VolAcumR108, TempPoolR108, PressureR108, xCH4R108, xCO2R108,
                                xO2R108, xH2SR108, xH2R108, EnergiaR108, TempR108, pHR108]
                    
                    Columns_names = ["VolAcumR108", "TempGasR108", "xCH4R108", "xCO2R108",
                                "xO2R108", "xH2SR108", "xH2R108", "EnergiaR108", "TempR108", "pHR108"]
                
            R108_data = DataR108[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR108[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R108_data = pd.merge(R108_data, df_rename, on="_time", how="outer")
            
            R108_data = R108_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R108_data.columns = new_columns
            try:
                cols_to_fill = R108_data.columns.difference(["Inyections"])
                R108_data[cols_to_fill] = R108_data[cols_to_fill].bfill().ffill()
                R108_data["Inyections"] = R108_data["Inyections"].fillna(0)
            except:
                R108_data = R108_data.bfill()
                R108_data = R108_data.ffill()
            
            R108_data["normalice_time"] = normaliceTime(R108_data["_time"])

            if (R108_data["xCH4R108"] != 0).any():
                R108_data["xCH4R108"] = R108_data["xCH4R108"].replace(0, pd.NA).bfill()
            
            if (R108_data["xCO2R108"] != 0).any():
                R108_data["xCO2R108"] = R108_data["xCO2R108"].replace(0, pd.NA).bfill()
            
            if (R108_data["xO2R108"] != 0).any():
                R108_data["xO2R108"] = R108_data["xO2R108"].replace(0, pd.NA).bfill()
            
            if (R108_data["xH2SR108"] != 0).any():
                R108_data["xH2SR108"] = R108_data["xH2SR108"].replace(0, pd.NA).bfill()
            
            if (R108_data["xH2R108"] != 0).any():
                R108_data["xH2R108"] = R108_data["xH2R108"].replace(0, pd.NA).bfill()

            self.R108_data = R108_data

            #%%Reactor 109
            TempR109 = DataPlantSideB.loc["TE-109A", ["_time", "_value"]]
            pHR109 = DataPlantSideB.loc["AT-109", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-112", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R109
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR109 = DataEstimation.loc["PTotalR109", ["_time", "_value"]]
                    VolAcumR109 = DataEstimation.loc["Volumen_bioR109_Pressure", ["_time", "_value"]]
                    TempGasR109 = DataPlantSideB.loc["TE-109B", ["_time", "_value"]]
                    xCH4R109 = DataPlantSideB.loc["CH4-109", ["_time", "_value"]]
                    xCO2R109 = DataPlantSideB.loc["CO2-109", ["_time", "_value"]]
                    xO2R109 = DataPlantSideB.loc["O2-109", ["_time", "_value"]]
                    xH2SR109 = DataPlantSideB.loc["H2S-109", ["_time", "_value"]]
                    xH2R109 = DataPlantSideB.loc["H2-109", ["_time", "_value"]]
                    EnergiaR109 = DataEstimation.loc["Energia_mWhR109_Pressure", ["_time", "_value"]]
                    
                    DataR109 = [Inyections, AcumPressureR109, VolAcumR109, TempGasR109, xCH4R109, xCO2R109,
                                xO2R109, xH2SR109, xH2R109, EnergiaR109, TempR109, pHR109]
                    Columns_names = ["Inyections", "AcumPressureR109", "VolAcumR109", "TempGasR109", "xCH4R109", "xCO2R109",
                                "xO2R109", "xH2SR109", "xH2R109", "EnergiaR109", "TempR109", "pHR109"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR109 = DataEstimation.loc["VacumD", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR109 = DataEstimation.loc["TE-100D", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR109 = DataEstimation.loc["PT-100D", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R109 = DataPlantSideB.loc["CH4-109", ["_time", "_value"]]
                    xCO2R109 = DataPlantSideB.loc["CO2-109", ["_time", "_value"]]
                    xO2R109 = DataPlantSideB.loc["O2-109", ["_time", "_value"]]
                    xH2SR109 = DataPlantSideB.loc["H2S-109", ["_time", "_value"]]
                    xH2R109 = DataPlantSideB.loc["H2-109", ["_time", "_value"]]
                    EnergiaR109 = DataEstimation.loc["Energia_mWhR109_Pressure", ["_time", "_value"]]
                    
                    DataR109 = [Inyections, VolAcumR109, TempPoolR109, PressureR109, xCH4R109, xCO2R109,
                                xO2R109, xH2SR109, xH2R109, EnergiaR109, TempR109, pHR109]
                    
                    Columns_names = ["Inyections", "VolAcumR109", "TempGasR109", "xCH4R109", "xCO2R109",
                                "xO2R109", "xH2SR109", "xH2R109", "EnergiaR109", "TempR109", "pHR109"]
                
                R109_data = pd.concat(DataR109)
                R109_data = R109_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R109
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR109 = DataEstimation.loc["PTotalR109", ["_time", "_value"]]
                    VolAcumR109 = DataEstimation.loc["Volumen_bioR109_Pressure", ["_time", "_value"]]
                    TempGasR109 = DataPlantSideB.loc["TE-109B", ["_time", "_value"]]
                    xCH4R109 = DataPlantSideB.loc["CH4-109", ["_time", "_value"]]
                    xCO2R109 = DataPlantSideB.loc["CO2-109", ["_time", "_value"]]
                    xO2R109 = DataPlantSideB.loc["O2-109", ["_time", "_value"]]
                    xH2SR109 = DataPlantSideB.loc["H2S-109", ["_time", "_value"]]
                    xH2R109 = DataPlantSideB.loc["H2-109", ["_time", "_value"]]
                    EnergiaR109 = DataEstimation.loc["Energia_mWhR109_Pressure", ["_time", "_value"]]
                    
                    DataR109 = [AcumPressureR109, VolAcumR109, TempGasR109, xCH4R109, xCO2R109,
                                xO2R109, xH2SR109, xH2R109, EnergiaR109, TempR109, pHR109]
                    
                    Columns_names = ["AcumPressureR109", "VolAcumR109", "TempGasR109", "xCH4R109", "xCO2R109",
                                "xO2R109", "xH2SR109", "xH2R109", "EnergiaR109", "TempR109", "pHR109"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR109 = DataEstimation.loc["VacumD", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR109 = DataEstimation.loc["TE-100D", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR109 = DataEstimation.loc["PT-100D", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R109 = DataPlantSideB.loc["CH4-109", ["_time", "_value"]]
                    xCO2R109 = DataPlantSideB.loc["CO2-109", ["_time", "_value"]]
                    xO2R109 = DataPlantSideB.loc["O2-109", ["_time", "_value"]]
                    xH2SR109 = DataPlantSideB.loc["H2S-109", ["_time", "_value"]]
                    xH2R109 = DataPlantSideB.loc["H2-109", ["_time", "_value"]]
                    EnergiaR109 = DataEstimation.loc["Energia_mWhR109_Pressure", ["_time", "_value"]]
                    
                    DataR109 = [VolAcumR109, TempPoolR109, PressureR109, xCH4R109, xCO2R109,
                                xO2R109, xH2SR109, xH2R109, EnergiaR109, TempR109, pHR109]
                    
                    Columns_names = ["VolAcumR109", "TempGasR109", "xCH4R109", "xCO2R109",
                                "xO2R109", "xH2SR109", "xH2R109", "EnergiaR109", "TempR109", "pHR109"]
                
            R109_data = DataR109[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR109[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R109_data = pd.merge(R109_data, df_rename, on="_time", how="outer")
            
            R109_data = R109_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R109_data.columns = new_columns
            try:
                cols_to_fill = R109_data.columns.difference(["Inyections"])
                R109_data[cols_to_fill] = R109_data[cols_to_fill].bfill().ffill()
                R109_data["Inyections"] = R109_data["Inyections"].fillna(0)
            except:
                R109_data = R109_data.bfill()
                R109_data = R109_data.ffill()
            
            R109_data["normalice_time"] = normaliceTime(R109_data["_time"])

            if (R109_data["xCH4R109"] != 0).any():
                R109_data["xCH4R109"] = R109_data["xCH4R109"].replace(0, pd.NA).bfill()
            
            if (R109_data["xCO2R109"] != 0).any():
                R109_data["xCO2R109"] = R109_data["xCO2R109"].replace(0, pd.NA).bfill()
            
            if (R109_data["xO2R109"] != 0).any():
                R109_data["xO2R109"] = R109_data["xO2R109"].replace(0, pd.NA).bfill()
            
            if (R109_data["xH2SR109"] != 0).any():
                R109_data["xH2SR109"] = R109_data["xH2SR109"].replace(0, pd.NA).bfill()
            
            if (R109_data["xH2R109"] != 0).any():
                R109_data["xH2R109"] = R109_data["xH2R109"].replace(0, pd.NA).bfill()

            self.R109_data = R109_data

            #%%Reactor 110
            TempR110 = DataPlantSideB.loc["TE-110A", ["_time", "_value"]]
            pHR110 = DataPlantSideB.loc["AT-110", ["_time", "_value"]]
            
            #inyections
            if OperationMethod in ["Time", "Injection"]:
                #Inyections
                Inyections = DataEstimation.loc["M-112", ["_time", "_value"]]
                #Accumulated volume for each reactor by pressure
                #R110
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR110 = DataEstimation.loc["PTotalR110", ["_time", "_value"]]
                    VolAcumR110 = DataEstimation.loc["Volumen_bioR110_Pressure", ["_time", "_value"]]
                    TempGasR110 = DataPlantSideB.loc["TE-110B", ["_time", "_value"]]
                    xCH4R110 = DataPlantSideB.loc["CH4-110", ["_time", "_value"]]
                    xCO2R110 = DataPlantSideB.loc["CO2-110", ["_time", "_value"]]
                    xO2R110 = DataPlantSideB.loc["O2-110", ["_time", "_value"]]
                    xH2SR110 = DataPlantSideB.loc["H2S-110", ["_time", "_value"]]
                    xH2R110 = DataPlantSideB.loc["H2-110", ["_time", "_value"]]
                    EnergiaR110 = DataEstimation.loc["Energia_mWhR110_Pressure", ["_time", "_value"]]
                    
                    DataR110 = [Inyections, AcumPressureR110, VolAcumR110, TempGasR110, xCH4R110, xCO2R110,
                                xO2R110, xH2SR110, xH2R110, EnergiaR110, TempR110, pHR110]
                    Columns_names = ["Inyections", "AcumPressureR110", "VolAcumR110", "TempGasR110", "xCH4R110", "xCO2R110",
                                "xO2R110", "xH2SR110", "xH2R110", "EnergiaR110", "TempR110", "pHR110"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR110 = DataEstimation.loc["VacumE", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR110 = DataEstimation.loc["TE-100E", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR110 = DataEstimation.loc["PT-100E", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R110 = DataPlantSideB.loc["CH4-110", ["_time", "_value"]]
                    xCO2R110 = DataPlantSideB.loc["CO2-110", ["_time", "_value"]]
                    xO2R110 = DataPlantSideB.loc["O2-110", ["_time", "_value"]]
                    xH2SR110 = DataPlantSideB.loc["H2S-110", ["_time", "_value"]]
                    xH2R110 = DataPlantSideB.loc["H2-110", ["_time", "_value"]]
                    EnergiaR110 = DataEstimation.loc["Energia_mWhR110_Pressure", ["_time", "_value"]]
                    
                    DataR110 = [Inyections, VolAcumR110, TempPoolR110, PressureR110, xCH4R110, xCO2R110,
                                xO2R110, xH2SR110, xH2R110, EnergiaR110, TempR110, pHR110]
                    
                    Columns_names = ["Inyections", "VolAcumR110", "TempGasR110", "xCH4R110", "xCO2R110",
                                "xO2R110", "xH2SR110", "xH2R110", "EnergiaR110", "TempR110", "pHR110"]
                
                R110_data = pd.concat(DataR110)
                R110_data = R110_data.sort_values(by="_time").reset_index(drop=True)
            
            else:
                #Accumulated volume for each reactor by pressure
                #R110
                if MeasureMethodSideB == "Pressure":
                    #Biogas topcase
                    AcumPressureR110 = DataEstimation.loc["PTotalR110", ["_time", "_value"]]
                    VolAcumR110 = DataEstimation.loc["Volumen_bioR110_Pressure", ["_time", "_value"]]
                    TempGasR110 = DataPlantSideB.loc["TE-110B", ["_time", "_value"]]
                    xCH4R110 = DataPlantSideB.loc["CH4-110", ["_time", "_value"]]
                    xCO2R110 = DataPlantSideB.loc["CO2-110", ["_time", "_value"]]
                    xO2R110 = DataPlantSideB.loc["O2-110", ["_time", "_value"]]
                    xH2SR110 = DataPlantSideB.loc["H2S-110", ["_time", "_value"]]
                    xH2R110 = DataPlantSideB.loc["H2-110", ["_time", "_value"]]
                    EnergiaR110 = DataEstimation.loc["Energia_mWhR110_Pressure", ["_time", "_value"]]
                    
                    DataR110 = [AcumPressureR110, VolAcumR110, TempGasR110, xCH4R110, xCO2R110,
                                xO2R110, xH2SR110, xH2R110, EnergiaR110, TempR110, pHR110]
                    
                    Columns_names = ["AcumPressureR110", "VolAcumR110", "TempGasR110", "xCH4R110", "xCO2R110",
                                "xO2R110", "xH2SR110", "xH2R110", "EnergiaR110", "TempR110", "pHR110"]

                #Accumulated Volume
                elif MeasureMethodSideB == "VolumeDisplaced":
                    #Biogas volume
                    VolAcumR110 = DataEstimation.loc["VacumE", ["_time", "_value"]]       #Preguntar si es nivel o volumen
                    TempPoolR110 = DataEstimation.loc["TE-100E", ["_time", "_value"]]     #Temperature of flowmeter
                    PressureR110 = DataEstimation.loc["PT-100E", ["_time", "_value"]]     #Pressure of flowmeter
                    xCH4R110 = DataPlantSideB.loc["CH4-110", ["_time", "_value"]]
                    xCO2R110 = DataPlantSideB.loc["CO2-110", ["_time", "_value"]]
                    xO2R110 = DataPlantSideB.loc["O2-110", ["_time", "_value"]]
                    xH2SR110 = DataPlantSideB.loc["H2S-110", ["_time", "_value"]]
                    xH2R110 = DataPlantSideB.loc["H2-110", ["_time", "_value"]]
                    EnergiaR110 = DataEstimation.loc["Energia_mWhR110_Pressure", ["_time", "_value"]]
                    
                    DataR110 = [VolAcumR110, TempPoolR110, PressureR110, xCH4R110, xCO2R110,
                                xO2R110, xH2SR110, xH2R110, EnergiaR110, TempR110, pHR110]
                    
                    Columns_names = ["VolAcumR110", "TempGasR110", "xCH4R110", "xCO2R110",
                                "xO2R110", "xH2SR110", "xH2R110", "EnergiaR110", "TempR110", "pHR110"]
                
            R110_data = DataR110[0].rename(columns={'_value': 'df1_value'})

            for i, df in enumerate(DataR110[1:], start=2):
                df_rename = df.rename(columns={'_value': f'df{i}_value'})
                R110_data = pd.merge(R110_data, df_rename, on="_time", how="outer")
            
            R110_data = R110_data.sort_values(by="_time").reset_index(drop=True)
            new_columns = ["_time"] + Columns_names
            R110_data.columns = new_columns
            try:
                cols_to_fill = R110_data.columns.difference(["Inyections"])
                R110_data[cols_to_fill] = R110_data[cols_to_fill].bfill().ffill()
                R110_data["Inyections"] = R110_data["Inyections"].fillna(0)
            except:
                R110_data = R110_data.bfill()
                R110_data = R110_data.ffill()
            
            R110_data["normalice_time"] = normaliceTime(R110_data["_time"])

            if (R110_data["xCH4R110"] != 0).any():
                R110_data["xCH4R110"] = R110_data["xCH4R110"].replace(0, pd.NA).bfill()
            
            if (R110_data["xCO2R110"] != 0).any():
                R110_data["xCO2R110"] = R110_data["xCO2R110"].replace(0, pd.NA).bfill()
            
            if (R110_data["xO2R110"] != 0).any():
                R110_data["xO2R110"] = R110_data["xO2R110"].replace(0, pd.NA).bfill()
            
            if (R110_data["xH2SR110"] != 0).any():
                R110_data["xH2SR110"] = R110_data["xH2SR110"].replace(0, pd.NA).bfill()
            
            if (R110_data["xH2R110"] != 0).any():
                R110_data["xH2R110"] = R110_data["xH2R110"].replace(0, pd.NA).bfill()

            self.R110_data = R110_data
    
    def StochoimetricExpendtire_Reactor_batch (self, ReactorName, ReactorData, Vrxn, OperationMethod):    #Reactor name: R101, ReactorData: ProccesingData, Vrxn: mL
        Pstd = 100000     
        #ReactorData[f'VolAcum{ReactorName}'] = ReactorData[f'VolAcum{ReactorName}'] - min(ReactorData[f'VolAcum{ReactorName}'])                                                          #Pa
        ReactorData["nbiogas"] = Pstd * (ReactorData[f'VolAcum{ReactorName}']/1000000)/(8.314 * 273.15)
        ReactorData["nCH4"] = ReactorData["nbiogas"] * (ReactorData[f'xCH4{ReactorName}']/100)
        ReactorData["nCO2"] = ReactorData["nbiogas"] * (ReactorData[f'xCO2{ReactorName}']/100)
        ReactorData["nO2"] = ReactorData["nbiogas"] * (ReactorData[f'xO2{ReactorName}']/100)
        ReactorData["nH2S"] = ReactorData["nbiogas"] * (ReactorData[f'xH2S{ReactorName}']/1000000)
        ReactorData["nH2"] = ReactorData["nbiogas"] * (ReactorData[f'xH2{ReactorName}']/1000000)
        ReactorData["nNH3"] = ReactorData["nCH4"] * self.s_NH3/self.s_CH4
        ReactorData["nUn"] = ReactorData["nbiogas"] - ReactorData["nCH4"] - ReactorData["nCO2"] - ReactorData["nO2"] - ReactorData["nH2S"] - ReactorData["nH2"] - ReactorData["nNH3"]

        MW_CH4 = 16.04256  # g/mol
        MW_CO2 = 44.009    #g/mol
        MW_O2 = 31.9988    #g/mol
        MW_H2S = 34.082    #g/mol
        MW_H2 = 2.01588    #g/mol
        MW_NH3 = 17.03052  #g/mol
        ReactorData["wCH4"] = ReactorData["nCH4"] * MW_CH4
        ReactorData["wCO2"] = ReactorData["nCO2"] * MW_CO2
        ReactorData["wO2"] = ReactorData["nO2"] * MW_O2
        ReactorData["wH2S"] = ReactorData["nH2S"] * MW_H2S
        ReactorData["wH2"] = ReactorData["nH2"] * MW_H2
        ReactorData["wNH3"] = ReactorData["nNH3"] * MW_NH3
        ReactorData["wTotal"] = ReactorData["wCH4"] + ReactorData["wCO2"] + ReactorData["wO2"] + ReactorData["wH2S"] + ReactorData["wH2"] + ReactorData["wNH3"]
        
        #Derivation per time moles
        ReactorData["dnbiogas_dt"] = ReactorData["nbiogas"].diff()
        ReactorData["dnCH4_dt"] = ReactorData["nCH4"].diff()
        ReactorData["dnCO2_dt"] = ReactorData["nCO2"].diff()
        ReactorData["dnO2_dt"] = ReactorData["nO2"].diff()
        ReactorData["dnH2S_dt"] = ReactorData["nH2S"].diff()
        ReactorData["dnH2_dt"] = ReactorData["nH2"].diff()
        ReactorData["dnNH3_dt"] = ReactorData["nNH3"].diff()

        #Derivation per time mass
        ReactorData["dWtotal_dt"] = ReactorData["wTotal"].diff()
        ReactorData["dWCH4_dt"] = ReactorData["wCH4"].diff()
        ReactorData["dWCO2_dt"] = ReactorData["wCO2"].diff()
        ReactorData["dWO2_dt"] = ReactorData["wO2"].diff()
        ReactorData["dWH2S_dt"] = ReactorData["wH2S"].diff()
        ReactorData["dWH2_dt"] = ReactorData["wH2"].diff()
        ReactorData["dWNH3_dt"] = ReactorData["wNH3"].diff()

        #Delta_time
        ReactorData["dt"] = ReactorData["normalice_time"].diff()

        #fill first row with 0
        ReactorData.fillna(0, inplace=True)

        #Feeding conditions
        if OperationMethod == "Time":
            if ReactorName in ["R101", "R102", "R103", "R104", "R105"]:
                Q_time = float(self.PlantEstimation.loc["FE_A1", "_value"].iloc[-1])/1000
            elif ReactorName in ["R106", "R107", "R108", "R109", "R110"]:
                Q_time = float(self.PlantEstimation.loc["FE_B1", "_value"].iloc[-1])/1000
        elif OperationMethod == "Injection":
            if ReactorName in ["R101", "R102", "R103", "R104", "R105"]:
                Q_time = float(self.PlantEstimation.loc["FE_A2", "_value"].iloc[-1])/1000
            elif ReactorName in ["R106", "R107", "R108", "R109", "R110"]:
                Q_time = float(self.PlantEstimation.loc["FE_B2", "_value"].iloc[-1])/1000
        else:
            Q_time = 0        

        ST_ini = []
        SV_ini = []
        Csus_mol = []
        Q_inv = []
        #Total solids balance
        if OperationMethod in ["Time", "Injection"]:
            for i in range (len(ReactorData)):
                #Total solids balance
                gST_ini = self.ST_ini * (Vrxn/1000) * self.rho
                flow_in = ReactorData["Inyections"].iloc[i]
                if flow_in == 1:
                    Q_in = Q_time
                else:
                    Q_in = 0
                Q_inv.append(Q_in)
                gST_in = Q_in * self.ST * self.rho * ReactorData["dt"].iloc[i]
                gST_out_g =  ReactorData["dWtotal_dt"].iloc[i]
                gST_out_l = Q_in * self.ST_ini * ReactorData["dt"].iloc[i]
                self.ST_ini = (gST_ini + gST_in - gST_out_g - gST_out_l) / (Vrxn/1000) / self.rho
                ST_ini.append(self.ST_ini)
                #Volatile Solids balance
                gSV_ini = self.SV_ini * (Vrxn/1000) * self.rho
                gSV_in = Q_in * self.SV * self.rho * ReactorData["dt"].iloc[i]
                gSV_out_g =  ReactorData["dWtotal_dt"].iloc[i]
                gSV_out_l = Q_in * self.SV_ini * ReactorData["dt"].iloc[i]
                self.SV_ini = (gSV_ini + gSV_in - gSV_out_g - gSV_out_l) / (Vrxn/1000) / self.rho
                SV_ini.append(self.SV_ini)
                #Volatile mol balance
                mol_ini = self.Csus_ini_SV_mol * (Vrxn/1000)
                mol_in = Q_in * self.Csus_SV_mol * ReactorData["dt"].iloc[i]
                mol_out_g = ReactorData["dnCH4_dt"].iloc[i] * (1/self.s_CH4)
                mol_out_l = Q_in * self.Csus_ini_SV_mol * ReactorData["dt"].iloc[i]
                self.Csus_ini_SV_mol = (mol_ini + mol_in - mol_out_g - mol_out_l) / (Vrxn/1000)
                Csus_mol.append(self.Csus_ini_SV_mol)

            ReactorData["Q_in"] = Q_inv
            ReactorData["C_in"] = self.Csus_SV_mol
                
        elif OperationMethod == "NoDosing":
            for i in range (len(ReactorData)):
                #total solids balance
                gST_ini = self.ST_ini * (Vrxn/1000) * self.rho_ini
                gST_out_g =  ReactorData["dWtotal_dt"].iloc[i]
                self.ST_ini = (gST_ini - gST_out_g) / (Vrxn/1000) / self.rho_ini
                ST_ini.append(self.ST_ini)
                #Balance solids balance
                gSV_ini = self.SV_ini * (Vrxn/1000) * self.rho_ini
                gSV_out_g =  ReactorData["dWtotal_dt"].iloc[i]
                self.SV_ini = (gSV_ini - gSV_out_g)/(Vrxn/1000)/self.rho_ini
                SV_ini.append(self.SV_ini)
                #mol volatile balance
                mol_ini = self.Csus_ini_SV_mol * (Vrxn/1000)
                mol_out_g =  ReactorData["dnCH4_dt"].iloc[i] * (1/self.s_CH4)
                self.Csus_ini_SV_mol = (mol_ini - mol_out_g)/(Vrxn/1000)
                Csus_mol.append(self.Csus_ini_SV_mol)
      
        ReactorData["ST_int"] = ST_ini
        ReactorData["SV_int"] = SV_ini
        ReactorData["Csus_mol_int"] = Csus_mol
        
        return ReactorData