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
            self.influxDBclient = InfluxDBClient(url = self.server, token = self.token, timeout=10000)
            return self.influxDBclient.ping()
        except:
            return False

    # %%  InfluxDB Reader 
    def InfluxDBreader(self, query):
        self.query = query
        try:
            self.influxReturndf = self.influxDBclient.query_api().query_data_frame(self.query, self.org)
            return self.influxReturndf
        except Exception as error:
            return error

    # %%  InfluxDB Writer         
    def InfluxDBwriter(self, measurement, device, variable, value, timestamp):
        write_api = self.influxDBclient.write_api(write_options=SYNCHRONOUS)
        payload = influxdb_client.Point(measurement).tag('device',device).field(variable, value).time(timestamp, write_precision=WritePrecision.S)
        
        try:
            write_api.write(self.bucket, self.org, payload)
            
        except:
            return 'An error ocurred writing the InfluxDB Database'
        
    # %%  InfluxDB Writer         
    def InfluxDBwriterBiogasTraining(self, measurement, device, mode, model, variable, value, timestamp):
        write_api = self.influxDBclient.write_api(write_options=SYNCHRONOUS)
        payload = influxdb_client.Point(measurement).tag('device',device).field('mode', mode).field('model', model).field(variable, value).time(timestamp, write_precision=WritePrecision.S)
        
        try:
            write_api.write(self.bucket, self.org, payload)
            
        except:
            return 'An error ocurred writing the InfluxDB Database'

    # %% InfluxDB close connection
    def InfluxDBclose(self):
        self.influxDBclient.close()

    # %% InfluxDB query creator
    def QueryCreator(self, measurement='', device='', variable='', location='', t_start_str='', t_end_str='', type=0, forecastTime=0, train_time = 0): #type 0: electrical last value, type 1: weather last value, type 2: electrical and weather forecast, type 3: next day forecast
        if type == 0:
            self.query = '''from(bucket: "''' + self.bucket + '''")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            |> filter(fn: (r) => r["device"] == "''' + device + '''")
            |> filter(fn: (r) => r["_field"] == "''' + variable + '''")
            |> last()'''
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
        elif type == 4:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: -{train_time}m, stop: now())
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) => 
                r["device"] == "P104" or 
                r["device"] == "P101" or 
                r["device"] == "P102" or 
                r["device"] == "R101" or 
                r["device"] == "R102" or 
                r["device"] == "V101" or 
                r["device"] == "V102" or 
                r["device"] == "V107" or
                r["device"] == "TK100"
            )'''

        elif type == 5:
            self.query ='''from(bucket: "''' + self.bucket + '''")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            |> filter(fn: (r) => r["device"] == "''' + device + '''")
            |> last()'''
        elif type == 6:
            self.query = '''from(bucket: "''' + self.bucket + '''")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            |> filter(fn: (r) => r["device"] == "''' + device + '''")
            |> filter(fn: (r) => r["_field"] == "''' + variable + '''")
            |> aggregateWindow(every: 3m, fn: mean, createEmpty: false)
            |> last()'''
        
        elif type == 7:
            self.query ='''from(bucket: "''' + self.bucket + '''")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
            |> filter(fn: (r) => r["_field"] == "SE-107" or r["_field"] == "SE-108" or r["_field"] == "SE-109")
            |> last()
            '''
        elif type == 8:
            self.query = f'''
                from(bucket: "{self.bucket}")
                |> range(start: -{train_time}m, stop: now())
                |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                |> filter(fn: (r) => r["device"] == "interfaz")
                |> filter(fn: (r) => 
                    r["_field"] == "PAcumV101" or 
                    r["_field"] == "PAcumV102" or 
                    r["_field"] == "PAcumV107" or
                    r["_field"] == "PacumGasesV102" or
                    r["_field"] == "Volumen_bioV101" or
                    r["_field"] == "Volumen_bioV102" or
                    r["_field"] == "Volumen_bioV107" or
                    r["_field"] == "LHV_bioV101" or
                    r["_field"] == "LHV_bioV102" or
                    r["_field"] == "LHV_bioV107" or
                    r["_field"] == "LHV_bio_WhV101" or
                    r["_field"] == "LHV_bio_WhV102" or
                    r["_field"] == "LHV_bio_WhV107" or
                    r["_field"] == "Energia_jouleV101" or
                    r["_field"] == "Energia_jouleV102" or
                    r["_field"] == "Energia_jouleV107" 
                )'''
        elif type == 9:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) =>
                r["device"] == "P104" or 
                r["device"] == "P101" or 
                r["device"] == "P102" or 
                r["device"] == "R101" or 
                r["device"] == "R102" or 
                r["device"] == "V101" or 
                r["device"] == "V102" or 
                r["device"] == "V107" or 
                r["device"] == "TK100"
            )
            |> last()
            '''
        elif type == 12:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: -{train_time}m)
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) =>
                r["device"] == "R101" or 
                r["device"] == "R102" or 
                r["device"] == "R103" or 
                r["device"] == "R104" or 
                r["device"] == "R105")
            |> last()
            '''
        
        elif type == 13:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: time(v: "{t_start_str}"), stop: time(v: "{t_end_str}"))
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) =>
                r["device"] == "R101" or 
                r["device"] == "R102" or 
                r["device"] == "R103" or 
                r["device"] == "R104" or 
                r["device"] == "R105")
            '''
        elif type == 14:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: -{train_time}m)
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) =>
                r["device"] == "R106" or 
                r["device"] == "R107" or 
                r["device"] == "R108" or 
                r["device"] == "R109" or 
                r["device"] == "R110")
            |> last()
            '''
        elif type == 15:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: time(v: "{t_start_str}"), stop: time(v: "{t_end_str}"))
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) =>
                r["device"] == "R106" or 
                r["device"] == "R107" or 
                r["device"] == "R108" or 
                r["device"] == "R109" or 
                r["device"] == "R110")
            '''
        elif type == 16:
            self.query = f'''
                from(bucket: "{self.bucket}")
                |> range(start: -{train_time}m)
                |> filter(fn: (r) => r["_measurement"] == "{measurement}")
                |> filter(fn: (r) => 
                    r["device"] == "interfaz" or
                    r["device"] == "dosificacion" or
                    r["device"] == "piscina")
                |> last()
                '''
        elif type == 17:
            self.query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: time(v: "{t_start_str}"), stop: time(v: "{t_end_str}"))
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) =>
                r["device"] == "interfaz" or 
                r["device"] == "dosificacion" or 
                r["device"] == "piscina")
            '''
            
        else:
            self.query = "Tipo de query inválido"
        
        return self.query