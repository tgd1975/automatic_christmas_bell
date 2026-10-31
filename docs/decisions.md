# Board decisions

Numbered, with reason and date. Source of the circuit: `weihnachtsglocke.fzz` (docs/old/). The hardware graph
`hardware/graph.toml` reproduces it 1:1, with the Fritzing designators (Bauteil1 = U1, Servo = J1); `hardware/graph.json`
beside it is the generated file (`edakit graph json --write`, D-25).

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
- **Firmware:** variants/esp32/firmware (D-17), the port of src/firmware with the pins above (`locks.pins` in
  variants/esp32/hardware/graph.toml), the servo on an LEDC channel at 50 Hz. Requirements from the M-1 review:
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

## D-21 Footprint print accepted at the gates with EasyEDA (2026-10-30)

The first gate runs with EasyEDA after the import acknowledgement (edakit b36a6d0) failed only L-17: it tells
edakit's own print from the footprints' by the silk files `silk apply` keeps before it prints, and the boards had been
printed by an older edakit. `edakit silk apply` ran again on all four boards; the manufacturing files came out the same
(fab hashes of D-20), so M-5 still counts. Left were warnings about print that is not edakit's. Owner's decision: all
four accepted, in `accepted_warnings` of each sign-off file, bound to the parts concerned.

1. **S1/S2** (all four boards): the buttons' footprint print reaches onto their pads' solder-mask openings –
   0.012 mm², on tht 0.067 mm². JLCPCB clips print on openings.
2. **C1** (smd, esp32): the same for the capacitor's footprint, 0.051 mm².
3. **U1, the Nano** (main, smd, tht): its footprint prints 0.4 mm beyond the left board edge, where the USB socket
   overhangs (1.8 mm²). JLCPCB leaves out print beyond the board; M-5 of main accepted it on 2026-10-25.
4. **main, top copper:** a copper-free spot of 12 mm diameter at (55, 25) mm between C1 and the buttons, above
   `[copper] max_bare_mm` (5 mm); 75 % copper on top. Not a manufacturing matter; removing it would mean routing
   again, new manufacturing files and M-5 again.

Release runs of 2026-10-30, all RELEASED: main 20261030-232729 (supersedes 20261025-220549), smd 20261030-232631,
tht 20261030-232650, esp32 20261030-232707 – build output, kept out of git (D-22).

## D-22 Manufacturing files: build output, published with the order (2026-10-31)

Owner's view after the release of D-21: the gate runs archived in git are build output, not repository content –
but important states should be kept now and then. What holds a release is in the repository already: the sign-offs
with their hashes (M-5 names the manufacturing files it reviewed, D-20). The files themselves need no archive: as long
as the PCB in EasyEDA is untouched the gate exports the same files with the same hash (seen on 2026-10-30, four days
after the review), and once ordered JLCPCB keeps them for a reorder. If the EasyEDA state is lost, the board is made
again from the graph and the board file – routed anew, so M-5 anew: agent time, none of the owner's.

1. Gate runs stay in `build/release/` (ignored by git). The archive of the release commit was undone before the
   push; nothing else is archived. This deviates from edakit's release skill (step 6, `git add -f`).
2. Important states are published, not archived: a GitHub release per order, tag = the date, the current release
   of all four boards each time (`gerber_<b>.zip`, `bom_<b>.csv`, `cpl_<b>.csv`, `polarity_<b>.png`,
   `manifest_<b>.json`, `SHA256SUMS`), marked pre-release until a board of that state has been built and works.
   The notes name the gate runs, the fab hashes, which boards changed since the previous release, the decisions
   since then, and the purpose: private use (D-16) – the regulatory review is support, not legal advice.
3. One command, `make publish` ([tools/publish_release.py](../tools/publish_release.py)): clean tree and HEAD
   pushed, `edakit release current` per board, `edakit release verify` on the order files (it refuses otherwise),
   staging in `build/publish/<tag>/`, `gh release create --prerelease`. `make publish-draft` runs the same as a draft
   only the account sees – tested on 2026-10-31, 21 files, deleted again. `make publish-built TAG=<tag>` drops the
   pre-release mark. It needs `gh`, logged in, and edakit (on the PATH, `$EDAKIT`, or a clone `../edakit` with
   its `.venv`; the first test from a terminal without edakit on the PATH would have failed).
4. The firmware is not published; whoever wants it builds it (`pio run`).

Owner (2026-10-31): this is the desired behaviour and should be edakit's default – no archive in git, and
`edakit release publish` doing what the script does. Handed to edakit as a prompt for an edakit session, not as an
issue. Once edakit has it, `make publish` calls it and tools/publish_release.py goes.

