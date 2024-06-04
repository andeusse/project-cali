from simulation_models.Biogas import MachineLearningModule

class MachineLearningStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self, t_train, OperationMode, Kini, Eaini, VR1):
        if self._data is None:
          self._data = MachineLearningModule.BiogasModelTrain(t_train, OperationMode, Kini, Eaini, VR1)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Learning model not created. Please call createConnection method first.")
        return self._data
    
    @staticmethod
    def reset_instance():
        MachineLearningStart._instance = None