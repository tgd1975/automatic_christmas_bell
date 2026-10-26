#include <Servo.h>

// ========== PIN DEFINITIONS ==========
const int buttonPinStart = 11;     // the number of the pushbutton pin
const int buttonPinReset = 12;

const int ledGreen1 = 6;      // the number of the LED pin
const int ledGreen2 = 5;      // the number of the LED pin
const int ledYellow1 = 2;
const int ledYellow2 = 3;
const int ledRed = 4;

const int servoPin = 8;

// ========== TIMING CONSTANTS ==========
const unsigned long blinkrate = 500; // toggle on/off every n ms
const unsigned long DEBOUNCE_DELAY = 50; // ms for button debouncing

// ========== SERVO CONSTANTS ==========
const unsigned long anglestepdelay = 1; // ms between angle steps
const unsigned long angleextremeposdelay = 400; // ms to wait at extreme positions
const int SERVO_MIN_ANGLE = 60;
const int SERVO_MAX_ANGLE = 110;
const int SERVO_REST_ANGLE = (SERVO_MIN_ANGLE + SERVO_MAX_ANGLE) / 2; // 85 degrees
const int stepsize = 10;
const unsigned long SERVO_SETTLE_MS = 1000; // ms at rest before the servo is detached (D-3)

// Calculate one bell swing duration: (half swing * 2 / stepsize) * step delay + extreme pos delay * 2
const int SERVO_RANGE = SERVO_MAX_ANGLE - SERVO_MIN_ANGLE;
const long onebellswing = ((SERVO_RANGE / 2) * 2 / stepsize) * anglestepdelay + angleextremeposdelay * 2;
const long bellswings = 6;

const long countdowntime = 60; // seconds for countdown
const long finalwarningtime = 5; // seconds for final warning that bell starts immediately
const long bellduration = onebellswing * bellswings / 1000; // seconds for bell ringing

// ========== EVENT CONSTANTS ==========
const int NOEVENT = 0;
const int TOLOW = -1;
const int TOHIGH = 1;

// ========== STATE MACHINE ==========
enum SystemState {
  STATE_IDLE,
  STATE_COUNTDOWN,
  STATE_FINAL_WARNING,
  STATE_BELL_RINGING,
  STATE_FINISHED
};

// ========== GLOBAL VARIABLES ==========
// Button states
int currentStateStart = 0;         // variable for reading the pushbutton status
int currentStateReset = 0;         // variable for reading the pushbutton status
int lastStateStart = 0;            // debounced state of the previous loop (for the events)
int lastStateReset = 0;            // debounced state of the previous loop (for the events)
int lastReadingStart = LOW;        // raw reading of the previous loop (for debouncing)
int lastReadingReset = LOW;        // raw reading of the previous loop (for debouncing)
int eventStart = 0;                // 0 ... no event, -1 ... to LOW, +1 ... to HIGH
int eventReset = 0;                // 0 ... no event, -1 ... to LOW, +1 ... to HIGH
unsigned long lastDebounceTimeStart = 0;
unsigned long lastDebounceTimeReset = 0;

// Servo
Servo servo;
int angle = SERVO_REST_ANGLE;
int anglestep = stepsize;
unsigned long servodetachtime = 0;
bool servodetachpending = false;

// State
SystemState state = STATE_IDLE;
bool bellactive = false;
unsigned long cyclestarttime = 0;
unsigned long nextbellupdatetime = 0;

// LED Array for countdown visualization
const int ledPins[] = {ledGreen1, ledGreen2, ledYellow1, ledYellow2, ledRed};
const int numLEDs = 5;
int currentledpin = -1; // no countdown LED yet; countdownVisualization() checks for -1 before writing

// ========== HELPER FUNCTIONS ==========
// True once millis() has reached `when` – also across the millis() overflow
bool reached(unsigned long when) {
  return (long)(millis() - when) >= 0;
}

// Attach the servo for a bell phase
void servoAttach() {
  servodetachpending = false;
  if (!servo.attached()) {
    servo.attach(servoPin);
  }
}

// Move the servo to its rest position and detach it once it is there, so a jam at rest
// cannot load the Nano's 5V permanently (D-3)
void servoToRest() {
  servoAttach();
  angle = SERVO_REST_ANGLE;
  servo.write(SERVO_REST_ANGLE);
  servodetachtime = millis() + SERVO_SETTLE_MS;
  servodetachpending = true;
}

