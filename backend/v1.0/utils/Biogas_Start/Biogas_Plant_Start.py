from simulation_models.Biogas import Biogas_Model_DT

class BiogasStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self,  VR1, VR2, VG1, VG2, VG3, tp, rho_R101, rho_R102, OperationMode):
        if self._data is None:
          self._data = Biogas_Model_DT.BiogasPlantDT(VR1, VR2, VG1, VG2, VG3, tp, rho_R101, rho_R102, OperationMode)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Biogas model not created. Please call createConnection method first.")
        return self._data
    
    @staticmethod
    def reset_instance():
        BiogasStart._instance = None