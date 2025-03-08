#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "Wokwi-GUEST";  // Open network (no password needed)
const char* password = "";

// MongoDB API Endpoint (Replace with actual endpoint)
const char* serverName = "https://eternal-virtual-car-path-robot.onrender.com/update";

// Function to Fetch Simulated Sensor Data
float fetchOutsideTemperature() { return 10.0; }
float fetchHumidity() { return 30.0; }
float fetchPressure() { return 10.13; }
float fetchRadiation() { return 4.0; }

// Adjust heading to allow negative values instead of 357° using -3°
float adjustHeading(float heading) {
    return (heading > 180) ? heading - 360 : heading;
}

// Function to Generate a Simulated Car Update
void generateCarUpdate(float &x, float &y, float &battery, float &heading) {
  float speed = random(10, 20) / 10.0; // Speed between 1.0 to 2.0 m/s
  float distance = speed * 5 * 3.6 * 0.000008; // Convert meters to lat/lon change

  heading = adjustHeading(fmod(random(-3, 4) + heading, 360));

  x += distance * random(90, 110) / 100.0;
  y += distance * random(90, 110) / 100.0;
  x = constrain(x, -180, 180);
  y = constrain(y, -90, 90);

  battery = max(0.0f, battery - random(5, 20) / 100.0f);

  // Use JsonDocument instead of DynamicJsonDocument
  JsonDocument doc;
  doc["car_id"] = "CAR_1";
  doc["position"]["x"] = x;
  doc["position"]["y"] = y;
  doc["position"]["z"] = 0;
  doc["average_speed"] = speed;
  doc["battery_level"] = battery;
  doc["humidity"] = fetchHumidity();
  doc["pressure"] = fetchPressure();
  doc["radiation"] = fetchRadiation();
  doc["car_status"] = (battery > 0) ? "active" : "offline";
  doc["heading"] = heading;
  doc["fuel_level"] = 50;
  doc["temperature"] = fetchOutsideTemperature();
  doc["gps_accuracy"] = random(10, 100) / 100.0;

  String jsonString;
  serializeJson(doc, jsonString);

  if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST(jsonString);

      if (httpResponseCode > 0) {
          String response = http.getString();
          Serial.print("HTTP Response Code: ");
          Serial.println(httpResponseCode);
          Serial.print("Server Response: ");
          Serial.println(response);
      } else {
          Serial.print("Error Sending Request: ");
          Serial.println(httpResponseCode);
      }

      http.end();
  } else {
      Serial.println("WiFi Disconnected. Cannot send data.");
  }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    randomSeed(esp_random()); 
}

void loop() {
    static float x = -0.1276, y = 51.5074, battery = 100.0, heading = 0.0;
    generateCarUpdate(x, y, battery, heading);
    delay(1000);
}