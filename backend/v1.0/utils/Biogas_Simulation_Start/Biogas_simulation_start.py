from simulation_models.Biogas import Biogas_Model_Simulation

class BiogasSimulationStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self, VR1, VR2, VG1, VG2, VG3, tp, 
                 ST_R101, SV_R101, Cc_R101, Ch_R101, Co_R101, Cn_R101, Cs_R101, rho_R101,
                 ST_R102, SV_R102, Cc_R102, Ch_R102, Co_R102, Cn_R102, Cs_R102, rho_R102, OperationMode):
        if self._data is None:
          self._data = Biogas_Model_Simulation.BiogasPlantSimulation(VR1, VR2, VG1, VG2, VG3, tp, 
                    ST_R101, SV_R101, Cc_R101, Ch_R101, Co_R101, Cn_R101, Cs_R101, rho_R101,
                    ST_R102, SV_R102, Cc_R102, Ch_R102, Co_R102, Cn_R102, Cs_R102, rho_R102, OperationMode)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Biogas model not created. Please call createConnection method first.")
        return self._data
    
    @staticmethod
    def reset_instance():
        BiogasSimulationStart._instance = None
    
    def to_dict(self):
      # Convert the instance into a dictionary
      data_dict = {}
      if self._data:
          data_dict['data'] = self._data.to_dict()  # Assuming _data has its own to_dict method
      return data_dict
    
    @classmethod
    def from_dict(cls, data_dict):
        """Deserialize the dictionary back into the singleton instance."""
        instance = cls()
        # Recreate the _data attribute from the stored dictionary
        if 'data' in data_dict:
            instance._data = Biogas_Model_Simulation.BiogasPlantSimulation.from_dict(data_dict['data'])
        return instance

