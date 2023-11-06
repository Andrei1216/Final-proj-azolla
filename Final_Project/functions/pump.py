# import serial
# # from ..configs.config_bluetooth import BAUD_RATE, PORT as BLUETOOTH_PORT
# PORT = "COM5"
# BAUD_RATE = 9600

# def get_distance():
#     try:
#         ser = serial.Serial(PORT, BAUD_RATE)
#         # print(f"Connected to {PORT} at {BAUD_RATE} baud")

#         while True:
#             if ser.in_waiting > 0:
#                 received_data = ser.readline().decode('utf-8').rstrip()
#                 return int(received_data)
#                 # print(f"Received data: { type(int(received_data)) }")

#     except Exception as e:
#         print(e)

# from flask_sqlalchemy import SQLAlchemy
    
class PumpFunction:
    def __init__(self, *args):
        self.args = args
        self.status = 0
    
    def open_pump(self):
        self.status = 1
        return self.status
    
    def close_pump(self):
        self.status = 0
        return self.status

        # self.pump_name = "Pump"

    # def scan(self, pin):
    #     # send data to controller 
    #     # controller detects if a new device has installed
    #     # send back to the server
    #     pass

    # def create(self, no_pump):
    #     sql = "INSERT INTO pump (id, pump_name, status) VALUES (%s, %s, %s)"
    #     pump_name = f"{self.name}{no_pump}"
    #     value = ()
    #     return f""

    
    