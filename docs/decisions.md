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
(0.7 A assumed) would draw about 810 mA. The original Nano's
polyfuse (MF-MSMF050) holds 0.5 A and is only guaranteed to trip at 1.0 A, many clones have none, and the Schottky
diode (MBR0520, 0.5 A average) then carries about 0.81 A – harmless for the few seconds of a bell phase, not as a
permanent state. The scenario `servo-stalled` runs as information only; the firmware detaches the servo 1 s after it
has reached its rest position (since 2026-10-26, D-16), so a jam there cannot become a permanent overload (M-1
review, note 4) – with an analog servo such as the SG90; a digital one may keep holding without pulses.

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

## D-7 Nano footprint with 1.1 mm holes (2026-10-25)

The first Nano footprint (user library, C9900017879) had 0.90 mm holes – too small for the usual 0.64 mm square tails
of the female headers (0.91 mm across the diagonal; gate check L-9 failed). U1 now uses the footprint of C9900187880
(COMM-TH_L43.2-W17.8-P2.54_ATMEGA328P): 1.1 mm holes, 1.7 mm pads, the same pad numbering (checked after placing:
pad 14 = D11, pad 15 = D12 at the end of the row). Its symbol names the pins after the ATmega ports and labels pins
14/15 the wrong way round (PB4/PB3); only the labels are swapped, the connections go by pin number.
The footprint also brings the Nano's four corner holes (NPTH Ø1.9 mm) – harmless, nothing sits there.

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

# Board variants (2026-10-26)

Three variants of the board, each with the full edakit pipeline (variants/README.md). The main board above stays as
released on 2026-10-25.

## D-11 Variant SMD: everything the Economic assembly can place (2026-10-26)

