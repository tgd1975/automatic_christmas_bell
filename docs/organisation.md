# How the repository is organised

What each part of the repository is, who keeps it, how it changes – and which files a review of the documentation
may change and which it only reads. For everyone working on the bell's files; the [README](../README.md) is for those
who build and use it. The working rules for sessions are in [AGENTS.md](../AGENTS.md); edakit's working agreements
(handbook 11.4) come with its plugin.

## Kinds of content

| Kind | What it is | How it changes |
|---|---|---|
| **Documentation** | Text for the reader of the bell: how it is used, flashed, built and ordered, how the boards came about | Kept true to the design data, the firmware and the decisions; a review of the documentation corrects it |
| **Source** | Working material that the documentation and the work draw on: the decision log, the rules for sessions, notes and proposals | Only by the work it belongs to and the owner's word – never by a review of the documentation, which only reads it and reports what it finds |
| **Requirements** | What the circuit must do – the pipeline's inputs, said by the owner, never derived from what edakit generates (D-38) | Through the skill requirements: Claude drafts, only the owner accepts; a change voids the circuit's sign-offs |
| **Circuit** | Hardware graph, parts database, simulation scenarios, the schematic's arrangement | By the circuit designer (skills circuit-design, hardware-change, part-search), handed over to the layout in writing |
| **Layout** | Board files – outline, holes, placement, routing, pours, silkscreen – and the silkscreen artwork | By the PCB designer (skill pcb-round), in a session of its own (edakit handbook 11.4, agreement 12) |
| **Configuration** | Each board's edakit.toml: where the files are, release, order, cart, cost, the project's scripts | On the owner's word, as a decision |
| **Code** | The firmware, the build files, the tools and the git hook | On the owner's word (AGENTS.md) |
| **Generated** | Written by edakit or a script from the files above | Never by hand: the source changes, the command runs again |
| **Record** | Sign-offs, script stamps and stock snapshots, each bound to a hash or a date | Only by the step it records, committed with what it records |
| **History** | The state before edakit: the Fritzing drawing and the first implementation | Never – the circuit's origin, kept as it is |

## The repository, path by path

Every board is an edakit project of its own: main at the top, smd, tht, esp32 and esp32tht in `variants/<name>/`,
each with the same files. "Every board" below means `hardware/…` and `variants/<name>/hardware/…`.

