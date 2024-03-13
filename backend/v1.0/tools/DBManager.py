import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# %%  InfluxDB Model        
class InfluxDBmodel:
    def __init__(self, server, org, bucket, token):
        self.server = server
        self.org = org
        self.token = token
        self.bucket = bucket

    # %%  InfluxDB Connection         
    def InfluxDBconnection(self):
        try:
            self.influxDBclient = InfluxDBClient(url = self.server, token = self.token)
            return 'Succesfully connected to the InfluxDB Database'
        except:
            return 'An error ocurred connecting to the InfluxDB Database'    

    # %%  InfluxDB Reader 
    def InfluxDBreader(self, query):
        self.query = query
        try:
            self.influxReturndf = self.influxDBclient.query_api().query_data_frame(self.query, self.org)
            return self.influxReturndf
        except:
            return 'An error ocurred reading the InfluxDB Database'

    # %%  InfluxDB Writer         
    def InfluxDBwriter(self, load, variable, value, timestamp):
        write_api = self.influxDBclient.write_api(write_options=SYNCHRONOUS)
        payload = influxdb_client.Point(load).field(variable, value)
        # payload = {"measurement": analyzer,
        #       "tags":{"_load": load},
        #       "fields": {variable: value},
        #      "time": timestamp}
        
        try:
            write_api.write(self.bucket, self.org, payload)
            
        except:
            return 'An error ocurred writing the InfluxDB Database'

    # %% InfluxDB query creator
    def QueryCreator(self, device, variable, location, type, forecastTime): #type 0: electrical last value, type 1: weather last value, type 2: electrical and weather forecast, type 3: next day forecast
        if type == 0:
            self.query = '''from(bucket: "''' + self.bucket + '''")
            |> range(start: -180m)
            |> filter(fn: (r) => r["_measurement"] == "''' + device + '''")
            |> filter(fn: (r) => r["_field"] == "''' + variable + '''")
            |> last() |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")''' #-10m
        elif type == 1:
            self.query ='''from(bucket: "''' + self.bucket + '''")
            |> range(start: -60m, stop: now()) 
            |> filter(fn: (r) => r["_measurement"] == "''' + device + '''")
            |> filter(fn: (r) => r["_field"] == "''' + variable + '''")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        elif type == 2:
            self.query ='''import "experimental"\nfrom(bucket: "''' + self.bucket + '''")
            |> range(start: -60m, stop: experimental.addDuration(d: ''' + str(forecastTime) + '''s, to: now()))
            |> filter(fn: (r) => r["_measurement"] == "forecast")
            |> filter(fn: (r) => r["_field"] == "''' + device + '''")
            |> filter(fn: (r) => r["location"] == "''' + location + '''")
            |> filter(fn: (r) => r["period"] == "0")
            |> last()'''
        elif type == 3:
            self.query ='''import "experimental"
            from(bucket: "''' + self.bucket + '''")
            |> range(start: ''' + forecastTime + ''', stop: experimental.addDuration(d: 24h, to: ''' + forecastTime + '''))
            |> filter(fn: (r) => r["_measurement"] == "forecast")
            |> filter(fn: (r) => r["_field"] == "''' + device + '''")
            |> filter(fn: (r) => r["location"] == "''' + location + '''")
            |> filter(fn: (r) => r["period"] == "0")'''
        else:
            self.query = "Tipo de query inválido"
        return self.query