void servoHandling() {
  if (servodetachpending && reached(servodetachtime)) {
    servo.detach();
    servodetachpending = false;
    Serial.println("servo detached");
  }
}

void allLEDStoHIGH() {
  for (int i = 0; i < numLEDs; i++) {
    digitalWrite(ledPins[i], HIGH);
  }
}

void allLEDStoLOW() {
  for (int i = 0; i < numLEDs; i++) {
    digitalWrite(ledPins[i], LOW);
  }
}

void printConfig() {
  Serial.println("config");
  Serial.println(" - timings:");
  Serial.print("   . Countdown duration: "); Serial.println(countdowntime);
  Serial.print("   . Final warning duration: "); Serial.println(finalwarningtime);
  Serial.print("   . Bell duration: "); Serial.println(bellduration);
  Serial.print("   . Blinkrate: "); Serial.println(blinkrate);
  Serial.print("   . Anglestepdelay: "); Serial.println(anglestepdelay);
  Serial.print("   . Angleextremeposdelay: "); Serial.println(angleextremeposdelay);
  Serial.print("   . onebellswing: "); Serial.println(onebellswing);
  Serial.print("   . bellswings: "); Serial.println(bellswings);

  Serial.println(" - pins:");
  Serial.print("   . Button Start: "); Serial.println(buttonPinStart);
  Serial.print("   . Button Reset: "); Serial.println(buttonPinReset);
  Serial.print("   . Led Green 1: "); Serial.println(ledGreen1);
  Serial.print("   . Led Green 2: "); Serial.println(ledGreen2);
  Serial.print("   . Led Yellow 1: "); Serial.println(ledYellow1);
  Serial.print("   . Led Yellow 2: "); Serial.println(ledYellow2);
  Serial.print("   . Led Red: "); Serial.println(ledRed);
  Serial.print("   . Servo: "); Serial.println(servoPin);
  Serial.println(" - servo:");
  Serial.print("   . angle from: "); Serial.println(SERVO_MIN_ANGLE);
  Serial.print("   . angle to: "); Serial.println(SERVO_MAX_ANGLE);
  Serial.print("   . rest angle: "); Serial.println(SERVO_REST_ANGLE);
  Serial.print("   . stepsize: "); Serial.println(stepsize);
}

