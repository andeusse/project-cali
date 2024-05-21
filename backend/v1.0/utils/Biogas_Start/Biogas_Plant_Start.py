from simulation_models.Biogas import Biogas_Model_DT

class BiogasStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self, VR1, VR2, VG1, VG2, VG3, tp, ST_R101, SV_R101, Cc_R101, Ch_R101, Co_R101, Cn_R101, Cs_R101, rho_R101,
                 ST_R102, SV_R102, Cc_R102, Ch_R102, Co_R102, Cn_R102, Cs_R102, rho_R102):
        if self._data is None:
          self._data = Biogas_Model_DT.BiogasPlantDT(VR1, VR2, VG1, VG2, VG3, tp, ST_R101, SV_R101, Cc_R101, Ch_R101, Co_R101, Cn_R101, Cs_R101, rho_R101,
                 ST_R102, SV_R102, Cc_R102, Ch_R102, Co_R102, Cn_R102, Cs_R102, rho_R102)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Biogas model not created. Please call createConnection method first.")
        return self._data