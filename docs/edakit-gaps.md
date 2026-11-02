# Gaps in edakit found while moving the bell to edakit main (D-25, 2026-10-31/11-01)

Collected for the skill propose-feature – nothing of it is built in this project. Each with where it showed and what
the project does meanwhile.

1. **`cart prepare` ignores `rehashed`.** `edakit convert` (D-24) and `edakit graph convert` (D-25) change the circuit
   hash and carry the sign-offs over (`rehashed`), but `cart prepare` compares the release run's circuit hash with
   today's and refuses ("the circuit changed since run …"). A release whose files are unchanged cannot be ordered
   through the skill cart after a format conversion. Meanwhile: a new gate run.
2. **edakit is not on the PATH, and the plugin's path changes with every version.** A hook and a Makefile need their
   own locator (tools/edakit: `$EDAKIT`, PATH, `installed_plugins.json`). A shipped hook template or `edakit hook
   install` would save every project from writing one.
   Closed for the hook by edakit 1.0.11 (2026-11-02): `edakit hook install` writes edakit's block, which finds edakit
   itself; the hook has no locator of its own any more. The Makefile keeps tools/edakit.
3. **`part footprint` from a dump older than footprint data** takes the pad places only – shape, size and hole are
   missing (PARTS.footprint), and only the project's script knew them (D-30). It could read them from the copy's
   library footprint in EasyEDA, or `pcb dump` could measure them for every part, not only for those with data.
4. **`[firmware]` for a module whose pin names are not its firmware's names.** The Nano's symbol names its pins by
   ATmega port (PD2), the firmware by Arduino number (D2); no `gpio` regex maps one to the other. Now that a pin has
   `print` (W.5, "D2", "~D3"), `gpio` could read the print instead of the name. Meanwhile: `locks.pins` only (D-35).
5. **`[docs]` blocks in a file shared by several configurations.** variants/README.md quotes values of four boards;
   a block has no configuration of its own, so every variant would check every block against its own graph (D-35).
   A block could name its configuration (`<!--edakit esp32: graph:R1.value-->`).
6. **A project-library change shared by boards of one EasyEDA project.** `tdisplay_device.py symbol` changes the
   copy esp32 and esp32tht both use; edakit models it per board (`project-library:<b>`), so esp32tht cannot register
   it. A data name for the project's library as a whole would fit.
7. **Distributors.** The owner buys at Berrybase, Bürklin, Reichelt, RS and LCSC; edakit knows lcsc, rs, farnell,
   mouser, digikey, reichelt – Berrybase and Bürklin are missing, and Tinytronics (the T-Display) too.
8. **`edakit stock` on a bare board** (`[release] assembly = { sides = [] }`) prints "standard PCBA … two sides";
   nothing is asked, so only the wording is off.
9. **The purpose knows a market, not a country.** M-6 of 2026-11-01 found Austria's FMaG 2016 § 24 stricter than the
   German frame of handbook 15 (D-36): a country in `purpose` beside `market`, and Austrian sources in handbook 15.
10. **A plug-in transient against a surge rating** (M-1 note 1): C1's inrush through the module's diode on every
    plug-in (~9 A for ~0.5 ms) could be a transient run checked against a surge value (`i_fsm_a`, `i2t`) in the
    diode's or module's entry.
11. **`verified.open` items the entry already holds** (M-1 note 3): a check that names an open point whose fact the
    entry has meanwhile (a lead diameter, a pad assignment).
12. **A settled `verified.open` item voids the sign-offs.** The open item "measure the module" of the T-Display's entry
    is settled by the owner (D-37), but removing it changes the circuit hash and voids M-1, M-6 and the release of
    esp32 and esp32tht. A way to close an open item without a new review – a note the gate shows – would fit.

Not gaps, for edakit's own documents: its README says the circuit as TOML has no real project yet and "the Christmas
bell keeps its JSON graph", and that own footprints as data are "built offline only" – the bell has both since D-25
and D-30.
10. **Requirements written from edakit's output, not from the inputs.** The bell's file (D-32) has 20
    requirements; 17 are derived – catalog checks (R-1 supply voltage, R-6 derating, …), M-6, or the maker's wishes
    rewritten as circuit values – while the README's inputs (5 LEDs, 2 green, 2 yellow, 1 red; two buttons; a servo
    that strikes the bell) and the variants' wishes are missing. The owner's principle: requirements steer the
    pipeline, nothing edakit generates can be one. Causes and proposals A to G: docs/requirements-review.md;
    sent as edakit #97 (feature) and #98 (rule DOCS.derived).
