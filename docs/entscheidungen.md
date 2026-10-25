# Entscheidungen Platine

Nummeriert, mit Grund und Datum. Quelle der Schaltung: `weihnachtsglocke.fzz`; der Graph `hardware/graph.json` gibt
sie 1:1 wieder, Bauteilnamen wie in Fritzing (Bauteil1 = U1, Servo = J1).

## E-1 Bestückung: JLCPCB setzt nur die SMD-Teile (25.10.2026, offen bis zum Angebot)

JLCPCB Economic bestückt nur SMD auf einer Seite. Daher bestückt JLCPCB R1–R7 (0805) und S1/S2 (SMD-Taster). Von Hand
gelötet werden die beiden Buchsenleisten für den Nano, die fünf 5-mm-LEDs, C1 und die Servo-Stiftleiste (im Graphen
`"bom": false`). Die Alternative ist alles in THT und nur die leere Platine zu bestellen. Entschieden wird nach dem
Preis im JLCPCB-Angebot.

## E-2 Taster als SMD 6 × 6 mm (25.10.2026, Vorschlag)

C127509 (K2-1102SP) statt der THT-Taster aus Fritzing: JLCPCB kann ihn bestücken, und er ist in pytree schon geprüft.

## E-3 Versorgung über USB, Servo am 5V-Pin des Nano (25.10.2026)

Alles wird über die USB-Buchse des Nano versorgt; dessen 5V-Pin speist das Servo. Die Simulation zeigt für die
schwingende Glocke (0,3 A angenommen) 325 mA aus USB, das ist in Ordnung. Ein blockiertes Servo (0,7 A angenommen) zöge
725 mA. Dann löst die Polyfuse des Nano (500 mA) aus, und der Nano startet neu. Das ist ein Fehlerfall, kein
Betriebsfall: Das Szenario `servo-blockiert` läuft nur als Information.

## E-4 Taster schalten 5 V statt 3,3 V (25.10.2026)

In Fritzing hingen S1/S2 am 3V3-Pin. Dagegen sprechen zwei Gründe:

- **Pegel:** Der ATmega328P erkennt High erst ab 0,6 × VCC. Bei USB-Versorgung sind das bis zu 3,03 V, und 3,3 V liegen
  nur 0,28 V darüber. Störungen auf den Tasterleitungen oder eine etwas niedrigere 3,3-V-Spannung reichen dann für
  einen unsicheren Pegel. An 5 V beträgt der Abstand 1,7 V oder mehr.
- **Quelle:** Der 3V3-Pin kommt beim Original aus dem FT232RL, bei den üblichen Nachbauten aus dem V3-Pin des CH340.
  Der ist laut Datenblatt nur zum Abblocken gedacht, nicht als Ausgang für andere Lasten. 5 V dagegen ist die
  Versorgung selbst.

Die Taster hängen jetzt an +5V, und der 3V3-Pin bleibt frei.

## E-5 C1 mit 16 V statt 35 V (25.10.2026)

Am Elko liegen höchstens 5,5 V. 16 V reichen mit Faktor 2,9, und das Gehäuse ist kleiner (Ø10 × 13 mm statt
Ø13 × 25 mm). C439782, 18 720 Stück bei LCSC.

## E-6 Servo-Stiftleiste C2937625 statt C492402 (25.10.2026)

Gleiche Leiste (XFCN PZ254V-11-03P), aber C492402 hat 0 Stück am Lager, C2937625 hat 659 300.