## D-23 Variant ESP32 THT: the T-Display board with through-hole parts, no assembly (2026-10-31)

Owner's wish: "eine Version mit ESP32 und Pins zum selber Löten" – a fifth board `esp32tht` next to `esp32`, the
circuit of the variant ESP32 (D-13, D-14, D-17) with the through-hole parts of the variant THT (D-12): a bare board,
everything hand-soldered, the BOM empty (`[release] assembly = { sides = [] }`), no tooling holes. Folder
variants/esp32tht/, board `esp32tht` in the EasyEDA project christmas-bell (D-15).

- **Same circuit, same pins** as the variant ESP32: the firmware variants/esp32/firmware runs unchanged (pin locks
  copied), Wi-Fi as in D-17.
- **Parts of the variant THT:** buttons C110153, pull-downs 4.7 kΩ ¼ W (C57204), base load 2 × 100 Ω 1 W (C119469),
  C1 1000 µF / 16 V radial (C439782), servo header C2937625, red XL-504SURD (C2895493) and yellow XL-504UYD
  (C2895495).
- **New parts:** the series resistors 100 Ω ¼ W metal film, MFR0W4F1000A50 (C57438, the sibling of the THT board's
  330 Ω, 25 084 at LCSC on 2026-10-31); the two green LEDs yellow-green as in D-14 – the 3 V green XL-504UGD of the
  THT board would shine unevenly from 3.3 V outputs: XL-504SYGD (C2895551, same series, diffused, 562–575 nm,
  VF 2.0–2.6 V at 20 mA, 6 592 at LCSC). 7.2–11.2 mA (yellow-green) and 8.6–12.6 mA (red, yellow) in the simulation.
- **Radio:** `purpose.radio` states channels 1–13 (2412–2472 MHz) for U1 right away – on esp32 that entry waits
  for its next circuit change (D-18).
- **Tooling:** the board's files are in the form of edakit's restructuring ("rules at scale", edakit main 5196c6f,
  `edakit convert`); the four released boards stay as they are (edakit b36a6d0) until their next change.
- Alternative: the variant ESP32 with the SMD parts hand-soldered – 0805 parts and the SMD servo header are harder
  to solder by hand and hold less.

After the reviews of state e4a24024… (M-1 OK, M-6 OK; 2026-10-31):

- **Brightness** (owner's decision): the yellow-green LEDs give 50–200 mcd at 20 mA, the red and yellow ones
  400–900 mcd – every 5 mm yellow-green at LCSC is as dim (Everlight 333-2SYGD 40–80, TONYU DY-333UYGD 120,
  TOGIALED 30–60 mcd). R1, R2 and R5 (red and yellow) are 330 Ω (C58608, as on the THT board): 3.4–5.0 mA there,
  7.2–11.2 mA in the yellow-green ones. The SMD board esp32 has the same gap, smaller (24–70 against 70–210 mcd); it
  stays as released.
- **Order:** a bare board is bought part by part (`edakit order`). U1's entry now names its supplier (Tinytronics,
  the V1.1 – neither LCSC nor Berrybase or Reichelt sell it), so the stand-in C18722937 no longer lands in the LCSC
  cart; the two 1×12 female headers KH-2.54FH-1X12P-H8.5 (C2905419, pin 0.64 × 0.4 mm, recommended hole 1.02 mm,
  ours 1.1 mm) are an `[[extra]]` of edakit.toml.
- With the same renewal: the hand-over to the layout in the graph (`layout`), U1's least current 0.04 A and its LDO
  AP2112K at 184 K/W, 150 °C (D-18's values, θJA from the Diodes datasheet; at most 117 °C simulated against 125 °C),
  C2895551 colour "green" (edakit's list), the R8/R9 notes (at least 0.136 A with the base load).
- M-1 and M-6 renewed for state bcb27b87… (2026-10-31). The 330 Ω bring red and yellow *towards* the yellow-green,
  not to it: 79–257 mcd against 20–124 mcd by the datasheets' Iv–IF curve (the ranges overlap; about 2.5× in
  luminous intensity, to the eye about 1.5×) – before 6–7×. Judged by eye at M-4 on the first board; 470 Ω (C58592,
  about 2×) is the next step, 680 Ω (C58599, 1.3–1.5×) would need a lower LED-on limit in the simulation. The R1/R2/R5
  notes in the graph say "dimmed to" – corrected with the next circuit change, as are Tinytronics' SKU 002649 in U1's
  `order` and a hint on the module's single CC pull-down (USB-A-to-C cable).
- **Layout** (first round 53c1139, M-5 reviewed offline: would sign on equal files): the T-Display 3.5 mm nearer the
  front than on esp32 so that tht's staggered resistors fit; 0 vias. From the review: a "+" at LED4/LED5 (their
  footprint shows only the flat), the board label 1 mm above the milled edge, LED2's anode link and BTN_START on the
  bottom (fixed wires), `[looks]` top ≤ 0.35 m track and no via, `hand_solder_keep_mm` 0.5. GND under the module's
  antenna end stays as on esp32 (86–93 % copper there, 8.5 mm below the module; a cut-out would leave a bare
  7 × 26 mm field) – the open hardware test of esp32 answers it for both. The buttons' own corner circles reach into
  their pad openings (0.14 mm²): JLCPCB clips them, as D-21 (1) accepted for the same button C110153 on tht.
