# Kostenvergleich der Hersteller – Stand 1. November 2026

Was die fünf Platinen bei JLCPCB, Eurocircuits, AISLER und PCBWay kosten: je 5 Stück, die unbestückten THT-Platinen
(tht, esp32tht) und die bestückten SMD-Platinen (main, smd, esp32) samt den Teilen, die von Hand gelötet werden.
Die Preise wurden am 1.11.2026 zwischen 19:15 und 20:00 Uhr in den Angebotsformularen der Hersteller abgelesen, mit
den Fertigungsdateien der aktuellen Releases. Nichts wurde in einen Warenkorb gelegt oder bestellt.

Umrechnung: 1 USD = 0,8951 € (EZB-Referenzkurs 30.10.2026, `[cost] rates`). „Netto“ heißt ohne Umsatzsteuer, für
Österreich kommen 20 % dazu.

## Ergebnis

| Platine (5 Stück) | JLCPCB | Eurocircuits | AISLER | PCBWay |
|---|---|---|---|---|
| tht, unbestückt | **4,65 €** (5,20 USD) | 82,60 € | 33,07 € (6 Stück) | nicht abgefragt |
| esp32tht, unbestückt | **4,65 €** (5,20 USD) | wie tht (nicht einzeln abgefragt) | wie tht (nicht einzeln abgefragt) | nicht abgefragt |
| main, bestückt | **21,74 €** (24,29 USD) | 234,55 € **ohne Bauteile** | nicht abgefragt | nicht abgefragt |
| smd, bestückt | **31,66 €** (35,37 USD) | 295,05 € **ohne Bauteile** | 393,14 € ohne die Taster | nicht abgefragt |
| esp32, bestückt | **34,58 €** (38,63 USD) | nicht abgefragt | nicht abgefragt | nicht abgefragt |

Alle Beträge netto, ohne Versand.

**JLCPCB ist bei jeder Platine um den Faktor 7 bis 18 günstiger.** Die europäischen Hersteller scheitern schon an der
Stückliste: Sie ist auf LCSC/JLCPCB zugeschnitten (KENTO-LEDs, Honor-Elko, hanxia-Stiftleiste, Hroparts-Taster).
Eurocircuits findet für keines dieser Teile einen Preis, AISLER bekommt die Taster nicht, und beide verlangen für die
Bestückung allein ein Vielfaches des gesamten JLCPCB-Preises. Ein Wechsel zu einem europäischen Hersteller wäre nur mit
einer anderen Stückliste sinnvoll, und auch dann bliebe die Bestückung deutlich teurer.

## Gesamtkosten bei JLCPCB, Handlötteile eingeschlossen

Pro Platine, 5 Stück, Handlötteile von LCSC mit deren Mindestmengen:

| Platine | Platinen (JLCPCB) | Handlötteile (LCSC) | Summe netto | mit 20 % USt |
|---|---|---|---|---|
| tht | 4,65 € | 6,41 € (alle 19 Teile + 2 Buchsenleisten je Satz) | 11,06 € | 13,28 € |
| esp32tht | 4,65 € | 7,79 € (alle 19 Teile + 2 Buchsenleisten je Satz) | 12,44 € | 14,93 € |
| main | 21,74 € | 4,31 € (C1, J1, 5 LEDs, Buchsenleisten) | 26,05 € | 31,26 € |
| smd | 31,66 € | 0,81 € (nur die Buchsenleisten) | 32,47 € | 38,97 € |
| esp32 | 34,58 € | 1,59 € (nur die Buchsenleisten) | 36,17 € | 43,41 € |

Dazu kommt **einmal pro Bestellung** der Versand, egal wie viele Platinen im Warenkorb liegen (Österreich, laut
Angebotsformular):

| Versandart | 0,20 kg | 0,28 kg | Lieferzeit |
|---|---|---|---|
| DHL Express | 20,98 € (23,44 USD) | 20,98 € (23,44 USD) | 2–4 Werktage |
| EuroPacket | 11,79 € (13,17 USD) | 12,93 € (14,45 USD) | 5–8 Werktage |
| Global Standard Direct Line | 6,27 € (7,00 USD) | 7,27 € (8,12 USD) | 10–12 Werktage |