// ========== SETUP ==========
void setup() {
  Serial.begin(115200); // Changed from 500000 to 115200 for better compatibility

  Serial.println("setup");
  printConfig();

  // Initialize LED pins as outputs
  for (int i = 0; i < numLEDs; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  allLEDStoHIGH();

  // Initialize button pins as inputs
  pinMode(buttonPinStart, INPUT);
  pinMode(buttonPinReset, INPUT);

  // Initialize the bell servo: to its rest position, then detached
  servoToRest();
}

// ========== BUTTON HANDLING WITH DEBOUNCING ==========
void buttonPreLoop() {
  unsigned long now = millis();

  // Read and debounce Start button
  int readingStart = digitalRead(buttonPinStart);
  if (readingStart != lastReadingStart) {
    lastDebounceTimeStart = now;
    lastReadingStart = readingStart;
  }
  if (now - lastDebounceTimeStart > DEBOUNCE_DELAY) {
    currentStateStart = readingStart;
  }

  // Read and debounce Reset button
  int readingReset = digitalRead(buttonPinReset);
  if (readingReset != lastReadingReset) {
    lastDebounceTimeReset = now;
    lastReadingReset = readingReset;
  }
  if (now - lastDebounceTimeReset > DEBOUNCE_DELAY) {
    currentStateReset = readingReset;
  }

  // Calculate transition events
  eventStart = currentStateStart - lastStateStart;
  eventReset = currentStateReset - lastStateReset;

  if (eventStart == TOHIGH) {
    Serial.println("pressed A");
  }
  if (eventReset == TOHIGH) {
    Serial.println("pressed B");
  }
}

void buttonPostLoop() {
  lastStateStart = currentStateStart;
  lastStateReset = currentStateReset;
}

// ========== STATE TRANSITIONS ==========
void handleStateTransitions() {
  // Button-based transitions
  if (eventReset == TOHIGH && currentStateStart == HIGH) {
    Serial.println("bypassed countdown");
    if (bellactive) {
      servoToRest();
    }
    state = STATE_FINAL_WARNING;
    cyclestarttime = millis() - (countdowntime + finalwarningtime) * 1000;
    currentledpin = ledRed;
  } else if (eventStart == TOHIGH) {
    Serial.println("countdown started");
    if (bellactive) {
      servoToRest();
    }
    state = STATE_COUNTDOWN;
    cyclestarttime = millis();
    currentledpin = -1;
    bellactive = false;
  } else if (eventReset == TOHIGH) {
    Serial.println("countdown reset");
    if (bellactive) {
      servoToRest();
    }
    state = STATE_IDLE;
    allLEDStoHIGH();
    bellactive = false;
  }

  // Time-based transitions
  if (state == STATE_COUNTDOWN) {
    int timelapsed = (millis() - cyclestarttime) / 1000;
    if (timelapsed >= countdowntime) {
      Serial.println("countdown final warning");
      state = STATE_FINAL_WARNING;
    }
  } else if (state == STATE_FINAL_WARNING) {
    int timelapsed = (millis() - cyclestarttime) / 1000;
    if (timelapsed >= countdowntime + finalwarningtime) {
      Serial.println("countdown bell");
      state = STATE_BELL_RINGING;
      bellactive = true;
      servoAttach();
      nextbellupdatetime = millis();
      allLEDStoLOW();
    }
  } else if (state == STATE_BELL_RINGING) {
    int timelapsed = (millis() - cyclestarttime) / 1000;
    if (timelapsed >= countdowntime + finalwarningtime + bellduration) {
      state = STATE_FINISHED;
    }
  } else if (state == STATE_FINISHED) {
    finishCycle();
  }
}

// ========== STATE ACTIONS ==========
void bellHandling() {
  if (bellactive && state == STATE_BELL_RINGING) {
    if (reached(nextbellupdatetime)) {
      nextbellupdatetime = millis() + anglestepdelay;
      angle += anglestep;
      if (angle >= SERVO_MAX_ANGLE) {
        Serial.println("reached angleto");
        angle = SERVO_MAX_ANGLE;
        anglestep = -stepsize;
        nextbellupdatetime += angleextremeposdelay; // wait longer at extreme pos
      } else if (angle < SERVO_MIN_ANGLE) {
        Serial.println("reached anglefrom");
        angle = SERVO_MIN_ANGLE;
        anglestep = stepsize;
        nextbellupdatetime += angleextremeposdelay; // wait longer at extreme pos
      }
      servo.write(angle);
    }
  }
}

void countdownVisualization(int timelapsed) {
  long interval = countdowntime / numLEDs;
  int phase = timelapsed / interval;

  // Clamp phase to valid range
  if (phase < 0) phase = 0;
  if (phase >= numLEDs) phase = numLEDs - 1;

  if (currentledpin != ledPins[phase]) {
    if (currentledpin >= 0) {
      digitalWrite(currentledpin, LOW);
    }
    currentledpin = ledPins[phase];
    Serial.print("countdown phase ");
    Serial.println(phase);
    Serial.print("timelapsed: ");
    Serial.println(timelapsed);
  }

  // Blink the current LED
  if ((millis() / blinkrate) % 2) {
    digitalWrite(currentledpin, HIGH);
  } else {
    digitalWrite(currentledpin, LOW);
  }
}

void countdownFinalWarning() {
  // Blink all LEDs during final warning
  if ((millis() / blinkrate) % 2) {
    allLEDStoHIGH();
  } else {
    allLEDStoLOW();
  }
}

void finishCycle() {
  if (bellactive) {
    Serial.println("countdown finished");
    bellactive = false;
    servoToRest();
    nextbellupdatetime = millis() + 10; // Non-blocking delay
    allLEDStoLOW();
    state = STATE_IDLE;
  }
}

// ========== MAIN LOOP ==========
void loop() {
  buttonPreLoop();
  buttonPostLoop();

  handleStateTransitions();

  // Execute state-specific actions
  switch (state) {
    case STATE_COUNTDOWN: {
      int timelapsed = (millis() - cyclestarttime) / 1000;
      countdownVisualization(timelapsed);
      break;
    }
    case STATE_FINAL_WARNING:
      countdownFinalWarning();
      break;
    case STATE_BELL_RINGING:
      bellHandling();
      break;
    case STATE_IDLE:
    case STATE_FINISHED:
      // No specific actions needed
      break;
  }
  servoHandling();
}
