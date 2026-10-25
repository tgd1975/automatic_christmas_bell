# Weihnachtsglocke (Xmas Bell) - Projektbeschreibung

## Übersicht

Dieses Projekt ist eine automatische Weihnachtsglocke mit Countdown-Funktion. Das System verwendet einen Arduino Nano, einen Servo-Motor zur Betätigung der Glocke und mehrere LEDs für die visuelle Countdown-Anzeige. Zwei Taster ermöglichen das Starten und Zurücksetzen des Countdowns.

---

## Hardware-Komponenten

### aus Fritzing-Schaltplan (weihnachtsglocke.fzz)

| Komponente | Menge | Beschreibung |
|------------|-------|--------------|
| **Arduino Nano 3** | 1 | Mikrocontroller-Plattform |
| **Dagu DG Servo 9g** | 1 | Servo-Motor für Glockenschwung (männlicher Header) |
| **5mm farbige LEDs** | 5 | Countdown-Visualisierung (2x Grün, 2x Gelb, 1x Rot) |
| **Widerstände** | 7 | Vorwiderstände für LEDs und Pull-down für Taster |
| **Drucktaster** | 2 | Start- und Reset-Taster (S1, S2) |
| **Großer Elektrolyt-Kondensator** | 1 | Stabilisierung der Stromversorgung |
| **Steckbrett** | 1 | Breadboard RSR03MB102 für Prototypenaufbau |
| **Zweilagige PCB** | 1 | Optionale Platine (8,47 cm x 5,64 cm) |
| **Verkabelung** | 121+ | Verbindungskabel |

---

## Software-Architektur

### Arduino-Sketch (buttons.ino)

#### Pins und Anschlüsse

| Funktion | Pin | Beschreibung |
|----------|-----|--------------|
| **Servo** | 8 | Servo-Steuerung für Glockenschwung |
| **Button Start** | 11 | Start-Taster (Pull-down) |
| **Button Reset** | 12 | Reset-Taster (Pull-down) |
| **LED Grün 1** | 6 | Erste grüne LED (Countdown-Stufe 1) |
| **LED Grün 2** | 5 | Zweite grüne LED (Countdown-Stufe 2) |
| **LED Gelb 1** | 2 | Erste gelbe LED (Countdown-Stufe 3) |
| **LED Gelb 2** | 3 | Zweite gelbe LED (Countdown-Stufe 4) |
| **LED Rot** | 4 | Rote LED (Countdown-Stufe 5 / Finale Warnung) |

#### Servo-Parameter

- **Winkelbereich:** 60° bis 110°
- **Schrittgröße:** 10°
- **Schrittverzögerung:** 1 ms
- **Extrempositions-Verzögerung:** 400 ms
- **Ein Schwung:** ~4,4 Sekunden (berechnet aus Winkeln und Verzögerungen)
- **Anzahl Schwünge:** 6 pro Aktivierung
- **Glockendauer:** ~26,4 Sekunden

#### Timing-Parameter

- **Countdown-Dauer:** 60 Sekunden (konfigurierbar)
- **Finale Warnzeit:** 5 Sekunden (alle LEDs blinken schnell)
- **Blinkrate:** 500 ms (LED-Blinkfrequenz)

---

## Funktionsweise

### 1. System-Initialisierung

Bei jedem Start:
- Serielle Verbindung mit 500.000 Baud wird aufgebaut
- Alle LEDs werden auf HIGH (aus) gesetzt
- Servo wird initialisiert und in Mittelposition (85°) gebracht
- Systemkonfiguration wird über Serial Monitor ausgegeben

### 2. Countdown-Phasen

Der Countdown wird in 5 visuelle Phasen unterteilt:

| Phase | Dauer | LED | Bedeutung |
|-------|--------|-----|-----------|
| 1 | 0-12s | LED Grün 1 | Start - grüne Phase |
| 2 | 12-24s | LED Grün 2 | Zweite grüne Phase |
| 3 | 24-36s | LED Gelb 1 | Erste Warnphase |
| 4 | 36-48s | LED Gelb 2 | Zweite Warnphase |
| 5 | 48-60s | LED Rot | Letzte Phase vor Warnung |