Die bestückten Platinen wiegen laut JLCPCB 0,41–0,44 kg je 5 Stück. Den Versand für dieses Gewicht zeigt JLCPCB erst
im Warenkorb; DHL Express kostete bis 0,28 kg gleich viel. Für LCSC kommt ein eigener Versand dazu, der nicht
abgefragt wurde.

Die Module (Arduino Nano, LILYGO T-Display) sind nirgends eingerechnet.

## Die Hersteller im Einzelnen

### JLCPCB

Formular cart.jlcpcb.com/quote, angemeldet, Einstellungen aus `order.json` des Releases: 1,6 mm, grün/weiß,
LeadFree HASL, „Remove Mark“; bestückt: Economic, Oberseite, 5 Stück, „Tooling holes: Added by Customer“,
„Confirm Parts Placement: Yes“.

| | PCB | Setup | Schablone | Bauteile | Extended-Zuschlag | SMT | Stickstoff | Teile prüfen | Summe |
|---|---|---|---|---|---|---|---|---|---|
| tht, esp32tht | 5,20 | – | – | – | – | – | – | – | 5,20 USD |
| main | 5,20 | 8,24 | 1,55 | 1,51 (4 Pos.) | 6,18 (2 Teile) | 0,25 | 0,91 | 0,45¹ | 24,29 USD |
| smd | 5,20 | 8,24 | 1,55 | 3,11 (9 Pos.) | 15,45 (5 Teile) | 0,46 | 0,91 | 0,45¹ | 35,37 USD |
| esp32 | 5,20 | 8,24 | 1,55 | 3,25 (9 Pos.) | 18,54 (6 Teile) | 0,49 | 0,91 | 0,45 | 38,63 USD |

¹ Bei main und smd wurde „Confirm Parts Placement“ im Formular nicht gesetzt; die 0,45 USD aus dem esp32-Angebot
sind dazugerechnet.

- Der Platinenpreis ist der Sonderpreis für 5 Stück bis 100 × 100 mm (4,00 USD) plus 1,20 USD für bleifreies HASL.
- Den größten Posten bei den bestückten Platinen macht der Zuschlag für Extended-Teile aus (3,09 USD je Teileart).
  Die Extended-Teile bei smd: C1, J1, LED1, R8/R9, S1/S2; bei esp32 zusätzlich die gelbgrünen LEDs LED4/LED5 (C2292).
  smd kostet deshalb 3,26 USD weniger als esp32.
- Alle Teile wurden zugeordnet, keines fehlte.
- JLCPCB legt für jede bestückte Platine einen gespeicherten Entwurf an („Automatically saved“), im Warenkorb liegt
  nichts.

### Eurocircuits (Belgien)

Konfigurator be.eurocircuits.com, angemeldet; hochgeladen wurden die Gerber, die Stückliste mit Herstellernummern
(`bom_<b>_mpn.csv`) und die auf Eurocircuits gedrehte Bestückungsdatei. Eurocircuits wählt den Dienst selbst
(„PCB proto“); der STANDARD pool ließ sich nicht wählen. Die Brettdicke beträgt 1,55 statt 1,6 mm (Eurocircuits bietet
1,6 nicht an).

| | Platinen | Bestückung | Bauteile | Summe netto | brutto (20 %) | Lieferzeit |
|---|---|---|---|---|---|---|
| tht | 82,60 € | – | – | 82,60 € | 99,12 € | 3 Arbeitstage |
| main | 82,60 € | 151,95 € | **kein Preis** (4 von 4 Positionen) | 234,55 € + Bauteile | 281,46 € + Bauteile | 6 Arbeitstage |
| smd | 82,60 € | 212,45 € (unvollständig) | **kein Preis** (8 Positionen ohne Preis, LED1 KT-0805R nicht erkannt) | 295,05 € + Bauteile | 354,06 € + Bauteile | 6 Arbeitstage |

