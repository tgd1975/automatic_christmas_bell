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
  (silkscreen "5V" next to U1.1). The module's USB-C has a CC pull-down on one line only: power it from a USB-A port
  with an A-to-C cable, or turn a C-to-C plug over if it stays dark. No LiPo at the module's battery connector: the
  base load would drain it (D-13).
- **SMD and ESP32:** the SMD servo header J1 holds less sideways pull than a through-hole one – plug the servo
  straight and tie its cable to the frame.
- **THT:** the button holes are 1.3 mm (library footprint) – press each button flat while soldering its first leg.
  5 mm LEDs: flat side and short leg to the right.

## Status (2026-10-26)

| | smd | tht | esp32 |
|---|---|---|---|
| check, hints, sim | 0 errors, 1186 checks | 0 errors, 1186 checks | 0 errors, 1412 checks |
| schematics in EasyEDA = graph | yes | yes | yes |
| PCB routed | 15 nets, 3 vias | 15 nets, 1 via | 16 nets, 7 vias |
| M-1 circuit review | OK (1ed944d2…) | OK (5ddc2553…) | OK (6224647f…) |
| M-5 layout review | OK (67c811e0…) | OK (d0021b33…) | OK (4e836f8e…) |
| M-6 regulatory review | OK, private (1ed944d2…) | OK, private (5ddc2553…) | OK, private, radio off (6224647f…) |
| last gate run with EasyEDA | 20261026-123018 | 20261026-123036 | 20261026-123051 |
| release gate | L-3 open | L-3 open | L-3 open |

The hashes are the ones the reviewers signed. The move to edakit's split config (commit a1a1d80) re-stamped the
layout hashes without a change of content ("rehashed" in each signoff.json). The purpose `private` in each graph
(D-16) changed the circuit hashes: M-1 was confirmed again, M-6 – the regulatory review, required for every release
since edakit ef1183f – signed for the new ones. On esp32 it holds only while the firmware keeps Wi-Fi and Bluetooth
off and the module runs from USB without a cell (D-13). The offline gate (runs 20261026-145535 of smd and tht,
20261026-145638 of esp32) counts M-1, M-5 and M-6. One thing is left:

- **L-3** (EasyEDA DRC without findings): EasyEDA reports "Netlist Error – Import Changes" for parts freshly placed in
  a schematic until its import view was opened once in the GUI (edakit handbook 7.3). That needs a person at EasyEDA:

1. In EasyEDA, for each of the PCBs `smd`, `tht` and `esp32`: open the PCB, *Design → Import Changes*, it shows "no
   changes", close.
2. Close all other tabs, then per variant `edakit gate --easyeda --config variants/<v>/edakit.toml`. With several
   boards in one project, EasyEDA's BOM tool lists the parts of every open schematic tab – other boards' tabs make
   F-1 fail.
3. The reviews hold only for the files they checked: compare each new run's `fab/<v>/gerber/` with the run in the
   table, ignoring the `G04` header lines, e.g.
   `for f in <old run>/fab/esp32/gerber/*; do diff -q <(grep -v '^G04' "$f") <(grep -v '^G04' "<new run>/fab/esp32/gerber/${f##*/}"); done`.
   Any difference – above all at U1's holes on esp32 – needs the reviewer again.
4. RELEASED: archive the run folder (`git add -f`), order from it (edakit release skill). At JLCPCB choose "Order
   Number: Specify Position" – each board has `JLCJLCJLCJLC` under the module.

## Open

- ESP32 firmware: src/firmware is written for the Nano. The pins of the ESP32 board are fixed in `checks.pin_locks` of
  the graph [esp32/hardware/graph.json](esp32/hardware/graph.json) (LEDs IO27/IO26/IO25/IO33/IO32, servo IO13, buttons
  IO38/IO37); requirements from the reviews in D-13 – plain inputs, debounce, the servo detached at rest (M-1), Wi-Fi
  and Bluetooth off (M-6).
- smd, cosmetic: a tented GND via sits on LED4's silkscreen outline at (37.82, 48.00); a keep-out
  `rect = [37.2, 46.6, 38.4, 49.4]` would move it (then route, silk, gate and M-5 again).
- The EasyEDA project library still holds a device "zz-test-copy-nano" from the T-Display experiments; it is used
  nowhere and can be deleted in EasyEDA (Library → Project).
