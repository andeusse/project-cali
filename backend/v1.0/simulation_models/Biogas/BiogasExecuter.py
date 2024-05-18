import BiogasModel as BM

#Entrance Variables
DT = 1

tp=30
Biogas_Plant = BM.BiogasPlant(VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, t_prediction = 1, timetrain=0.05, Kini=1)

while True:
    
    TimeCounterPump = 0
    Biogas_Plant.GetValuesFromBiogasPlant()
    #print(Biogas_Plant.AT103A1v)
    Biogas_Plant.RxnParameters(Online=1, manual_sustrate=1, ST=10, SV=4, Cc=40.48, Ch=5.29, Co=29.66, Cn=1.37, Cs=0.211, rho = 1000)
    if DT == 1:
        Biogas_Plant.DTOperationModel1(manual_P104=1, manual_temp_R101=0,  TRH=30, FT_P104=5, TTO_P104=10, Temp_R101 = 35)
    # print("El caudal de la bomba es: "+str(Biogas_Plant.Q_P104))
    # print("El tiempo de encendido es: "+str())
    # else:
    #     Biogas_Plant.OperationModel1(manual_P104=0, manual_temp_R101=0,  TRH=30, FT_P104=5, TTO_P104=10, Temp_R101 = 35)