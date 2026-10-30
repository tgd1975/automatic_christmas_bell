# Board variants

Three variants of the Christmas bell's carrier board, next to the released main board ([../hardware](../hardware)). Each
one is an edakit project of its own: a folder here with its own edakit.toml, board and schematic file, hardware graph,
parts database, simulation config and sign-offs. All four share the EasyEDA project `christmas-bell`, one EasyEDA board
each (decision D-15 in [../docs/decisions.md](../docs/decisions.md)).

| | [smd](smd) | [tht](tht) | [esp32](esp32) |
|---|---|---|---|
| Decision | D-11 | D-12 | D-13, D-14 |
| Controller | Arduino Nano on 2 × 1×15 female headers | Arduino Nano on 2 × 1×15 female headers | LILYGO T-Display V1.1 (ESP32, 1.14″ TFT) on 2 × 1×12 female headers |
| LEDs | 0805: red, 2 × yellow, 2 × emerald green | 5 mm THT, as on the main board | 0805: red, 2 × yellow, 2 × yellow-green |
| Series resistors | 330 Ω 0805 | 330 Ω ¼ W THT | 100 Ω 0805 |
| Buttons | 6 × 6 SMD | 6 × 6 THT | 6 × 6 SMD, switching 3V3 |
| C1 1000 µF / 16 V | SMD can | THT radial | SMD can |
| Servo header J1 | SMD 1×3 | THT 1×3 | SMD 1×3 |
| Base load R8 ∥ R9 | 2 × 100 Ω 2512 | 2 × 100 Ω 1 W THT | 2 × 100 Ω 2512 |
| Assembly | JLCPCB Economic, top side: everything but the female headers | none – a bare board, everything hand-soldered | JLCPCB Economic, top side: everything but the female headers |
| EasyEDA board | `smd` | `tht` | `esp32` |

Board 85 × 56 mm with four M3 holes for all of them, like the main board. The circuit of smd and tht is the main
board's; esp32 replaces the Nano and follows from 3.3 V logic: the buttons switch 3V3, the LEDs are driven from
3.3 V outputs.

## Commands

Every edakit command takes the variant's config:

```bash
edakit check --config variants/esp32/edakit.toml       # rules
edakit sim --config variants/esp32/edakit.toml         # ngspice over all scenarios
edakit schematic draw --config variants/esp32/edakit.toml   # the schematic as SVG, no EasyEDA
```

The drawn schematics are committed next to each config: [smd/schematic_smd.svg](smd/schematic_smd.svg),
[tht/schematic_tht.svg](tht/schematic_tht.svg), [esp32/schematic_esp32.svg](esp32/schematic_esp32.svg).

Through EasyEDA the order is the one of the main board (../hardware/README.md), each with `--config`:
`schematic create --save`, `schematic layout --save`, `pcb parts --write`, `pcb dump`, `pcb plan`, `pcb apply`,
`route all`, `silk apply`, `gate --easyeda`.

## The T-Display in EasyEDA

