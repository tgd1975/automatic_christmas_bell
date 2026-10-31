# Board variants

Four variants of the Christmas bell's carrier board, next to the released main board ([../hardware](../hardware)). Each
one is an edakit project of its own: a folder here with its own edakit.toml, board and schematic file, hardware graph,
parts database, simulation config and sign-offs. All five share the EasyEDA project `christmas-bell`, one EasyEDA board
each (decision D-15 in [../docs/decisions.md](../docs/decisions.md)).

| | [smd](smd) | [tht](tht) | [esp32](esp32) | [esp32tht](esp32tht) |
|---|---|---|---|---|
| Decision | D-11 | D-12 | D-13, D-14 | D-23 |
| Controller | Arduino Nano on 2 × 1×15 female headers | Arduino Nano on 2 × 1×15 female headers | LILYGO T-Display V1.1 (ESP32, 1.14″ TFT) on 2 × 1×12 female headers | as esp32 |
| LEDs | 0805: red, 2 × yellow, 2 × emerald green | 5 mm THT, as on the main board | 0805: red, 2 × yellow, 2 × yellow-green | 5 mm THT: red, 2 × yellow, 2 × yellow-green |
| Series resistors | 330 Ω 0805 | 330 Ω ¼ W THT | 100 Ω 0805 | 100 Ω ¼ W THT |
| Buttons | 6 × 6 SMD | 6 × 6 THT | 6 × 6 SMD, switching 3V3 | 6 × 6 THT, switching 3V3 |
| C1 1000 µF / 16 V | SMD can | THT radial | SMD can | THT radial |
| Servo header J1 | SMD 1×3 | THT 1×3 | SMD 1×3 | THT 1×3 |
| Base load R8 ∥ R9 | 2 × 100 Ω 2512 | 2 × 100 Ω 1 W THT | 2 × 100 Ω 2512 | 2 × 100 Ω 1 W THT |
| Assembly | JLCPCB Economic, top side: everything but the female headers | none – a bare board, everything hand-soldered | JLCPCB Economic, top side: everything but the female headers | none – a bare board, everything hand-soldered |
| Firmware | [../src/firmware](../src/firmware) | [../src/firmware](../src/firmware) | [esp32/firmware](esp32/firmware) | [esp32/firmware](esp32/firmware), unchanged |
| EasyEDA board | `smd` | `tht` | `esp32` | `esp32tht` |

Board 85 × 56 mm with four M3 holes for all of them, like the main board. The circuit of smd and tht is the main
board's; esp32 replaces the Nano and follows from 3.3 V logic: the buttons switch 3V3, the LEDs are driven from
3.3 V outputs. esp32tht is esp32's circuit with tht's parts. All five are in the form of edakit's restructuring
(edakit main 5196c6f and later): esp32tht from the start (D-23), the other four by `edakit convert` (D-24).

## Commands

Every edakit command takes the variant's config:

```bash
edakit check --config variants/esp32/edakit.toml       # rules
edakit sim --config variants/esp32/edakit.toml         # ngspice over all scenarios
edakit schematic draw --config variants/esp32/edakit.toml   # the schematic as SVG, no EasyEDA
```

The drawn schematics – every connection a wire (D-28) – are committed next to each config:
[smd/schematic_smd.svg](smd/schematic_smd.svg), [tht/schematic_tht.svg](tht/schematic_tht.svg),
[esp32/schematic_esp32.svg](esp32/schematic_esp32.svg), [esp32tht/schematic_esp32tht.svg](esp32tht/schematic_esp32tht.svg);
the main board's is [../hardware/schematic_main.svg](../hardware/schematic_main.svg).

Through EasyEDA the order is the one of the main board (../hardware/README.md), each with `--config`:
`schematic create --save`, `schematic layout --save`, `pcb parts --write`, `pcb dump`, `pcb plan`, `pcb apply`,
`route all`, `silk apply`, `gate --easyeda`.

## The T-Display in EasyEDA

The T-Display is neither in EasyEDA's library nor at LCSC, and a device created through EasyEDA's API cannot be placed
in the local client. The EasyEDA device of U1 is therefore a stand-in, the 2×12 female header C18722937, whose project
copies become the T-Display's (D-13). The **footprint** is data in the parts entry since D-30 – `footprint_data` in
[esp32/hardware/parts/C18722937.json](esp32/hardware/parts/C18722937.json) and the same in esp32tht's entry: 24 pads,
their shape, size and hole, the outline, the USB box and the two texts, checked by PARTS.footprint and against the
dump by SYNC.footprint; `edakit part build C18722937 --config variants/esp32/edakit.toml --write` builds the copy from
it. The **symbol** stays the script's: `edakit run tdisplay --config variants/esp32/edakit.toml` runs
[esp32/hardware/lib/tdisplay_device.py](esp32/hardware/lib/tdisplay_device.py) `symbol` under the EasyEDA claim.
Order on a fresh EasyEDA project: `schematic create` (places the header, the copies appear in the project),
`part build --write` and `run tdisplay`, `schematic create` and `schematic layout` again (now with the T-Display's
pins and pads), then as usual. The parts entry describes the T-Display, not the header.