- **Gate round** (e7f3f24): the geometry dumped again with edakit's hole fix (`pcb dump` read the holes ten times too
  small; fixed on edakit main 8bdb933), routed again with the layout notes – one via was left on LED_G1, which changed
  to the top for its last 6 mm, so its route is a bottom fixed wire now: 16 nets, 0 vias, top 0.27 m, DRC 0. Gate run
  20261031-154618 (edakit 8bdb933): everything passed except M-5, open, and GEO.silk at S1/S2 – the buttons' own print,
  0.067 mm² each. Owner's decision 2026-10-31: D-21 (1) holds for esp32tht too, accepted in its sign-off file, bound
  to S1/S2 = C110153.
  M-5 by the agent pcb-reviewer on that run (fab b768d2f5…): no block or important finding; S1/S2's 1.3 mm holes
  (datasheet 1.0 mm) do not hold the snap-in legs – press them flat while soldering (variants/README.md, THT). Gate run
  20261031-160323 on the same files: **RELEASED** (git 0516fc4) – build output, published with the order (D-22).

## D-24 All boards in edakit's current file form (2026-10-31)

Owner's request: "convert this project to an edakit project". It was one already – five boards, all released – but
main, smd, tht and esp32 were still in the form before edakit's restructuring (D-23), and edakit 8bdb933 no longer
reads it: `edakit check` and `edakit sim` stopped at the first parts entry ("the form of before the restructuring").
`edakit convert --write` per board turned graph, parts entries and sign-off file into the new form (values/limits with
units, `accept` by code instead of `waive`/`accepted_warnings`, P-5 → PARTS.supplier); the content is unchanged.

- **Sign-offs:** M-1 and M-6 (scope circuit) keep counting – edakit moved them to the new circuit hashes and listed
  both in `rehashed`: main 36ddd746… → 77c5ddc9…, smd 1ed944d2… → f66ebc83…, tht 5ddc2553… → e7abaa97…, esp32
  3f7cec3d… → 4f36f0b7…. M-5 (scope fab) is bound to the manufacturing files, which the conversion does not touch.
  D-19's acceptance of the Nano without supplier carries over (accepted in the offline gate).
- **Releases:** unchanged – `edakit release current` names the same runs (main 20261030-232729, smd -232631,
  tht -232650, esp32 -232707, esp32tht 20261031-160323), so `make publish` covers all five as before.
- **Checked** on all five boards with edakit 8bdb933: `check`, `sim` and `docs` exit 0, the offline gate open only
  in M-5 and the EasyEDA stages S, L and F, as on esp32tht.
- What waits for a board's next circuit change (D-18, D-23) still waits: the conversion changes the form, not the
  circuit.

## D-25 The whole bell on today's edakit: migrate first, then release all five and order (2026-10-31)