The T-Display is neither in EasyEDA's library nor at LCSC, and a device created through EasyEDA's API cannot be placed
in the local client. The EasyEDA device of U1 is therefore a stand-in, the 2×12 female header C18722937, whose symbol
and footprint copies in the project are rebuilt into the T-Display's by
[esp32/hardware/lib/tdisplay_device.py](esp32/hardware/lib/tdisplay_device.py) (D-13). Order on a fresh EasyEDA
project: `schematic create` (places the header, the copies appear in the project), the script, `schematic create`
again (now with the T-Display's pins), then as usual. The parts entry
[esp32/hardware/parts/C18722937.json](esp32/hardware/parts/C18722937.json) describes the T-Display, not the header.

**Before ordering the ESP32 board, measure the module:** two rows of 12 pins, pitch 2.54 mm, rows 22.86 mm apart,
pin 1 (5V) and pin 13 (3V3) at the USB end.

## Building and using

- **ESP32:** solder the two 1×12 female headers with the T-Display plugged in, so they stand straight. Plug the module
  in with USB-C at the board edge and the display up – the pin field is symmetric, turned round it shorts 5V to GND
  (silkscreen "5V" next to U1.1). The module's USB-C has a CC pull-down on one line only: power it from a USB charger
  or power bank (at least 1 A, D-17) with an A-to-C cable, or turn a C-to-C plug over if it stays dark. No LiPo at the
  module's battery connector: the base load would drain it (D-13).
- **SMD and ESP32:** the SMD servo header J1 holds less sideways pull than a through-hole one – plug the servo
  straight and tie its cable to the frame.
- **THT:** the button holes are 1.3 mm (library footprint) – press each button flat while soldering its first leg.
  5 mm LEDs: flat side and short leg to the right.

## The ESP32 firmware

[esp32/firmware](esp32/firmware) is a PlatformIO project (D-17): the countdown of the Nano, plus the display and a
web page – status, time to ding, start, pause, stop and the timer.

```bash
cd variants/esp32/firmware
pio run -e tdisplay -t upload   # build and flash (USB-C of the T-Display)
pio test -e native              # the countdown logic lib/BellTimer on the computer
```

- **First start:** the bell opens the hotspot `Glocke-XXXX`; name and password are on the display. Join it with a
  phone, the setup page opens (otherwise http://192.168.4.1), choose the home network and enter its password. The
  bell joins it and shows its address – http://glocke.local. A network it cannot reach within 30 s opens the hotspot
  again.
- **Buttons:**

  | Button | Does |
  |---|---|
  | start | countdown; while paused: go on |
  | reset | stop |
  | start held, then reset | ring now |
  | reset held 3 s, released | Wi-Fi on/off (green LEDs while held) |
  | reset held 10 s, released | forget the home network, the hotspot opens (red LED while held) |

- **Radio:** channels 1–13 only (country DE, 802.11d off), no Bluetooth (D-13 "Radio").
- **Before the module leaves the house** (gift, repair, e-waste): erase its flash, `pio run -e tdisplay -t erase` –
  the home Wi-Fi password is stored in it.
- **Servo:** an analog one (SG90 type). The firmware detaches it at rest so that a jam cannot load the supply; a
  digital servo would keep holding without pulses.
- Not yet tried on a module: flash it, then check the buttons, the LEDs, the servo, the page and the hotspot – a
  Wi-Fi analyser app shows `Glocke-XXXX` on a channel 1–13 with WPA2 – and that the module is marked T-DISPLAY V1.1
  (M-4).

## Status (2026-10-30)

| | smd | tht | esp32 |
|---|---|---|---|
| check, hints, sim | 0 errors, 1211 checks | 0 errors, 1211 checks | 0 errors, 1436 checks |
| schematics in EasyEDA = graph | yes | yes | yes |
| PCB routed | 15 nets, 3 vias | 15 nets, 1 via | 16 nets, 7 vias |
| M-1 circuit review | OK (1ed944d2…) | OK (5ddc2553…) | OK (3f7cec3d…) |
| M-5 layout review | OK on run 20261026-123018 (fab 4e79e5c0…) | OK on run 20261026-123036 (fab 441ab22c…) | OK on run 20261026-123051 (fab f2962d76…) |
| M-6 regulatory review | OK, private (1ed944d2…) | OK, private (5ddc2553…) | OK, private, Wi-Fi (3f7cec3d…) |
| release gate | **RELEASED**, run 20261030-232631 | **RELEASED**, run 20261030-232650 | **RELEASED**, run 20261030-232707 |

The hashes are the ones the reviewers signed. The move to edakit's split config (commit a1a1d80) re-stamped the
layout hashes without a change of content ("rehashed" in each signoff.json). The purpose `private` in each graph
(D-16) changed the circuit hashes: M-1 was confirmed again, M-6 – the regulatory review, required for every release
since edakit ef1183f, support and not legal advice – signed for the new ones. On esp32 both were renewed for Wi-Fi
(D-17): M-6 holds with the radio settings of D-13 (channels 1–13, no Bluetooth) and USB power without a cell, M-1
with the module's higher current and a USB source of at least 1 A. The Nanos are at hand, so edakit's warning P-5 (no
supplier) is accepted (D-19). M-5 is bound to the manufacturing files its reviewer checked (D-20).

The release, on 2026-10-30 with edakit b36a6d0:

1. *Design → Import Changes* opened once on each of the PCBs `smd`, `tht` and `esp32` (it showed no changes) – the
   EasyEDA DRC is clean since (L-3).
2. Before each `edakit gate --easyeda --config variants/<v>/edakit.toml` all EasyEDA tabs were closed: with several
   boards in one project, EasyEDA's BOM tool lists the parts of every open schematic tab, and other boards' tabs make
   F-1 fail.
3. L-17 tells edakit's print from the footprints' by the silk files `silk apply` keeps, so `edakit silk apply` ran
   again on every board. The manufacturing files came out the same as the reviewed runs' (fab hashes above), so M-5
   counts.
4. The footprints' own print on the buttons' and C1's pads and the Nano's print beyond the board edge are accepted
   warnings (D-21).

The release runs are archived in git (`build/release/<run>/` of each variant). To order: the edakit release skill,
`edakit release verify` on the files about to be uploaded. At JLCPCB choose "Order Number: Specify Position" – each
board has `JLCJLCJLCJLC` under the module. Before ordering the ESP32 board, measure the T-Display (above).

## Open

- ESP32 firmware: built and its countdown logic tested on the computer, not yet on a module (see above).
- smd, cosmetic: a tented GND via sits on LED4's silkscreen outline at (37.82, 48.00); a keep-out
  `rect = [37.2, 46.6, 38.4, 49.4]` would move it (then route, silk, gate and M-5 again).
- The EasyEDA project library still holds a device "zz-test-copy-nano" from the T-Display experiments; it is used
  nowhere and can be deleted in EasyEDA (Library → Project).
