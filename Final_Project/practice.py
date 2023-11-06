import serial
import json
import time

# Replace 'COMx' with the correct serial port
ser = serial.Serial('COM5', 9600, timeout=1)

# while True:
data = {
    "pump_id": 2,
    "status": 0
}

json_data = json.dumps(data)  # Convert Python dictionary to JSON string
ser.write(json_data.encode())  # Send the JSON data to the Arduino

print(json_data)
time.sleep(1)  # Send data every 1 second

# import serial

# # Replace 'COMx' with the correct serial port and adjust the baud rate if needed
# ser = serial.Serial('COM5', 9600)

# while True:
#     try:
#         data = ser.readline().decode().strip()
#         if data:
#             print("Received:", data)
#     except KeyboardInterrupt:
#         break

# ser.close()