### 3. Finale Warnung

- **Dauer:** 5 Sekunden (60-65s)
- **Verhalten:** Alle LEDs blinken schnell (500ms Intervall)
- **Zweck:** Visueller Hinweis, dass die Glocke gleich läutet

### 4. Glockenklingeln

- **Start:** Nach 65 Sekunden
- **Dauer:** ~26,4 Sekunden
- **Mechanismus:**
  - Servo bewegt sich pendelartig zwischen 60° und 110°
  - Jede Positionsänderung hat eine Verzögerung von 1ms
  - An den Extrempositionen wartet der Servo 400ms
  - Gesamt: 6 vollständige Schwingungen
- **LED-Verhalten:** Alle LEDs sind aus

### 5. Reset und Bypass

- **Reset-Taster (Pin 12):** Setzt den Countdown zurück
- **Start-Taster (Pin 11):** Startet neuen Countdown
- **Bypass-Funktion:** Wenn Reset gedrückt wird, während Start gedrückt ist, wird der Countdown übersprungen und die Glocke läutet sofort

---

## Schaltplan-Architektur

### Stromversorgung

- Arduino Nano wird über USB oder externe Quelle versorgt
- Servo benötigt separate Stromversorgung (5V) aufgrund des hohen Strombedarfs
- Elektrolyt-Kondensator stabilisiert die Spannung für das Servo

### Signalverbindungen

```
Arduino Nano
├── Pin 2  → LED Gelb 1
├── Pin 3  → LED Gelb 2
├── Pin 4  → LED Rot
├── Pin 5  → LED Grün 2
├── Pin 6  → LED Grün 1
├── Pin 8  → Servo Signal
├── Pin 11 → Taster Start (mit Pull-down-Widerstand)
└── Pin 12 → Taster Reset (mit Pull-down-Widerstand)

Jede LED hat einen eigenen Vorwiderstand (typischerweise 220Ω-1kΩ)
```

---

## Code-Struktur

### Wichtige Funktionen

| Funktion | Beschreibung |
|----------|--------------|
| `setup()` | Initialisiert Pins, Servo und serielle Verbindung |
| `loop()` | Hauptschleife - ruft alle anderen Funktionen auf |
| `buttonPreLoop()` | Liest Tasterzustände |
| `buttonPostLoop()` | Speichert Tasterzustände für nächsten Zyklus |
| `bellHandling()` | Steuerung des Servo-Schwungs |
| `cycleManagement()` | Verwaltung des gesamten Countdown-Zyklus |
| `countdownVisualization()` | Steuerung der LED-Anzeige |
| `countdownFinalWarning()` | Blinkende Warnung vor Glockenklingeln |
| `countdownStartBell()` | Startet das Glockenklingeln |
| `finishCycle()` | Beendet den Zyklus und setzt alles zurück |
| `printConfig()` | Gibt Konfiguration über Serial aus |

### Zustandsvariablen

| Variable | Typ | Beschreibung |
|----------|-----|--------------|
| `cycleactive` | bool | Gibt an, ob ein Countdown aktiv ist |
| `bellactive` | bool | Gibt an, ob die Glocke gerade läutet |
| `finalwarningactive` | bool | Gibt an, ob die finale Warnphase aktiv ist |
| `angle` | int | Aktueller Servo-Winkel |
| `anglestep` | int | Aktuelle Schrittgröße (+10 oder -10) |
| `currentledpin` | int | Aktuell aktive LED für Countdown |

---

## Konfigurationsmöglichkeiten

Die folgenden Parameter können einfach im Code angepasst werden:

