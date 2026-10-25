# 🎄 Weihnachtsglocke - Christkind-Klingel

Automatische mechanische Weihnachtsglocke für den traditionellen **Christkind-Brauch** an Heiligabend. Die Schaltung läuft einen Countdown ab und läutet dann eine **echte Glocke** mechanisch an, um den Kindern zu signalisieren, dass sie hereinkommen dürfen.

---

## 📌 Was es macht

An Heiligabend:
1. Eltern bereiten Geschenke und Kerzen am Weihnachtsbaum vor
2. **Start-Taster drücken** → Countdown (60s) beginnt, LEDs zeigen die verbleibende Zeit
3. Eltern verlassen kurz den Raum (wegen der Kerzen)
4. **Nach 65 Sekunden läutet die Glocke automatisch**
5. Kinder stürmen herein → Bescherung beginnt! 🎅✨

> ⚠️ **Wichtig:** Die Glocke wird **mechanisch angeschlagen** (kein elektronischer Ton!) für authentischen Klang.

---

## 📁 Dateien

| Datei | Beschreibung |
|-------|--------------|
| `buttons.ino` | Arduino-Sketch (Hauptprogramm) |
| `weihnachtsglocke.fzz` | Fritzing-Projektdatei |
| `weihnachtsglocke_Schaltplan.png` | Schaltplan (Bild) |
| `weihnachtsglocke_Schaltplan.svg` | Schaltplan (Vektor) |
| `PROJEKT.md` | Detaillierte Projektbeschreibung |
| `LIZENZ` | MIT-Lizenz |

---

## 🔧 Hardware

- **Arduino Nano** – Mikrocontroller
- **Servo 9g** – Betätigt die Glocke mechanisch
- **5 LEDs** – Visueller Countdown (2× Grün, 2× Gelb, 1× Rot)
- **2 Taster** – Start und Reset
- **Widerstände** – Für LEDs und Taster
- **Echte Glocke** – Wird vom Servo angeschlagen

---

## ⚡ Schnellstart

### 1. Hardware aufbauen
- Fritzing-Schaltplan (`weihnachtsglocke_Schaltplan.png`) verwenden
- Servo mit Hebelarm an Glocke anbringen
- Stromversorgung: Arduino per USB, Servo separat (5V, 1A)

### 2. Software hochladen
```bash
# Arduino IDE öffnen
# buttons.ino öffnen und auf Arduino Nano hochladen
```

### 3. Testen
- Start-Taster drücken → Countdown beginnt
- Nach 65 Sekunden läutet die Glocke
- Reset-Taster zum Zurücksetzen

---

## 🛠️ Anpassungen

In `buttons.ino`:

```cpp
// Kürzerer Countdown (30-45s empfohlen für Christkind-Szenario)
const long countdowntime = 30;

// Lauteres Läuten
const long bellswings = 10;      // Mehr Schwingungen
const int anglefrom = 45;        // Größerer Winkelbereich
const int angleto = 135;

// Schnellere Warnung
const long finalwarningtime = 8;
const long blinkrate = 300;
```

---

## 📐 Mechanik

### Servo-Glocken-Mechanismus

**Option 1: Direkter Anschlag**
```
Servo-Horn → Holzarm (5-10 cm) → Gummikopf → Glocke
```

**Option 2: Hebelübersetzung** (für mehr Kraft)
```
Servo (kurzer Arm) → Hebel → Glocke (langer Arm mit Klöppel)
```

**Option 3: Seilzug** (für entfernte Glocke)
```
Servo → Nylonfaden → Klöppel
```

---

## 🎯 Tipps für Heiligabend

✅ **Glocke verstecken** – Nicht zu offensichtlich platzieren
✅ **Klang testen** – Vorher prüfen, ob die Glocke im ganzen Haus hörbar ist
✅ **Timing üben** – Eltern sollten den Countdown vorher testen
✅ **Kerzen ausblasen** – Vor dem Verlassen des Raums!
✅ **Kinder vorbereiten** – Ihnen erklären, dass sie auf die Glocke warten sollen

---

## 📜 Lizenz

[MIT Lizenz](LIZENZ) – Freie Nutzung, Modifikation und Verteilung.

---

**Frohe Weihnachten! 🎄🔔**

> *"Wenn die Glocke läutet, kommt das Christkind!"*
