// Firmware of the ESP32 variant (D-13, D-17): a LILYGO T-Display V1.1 on the carrier board variants/esp32.
// The countdown of src/firmware/buttons.ino, plus the module's display and a web page: status, time to ding, start,
// pause, stop and the timer. The countdown logic is lib/BellTimer, Wi-Fi and the web pages are net.cpp.
//
// Pins: checks.pin_locks in variants/esp32/hardware/graph.json. Buttons as on the Nano – start (while paused: go on),
// reset = stop, start held and reset = ring now – and for Wi-Fi: reset held 3 s and released = Wi-Fi on/off, held
// 10 s = forget the home network and open the setup hotspot. While reset is held, display and LEDs show what
// releasing it does: green = on/off, red = forget.

#include <Arduino.h>
#include <Preferences.h>
#include <TFT_eSPI.h>

#include "BellTimer.h"
#include "net.h"

// ========== PIN DEFINITIONS (graph checks.pin_locks) ==========
const int buttonPinStart = 38;  // input only, no internal pull: R7 pulls down, the button switches 3V3
const int buttonPinReset = 37;  // input only, R6 pulls down
const int ledPins[BellTimer::NUM_LEDS] = {27, 26, 25, 33, 32};  // green 1, green 2, yellow 1, yellow 2, red
const int servoPin = 13;

// ========== TIMING CONSTANTS ==========
const unsigned long DEBOUNCE_DELAY = 50;      // ms for button debouncing
const unsigned long HOLD_WIFI_MS = 3000;      // reset held this long: Wi-Fi on/off on release
const unsigned long HOLD_FORGET_MS = 10000;   // reset held this long: forget the home network on release
const uint32_t DEFAULT_TIMER_S = 65;          // 60 s countdown + 5 s final warning, as on the Nano
const unsigned long DISPLAY_EVERY = 100;      // ms between display updates

// ========== SERVO CONSTANTS (as buttons.ino) ==========
const unsigned long anglestepdelay = 1;           // ms between angle steps
const unsigned long angleextremeposdelay = 400;   // ms to wait at extreme positions
const int SERVO_MIN_ANGLE = 60;
const int SERVO_MAX_ANGLE = 110;
const int SERVO_REST_ANGLE = (SERVO_MIN_ANGLE + SERVO_MAX_ANGLE) / 2;  // 85 degrees
const int stepsize = 10;
const int SERVO_RANGE = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE;
const long onebellswing = ((SERVO_RANGE / 2) * 2 / stepsize) * anglestepdelay + angleextremeposdelay * 2;
const long bellswings = 6;
const unsigned long SERVO_SETTLE_MS = 1000;  // ms at rest before the servo is detached (D-13)
// 50 Hz on an LEDC channel; 0-180 degrees = 544-2400 us, as the Arduino Servo library
const int SERVO_CHANNEL = 2;
const int SERVO_FREQ = 50;
const int SERVO_BITS = 16;
const uint32_t SERVO_MIN_US = 544;
const uint32_t SERVO_MAX_US = 2400;

// ========== GLOBAL VARIABLES ==========
BellTimer bell(DEFAULT_TIMER_S, onebellswing * bellswings);
BellTimer::State lastState = BellTimer::IDLE;
TFT_eSPI tft;

// Buttons
int currentStateStart = LOW;
int currentStateReset = LOW;
int lastStateStart = LOW;      // debounced state of the previous loop (for the events)
int lastStateReset = LOW;
int lastReadingStart = LOW;    // raw reading of the previous loop (for debouncing)
int lastReadingReset = LOW;
unsigned long lastDebounceTimeStart = 0;
unsigned long lastDebounceTimeReset = 0;
bool resetholding = false;     // reset pressed alone: a Wi-Fi action when held long enough
unsigned long resetpressedtime = 0;

// Servo
bool servoattached = false;
int angle = SERVO_REST_ANGLE;
int anglestep = stepsize;
unsigned long nextbellupdatetime = 0;
unsigned long servodetachtime = 0;
bool servodetachpending = false;

// Display
bool setuplayout = false;
unsigned long nextdisplaytime = 0;
String shown[4];

// ========== HELPER FUNCTIONS ==========
// True once millis() has reached `when` – also across the millis() overflow
bool reached(unsigned long when) {
  return (long)(millis() - when) >= 0;
}

