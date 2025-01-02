#include <AFMotor.h>

String command;
#define iLED LED_BUILTIN
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);


void setup() {

  Serial.begin(9600);
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

  if (Serial.available()>0){
    Serial.print("OK!");
    command=Serial.read();
    Serial.print(command);
  }
  if (command=="49"){
    digitalWrite(iLED,LOW);
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor3.run(FORWARD);
    motor4.run(FORWARD);
  }
  // else{
  //   motor1.run(RELEASE);
  //   motor2.run(RELEASE);
  //   motor3.run(RELEASE);
  //   motor4.run(RELEASE);
  // }
  
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);

  // delay(7000);
  // motor1.run(RELEASE);
  // motor2.run(RELEASE);
  // motor3.run(RELEASE);
  // motor4.run(RELEASE);
  // delay(200);
  
  // motor1.run(BACKWARD);
  // motor2.run(BACKWARD);
  // motor3.run(BACKWARD);
  // motor4.run(BACKWARD);

  // delay(4000);
  // motor1.run(RELEASE);
  // motor2.run(RELEASE);
  // motor3.run(RELEASE);
  // motor4.run(RELEASE);
  // delay(200);
  
}