Owner's goal: everything the skill new-project writes today, nothing only in EasyEDA or in a head – all five boards,
edakit 868e942. Owner's decision (round of 2026-10-31, item 1): **migrate now**, then each board once M-1 and M-6, an
EasyEDA gate for all five, and the order through the skill cart. Reason: the skill cart refuses today's releases
already (D-24 rehashed the circuit, `cart prepare` compares the run's circuit hash), the requirements file changes the
circuit hash of all five boards and `[order]` their fab hash – one round of reviews and gates instead of two. The
alternatives, steps 1–3 now and ordering by hand with `make publish`, or ordering first, would have meant a second
round before the next order.

Further answers of the round:

- **No CI** (item 7): one author on one machine; the pre-commit hook runs the same checks on every commit.
- **Decided by Claude, confirmed by the owner** (item 9): `[scripts.kunst]` in all five configurations, first
  recorded with `edakit scripts stamp` (the SVGs stay byte for byte); `[scripts.tdisplay]` only in esp32 with the step
  `symbol` (the footprint goes to `footprint_data`); `distributors = ["lcsc", "reichelt", "rs"]` after the owner's
  supplier rule (Berrybase, Bürklin and Tinytronics are not edakit distributors – a gap for edakit); `[firmware]` for
  esp32 and esp32tht, not for the Nano boards (their pin names are ATmega ports, no regex gives Arduino numbers – a gap
  for edakit); `[docs]` with hardware/README.md; `[[extra]]` for the female headers of every board; `spare_pct`,
  `datasheets` and `domains` at edakit's defaults (the graph suggests radio on esp32 and esp32tht, so it is on); the
  circuit items waiting since D-18 and D-23 come now, as M-1 and M-6 are drawn anew anyway; stale documents fixed.

## D-26 esp32: the 0805 LEDs at 52 % of their rating accepted (2026-10-31)

edakit 868e942 holds LEDs to LIM.p: on esp32 LED1–LED5 (KENTO KT-0805R/Y/YG, Pd 40 mW by the datasheet) take
20.7 mW at the forward-voltage minimum against the 20 mW of edakit's 50 % derating – 18 × LIM.p, stage E red.
Owner's decision (item 2): accepted in the sign-off file – 52 % of the datasheet's rating at the worst corner, the
brightness stays. Alternative: R1–R5 120 Ω (about 18 mW, about 15 % darker).

## D-27 The order form as keys: order number, delivery, cost (2026-10-31)

Owner's decisions (items 3, 4, 8):

- **Order number** (`[order] mark`): `"remove"` on all five boards, and nothing instead – no 2D barcode, no serial
  number. The `JLCJLCJLCJLC` placeholder comes off the silkscreen of smd, tht and esp32. main and esp32tht never had
  one. Changed by the owner on 2026-10-31 ("I don't need the order number, nothing instead"); the first answer of the
  round was `"specify"` on smd, tht and esp32. Reason: on 2026-10-31 edakit-c9's ordering step 0 found that JLCPCB's
  form no longer offers an order number. "Mark on PCB" has only "Remove Mark" and "2D barcode (Serial Number)", and
  with a placeholder and `"specify"` edakit's updated JLCPCB profile reports FILES.order. Taking the placeholder off
  changes the layout hash of the three boards; `[order]` changes the fab hash of every board. Both fall into the one
  M-5 round D-25 plans.
- **Delivery** (`[cart]`): Austria, DHL Express.
- **Cost** (`[cost]`): no budget, the estimate in EUR.

## D-28 Schematic drawings with wires (2026-10-31)

Owner's decision (item 5): `style = "wires"` for all five boards – every connection a wire, as the bell's first
drawing had it (docs/old/). Only the SVGs of `edakit schematic draw`; EasyEDA's schematics keep their labels; no hash.

## D-29 Publishing with edakit itself (2026-10-31)

Owner's decision (item 6), replacing D-22's own script: `make publish`, `publish-draft` and `publish-built` call
`edakit release publish` (`--draft`, `--built TAG`), with `[release] publish = { variants = true, decisions =
"docs/decisions.md" }` in the main configuration; tools/publish_release.py goes. Nothing was published yet, so no
history breaks. D-22's rule stays: gate runs are build output (`archive = "none"`), what is ordered is a GitHub release.

## D-30 The T-Display's footprint as data (2026-10-31)

Plan 3.6 of edakit, its live run of 2026-10-31: the footprint goes to the data path, the symbol stays the script's.
`edakit part footprint C18722937 --board esp32` (and `--board esp32tht`) took the pad places from the dump – they
agree with tdisplay_device.py to 0.001 mm –; shape, size, hole, outline, the USB box and the texts came from the same
script, as edakit's dry run took them; no `"symbol"` in the data, so `part build` leaves the symbol to
`tdisplay_device.py symbol` (`[scripts.tdisplay]`, D-25). PARTS.footprint passes on both entries; SYNC.footprint
compares the places now and shape, size and hole after the next `pcb dump` (esp32's dump has no holes yet). The copy in
EasyEDA is the script's, built from the same values, so nothing is rebuilt. The entry changes the circuit hash of esp32
and esp32tht (M-1 anew; M-6 too, until edakit binds it to its hash 'electrical' without footprint data – the owner's
decision of 2026-10-31 in edakit) and their layout hash.

## D-31 The Nano's pin print in its parts entry (2026-10-31)

edakit W.5: `print` per pin – what the module's own silkscreen says – in the Nano's entry C9900187880 of main, smd
and tht, taken by pin number from edakit's library entry A000005 (Arduino's pinout page A000005-full-pinout.pdf of
30/06/2021; ~ marks a PWM pin). Pin 14 prints ~D11 and pin 15 D12, although the EasyEDA symbol names them PB4/PB3
(D-7) – the print is the module's. It changes the circuit hash of the three Nano boards, so it comes in the same
renewal of M-1 and M-6 as the requirements file. The T-Display gets no `print`: no written source of its silkscreen
text is at hand (the pin map is a picture) – open until the module is measured (TODO.md), then with that as source.

## D-32 The bell's requirements file (2026-10-31)

Plan 4.1 of edakit: the inventory of the agent requirements-engineer (2026-10-31), drafts by the skill requirements,
the owner's round of the same day (items 11 to 16). **All drafts accepted as written**: N-1 to N-7, R-1 to R-12 and
R-40 for all five boards (`hardware/requirements.toml`), R-20 for the Nano boards (`hardware/requirements_nano.toml`,
read by main, smd and tht), R-30 to R-35 for the ESP32 boards (`variants/esp32/hardware/requirements.toml`, read by
esp32 and esp32tht) – three files, so that no Nano value binds the ESP32 boards (decided by Claude, confirmed).

- **Servo supply** (item 11): the separate 5 V, 1 A supply of README.md and IMPLEMENTIERUNG.md stays dropped – D-3
  holds, N-11 is `dropped`; README.md corrected.
- **docs/IMPLEMENTIERUNG.md** (item 12): history of the Fritzing time, moved to docs/old/ with a note on top; its
  values (220 Ω–1 kΩ, 10 kΩ, the separate servo supply, the size) are not the boards'.
- **Running time** (item 13): no requirement – the user picks the power bank; R-2 keeps it on.
- **Brightness** (item 14): R-40 `should`, judged by eye at the acceptance test M-4 (all five on at 1–2 m in room
  light) – no number, no change to the boards now.
- **Decided by Claude, confirmed** (item 16): a transient scenario of the servo's start in every sim.json as the
  evidence of R-9 beside its acceptance step (D-33); esp32's U1 gets the regulator's thermal values of esp32tht so that
  R-32 has its evidence there (D-34); mounting, firmware times and Wi-Fi behaviour stay in the README and the
  firmware.

The files are in the circuit hash of every board: M-1 and M-6 anew on all five, whose notes name the requirements
they find met.

## D-33 The servo's start as a transient run (2026-10-31)

Evidence of R-9 (D-32, item 16 b): every sim.json has the transient run `servo-start` – USB at the low end of the
supply (4.45 V at the Nano's 5V pin, 4.35 V at the T-Display's), the servo jumping from 10 mA to its stall current
0.7 A for 20 ms, then 0.3 A swinging. +5V falls to 4.05 V on the Nano boards (minimum 3.8 V) and to 3.93 V on the
ESP32 boards (minimum 3.6 V); the ESP32 boards' peak is 1.05 A for those 20 ms. R-9 names the row (LIM.range
servo-start U1 lowest supply voltage once started) beside its acceptance step; its text says the step instead of the
open question – a sharper condition, the ID stays (skill requirements, 7). The idle load's note says the servo is
detached at rest (3596f3f, D-17), the stalled case's note no longer that the ESP32 firmware should detach it.

## D-34 The circuit items waiting since D-18 and D-23 (2026-10-31)

They come with this renewal of M-1 and M-6 (D-25, item 9 h):

- Nano C9900187880 (main, smd, tht): `compliance.radio = "none"` – P-11 clears.
- esp32: `purpose.radio` with channels 1–13 (2412–2472 MHz), as on esp32tht – G-25 clears; U1's `i_core_min_a`
  0.04 A, `rth_ja_k_per_w` 184 and `tj_max_c` 150 of the AP2112K (Diodes datasheet), so that R-32 has its rows; R8/R9's
  notes say the simulated least current, 0.136 A; HINT.debounce names the firmware that debounces.
- esp32 and esp32tht: U1's `order` is Tinytronics SKU 002649, so the stand-in header no longer lands in an LCSC cart;
  U1's notes say the module's single CC pull-down (an A-to-C cable).
- esp32tht: R1/R2/R5's notes say "dimmed towards" the yellow-green (D-23).
- C439782 (main, tht, esp32tht): the polarity source no longer says "assumption" – compared at schematic create and in
  M-1.