// m:ss or h:mm:ss, seconds rounded up
String clockText(uint32_t ms) {
  uint32_t s = (ms + 999) / 1000;
  char text[16];
  if (s >= 3600) {
    snprintf(text, sizeof text, "%lu:%02lu:%02lu", (unsigned long)(s / 3600), (unsigned long)(s / 60 % 60),
             (unsigned long)(s % 60));
  } else {
    snprintf(text, sizeof text, "%lu:%02lu", (unsigned long)(s / 60), (unsigned long)(s % 60));
  }
  return String(text);
}

// ========== SERVO ==========
void servoWrite(int deg) {
  uint32_t us = SERVO_MIN_US + (uint32_t)deg * (SERVO_MAX_US - SERVO_MIN_US) / 180;
  ledcWrite(SERVO_CHANNEL, us * ((1UL << SERVO_BITS) - 1) / 20000UL);
}

// Attach the servo for a bell phase
void servoAttach() {
  servodetachpending = false;
  if (!servoattached) {
    ledcSetup(SERVO_CHANNEL, SERVO_FREQ, SERVO_BITS);
    ledcAttachPin(servoPin, SERVO_CHANNEL);
    servoattached = true;
  }
}

// Move the servo to its rest position and detach it once it is there, so a jam at rest cannot load the
// module's 5V permanently (D-13)
void servoToRest() {
  servoAttach();
  angle = SERVO_REST_ANGLE;
  servoWrite(SERVO_REST_ANGLE);
  servodetachtime = millis() + SERVO_SETTLE_MS;
  servodetachpending = true;
}

void servoHandling() {
  if (servodetachpending && reached(servodetachtime)) {
    ledcDetachPin(servoPin);
    pinMode(servoPin, OUTPUT);
    digitalWrite(servoPin, LOW);
    servoattached = false;
    servodetachpending = false;
    Serial.println("servo detached");
  }
}

void bellHandling() {
  if (reached(nextbellupdatetime)) {
    nextbellupdatetime = millis() + anglestepdelay;
    angle += anglestep;
    if (angle >= SERVO_MAX_ANGLE) {
      angle = SERVO_MAX_ANGLE;
      anglestep = -stepsize;
      nextbellupdatetime += angleextremeposdelay;  // wait longer at extreme pos
    } else if (angle < SERVO_MIN_ANGLE) {
      angle = SERVO_MIN_ANGLE;
      anglestep = stepsize;
      nextbellupdatetime += angleextremeposdelay;
    }
    servoWrite(angle);
  }
}

// The servo follows the countdown: attached for the bell, to rest and detached after it
void stateChange(BellTimer::State from, BellTimer::State to) {
  Serial.printf("%s -> %s\n", BellTimer::stateName(from), BellTimer::stateName(to));
  if (to == BellTimer::RINGING) {
    servoAttach();
    nextbellupdatetime = millis();
  } else if (from == BellTimer::RINGING) {
    servoToRest();
  }
}

// ========== BUTTON HANDLING WITH DEBOUNCING (as buttons.ino) ==========
// What releasing reset would do now: 0 nothing, 1 Wi-Fi on/off, 2 forget the home network
int holdAction() {
  if (!resetholding || currentStateReset != HIGH) {
    return 0;
  }
  unsigned long held = millis() - resetpressedtime;
  return held >= HOLD_FORGET_MS ? 2 : held >= HOLD_WIFI_MS ? 1 : 0;
}

void buttonHandling() {
  unsigned long now = millis();

  int readingStart = digitalRead(buttonPinStart);
  if (readingStart != lastReadingStart) {
    lastDebounceTimeStart = now;
    lastReadingStart = readingStart;
  }
  if (now - lastDebounceTimeStart > DEBOUNCE_DELAY) {
    currentStateStart = readingStart;
  }

  int readingReset = digitalRead(buttonPinReset);
  if (readingReset != lastReadingReset) {
    lastDebounceTimeReset = now;
    lastReadingReset = readingReset;
  }
  if (now - lastDebounceTimeReset > DEBOUNCE_DELAY) {
    currentStateReset = readingReset;
  }

  bool pressedStart = currentStateStart == HIGH && lastStateStart == LOW;
  bool pressedReset = currentStateReset == HIGH && lastStateReset == LOW;
  bool releasedReset = currentStateReset == LOW && lastStateReset == HIGH;
  lastStateStart = currentStateStart;
  lastStateReset = currentStateReset;

  if (pressedReset && currentStateStart == HIGH) {
    Serial.println("bypassed countdown");
    bell.ringNow(now);
  } else if (pressedStart) {
    Serial.println("pressed start");
    resetholding = false;  // start during a long press: no Wi-Fi action
    bell.start(now);       // paused: go on; otherwise a fresh countdown
  } else if (pressedReset) {
    Serial.println("pressed reset");
    bell.stop();
    resetholding = true;
    resetpressedtime = now;
  }

  if (releasedReset && resetholding) {
    resetholding = false;
    unsigned long held = now - resetpressedtime;
    if (held >= HOLD_FORGET_MS) {
      Serial.println("reset held: forget the home network");
      net::forget();
    } else if (held >= HOLD_WIFI_MS) {
      Serial.println("reset held: wifi on/off");
      net::toggle();
    }
  }
}

