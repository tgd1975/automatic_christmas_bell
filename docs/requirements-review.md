# The bell's requirements: why they restate edakit, and what edakit should change (2026-11-01)

The owner's finding: R-1 (supply voltage) is self-evident and still complicated, it is what edakit is for; R-40
(brightness) is what a maker says at this point. This note looks at how the file came about, why, and what edakit can
change so that requirements, above all those written after the design, have the right size and scope. Nothing in the
bell or in edakit is changed by it.

## The principle (owner, 2026-11-01)

**Requirements are the pipeline's input.** They steer what the build pipeline must produce, so nothing edakit
generates or the circuit designer derives can be a requirement. That rules out a simulated value, a check result, the
derating, a part's limit, and a choice the graph made on its own. Requirements come from the customer-experience view:
"5 LEDs, two green, two yellow, one red, in a row in this order", "a servo must be driven". They need not be high
level: a maker's own detailed rule ("pin X never more than Y") is a requirement too. What makes one is who said it, not
how detailed it is. That holds in its strict form when a maker says from the start what they want. In projects that
were designed before their file (the bell, the tree), or where only a circuit exists (a Fritzing file), the
requirements must be reverse-engineered: from the circuit to what the thing is that is being built. That is harder,
and the result needs the owner's confirmation (proposal C).

## What happened

