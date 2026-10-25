#include <Servo.h>

// constants won't change. They're used here to set pin numbers:
const int buttonPinStart = 11;     // the number of the pushbutton pin
const int buttonPinReset = 12;

const int ledGreen1 =  6;      // the number of the LED pin
const int ledGreen2 =  5;      // the number of the LED pin
const int ledYellow1 = 2;
const int ledYellow2 = 3;
const int ledRed = 4;

const int servoPin = 8;

const int blinkrate = 500; // toggle on/off every n ms

const int NOEVENT = 0;
const int TOLOW = -1;
const int TOHIGH = 1;

const long anglestepdelay = 1;
const long angleextremeposdelay = 400;
const int anglefrom = 60;
const int angleto = 110;
const int stepsize = 10;

const long onebellswing = (((angleto-anglefrom)/2+anglefrom)*2/stepsize)*anglestepdelay + angleextremeposdelay*2;
const long bellswings = 6;

const long countdowntime = 60; // seconds for countdown
const long finalwarningtime = 5; // seconds for final warning that bell starts immediately
const long bellduration = onebellswing*bellswings/1000; // seconds for bell ringing

// variables will change:
int currentStateStart = 0;         // variable for reading the pushbutton status
int currentStateReset = 0;         // variable for reading the pushbutton status
int lastStateStart = 0;         // variable for reading the pushbutton status
int lastStateReset = 0;         // variable for reading the pushbutton status
int eventStart = 0; // 0 ... no event, -1 ... to LOW, +1 ... to HIGH
int eventReset = 0; // 0 ... no event, -1 ... to LOW, +1 ... to HIGH

Servo servo;

int angle = (angleto-anglefrom)/2 + anglefrom;
int anglestep = stepsize;

bool cycleactive = false;
bool bellactive = false;
bool finalwarningactive = true;

long cyclestarttime = 0;
long nextbellupdatetime = 0;

int currentledpin = -1;

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
  Serial.print("   . anglefrom: "); Serial.println(anglefrom);  
  Serial.print("   . angleto: "); Serial.println(angleto);  
  Serial.print("   . stepsize: "); Serial.println(stepsize);  
}

void setup() {
  Serial.begin(500000);
  
  Serial.println("setup");
  printConfig();

  // initialize the LED pin as an output:
  pinMode(ledGreen1, OUTPUT);
  pinMode(ledYellow1, OUTPUT);
  pinMode(ledGreen2, OUTPUT);
  pinMode(ledYellow2, OUTPUT);
  pinMode(ledRed, OUTPUT);
  allLEDStoHIGH();

  // initialize the pushbutton pin as an input:
  pinMode(buttonPinStart, INPUT);
  pinMode(buttonPinReset, INPUT);

  // initialize the bell servo
  servo.attach(servoPin); 
}

void bellHandling() {
  if (bellactive) {
    if (millis() > nextbellupdatetime) {
      nextbellupdatetime = millis() + anglestepdelay;
      angle += anglestep;
      if (angle >= angleto) {
        Serial.println("reached angleto");
        angle = angleto;
        anglestep = -stepsize;
        nextbellupdatetime += angleextremeposdelay; // wait longer at extreme pos
      } else if (angle < anglefrom) {
        Serial.println("reached anglefrom");
        angle = anglefrom;
        anglestep = stepsize;
        nextbellupdatetime += angleextremeposdelay; // wait longer at extreme pos
      }
      servo.write(angle);
    }
  }
}

