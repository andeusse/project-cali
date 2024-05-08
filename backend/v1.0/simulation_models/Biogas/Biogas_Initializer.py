class BiogasInitializer:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, t_prediction = 1, timetrain=1, Kini=1):

        #Interface Inputs
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.tp = tp
        self.t_prediction = t_prediction * 3600
        self.timetrain = timetrain * 3600
        self.validation_time = timetrain * 3600
        self.Kini = Kini
        #Initial values
        #Global time
        self.TotalTime = 0
        #Pumps
        self.TimeCounterPump_P104 = 0
        self.TimeCounterPump_P101 = 0
        self.TimeCounterPump_P102 = 0
        #Biogas V_101
        self.Pacum_v101 = 0
        self.P_ini_V101 = 0
        #Biogas V_102
        self.Pacum_v102 = 0
        self.P_ini_V102 = 0
        #Biogas V_107
        self.Pacum_v107 = 0
        self.P_ini_V107 = 0