The circuit of the main board, assembled by JLCPCB's Economic PCBA on the top side; only the Nano's two female headers
are hand-soldered (owner's wish: "smd LEDs, the pins as SMD if possible, the microcontroller on headers to solder
yourself, the capacitor only if it does not force the more expensive assembly").

- **LEDs:** 0805 LEDs of one series, KENTO KT-0805: red KT-0805R (C2295, Extended), yellow KT-0805Y (C2296, Basic),
  emerald green KT-0805G (C2297, Basic). One footprint (LED0805-R-RD) for all five: its triangle and its chamfered
  corner both mark pad 2 as the cathode, and every symbol has the anode on pin 1 – the row points the same way at 0°.
  The Basic red NCD0805R1 (C84256) was dropped: its footprint has the chamfer at pad 1 but a bar mark at pad 2, too
  ambiguous for a part JLCPCB turns by the footprint. The series resistors stay 330 Ω: 5.8–9.0 mA (red, yellow) and
  3.7–6.6 mA (green) in the simulation.
- **Servo header:** SMD 1×3, 2.54 mm, staggered pins (C41417360). It holds less pulling force than the through-hole
  header; the servo plug is plugged once.
- **C1:** 1000 µF / 16 V SMD can Ø10 × 10.2 mm (C3359). JLCPCB lists it for Economic *and* Standard PCBA, so it does
  not force the Standard assembly; it costs one more Extended-part fee.
- Alternatives: 1206 LEDs (larger, all Extended), the 5 mm LEDs through Standard PCBA (THT assembly, more expensive),
  C1 hand-soldered as on the main board.

## D-12 Variant THT: no assembly, through-hole only (2026-10-26)

A bare board, every part soldered by hand: resistors 1/4 W metal film (330 Ω C58608, 4.7 kΩ C57204), the base load
1 W metal film (100 Ω C119469), buttons 6 × 6 mm THT (K2-1102DP-C4SW-04, C110153 – the through-hole sibling of the
SMD button C127509, same pin pairs). LEDs, C1, J1 and the Nano as on the main board. The BOM is empty
(`[release] assembly = { sides = [] }`), no tooling holes. The series resistors lie flat below their LEDs, staggered
(10.5 mm pitch next to 10 mm LED spacing); R8/R9 stand between the Nano and C1, 6 mm apart.

## D-13 Variant ESP32: LILYGO T-Display V1.1 instead of the Nano (2026-10-26)

Like the variant SMD, with a LILYGO T-Display V1.1 (ESP32-D0WDQ6, 1.14 inch ST7789V TFT) plugged into two 1×12
female headers – the owner's choice, "the smaller variant" (the T-Display-S3 has a 1.9 inch display).

- **Library:** the module is neither in EasyEDA's library nor at LCSC, and a device created through the API cannot
  be placed in the local client (GET_DEVICE: "Device details data does not exist"). So the EasyEDA device is a
  stand-in: the 2×12 female header 2541FV-2x12P (C18722937, symbol pins 1–24, prefix U). EasyEDA keeps its symbol and
  footprint as copies in the project; variants/esp32/hardware/lib/tdisplay_device.py rebuilds both into the
  T-Display's – pin names from LILYGO's pin map, its schematic (headers P4/P5) and the KiCad and Eagle libraries of its
  repository (all four agree), 2 × 12 pads 22.86 mm apart, holes 1.1 mm and pads 1.7 mm as on the Nano footprint
  (D-7), module outline and USB end on the silkscreen. The same way the pytree project builds its RP2350-Zero from the
  RP2040-Zero. Only the board esp32 uses C18722937; the footprint keeps the header's name. **Measure the module before
  ordering:** rows 22.86 mm apart, pitch 2.54 mm.
- **Pins:** LEDs on IO27, IO26, IO25, IO33, IO32 (one row, in countdown order), servo on IO13, buttons on IO38/IO37
  (input only, no internal pulls – R7/R6 pull down). The strapping pins IO12, IO15 and IO2 stay free.
- **3.3 V logic:** the buttons switch the module's 3V3 (AP2112K) instead of 5 V – the ESP32's inputs take at most
  3.6 V (D-4 does not apply). The servo gets a 3.3 V PWM signal; hobby servos accept it.
- **Supply:** the module's 5V pin is USB VBUS behind its 1N5819 (1 A): servo, C1 and the base load R8/R9 (D-8, kept)
  hang there as on the Nano. The simulation gives about 470 mA while the bell swings, 870 mA with a stalled servo –
  with Wi-Fi (D-17) up to 0.66 A and 1.06 A.
- **Placement:** the module where the Nano was, USB-C at the left edge; R8/R9 move to the right (the module covers
  their place).
- **Firmware:** variants/esp32/firmware (D-17), the port of src/firmware with the pins above (`checks.pin_locks` in
  variants/esp32/hardware/graph.json), the servo on an LEDC channel at 50 Hz. Requirements from the M-1 review:
  IO37/IO38 configured as plain inputs (no internal pulls exist), debounce as in buttons.ino (H-3), and the servo
  detached once it is at rest with a limited bell phase – a stalled servo loads the module's 1N5819 with 0.87 A of its
  1 A (like D-3 on the Nano), with Wi-Fi up to 1.06 A.
- **Radio** (requirement from the M-6 review, D-16 – support, not legal advice; Wi-Fi since D-17): Bluetooth is never
  started – no `BLEDevice::init`, `BluetoothSerial.begin`, `btStart`, `esp_bt_controller_enable`. Wi-Fi only as D-17
  says: the ESP32 can also use channel 14 (2484 MHz), outside the EU band 2400–2483.5 MHz, so the firmware sets the
  country DE with 802.11d off (`esp_wifi_set_country_code("DE", false)` – with 802.11d on, an access point announcing
  JP would open channel 14): channels 1–13 only. The module's own antenna, the default power limit (at most 20.5 dBm
  at the chip, antenna −4.32 dBi: about 16 dBm e.i.r.p. against 20 dBm), no custom PHY init data, no frames that
  disconnect or disturb other WLANs (BNetzA Vfg. 91/2025). Checked at M-4: a phone shows no Bluetooth device of the
  bell.
- **Use:** the module's USB-C socket has a 5.1 kΩ pull-down on one CC line only: from a USB-C source (C-to-C cable)
  it gets power in one plug orientation only – use a USB-A-to-C cable or turn the plug over. The 2 × 12 pin field is
  symmetric: plug the module in with USB-C at the board edge and the display up (silkscreen "5V" at U1.1). No cell at
  the module's battery input: the base load R8 ∥ R9 (D-8) would drain it with about 80 mA, and there is no switch
  (D-10); a cell needs a new M-6 (D-16).

## D-14 Variant ESP32: yellow-green instead of emerald green (2026-10-26)

The emerald-green KT-0805G needs 2.6–3.1 V at 5 mA; from a 3.3 V output it would shine unevenly from part to part.
Owner's decision: yellow-green KT-0805YG (C2292, Extended, 1.8–2.4 V). All five series resistors 100 Ω (C17408):
(3.3 V − 2.1 V) / (100 Ω + 30 Ω output + 10 Ω LED) ≈ 8.6 mA; 7.3–11.4 mA over all corners in the simulation.

## D-15 Variants as boards of one EasyEDA project, as folders in the repository (2026-10-26)