```cpp
// Timing
const long countdowntime = 60;        // Countdown in Sekunden
const long finalwarningtime = 5;     // Warnzeit in Sekunden
const long blinkrate = 500;          // Blinkrate in ms

// Servo-Einstellungen
const int anglefrom = 60;            // Startwinkel
const int angleto = 110;             // Endwinkel
const int stepsize = 10;             // Schrittgröße
const long anglestepdelay = 1;       // Verzögerung zwischen Schritten
const long angleextremeposdelay = 400; // Verzögerung an Extrempositionen
const long bellswings = 6;          // Anzahl der Schwingungen

// Pin-Belegung
const int buttonPinStart = 11;
const int buttonPinReset = 12;
const int servoPin = 8;
const int ledGreen1 = 6;
const int ledGreen2 = 5;
const int ledYellow1 = 2;
const int ledYellow2 = 3;
const int ledRed = 4;
```

---

## Anwendungsfälle

### 1. Weihnachtsbaum-Dekoration
- Automatisches Läuten zu festgelegten Zeiten
- Visueller Countdown für Kinder

### 2. Timer für Spiele/Events
- Zeitmessung für Weihnachts-Spiele
- Visueller Timer für Gruppenaktivitäten

### 3. Lernprojekt
- Einführung in Servo-Steuerung
- Arbeit mit Tastern und LEDs
- State-Machine-Konzept

---

## Technische Spezifikationen

| Spezifikation | Wert |
|---------------|------|
| **Versorgungsspannung** | 5V (Arduino) + 5V (Servo) |
| **Stromverbrauch (Servo)** | ~500mA (im Betrieb) |
| **Stromverbrauch (LEDs)** | ~20mA pro LED |
| **Gesamtstrom** | ~600mA |
| **Abmessungen** | ~8,5 cm x 5,6 cm (PCB) |
| **Gewicht** | ~50-100g (ohne Gehäuse) |

---

## Erweiterungsmöglichkeiten

### Hardware
- [ ] Externes RTC-Modul für präzise Zeitmessung
- [ ] OLED-Display für numerischen Countdown
- [ ] Piezo-Lautsprecher für akustische Warnung
- [ ] EEPROM zum Speichern von Konfigurationen
- [ ] Bluetooth/WiFi-Modul für Fernsteuerung

### Software
- [ ] Mehrere vorprogrammierte Countdown-Zeiten
- [ ] Schlummerfunktion (Snooze)
- [ ] Automatische Aktivierung zu bestimmten Uhrzeiten
- [ ] Melodie-Wiedergabe während des Countdowns
- [ ] Web-Interface für Konfiguration

---

## Feindesign-Tipps

### 1. Mechanische Glocke
- Verwende einen stabilen Aufbau für die Glocke
- Der Servo-Hebel sollte lang genug sein für guten Schwung
- Achte auf ausgewogene Mechanik, um den Servo nicht zu überlasten

### 2. Elektronik
- Separate Stromversorgung für Servo empfohlen
- Kondensator (1000μF+) nahe am Servo platzieren
- alle Verbindungen fest löten oder mit Steckverbindern sichern

### 3. Gehäuse
- Schützendes Gehäuse für Außenbereich
- Transparentes Fenster für LED-Anzeige
- Einfacher Zugang zu Tastern

---

## Fehlersuche

| Problem | Mögliche Ursache | Lösung |
|---------|-------------------|--------|
| Glocke läutet nicht | Servo nicht richtig angeschlossen | Verbindung prüfen |
| LEDs bleiben dunkel | Falsche Pin-Belegung | Schaltplan prüfen |
| Countdown startet nicht | Taster nicht richtig verdrahtet | Pull-down-Widerstände prüfen |
| Servo zuckert | zu geringe Spannung | Separate Stromversorgung verwenden |
| Arduino startet neu | Stromspitze beim Servo | Großer Kondensator hinzufügen |

---

## Lizenz

Dieses Projekt ist Open Source und kann frei verwendet, modifiziert und verteilt werden.

---

*Letzte Aktualisierung: 25. Oktober 2025*
*Erstellt aus: buttons.ino und weihnachtsglocke.fzz*
