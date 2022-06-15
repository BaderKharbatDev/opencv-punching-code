#include <Servo.h>

//hardware vars
Servo tilt_servo;
Servo base_servo;
int base_servo_pin = 9;
int tilt_servo_pin = 11;
int relay_pin = 6;

//software vars
int base_servo_value = 90;
int tilt_servo_value = 90;
bool rotationChange = false;

void setup() {
  pinMode(relay_pin, OUTPUT);
  Serial.begin(9600);
  base_servo.attach(base_servo_pin);
  base_servo.write(base_servo_value);
  tilt_servo.attach(tilt_servo_pin);
  tilt_servo.write(tilt_servo_value);
}

void loop() {
  if(rotationChange) {
    base_servo.write(base_servo_value);
    tilt_servo.write(tilt_servo_value);
    rotationChange = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    String command = Serial.readStringUntil('|');
    if(command=="a"){
      String inByteA = Serial.readStringUntil('/'); // read data until newline
      String inByteB = Serial.readStringUntil('\n'); // read data until newline
      base_servo_value = inByteA.toInt();
      tilt_servo_value = inByteB.toInt();
      rotationChange = true;
    }else if(command=="b"){
      String inByteB = Serial.readStringUntil('\n'); // read data until newline 
      if(inByteB=="a"){
         digitalWrite(relay_pin, HIGH);
      } else if(inByteB=="b"){
         digitalWrite(relay_pin, LOW);
      }
    }
    
  }
}
