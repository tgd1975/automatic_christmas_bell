# Board decisions

Numbered, with reason and date. Source of the circuit: `weihnachtsglocke.fzz`. The hardware graph
`hardware/graph.json` reproduces it 1:1, with the Fritzing designators (Bauteil1 = U1, Servo = J1).

## D-1 Assembly: JLCPCB places only the SMD parts (2026-10-25, open until the quote)

JLCPCB's Economic assembly places SMD parts on one side only. It places R1–R7 (0805) and S1/S2 (SMD buttons). The two
female headers for the Nano, the five 5 mm LEDs, C1 and the servo header are hand-soldered (`"bom": false` in the
graph). The alternative: everything THT and a bare board. Decided by the price in the JLCPCB quote.

## D-2 SMD buttons 6 × 6 mm (2026-10-25)

C127509 (K2-1102SP) instead of the THT buttons of the Fritzing drawing: JLCPCB can place it, and its entry was already
verified in another project.

## D-3 USB power, servo at the Nano's 5V pin (2026-10-25)

Everything runs from the Nano's USB socket; its 5V pin supplies the servo. The simulation gives 325 mA from USB while
the bell swings (0.3 A assumed) – fine. A stalled servo (0.7 A assumed) would draw 725 mA: the Nano's polyfuse
(500 mA) trips and the Nano resets. That is a fault case, not an operating state, so the scenario `servo-stalled` runs
as information only.

## D-4 Buttons switch 5 V instead of 3.3 V (2026-10-25)

In the Fritzing drawing S1/S2 were connected to the 3V3 pin. Two reasons against it:

- **Level:** the ATmega328P reads high from 0.6 × VCC, up to 3.03 V on USB power. 3.3 V is only 0.28 V above that; a
  little noise on the button wires or a slightly low 3.3 V makes the level uncertain. At 5 V the margin is 1.7 V or
  more.
- **Source:** the 3V3 pin comes from the FT232RL on the original Nano and from the CH340's V3 pin on the usual clones.
  The CH340 datasheet means that pin for a decoupling capacitor, not as an output for other loads. 5 V is the supply
  itself.

The buttons now switch +5V; the 3V3 pin stays free.

## D-5 C1 rated 16 V instead of 35 V (2026-10-25)

C1 sees at most 5.5 V. 16 V gives a factor of 2.9, and the can is smaller (Ø10 × 13 mm instead of Ø13 × 25 mm).
C439782, 18 720 pcs at LCSC.

## D-6 Servo header C2937625 instead of C492402 (2026-10-25)

The same header (XFCN PZ254V-11-03P), but C492402 has 0 pcs in stock, C2937625 has 659 300.
