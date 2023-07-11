#include <WiFi.h>
#include <Wire.h>
#include <WebSocketsServer.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver servos = Adafruit_PWMServoDriver(0x40);

//ssid y contraseña del wifi
const char* ssid = "rizoPc";
const char* password = "sandra18";

WebSocketsServer webSocket = WebSocketsServer(80);

int Dedo_accion[5] = {0, 0, 0, 0, 0};

int pos0 = 102;
int pos180 = 512;
int valorS[5] = {0, 1, 2, 3, 4};

void onWebSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length){
  switch(type){
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_CONNECTED:
      {
        IPAddress ip = webSocket.remoteIP(num);
        Serial.printf("[%u] Connection from ", num);
        Serial.println(ip.toString());
      }
      break;
    case WStype_TEXT:
      Serial.printf("[%u] Text: %s\n", num, payload);
      webSocket.sendTXT(num, payload);
      //Serial.print(payload[0]);
    
    
      break;
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
    default:
      break;
  }
}

void setup() {
  servos.begin();
  servos.setPWMFreq(50);
  Serial.begin(115200);

  Serial.println("Connecting");
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("Connected!");
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
}

void loop() {
  webSocket.loop();
}

void setServo(uint8_t n_servo, int angulo){
  int duty;
  duty = map(angulo, 0, 180, pos0, pos180);
  servos.setPWM(n_servo, 0, duty);
}