- **2026-10-31, 22:14:** inside the migration to edakit main (D-25, the whole bell on today's edakit), plan step 4.1
  of edakit (the bell as pilot of the requirements file) started the agent requirements-engineer for the inventory.
  It read the documents, the five sim.json, the parts entries and the gate protocols, ran `edakit sim --json` and
  counted which rows each candidate's pattern matches. It returned 13 needs, about 30 candidates for requirements and
  8 contradictions.
- **22:42:** decision round, items 11 to 16. Item 15 put all 19 drafts in one question, "Alle so annehmen
  (Empfohlen)", among questions on the order mark, the servo supply and the CE mark, shortly before the order.
  Accepted.
- **23:43:** commit 016ca2f (D-32, the bell's requirements file): 7 needs, 20 requirements in three files. No second
  opinion on the file was run (skill requirements, section 6).

## What the 20 requirements are

| Requirement | What it says | What it is | Already in edakit |
| --- | --- | --- | --- |
| R-1 (supply voltage) | U1's supply ≥ the module's minimum | derived | LIM.range, error on every board |
| R-2 (base load) | ≥ 100 mA from USB | derived from "runs from a power bank" (D-8) | i_min_a in sim.json → LIM.i |
| R-3 (LED on/off) | on 2–16 mA, off ≤ 10 µA | derived from N-2 | LIM.i; SIM.state from sim.json's criteria |
| R-4 (output pins) | ≤ 16 mA per pin | derived | LIM.i (gpio_i_max_a, derating) |
| R-5 (button levels) | above VIH, below VIL | derived | LVL.threshold |
| R-6 (derating) | 50 % power, 80 % current, 67 % voltage | derived | LIM.p, LIM.i, LIM.v |
| R-7 (stalled servo) | 0.7 A for ≤ 6 s, no damage | derived from N-5 (a jam does no harm) | scenario servo-stalled, M-1 |
| R-8 (servo at rest) | ≤ 10 mA from 2 s after the bell | firmware behaviour (detach) of N-5 | acceptance only |
| R-9 (no reset at servo start) | +5V ≥ minimum during the peak | derived from N-1 (the bell rings) | transient servo-start (D-33) |
| R-10 (USB only) | no second input, no battery, no mains | input: = N-3, N-6 and the purpose (D-16) | M-6 reads the purpose |
| R-11 (base-load resistors) | ≤ 0.25 W, < 60 °C | derived; "they get warm" (variants/README.md) | LIM.p; LIM.t with touch_c |
| R-12 (firmware pins) | pins as in locks.pins | derived | STRUCT.lock |
| R-20 (Nano 500 mA) | ≤ 500 mA during the bell | derived from the power source | i_max_a in sim.json → LIM.i |
| R-30 (ESP32 1 A) | ≤ 1 A | derived from the power source (D-17: at least 1 A) | i_max_a → LIM.i |
| R-31 (3.3 V pins) | no ESP32 pin above 3.4 V | derived | LIM.v, LIM.declared |
| R-32 (module regulator) | AP2112K ≤ 200 mA, ≤ 125 °C | derived | LIM.i, LIM.t |
| R-33 (radio band) | 2400–2483.5 MHz, ≤ 20 dBm | law | purpose.radio → LIM.band, LIM.eirp; M-6 |
| R-34 (strapping pins) | IO0, IO2, IO12, IO15 free | derived | LVL.boot with `strap` in the T-Display's entry |
| R-35 (servo on 3.3 V) | J1's signal 0/3.3 V moves the servo | input: a servo must be driven | acceptance |
| R-40 (brightness) | the five LEDs look about equally bright | input (owner's decision, D-23) | acceptance – the pattern |

Under the principle, 17 of the 20 are not requirements: eight restate catalog checks that are errors on every board,
R-33 restates the law that M-6 (regulatory review) checks from the purpose, and eight more are inputs rewritten as
circuit values. The real inputs are R-10, R-35 and R-40.

Meanwhile the inputs the documents state are missing:

- **README.md, "Hardware":** 5 LEDs (2 green, 2 yellow, 1 red) as a visual countdown; 2 buttons, start and reset; a
  9 g servo that strikes the bell; the Nano or the T-Display. **"Anwendung":** the bell is struck mechanically, no
  electronic sound.
- **The owner's decisions and wishes:** the LED row stays at the back edge, the board seen from above (D-9). smd:
  "smd LEDs, the pins as SMD if possible, the microcontroller on headers to solder yourself, the capacitor only if it
  does not force the more expensive assembly" (D-11). esp32: the T-Display, "the smaller variant" (D-13), with
  yellow-green LEDs instead of green (D-14). esp32tht: "eine Version mit ESP32 und Pins zum selber Löten" (D-23). The
  web page on the home Wi-Fi (D-17).

The inventory had the variants' wishes as N-8 and N-9; they did not reach the file.

## Why

1. **The inventory starts from the design data.** The agent's prompt (agents/requirements-engineer.md, "Sources")
   names sim.json's limits as "often a requirement whose evidence exists already", the protocol's rows as "what a
   rows pattern can match", and `edakit sim --json`. In a project designed before its file, the documents are mostly
   decisions and data, so the candidates became what the pipeline produces: from output to sentence instead of from
   input to evidence.
2. **The rule for design choices is the wrong one.** Agent and skill say "a design choice is no requirement (an
   AMS1117 makes the 3.3 V)". That took out the inputs that look like a design: the LED colours, two buttons, the
   module on headers. Yet derived values stayed in, because they look like requirements. The question that separates
   the two is who decided, not what it looks like.
3. **edakit has no baseline.** Neither handbook 3.6, nor the skill, nor the agent says that the catalog's checks hold
   without a requirement.
4. **The format asks for engineering sentences.** "One testable sentence with quantity, limit and condition"
   (handbook 3.6, 10.4, skill section 2), and the handbook's own example "draws at most 500 mA from J1 at 4.75 to
   5.25 V". So the agent derives a number and a condition when the maker gave neither.
5. **The gate rewards restating.** A `must` without passing evidence blocks the release, and the skill says "look for
   existing evidence first – it is often there". The cheapest requirement with evidence is one that matches rows that
   exist already.
6. **The round allowed a bulk yes.** The skill lets "several that need no discussion" go into one item. Nobody asked
   per draft who had said it. The second opinion did not run, and its checklist has no item for derived entries
   either.

What it costs: the file counts in the circuit hash. Every change voids M-1 (circuit review) and M-6 on all five
boards, and their notes must list the IDs they found met. The 20 entries hide the few that matter, and the inputs that
would steer a redesign are not there. And plan step 4.5 of edakit makes the file required for every project once the
bell and the tree have one, so the bell's file becomes the example that others copy.

## Proposals for edakit

- **A (requirements are inputs).** Handbook 3.6, skill requirements and the agent get the principle above. A
  requirement is what someone involved states: the maker, a user, a standard or law the maker chooses (USB 2.0, a
  market). Nothing edakit generates or the circuit designer derives is one. "A design choice is no requirement"
  becomes "a choice the maker made is a requirement; a choice the designer or edakit made is not". Every requirement
  says who stated it (`source`: a document, an owner's decision, the user with a date).
- **B (the maker's level of detail).** The text stays as the maker gives it, high level ("a servo must be driven") or
  detailed ("pin X never above Y"). The agent asks back only where a sentence cannot be decided: vague words, or a
  missing condition the maker must choose. It does not add derived numbers. Circuit values that follow (100 mA,
  0.7 A, 3.8 V) belong to the designer, in sim.json and the graph's notes with the requirement's ID. They reach the
  requirement as evidence (`rows`). The example in 10.4 changes with it: led-bar's R-1 becomes "runs from a laptop's
  USB port with all eight LEDs on".
- **C (forward and reverse).** Forward, a maker says from the start what they want: the requirements are what they
  state. Reverse, only a circuit exists (a Fritzing file, a finished project like the bell): the agent reads first
  what people said (README, the owner's decisions), then infers from the circuit what the thing is – what a person
  sees, presses, plugs in, hears. The test: would anyone notice if it were different? LED colours yes, the 330 Ω of a
  series resistor no, the derating never. An inferred candidate says so and waits for the owner's yes. In both cases
  the design data serve only as evidence.
- **D (baseline visible).** The agent lists what edakit checks on every board as "already checked by edakit", not as
  candidates. Section 11 of the protocol starts with one line for it: the catalog checks of stages G and E, passed or
  failed. That answers "what do I have edakit for?" in the protocol itself.
- **E (a check for derived entries).** DOCS.derived, a warning that also fires on drafts: a requirement whose
  `source` and `from` name only edakit's data (sim.json, parts entries, the graph, a protocol, a datasheet) and no
  person, document, need or chosen standard is derived, not stated. An inferred candidate (C, reverse) names the graph
  too, but it is a draft, and a draft only warns; once the owner confirms it, its `source` names the owner. The fields
  exist today, so the check needs nothing new from the simulation.
- **F (the round).** As today; each draft only names its source in a word (README, D-9, inferred).
- **G (pilot first).** Plan step 4.5 (the file required for every project) waits for A to F and the bell's rewritten
  file.

## The bell's file under the principle

The proposal is docs/requirements-proposal.toml: 10 needs, 11 requirements, every one an input with its source. The
owner reviewed it on 2026-11-01 (D-38): the level fits, the inferred points are confirmed, and the variants are one
requirement per assembly (SMD, THT) for both modules. The 17 derived entries of D-32 are dropped there with their
reason, and their numbers stay in sim.json and the graph's notes, where the designer keeps them.

A changed file before the order means: `cart prepare` compares the release's circuit hash with today's
(docs/edakit-gaps.md, 1), so all five boards would need new gate runs, and M-1 and M-6 would have to be signed again.
The boards themselves do not change.
