# Board variants

Three variants of the Christmas bell's carrier board, next to the released main board ([../hardware](../hardware)).
Each one is an edakit project of its own: a folder here with its own edakit.toml, hardware graph, parts database,
simulation config and sign-offs. All four share the EasyEDA project `christmas-bell`, one EasyEDA board each
(decision D-15 in [../docs/decisions.md](../docs/decisions.md)).

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
  (silkscreen "5V" next to U1.1). The module's USB-C has a CC pull-down on one line only: power it from a USB-A port
  with an A-to-C cable, or turn a C-to-C plug over if it stays dark.
- **SMD and ESP32:** the SMD servo header J1 holds less sideways pull than a through-hole one – plug the servo
  straight and tie its cable to the frame.
- **THT:** the button holes are 1.3 mm (library footprint) – press each button flat while soldering its first leg.
  5 mm LEDs: flat side and short leg to the right.

## Open

- ESP32 firmware: src/firmware is written for the Nano. The pins of the ESP32 board are fixed in
  `[checks] pin_locks` of [esp32/edakit.toml](esp32/edakit.toml) (LEDs IO27/IO26/IO25/IO33/IO32, servo IO13,
  buttons IO38/IO37).
