#include <WiFi.h>
#include <HTTPClient.h>
#include "pitches.h"
#include <ESP32Servo.h>

#define RED_LED 18        // ESP32 pin GIOP18, connected to red RGB
#define GREEN_LED 19      // ESP32 pin GIOP19, connected to green RGB
#define BUZZER_PIN 21     // ESP32 pin GIOP21 connected to Buzzer
#define YELLOW_LED 25     // ESP32 pin GIOP25, connected to yellow RGB
#define SERVO_PIN 26      // ESP32 pin GIOP26, connected to servo motor

Servo servoMotor;

bool alreadyOpened = false;
bool alreadyClosed = false;

int melody[] = {
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};

// note durations: 4 = quarter note, 8 = eighth note, etc.:
int noteDurations[] = {
  4, 8, 8, 4, 4, 4, 4, 4
};

const char* ssid = "ssid";
const char* password = "password";

void setup() {
  Serial.begin(115200);
  delay(4000);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  pinMode(RED_LED, OUTPUT);      // set ESP32 pin to output mode
  pinMode(GREEN_LED, OUTPUT);    // set ESP32 pin to output mode
  pinMode(YELLOW_LED, OUTPUT);   // set ESP32 pin to output mode
  servoMotor.attach(SERVO_PIN);  // attaches the servo on ESP32 pin
}

void loop() {
  if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection status
    HTTPClient http;
    http.begin("https://172.20.10.5/getdata"); //URL of the Website
    int httpCode = http.GET();                 //Make the request
    if (httpCode > 0) { //Check for the returning code
        String payload = http.getString();
        Serial.println(payload);
        if (payload == "OPEN" && alreadyOpened == false){
          open_door();
          Serial.println("Open Door function ran!");
          alreadyOpened = true;
          alreadyClosed = false;
        }
        else if (payload == "CLOSE" && alreadyClosed == false){
          close_door();
          Serial.println("Close Door function ran!");
          alreadyClosed = true;
          alreadyOpened = false;
        }
    }
  else {Serial.println("Error on HTTP request");}
  http.end(); //Free the resources
  }
  delay(5000);
}

//To open the pod door
void open_door(){
  digitalWrite(RED_LED,LOW);        //OFF Red LED
  digitalWrite(GREEN_LED,LOW);      //ON Green LED, common anode RGB LED
  playMelody();                     // play opening song
  digitalWrite(YELLOW_LED,HIGH);    //ON Yellow LED
  servoMotor.write(90);             //Motor move to 90 degree/open the door
}

//To close thd pod door
void close_door(){
  digitalWrite(GREEN_LED,HIGH);     //OFF Green LED, common anode RGB LED
  //Blink Red LED and buzz 4 times
  for(int i = 0; i < 4; i++){
    digitalWrite(BUZZER_PIN, HIGH);
    digitalWrite(RED_LED,HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(RED_LED,LOW);
    delay(500);
  }
  servoMotor.write(0);            //Motor move to 0 degree/close the door
  digitalWrite(YELLOW_LED,LOW);   //OFF Yellow LED
  digitalWrite(RED_LED,HIGH);     //ON Red LED
}

float floatMap(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void playMelody() {
  // iterate over the notes of the melody:
  int size = sizeof(noteDurations) / sizeof(int);

  for (int thisNote = 0; thisNote < size; thisNote++) {
    // to calculate the note duration, take one second divided by the note type
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(BUZZER_PIN, melody[thisNote], noteDuration);

    // set a minimum time between the notes
    // the note's duration + 30%
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(BUZZER_PIN);
  }
}
