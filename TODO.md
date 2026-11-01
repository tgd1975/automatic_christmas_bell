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

Nächste Kennung: TD-7

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
- [ ] TD-6 - **Vier Warnungen DOCS.derived (Anforderung nennt, wer sie aufgestellt hat) akzeptieren:** R-1, R-3, R-4
  und R-12 nennen Entwurfsdaten statt einer Person oder Entscheidung – bis der Anforderungsvorschlag nach der
  Bestellung die Dateien ersetzt (D-39). Warum: ohne Akzeptanz bleiben main, smd und esp32 nach D-41 NOT RELEASED, und
  TD-4 kann nicht bestellen. *(Chat Kupferflächen)*

## Erledigt

- [x] TD-5 - **Blanke Stellen im GND-Kupfer schließen:** ja – main, smd und esp32 mit Stitching-Vias gefüllt, M-5 neu
  (D-41). [2026-11-01]
- [x] TD-3 - **T-Display vermessen, bevor die ESP32-Platine bestellt wird:** verworfen – D-37: CE-Zeichen vorhanden,
  kein Vermessen; das Footprint bleibt bei LILYGOs Zeichnungen (D-13) (bdc3678). [2026-11-01]
