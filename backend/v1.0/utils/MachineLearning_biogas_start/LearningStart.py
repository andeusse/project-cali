from simulation_models.Biogas import MachineLearningModule

class MachineLearningStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self, VR1, Kini, Eaini, DatabaseConnection_df, database_df, Influx):
        if self._data is None:
          self._data = MachineLearningModule.BiogasModelTrain(VR1, Kini, Eaini, DatabaseConnection_df, database_df, Influx)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Learning model not created. Please call createConnection method first.")
        return self._data