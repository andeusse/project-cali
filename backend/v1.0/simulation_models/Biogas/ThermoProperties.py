# -*- coding: utf-8 -*-
"""
Created on Tue May 30 21:24:07 2023

@author: Sergio
"""

# from thermo import ChemicalConstantsPackage, PRMIX, CEOSLiquid, CEOSGas, FlashPureVLS
from scipy.integrate import quad

class ThermoProperties:
    
    def __init__(self, name = "TermoProperties"):
        return

    def Hliq (self, T, P, Patm):
        self.T=T
        self.P=P
        self.Patm = Patm
        
        self.A=7.243E+01
        self.B=1.039E-02
        self.C=-1.497E-06
        
        self.MWH20 = 18.015  # Peso molecular del agua [kg/kmol]
        self.TcH2O = 647.19  #Temperatura critica del agua [K]
        self.PcH2O = 22055   #presion crítica del agua [kPa]
        self.wH2O = 0.34486  #Factor acentrico del agua
        self.R = 8.314       #[J/molK]
        
        #Temperatura de referencia
        self.TrH2O = self.T/self.TcH2O
        
        #Presion de referencia
        self.PrH2O = (self.P+self.Patm)/self.PcH2O
        
        #Factor de comresibilidad
        
        #Parametro BO
        self.BoH2O = 0.083-(0.422/pow(self.TrH2O, 1.6))
        
        #Parametro B1
        self.B1H2O = 0.139-(0.172/pow(self.TrH2O, 4.2))
        
        #Estimacion del factor de compresion
        self.ZH2O = 1+(self.BoH2O+self.wH2O*self.B1H2O)*(self.PrH2O/self.TrH2O)
        
        #Volumen específico del agua
        self.vH2O = (self.ZH2O*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        
        def integrate(A, B, C, Tref, T):
                result = quad(lambda x: A + B*x + C*x**2, Tref, T)
                I = (result[0])
                return I
        
        self.Tref = 273.15
        
        EntalpiaMolar = integrate(A=self.A, B=self.B, C=self.C, Tref=self.Tref, T=self.T ) + (self.P+self.Patm)*(self.vH2O/self.MWH20)
        
        return EntalpiaMolar
    
    def Hgases(self, xCH4, xCO2, xH2O, xO2, xN2, xH2S, xH2, P, Patm, T, xNH3=0):
        self.xCH4 = xCH4
        self.xCO2 = xCO2
        self.xH2O = xH2O
        self.xO2 = xO2
        self.xN2 = xN2
        self.xH2S = xH2S
        self.xH2 = xH2
        self.xNH3 = xNH3
        self.P = P
        self.Patm = Patm
        self.T = T+273.15
        
        # Pesos moleculares de los compuestos
        self.MWCH4 = 16.043  # Peso molecular del metano [kg/kmol]
        # Peso molecular del diÃÂ³xido de carbono [kg/kmol]
        self.MWCO2 = 44.01
        self.MWN2 = 28.014  # Peso molecular del nitrÃÂ³geno [kg/kmol]
        self.MWO2 = 31.999  # Peso molecular del oxÃÂ­geno [kg/kmol]
        self.MWH20 = 18.015  # Peso molecular del agua [kg/kmol]
        # Peso molecular del sulfuro de hidrÃ³geno [kg/kmol]
        self.MWH2S = 34.082
        self.MWH2 = 2.016
        self.MWNH3 = 17.031

        # Temperaturas crÃÂ­ticas de los compuestos
        self.TcCH4 = 190.564  # Temperatura crÃÂ­tica del metano [K]
        # Temperatura crÃÂ­tica del diÃÂ³xido de carbono [K]
        self.TcCO2 = 304.21
        self.TcN2 = 28.014  # Temperatura crÃÂ­tica del nitrÃÂ³geno [K]
        self.TcO2 = 154.58  # Temperatura crÃÂ­tica del oxÃÂ­geno [K]
        self.TcH2O = 647.19  # Temperatura crÃÂ­tica del agua [k]
        self.TcH2S = 373.53  # Temperatura critica del sulfuro de hidrogeno [K]
        self.TcH2 = 33.19
        self.TcNH3 = 405.65

        # Presiones crÃÂ­ticas
        self.PcCH4 = 4599  # presiÃÂ³n crÃÂ­tica del metano [kPa]
        # PresiÃÂ³n crÃÂ­tica del diÃÂ³xido de carbono [kPa]
        self.PcCO2 = 7383
        self.PcN2 = 3400  # PresiÃÂ³n crÃÂ­tica del nitrÃÂ³geno [kPa]
        self.PcO2 = 5043  # PresiÃÂ³n crÃÂ­tica del oxÃÂ­geno [kPa]
        self.PcH2O = 22055  # PresiÃÂ³n crÃÂ­tica del agua [kPa]
        self.PcH2S = 8962.9  # Presion critica del sulfuro de hidrogeno [kPa]
        self.PcH2 = 1313
        self.PcNH3 = 11280

        # Factores acÃÂ©ntricos
        self.wCH4 = 0.01153
        self.wCO2 = 0.22362
        self.wN2 = 0.03772
        self.wO2 = 0.022218
        self.wH2O = 0.34486
        self.wH2S = 0.09417
        self.wH2 = -0.21599
        self.wNH3 = 0.25261

        # EstimaciÃÂ³n del peso molecular de la mezcla
        self.MWgas = self.xCH4 * self.MWCH4 + self.xCO2 * self.MWCO2 + self.xH2O * \
            self.MWH20 + self.xO2 * self.MWO2 + self.xN2 * self.MWN2 + self.xH2S * self.MWH2S + self.xH2 * self.MWH2 + self.xNH3 * self.MWNH3

        # constante universal de ls gases
        self.R = 8.314  # [kJ/kmol-K]

        # Presiones de referencia
        self.PrCH4 = (self.P+self.Patm)/self.PcCH4
        self.PrCO2 = (self.P+self.Patm)/self.PcCO2
        self.PrN2 = (self.P+self.Patm)/self.PcN2
        self.PrO2 = (self.P+self.Patm)/self.PcO2
        self.PrH20 = (self.P+self.Patm)/self.PcH2O
        self.PrH2S = (self.P+self.Patm)/self.PcH2S
        self.PrH2 = (self.P+self.Patm)/self.PcH2
        self.PrNH3 = (self.P+self.Patm)/self.PcNH3

        # Temperaturas de referencia
        self.TrCH4 = self.T/self.TcCH4
        self.TrCO2 = self.T/self.TcCO2
        self.TrN2 = self.T/self.TcN2
        self.TrO2 = self.T/self.TcO2
        self.TrH2O = self.T/self.TcH2O
        self.TrH2S = self.T/self.TcH2S
        self.TrH2 = self.T/self.TcH2
        self.TrNH3 = self.T/self.TcNH3

        # Factor de ocmpresibilidad

        # parametro Bo
        self.BoCH4 = 0.083-(0.422/pow(self.TrCH4, 1.6))
        self.BoCO2 = 0.083-(0.422/pow(self.TrCO2, 1.6))
        self.BoN2 = 0.083-(0.422/pow(self.TrN2, 1.6))
        self.BoO2 = 0.083-(0.422/pow(self.TrO2, 1.6))
        self.BoH2O = 0.083-(0.422/pow(self.TrH2O, 1.6))
        self.BoH2S = 0.083-(0.422/pow(self.TrH2S, 1.6))
        self.BoH2 = 0.083-(0.422/pow(self.TrH2, 1.6))
        self.BoNH3 = 0.083-(0.422/pow(self.TrNH3, 1.6))

        # ParÃÂ¡metro B1
        self.B1CH4 = 0.139-(0.172/pow(self.TrCH4, 4.2))
        self.B1CO2 = 0.139-(0.172/pow(self.TrCO2, 4.2))
        self.B1N2 = 0.139-(0.172/pow(self.TrN2, 4.2))
        self.B1O2 = 0.139-(0.172/pow(self.TrO2, 4.2))
        self.B1H2O = 0.139-(0.172/pow(self.TrH2O, 4.2))
        self.B1H2S = 0.139-(0.172/pow(self.TrH2S, 4.2))
        self.B1H2 = 0.139-(0.172/pow(self.TrH2, 4.2))
        self.B1NH3 = 0.139-(0.172/pow(self.TrNH3, 4.2))

        # EstimaciÃÂ³n del factor de compresiÃÂ³n
        self.ZCH4 = 1+(self.BoCH4+self.wCH4*self.B1CH4)*(self.PrCH4/self.TrCH4)
        self.ZCO2 = 1+(self.BoCO2+self.wCO2*self.B1CO2)*(self.PrCO2/self.TrCO2)
        self.ZN2 = 1+(self.BoN2+self.wN2*self.B1N2)*(self.PrN2/self.TrN2)
        self.ZO2 = 1+(self.BoO2+self.wO2*self.B1O2)*(self.PrO2/self.TrO2)
        self.ZH2O = 1+(self.BoH2O+self.wH2O*self.B1H2O)*(self.PrH20/self.TrH2O)
        self.ZH2S = 1+(self.BoH2S+self.wH2S*self.B1H2S)*(self.PrH2S/self.TrH2S)
        self.ZH2 = 1+(self.BoH2+self.wH2*self.B1H2)*(self.PrH2/self.TrH2)
        self.ZNH3 = 1+(self.BoNH3+self.wNH3*self.B1NH3)*(self.PrNH3/self.TrNH3)

        # Volumen especÃÂ­fico
        self.vCH4 = (self.ZCH4*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        self.vCO2 = (self.ZCO2*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        self.vN2 = (self.ZN2*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        self.vO2 = (self.ZO2*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        self.vH2O = (self.ZH2O*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        self.vH2S = (self.ZH2S*self.R*self.T)/(self.P+self.Patm)  # [m3/kmol]
        self.vH2 = (self.ZH2*self.R*self.T)/(self.P+self.Patm)
        self.vNH3 = (self.ZNH3*self.R*self.T)/(self.P+self.Patm)

        # entalpias individuales
        self.TrefH = 25+273.15  # Temperatura de refrencia pra soluciÃÂ³n de integral

        def integrate(A, B, C, D, TrefH, T):
            result = quad(lambda x: A + B*x + C*x**2 + D*x**3, TrefH, T)
            I = (result[0])
            return I

        self.HCH4 = integrate(19.25, 5.213E-2, 1.197E-5, -1.132E-8,
                         self.TrefH, self.T) + (self.P+self.Patm)*(self.vCH4/self.MWCH4)  # [kJ/kmol]
        self.HCO2 = integrate(1.980E+1, 7.344E-2, -5.602E-5,
                         1.715E-8, self.TrefH, self.T) + (self.P+self.Patm)*(self.vCO2/self.MWCO2)
        self.HN2 = integrate(3.115E+1, -1.357E-2, 2.680E-5, -
                        1.168E-8, self.TrefH, self.T) + (self.P+self.Patm)*(self.vN2/self.MWN2)
        self.HO2 = integrate(2.811E+1, -3.680E-6, 1.746E-5, -
                        1.065E-8, self.TrefH, self.T) + (self.P+self.Patm)*(self.vO2/self.MWO2)
        self.HH2O = integrate(32.24, 1.924E-3, 1.055E-5, -3.596E-8,
                         self.TrefH, self.T) + (self.P+self.Patm)*(self.vH2O/self.MWH20)
        self.HH2S = integrate(3.194E+1, 1.436E-3, 2.432E-5, -
                         1.176E-8, self.TrefH, self.T) + (self.P+self.Patm)*(self.vH2S/self.MWH2S)
        self.HH2 = integrate(3.249, 1.436E-3, 2.432E-5, -
                         1.176E-8, self.TrefH, self.T) + (self.P+self.Patm)*(self.vH2S/self.MWH2S)  #Buscar en el libro 
        self.HNH3 = integrate(2.731E+1, 2.383E-2, 1.707E-5, -
                         1.185E-8, self.TrefH, self.T) + (self.P+self.Patm)*(self.vH2S/self.MWH2S) 
        

        # Entalpia mezcla

        self.Hbiogasmolar = self.xCH4*self.HCH4 + self.xCO2*self.HCO2 + self.xN2*self.HN2 + \
            self.xO2*self.HO2 + self.xH2O*self.HH2O + self.xH2S*self.HH2S + self.xH2*self.HH2 + self.xNH3*self.HNH3 # [kJ/kmol]
        
        self.Hbiogasmas = self.Hbiogasmolar/self.MWgas  # [kJ/kg]
        
        self.Volumenespbio = self.xCH4*self.vCH4 + self.xCO2*self.vCO2 + self.xN2*self.vN2 + \
            self.xO2*self.vO2 + self.xH2O*self.vH2O + self.xH2S*self.vH2S + self.xH2*self.vH2 + self.xNH3*self.vNH3  # [m^3/kmol]

        return self.Hbiogasmolar, self.Hbiogasmas, self.Volumenespbio
    
    def BiogasAbsoluteHumidity (self, RH, T):
         #Antoine Equation for saturation pressure estimation
         self.RH = RH
         self.T = T

         A = 8.140191
         B = 1810.94
         C = 244.485

         self.P_sat = 10**(A - B/(self.T + C))

         self.AH = (self.RH * self.P_sat)/(461.5 * self.T * 100)

         return self.AH
    
    def BiogasRelativeHumidity (self, nH2O, VnormalTotal, T):
         
         self.nH2O = nH2O
         self.Vnormal = VnormalTotal
         self.AH = self.nH2O/self.Vnormal
         self.T = T

         A = 8.140191
         B = 1810.94
         C = 244.485

         self.P_sat = 10**(A - B/(self.T + C))
         self.RH = (self.AH * self.P_sat)/(461.5 * self.T * 100)

         return self.RH

    def LHV (self, molCH4, molCO2, molH2S, molO2, molH2):
         
        molT = molCH4 + molCO2 + molH2S + molO2 + molH2

        if molT>0:
            self.xCH4 = molCH4/molT
            self.xCO2 = molCO2/molT
            self.xH2S = molH2S/molT
            self.xO2 = molO2/molT
            self.H2 = molH2/molT

            self.hf_CH4 = -74520     #[J/mol]
            self.hf_CO2 = -393510    #[J/mol]
            self.hf_H2S = -20630     #[J/mol]
            self.hf_O2 = 0
            self.hf_H2 = 0
            self.hf_N2 = 0
            self.hf_H2O = -241810    #[J/mol]

            n_CO2 = self.xCH4 + self.xCO2
            n_H2O = (4*self.xCH4 + 2*self.xCO2 + 2*self.xH2)/2
            alfa = (2*n_CO2 + n_H2O - 2*self.xCO2 - 2*self.xO2)/2
            n_N2 = alfa * 3.76

            LHV = (self.xCH4*self.hf_CH4 + self.xCO2*self.hf_CO2 + self.xH2S*self.hf_H2S + self.xO2*self.hf_O2 + self.xH2*self.hf_H2) + (alfa*self.hf_O2 + 3.76*alfa*self.hf_N2) - (n_CO2 * self.hf_CO2 + n_H2O * self.hf_H2O + n_N2 * self.hf_N2)

            Energia_J = LHV * molT
        
        else:
            LHV = 0
            Energia_J = 0

        return LHV, Energia_J    


    
   
      
        
        
        
        
        
        
        
        

