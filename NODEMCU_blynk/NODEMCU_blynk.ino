/*************************************************************
  Download latest Blynk library here:
    https://github.com/blynkkk/blynk-library/releases/latest

  Blynk is a platform with iOS and Android apps to control
  Arduino, Raspberry Pi and the likes over the Internet.
  You can easily build graphic interfaces for all your
  projects by simply dragging and dropping widgets.

    Downloads, docs, tutorials: http://www.blynk.cc
    Sketch generator:           http://examples.blynk.cc
    Blynk community:            http://community.blynk.cc
    Follow us:                  http://www.fb.com/blynkapp
                                http://twitter.com/blynk_app

  Blynk library is licensed under MIT license
  This example code is in public domain.

 *************************************************************

  You’ll need:
   - Blynk App (download from AppStore or Google Play)
   - NodeMCU board
   - Decide how to connect to Blynk
     (USB, Ethernet, Wi-Fi, Bluetooth, ...)

  There is a bunch of great example sketches included to show you how to get
  started. Think of them as LEGO bricks  and combine them as you wish.
  For example, take the Ethernet Shield sketch and combine it with the
  Servo example, or choose a USB sketch and add a code from SendData
  example.

  THIS CODE IS EDITED TO READ ATHE VOLTAGE AND AMPERE FROM PIN A0
 *************************************************************/

/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial


#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#define VIN A0 
const float VCC   = 5.0;
const int model = 2; 
float cutOffLimit = 1.01; 
float sensitivity[] ={
          0.185,// for ACS712ELCTR-05B-T
          0.100,// for ACS712ELCTR-20A-T
          0.066// for ACS712ELCTR-30A-T
     
         }; 
const float QOV =   0.5 * VCC;
float voltage;

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "4LrnMs0PkPlgyC6GDKrzBJYLdDZDjmfi";

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "akash";
char pass[] = "R3F2S5H3A7M5";

BlynkTimer timer;

void setup()
{
  // Debug console
  Serial.begin(9600);

  Blynk.begin(auth, ssid, pass);
  timer.setInterval(1000L, sensordata);
  digitalWrite(5,HIGH);
  digitalWrite(4,HIGH);
  digitalWrite(0,HIGH);
  digitalWrite(2,HIGH);
  // You can also specify server:
  //Blynk.begin(auth, ssid, pass, "blynk-cloud.com", 80);
  //Blynk.begin(auth, ssid, pass, IPAddress(192,168,1,100), 8080);
}

void sensordata()
{
  float voltage_raw =   (5.0 / 1023.0)* analogRead(VIN);
  voltage =  voltage_raw - QOV + 0.012 ;
  float current = voltage / sensitivity[model];
  if(abs(current) > cutOffLimit )
  {
    Serial.print("Analogue Read: ");
    Serial.print(analogRead(VIN),3);  // to get raw analogue value
    Serial.print(" V: ");
    Blynk.virtualWrite(V1, voltage);
    Serial.print(voltage,3);// print voltage with 3 decimal places
    Serial.print("V, I: ");
    Blynk.virtualWrite(V2, current);
    Serial.print(current,2); // print the current with 2 decimal places
    Serial.println("A");
  }
  else
  {
    Serial.println("No Current");
  }
  //delay(500);
    
}

void loop()
{
  Blynk.run();
  timer.run();
  // You can inject your own code or combine it with other sketches.
  // Check other examples on how to communicate with Blynk. Remember
  // to avoid delay() function!
}