**Before ordering an ESP32 board (esp32, esp32tht), measure the module:** two rows of 12 pins, pitch 2.54 mm, rows 22.86 mm apart,
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
- **ESP32 THT:** as ESP32 and THT together. Low parts first – the resistors lying flat, then LEDs (flat side and short
  leg to the right), buttons, J1, C1 ("+" to the left), the two female headers last with the T-Display plugged in.
  R8 and R9 get warm (0.25 W each): let them stand 1–2 mm above the board. The firmware is esp32's.

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

## Status (2026-11-01)

All five boards are on edakit main (bc44fa7) and released again (D-25 to D-36): graph as TOML, requirements files,
the T-Display's footprint as data, the order form as keys, no order-number placeholder.

| | main | smd | tht | esp32 | esp32tht |
|---|---|---|---|---|---|
| check, sim, graph json, scripts | green | green | green | green (LIM.p accepted, D-26) | green |
| requirements | 7 needs, 14 requirements | as main | as main | 8 needs, 19 requirements | as esp32 |
| M-1 circuit review (state) | OK (861f9237…) | OK (a8a4db48…) | OK (79642329…) | OK (6ca3b2e3…) | OK (0bd61e5f…) |
| M-6 regulatory review (electrical) | OK, private (1a518dc3…) | OK, private (4024ed6b…) | OK, private (db32b8ea…) | OK, private, Wi-Fi, D-36 (1beca6c8…) | OK, private, Wi-Fi, D-36 (668320d8…) |
| M-5 layout review (fab) | OK on run 20261101-004618 (a9b42ee5…) | OK on run 20261101-003727 (d1875bf7…) | OK on run 20261101-003912 (197fe082…) | OK on run 20261101-004304 (fe891ad5…) | OK on run 20261101-004536 (02441da3…) |
| release gate | **RELEASED**, run 20261101-005804 | **RELEASED**, run 20261101-005512 | **RELEASED**, run 20261101-005606 | **RELEASED**, run 20261101-005656 | **RELEASED**, run 20261101-005734 |

The hashes are the ones the reviewers signed; M-1, M-6 and M-5 by edakit's agents electrical-reviewer,
regulatory-reviewer and pcb-reviewer in their own sessions. Against the releases of 2026-10-30/31 the manufacturing
files differ only by the removed `JLCJLCJLCJLC` on smd, tht and esp32 and by the new order form `order.json`
(`edakit fab diff`). M-6 is support, not legal advice: no claim to correctness, nothing legally guaranteed.

How it went: `silk apply` took the placeholder off by itself (it was in its memo of what it printed); on esp32 and
esp32tht `pcb dump` measured U1's pads anew and SYNC.footprint passed, so nothing was rebuilt – `pcb apply` and
`route save/reload/drc` put the dumped parts back (DRC 0). Before each `edakit gate --easyeda` every EasyEDA tab was
closed (the BOM tool lists the parts of every open schematic tab). The footprints' own print and main's copper-free
spot stay accepted warnings (D-21).

The release runs are build output and stay out of git (D-22); `edakit release current --config …` names the current
one. **To order:** the skill cart puts each board into JLCPCB's cart from the keys of its edakit.toml (`[order]`
mark "Remove Mark", `[cart]` Austria, DHL Express) and stops at the cart – `edakit cart prepare --config …` accepts
all five releases. `make publish` publishes the order files as a GitHub pre-release first (`edakit release publish`,
D-29); once a board of that state has been built and works, `make publish-built TAG=<tag>`. Before ordering an ESP32
board, measure the T-Display and look for its CE mark (above, D-36). Check JLCPCB's preview (M-2).

## Open

- ESP32 firmware: built and its countdown logic tested on the computer, not yet on a module (see above).
- smd, cosmetic: a tented GND via sits on LED4's silkscreen outline at (37.82, 48.00); a keep-out
  `rect = [37.2, 46.6, 38.4, 49.4]` would move it (then route, silk, gate and M-5 again).
- The EasyEDA project library still holds a device "zz-test-copy-nano" from the T-Display experiments; it is used
  nowhere and can be deleted in EasyEDA (Library → Project).
