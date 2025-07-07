from tools import DBManager
from fractions import Fraction
from functools import reduce
from math import gcd
from simulation_models.Biogas import ThermoProperties
from simulation_models.Biogas import Biogas_Model_Simulation
import pandas as pd
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st
import time

class Biogas_Plant_prediction:
    def __init__ (self, plant, DB_IP, DB_Port, DB_Organization, DB_Bucket, DB_Token,
                  VG1, VG2, VG3):
        self.influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
        self.connectionState = self.influxDB.InfluxDBconnection()
        if not self.connectionState:
            raise ConnectionError(f"Database connection failed: {self.influxDB.ERROR_MESSAGE}")
        self.plant = plant
        self.Thermo = ThermoProperties.ThermoProperties()
        
        #Construction parameters
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3

        #Biogas_treatment
        self.mol_H2S_ads_acum = 0
        self.molH2S_acum_V107_i = 0
        self.mol_NH3_ads_acum = 0
        self.molNH3_acum_V107_i = 0
        self.mol_H2O_ads_acum = 0
        self.molH2O_acum_V107_i = 0

        #Global time
        self.GlobalTime = 0
    
    def get_data(self):
        attempts = 1
        while attempts <= 5:
            try:
                self.query1 = self.influxDB.QueryCreator(measurement="Planta_Biogas", device="interfaz", type=5)
                self.Datainterfaz = pd.concat(self.influxDB.InfluxDBreader(query = self.query1), ignore_index=True)
                # self.Datainterfaz = self.influxDB.InfluxDBreader(query = self.query1)
                self.Datainterfaz.set_index("_field", inplace = True)
                self.Operation_mode = self.Datainterfaz["_value"]["ciclo"]
                self.Operation_mode = self.Operation_mode.iloc[-1]
                break
            except:
                attempts += 1
        
        attempts = 1
        while attempts <= 5:
            try:
                self.query2 = self.influxDB.QueryCreator(measurement="Planta_Biogas", train_time=str(10), type=4)
                print("acquiring Data from sensors...")
                # DataPlant = pd.concat(self.influxDB.InfluxDBreader(query = self.query2), ignore_index=True)
                DataPlant = self.influxDB.InfluxDBreader(query = self.query2)
                print("Instrumentation Data acquired...")
                DataPlant.set_index("_field", inplace = True)
                self.DataPlanti = DataPlant
                break
            except:
                attempts += 1
        # print(self.Datainterfaz)
        # self.DataPlanti.to_csv(r'.\test.csv')
        
    def substrate_conditions (self, Cc, Ch, Co, Cn, Cs, ST, SV, rho, inputSubstrateConditions):
        if inputSubstrateConditions == "True":
            self.plant.Substrate_conditions(Cc = Cc, Ch = Ch, Co = Co, Cn = Cn, Cs = Cs, ST = ST, SV = SV, rho = rho)
        
            self.n = self.plant.n
            self.a = self.plant.a
            self.b = self.plant.b
            self.c = self.plant.c
            self.d = self.plant.d
        
            self.s_H2O = self.plant.s_H2O
            self.s_CH4 = self.plant.s_CH4
            self.s_CO2 = self.plant.s_CO2
            self.s_NH3 = self.plant.s_NH3
            self.s_H2S = self.plant.s_H2S
        
            #molar concentration
            self.MW_sustrato = self.plant.MW_sustrato                                 #[g/mol]
            self.Csus_ini = self.plant.Csus_ini                                 #[mol/L] 
            self.Csus_ini_ST = self.plant.Csus_ini_ST                         #[mol/L](self.rho*(self.ST/100))/self.MW_sustrato                         #[mol/L]
            self.Csus_fixed = self.plant.Csus_fixed                            #[mol/L] 

            self.Csv = self.plant.Csv                                           #[g/L] 
            self.Cst = self.plant.Cst                                            #[g/L] 

        else:
            self.SN = self.Datainterfaz["_value"]["MNS"]
            #Water proportion
            self.MPH = self.Datainterfaz["_value"]["MPH"]    #MPH: Water proportion in the mix

            if self.SN  == 4:    
                #Substrate 1 Characterization
                self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
                self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
                self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
                self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
                self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
                self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
                self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
                self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
                self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
                self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
                
                #Substrate 2 Characterization
                self.MST2 = self.Datainterfaz["_value"]["ST2"]   #ST2: Substrate 2 name
                self.MP2 = self.Datainterfaz["_value"]["MP2"]    #MP2: substrate 2 proportion in mix
                self.ST2 = self.Datainterfaz["_value"]["MST2"]   #MST2: Total solids of substrate 2
                self.SV2 = self.Datainterfaz["_value"]["MSV2"]   #MSV2: Volatile solids of substrate 2
                self.Cc2 = self.Datainterfaz["_value"]["MCc2"]   #MCc2: Carbon concentration substrate 2
                self.Ch2 = self.Datainterfaz["_value"]["MCh2"]   #MCh2: hydrogen concentration substrate 2 
                self.Co2 = self.Datainterfaz["_value"]["MCo2"]   #MCo2: oxygen concentration substrate 2
                self.Cn2 = self.Datainterfaz["_value"]["MCn2"]   #MCh2: nytrogen concentration substrate 2
                self.Cs2 = self.Datainterfaz["_value"]["MCs2"]   #MCh2: sulfur concentration substrate 2
                self.rho2 = self.Datainterfaz["_value"]["Md2"]   #Md2: substrate density
                
                #Substrate 3 Characterization
                self.MST3 = self.Datainterfaz["_value"]["ST3"]   #ST3: Substrate 3 name
                self.MP3 = self.Datainterfaz["_value"]["MP3"]    #MP3: substrate 3 proportion in mix
                self.ST3 = self.Datainterfaz["_value"]["MST3"]   #MST3: Total solids of substrate 3
                self.SV3 = self.Datainterfaz["_value"]["MSV3"]   #MSV3: Volatile solids of substrate 3
                self.Cc3 = self.Datainterfaz["_value"]["MCc3"]   #MCc3: Carbon concentration substrate 3
                self.Ch3 = self.Datainterfaz["_value"]["MCh3"]   #MCh3: hydrogen concentration substrate 3 
                self.Co3 = self.Datainterfaz["_value"]["MCo3"]   #MCo3: oxygen concentration substrate 3
                self.Cn3 = self.Datainterfaz["_value"]["MCn3"]   #MCh3: nytrogen concentration substrate 3
                self.Cs3 = self.Datainterfaz["_value"]["MCs3"]   #MCh3: sulfur concentration substrate 3
                self.rho3 = self.Datainterfaz["_value"]["Md3"]   #Md3: substrate density
                
                #Substrate 4 Characterization
                self.MST4 = self.Datainterfaz["_value"]["ST4"]   #ST4: Substrate 4 name
                self.MP4 = self.Datainterfaz["_value"]["MP4"]    #MP4: substrate 4 proportion in mix
                self.ST4 = self.Datainterfaz["_value"]["MST4"]   #MST4: Total solids of substrate 4
                self.SV4 = self.Datainterfaz["_value"]["MSV4"]   #MSV4: Volatile solids of substrate 4
                self.Cc4 = self.Datainterfaz["_value"]["MCc4"]   #MCc4: Carbon concentration substrate 4
                self.Ch4 = self.Datainterfaz["_value"]["MCh4"]   #MCh4: hydrogen concentration substrate 4 
                self.Co4 = self.Datainterfaz["_value"]["MCo4"]   #MCo4: oxygen concentration substrate 4
                self.Cn4 = self.Datainterfaz["_value"]["MCn4"]   #MCh4: nytrogen concentration substrate 4
                self.Cs4 = self.Datainterfaz["_value"]["MCs4"]   #MCh4: sulfur concentration substrate 4
                self.rho4 = self.Datainterfaz["_value"]["Md4"]   #Md4: substrate density
                
                #Proximate analysis for mixture
                self.ST = (self.ST1*self.MP1 + self.ST2*self.MP2 + self.ST3*self.MP3 + self.ST4*self.MP4)/100
                self.SV = (self.SV1*self.MP1 + self.SV2*self.MP2 + self.SV3*self.MP3 + self.SV4*self.MP4)/100
                self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + self.rho3*self.MP3 + self.rho4*self.MP4 + 1000*self.MPH)
                
                gCc1 = self.Cc1 * self.MP1 * self.ST1; gCc2 = self.Cc2 * self.MP2 * self.ST2; gCc3 = self.Cc3 * self.MP3 * self.ST3; gCc4 = self.Cc4 * self.MP4 * self.ST4    #Carbon content
                gCh1 = self.Ch1 * self.MP1 * self.ST1; gCh2 = self.Ch2 * self.MP2 * self.ST2; gCh3 = self.Ch3 * self.MP3 * self.ST3; gCh4 = self.Ch4 * self.MP4 * self.ST4    #hydrogen content
                gCo1 = self.Co1 * self.MP1 * self.ST1; gCo2 = self.Co2 * self.MP2 * self.ST2; gCo3 = self.Co3 * self.MP3 * self.ST3; gCo4 = self.Co4 * self.MP4 * self.ST4    #oxygen content
                gCn1 = self.Cn1 * self.MP1 * self.ST1; gCn2 = self.Cn2 * self.MP2 * self.ST2; gCn3 = self.Cn3 * self.MP3 * self.ST3; gCn4 = self.Cn4 * self.MP4 * self.ST4    #nitrogen content
                gCs1 = self.Cs1 * self.MP1 * self.ST1; gCs2 = self.Cs2 * self.MP2 * self.ST2; gCs3 = self.Cs3 * self.MP3 * self.ST3; gCs4 = self.Cs4 * self.MP4 * self.ST4    #sulfur content
                
                #Elemental analysis for mixture
                self.Cc = ((gCc1 + gCc2 + gCc3 + gCc4) / self.ST)/100
                self.Ch = ((gCh1 + gCh2 + gCh3 + gCh4) / self.ST)/100
                self.Co = ((gCo1 + gCo2 + gCo3 + gCo4) / self.ST)/100
                self.Cn = ((gCn1 + gCn2 + gCn3 + gCn4) / self.ST)/100
                self.Cs = ((gCs1 + gCs2 + gCs3 + gCs4) / self.ST)/100
                        
            elif self.SN  == 3:
                #Substrate 1 Characterization
                self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
                self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
                self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
                self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
                self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
                self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
                self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
                self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
                self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
                self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
                
                #Substrate 2 Characterization
                self.MST2 = self.Datainterfaz["_value"]["ST2"]   #ST2: Substrate 2 name
                self.MP2 = self.Datainterfaz["_value"]["MP2"]    #MP2: substrate 2 proportion in mix
                self.ST2 = self.Datainterfaz["_value"]["MST2"]   #MST2: Total solids of substrate 2
                self.SV2 = self.Datainterfaz["_value"]["MSV2"]   #MSV2: Volatile solids of substrate 2
                self.Cc2 = self.Datainterfaz["_value"]["MCc2"]   #MCc2: Carbon concentration substrate 2
                self.Ch2 = self.Datainterfaz["_value"]["MCh2"]   #MCh2: hydrogen concentration substrate 2 
                self.Co2 = self.Datainterfaz["_value"]["MCo2"]   #MCo2: oxygen concentration substrate 2
                self.Cn2 = self.Datainterfaz["_value"]["MCn2"]   #MCh2: nytrogen concentration substrate 2
                self.Cs2 = self.Datainterfaz["_value"]["MCs2"]   #MCh2: sulfur concentration substrate 2
                self.rho2 = self.Datainterfaz["_value"]["Md2"]   #Md2: substrate density
                
                #Substrate 3 Characterization
                self.MST3 = self.Datainterfaz["_value"]["ST3"]   #ST3: Substrate 3 name
                self.MP3 = self.Datainterfaz["_value"]["MP3"]    #MP3: substrate 3 proportion in mix
                self.ST3 = self.Datainterfaz["_value"]["MST3"]   #MST3: Total solids of substrate 3
                self.SV3 = self.Datainterfaz["_value"]["MSV3"]   #MSV3: Volatile solids of substrate 3
                self.Cc3 = self.Datainterfaz["_value"]["MCc3"]   #MCc3: Carbon concentration substrate 3
                self.Ch3 = self.Datainterfaz["_value"]["MCh3"]   #MCh3: hydrogen concentration substrate 3 
                self.Co3 = self.Datainterfaz["_value"]["MCo3"]   #MCo3: oxygen concentration substrate 3
                self.Cn3 = self.Datainterfaz["_value"]["MCn3"]   #MCh3: nytrogen concentration substrate 3
                self.Cs3 = self.Datainterfaz["_value"]["MCs3"]   #MCh3: sulfur concentration substrate 3
                self.rho3 = self.Datainterfaz["_value"]["Md3"]   #Md3: substrate density
                            
                #Proximate analysis for mixture
                self.ST = (self.ST1*self.MP1 + self.ST2*self.MP2 + self.ST3*self.MP3)/100
                self.SV = (self.SV1*self.MP1 + self.SV2*self.MP2 + self.SV3*self.MP3)/100
                self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + self.rho3*self.MP3 + 1000*self.MPH)
                
                gCc1 = self.Cc1 * self.MP1 * self.ST1; gCc2 = self.Cc2 * self.MP2 * self.ST2; gCc3 = self.Cc3 * self.MP3 * self.ST3    #Carbon content
                gCh1 = self.Ch1 * self.MP1 * self.ST1; gCh2 = self.Ch2 * self.MP2 * self.ST2; gCh3 = self.Ch3 * self.MP3 * self.ST3    #hydrogen content
                gCo1 = self.Co1 * self.MP1 * self.ST1; gCo2 = self.Co2 * self.MP2 * self.ST2; gCo3 = self.Co3 * self.MP3 * self.ST3    #oxygen content
                gCn1 = self.Cn1 * self.MP1 * self.ST1; gCn2 = self.Cn2 * self.MP2 * self.ST2; gCn3 = self.Cn3 * self.MP3 * self.ST3    #nitrogen content
                gCs1 = self.Cs1 * self.MP1 * self.ST1; gCs2 = self.Cs2 * self.MP2 * self.ST2; gCs3 = self.Cs3 * self.MP3 * self.ST3    #sulfur content
                
                #Elemental analysis for mixture
                self.Cc = ((gCc1 + gCc2 + gCc3) / self.ST)/100
                self.Ch = ((gCh1 + gCh2 + gCh3) / self.ST)/100
                self.Co = ((gCo1 + gCo2 + gCo3) / self.ST)/100
                self.Cn = ((gCn1 + gCn2 + gCn3) / self.ST)/100
                self.Cs = ((gCs1 + gCs2 + gCs3) / self.ST)/100
            
            elif self.SN  == 2:
                #Substrate 1 Characterization
                self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
                self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
                self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
                self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
                self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
                self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
                self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
                self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
                self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
                self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
                
                #Substrate 2 Characterization
                self.MST2 = self.Datainterfaz["_value"]["ST2"]   #ST2: Substrate 2 name
                self.MP2 = self.Datainterfaz["_value"]["MP2"]    #MP2: substrate 2 proportion in mix
                self.ST2 = self.Datainterfaz["_value"]["MST2"]   #MST2: Total solids of substrate 2
                self.SV2 = self.Datainterfaz["_value"]["MSV2"]   #MSV2: Volatile solids of substrate 2
                self.Cc2 = self.Datainterfaz["_value"]["MCc2"]   #MCc2: Carbon concentration substrate 2
                self.Ch2 = self.Datainterfaz["_value"]["MCh2"]   #MCh2: hydrogen concentration substrate 2 
                self.Co2 = self.Datainterfaz["_value"]["MCo2"]   #MCo2: oxygen concentration substrate 2
                self.Cn2 = self.Datainterfaz["_value"]["MCn2"]   #MCh2: nytrogen concentration substrate 2
                self.Cs2 = self.Datainterfaz["_value"]["MCs2"]   #MCh2: sulfur concentration substrate 2
                self.rho2 = self.Datainterfaz["_value"]["Md2"]   #Md2: substrate density
                                        
                #Proximate analysis for mixture
                self.ST = (self.ST1*self.MP1 + self.ST2*self.MP2 )/100
                self.SV = (self.SV1*self.MP1 + self.SV2*self.MP2 )/100
                self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + 1000*self.MPH)
                
                gCh1 = self.Ch1 * self.MP1 * self.ST1; gCh2 = self.Ch2 * self.MP2 * self.ST2    #hydrogen content
                gCc1 = self.Cc1 * self.MP1 * self.ST1; gCc2 = self.Cc2 * self.MP2 * self.ST2    #Carbon content
                gCo1 = self.Co1 * self.MP1 * self.ST1; gCo2 = self.Co2 * self.MP2 * self.ST2    #oxygen content
                gCn1 = self.Cn1 * self.MP1 * self.ST1; gCn2 = self.Cn2 * self.MP2 * self.ST2    #nitrogen content
                gCs1 = self.Cs1 * self.MP1 * self.ST1; gCs2 = self.Cs2 * self.MP2 * self.ST2    #sulfur content
                
                #Elemental analysis for mixture
                self.Cc = ((gCc1 + gCc2) / self.ST)/100
                self.Ch = ((gCh1 + gCh2) / self.ST)/100
                self.Co = ((gCo1 + gCo2) / self.ST)/100
                self.Cn = ((gCn1 + gCn2) / self.ST)/100
                self.Cs = ((gCs1 + gCs2) / self.ST)/100
            
            elif self.SN  == 1:
                #Substrate 1 Characterization
                self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
                self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
                self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
                self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
                self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
                self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
                self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
                self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
                self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
                self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
                                                            
                #Proximate analysis for mixture
                self.ST = (self.ST1*self.MP1 )/100
                self.SV = (self.SV1*self.MP1 )/100
                self.rho = (self.rho1*self.MP1 + 1000*self.MPH)
                
                gCh1 = self.Ch1 * self.MP1 * self.ST1   #hydrogen content
                gCc1 = self.Cc1 * self.MP1 * self.ST1   #Carbon content
                gCo1 = self.Co1 * self.MP1 * self.ST1   #oxygen content
                gCn1 = self.Cn1 * self.MP1 * self.ST1   #nitrogen content
                gCs1 = self.Cs1 * self.MP1 * self.ST1   #sulfur content
                
                #Elemental analysis for mixture
                self.Cc = ((gCc1) / self.ST)/100
                self.Ch = ((gCh1) / self.ST)/100
                self.Co = ((gCo1) / self.ST)/100
                self.Cn = ((gCn1) / self.ST)/100
                self.Cs = ((gCs1) / self.ST)/100
            
            self.molC = self.Cc*(1/12.01)
            self.molH = self.Ch*(1/1.01)
            self.molO = self.Co*(1/16)
            self.molN = self.Cn*(1/14)
            self.molS = self.Cs*(1/32)
            
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

            self.n = self.subindex[0]
            self.a = self.subindex[1]
            self.b = self.subindex[2]
            self.c = self.subindex[3]
            self.d = self.subindex[4]
            
            self.s_H2O = self.n-(self.a/4)-(self.b/2)+(3/4)*c+(self.d/2)
            self.s_CH4 = (self.n/2)+(self.a/8)-(self.b/4)-(3/8)*self.c-(self.d/4)
            self.s_CO2 = (self.n/2)-(self.a/8)+(self.b/4)+(3/8)*self.c-(self.d/4)
            self.s_NH3 = self.c
            self.s_H2S = self.d 
            
            #sustrate
            self.MW_sustrato = self.n*12.01 + self.a*1.01 + self.b*16 + self.c*14 + self.d*32
            self.Cst_sus = (self.rho*(self.ST))/self.MW_sustrato
            self.Cst_sus_gl = (self.rho*(self.ST))
            self.Csv_sus = (self.rho*(self.SV))/self.MW_sustrato
            self.Csv_sus_gl = (self.rho*(self.SV))
            self.Cfixed = self.Cst_sus - self.Csv_sus
            self.plant.Substrate_conditions (Cc = self.Cc, Ch = self.Ch, Co = self.Co, Cn = self.Cn, Cs = self.Cs, ST = self.ST*100, SV = self.SV*100, rho = self.rho)
            self.Csus_ini = self.plant.Csus_ini
            
    def ProcessData (self):    #runs once
        #V101
        try:
            self.Pacum_V101 = float(self.Datainterfaz.loc["PAcumV101",["_value"]].iloc[-1])
            self.Pstorage_V101 = float(self.DataPlanti.loc["PT-103", ["_value"]].iloc[-1].iloc[0])
            self.Vacum_V101 = float(self.Datainterfaz.loc["Volumen_bioV101",["_value"]].iloc[-1])
            self.T_V101 = float(self.DataPlanti.loc["TT-103", ["_value"]].iloc[-1].iloc[0])
            self.xCH4_V101 = float(self.DataPlanti.loc["AT-103A-CH4", ["_value"]].iloc[-1].iloc[0])
            self.xCO2_V101 = float(self.DataPlanti.loc["AT-103A-CO2", ["_value"]].iloc[-1].iloc[0])
            self.xO2_V101 = float(self.DataPlanti.loc["AT-103A-O2", ["_value"]].iloc[-1].iloc[0])
            self.xH2_V101 = float(self.DataPlanti.loc["AT-103A-H2", ["_value"]].iloc[-1].iloc[0])
            self.xH2S_V101 = float(self.DataPlanti.loc["AT-103A-H2S", ["_value"]].iloc[-1].iloc[0])
            self.HR_V101 = float(self.DataPlanti.loc["AT-103B", ["_value"]].iloc[-1].iloc[0])
        except KeyError:
            self.Pacum_V101 = 0
            self.Vacum_V101 = 0
            self.Pstorage_V102 = 0
            self.T_V101 = 35.0
            self.xCH4_V101 = self.s_CH4/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.xCO2_V101 = self.s_CO2/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.xO2_V101 = self.xCH4_V101 * 0.01
            self.xH2_V101 = self.xCH4_V101 * 0.0000001
            self.xH2S_V101 = self.s_H2S/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.HR_V101 = 50
        #Moles estimation
        self.nbiogas_V101_acum_i = ((self.Pacum_V101*6894.76) * (self.VG1/1000))/(8.314*(self.T_V101+273.15))
        self.nCH4_V101_acum_i = self.nbiogas_V101_acum_i * (self.xCH4_V101/100)
        self.nCO2_V101_acum_i = self.nbiogas_V101_acum_i * (self.xCO2_V101/100)
        self.nO2_V101_acum_i = self.nbiogas_V101_acum_i * (self.xO2_V101/100)
        self.nH2_V101_acum_i = self.nbiogas_V101_acum_i * (self.xH2_V101/1000000)
        self.nH2S_V101_acum_i = self.nbiogas_V101_acum_i * (self.xH2S_V101/1000000)
        self.nNH3_V101_acum_i = self.nCH4_V101_acum_i * (1/self.s_CH4)
        #Water
        AbsoluteHumidity_V101 = self.Thermo.BiogasAbsoluteHumidity(RH = self.HR_V101/100, T=self.T_V101)
        self.nH2O_V101_acum_i = AbsoluteHumidity_V101 * (self.Vacum_V101)
        
        #V102
        try:
            self.Pacum_V102 = float(self.Datainterfaz.loc["PAcumV102",["_value"]].iloc[-1])
            self.Pstorage_V102 = float(self.DataPlanti.loc["PT-104", ["_value"]].iloc[-1].iloc[0])
            self.Vacum_V102 = float(self.Datainterfaz.loc["Volumen_bioV102",["_value"]].iloc[-1])
            self.T_V102 = float(self.DataPlanti.loc["TT-104", ["_value"]].iloc[-1].iloc[0])
            self.xCH4_V102 = float(self.DataPlanti.loc["AT-104A-CH4", ["_value"]].iloc[-1].iloc[0])
            self.xCO2_V102 = float(self.DataPlanti.loc["AT-104A-CO2", ["_value"]].iloc[-1].iloc[0])
            self.xO2_V102 = float(self.DataPlanti.loc["AT-104A-O2", ["_value"]].iloc[-1].iloc[0])
            self.xH2_V102 = float(self.DataPlanti.loc["AT-104A-H2", ["_value"]].iloc[-1].iloc[0])
            self.xH2S_V102 = float(self.DataPlanti.loc["AT-104A-H2S", ["_value"]].iloc[-1].iloc[0])
            self.HR_V102 = float(self.DataPlanti.loc["AT-104B", ["_value"]].iloc[-1].iloc[0])
        except KeyError:
            self.Pacum_V102 = 0
            self.Vacum_V102 = 0
            self.Pstorage_V102 = 0
            self.T_V102 = 35.0
            self.xCH4_V102 = self.s_CH4/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.xCO2_V102 = self.s_CO2/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.xO2_V102 = self.xCH4_V102 * 0.01
            self.xH2_V102 = self.xCH4_V102 * 0.0000001
            self.xH2S_V102 = self.s_H2S/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.HR_V102 = 50
        #Moles estimation
        self.nbiogas_V102_acum_i = ((self.Pacum_V102*6894.76) * (self.VG2/1000))/(8.314*(self.T_V101+273.15))
        self.nCH4_V102_acum_i = self.nbiogas_V102_acum_i * (self.xCH4_V102/100)
        self.nCO2_V102_acum_i = self.nbiogas_V102_acum_i * (self.xCO2_V102/100)
        self.nO2_V102_acum_i = self.nbiogas_V102_acum_i * (self.xO2_V102/100)
        self.nH2_V102_acum_i = self.nbiogas_V102_acum_i * (self.xH2_V102/1000000)
        self.nH2S_V102_acum_i = self.nbiogas_V102_acum_i * (self.xH2S_V102/1000000)
        self.nNH3_V102_acum_i = self.nCH4_V102_acum_i * (1/self.s_CH4)
        #Water
        AbsoluteHumidity_V102 = self.Thermo.BiogasAbsoluteHumidity(RH = self.HR_V102/100, T=self.T_V102)
        self.nH2O_V102_acum_i = AbsoluteHumidity_V102 * (self.Vacum_V102)
        self.biogas_storage_mol_V102 = self.nCH4_V102_acum_i + self.nCO2_V102_acum_i + self.nO2_V102_acum_i + self.nH2_V102_acum_i + self.nH2S_V102_acum_i + self.nNH3_V102_acum_i + self.nH2O_V102_acum_i
        
        #V107
        try:
            self.Pacum_V107 = float(self.Datainterfaz.loc["PAcumV107",["_value"]].iloc[-1])
            self.Pstorage_V107 = float(self.DataPlanti.loc["PT-105", ["_value"]].iloc[-1].iloc[0])
            self.Vacum_V107 = float(self.Datainterfaz.loc["Volumen_bioV107",["_value"]].iloc[-1])
            self.T_V107 = float(self.DataPlanti.loc["TT-105", ["_value"]].iloc[-1].iloc[0])
            self.xCH4_V107 = float(self.DataPlanti.loc["AT-105A-CH4", ["_value"]].iloc[-1].iloc[0])
            self.xCO2_V107 = float(self.DataPlanti.loc["AT-105A-CO2", ["_value"]].iloc[-1].iloc[0])
            self.xO2_V107 = float(self.DataPlanti.loc["AT-105A-O2", ["_value"]].iloc[-1].iloc[0])
            self.xH2_V107 = float(self.DataPlanti.loc["AT-105A-H2", ["_value"]].iloc[-1].iloc[0])
            self.xH2S_V107 = float(self.DataPlanti.loc["AT-105A-H2S", ["_value"]].iloc[-1].iloc[0])
            self.HR_V107 = float(self.DataPlanti.loc["AT-105B", ["_value"]].iloc[-1].iloc[0])
        except KeyError:
            self.Pacum_V107 = 0
            self.Vacum_V107 = 0
            self.Pstorage_V107 = 0
            self.T_V107 = 35.0
            self.xCH4_V107 = self.s_CH4/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.xCO2_V107 = self.s_CO2/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.xO2_V107 = self.xCH4_V107 * 0.01
            self.xH2_V107 = self.xCH4_V107 * 0.0000001
            self.xH2S_V107 = self.s_H2S/(self.s_CH4 + self.s_CO2 + self.s_H2O + self.s_NH3 + self.s_H2S)
            self.HR_V107 = 50
        #Moles estimation
        self.nbiogas_V107_acum_i = ((self.Pacum_V107*6894.76) * (self.VG3/1000))/(8.314*(self.T_V101+273.15))
        self.nCH4_V107_acum_i = self.nbiogas_V107_acum_i * (self.xCH4_V107/100)
        self.nCO2_V107_acum_i = self.nbiogas_V107_acum_i * (self.xCO2_V107/100)
        self.nO2_V107_acum_i = self.nbiogas_V107_acum_i * (self.xO2_V107/100)
        self.nH2_V107_acum_i = self.nbiogas_V107_acum_i * (self.xH2_V107/1000000)
        self.nH2S_V107_acum_i = self.nbiogas_V107_acum_i * (self.xH2S_V107/1000000)
        self.nNH3_V107_acum_i = self.nCH4_V107_acum_i * (1/self.s_CH4)
        #Water
        AbsoluteHumidity_V107 = self.Thermo.BiogasAbsoluteHumidity(RH = self.HR_V107/100, T=self.T_V107)
        self.nH2O_V107_acum_i = AbsoluteHumidity_V107 * (self.Vacum_V107)
        self.biogas_storage_mol_V107 = self.nCH4_V107_acum_i + self.nCO2_V107_acum_i + self.nO2_V107_acum_i + self.nH2_V107_acum_i + self.nH2S_V107_acum_i + self.nNH3_V107_acum_i + self.nH2O_V107_acum_i

    def Pump104(self, TRH, FT_P104, TTO_P104, time_accelerator, inputPump104):
        if inputPump104 == True:
            self.plant.Pump104(TRH = TRH, FT_P104 = FT_P104, TTO_P104 = TTO_P104, time_accelerator=time_accelerator)
            self.Q_P104_Lh = self.plant.Q_P104_Lh
            self.Q_P104v = self.plant.Q_P104v
        else:
            try:
                TRH = self.Datainterfaz["_values"]["MTRH"]
                FT_P104 = self.Datainterfaz["_value"]["MFTP104"]
                TTO_P104 = self.Datainterfaz["_value"]["MTTOP104"]
            except KeyError:
                TRH = TRH
                FT_P104 = FT_P104
                TTO_P104 = TTO_P104
            self.plant.Pump104(TRH = TRH, FT_P104 = FT_P104, TTO_P104 = TTO_P104, time_accelerator=time_accelerator)
            self.Q_P104_Lh = self.plant.Q_P104_Lh
            self.Q_P104v = self.plant.Q_P104v
    
    def Pump101 (self, FT_P101, TTO_P101, Q_P101, inputPump101):
        if inputPump101 == True:
            self.plant.Pump101(FT_P101 = FT_P101, TTO_P101 = TTO_P101, Q_P101 = Q_P101)
            self.Q_P101 = self.plant.Q_P101
        else:
            try:
                FT_P101 = self.Datainterfaz["_value"]["MFTP101"]
                TTO_P101 = self.Datainterfaz["_value"]["MTTOP101"]
                Q_P101 = self.Datainterfaz["_value"]["MQP101"]
            except KeyError: 
                FT_P101 = FT_P101
                TTO_P101 = TTO_P101
                Q_P101 = Q_P101
            self.plant.Pump101(FT_P101 = FT_P101, TTO_P101 = TTO_P101, Q_P101 = Q_P101)
            self.Q_P101 = self.plant.Q_P101
    
    def Pump102 (self, FT_P102, TTO_P102, Q_P102, inputPump102):
        if inputPump102 == True:
            self.plant.Pump102(FT_P102 = FT_P102, TTO_P102 = TTO_P102, Q_P102 = Q_P102)
            self.Q_P102 = self.plant.Q_P102
            if self.plant.OperationMode in ["Modo4", "Modo5"]:
                self.Q_P102v = self.plant.Q_P102v
        else:
            try:
                FT_P102 = self.Datainterfaz["_value"]["MFTPP102"]
                TTO_P102 = self.Datainterfaz["_value"]["MTTOP102"]
                Q_P102 = self.Datainterfaz["_value"]["MQP102"]
            except KeyError:
                FT_P102 = FT_P102
                TTO_P102 = TTO_P102
                Q_P102 = Q_P102
            self.plant.Pump102(FT_P102 = FT_P102, TTO_P102 = TTO_P102, Q_P102 = Q_P102)
            self.Q_P102 = self.plant.Q_P102
            if self.plant.OperationMode in ["Modo4", "Modo5"]:
                self.Q_P102v = self.plant.Q_P102v
            
    def Mixing_TK100(self, FT_mixin_TK100, TTO_mixing_TK100, RPM_TK100, inputMixTK100):
        if inputMixTK100 == True:
            self.plant.Mixing_TK100(FT_mixin_TK100 = FT_mixin_TK100, TTO_mixing_TK100 = TTO_mixing_TK100, RPM_TK100 = RPM_TK100)
            self.RPM_TK100 = self.plant.RPM_TK100
        else:
            try:
                FT_mixin_TK100 = self.Datainterfaz["_value"]["FT_mixin_TK100"]
                TTO_mixing_TK100 = self.Datainterfaz["_value"]["TTO_mixing_TK100"]
                RPM_TK100 = self.Datainterfaz["_value"]["RPM_TK100"]
            except KeyError:
                FT_mixin_TK100 = FT_mixin_TK100
                TTO_mixing_TK100 = TTO_mixing_TK100
                RPM_TK100 = RPM_TK100
            self.plant.Mixing_TK100(FT_mixin_TK100 = FT_mixin_TK100, TTO_mixing_TK100 = TTO_mixing_TK100, RPM_R101 = RPM_TK100)
            self.RPM_TK100 = self.plant.RPM_TK100

    def Mixing_R101 (self, FT_mixin_R101, TTO_mixing_R101, RPM_R101, inputMixR101):
        if inputMixR101 == True:
            self.plant.Mixing_R101(FT_mixin_R101 = FT_mixin_R101, TTO_mixing_R101 = TTO_mixing_R101, RPM_R101 = RPM_R101)
            self.RPM_R101 = self.plant.RPM_R101
        else:
            try:
                FT_mixin_R101 = self.Datainterfaz["_value"]["FT_mixin_R101"]
                TTO_mixing_R101 = self.Datainterfaz["_value"]["TTO_mixing_R101"]
                RPM_R101 = self.Datainterfaz["_value"]["RPM_R101"]
            except KeyError:
                FT_mixin_R101 = FT_mixin_R101
                TTO_mixing_R101 = TTO_mixing_R101
                RPM_R101 = RPM_R101
            self.plant.Mixing_R101(FT_mixin_R101 = FT_mixin_R101, TTO_mixing_R101 = TTO_mixing_R101, RPM_R101 = RPM_R101)
            self.RPM_R101 = self.plant.RPM_R101

    def Mixing_R102 (self, FT_mixin_R102, TTO_mixing_R102, RPM_R102, inputMixR102):
        if inputMixR102 == True:
            self.plant.Mixing_R102(FT_mixin_R102 = FT_mixin_R102, TTO_mixing_R102 = TTO_mixing_R102, RPM_R102 = RPM_R102)
            self.RPM_R102 = self.plant.RPM_R102
        else:
            try:
                FT_mixin_R102 = self.Datainterfaz["_value"]["FT_mixin_R102"]
                TTO_mixing_R102 = self.Datainterfaz["_value"]["TTO_mixing_R102"]
                RPM_R102 = self.Datainterfaz["_value"]["RPM_R102"]
                self.RPM_R102 = self.plant.RPM_R102
            except ZeroDivisionError:
                FT_mixin_R102 = FT_mixin_R102 
                TTO_mixing_R102 = TTO_mixing_R102
                RPM_R102 = RPM_R102
            self.plant.Mixing_R102(FT_mixin_R102 = FT_mixin_R102, TTO_mixing_R102 = TTO_mixing_R102, RPM_R102 = RPM_R102)
    
    def Reactor101Simulation_Arrhenius(self, Operation, VR, Qin_1, Csus_in1, K, Ea, T, pH, Qin_2=[0], Csus_in2 = 0.0):

        self.plant.Reactor101Simulation_ArrheniusModel(Operation, VR, Qin_1, Csus_in1, K, Ea, T, pH, Qin_2, Csus_in2)
        self.x_R101 = self.plant.x_R101
        self.SV_R101_p = self.plant.self.SV_R101_p
        self.molCH4_R101 = self.plant.molCH4_R101 
        self.molCO2_R101 = self.plant.molCO2_R101 
        self.molH2S_R101 = self.plant.molH2S_R101 
        self.molNH3_R101 = self.plant.molNH3_R101
        self.molO2_R101 = self.plant.molO2_R101
        self.molH2_R101 = self.plant.molH2_R101 
        self.molH2O_R101 = self.plant.molH2O_R101

        self.Csus_ini_R101 = self.plant.Csus_ini_R101

    def Reactor101Simulation_ADM1(self, Operation, VR, Qin_1, Csus_in1, K, Qin_2=[0], Csus_in2 = 0.0):

        self.plant.Reactor101Simulation_ADM1(Operation, VR, Qin_1, Csus_in1, K, Qin_2, Csus_in2)
        self.x_R101 = self.plant.x_R101
        self.SV_R101_p = self.plant.SV_R101_p
        self.molCH4_R101 = self.plant.molCH4_R101
        self.molCO2_R101 = self.plant.molCO2_R101 
        self.molH2S_R101 = self.plant.molH2S_R101 
        self.molNH3_R101 = self.plant.molNH3_R101
        self.molO2_R101 = self.plant.molO2_R101
        self.molH2_R101 = self.plant.molH2_R101 
        self.molH2O_R101 = self.plant.molH2O_R101

        self.Csus_ini_R101 = self.plant.Csus_ini_R101
    
    def Reactor101Simulation_Gompertz(self, Operation, ym, U, Lambda, Qin_1, Qin_2 = [0]):
        
        self.plant.Reactor101Simulation_Gompertz(Operation, ym, U, Lambda, Qin_1, Qin_2)
        self.x_R101 = self.plant.x_R101
        self.SV_R101_p = self.plant.SV_R101_p
        self.molCH4_R101 = self.plant.molCH4_R101 
        self.molCO2_R101 = self.plant.molCO2_R101 
        self.molH2S_R101 = self.plant.molH2S_R101 
        self.molNH3_R101 = self.plant.molNH3_R101
        self.molO2_R101 = self.plant.molO2_R101
        self.molH2_R101 = self.plant.molH2_R101 
        self.molH2O_R101 = self.plant.molH2O_R101

        self.Csus_ini_R101 = self.plant.Csus_ini_R101
    
    def V101 (self, Pset=30):
        #Accumulated mol of coompounds by the time 
        self.nCH4_V101_acum_i = self.nCH4_V101_acum_i + self.molCH4_R101                     #accumulated mol (integral)
        self.nCO2_V101_acum_i = self.nCO2_V101_acum_i + self.molCO2_R101 
        self.nH2S_V101_acum_i = self.nH2S_V101_acum_i + self.molH2S_R101
        self.nNH3_V101_acum_i = self.nNH3_V101_acum_i + self.molNH3_R101
        self.nH2O_V101_acum_i = self.nH2O_V101_acum_i  + self.molH2O_R101
        self.nO2_V101_acum_i = self.nO2_V101_acum_i + self.molO2_R101
        self.nH2_V101_acum_i = self.nH2_V101_acum_i + self.molH2_R101 
        
        self.biogas_acum_V101_dry = self.nCH4_V101_acum_i + self.nCO2_V101_acum_i + self.nH2S_V101_acum_i + self.nNH3_V101_acum_i + self.nO2_V101_acum_i + self.nH2_V101_acum_i
        self.biogas_acum_V101_wet = self.biogas_acum_V101_dry + self.nH2O_V101_acum_i 
        self.Energia_V101 = self.Thermo.LHV(molCH4=self.nCH4_V101_acum_i, molCO2=self.nCO2_V101_acum_i, molH2S=self.nH2S_V101_acum_i, molO2=self.nO2_V101_acum_i, molH2=self.nH2_V101_acum_i)[1]
        
        #Biogas compound Concentration
        try: 
            if self.biogas_acum_V101_dry == 0:
                self.xCH4_V101 = 0
                self.xCO2_V101 = 0
                self.xH2S_V101 = 0
                self.xNH3_V101 = 0
                self.xH2O_V101 = 0
                self.xO2_V101 = 0
                self.xH2_V101 = 0
            else:
                self.xCH4_V101_wet = self.nCH4_V101_acum_i/self.biogas_acum_V101_wet
                self.xCO2_V101_wet = self.nCO2_V101_acum_i/self.biogas_acum_V101_wet
                self.xH2S_V101_wet = self.nH2S_V101_acum_i/self.biogas_acum_V101_wet
                self.xNH3_V101_wet = self.nNH3_V101_acum_i/self.biogas_acum_V101_wet
                self.xH2O_V101_wet = self.nH2O_V101_acum_i/self.biogas_acum_V101_wet
                self.xO2_V101_wet = self.nO2_V101_acum_i/self.biogas_acum_V101_wet
                self.xH2_V101_wet = self.nH2_V101_acum_i/self.biogas_acum_V101_wet
                
                self.xCH4_V101 = self.nCH4_V101_acum_i/self.biogas_acum_V101_dry
                self.xCO2_V101 = self.nCO2_V101_acum_i/self.biogas_acum_V101_dry
                self.xH2S_V101 = self.nH2S_V101_acum_i/self.biogas_acum_V101_dry
                self.xNH3_V101 = self.nNH3_V101_acum_i/self.biogas_acum_V101_dry
                self.xH2O_V101 = self.nH2O_V101_acum_i/self.biogas_acum_V101_dry
                self.xO2_V101 = self.nO2_V101_acum_i/self.biogas_acum_V101_dry
                self.xH2_V101 = self.nH2_V101_acum_i/self.biogas_acum_V101_dry
        except ZeroDivisionError:
            self.xCH4_V101 = 0
            self.xCO2_V101 = 0
            self.xH2S_V101 = 0
            self.xNH3_V101 = 0
            self.xH2O_V101 = 0
            self.xO2_V101 = 0
            self.xH2_V101 = 0
        
        self.Temperature = np.random.normal(25, 1)
        p_i = (((self.biogas_acum_V101_wet * 8.314 * (self.Temperature+273.15))/(self.VG1/1000))/6894.76) - self.Pacum_V101 
        if self.Pacum_V101 < Pset:
            self.Pstorage_V101 = self.Pacum_V101
        else:
            self.Pstorage_V101 = p_i + self.Pstorage_V101                                                                   #psig
        self.Pacum_V101 = ((self.biogas_acum_V101_wet * 8.314 * (self.Temperature+273.15))/(self.VG1/1000))/6894.76     #psig
        #Storage biogas moles
        self.biogas_storage_mol_V101 = ((self.Pstorage_V101*6894.76) * (self.VG1/1000))/(8.314*(self.Temperature+273.15))               #mol

        #Standard volume estimation for storage and accumulated biogas
        #Standard conditions
        self.Tstd = 273.15            #[K]
        self.Pstd = 14.5038           #[Psi]  
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V101 = (self.Pacum_V101*self.VG1*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard colume estimation for storage biogas
        self.Vstorage_std_V101 = (self.Pstorage_V101*self.VG1*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        
        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V101 = self.Vol_esp_CH4 * self.nCH4_V101_acum_i
        self.Vol_acum_CO2_V101 = self.Vol_esp_CO2 * self.nCO2_V101_acum_i
        self.Vol_acum_O2_V101 = self.Vol_esp_O2 * self.nO2_V101_acum_i
        self.Vol_acum_H2S_V101 = self.Vol_esp_H2S * self.nH2S_V101_acum_i
        self.Vol_acum_H2_V101 = self.Vol_esp_H2 * self.nH2_V101_acum_i
        self.Vol_acum_NH3_V101 = self.Vol_esp_NH3 * self.nNH3_V101_acum_i  

        #Relative Humidity estimation
        self.RH_V101 = self.Thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V101*self.xH2O_V101*20, VnormalTotal=self.Vstorage_std_V101/1000, T=self.Temperature, P=self.Pstorage_V101)  
        
        #Pressure control
        if self.Pstorage_V101 > Pset:
            P_storage_V101_pres = ((self.biogas_storage_mol_V101 *8.314 * (self.Temperature+273.15)) / ((self.VG1)/1000))/6894.76   #pressure before trnasfer
            self.Pstorage_V101 = (((self.biogas_storage_mol_V101+self.biogas_storage_mol_V102) * 8.314 * (self.Temperature+273.15))/((self.VG1 + self. VG2)/1000))/6894.76      #equilibrium pressure between V101 and V102
            # if self.Pstorage_V102 == 0:
            #     self.Pstorage_V102 = self.Pstorage_V101
            #     print(self.Pstorage_V102)
            self.biogasmol_storage_V101 = ((self.Pstorage_V101*6894.76) * ((self.VG1)/1000))/(8.314*(self.Temperature+273.15)) 
            biogasmol_storage_V101_pres = ((P_storage_V101_pres*6894.76) * ((self.VG1)/1000))/(8.314*(self.Temperature+273.15))
 
            self.mol_CH4_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xCH4_V101_wet
            self.mol_CO2_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xCO2_V101_wet
            self.mol_O2_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xO2_V101_wet
            self.mol_H2S_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xH2S_V101_wet
            self.mol_NH3_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xNH3_V101_wet
            self.mol_H2O_transfertoV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xH2O_V101_wet
            self.mol_H2_transfertoV102 =  (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xH2_V101_wet                                                 
        else:
            self.mol_CH4_transferToV102 = 0
            self.mol_CO2_transferToV102 = 0
            self.mol_O2_transferToV102 =  0
            self.mol_H2S_transferToV102 = 0
            self.mol_NH3_transferToV102 = 0
            self.mol_H2O_transfertoV102 = 0
            self.mol_H2_transfertoV102 = 0
    
    def V102mode1 (self, Pset):
        self.nCH4_V102_acum_i = self.nCH4_V102_acum_i + self.mol_CH4_transferToV102                      #accumulated mol (integral)
        self.nCO2_V102_acum_i = self.nCO2_V102_acum_i + self.mol_CO2_transferToV102 
        self.nH2S_V102_acum_i = self.nH2S_V102_acum_i + self.mol_H2S_transferToV102
        self.nNH3_V102_acum_i = self.nNH3_V102_acum_i + self.mol_NH3_transferToV102
        self.nH2O_V102_acum_i = self.nH2O_V102_acum_i  + self.mol_H2O_transfertoV102
        self.nO2_V102_acum_i = self.nO2_V102_acum_i + self.mol_O2_transferToV102
        self.nH2_V102_acum_i = self.nH2_V102_acum_i + self.mol_H2_transfertoV102

        self.biogas_acum_V102_dry = self.nCH4_V102_acum_i + self.nCO2_V102_acum_i + self.nH2S_V102_acum_i + self.nNH3_V102_acum_i + self.nO2_V102_acum_i + self.nH2_V102_acum_i
        self.biogas_acum_V102_wet = self.biogas_acum_V102_dry + self.nH2O_V102_acum_i
        self.Energia_V102 = self.Thermo.LHV(molCH4=self.nCH4_V102_acum_i, molCO2=self.nCO2_V102_acum_i, molH2S=self.nH2S_V102_acum_i, molO2=self.nO2_V102_acum_i, molH2=self.nH2_V102_acum_i)[1]
       
        #Biogas compound Concentration
        try:
            if self.biogas_acum_V102_dry == 0:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0
            else:
                self.xCH4_V102_wet = self.nCH4_V102_acum_i/self.biogas_acum_V102_wet
                self.xCO2_V102_wet = self.nCO2_V102_acum_i/self.biogas_acum_V102_wet
                self.xH2S_V102_wet = self.nH2S_V102_acum_i/self.biogas_acum_V102_wet
                self.xNH3_V102_wet = self.nNH3_V102_acum_i/self.biogas_acum_V102_wet
                self.xH2O_V102_wet = self.nH2O_V102_acum_i/self.biogas_acum_V102_wet
                self.xO2_V102_wet = self.nO2_V102_acum_i/self.biogas_acum_V102_wet
                self.xH2_V102_wet = self.nH2_V102_acum_i/self.biogas_acum_V102_wet
                
                self.xCH4_V102 = self.nCH4_V102_acum_i/self.biogas_acum_V102_dry
                self.xCO2_V102 = self.nCO2_V102_acum_i/self.biogas_acum_V102_dry
                self.xH2S_V102 = self.nH2S_V102_acum_i/self.biogas_acum_V102_dry
                self.xNH3_V102 = self.nNH3_V102_acum_i/self.biogas_acum_V102_dry
                self.xH2O_V102 = self.nH2O_V102_acum_i/self.biogas_acum_V102_wet
                self.xO2_V102 = self.nO2_V102_acum_i/self.biogas_acum_V102_dry
                self.xH2_V102 = self.nH2_V102_acum_i/self.biogas_acum_V102_dry
        except ZeroDivisionError:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0

        p_i = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76 - self.Pacum_V102
        self.Pstorage_V102 = p_i + self.Pstorage_V102
        self.Pacum_V102 = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76
        
        #Storage biogas moles
        self.biogas_storage_mol_V102 = ((self.Pstorage_V102*6894.76) * (self.VG2/1000))/(8.314*(self.Temperature+273.15))

        #Standard volume estimation for storage and accumulated biogas
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V102 = (self.Pacum_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard Volume estimation for storage biogas
        self.Vstorage_std_V102 = (self.Pstorage_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))

        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4_V102 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2_V102 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V102 = self.Vol_esp_CH4_V102 * self.nCH4_V102_acum_i
        self.Vol_acum_CO2_V102 = self.Vol_esp_CO2_V102 * self.nCO2_V102_acum_i
        self.Vol_acum_O2_V102 = self.Vol_esp_O2_V102 * self.nO2_V102_acum_i
        self.Vol_acum_H2S_V102 = self.Vol_esp_H2S_V102 * self.nH2S_V102_acum_i
        self.Vol_acum_H2_V102 = self.Vol_esp_H2_V102 * self.nH2_V102_acum_i
        self.Vol_acum_NH3_V102 = self.Vol_esp_NH3_V102 * self.nNH3_V102_acum_i

        #Relative Humidity estimation
        self.RH_V102 = self.Thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V102 * self.xH2O_V102 * 20, VnormalTotal=self.Vstorage_std_V102/1000, T=self.Temperature, P=self.Pstorage_V102)
        
        #Pressure control
        if self.Pstorage_V102 > Pset:
            P_storage_V102_pres = ((self.biogas_storage_mol_V102 *8.314 * (self.Temperature+273.15)) / ((self.VG2)/1000))/6894.76   #pressure before trnasfer
            self.Pstorage_V102 = (((self.biogas_storage_mol_V102 + self.biogas_storage_mol_V107) * 8.314 * (self.Temperature+273.15))/((self.VG3 + self.VG2)/1000))/6894.76      #equilibrium pressure between V102 and V102  
            # if self.Pstorage_V107 != 0:
            #     self.Pstorage_V107 = self.Pstorage_V102
            
            self.biogasmol_storage_V102= ((self.Pstorage_V102*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15))                 #mol trnasfer since V102 to V102
            biogasmol_storage_V102_pres = ((P_storage_V102_pres*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15)) 

            self.mol_CH4_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCH4_V102_wet
            self.mol_CO2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCO2_V102_wet
            self.mol_O2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xO2_V102_wet
            self.mol_H2S_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2S_V102_wet
            self.mol_NH3_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xNH3_V102_wet
            self.mol_H2O_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2O_V102_wet
            self.mol_H2_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2_V102_wet
            
        else:
            self.mol_CH4_transferToV107 = 0
            self.mol_CO2_transferToV107 = 0
            self.mol_O2_transferToV107 =  0
            self.mol_H2S_transferToV107 = 0
            self.mol_NH3_transferToV107 = 0
            self.mol_H2O_transfertoV107 = 0
            self.mol_H2_transfertoV107 = 0
    
    def V107mode1 (self, Pset, Pmin=0):
        self.nCH4_V107_acum_i = self.nCH4_V107_acum_i + self.mol_CH4_transferToV107                      #accumulated mol (integral)
        self.nCO2_V107_acum_i = self.nCO2_V107_acum_i + self.mol_CO2_transferToV107 
        self.nH2S_V107_acum_i = self.nH2S_V107_acum_i + self.mol_H2S_transferToV107
        self.nNH3_V107_acum_i = self.nNH3_V107_acum_i + self.mol_NH3_transferToV107
        self.nH2O_V107_acum_i = self.nH2O_V107_acum_i  + self.mol_H2O_transfertoV107
        self.nO2_V107_acum_i = self.nO2_V107_acum_i + self.mol_O2_transferToV107
        self.nH2_V107_acum_i = self.nH2_V107_acum_i + self.mol_H2_transfertoV107
        self.nfree = self.nbiogas_V107_acum_i * (1-self.xCH4_V107/100-self.xCO2_V107/100-self.xO2_V107/100-self.xH2_V107/1000000-self.xH2S_V107/1000000) - self.nNH3_V107_acum_i
        
        self.biogas_acum_V107_dry = self.nCH4_V107_acum_i + self.nCO2_V107_acum_i + self.nH2S_V107_acum_i + self.nNH3_V107_acum_i + self.nO2_V107_acum_i + self.nH2_V107_acum_i
        self.biogas_acum_V107_wet = self.biogas_acum_V107_dry + self.nH2O_V107_acum_i
        self.Energia_V107 = self.Thermo.LHV(molCH4=self.nCH4_V107_acum_i, molCO2=self.nCO2_V107_acum_i, molH2S=self.nH2S_V107_acum_i, molO2=self.nO2_V107_acum_i, molH2=self.nH2_V107_acum_i)[1]
        
        try:
            if self.biogas_acum_V101_dry == 0:
                self.xCH4_V107 = 0
                self.xCO2_V107 = 0
                self.xH2S_V107 = 0
                self.xNH3_V107 = 0
                self.xH2O_V107 = 0
                self.xO2_V107 = 0
                self.xH2_V107 = 0
            else:
                self.xCH4_V107_wet = self.nCH4_V107_acum_i/self.biogas_acum_V107_wet
                self.xCO2_V107_wet = self.nCO2_V107_acum_i/self.biogas_acum_V107_wet
                self.xH2S_V107_wet = self.nH2S_V107_acum_i/self.biogas_acum_V107_wet
                self.xNH3_V107_wet = self.nNH3_V107_acum_i/self.biogas_acum_V107_wet
                self.xH2O_V107_wet = self.nH2O_V107_acum_i/self.biogas_acum_V107_wet
                self.xO2_V107_wet = self.nO2_V107_acum_i/self.biogas_acum_V107_wet
                self.xH2_V107_wet = self.nH2_V107_acum_i/self.biogas_acum_V107_wet
                
                self.xCH4_V107 = self.nCH4_V107_acum_i/self.biogas_acum_V107_dry
                self.xCO2_V107 = self.nCO2_V107_acum_i/self.biogas_acum_V107_dry
                self.xH2S_V107 = self.nH2S_V107_acum_i/self.biogas_acum_V107_dry
                self.xNH3_V107 = self.nNH3_V107_acum_i/self.biogas_acum_V107_dry
                self.xH2O_V107 = self.nH2O_V107_acum_i/self.biogas_acum_V107_wet
                self.xO2_V107 = self.nO2_V107_acum_i/self.biogas_acum_V107_dry
                self.xH2_V107 = self.nH2_V107_acum_i/self.biogas_acum_V107_dry
        
        except ZeroDivisionError:
            self.xCH4_V107 = 0
            self.xCO2_V107 = 0
            self.xH2S_V107 = 0
            self.xNH3_V107 = 0
            self.xH2O_V107 = 0
            self.xO2_V107 = 0
            self.xH2_V107 = 0
        
        p_i = ((((self.biogas_acum_V107_wet + self.nfree) * 8.314 * (self.Temperature+273.15))/((self.VG3)/1000))/6894.76) - self.Pacum_V107
        self.Pstorage_V107 = p_i + self.Pstorage_V107
        self.Pacum_V107 = (((self.biogas_acum_V107_wet + self.nfree) * 8.314 * (self.Temperature+273.15))/((self.VG3)/1000))/6894.76

        #Storage biogas moles
        self.biogas_storage_mol_V107 = ((self.Pstorage_V107*6894.76) * (self.VG3/1000))/(8.314*(self.Temperature+273.15))

        #Standard volume estimation for storage and accumulated biogas
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V107 = (self.Pacum_V107*self.VG3*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard colume estimation for storage biogas
        self.Vstorage_std_V107 = (self.Pstorage_V107*self.VG3*self.Tstd)/(self.Pstd*(self.Temperature+273.15))

        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4_V107 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2_V107 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2_V107 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S_V107 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2_V107 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3_V107 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V107 = self.Vol_esp_CH4_V107 * self.nCH4_V107_acum_i
        self.Vol_acum_CO2_V107 = self.Vol_esp_CO2_V107 * self.nCO2_V107_acum_i
        self.Vol_acum_O2_V107 = self.Vol_esp_O2_V107 * self.nO2_V107_acum_i
        self.Vol_acum_H2S_V107 = self.Vol_esp_H2S_V107 * self.nH2S_V107_acum_i
        self.Vol_acum_H2_V107 = self.Vol_esp_H2_V107 * self.nH2_V107_acum_i
        self.Vol_acum_NH3_V107 = self.Vol_esp_NH3_V107 * self.nNH3_V107_acum_i

        #Relative Humidity estimation
        self.RH_V107 = self.Thermo.BiogasRelativeHumidity(nH2O=self.nH2O_V107_acum_i*25, VnormalTotal=self.Vacum_std_V107/1000, T=self.Temperature, P=self.Pstorage_V107)

        #Pressure control
        if self.Pstorage_V107 > Pset:
            self.biogas_transferToEnv = ((self.Pstorage_V107*6894.76) * (self.VG3/1000))/(8.314*(self.Temperature+273.15))                 #mol trnasfer since V102 to V102
            self.mol_CH4_transferToEnv = self.biogas_transferToEnv*self.xCH4_V107
            self.mol_CO2_transferToEnv = self.biogas_transferToEnv*self.xCO2_V107
            self.mol_O2_transferToEnv = self.biogas_transferToEnv*self.xO2_V107
            self.mol_H2S_transferToEnv = self.biogas_transferToEnv*self.xH2S_V107
            self.mol_NH3_transferToEnv = self.biogas_transferToEnv*self.xNH3_V107
            self.mol_H2O_transfertoEnv = self.biogas_transferToEnv*self.xH2O_V107
            self.Pstorage_V107 = Pmin 
             
        else:
            self.mol_CH4_transferToEnv = 0
            self.mol_CO2_transferToEnv = 0
            self.mol_O2_transferToEnv =  0
            self.mol_H2S_transferToEnv = 0
            self.mol_NH3_transferToEnv = 0
            self.mol_H2O_transfertoEnv = 0
            self.mol_H2_transfertoEnv = 0
    
    def biogas_treatment_model1 (self, W_fe2O3, K_H2S, K_NH3, K_H2O, w_carbon = 1.0, w_silica = 1.0, qmax_H2S = 0.0188,
                                 qmax_NH3 = 0.1, qmax_H2O = 0.1, k2_H2O = 0.1, k2_NH3 = 0.1, k2_H2S = 0.1):
        #-------H2S--------
        q_H2S = (qmax_H2S * K_H2S * (self.Pacum_V107*self.xH2S_V107_wet))/(1+(K_H2S*self.Pacum_V107*self.xH2S_V107_wet))
        self.mol_H2S_ads_acum_i = self.mol_H2S_ads_acum
        self.mol_H2S_ads_acum = W_fe2O3 * (q_H2S**2 * k2_H2S * self.GlobalTime)/(1+q_H2S*k2_H2S*self.GlobalTime)
        # self.mol_H2S_ads_acum = q_H2S * W_fe2O3
        self.mol_H2S_transferToV107_i = self.mol_H2S_ads_acum - self.mol_H2S_ads_acum_i
        self.molH2S_acum_V107_i = self.molH2S_acum_V107_i + self.mol_H2S_transferToV107_i 

        #------NH3---------
        q_NH3 = (qmax_NH3 * K_NH3 * (self.Pacum_V107*self.xNH3_V107_wet))/(1+(K_NH3*self.Pacum_V107*self.xNH3_V107_wet))
        self.mol_NH3_ads_acum_i = self.mol_NH3_ads_acum
        self.mol_NH3_ads_acum = w_carbon * (q_NH3**2 * k2_NH3 * self.GlobalTime)/(1+q_NH3*k2_NH3*self.GlobalTime)
        # self.mol_NH3_ads_acum = q_NH3 * w_carbon
        self.mol_NH3_transferToV107_i = self.mol_NH3_ads_acum - self.mol_NH3_ads_acum_i
        self.molNH3_acum_V107_i = self.molNH3_acum_V107_i + self.mol_NH3_transferToV107_i

        #------H2O-------- 
        q_H2O = (qmax_H2O * K_H2O * (self.Pacum_V107*self.xH2O_V107_wet))/(1+(K_H2O+self.Pacum_V107*self.xH2O_V107_wet))
        self.mol_H2O_ads_acum_i = self.mol_H2O_ads_acum
        self.mol_H2O_ads_acum = w_silica * (q_H2O**2 * k2_H2O * self.GlobalTime)/(1+q_H2O*k2_H2O*self.GlobalTime)
        # self.mol_H2O_ads_acum = q_H2O * w_silica
        self.mol_H2O_transfertoV107_i = self.mol_H2O_ads_acum - self.mol_H2O_ads_acum_i 
        self.molH2O_acum_V107_i = self.molH2O_acum_V107_i + self.mol_H2O_transfertoV107_i
    
    def Reactor102Simulation_Arrhenius(self, Operation, VR, Qin_1, Csus_in1,
                                            K, Ea, T, pH, Qin_2=[0], Csus_in2 = 0.0):
        
        self.plant.Reactor102Simulation_ArrheniusModel (Operation, VR, Qin_1, Csus_in1, K, Ea, T, pH, Qin_2, Csus_in2)
        self.x_R102 = self.plant.x_R102
        self.SV_R102_p = self.plant.SV_R102_p
        self.molCH4_R102 = self.plant.molCH4_R102 
        self.molCO2_R102 = self.plant.molCO2_R102 
        self.molH2S_R102 = self.plant.molH2S_R102 
        self.molNH3_R102 = self.plant.molNH3_R102
        self.molO2_R102 = self.plant.molO2_R102
        self.molH2_R102 = self.plant.molH2_R102 
        self.molH2O_R102 = self.plant.molH2O_R102
    
    def Reactor102Simulation_ADM1(self, Operation, VR, Qin_1, Csus_in1, K, Qin_2=[0], Csus_in2 = 0.0):

        self.plant.Reactor102Simulation_ADM1 (Operation, VR, Qin_1, Csus_in1, K, Qin_2, Csus_in2)
        self.x_R102 = self.plant.x_R102
        self.SV_R102_p = self.plant.SV_R102_p
        self.molCH4_R102 = self.plant.molCH4_R102 
        self.molCO2_R102 = self.plant.molCO2_R102 
        self.molH2S_R102 = self.plant.molH2S_R102 
        self.molNH3_R102 = self.plant.molNH3_R102
        self.molO2_R102 = self.plant.molO2_R102
        self.molH2_R102 = self.plant.molH2_R102 
        self.molH2O_R102 = self.plant.molH2O_R102
    
    def Reactor102Simulation_Gompertz(self,Operation, ym, U, Lambda, Qin_1, Qin_2 = [0]):

        self.plant.Reactor102Simulation_Gompertz (Operation, ym, U, Lambda, Qin_1, Qin_2)
        self.x_R102 = self.plant.x_R102
        self.SV_R102_p = self.plant.SV_R102_p
        self.molCH4_R102 = self.plant.molCH4_R102 
        self.molCO2_R102 = self.plant.molCO2_R102 
        self.molH2S_R102 = self.plant.molH2S_R102 
        self.molNH3_R102 = self.plant.molNH3_R102
        self.molO2_R102 = self.plant.molO2_R102
        self.molH2_R102 = self.plant.molH2_R102 
        self.molH2O_R102 = self.plant.molH2O_R102
    
    def V102_model2 (self, Pset):
        self.nCH4_V102_acum_i = self.nCH4_V102_acum_i + self.molCH4_R102 + self.mol_CH4_transferToV102                      #accumulated mol (integral)
        self.nCO2_V102_acum_i = self.nCO2_V102_acum_i + self.molCO2_R102 + self.mol_CO2_transferToV102 
        self.nH2S_V102_acum_i = self.nH2S_V102_acum_i + self.molH2S_R102 + self.mol_H2S_transferToV102
        self.nNH3_V102_acum_i = self.nNH3_V102_acum_i + self.molNH3_R102 + self.mol_NH3_transferToV102
        self.nH2O_V102_acum_i = self.nH2O_V102_acum_i  + self.molH2O_R102 + self.mol_H2O_transfertoV102
        self.nO2_V102_acum_i = self.nO2_V102_acum_i + self.molO2_R102 + self.mol_O2_transferToV102
        self.nH2_V102_acum_i = self.nH2_V102_acum_i + self.molH2_R102 + self.mol_H2_transfertoV102

        self.biogas_acum_V102_dry = self.nCH4_V102_acum_i + self.nCO2_V102_acum_i + self.nH2S_V102_acum_i + self.nNH3_V102_acum_i + self.nO2_V102_acum_i + self.nH2_V102_acum_i
        self.biogas_acum_V102_wet = self.biogas_acum_V102_dry + self.nH2O_V102_acum_i 
        self.Energia_V102 = self.Thermo.LHV(molCH4=self.nCH4_V102_acum_i, molCO2=self.nCO2_V102_acum_i, molH2S=self.nH2S_V102_acum_i, molO2=self.nO2_V102_acum_i, molH2=self.nH2_V102_acum_i)[1]

        #Biogas compound Concentration
        try:
            if self.biogas_acum_V102_dry == 0:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0
            else:
                self.xCH4_V102_wet = self.nCH4_V102_acum_i/self.biogas_acum_V102_wet
                self.xCO2_V102_wet = self.nCO2_V102_acum_i/self.biogas_acum_V102_wet
                self.xH2S_V102_wet = self.nH2S_V102_acum_i/self.biogas_acum_V102_wet
                self.xNH3_V102_wet = self.nNH3_V102_acum_i/self.biogas_acum_V102_wet
                self.xH2O_V102_wet = self.nH2O_V102_acum_i/self.biogas_acum_V102_wet
                self.xO2_V102_wet = self.nO2_V102_acum_i/self.biogas_acum_V102_wet
                self.xH2_V102_wet = self.nH2_V102_acum_i/self.biogas_acum_V102_wet
                
                self.xCH4_V102 = self.nCH4_V102_acum_i/self.biogas_acum_V102_dry
                self.xCO2_V102 = self.nCO2_V102_acum_i/self.biogas_acum_V102_dry
                self.xH2S_V102 = self.nH2S_V102_acum_i/self.biogas_acum_V102_dry
                self.xNH3_V102 = self.nNH3_V102_acum_i/self.biogas_acum_V102_dry
                self.xH2O_V102 = self.nH2O_V102_acum_i/self.biogas_acum_V102_wet
                self.xO2_V102 = self.nO2_V102_acum_i/self.biogas_acum_V102_dry
                self.xH2_V102 = self.nH2_V102_acum_i/self.biogas_acum_V102_dry
        except ZeroDivisionError:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0
        
        p_i = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76 - self.Pacum_V102
        self.Pstorage_V102 = p_i + self.Pstorage_V102
        self.Pacum_V102 = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76

        #Storage biogas moles
        self.biogas_storage_mol_V102 = ((self.Pstorage_V102*6894.76) * (self.VG2/1000))/(8.314*(self.Temperature+273.15))

        #Standard volume estimation for storage and accumulated biogas
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V102 = (self.Pacum_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard colume estimation for storage biogas
        self.Vstorage_std_V102 = (self.Pstorage_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))

        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4_V102 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2_V102 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3_V102 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V102 = self.Vol_esp_CH4_V102 * self.nCH4_V102_acum_i
        self.Vol_acum_CO2_V102 = self.Vol_esp_CO2_V102 * self.nCO2_V102_acum_i
        self.Vol_acum_O2_V102 = self.Vol_esp_O2_V102 * self.nO2_V102_acum_i
        self.Vol_acum_H2S_V102 = self.Vol_esp_H2S_V102 * self.nH2S_V102_acum_i
        self.Vol_acum_H2_V102 = self.Vol_esp_H2_V102 * self.nH2_V102_acum_i
        self.Vol_acum_NH3_V102 = self.Vol_esp_NH3_V102 * self.nNH3_V102_acum_i 

        #Relative Humidity estimation
        self.RH_V102 = self.Thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V102 * self.xH2O_V102 * 20, VnormalTotal=self.Vstorage_std_V102/1000, T=self.Temperature, P=self.Pstorage_V102)

        #Pressure control
        if self.Pstorage_V102 > Pset:
            P_storage_V102_pres = ((self.biogas_storage_mol_V102 *8.314 * (self.Temperature+273.15)) / ((self.VG2)/1000))/6894.76   #pressure before trnasfer
            self.Pstorage_V102 = (((self.biogas_storage_mol_V102 + self.biogas_storage_mol_V107) * 8.314 * (self.Temperature+273.15))/((self.VG3 + self.VG2)/1000))/6894.76      #equilibrium pressure between V102 and V102  
            # if self.Pstorage_V107 != 0:
            #     self.Pstorage_V107 = self.Pstorage_V102
            
            self.biogasmol_storage_V102= ((self.Pstorage_V102*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15))                 #mol trnasfer since V102 to V102
            biogasmol_storage_V102_pres = ((P_storage_V102_pres*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15)) 

            self.mol_CH4_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCH4_V102_wet
            self.mol_CO2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCO2_V102_wet
            self.mol_O2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xO2_V102_wet
            self.mol_H2S_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2S_V102_wet
            self.mol_NH3_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xNH3_V102_wet
            self.mol_H2O_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2O_V102_wet
            self.mol_H2_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2_V102_wet 

        else:
            self.mol_CH4_transferToV107 = 0
            self.mol_CO2_transferToV107 = 0
            self.mol_O2_transferToV107 =  0
            self.mol_H2S_transferToV107 = 0
            self.mol_NH3_transferToV107 = 0
            self.mol_H2O_transfertoV107 = 0
            self.mol_H2_transfertoV107 = 0                                   
                                            
    def time_counter (self):
        self.GlobalTime = self.GlobalTime + (self.plant.tp * self.plant.time_accelerator)