# Todos

Was nur du selbst tun kannst: Konto, Zahlung, Freigabe, Hardware in der Hand. Was ein Chat selbst kann, gehört nicht
hierher. Form (Stilvorlage dieser Datei):

- offen: `- [ ] TD-<n> - **Was:** Befehl oder Link – warum. *(Chat)*`
- erledigt: `- [x] TD-<n> - **Was:** was daraus wurde (Commit). [2026-11-01]` – ein verworfenes sagt es

Jeder Punkt hat Kästchen und Kennung, offen wie erledigt. Die Kennung gilt nur in dieser Datei, wird hochgezählt und nie
wieder vergeben, auch für erledigte nicht; wer eine Zeile einträgt, nimmt die nächste und zählt sie hier hoch. Vor
jeder Änderung die Datei frisch lesen und nur eigene Zeilen ändern (außer Kennung und Form). Erledigt: sofort abhaken,
Datum ans Ende, nach „## Erledigt“ am Ende verschieben, neueste zuerst – der Chat, der es erfährt, nicht nur der, der
die Zeile schrieb. Keine Zeile wird gelöscht. Überschriften gruppieren offene Todos; ist unter einer keines mehr offen,
gehen Überschrift und Text, bis das nächste dazukommt.

Nächste Kennung: TD-8

## Für dich

- [ ] TD-1 - **ESP32-Firmware auf einem T-Display ausprobieren:**
  `cd variants/esp32/firmware && pio run -e tdisplay -t upload`, dann Hotspot `Glocke-XXXX` (WLAN-Analyse-App: Kanal
  1–13, WPA2), Einrichtung, <http://glocke.local> und Display prüfen, Aufdruck „T-DISPLAY V1.1“ ansehen; Tasten, LEDs
  und Servo erst auf der Platine. Warum: bisher nur übersetzt und am Rechner getestet. *(automatic-christmas-bell-41)*
- [ ] TD-2 - **Nano-Firmware ausprobieren:** `pio run -e nano -t upload` im Repo; nach dem Läuten fährt das Servo in
  die Ruhestellung und ist 1 s später abgeschaltet. Warum: bisher nur übersetzt. *(automatic-christmas-bell-41)*
- [ ] TD-4 - **Platinen bestellen:** vorher das edakit-Plugin aktualisieren (Zeile in edakit/TODO.md) – mit dem
  installierten 868e942 bricht `edakit cart prepare` an M-6 (regulatorische Prüfung) ab. Dann in Chrome bei JLCPCB
  anmelden, in einem Profil ohne gespeicherte Karte, und in Claude Code im Repo „bestell die Platinen“ sagen: der
  Skill cart füllt das Formular je Platine und hält am Warenkorb. Bei JLCPCB M-2 (Prüfung vor dem Bezahlen:
  Bestückungsvorschau, Stückliste ohne Lücken, Preis) ansehen, dann bezahlen. Warum: alle fünf Platinen sind
  freigegeben, ihre Bestellaufträge lassen sich mit neuerem edakit erzeugen (geprüft am 1.11.).
  *(automatic-christmas-bell-b3, automatic-christmas-bell-41, automatic-christmas-bell-fe)*

## Erledigt

- [x] TD-7 - **edakit-Plugin auf 0.4.14 gehoben:** user- und Projekt-Eintrag 0.4.14, Bridge-Erweiterung 1.6.0 =
  Server 1.6.0 (edakit doctor); der Klon über SSH ging nicht (kein GitHub-Schlüssel) – git leitet
  `git@github.com:tgd1975/` jetzt auf HTTPS um. [2026-11-01]
- [x] TD-6 - **Vier Warnungen DOCS.derived akzeptiert** (R-1, R-3, R-4, R-12, Grund D-39) auf main, smd und esp32 –
  alle drei RELEASED (D-41, 1fa3ba8). [2026-11-01]
- [x] TD-5 - **Blanke Stellen im GND-Kupfer schließen:** ja – main, smd und esp32 mit Stitching-Vias gefüllt, M-5 neu
  (D-41, 67f0b44). [2026-11-01]
- [x] TD-3 - **T-Display vermessen, bevor die ESP32-Platine bestellt wird:** verworfen – D-37: CE-Zeichen vorhanden,
  kein Vermessen; das Footprint bleibt bei LILYGOs Zeichnungen (D-13) (bdc3678). [2026-11-01]
