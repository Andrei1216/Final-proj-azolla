import json
from configs.serial_config import ser

class Communication:

    def send_data(data):
        
        json_data = json.dumps(data)  # Convert Python dictionary to JSON string
        ser.write(json_data.encode())  # Send the JSON data to the Arduino

    def received_data():
        while True:

            try:
                data = ser.readline().decode().strip()
                if data:
                    return data

            except KeyboardInterrupt:
                break

        ser.close()