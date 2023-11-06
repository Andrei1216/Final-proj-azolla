#include <ArduinoJson.h>
#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(3, 2); // RX, TX pins

// Maximum JSON data size
const int maxJsonSize = 256; 

// H-BRIDGE
const int INPUT1 = 12;
const int INPUT2 = 13;

// MOISTURE SENSOR
const int MOISTURE_PIN = A0;

// TURN ON THE PUMP
void open_pump(int pump_id){

  digitalWrite(INPUT1, HIGH);
  digitalWrite(INPUT2, LOW);
  
  delay(5000);
}

// TURN OFF THE PUMP
void close_pump(int pump_id){
  digitalWrite(INPUT1, LOW);
  digitalWrite(INPUT2, LOW);
  delay(1000);
}

// MONITOR THE SOIL MOISTURE
int monitor_soil(){
  // Read the analog value from the soil moisture sensor
  int moisture_value = analogRead(MOISTURE_PIN);

  // Convert the analog value to a percentage (0% - 100%)
  int moisture_percentage = map(moisture_value, 0, 1023, 0, 100);

  return moisture_percentage;
}

// RETREIVE DATA FROM THE BLUETOOTH
char* receive_data(){
  // Check if data is available from Bluetooth module
  if (bluetoothSerial.available()) {
    char receivedChar = bluetoothSerial.read();
    Serial.print(receivedChar);
  }
}

// RETREIVE DATA TO THE BLUETOOTH
char* send_data(){
}


void setup() {
  Serial.begin(9600);   // Initialize serial communication
  bluetoothSerial.begin(9600); // Bluetooth module baud rate

  // H-BRIDGE
  pinMode(INPUT1, OUTPUT);
  pinMode(INPUT2, OUTPUT);

}

void loop() {

  char jsonBuffer[maxJsonSize];
  // Clear the buffer
  memset(jsonBuffer, 0, sizeof(jsonBuffer)); 

  // EXECUTE IF A BLUETOOTH SERIAL ARE AVAILABLE
  if (bluetoothSerial.available()) {
    // Read JSON data from Bluetooth module
    int bytesRead = bluetoothSerial.readBytesUntil('\n', jsonBuffer, maxJsonSize);

    if (bytesRead > 0) {
      // Parse the received JSON data
      StaticJsonDocument<200> jsonDoc; // Adjust the capacity as needed
      DeserializationError error = deserializeJson(jsonDoc, jsonBuffer);

      if (!error) {
        const int pump_id = jsonDoc["pump_id"];
        int status = jsonDoc["status"];

        if(status == 1){
          open_pump(pump_id);
        }else if(status == 0){
          close_pump(pump_id);
        }
        
      } else {
        Serial.println("Error parsing JSON");
      }
    }
  }

  // bluetoothSerial.println("Hello, Bluetooth!");
  // delay(1000); // Delay for 1 second

  // receive_data();
}