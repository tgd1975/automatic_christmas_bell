# Todos

Was nur du selbst tun kannst: Konto, Zahlung, Freigabe, Hardware in der Hand. Was ein Chat selbst kann, gehört nicht
hierher. Eine Zeile je Todo: `- [ ] TD-<n> **Was:** Befehl oder Link – warum. *(Chat)*`. Die Kennung gilt nur in
dieser Datei, wird hochgezählt und nie wieder vergeben, auch nicht nach dem Löschen; wer eine Zeile einträgt, nimmt
die nächste und zählt sie hier hoch. Vor jeder Änderung die Datei frisch lesen und nur eigene Zeilen ändern; erledigt
sofort abhaken (`- [x]`), der Chat, der die Zeile eingetragen hat, löscht abgehakte Zeilen beim nächsten Lesen.

Nächste Kennung: TD-5

## Für dich

- [ ] TD-1 **ESP32-Firmware auf einem T-Display ausprobieren:**
  `cd variants/esp32/firmware && pio run -e tdisplay -t upload`, dann Hotspot `Glocke-XXXX` (WLAN-Analyse-App: Kanal
  1–13, WPA2), Einrichtung, <http://glocke.local> und Display prüfen, Aufdruck „T-DISPLAY V1.1“ ansehen; Tasten, LEDs
  und Servo erst auf der Platine. Warum: bisher nur übersetzt und am Rechner getestet. *(automatic-christmas-bell-41)*
- [ ] TD-2 **Nano-Firmware ausprobieren:** `pio run -e nano -t upload` im Repo; nach dem Läuten fährt das Servo in die
  Ruhestellung und ist 1 s später abgeschaltet. Warum: bisher nur übersetzt. *(automatic-christmas-bell-41)*
- [x] TD-3 **T-Display vermessen, bevor die ESP32-Platine bestellt wird:** Reihenabstand 22,86 mm, Raster 2,54 mm.
  Warum: das Footprint beruht auf LILYGOs Zeichnungen (D-13). *(automatic-christmas-bell-41)*
- [ ] TD-4 **Bestellen mit dem Skill cart:** in Claude Code im Repo „bestell die Platinen“ – füllt JLCPCBs Formular je
  Board aus den Schlüsseln (Remove Mark, Österreich, DHL Express) und hält am Warenkorb; Vorschau ansehen (M-2), bei
  esp32tht (ESP32 THT) besonders: sie hat keinen `JLCJLCJLCJLC`-Platzhalter, eine Bestellnummer stünde sichtbar oben.
  Bezahlen machst du. Die Fertigungsdateien liegen nicht im Repo (D-22); läuft eine Platine:
  `make publish-built TAG=<tag>`. Ersetzt die alte Zeile mit `make publish` und „Specify Position“, das es bei JLCPCB
  nicht mehr gibt. Braucht das aktuelle edakit-Plugin (Todo in edakit/TODO.md). *(automatic-christmas-bell-b3,
  automatic-christmas-bell-41, automatic-christmas-bell-fe)*
