from simulation_models.Biogas import BiogasModel

class BiogasStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self, VR1, VR2, VG1, VG2, VG3, tp, t_prediction, timetrain, Kini):
        if self._data is None:
          self._data = BiogasModel.BiogasPlant(VR1, VR2, VG1, VG2, VG3, tp, t_prediction, timetrain, Kini)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Database model not created. Please call createConnection method first.")
        return self._data