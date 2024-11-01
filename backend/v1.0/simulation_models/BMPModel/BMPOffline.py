from math import gcd
from functools import reduce
from fractions import Fraction
import numpy as np
from scipy.integrate import odeint
from simulation_models.Biogas import ThermoProperties as TP


class BMPModelOffline:
    def __init__ (self, Vrxn, Vf, tp):
        self.Vrxn = Vrxn       #mL
        self.Vf = Vf           #mL 
        self.tp = tp           #s

        #Thermodynamic properties for biogas
        self.Thermo = TP.ThermoProperties()
        
        #Initial values for mixing
        self.countermixing = 0

        #Initial values for feed
        self.counterfeed = 0
        self.TotalVolFeed = 0

        #Initial values for Reactor
        self.counterReactor = 0
        self.mol_CH4_ini = 0
        self.mol_O2 = 0
        self.mol_H2 = 0
        self.mol_H2O = 0

        #Thermodynamics measuremnts
        self.Vf1 = self.Vf       #free volume that change with substrate injections
        self.n_ii_wet = 0
        self.n_ii_dry = 0
        self.P_storage=0

    def MixtureCalculation (self, substratesNumber, MixtureRule, WaterFraction, WaterVolume, WaterWeight,
                            Fraction1, Volume1, Weight1, TS1, VS1, rho1, Cc1, Hc1, Oc1, Nc1, Sc1,
                            Fraction2 = 1, Volume2 = 1, Weight2 = 1, TS2 = 0.1, VS2 = 0.05, rho2 = 1000, Cc2 = 43, Hc2 = 5, Oc2 = 30, Nc2 = 2, Sc2 = 0.21,
                            Fraction3 = 1, Volume3 = 1, Weight3 = 1, TS3 = 0.1, VS3 = 0.05, rho3 = 1000, Cc3 = 43, Hc3 = 5, Oc3 = 30, Nc3 = 2, Sc3 = 0.21,
                            Fraction4 = 1, Volume4 = 1, Weight4 = 1, TS4 = 0.1, VS4 = 0.05, rho4 = 1000, Cc4 = 43, Hc4 = 5, Oc4 = 30, Nc4 = 2, Sc4 = 0.21,):
        
        if substratesNumber == 1 and MixtureRule == "Fracción":
            if WaterFraction + Fraction1 != 100:
                Fraction1 = 100 - WaterFraction
            
            Fraction1 = Fraction1/100
            WaterFraction = WaterFraction/100
            self.TSini = TS1 * Fraction1
            self.VSini = VS1 * Fraction1
            self.rho = rho1 * Fraction1 + 1000 * WaterFraction
            self.Cc = Cc1
            self.Hc = Hc1
            self.Oc = Oc1
            self.Nc = Nc1
            self.Sc = Sc1
        
        elif substratesNumber == 2 and MixtureRule == "Fracción":
            if WaterFraction + Fraction1 + Fraction2 != 100:
                Fraction2 = 100 - WaterFraction - Fraction1
            
            Fraction1 = Fraction1/100
            Fraction2 = Fraction2/100
            WaterFraction = WaterFraction/100
            self.TSini = Fraction1 * TS1 + Fraction2 * TS2
            self.VSini = Fraction1 * VS1 + Fraction2 * VS2
            self.rho = rho1 * Fraction1 + rho2 * Fraction2 + 1000 * WaterFraction
            dryWeight = (Fraction1 * 100)*(TS1/100) + (Fraction2 * 100)*(TS2/100)
            gC1 = (Fraction1 * 100) * Cc1; gC2 = (Fraction2 * 100) * Cc2
            gH1 = (Fraction1 * 100) * Hc1; gH2 = (Fraction2 * 100) * Hc2
            gO1 = (Fraction1 * 100) * Oc1; gO2 = (Fraction2 * 100) * Oc2
            gN1 = (Fraction1 * 100) * Nc1; gN2 = (Fraction2 * 100) * Nc2
            gS1 = (Fraction1 * 100) * Sc1; gS2 = (Fraction2 * 100) * Sc2
            self.Cc = (gC1 + gC2)/dryWeight
            self.Hc = (gH1 + gH2)/dryWeight
            self.Oc = (gO1 + gO2)/dryWeight
            self.Nc = (gN1 + gN2)/dryWeight
            self.Sc = (gS1 + gS2)/dryWeight
        
        elif substratesNumber == 3 and MixtureRule == "Fracción":
            if WaterFraction + Fraction1 + Fraction2 + Fraction3 != 100:
                Fraction3 = 100 - WaterFraction - Fraction1 - Fraction2
            
            Fraction1 = Fraction1/100
            Fraction2 = Fraction2/100
            Fraction3 = Fraction3/100
            WaterFraction = WaterFraction/100
            self.TSini = Fraction1 * TS1 + Fraction2 * TS2 * Fraction3 * TS3
            self.VSini = Fraction1 * VS1 + Fraction2 * VS2 * Fraction3 * VS3
            self.rho = rho1 * Fraction1 + rho2 * Fraction2 + rho3 * Fraction3 + 1000 * WaterFraction
            dryWeight = (Fraction1 * 100)*(TS1/100) + (Fraction2 * 100)*(TS2/100) + (Fraction3 * 100)*(TS3/100)
            gC1 = (Fraction1 * 100) * Cc1; gC2 = (Fraction2 * 100) * Cc2; gC3 = (Fraction3 * 100) * Cc3
            gH1 = (Fraction1 * 100) * Hc1; gH2 = (Fraction2 * 100) * Hc2; gH3 = (Fraction3 * 100) * Hc3
            gO1 = (Fraction1 * 100) * Oc1; gO2 = (Fraction2 * 100) * Oc2; gO3 = (Fraction3 * 100) * Oc3
            gN1 = (Fraction1 * 100) * Nc1; gN2 = (Fraction2 * 100) * Nc2; gN3 = (Fraction3 * 100) * Nc3
            gS1 = (Fraction1 * 100) * Sc1; gS2 = (Fraction2 * 100) * Sc2; gS3 = (Fraction3 * 100) * Sc3
            self.Cc = (gC1 + gC2 + gC3)/dryWeight
            self.Hc = (gH1 + gH2 + gH3)/dryWeight
            self.Oc = (gO1 + gO2 + gO3)/dryWeight
            self.Nc = (gN1 + gN2 + gN3)/dryWeight
            self.Sc = (gS1 + gS2 + gS3)/dryWeight
        
        elif substratesNumber == 4 and MixtureRule == "Fracción":
            if WaterFraction + Fraction1 + Fraction2 + Fraction3 + Fraction4 != 100:
                Fraction4 = 100 - WaterFraction - Fraction1 - Fraction2 - Fraction3
            
            Fraction1 = Fraction1/100
            Fraction2 = Fraction2/100
            Fraction3 = Fraction3/100
            Fraction4 = Fraction4/100
            WaterFraction = WaterFraction/100
            self.TSini = Fraction1 * TS1 + Fraction2 * TS2 * Fraction3 * TS3 * Fraction4 * TS4
            self.VSini = Fraction1 * VS1 + Fraction2 * VS2 * Fraction3 * VS3 * Fraction4 * VS4
            self.rho = rho1 * Fraction1 + rho2 * Fraction2 + rho3 * Fraction3 + rho4 * Fraction4 + 1000 * WaterFraction
            dryWeight = (Fraction1 * 100)*(TS1/100) + (Fraction2 * 100)*(TS2/100) + (Fraction3 * 100)*(TS3/100) + (Fraction4 * 100)*(TS4/100)
            gC1 = (Fraction1 * 100) * Cc1; gC2 = (Fraction2 * 100) * Cc2; gC3 = (Fraction3 * 100) * Cc3; gC4 = (Fraction4 * 100) * Cc4
            gH1 = (Fraction1 * 100) * Hc1; gH2 = (Fraction2 * 100) * Hc2; gH3 = (Fraction3 * 100) * Hc3; gH4 = (Fraction4 * 100) * Hc4
            gO1 = (Fraction1 * 100) * Oc1; gO2 = (Fraction2 * 100) * Oc2; gO3 = (Fraction3 * 100) * Oc3; gO4 = (Fraction4 * 100) * Oc4
            gN1 = (Fraction1 * 100) * Nc1; gN2 = (Fraction2 * 100) * Nc2; gN3 = (Fraction3 * 100) * Nc3; gN4 = (Fraction4 * 100) * Nc4
            gS1 = (Fraction1 * 100) * Sc1; gS2 = (Fraction2 * 100) * Sc2; gS3 = (Fraction3 * 100) * Sc3; gS4 = (Fraction4 * 100) * Sc4
            self.Cc = (gC1 + gC2 + gC3 + gC4)/dryWeight
            self.Hc = (gH1 + gH2 + gH3 + gH4)/dryWeight
            self.Oc = (gO1 + gO2 + gO3 + gO4)/dryWeight
            self.Nc = (gN1 + gN2 + gN3 + gN4)/dryWeight
            self.Sc = (gS1 + gS2 + gS3 + gS4)/dryWeight
        
        elif substratesNumber == 1 and (MixtureRule == "Volumen" or MixtureRule == "Peso"):
            if MixtureRule == "Volumen":
                wWater = WaterVolume                    #g
                wS1 = Volume1 * (rho1/1000)             #g
                
            elif MixtureRule == "Peso":
                wWater = WaterWeight
                wS1 = Weight1
            
            Fraction1 = wS1/(wS1 + wWater)          #Substrate fraction
            WaterFraction = wWater/(wS1 + wWater)   #Water fraction

            self.TSini = Fraction1 * TS1     
            self.VSini = Fraction1 * VS1
            self.rho = Fraction1 * rho1 + WaterFraction * 1000
            self.Cc = Cc1
            self.Hc = Hc1
            self.Oc = Oc1
            self.Nc = Nc1
            self.Sc = Sc1
        
        elif substratesNumber == 2 and (MixtureRule == "Volumen" or MixtureRule == "Peso"):
            if MixtureRule == "Volumen":
                wWater = WaterVolume                    #g
                wS1 = Volume1 * (rho1/1000)             #g
                wS2 = Volume2 * (rho2/1000)             #g
            
            elif MixtureRule == "Peso":
                wWater = WaterWeight
                wS1 = Weight1
                wS2 = Weight2

            Fraction1 = wS1/(wS1 + wS2 + wWater)          #Substrate fraction
            Fraction2 = wS2/(wS1 + wS2 + wWater)
            WaterFraction = wWater/(wS1 + wS2 + wWater)   #Water fraction

            self.TSini = Fraction1 * TS1 + Fraction2 * TS2
            self.VSini = Fraction1 * VS1 + Fraction2 * VS2
            self.rho = rho1 * Fraction1 + rho2 * Fraction2 + 1000 * WaterFraction
            dryWeight = (Fraction1 * 100)*(TS1/100) + (Fraction2 * 100)*(TS2/100)
            gC1 = (Fraction1 * 100) * Cc1; gC2 = (Fraction2 * 100) * Cc2
            gH1 = (Fraction1 * 100) * Hc1; gH2 = (Fraction2 * 100) * Hc2
            gO1 = (Fraction1 * 100) * Oc1; gO2 = (Fraction2 * 100) * Oc2
            gN1 = (Fraction1 * 100) * Nc1; gN2 = (Fraction2 * 100) * Nc2
            gS1 = (Fraction1 * 100) * Sc1; gS2 = (Fraction2 * 100) * Sc2
            self.Cc = (gC1 + gC2)/dryWeight
            self.Hc = (gH1 + gH2)/dryWeight
            self.Oc = (gO1 + gO2)/dryWeight
            self.Nc = (gN1 + gN2)/dryWeight
            self.Sc = (gS1 + gS2)/dryWeight
        
        elif substratesNumber == 3 and (MixtureRule == "Volumen" or MixtureRule == "Peso"):
            if MixtureRule == "Volumen":
                wWater = WaterVolume                    #g
                wS1 = Volume1 * (rho1/1000)             #g
                wS2 = Volume2 * (rho2/1000)             #g
                wS3 = Volume3 * (rho3/1000)             #g
            
            elif MixtureRule == "Peso":
                wWater = WaterWeight
                wS1 = Weight1
                wS2 = Weight2
                wS3 = Weight3
            
            Fraction1 = wS1/(wS1 + wS2 + wS3 + wWater)          #Substrate fraction
            Fraction2 = wS2/(wS1 + wS2 + wS3 + wWater)
            Fraction3 = wS3/(wS1 + wS2 + wS3 + wWater)
            WaterFraction = wWater/(wS1 + wS2 + wS3 + wWater)   #Water fraction

            self.TSini = Fraction1 * TS1 + Fraction2 * TS2 * Fraction3 * TS3
            self.VSini = Fraction1 * VS1 + Fraction2 * VS2 * Fraction3 * VS3
            self.rho = rho1 * Fraction1 + rho2 * Fraction2 + rho3 * Fraction3 + 1000 * WaterFraction
            dryWeight = (Fraction1 * 100)*(TS1/100) + (Fraction2 * 100)*(TS2/100) + (Fraction3 * 100)*(TS3/100)
            gC1 = (Fraction1 * 100) * Cc1; gC2 = (Fraction2 * 100) * Cc2; gC3 = (Fraction3 * 100) * Cc3
            gH1 = (Fraction1 * 100) * Hc1; gH2 = (Fraction2 * 100) * Hc2; gH3 = (Fraction3 * 100) * Hc3
            gO1 = (Fraction1 * 100) * Oc1; gO2 = (Fraction2 * 100) * Oc2; gO3 = (Fraction3 * 100) * Oc3
            gN1 = (Fraction1 * 100) * Nc1; gN2 = (Fraction2 * 100) * Nc2; gN3 = (Fraction3 * 100) * Nc3
            gS1 = (Fraction1 * 100) * Sc1; gS2 = (Fraction2 * 100) * Sc2; gS3 = (Fraction3 * 100) * Sc3
            self.Cc = (gC1 + gC2 + gC3)/dryWeight
            self.Hc = (gH1 + gH2 + gH3)/dryWeight
            self.Oc = (gO1 + gO2 + gO3)/dryWeight
            self.Nc = (gN1 + gN2 + gN3)/dryWeight
            self.Sc = (gS1 + gS2 + gS3)/dryWeight
        
        elif substratesNumber == 4 and (MixtureRule == "Volumen" or MixtureRule == "Peso"):
            if MixtureRule == "Volumen":
                wWater = WaterVolume                    #g
                wS1 = Volume1 * (rho1/1000)             #g
                wS2 = Volume2 * (rho2/1000)             #g
                wS3 = Volume3 * (rho3/1000)             #g
                wS4 = Volume4 * (rho4/1000)             #g
            
            elif MixtureRule == "Peso":
                wWater = WaterWeight
                wS1 = Weight1
                wS2 = Weight2
                wS3 = Weight3
                wS4 = Weight4
            
            Fraction1 = wS1/(wS1 + wS2 + wS3 + wS4 + wWater)          #Substrate fraction
            Fraction2 = wS2/(wS1 + wS2 + wS3 + wS4 + wWater)
            Fraction3 = wS3/(wS1 + wS2 + wS3 + wS4 + wWater)
            Fraction4 = wS4/(wS1 + wS2 + wS3 + wS4 + wWater)
            WaterFraction = wWater/(wS1 + wS2 + wS3 + wS4 + wWater)   #Water fraction
            
            self.TSini = Fraction1 * TS1 + Fraction2 * TS2 * Fraction3 * TS3 * Fraction4 * TS4
            self.VSini = Fraction1 * VS1 + Fraction2 * VS2 * Fraction3 * VS3 * Fraction4 * VS4
            self.rho = rho1 * Fraction1 + rho2 * Fraction2 + rho3 * Fraction3 + rho4 * Fraction4 + 1000 * WaterFraction
            dryWeight = (Fraction1 * 100)*(TS1/100) + (Fraction2 * 100)*(TS2/100) + (Fraction3 * 100)*(TS3/100) + (Fraction4 * 100)*(TS4/100)
            gC1 = (Fraction1 * 100) * Cc1; gC2 = (Fraction2 * 100) * Cc2; gC3 = (Fraction3 * 100) * Cc3; gC4 = (Fraction4 * 100) * Cc4
            gH1 = (Fraction1 * 100) * Hc1; gH2 = (Fraction2 * 100) * Hc2; gH3 = (Fraction3 * 100) * Hc3; gH4 = (Fraction4 * 100) * Hc4
            gO1 = (Fraction1 * 100) * Oc1; gO2 = (Fraction2 * 100) * Oc2; gO3 = (Fraction3 * 100) * Oc3; gO4 = (Fraction4 * 100) * Oc4
            gN1 = (Fraction1 * 100) * Nc1; gN2 = (Fraction2 * 100) * Nc2; gN3 = (Fraction3 * 100) * Nc3; gN4 = (Fraction4 * 100) * Nc4
            gS1 = (Fraction1 * 100) * Sc1; gS2 = (Fraction2 * 100) * Sc2; gS3 = (Fraction3 * 100) * Sc3; gS4 = (Fraction4 * 100) * Sc4
            self.Cc = (gC1 + gC2 + gC3 + gC4)/dryWeight
            self.Hc = (gH1 + gH2 + gH3 + gH4)/dryWeight
            self.Oc = (gO1 + gO2 + gO3 + gO4)/dryWeight
            self.Nc = (gN1 + gN2 + gN3 + gN4)/dryWeight
            self.Sc = (gS1 + gS2 + gS3 + gS4)/dryWeight

        self.molC = self.Cc*(1/12.01)
        self.molH = self.Hc*(1/1.01)
        self.molO = self.Oc*(1/16)
        self.molN = self.Nc*(1/14)
        self.molS = self.Sc*(1/32)

        n = self.molC
        a = self.molH
        b = self.molO
        c = self.molN
        d = self.molS

        def lcm(a,b):
                return a * b // gcd(a, b)
        
        numbers = [n, a, b, c, d]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        self.subindex = [int(num * common_denominator) for num in numbers]

        self.s_H2O = n-(a/4)-(b/2)+(3/4)*c+(d/2)
        self.s_CH4 = (n/2)+(a/8)-(b/4)-(3/8)*c-(d/4)
        self.s_CO2 = (n/2)-(a/8)+(b/4)+(3/8)*c-(d/4)
        self.s_NH3 = c
        self.s_H2S = d

        self.MW_sustrato = n*12.01+a*1.01+b*16+c*14+d*32
        self.Csus_ini_ST = (self.rho*(self.TSini/100))/self.MW_sustrato   #mol/L
        self.Csus_ini_SV = (self.rho*self.VSini/100)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini_SV
    
    def MixControl (self, MixVelocity, MixTime, DailyMixing):
        self.MixTime = MixTime*60
        TimeInterval = 24/DailyMixing

        if self.countermixing < self.MixTime:
            self.MixVelocity = MixVelocity
        else:
            self.MixVelocity = 0
        
        if self.countermixing > TimeInterval*3600:
            self.countermixing = 0

        self.countermixing = self.countermixing + self.tp
    
    def SubstrateFeed (self, Mode = "Time", Volume = 50, Time = 4, Inyections = 4, Q=1):  #from frontend requieres add entrance vble for sideA and SideB
        self.Volume_feed = Volume
        if Mode == "Time":
            TimeFeed = (Volume/Q)*60
            if self.counterfeed < TimeFeed:
                self.Qr = Q
            else:
                self.Qr = 0
            self.counterfeed = self.counterfeed + self.tp
            if self.counterfeed > Time*3600:
                self.counterfeed = 0

        if Mode == "Injection":
            IntervalTimeInyection = 24/Inyections
            TimeFeed = (Volume/Q)*60
            if self.counterfeed < TimeFeed:
                self.Qr = Q
            else:
                self.Qr = 0
            self.counterfeed = self.counterfeed + self.tp
            if self.counterfeed > IntervalTimeInyection*3600:
                self.counterfeed = 0 

        self.TotalVolFeed = self.TotalVolFeed + self.Qr*(self.tp/60)  
        if Mode == "NoDosing":
            self.Qr = 0
    
    def Reactor (self, model, pH, T, K1, K2=1, K3=1):
        
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.T = T
        self.pH = pH
        def pH_effect (parameter, model):
            if model == "Arrhenius":
                variable = np.exp(-((float(parameter)-7)**2)/(2*5**2))
            else:
                variable = np.exp(-((float(parameter)-7)**2)/(2*1**2))
            return variable
        
        def Temperature_effect (parameter):
            variable = np.exp(-((float(parameter)-45)**2)/(2*35**2))
            return variable
        
        def mixing_effect (parameter):
            if parameter < 10:
                variable = 1
            elif parameter >= 10:
                variable = np.random.uniform(0.99, 1)
            return float(variable)
        
        def differentialEquation (C, t, Vrxn, Q, Csusi, model, pH, T, K1, K2 = 1, K3 = 1):
            R = 8.314
            pH = pH_effect(pH, model)
            Teffect = Temperature_effect(T)
            Vrxn = Vrxn/1000
            Q = (Q/1000*60)
            if model == "Arrhenius":
                dC_dt = (Q/Vrxn)*(Csusi - C) - (C * K1 * np.exp (-(K2)/(R*T*pH)))/Vrxn
            if model == "ADM1":
                dC_dt = (Q/Vrxn)*(Csusi - C) - (C * K1 * pH * Teffect)/Vrxn
            return dC_dt
        
        def model_Gompertz(t, ym, U, L):
            y_t = ym * np.exp(-np.exp((U * np.e) / ym * (L - t) + 1))
            return y_t
        
        t_sim = [self.counterReactor, self.counterReactor + self.tp]
        
        if model == "Gompertz":
            if self.counterReactor == 0:
                 self.SV = (self.Csus_ini_SV * self.MW_sustrato) / self.rho
            else:
                self.SV = (self.Csus_res * self.MW_sustrato) / self.rho
            y_t = model_Gompertz(t_sim[-1], ym = K1, U = K2, L = K3)
            self.y_t = y_t * mixing_effect(self.MixVelocity) * pH_effect(pH, model) * Temperature_effect(T)
            self.Vmolar_CH4 = self.Thermo.Hgases(xCH4 = 1, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
            self.mol_CH4 = (self.y_t*self.SV*self.rho*(self.Vrxn/1000))/self.Vmolar_CH4
            mol_CH4_list = [self.mol_CH4_ini, self.mol_CH4]
            self.mol_CO2 = self.mol_CH4*(self.s_CO2/self.s_CH4)
            self.mol_H2S = self.mol_CH4*(self.s_H2S/self.s_CH4)
            self.mol_NH3 = self.mol_CH4*(self.s_NH3/self.s_CH4)
            self.mol_O2 = self.mol_O2 + (mol_CH4_list[-1] - mol_CH4_list[0])* np.random.uniform (0.02, 0.2) 
            self.mol_H2 = self.mol_H2 + (mol_CH4_list[-1] - mol_CH4_list[0]) * np.random.uniform (0, 0.00003)
            self.mol_H2O = self.mol_H2O + (mol_CH4_list[-1] - mol_CH4_list[0]) * np.random.normal(0.01, 0.1)
            self.mol_CH4_ini = self.mol_CH4
            print(mol_CH4_list)
            #Stochoimetric spent
            mol_SV = (self.Csus_ini_SV * (self.Vrxn/1000)) - (self.mol_CH4 * (1/self.s_CH4))
            self.Csus_res = mol_SV/(self.Vrxn/1000)
            self.SV = self.Csus_res * self.MW_sustrato
            try:
                self.OC = self.SV/(self.counterReactor/86400)
            except ZeroDivisionError:
                self.OC = 0
            
            self.x = (self.Csus_ini_SV - self.Csus_res)/self.Csus_ini_SV
            self.ST = (self.Csus_ini_ST*(1-self.x))*self.MW_sustrato

        else:

            if self.counterReactor == 0:
                self.Csus_ini = self.Csus_ini_SV
            else:
                self.Csus_ini = float(self.Csus_res[-1])
            self.Csus_res = odeint(differentialEquation, self.Csus_ini, t_sim, args = (self.Vrxn, self.Qr, self.Csus_ini_SV, model, pH, T, K1, K2, K3))
            self.SV = (self.Csus_ini*mixing_effect(self.MixVelocity))*self.MW_sustrato
            try:
                self.OC = self.SV/(self.counterReactor/86400)
            except ZeroDivisionError:
                self.OC = 0
            
            self.x = ((self.Csus_ini_SV - self.Csus_ini)/self.Csus_ini_SV)*(1+(1-mixing_effect(self.MixVelocity)))
            self.ST = (self.Csus_ini_ST*(1-self.x))*self.MW_sustrato
            self.mol_CH4 = (self.Csus_ini_SV*(self.Vrxn/1000))*(self.x)*(self.s_CH4)
            self.mol_CO2 = (self.Csus_ini_SV*(self.Vrxn/1000))*(self.x)*(self.s_CO2)
            self.mol_H2S = (self.Csus_ini_SV*(self.Vrxn/1000))*(self.x)*(self.s_H2S)
            self.mol_NH3 = (self.Csus_ini_SV*(self.Vrxn/1000))*(self.x)*(self.s_NH3)
            self.mol_O2 = self.mol_O2 + (float(self.Csus_res[0])-float(self.Csus_res[-1])) * (self.Vrxn/1000) * np.random.uniform (0.02, 0.2) 
            self.mol_H2 = self.mol_H2 + (float(self.Csus_res[0])-float(self.Csus_res[-1])) * (self.Vrxn/1000) * np.random.uniform (0, 0.00005)
            self.mol_H2O = self.mol_H2O + (float(self.Csus_res[0])-float(self.Csus_res[-1])) * (self.Vrxn/1000) * np.random.normal(0.01, 0.1)
            self.biogas_mol_dry = self.mol_CH4 + self.mol_CO2 + self.mol_H2S + self.mol_NH3 + self.mol_O2 + self.mol_H2
            self.biogas_mol_wet = self.mol_CH4 + self.mol_CO2 + self.mol_H2S + self.mol_NH3 + self.mol_O2 + self.mol_H2 + self.mol_H2O
        
        self.counterReactor = self.counterReactor + self.tp

    def CompoundsUnits (self):
        self.Vmolar_CH4 = self.Thermo.Hgases(xCH4 = 1, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_CO2 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 1, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_O2 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 1, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_H2S = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 1, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_H2 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 1, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_H2O = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 1, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]

        self.Vnormal_CH4 = (self.Vmolar_CH4 * self.mol_CH4) * 1000
        self.Vnormal_CO2 = (self.Vmolar_CO2 * self.mol_CO2) * 1000
        self.Vnormal_O2 = (self.Vmolar_O2 * self.mol_O2) * 1000
        self.Vnormal_H2S = (self.Vmolar_H2S * self.mol_H2S) * 1000
        self.Vnormal_H2 = (self.Vmolar_H2 * self.mol_H2) * 1000
        self.Vnormal_H2O = (self.Vmolar_H2O * self.mol_H2O) * 1000

        self.Vbiogas = self.Vnormal_CH4 + self.Vnormal_CO2 + self.Vnormal_O2 + self.Vnormal_H2S + self.Vnormal_H2
        try:
            self.x_CH4 = (self.Vnormal_CH4/self.Vbiogas)*100
            self.x_CO2 = (self.Vnormal_CO2/self.Vbiogas)*100
            self.x_O2 = (self.Vnormal_O2/self.Vbiogas)*100
            self.x_H2S = (self.Vnormal_H2S/self.Vbiogas)*1000000
            self.x_H2 = (self.Vnormal_H2/self.Vbiogas)*1000000
        except ZeroDivisionError:
            self.x_CH4 = 0
            self.x_CO2 = 0
            self.x_O2 = 0
            self.x_H2S = 0
            self.x_H2 = 0
    
    def PressurebyBiogas (self):
        P_std = 100000  #kPa
        R = 8.314 #J/mol K

        if self.Qr == 0:
            self.Vf1 = self.Vf
        else:
            self.Vf1 = self.Vf - (self.TotalVolFeed)
        print(self.Vf1)
        self.P_acum = (self.biogas_mol_dry * R * (self.T+273.15))/(self.Vf1/1000000) #Pa pressure due biogas prodcution dry
        self.P_acum = self.P_acum/6894.76

        if self.P_storage >= 15:
            self.n_ii_dry = self.biogas_mol_dry      #save the last value of biogas mol before release
            self.n_ii_wet = self.biogas_mol_wet

        self.n_i = (P_std*(self.Vf/1000000))/(R*(self.T+273.15))   #mol
        self.mol_storage = (self.n_i + (self.biogas_mol_wet - self.n_ii_wet))
        self.Pabs = (self.mol_storage * R * (self.T+273.15))/(self.Vf1/1000000)  #Pa  #pressure by increasing for inyection
        self.P_storage = abs(self.Pabs - P_std)/6894.76      #psi  due inyection and biogas realese 
            
        

        
        


        




        
        





        


            


          
        
#test class
# BMP = BMPModelOffline (Vrxn = 750, Vf = 750, tp = 30)
# BMP.MixtureCalculation(substratesNumber = 4, MixtureRule = "Peso", WaterFraction = 60, WaterVolume = 400, WaterWeight = 1000, 
#                        Fraction1 = 10, Volume1 = 100, Weight1 = 150, TS1 = 30, VS1 = 20, rho1 = 700, Cc1 = 43, Hc1 = 5, Oc1 = 30, Nc1 = 2, Sc1 = 0.21,
#                        Fraction2 = 10, Volume2 = 100, Weight2 = 100, TS2 = 20, VS2 = 15, rho2 = 600, Cc2 = 40, Hc2 = 6, Oc2 = 29, Nc2 = 2, Sc2 = 1,
#                        Fraction3 = 10, Volume3 = 100, Weight3 = 100, TS3 = 30, VS3 = 15, rho3 = 500, Cc3 = 40, Hc3 = 6, Oc3 = 29, Nc3 = 2, Sc3 = 1,
#                        Fraction4 = 10, Volume4 = 100, Weight4 = 200, TS4 = 10, VS4 = 8, rho4 = 500, Cc4 = 40, Hc4 = 6, Oc4 = 29, Nc4 = 2, Sc4 = 1)




        

