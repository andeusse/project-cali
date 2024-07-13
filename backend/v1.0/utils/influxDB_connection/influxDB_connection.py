from tools import DBManager

class InfluxDbConnection():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def createConnection(self, server, org, bucket, token):
        if self._data is None:
          self._data = DBManager.InfluxDBmodel(server, org, bucket, token)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Database model not created. Please call createConnection method first.")
        return self._data
