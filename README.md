Sketch used was Blynk Blink from https://examples.blynk.cc/?board=ESP8266&shield=ESP8266%20WiFi&example=GettingStarted%2FBlynkBlink

esp8266_pin			Blynk_APP_digital	Comments

GPIO0(SPI_CS2)			gp0			Works Perfect	
GPIO1(onboard_Blue_LED)		gp1     		Crash besause it is TX pin     	      
GPIO2				gp2			Works Perfect


API for turning pins on/off

API refereance https://blynkapi.docs.apiary.io/#reference/0/get-pin-value/get-pin-value

Example: http://blynk-cloud.com/Auth_Code/update/PIN?value=0

D2 = GP2 = GPIO2
D0 = gp0 = GPIO0

value=1 means off (in our case)
value=0 means on (in our case)

http://blynk-cloud.com/lOQoVl4dE2x_Gqim7qU-iLAfhpqRPbQs/update/D2?value=0 (for pin D2 (GP2) in 'ON' state )
http://blynk-cloud.com/lOQoVl4dE2x_Gqim7qU-iLAfhpqRPbQs/update/D2?value=1 (for pin D2 (GP2) in 'OFF' state )

http://blynk-cloud.com/lOQoVl4dE2x_Gqim7qU-iLAfhpqRPbQs/update/D0?value=0 (for pin D0 (GP0) in 'ON' state )
http://blynk-cloud.com/lOQoVl4dE2x_Gqim7qU-iLAfhpqRPbQs/update/D0?value=1 (for pin D0 (GP0) in 'OFF' state )


API for checking pin status (on/off)

Example: http://blynk-cloud.com/auth_token/get/pin

http://blynk-cloud.com/lOQoVl4dE2x_Gqim7qU-iLAfhpqRPbQs/get/D2 (check status of pin D2 (gp2) is on or off, Returns '1' if off or '0' if on  ) 

http://blynk-cloud.com/lOQoVl4dE2x_Gqim7qU-iLAfhpqRPbQs/get/D0 (check status of pin D0 (gp0) is on or off, Returns '1' if off or '0' if on  ) 


api and blynk api pin corections

blynk_app_pin	api_pin
D2		D4
D1		D5
D6		D12
D7		D13
D5		D14



D16	Blue led on board
D2	Blue led on board

blynk_app_pin	api_pin
D0  		    D16 
D1   		    D5
D2    		    D4 
D3 		        D0
D4   		    D2
D5   		    D14
D6   		    D12 
D7   		    D13
D8  		    D15
D9   		    D3
D10  		    D1








=======
API to check device connected or not

http://blynk-cloud.com/auth_token/isHardwareConnected
returns true or false





