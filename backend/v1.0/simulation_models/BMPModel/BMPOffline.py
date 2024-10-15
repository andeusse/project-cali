from math import gcd
from functools import reduce
from fractions import Fraction


class BMPModelOffline:
    def __init__ (self, Vrxn, Vf, tp):
        self.Vrxn = Vrxn       #mL
        self.Vf = Vf           #mL 
        self.tp = tp           #s

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
        self.Csus_ini = (self.rho*(self.TSini/100))/self.MW_sustrato
        self.Csus_ini_ST = (self.rho*self.TSini)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini




#test class
BMP = BMPModelOffline (Vrxn = 750, Vf = 750, tp = 30)
BMP.MixtureCalculation(substratesNumber = 4, MixtureRule = "Fracción", WaterFraction = 60, WaterVolume = 1, WaterWeight = 1, 
                       Fraction1 = 10, Volume1 = 50, Weight1 = 10, TS1 = 30, VS1 = 15, rho1 = 700, Cc1 = 43, Hc1 = 5, Oc1 = 30, Nc1 = 2, Sc1 = 0.21,
                       Fraction2 = 10, Volume2 = 50, Weight2 = 10, TS2 = 20, VS2 = 12, rho2 = 600, Cc2 = 40, Hc2 = 6, Oc2 = 29, Nc2 = 2, Sc2 = 1,
                       Fraction3 = 10, Volume3 = 50, Weight3 = 10, TS3 = 30, VS3 = 12, rho3 = 500, Cc3 = 40, Hc3 = 6, Oc3 = 29, Nc3 = 2, Sc3 = 1,
                       Fraction4 = 10, Volume4 = 50, Weight4 = 10, TS4 = 30, VS4 = 12, rho4 = 500, Cc4 = 40, Hc4 = 6, Oc4 = 29, Nc4 = 2, Sc4 = 1)
        
print(BMP.subindex)
print(BMP.TSini)
print(BMP.VSini)
print(BMP.Csus_ini)

        

