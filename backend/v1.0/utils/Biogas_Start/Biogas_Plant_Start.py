from simulation_models.Biogas import BiogasModel

class BiogasStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._biogas = None
        return cls._instance
    def starting(self, VR1, VR2, VG1, VG2, VG3, tp, t_prediction, timetrain, Kini):
        if self._biogas is None:
          self._biogas = BiogasModel.BiogasPlant(VR1, VR2, VG1, VG2, VG3, tp, t_prediction, timetrain, Kini)
    @property
    def data(self):
        if self._biogas is None:
          raise ValueError("Biogas model not created. Please call createConnection method first.")
        return self._biogas