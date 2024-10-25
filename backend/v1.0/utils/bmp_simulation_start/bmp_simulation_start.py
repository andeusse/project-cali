from simulation_models.BMPModel import BMPOffline

class BMPSimulationStart:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def starting(self, Vrxn, Vf, tp):
        if self._data is None:
          self._data = BMPOffline.BMPModelOffline(Vrxn, Vf, tp)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("bmp model not created. Please call createConnection method first.")
        return self._data
    
    @staticmethod
    def reset_instance():
        BMPSimulationStart._instance = None

