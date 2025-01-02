#include <AFMotor.h>
#include <SoftwareSerial.h>

// Define RX and TX pins for SoftwareSerial
SoftwareSerial BTSerial(0, 1); // RX, TX

char received;
char data;
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);


void setup() {
  Serial.begin(9600);         // Initialize Serial Monitor
  BTSerial.begin(9600);       // Baud rate for HC-05 communication
  Serial.println("HC-05 Bluetooth Communication Ready");
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
  
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);

}

void loop() {
  // Check if data is available from HC-05
  if (BTSerial.available()) {
    char received = BTSerial.read(); // Read a single character
    Serial.print("Received: ");      // Print label
    Serial.println(received);        // Print the received character
  }
  if (received=='f'){
    forward();
  }
  if (received=='b'){
    back();
  }
  if (received=='r'){
    right();
  }
  if (received=='l'){
    left();
  }


  // Check if data is available from Serial Monitor (for testing)
  if (Serial.available()) {
    data = Serial.read();       // Read a single character from Serial Monitor
    BTSerial.write(data);            // Forward it to HC-05
    Serial.print("Sent: ");          // Print label
    Serial.println(data);            // Confirm the sent data

  }
}

void forward(){
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void back(){
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);

}
void right(){
  motor1.run(FORWARD);
  motor2.run(FORWARD);
}

void left(){
  motor4.run(FORWARD);
  motor3.run(FORWARD);
}

