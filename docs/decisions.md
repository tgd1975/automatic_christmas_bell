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

Everything runs from the Nano's USB socket; its 5V pin supplies the servo. The simulation gives about 420 mA from USB while
the bell swings (0.3 A assumed, with the base load of D-8) – within the 500 mA of the Nano's polyfuse. A stalled servo
(0.7 A assumed) would draw about 825 mA. The original Nano's
polyfuse (MF-MSMF050) holds 0.5 A and is only guaranteed to trip at 1.0 A, many clones have none, and the Schottky
diode (MBR0520, 0.5 A average) then carries about 0.83 A – harmless for the few seconds of a bell phase, not as a
permanent state. The scenario `servo-stalled` runs as information only; the firmware may detach the servo once it has
reached its rest position, so a jam there cannot become a permanent overload (M-1 review, note 4).

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

## D-7 Holes for the Nano's female headers (2026-10-25, open)

The gate fails L-9: the Nano footprint from the EasyEDA user library (C9900017879) has 0.90 mm holes. A female header
with the usual 0.64 mm square tail needs 0.91 mm across the diagonal; 1.0 mm is recommended. Options:

1. Another Nano footprint with 1.0 mm holes (EasyEDA has two more in user libraries) – the next EasyEDA session.
2. A female header whose datasheet gives a thinner tail (e.g. 0.6 mm square, 0.85 mm diagonal) – enter it as the lead
   size and buy exactly that one.

## D-8 Base load for USB power banks (2026-10-25)

Without the servo moving, the circuit draws 35–75 mA. Many power banks switch off below 50–100 mA after a few seconds –
possibly in the middle of the countdown, and the bell never rings. R8 ∥ R9 (2 × 100 Ω, 2512, 1 W) draw a permanent
100 mA from +5V, 0.25 W per resistor. Kept simple on purpose: the bell runs once a year for about 15 minutes, so the
wasted energy does not matter; a load switched by the Nano would need a transistor and firmware. The simulation checks
every scenario against a 100 mA minimum (`i_min_a`).

## D-9 The LED row stays at the back edge (2026-10-25)

The layout review (M-5) found that, seen flat from the front at a low angle, the plugged-in Nano (12–16 mm high) and C1
(13 mm) hide part of the LED row. Owner's decision: the placement stays as it is – the board is seen from above in its
place, and moving the row would mean a new layout for no practical gain.

## D-10 No power switch on the board (2026-10-25)

Kept simple: the bell runs once a year for about 15 minutes and is switched on and off by plugging in the power bank.
A switch on the carrier could not switch the Nano anyway, which is powered through its own USB socket (D-3).
