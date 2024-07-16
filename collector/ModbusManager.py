from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, Endian

class ModbusModel:
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port

    def ModbusConnection(self):
        self.ModbusClient = ModbusTcpClient(self.IP, port = self.port)
        
    def ModbusClose(self):
        self.ModbusClient.close()

    def ModbusReader(self, unitID, register, bytes, scale, sign):
        data = self.ModbusClient.read_holding_registers(register, bytes, slave = unitID)
        print(data)
        temp = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        if bytes == 2:
            if sign == 'Signed':
                readValue = float(temp.decode_32bit_int() / scale)
            elif sign == 'Unsigned':
                readValue = float(temp.decode_32bit_uint() / scale)
        elif bytes == 4:
            if sign == 'Signed':
                readValue = float(temp.decode_64bit_int() / scale)
            elif sign == 'Unsigned':
                readValue = float(temp.decode_64bit_uint() / scale)
        return readValue