Die Tabelle „Alternatives“ nennt für 5 Stück in 2 Arbeitstagen 192,95 € netto. Den Versand zeigt Eurocircuits erst im
Warenkorb („Express transport –“).

### AISLER (Niederlande/Deutschland)

aisler.net, angemeldet; zwei Projekte in der Sandbox: `gerber_tht` (Gerber, unbestückt) und `odb_smd` (ODB++,
bestückt). Konfiguration: 1,6 mm, HASL Lead Free, 35 µm, grün/weiß.

- **tht unbestückt („Beautiful Boards“):** AISLER fertigt in Dreierschritten, 5 wird auf 6 aufgerundet:
  **33,07 € netto** für 6 Stück (3 Stück: 23,53 €). Versand ab 13.11.2026.
- **smd bestückt („Amazing Assembly“), 5 Stück: 393,14 € netto**, davon Bauteile 179,92 €. Versand ab 25.11.2026.
  - AISLER erkannte über „Auto detect MPN“ 8 Positionen (J1, LEDs, Taster); C1 und die Widerstände wurden von Hand
    über die Herstellernummer des Releases zugeordnet (UNI-ROYAL heißt dort ROYALOHM); U1 (Nano) ist ausgeschlossen.
  - Die Taster **S1/S2 (K2-1102SP-C4SC-04) sind bei AISLER nicht lieferbar**. Für einen Preis stehen sie auf
    „You supply it“: sie müssten zugeschickt werden und sind im Preis nicht enthalten.
  - Die Bauteile kosten so viel, weil AISLER ganze Verpackungseinheiten kauft: 179,92 € für 5 Sätze, 182,21 € für
    10 Sätze.
- Die Auswahl „Auto assign parts using“ bietet bei EasyEDAs ODB++ keine Spalte „mpn“ an (nur comment, designator,
  device, footprint, value), anders als im edakit-Profil beschrieben.
- Den Versand zeigt AISLER erst nach „Continue to Checkout“. Die Seite rechnet mit 19 % Umsatzsteuer, für Österreich
  wären es 20 %: tht 39,68 €, smd 471,77 € brutto.

### PCBWay

Nicht abgefragt: Claude in Chrome darf pcbway.com nicht öffnen („Navigation to this domain is not allowed“).
Außerdem nennt PCBWay laut edakit-Profil den Bestückungspreis online ohne Bauteile; diese bepreisen erst die Ingenieure
nach der Prüfung der Dateien (1–2 Tage), und die Dateien gehen erst nach der Erklärung „Agree“ im Namen des
Bestellers hoch. Eine vollständige Zahl für die bestückten Platinen gibt es dort also ohnehin nicht sofort.

## Was die Abfrage gekostet hat

Für AISLER und Eurocircuits fehlten im Release die ODB++-Datei und die Stückliste mit Herstellernummern. Sie wurden
mit `edakit fab` neben dem Release erzeugt (`[cart] makers` vorübergehend erweitert und wieder zurückgesetzt).
`edakit fab diff` gegen die Releases zeigt: die Fertigungsdateien sind gleich. Damit das künftig ohne EasyEDA geht,
schlägt D-42 / edakit #153 vor, ODB++ und die MPN-Stückliste in jedes Release zu schreiben.

edakits Schätzung (`edakit cost`) lag bei JLCPCB 3–5 USD über den echten Preisen. Der Grund: Sie rechnet die Platine
mit 10,70 USD statt mit dem Sonderpreis von 4,00 USD + 1,20 USD für bleifreies HASL, und ihr fehlt der
Stickstoff-Zuschlag von 0,91 USD:

| | edakit cost | Angebot | Differenz |
|---|---|---|---|
| tht, esp32tht | 10,70 USD | 5,20 USD | −5,50 |
| main | 27,92 USD | 24,29 USD | −3,63 |
| smd | 38,38 USD | 35,37 USD | −3,01 |
| esp32 | 41,44 USD | 38,63 USD | −2,81 |