void buttonPreLoop() {
  currentStateStart = digitalRead(buttonPinStart);
  currentStateReset = digitalRead(buttonPinReset);

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

void startCycle() {
  Serial.println("countdown started");
  cycleactive = true;
  finalwarningactive = false;
  cyclestarttime = millis();
  currentledpin = -1;
}

void resetCycle() {
  Serial.println("countdown reset");
  cycleactive = false;
  bellactive = false;
  finalwarningactive = false;
  allLEDStoHIGH();
}

void allLEDStoHIGH() {
  digitalWrite(ledRed, HIGH);
  digitalWrite(ledGreen1, HIGH);
  digitalWrite(ledYellow1, HIGH);
  digitalWrite(ledGreen2, HIGH);
  digitalWrite(ledYellow2, HIGH);
}

void allLEDStoLOW() {
  digitalWrite(ledRed, LOW);
  digitalWrite(ledGreen1, LOW);
  digitalWrite(ledYellow1, LOW);
  digitalWrite(ledGreen2, LOW);
  digitalWrite(ledYellow2, LOW);
}

void countdownVisualization(int timelapsed) {
  long interval = countdowntime / 5;
  
  if (timelapsed < interval) {
    if (currentledpin != ledGreen1) {
      Serial.println("countdown green1");
      Serial.println(timelapsed);
      currentledpin = ledGreen1;
    }
  } else if (timelapsed < interval*2) {
    if (currentledpin != ledGreen2) {
      Serial.println("countdown green2");
      Serial.println(timelapsed);
      digitalWrite(currentledpin, LOW);
      currentledpin = ledGreen2;
    }
  } else if (timelapsed < interval*3) {
    if (currentledpin != ledYellow1) {
      Serial.println("countdown yellow1");
      Serial.println(timelapsed);
      digitalWrite(currentledpin, LOW);
      currentledpin = ledYellow1;
    }
  } else if (timelapsed < interval*4) {
    if (currentledpin != ledYellow2) {
      Serial.println("countdown yellow2");
      Serial.println(timelapsed);
      digitalWrite(currentledpin, LOW);
      currentledpin = ledYellow2;
    }
  } else {
    if (currentledpin != ledRed) {
      Serial.println("countdown red");
      Serial.println(timelapsed);
      digitalWrite(currentledpin, LOW);
      currentledpin = ledRed;          
    }
  }
  
  if ((millis() / blinkrate) % 2) {
    digitalWrite(currentledpin, HIGH);
  } else {
    digitalWrite(currentledpin, LOW);
  }
}


void countdownFinalWarning() {
  if (!finalwarningactive) {
    Serial.println("countdown final warning");
    finalwarningactive = true;
  }
  
  if ((millis() / blinkrate) % 2) {
    allLEDStoHIGH();
  } else {
    allLEDStoLOW();
  }  
}

void countdownStartBell() {
  if (!bellactive) {
    Serial.println("countdown bell");
    allLEDStoLOW();
    bellactive = true;
    finalwarningactive = false;
    nextbellupdatetime = millis();
  }
}

void finishCycle() {
  if (bellactive) {
    Serial.println("countdown finished");
    bellactive = false;
    Serial.println((angleto-anglefrom)/2+anglefrom);
    servo.write((angleto-anglefrom)/2+anglefrom);
    delay(10);
    finalwarningactive = false;
    allLEDStoLOW();
  }
}

void cycleManagement() {
  if (eventReset == TOHIGH && currentStateStart == HIGH) {
    Serial.println("bypassed countdown");
    startCycle();
    cyclestarttime = millis() - (countdowntime + finalwarningtime)*1000;
  } else if (eventStart == TOHIGH) {
    resetCycle();
    startCycle();
  } else if (eventReset == TOHIGH) {
    resetCycle();
  } 

  
    
  if (cycleactive) {
    int timelapsed = (millis() - cyclestarttime)/1000;
    if (timelapsed < countdowntime) { // countdown visualization via leds
      countdownVisualization(timelapsed);
    } else if (timelapsed < (countdowntime + finalwarningtime)) { // start final warning
      countdownFinalWarning();
    } else if (timelapsed < (countdowntime + finalwarningtime + bellduration)) { // start bell ringing
      countdownStartBell();
    } else { // finished cycle - deactivate and reset
      finishCycle();
    }
  }
}

void loop() {
  buttonPreLoop();
  cycleManagement();
  bellHandling();
  buttonPostLoop();
}