Owner's decision: no new EasyEDA projects – the variants are the boards `smd`, `tht` and `esp32` of the project
`christmas-bell`, next to `main`. In the repository each variant is a folder variants/<variant>/ with its own
edakit.toml, graph, parts database, simulation config and sign-offs. The parts database is not shared: the circuit
hash of a board covers every file of its parts folder, so a part added for one variant would void the sign-offs of
the others.

## D-16 Purpose: private, all four boards (2026-10-26)

Owner's decision: the boards main, smd, tht and esp32 are built for the owner's own use – `purpose.use = private`,
market EU, in each graph. The regulatory review M-6 (edakit handbook 15, required for a release since edakit ef1183f)
checks for this purpose; giving boards away or selling them needs a new purpose and a new M-6. The purpose is part of
the circuit hash: adding it voided M-1 once on all four boards. The main board stays released as ordered
(hardware/README.md) – M-6 counts for a new order.

**Not legal advice.** M-6 and everything this repository says about law – the purpose, radio, CE, RoHS, REACH,
e-waste – are support without any claim to correctness; nothing in them is legally guaranteed (edakit handbook 15).

The reviews of 2026-10-26, each by an agent in its own session:

- **M-1** confirmed on all four boards: the change adds only the purpose and, on esp32, the T-Display's compliance
  data; checks, simulation and hints are unchanged.
- **M-6** OK on main, smd and tht: no transmitter, 5 V USB only, no battery, no mains; RoHS and REACH data are not
  needed for own use.
- **M-6** OK on esp32 after one round: the ESP32 could use Wi-Fi channel 14, outside the EU band, so the firmware
  keeps Wi-Fi and Bluetooth off (D-13 "Radio"); its power is within the limit. USB power only, no cell at the module's
  battery input. The T-Display's radio data and certificates – a test lab's CE attestation, no EU declaration of
  conformity – are in its parts entry (variants/esp32/hardware/parts/C18722937.json). D-17 then put Wi-Fi to use
  on channels 1–13; M-1 and M-6 of esp32 were renewed for it.
- **Notes:** the Nano firmware did not detach the servo, so a jam at rest stayed an overload until the bell was
  unplugged (D-3); since 2026-10-26 it detaches the servo 1 s after the rest move (owner's OK). At its end the bell
  goes to e-waste collection (ElektroG § 10).

## D-17 Variant ESP32: a web page over Wi-Fi (2026-10-26)

Owner's decision: the ESP32 board gets a simple web page – status, time to ding, start, stop, pause and the timer.
The firmware is variants/esp32/firmware (PlatformIO; the countdown logic lib/BellTimer with host tests).

- **Wi-Fi:** on its first start the bell opens a setup hotspot `Glocke-XXXX` (WPA2; name and a password made once
  per module on the display). Its page – phones show it as a login page – stores the home network; the bell then
  joins it as a station and serves its page at http://glocke.local, the address is on the display. A home network
  that was never reached opens the hotspot again after 30 s; one that worked before is retried. No internet service,
  no Bluetooth; the page is open to everyone in the home network. Radio settings: D-13 "Radio" – channels 1–13
  (country DE, 802.11d off), the module's own antenna, the default power limit. This replaces "Wi-Fi and Bluetooth
  stay off" of D-16; M-6 was renewed for it.
- **Buttons:** as on the Nano – start (while paused: go on), reset = stop, start held and reset = ring now. Reset held
  3 s and released: Wi-Fi on or off, kept over a power cut. Held 10 s and released: forget the home network, the
  setup hotspot opens. While reset is held, the display shows what releasing it does, and the LEDs: the green ones =
  on/off, red = forget. A short press only stops, start during the hold cancels it.
- **Timer:** the time from start to ding, 10 s to 24 h, 65 s by default as on the Nano (the countdown on the LEDs,
  then 5 s final warning). It is stored in the module and counts from the next start. Pause holds the time to ding,
  the current LED stays on; start goes on.
- **Display:** the state, the time to ding (when idle: the timer) and the address of the page; while the setup
  hotspot is open and the bell idle, its name and password.
- **Supply:** with Wi-Fi the module draws more – 0.27 A as an upper bound in its parts entry (transmitting
  continuously, ESP32 datasheet table 5-4). The simulation gives up to 0.66 A while the bell swings and 1.06 A with a
  stalled servo, above the module's 1N5819 (1 A) for the seconds of a bell phase (information, like D-3); the servo is
  detached at rest. Power the bell from a USB charger or power bank with at least 1 A rather than from a computer.
  M-1 was renewed for it.

## D-18 Proposals to edakit from the reviews of D-16 and D-17 (2026-10-26)

Owner's decision: what the reviewers of D-16 and D-17 suggested for edakit goes there as proposals (edakit handbook
14.4 and 11.6) – all but the hint on a module's battery input.