// ========== LEDS AND DISPLAY ==========
void showLeds(uint32_t now) {
  uint8_t on = bell.leds(now);
  int action = holdAction();
  if (action == 1) {
    on = 0b00011;  // the green ones: Wi-Fi on/off
  } else if (action == 2) {
    on = 0b10000;  // red: forget the home network
  }
  for (int i = 0; i < BellTimer::NUM_LEDS; i++) {
    digitalWrite(ledPins[i], (on >> i) & 1 ? HIGH : LOW);
  }
}

void drawLine(int row, const String &text, int y, int font, uint16_t color) {
  if (text == shown[row]) {
    return;
  }
  shown[row] = text;
  tft.setTextColor(color, TFT_BLACK);
  tft.setTextDatum(TC_DATUM);
  tft.setTextPadding(tft.width());
  tft.drawString(text, tft.width() / 2, y, font);
}

// Rows: state, time to ding (when idle: the timer), Wi-Fi. While the setup hotspot is open and the bell is idle:
// its name and password instead.
void showDisplay(uint32_t now) {
  if (!reached(nextdisplaytime)) {
    return;
  }
  nextdisplaytime = millis() + DISPLAY_EVERY;

  BellTimer::State s = bell.state();
  bool setup = net::mode() == net::SETUP && s == BellTimer::IDLE;
  if (setup != setuplayout) {  // other fonts and rows: start from a blank screen
    setuplayout = setup;
    tft.fillScreen(TFT_BLACK);
    for (String &row : shown) {
      row = "\x01";
    }
  }

  // the built-in fonts have no umlauts
  static const char *const labels[] = {"Bereit", "Countdown", "Gleich!", "Pause", "Es laeutet"};
  int action = holdAction();
  String label = action == 2 ? "WLAN neu"
               : action == 1 ? (net::mode() == net::OFF ? "WLAN an" : "WLAN aus")
               : setup       ? "WLAN einrichten"
                             : labels[s];
  uint16_t labelColor = action || s != BellTimer::IDLE ? TFT_YELLOW : TFT_WHITE;

  if (setup) {
    drawLine(0, label, 4, 4, labelColor);
    drawLine(1, net::hotspotName(), 40, 4, TFT_WHITE);
    drawLine(2, "PW " + net::hotspotPassword(), 72, 4, TFT_WHITE);
    drawLine(3, action ? "Taste loslassen" : "http://192.168.4.1", 112, 2, TFT_LIGHTGREY);
  } else {
    drawLine(0, label, 4, 4, labelColor);
    drawLine(1, s == BellTimer::IDLE ? clockText(bell.timerS() * 1000) : clockText(bell.remainingMs(now)), 38, 7,
             TFT_WHITE);
    drawLine(3, action ? "Taste loslassen" : net::line(), 112, 2, TFT_LIGHTGREY);
  }
}

// ========== SETUP ==========
void setup() {
  Serial.begin(115200);
  Serial.println("setup");

  for (int i = 0; i < BellTimer::NUM_LEDS; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  pinMode(buttonPinStart, INPUT);
  pinMode(buttonPinReset, INPUT);

  // the bell servo: to its rest position, then detached
  servoToRest();

  Preferences prefs;
  prefs.begin("bell", true);
  bell.setTimer(prefs.getUInt("timer_s", DEFAULT_TIMER_S));
  prefs.end();
  Serial.printf("timer: %lu s\n", (unsigned long)bell.timerS());

  tft.init();
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);

  net::begin(bell);
}

// ========== MAIN LOOP ==========
void loop() {
  buttonHandling();
  net::loop();  // web commands

  uint32_t now = millis();
  bell.update(now);
  BellTimer::State s = bell.state();
  if (s != lastState) {
    stateChange(lastState, s);
    lastState = s;
  }
  if (s == BellTimer::RINGING) {
    bellHandling();
  }
  servoHandling();

  showLeds(now);
  showDisplay(now);
}
