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
        
        
    
   
      
        
        
        
        
        
        
        
        

