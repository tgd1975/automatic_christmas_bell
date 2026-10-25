# 🎄 Weihnachtsglocke - Christkind-Klingel

**Automatische mechanische Glocke für den Christkind-Brauch an Heiligabend.**

---

## 🎯 Anwendung

An Heiligabend:
1. Eltern bereiten Geschenke am Weihnachtsbaum vor
2. Elektrische Kerzen einschalten
3. **Start-Taster drücken** → Countdown beginnt (LEDs zeigen verbleibende Zeit)
4. Eltern verlassen den Raum
5. **Nach 65 Sekunden läutet die Glocke mechanisch**
6. Kinder stürmen herein → Bescherung beginnt! 🎅✨

> ⚠️ **Wichtig:** Die Glocke wird **mechanisch angeschlagen** (kein elektronischer Ton!).

---

## 📍 Positionierung

- **Intended Position:** Buchregal oder ähnlicher erhöhter Ort
- **Servo-Arm hängt nach UNTEN**, Glocke hängt UNTEN dran
- **Weiter hinten platzieren** – Kinder sind auf den Baum fokussiert

---

## 📁 Struktur

```
automatic_christmas_bell/
├── README.md              # Anwendung (dieses Dokument)
├── buttons.ino             # Arduino-Sketch
├── weihnachtsglocke.fzz   # Fritzing-Projekt
├── weihnachtsglocke_Schaltplan.png
├── weihnachtsglocke_Schaltplan.svg
└── docs/
    └── IMPLEMENTIERUNG.md   # Detaillierte Umsetzung
```

---

## 🔧 Hardware (Übersicht)

- **Arduino Nano** – Mikrocontroller
- **Servo 9g** – Betätigt die Glocke mechanisch
- **5 LEDs** – Visueller Countdown (2× Grün, 2× Gelb, 1× Rot)
- **2 Taster** – Start und Reset
- **Echte Glocke** – Wird vom Servo angeschlagen

---

## ⚡ Schnellstart

### 1. Position wählen
- Im Buchregal oben befestigen
- Servo mit nach unten hängendem Arm an Glocke anbringen

### 2. Hardware aufbauen
- Fritzing-Schaltplan (`weihnachtsglocke_Schaltplan.png`) verwenden
- Stromversorgung: Arduino per USB, Servo separat (5V, 1A)

### 3. Software hochladen
```bash
# Arduino IDE öffnen
# buttons.ino öffnen und auf Arduino Nano hochladen
```

### 4. Testen
- Start-Taster drücken → Countdown beginnt
- Nach 65 Sekunden läutet die Glocke
- Reset-Taster zum Zurücksetzen

---

## 📖 Detaillierte Dokumentation

Die komplette Implementierung (Schaltplan, Code-Erklärung, Mechanik, Anpassungen) findest du in:
→ **[docs/IMPLEMENTIERUNG.md](docs/IMPLEMENTIERUNG.md)**

---

## 📜 Lizenz

[MIT Lizenz](LIZENZ) – Freie Nutzung, Modifikation und Verteilung.

---

**Frohe Weihnachten! 🎄🔔**

> *"Wenn die Glocke läutet, kommt das Christkind!"*
