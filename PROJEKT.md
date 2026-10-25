# Weihnachtsglocke (Christkind-Klingel)

## Uebersicht

Automatische mechanische Weihnachtsglocke fuer den traditionellen Christkind-Brauch an Heiligabend.

**Ablauf (mit elektrischen Kerzen):**
1. Eltern bereiten Geschenke am Weihnachtsbaum vor
2. **Elektrische Kerzen EINSCHALTEN** -> Baum leuchtet
3. **Start-Taster druecken** -> Countdown beginnt (LEDs zeigen Zeit an)
4. Eltern verlassen den Raum
5. **Nach 65 Sekunden laeutet die Glocke automatisch**
6. Kinder hoeren das Laeuten und stuermen herein -> Bescherung beginnt! 🎅✨

WICHTIG: 
- Die Glocke wird PHYSIKALISCH angeschlagen (nicht elektronisch)
- ELEKTRISCHE KERZEN werden VOR dem Start eingeschaltet und bleiben an
- Kein Kerzen-Ausblasen noetig!

---

## Anwendungsfall

### Traditioneller Hintergrund
In Oesterreich und Teilen Deutschlands bringt das Christkind die Geschenke. Die Eltern muessen den Raum verlassen, waehrend das Christkind seine Arbeit erledigt. Das Laeuten einer kleinen, hellen Glocke signalisiert, dass das Christkind fertig ist.

### Diese Schaltung loest das Problem (mit elektrischen Kerzen):
- Diskret: Keine elektronischen Toene, sondern mechanische Glocke
- Zeitgesteuert: Eltern haben Zeit, den Raum zu verlassen
- Einfach: Ein Tastendruck startet alles
- Zuverlaessig: Servo-Mechanik fuer praezises Anschlagen
- **Sicher: Elektrische Kerzen - kein Feuerrisiko!**

---

## Hardware-Komponenten

Aus Fritzing-Schaltplan (weihnachtsglocke.fzz):

Komponenten:
- Arduino Nano 3 (1x) - Mikrocontroller
- Dagu DG Servo 9g (1x) - Servo-Motor fuer mechanische Glockenbetaetigung
- 5mm farbige LEDs (5x) - Visueller Countdown (2x Gruen, 2x Gelb, 1x Rot)
- Widerstaende (7x) - Vorwiderstaende fuer LEDs und Pull-down fuer Taster
- Drucktaster (2x) - Start-Taster (Pin 11) und Reset-Taster (Pin 12)
- Grosser Elektrolyt-Kondensator (1x) - Stabilisierung der Servo-Stromversorgung
- Steckbrett (1x) - Breadboard RSR03MB102 fuer Prototypen
- Zweilagige PCB (1x) - Optionale Platine (8.47 cm x 5.64 cm)
- **Elektrische Kerzen** - Werden VOR dem Start eingeschaltet

---

## Software-Architektur

### Arduino-Sketch (buttons.ino)

Pins und Anschluesse:
- Servo: Pin 8 (Servo-Steuerung fuer Glockenanschlag)
- Button Start: Pin 11 (Pull-down mit 10kOhm)
- Button Reset: Pin 12 (Pull-down mit 10kOhm)
- LED Gruen 1: Pin 6
- LED Gruen 2: Pin 5
- LED Gelb 1: Pin 2
- LED Gelb 2: Pin 3
- LED Rot: Pin 4

Servo-Parameter:
- Winkelbereich: 60 bis 110 Grad (50 Grad Gesamt-Schwingbereich)
- Schrittgroesse: 10 Grad
- Schrittverzoegerung: 1 ms
- Extrempositions-Verzoegerung: 400 ms
- Ein Schwung: ca. 4.4 Sekunden
- Anzahl Schwuenge: 6 pro Aktivierung
- Glockendauer: ca. 26.4 Sekunden

Timing-Parameter (anpassbar):
- countdowntime: 60 Sekunden (30-45s empfohlen fuer Christkind-Szenario)
- finalwarningtime: 5 Sekunden
- blinkrate: 500 ms

---

## Funktionsweise

### 1. Ablauf mit elektrischen Kerzen

**NEUER ABLAUF:**
1. Eltern bereiten Geschenke am Weihnachtsbaum vor
2. **Elektrische Kerzen EINSCHALTEN** -> Baum leuchtet schjon
3. **Start-Taster druecken** -> Countdown beginnt
4. Eltern verlassen den Raum
5. Nach 65 Sekunden laeutet die Glocke
6. Kinder kommen rein

**Vorteile elektrischer Kerzen:**
- Kein Feuerrisiko -> Eltern koennen Raum laenger verlassen
- Kein Ausblasen noetig
- Wetterunabhaengig
- Wiederverwendbar

### 2. Mechanische Glocke

Der Servo muss mit einem Hebel oder Arm verbunden sein, der eine ECHTE Glocke physisch anschlaegt.

