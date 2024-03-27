import pandas as pd

class ExcelReader():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance._data = None
        return cls._instance
    def read_excel(self, file_path, sheet):
        if self._data is None:
          self._data = pd.read_excel(file_path,sheet)
    @property
    def data(self):
        if self._data is None:
          raise ValueError("Excel file not read. Please call read_excel method first.")
        return self._data
