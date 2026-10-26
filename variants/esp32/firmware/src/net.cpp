#include "net.h"

#include <DNSServer.h>
#include <ESPmDNS.h>
#include <Preferences.h>
#include <WebServer.h>
#include <WiFi.h>
#include <esp_wifi.h>

#include "webpage.h"

namespace net {
namespace {

const char *HOSTNAME = "glocke";        // http://glocke.local
const uint32_t TRY_NEW_MS = 30000;      // a new home network not reached by then: the setup hotspot again
const uint32_t SWITCH_DELAY_MS = 1500;  // after saving: time for the answer before the hotspot closes
const IPAddress AP_IP(192, 168, 4, 1);

BellTimer *bell = nullptr;
Preferences prefs;
WebServer server(80);
DNSServer dns;
Mode current = OFF;
bool serverOn = false;
bool mdnsOn = false;
String ssid, pass, apName, apPass;
bool verified = false;  // the stored home network was reached once
uint32_t connectStart = 0;
bool switchPending = false;
uint32_t switchAt = 0;

// Every Wi-Fi start: country DE with 802.11d off – channels 1-13 only, also when an access point announces another
// country (D-13 "Radio"). WiFi.mode(WIFI_OFF) deinitialises the driver, so this runs after each mode change.
bool radio(wifi_mode_t m) {
  WiFi.mode(m);
  esp_err_t err = esp_wifi_set_country_code("DE", false);
  if (err != ESP_OK) {
    Serial.printf("wifi: country DE failed (%d), radio off\n", err);
    WiFi.mode(WIFI_OFF);
    current = OFF;
    return false;
  }
  if (!serverOn) {
    server.begin();
    serverOn = true;
  }
  return true;
}

void radioOff() {
  dns.stop();
  if (mdnsOn) {
    MDNS.end();
    mdnsOn = false;
  }
  WiFi.softAPdisconnect(true);
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  current = OFF;
}

void startStation() {
  radioOff();
  if (!radio(WIFI_STA)) {
    return;
  }
  WiFi.begin(ssid.c_str(), pass.c_str());
  connectStart = millis();
  current = CONNECTING;
  Serial.printf("wifi: joining %s\n", ssid.c_str());
}

void startSetup() {
  radioOff();
  if (!radio(WIFI_AP_STA)) {  // the station part scans for networks
    return;
  }
  WiFi.softAPConfig(AP_IP, AP_IP, IPAddress(255, 255, 255, 0));
  WiFi.softAP(apName.c_str(), apPass.c_str());
  dns.start(53, "*", AP_IP);  // every name leads to the setup page: the phone shows it as a login page
  WiFi.scanNetworks(true);
  current = SETUP;
  Serial.printf("wifi: setup hotspot %s, password %s, http://%s\n", apName.c_str(), apPass.c_str(),
                AP_IP.toString().c_str());
}

String json(const String &s) {
  String out = "\"";
  for (char c : s) {
    if (c == '"' || c == '\\') {
      out += '\\';
      out += c;
    } else if ((uint8_t)c >= 0x20) {
      out += c;
    }
  }
  return out + "\"";
}

void sendPage(const char *body) {
  String page(PAGE_HEAD);
  page += body;
  server.send(200, "text/html; charset=utf-8", page);
}

// ---------- the bell page ----------
void sendStatus() {
  char text[96];
  snprintf(text, sizeof text, "{\"state\":\"%s\",\"remaining_ms\":%lu,\"timer_s\":%lu}",
           BellTimer::stateName(bell->state()), (unsigned long)bell->remainingMs(millis()),
           (unsigned long)bell->timerS());
  server.send(200, "application/json", text);
}

void handleRoot() {
  sendPage(current == SETUP ? SETUPPAGE : BELLPAGE);
}

void handleBellPage() {
  sendPage(BELLPAGE);
}

void handleStart() {
  bell->start(millis());
  sendStatus();
}

void handlePause() {
  bell->pause(millis());
  sendStatus();
}

void handleStop() {
  bell->stop();
  sendStatus();
}

void handleTimer() {
  long s = server.arg("s").toInt();
  if (s <= 0 || !bell->setTimer((uint32_t)s)) {
    server.send(400, "text/plain", "timer: 10 s ... 24 h");
    return;
  }
  Preferences bellPrefs;
  bellPrefs.begin("bell", false);
  bellPrefs.putUInt("timer_s", bell->timerS());
  bellPrefs.end();
  sendStatus();
}

// ---------- the setup page ----------
void handleNetworks() {
  int n = WiFi.scanComplete();  // -1: scanning, -2: no scan
  String out = String("{\"scanning\":") + (n == -1 ? "true" : "false") + ",\"networks\":[";
  for (int i = 0; i < n; i++) {
    if (i) {
      out += ",";
    }
    out += "{\"ssid\":" + json(WiFi.SSID(i)) + ",\"rssi\":" + String(WiFi.RSSI(i)) + "}";
  }
  server.send(200, "application/json", out + "]}");
}

void handleScan() {
  if (current == SETUP && WiFi.scanComplete() != -1) {
    WiFi.scanDelete();
    WiFi.scanNetworks(true);
  }
  server.send(204);
}

void handleSave() {
  String s = server.arg("ssid");
  String p = server.arg("pass");
  if (current != SETUP) {
    server.send(409, "text/plain", "only in the setup hotspot");
    return;
  }
  if (s.isEmpty() || s.length() > 32 || p.length() > 63 || (p.length() > 0 && p.length() < 8)) {
    server.send(400, "text/plain; charset=utf-8",
                "Netzwerkname 1 bis 32 Zeichen, Passwort 8 bis 63 Zeichen (leer bei einem offenen WLAN)");
    return;
  }
  ssid = s;
  pass = p;
  verified = false;
  prefs.putString("ssid", ssid);
  prefs.putString("pass", pass);
  prefs.putBool("verified", false);
  sendPage(SAVEDPAGE);
  switchPending = true;
  switchAt = millis() + SWITCH_DELAY_MS;
}

void handleNotFound() {
  if (current == SETUP) {  // captive portal: every page is the setup page
    server.sendHeader("Location", String("http://") + AP_IP.toString() + "/", true);
    server.send(302, "text/plain", "");
    return;
  }
  server.send(404, "text/plain", "not found");
}

}  // namespace

void begin(BellTimer &b) {
  bell = &b;
  prefs.begin("wifi", false);
  WiFi.persistent(false);       // the settings live in our own NVS namespace
  WiFi.setHostname(HOSTNAME);   // before the first WiFi.mode(): taken when the interface starts
  ssid = prefs.getString("ssid", "");
  pass = prefs.getString("pass", "");
  verified = prefs.getBool("verified", false);

  apPass = prefs.getString("appass", "");
  if (apPass.length() != 8) {  // made once per module, shown on the display
    char digits[9];
    for (int i = 0; i < 8; i++) {
      digits[i] = '0' + esp_random() % 10;
    }
    digits[8] = 0;
    apPass = digits;
    prefs.putString("appass", apPass);
  }
  uint64_t mac = ESP.getEfuseMac();
  char name[16];
  snprintf(name, sizeof name, "Glocke-%02X%02X", (unsigned)(mac >> 32) & 0xFF, (unsigned)(mac >> 40) & 0xFF);
  apName = name;

  server.on("/", HTTP_GET, handleRoot);
  server.on("/glocke", HTTP_GET, handleBellPage);
  server.on("/api/status", HTTP_GET, sendStatus);
  server.on("/api/start", HTTP_POST, handleStart);
  server.on("/api/pause", HTTP_POST, handlePause);
  server.on("/api/stop", HTTP_POST, handleStop);
  server.on("/api/timer", HTTP_POST, handleTimer);
  server.on("/api/networks", HTTP_GET, handleNetworks);
  server.on("/api/scan", HTTP_POST, handleScan);
  server.on("/setup", HTTP_POST, handleSave);
  server.onNotFound(handleNotFound);

  if (!prefs.getBool("on", true)) {
    WiFi.mode(WIFI_OFF);
    Serial.println("wifi: off");
  } else if (ssid.isEmpty()) {
    startSetup();
  } else {
    startStation();
  }
}

void loop() {
  if (current == SETUP) {
    dns.processNextRequest();
  }
  if (serverOn && current != OFF) {
    server.handleClient();
  }
  if (switchPending && (int32_t)(millis() - switchAt) >= 0) {
    switchPending = false;
    startStation();
  }
  if (current == CONNECTING && WiFi.status() == WL_CONNECTED) {
    current = CONNECTED;
    if (!verified) {
      verified = true;
      prefs.putBool("verified", true);
    }
    if (!mdnsOn) {
      mdnsOn = MDNS.begin(HOSTNAME);
      if (mdnsOn) {
        MDNS.addService("http", "tcp", 80);
      }
    }
    Serial.printf("wifi: http://%s.local, http://%s\n", HOSTNAME, WiFi.localIP().toString().c_str());
  } else if (current == CONNECTED && WiFi.status() != WL_CONNECTED) {
    current = CONNECTING;  // the core reconnects by itself
    connectStart = millis();
  } else if (current == CONNECTING && !verified && millis() - connectStart >= TRY_NEW_MS) {
    Serial.println("wifi: the new network was not reached, setup hotspot again");
    startSetup();
  }
}

void toggle() {
  bool on = current == OFF;
  prefs.putBool("on", on);
  if (!on) {
    radioOff();
    Serial.println("wifi: off");
  } else if (ssid.isEmpty()) {
    startSetup();
  } else {
    startStation();
  }
}

void forget() {
  ssid = "";
  pass = "";
  verified = false;
  prefs.remove("ssid");
  prefs.remove("pass");
  prefs.remove("verified");
  prefs.putBool("on", true);
  startSetup();
}

Mode mode() {
  return current;
}

String hotspotName() {
  return apName;
}

String hotspotPassword() {
  return apPass;
}

String line() {
  switch (current) {
    case CONNECTED:
      return String(HOSTNAME) + ".local  " + WiFi.localIP().toString();
    case CONNECTING:
      return "WLAN " + ssid.substring(0, 20) + " ...";
    case SETUP:
      return "Hotspot " + apName;
    default:
      return "WLAN aus";
  }
}

}  // namespace net
