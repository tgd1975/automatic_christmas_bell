# Todos

Was nur du selbst tun kannst: Konto, Zahlung, Freigabe, Hardware in der Hand. Was ein Chat selbst kann, gehört nicht
hierher. Eine Zeile je Todo: `- [ ] TD-<n> **Was:** Befehl oder Link – warum. *(Chat)*`. Die Kennung gilt nur in
dieser Datei, wird hochgezählt und nie wieder vergeben, auch für erledigte nicht; wer eine Zeile einträgt, nimmt die
nächste und zählt sie hier hoch. Vor jeder Änderung die Datei frisch lesen und nur eigene Zeilen ändern. Erledigt: sofort
mit Datum abhaken (`- [x] 2026-11-01 TD-<n> …`, ein verworfenes sagt es) und nach „## Erledigt“ am Ende verschieben,
neueste zuerst – der Chat, der es erfährt, nicht nur der, der die Zeile schrieb. Keine Zeile wird gelöscht.

Nächste Kennung: TD-5

## Für dich

- [ ] TD-1 **ESP32-Firmware auf einem T-Display ausprobieren:**
  `cd variants/esp32/firmware && pio run -e tdisplay -t upload`, dann Hotspot `Glocke-XXXX` (WLAN-Analyse-App: Kanal
  1–13, WPA2), Einrichtung, <http://glocke.local> und Display prüfen, Aufdruck „T-DISPLAY V1.1“ ansehen; Tasten, LEDs
  und Servo erst auf der Platine. Warum: bisher nur übersetzt und am Rechner getestet. *(automatic-christmas-bell-41)*
- [ ] TD-2 **Nano-Firmware ausprobieren:** `pio run -e nano -t upload` im Repo; nach dem Läuten fährt das Servo in die
  Ruhestellung und ist 1 s später abgeschaltet. Warum: bisher nur übersetzt. *(automatic-christmas-bell-41)*
- [ ] TD-4 **Platinen bestellen:** vorher das edakit-Plugin aktualisieren (Zeile in edakit/TODO.md) – mit dem
  installierten 868e942 bricht `edakit cart prepare` an M-6 (regulatorische Prüfung) ab. Dann in Chrome bei JLCPCB
  anmelden, in einem Profil ohne gespeicherte Karte, und in Claude Code im Repo „bestell die Platinen“ sagen: der
  Skill cart füllt das Formular je Platine und hält am Warenkorb. Bei JLCPCB M-2 (Prüfung vor dem Bezahlen:
  Bestückungsvorschau, Stückliste ohne Lücken, Preis) ansehen, dann bezahlen. Warum: alle fünf Platinen sind
  freigegeben, ihre Bestellaufträge lassen sich mit neuerem edakit erzeugen (geprüft am 1.11.).
  *(automatic-christmas-bell-b3, automatic-christmas-bell-41, automatic-christmas-bell-fe)*

## Erledigt

- [x] 2026-11-01 TD-3 **T-Display vermessen, bevor die ESP32-Platine bestellt wird:** verworfen – D-37 (CE-Zeichen
  vorhanden, kein Vermessen). Reihenabstand 22,86 mm, Raster 2,54 mm. Warum: das Footprint beruht auf LILYGOs
  Zeichnungen (D-13). *(automatic-christmas-bell-41)*
