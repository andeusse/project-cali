import influxdb_client
from influxdb_client import InfluxDBClient
import warnings
from influxdb_client.client.warnings import MissingPivotFunction
from influxdb_client.client.write_api import SYNCHRONOUS, WritePrecision


# %%  InfluxDB Model        
class InfluxDBmodel:
    def __init__(self, server, org, bucket, token):
        self.ERROR_MESSAGE = 'Ocurrió un error al conectarse con la base de datos de InfluxDB, verifique que la base de datos exista y que los parámetros de conexión estén bien configurados.'
        self.server = server
        self.org = org
        self.token = token
        self.bucket = bucket
        warnings.simplefilter("ignore", MissingPivotFunction)

    # %%  InfluxDB Connection         
    def InfluxDBconnection(self):
        try:
            self.influxDBclient = InfluxDBClient(url = self.server, token = self.token)
            return self.influxDBclient.ping()
        except:
            return False

    # %%  InfluxDB Reader 
    def InfluxDBreader(self, query):
        self.query = query
        try:
            self.influxReturndf = self.influxDBclient.query_api().query_data_frame(self.query, self.org)
            return self.influxReturndf
        except:
            return self.ERROR_MESSAGE

    # %%  InfluxDB Writer         
    def InfluxDBwriter(self, measurement, device, variable, value, timestamp):
        write_api = self.influxDBclient.write_api(write_options=SYNCHRONOUS)
        payload = influxdb_client.Point(measurement).tag('device',device).field(variable, value).time(timestamp, write_precision=WritePrecision.S)
        
        try:
            write_api.write(self.bucket, self.org, payload)
            
        except:
            return 'An error ocurred writing the InfluxDB Database'

    # %% InfluxDB close connection
    def InfluxDBclose(self):
        self.influxDBclient.close()

    # %% InfluxDB query creator
    def QueryCreator(self, measurement='', device='', variable='', location='', type=0, forecastTime=0): #type 0: electrical last value, type 1: weather last value, type 2: electrical and weather forecast, type 3: next day forecast
        if type == 0:
            self.query = '''from(bucket: "''' + self.bucket + '''")
            |> range(start: -1m)
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            |> filter(fn: (r) => r["device"] == "''' + device + '''")
            |> filter(fn: (r) => r["_field"] == "''' + variable + '''")
            |> last() |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        elif type == 1:
            self.query ='''from(bucket: "''' + self.bucket + '''")
            |> range(start: -1m)
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            |> last()'''
        elif type == 2:
            self.query ='''from(bucket: "''' + self.bucket + '''")
            |> range(start: -120m, stop: now()) 
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            '''
        elif type == 3:
            self.query ='''import "experimental"
            from(bucket: "''' + self.bucket + '''")
            |> range(start: ''' + forecastTime + ''', stop: experimental.addDuration(d: 24h, to: ''' + forecastTime + '''))
            |> filter(fn: (r) => r["_measurement"] == "forecast")
            |> filter(fn: (r) => r["_field"] == "''' + measurement + '''")
            |> filter(fn: (r) => r["location"] == "''' + location + '''")
            |> filter(fn: (r) => r["period"] == "0")'''
        else:
            self.query = "Tipo de query inválido"
        return self.query