| Path | Kind | Content |
|---|---|---|
| [README.md](../README.md) | Documentation | The start page, in German: use, position, flashing, the ESP32's web page, troubleshooting |
| [hardware/README.md](../hardware/README.md) | Documentation | The main board: how it came about, its files, the commands, what the checks found |
| [variants/README.md](../variants/README.md) | Documentation | The four variants side by side, their state and how to order them |
| [hardware/img/](../hardware/img/) | Documentation | Pictures of the main board for the READMEs: silkscreen, placement plan, routing |
| [docs/organisation.md](organisation.md) | Documentation | This page |
| [docs/decisions.md](decisions.md) | Source | The decision log D-1 …: the owner's decisions with reason and date; the notes of every release are taken from it (D-29) |
| [docs/edakit-gaps.md](edakit-gaps.md) | Source | Gaps in edakit found on the way, for the skill propose-feature – nothing of it is built here |
| [docs/requirements-review.md](requirements-review.md), [docs/requirements-proposal.toml](requirements-proposal.toml) | Source | Why the first requirements restated edakit, the owner's principle, and the new requirements – accepted, they replace D-32's files after the order (D-39); edakit does not read the proposal |
| [AGENTS.md](../AGENTS.md) | Source | The working rules and permissions for agents in this repository |
| [TODO.md](../TODO.md) | Source | What only the owner can do – account, payment, a release, hardware in hand –, one line per to-do with the chat that wrote it; ticked when done, deleted by that chat the next time it reads the file |
| `.claude/settings.json` | Source | Claude Code's project settings: the edakit plugin and its marketplace |
| [edakit.toml](../edakit.toml), `variants/<name>/edakit.toml` | Configuration | One per board; main's also publishes all five (D-29) |
| [hardware/requirements.toml](../hardware/requirements.toml), [hardware/requirements_nano.toml](../hardware/requirements_nano.toml), [variants/esp32/hardware/requirements.toml](../variants/esp32/hardware/requirements.toml) | Requirements | Shared by all five boards; the Nano boards' (main, smd, tht); the ESP32 boards' (esp32, esp32tht) – D-32 |
| `graph.toml`, `parts/`, `sim.json`, `schematic.toml` of every board | Circuit | The graph – the only source of the circuit –, one parts entry per LCSC number, the simulation scenarios, the schematic's blocks and notes |
| `boards/<name>.toml` of every board | Layout | The board file |
| [hardware/art/make_art.py](../hardware/art/make_art.py) | Layout | Draws the silkscreen artwork of all five boards – the script `kunst` in every edakit.toml (D-25) |
| `graph.json` of every board | Generated | The resolved graph (`edakit graph json --write`) |
| [hardware/schematic_main.svg](../hardware/schematic_main.svg), `variants/<name>/schematic_<name>.svg` | Generated | The schematic drawings, every connection a wire (`edakit schematic draw`, D-28) |
| `boards/<name>.geometry.json` of every board | Generated | The footprint geometry as placed in EasyEDA (`edakit pcb dump`) – in the layout hash |
| [hardware/art/](../hardware/art/) `*.svg` | Generated | The artwork, written by make_art.py (`edakit run kunst`) – in the layout hash |
| `firmware.json` of esp32 and esp32tht | Generated | The firmware contract: the ESP32's IO numbers from the graph (`edakit firmware`) |
| `signoff.json` of every board | Record | The sign-offs M-1, M-2, M-4, M-5, M-6 and the accepted warnings, each bound to the hash of its scope – written after the review, on the hash it checked |
| `scripts.lock` of every board | Record | The stamps of the project scripts (`edakit run`, `edakit scripts stamp`) |
| `stock.json` of every board | Record | Stock and prices at JLCPCB before a gate (`edakit stock`) |
| [docs/old/](old/) | History | IMPLEMENTIERUNG.md and the Fritzing files – the circuit's origin (decisions.md, header) |
| [src/firmware/](../src/firmware/), [platformio.ini](../platformio.ini) | Code | The Nano's firmware (main, smd, tht) and its PlatformIO build |
| [variants/esp32/firmware/](../variants/esp32/firmware/) | Code | The ESP32's firmware (esp32, esp32tht): timer, display, web page, its tests |
| [variants/esp32/hardware/lib/tdisplay_device.py](../variants/esp32/hardware/lib/tdisplay_device.py) | Code | Rebuilds the T-Display's symbol in the EasyEDA project library – the script `tdisplay`, on command only (D-13, D-25) |
| [Makefile](../Makefile) | Code | The Arduino CLI build, and `make publish` for the releases (D-29) |
| [tools/edakit](../tools/edakit) | Code | Finds edakit for the hook and the Makefile (D-25) |
| [.githooks/pre-commit](../.githooks/pre-commit) | Code | Runs each staged board's checks: check, sim, graph json – firmware and docs where the board's edakit.toml has them |
| [LIZENZ](../LIZENZ) | – | MIT licence |

The variants read two things from main's `hardware/`: the artwork and the shared requirements file. A change there
touches all five boards, and the pre-commit hook then runs the checks of all five.

Quoted values inside documentation: the values between `<!--edakit …-->` and `<!--/edakit-->` in
hardware/README.md come from the simulation and are filled in by `edakit docs --write` (`[docs]`, D-35); the
pre-commit hook fails when they differ.

## Outside the repository

| Where | What |
|---|---|
| EasyEDA project `christmas-bell` | Schematic and PCB of all five boards, one EasyEDA board each (D-15) – generated from the files here, so all of it may be deleted and generated again |
| `build/` | Gate runs and staged releases – ignored by git (D-22) |
| [GitHub releases](https://github.com/tgd1975/automatic_christmas_bell/releases) | The order files of every released state (`make publish`, D-22, D-29) |
| [edakit's issues](https://github.com/tgd1975/edakit/issues) | What the bell proposed to edakit, each traced in its decision (D-39: #97, #98) |

## A review of the documentation

- **Changes:** the files of kind documentation above – README.md, hardware/README.md, variants/README.md and this
  page – outside the quoted values. A new document in `docs/` is a source unless it is listed here as documentation.
- **Reads:** everything else, the design data above all: a claim that can be checked is checked against the graph,
  the parts entries, the simulation, the edakit.toml files, the firmware and the decisions. What is wrong in a source,
  in design data, in a record or in a generated file goes to the owner as a finding with its path and line; it is
  fixed in its place, by its role, on the owner's word.
- **Decisions are a record.** A review reads docs/decisions.md and never rewrites it, not even its wording.
- **Language:** README.md, AGENTS.md and TODO.md are German, everything else is English; a review keeps each file's language.
  A correct sentence stays as it is.
- **Not legal advice:** content on M-6, CE, RoHS or radio (D-36) says once that it is support, not legal advice.