| # | Proposal | Kind | edakit |
|---|---|---|---|
| 1 | radio power at the RF port and the antenna gain | feature | G-24, built as a check ([#21](https://github.com/tgd1975/edakit/issues/21)) |
| 2a | a transmitter stays in the EU bands, or the graph says how it is used | check | G-25 ([#22](https://github.com/tgd1975/edakit/issues/22)) |
| 2b | modules and microcontrollers state their radio | check | P-11 ([#23](https://github.com/tgd1975/edakit/issues/23)) |
| 3 | own use and gifts: EMVG § 6 and REACH Art. 33 | hint (handbook 15) | handbook 15 and the regulatory reviewer ([#24](https://github.com/tgd1975/edakit/issues/24)) |
| 4 | a lower bound of a module's current for the minimum-load check | feature | built: `params.i_core_min_a` ([#25](https://github.com/tgd1975/edakit/issues/25)) |
| 5 | dissipation of a module's on-board LDO | feature | built: `ratings.rth_ja_k_per_w`, `tj_max_c` ([#26](https://github.com/tgd1975/edakit/issues/26)) |
| 6 | ESP32 firmware fixes the country with 802.11d off | hint (handbook 15) | handbook 15.2 and the regulatory reviewer ([#27](https://github.com/tgd1975/edakit/issues/27)) |

edakit accepted all seven (triaged by hand on 2026-10-29, its Action's token being dead); they are on edakit main since
bf7450a. The owner's rule for the new checks: edakit reports what the firmware has to keep but does not block on it –
for `use: "private"` G-25 and P-11 are notes, for a sale warnings to accept. The bell's gate decisions stay as they
were; `edakit check` and the gate protocol (end of section 2, "Information") show:

- **P-11** on main, smd and tht: the Nano's entry (C9900187880) states no radio.
- **G-25** on esp32: U1 can transmit in 2412–2484 MHz, beyond the EU band 2400–2483.5 MHz; the firmware keeps to
  channels 1–13 (D-13 "Radio": country DE, 802.11d off). G-24 passes at 16.2 dBm e.i.r.p.

The entries that clear the notes – `compliance.radio: "none"` in the Nano's entry, `purpose.radio` with the bands
2412–2472 MHz in esp32's graph – and the keys of #25 and #26 for U1 change the circuit hash, and M-1 and M-6 must then
be signed again. So they come with each board's next circuit change; on esp32 together with the T-Display's footprint
as data, if edakit's step 3.6 replaces `tdisplay_device.py`. Tried by edakit on a copy of esp32: with `i_core_min_a`
0.04 A the minimum load reads at least 0.136 A, so D-8 holds; with 184 K/W and 150 °C the on-board LDO reaches at
most 122 °C (USB at 5.05 V, warning phase, 30 °C around), 3 K under edakit's limit of 125 °C. As everywhere here:
support, not legal advice (D-16).

## D-19 The Nanos are at hand: P-5 accepted (2026-10-28)

Owner's decision: the Arduino Nanos for the boards main, smd and tht are at hand – nothing to order. edakit's warning
P-5 (supplier per part, since edakit a8b6011) is accepted in the three sign-off files for U1 with C9900187880; the
acceptance lapses when U1 gets another part. The ESP32 board's T-Display is bought separately (D-13).

## D-20 M-5 bound to the manufacturing files (2026-10-28)

Since edakit f6dd9f7 the artwork SVGs count in the layout hash. The SVGs are unchanged since 7667817, older than every
M-5 review, so the boards did not change – their layout hashes did, and M-5 lapsed on all four. The plan was that the
owner confirms M-5 for the new hashes. That adds nothing a comparison of the files cannot show.

M-5 therefore has edakit's default scope `fab` now (edakit handbook 8.2): it is bound to the hash of what the
manufacturer builds from – Gerber layers rasterised at 0.02 mm, drill hits, BOM and CPL rows – in the gate run its
reviewer checked.

| Board | Reviewed run | fab_sha256 |
|---|---|---|
| main | 20261025-215346 (the release run 20261025-220549 has the same) | f314419f… |
| smd | 20261026-123018 | 4e79e5c0… |
| tht | 20261026-123036 | 441ab22c… |
| esp32 | 20261026-123051 | f2962d76… |

The gate checks it: M-5 counts in a gate run with EasyEDA whose files give the same hash, and is not checked offline.
When the files differ, `edakit fab diff <reviewed run> <new run>` shows where, and the pcb-reviewer reviews the
difference. A layout hash that changes without a change of the board – a comment, a new hash method – no longer voids
M-5.