Moegliche Ausfuehrungen:
- Direkter Anschlag: Servo-Horn mit kleinem Arm -> Glocke
- Hebeluebersetzung: Kurzer Arm am Servo, langer Arm mit Kloepfel an der Glocke
- Seilzug: Nylonfaden vom Servo zum Kloepfel der Glocke

### 3. Countdown-Phasen (fuer Eltern sichtbar)

Phase 1: 0-12s - LED Gruen 1 (noch viel Zeit)
Phase 2: 12-24s - LED Gruen 2
Phase 3: 24-36s - LED Gelb 1 (bereit machen zum Gehen)
Phase 4: 36-48s - LED Gelb 2 (langsam Richtung Tuer)
Phase 5: 48-60s - LED Rot (JETZT GEHEN!)

### 4. Finale Warnung (5 Sekunden)

- Alle LEDs blinken schnell (500ms Intervall)
- Letzte Chance fuer Eltern, die Tuer zu schliessen

### 5. Glockenklingeln

- Start: Nach 65 Sekunden (60s Countdown + 5s Warnung)
- Dauer: ca. 26.4 Sekunden
- Mechanismus: Servo pendelt zwischen 60 und 110 Grad
- 6 vollstaendige Schwingungen = mehrere klare Glockenschlaege
- LEDs sind aus (keine Ablenkung)

### 6. Reset und Bypass

- Reset-Taster: Setzt Countdown zurueck
- Start-Taster: Startet neuen Countdown
- Bypass: Reset + Start gedrueckt = sofortiges Laeuten (Test)

---

## Schaltplan-Architektur

Stromversorgung:
- Arduino Nano: USB oder externe 5V
- Servo: SEPARATE Stromversorgung empfohlen! (5V, mind. 1A)
  - Servo kann Stromspitzen verursachen, die Arduino resetten
  - Grosser Kondensator (1000uF+) direkt am Servo verhindert dies
- LEDs: Werden vom Arduino versorgt (max. 20mA pro LED)
- **Elektrische Kerzen: Separate Stromversorgung (Batterien/Netzteil)**

Signalverbindungen:
Arduino Nano:
- Pin 2 -> LED Gelb 1 (mit 220-1kOhm Widerstand)
- Pin 3 -> LED Gelb 2 (mit 220-1kOhm Widerstand)
- Pin 4 -> LED Rot (mit 220-1kOhm Widerstand)
- Pin 5 -> LED Gruen 2 (mit 220-1kOhm Widerstand)
- Pin 6 -> LED Gruen 1 (mit 220-1kOhm Widerstand)
- Pin 8 -> Servo Signal (gelbes Kabel)
- Pin 11 -> Taster Start (mit 10kOhm Pull-down)
- Pin 12 -> Taster Reset (mit 10kOhm Pull-down)

Servo-Stromversorgung:
- Rot -> 5V (separate Versorgung!)
- Braun -> GND

---

## Mechanischer Aufbau

### Servo-Glocken-Mechanismus

Option 1: Direkter Anschlag
Servo-Horn -> Kleiner Holz/Kunststoffarm (5-10 cm) -> Gummikopf/Filz -> Glocke

Option 2: Hebeluebersetzung (fuer mehr Kraft)
Servo-Horn -> Kurzer Arm -> Hebel (Drehpunkt in Mitte) -> Glocke-Seite (langer Arm mit Kloepfel)

Option 3: Seilzug (fuer entfernte Glocke)
Servo-Horn -> Nylonfaden -> Kloepfel der Glocke

### Gehaeuse-Empfehlungen

1. Kompakt: Alles in kleiner Holzkiste (z.B. 15x10x8 cm)
2. Glocke aussen: Glocke sichtbar oben auf dem Gehaeuse
3. Taster zugaenglich: Start/Reset-Taster an der Seite
4. LEDs sichtbar: LED-Anzeige an der Front fuer Eltern
5. Belueftung: Loecher fuer Servo-Kuehlung

### Materialien fuer die Glocke

- Messing: Hell, klarer Klang (traditionell)
- Bronze: Warmer, tiefer Klang
- Eisen: Metallisch (rostet ohne Schutz)
- Schellen: Hell, hoch (mehrere fuer intensiveren Klang)
- Glas: Hoch, klar (Vorsicht - zerbrechlich)

---

## Anpassungen fuer Christkind-Szenario (mit elektrischen Kerzen)

### 1. Kuerzerer Countdown
In buttons.ino aendern:
const long countdowntime = 30;  // Statt 60 Sekunden

**Begründung:** Da die Kerzen elektrisch sind und nicht ausgeblasen werden muessen, 
koennen die Eltern den Raum laenger verlassen. Allerdings sollte der Countdown 
kurz genug sein, damit die Spannung erhalten bleibt.

### 2. Laengerer Countdown (alternativ)
const long countdowntime = 90;  // Wenn Eltern mehr Zeit brauchen

