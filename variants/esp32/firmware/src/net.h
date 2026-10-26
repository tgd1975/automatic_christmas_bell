// Wi-Fi and web pages of the ESP32 bell (D-17). Without a home network the bell opens a setup hotspot (WPA2, name and
// password on its display) with a captive portal; the page there stores the home network. Then the bell joins it as a
// station and serves its page at http://glocke.local. Settings in NVS (Preferences "wifi"), kept over a power cut.
#pragma once

#include <Arduino.h>

#include "BellTimer.h"

namespace net {

enum Mode { OFF, CONNECTING, CONNECTED, SETUP };

void begin(BellTimer &bell);  // from the stored settings: off, the home network, or the setup hotspot
void loop();                  // hotspot DNS, web requests, connection watch
void toggle();                // Wi-Fi on <-> off
void forget();                // forget the home network and open the setup hotspot

Mode mode();
String hotspotName();
String hotspotPassword();
String line();                // the Wi-Fi line of the display

}  // namespace net
