# 🎄 Weihnachtsglocke - Christkind-Klingel

Automatische mechanische Weihnachtsglocke für den traditionellen **Christkind-Brauch** an Heiligabend. Die Schaltung läuft einen Countdown ab und läutet dann eine **echte Glocke** mechanisch an, um den Kindern zu signalisieren, dass sie hereinkommen dürfen.

---

## 📌 Was es macht

An Heiligabend (mit **elektrischen Kerzen**):
1. Eltern bereiten Geschenke am Weihnachtsbaum vor
2. **Elektrische Kerzen EINSCHALTEN**
3. **Start-Taster drücken** → Countdown (60s) beginnt, LEDs zeigen die verbleibende Zeit
4. Eltern verlassen den Raum
5. **Nach 65 Sekunden läutet die Glocke automatisch**
6. Kinder stürmen herein → Bescherung beginnt! 🎅✨

> ⚠️ **Wichtig:** Die Glocke wird **mechanisch angeschlagen** (kein elektronischer Ton!) für authentischen Klang. **Elektrische Kerzen** bleiben während des gesamten Ablaufs eingeschaltet.

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
- **Elektrische Kerzen** – Werden vor dem Start eingeschaltet

---

## ⚡ Schnellstart

### 1. Hardware aufbauen
- Fritzing-Schaltplan (`weihnachtsglocke_Schaltplan.png`) verwenden
- Servo mit Hebelarm an Glocke anbringen
- Stromversorgung: Arduino per USB, Servo separat (5V, 1A)

### 2. Elektrische Kerzen vorbereiten
- Kerzen am Baum anbringen und **testen**
- Stromversorgung für Kerzen prüfen (Batterien/Netzteil)

### 3. Software hochladen
```bash
# Arduino IDE öffnen
# buttons.ino öffnen und auf Arduino Nano hochladen
```

### 4. Ablauf am Heiligabend
1. Geschenke unter den Baum legen
2. **Elektrische Kerzen EINSCHALTEN** → Baum leuchtet
3. **Start-Taster drücken** → Countdown beginnt
4. Raum verlassen
5. **Glocke läutet nach 65 Sekunden**
6. Kinder kommen rein → Bescherung! 🎄

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

✅ **Kerzen testen** – Vorher prüfen, dass alle elektrischen Kerzen funktionieren
✅ **Stromversorgung prüfen** – Batterien frisch? Netzteil ausreichend?
✅ **Klang testen** – Vorher prüfen, ob die Glocke im ganzen Haus hörbar ist
✅ **Timing üben** – Eltern sollten den Countdown vorher testen
✅ **Kinder vorbereiten** – Ihnen erklären, dass sie auf die Glocke warten sollen

---

## 📜 Lizenz

[MIT Lizenz](LIZENZ) – Freie Nutzung, Modifikation und Verteilung.

---

**Frohe Weihnachten! 🎄🔔**

> *"Wenn die Glocke läutet, kommt das Christkind!"*