### 3. Lauteres Laeuten
- Mehr Schwingungen: const long bellswings = 10;
- Groesserer Winkelbereich: const int anglefrom = 45; const int angleto = 135;
- Laengere Pause: const long angleextremeposdelay = 600;

### 4. Deutlichere Warnung
- Laengere Warnphase: const long finalwarningtime = 8;
- Schnelleres Blinken: const long blinkrate = 300;

---

## Technische Spezifikationen

- Versorgung Arduino: 5V (USB oder extern)
- Versorgung Servo: 5V (SEPARAT!)
- Strom Servo: ~500mA (Spitzen bis 1A)
- Strom LEDs: ~20mA pro LED (5 LEDs = ~100mA)
- **Versorgung Kerzen: je nach Typ (Batterien 3V/4.5V oder Netzteil 12V/24V)**
- Gesamtstrom: ~600mA (ohne Spitzen, ohne Kerzen)
- Abmessungen PCB: 8.47 cm x 5.64 cm
- Gewicht: ~50-100g (ohne Gehaeuse und Glocke)

---

## Fehlersuche

Problem: Glocke laeutet nicht -> Servo nicht richtig angeschlossen
Problem: Glocke zu leise -> Servo-Hebel zu kurz, laengeren verwenden
Problem: LEDs dunkel -> Falsche Pin-Belegung
Problem: Countdown startet nicht -> Pull-down-Widerstaende (10kOhm) pruefen
Problem: Servo zuckert/Arduino resettet -> Separate Stromversorgung + Kondensator (1000uF) verwenden
Problem: Servo bewegt sich nicht -> anglefrom/angleto pruefen
Problem: **Kerzen leuchten nicht** -> **Stromversorgung der Kerzen pruefen**

---

## Erweiterungsmoeglichkeiten

### Spezifisch fuer elektrische Kerzen:
- **Fernsteuerung fuer Kerzen:** Kerzen zusammen mit Glocke steuern
- **Lichtsensor:** Automatische Aktivierung bei Dämmerung
- **Zeitschaltuhr:** Automatisches Einschalten der Kerzen zu bestimmter Zeit

Fortgeschritten:
- Externes RTC-Modul (praezise Zeitmessung)
- OLED-Display (numerischer Countdown)
- RFID/Taster am Tuerrahmen (automatischer Start)
- Funkfernbedienung (433MHz)
- Mehrere Glocken (Stereo-Klang)
- Bluetooth (Smartphone-Steuerung)
- Sprachausgabe ("Das Christkind kommt!")

Einfach:
- Kuerzere Draehte
- Kleineres Gehaeuse
- Andere Glocke
- Mehr LEDs
- Lautstaerkere Glocke

---

## Tradition & Brauchtum

Warum mechanische Glocke?
- Authentischer Klang (keine elektronischen Toene)
- Tradition (echte Glocken seit Jahrhunderten)
- Magie (Kinder glauben eher an Christkind)
- Ritual (Klang signalisiert Bescherungsbeginn)

**Angepasst fuer elektrische Kerzen:**
- Kein Feuerrisiko -> Eltern koennen entspannter sein
- Kein Zeitdruck beim Verlassen des Raums
- Wiederholbares Experimentieren mit Timing
- Wetterunabhaengig (auch bei geschlossenem Fenster moeglich)

Tipps fuer Inszenierung:
1. **Kerzen testen** – Vorher prüfen, dass alle elektrischen Kerzen funktionieren
2. **Stromversorgung prüfen** – Batterien frisch? Netzteil ausreichend?
3. **Klang testen** – Vorher prüfen, ob die Glocke im ganzen Haus hoerbar ist
4. **Timing ueben** – Eltern sollten den Countdown vorher testen
5. **Kinder vorbereiten** – Ihnen erklären, dass sie auf die Glocke warten sollen

---

## Dateien im Repository

- buttons.ino - Arduino-Sketch
- weihnachtsglocke.fzz - Fritzing-Projekt
- weihnachtsglocke_Schaltplan.png - Schaltplan Bild
- weihnachtsglocke_Schaltplan.svg - Schaltplan Vektor
- PROJEKT.md - Diese Beschreibung
- LIZENZ - MIT-Lizenz
- .gitignore - Ignorierliste

---

## Lizenz

MIT-Lizenz (siehe LIZENZ Datei)

---

Letzte Aktualisierung: 25. Oktober 2025
Erstellt aus: buttons.ino und weihnachtsglocke.fzz
Anwendungsfall: Traditionelle Christkind-Klingel fuer Heiligabend mit ELEKTRISCHEN KERZEN

---

Frohe Weihnachten! 🎄🔔

"Wenn die Glocke laeutet, kommt das Christkind!"
=> Jetzt koennen die Kinder reinkommen und die Bescherung beginnt!

---

Hinweis: In einigen Regionen wird auch eine Schelle oder ein Gloeckchen verwendet. 
Die Mechanik bleibt die gleiche.
