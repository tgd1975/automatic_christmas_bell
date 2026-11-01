# The bell's requirements: why they restate edakit, and what edakit should change (2026-11-01)

The owner's finding: R-1 (supply voltage) is self-evident and still complicated, it is what edakit is for; R-40
(brightness) is what a maker says at this point. This note looks at how the file came about, why, and what edakit can
change so that requirements, above all those written after the design, have the right size and scope. Nothing in the
bell or in edakit is changed by it.

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
|---|---|---|---|
| R-1 (supply voltage) | U1's supply ≥ the module's minimum | baseline | LIM.range, error on every board |
| R-2 (base load) | ≥ 100 mA from USB | the maker's wish N-4 (power bank stays on), technical | i_min_a in sim.json → LIM.i |
| R-3 (LED on/off) | on 2–16 mA, off ≤ 10 µA | half baseline, half wish (N-2) | LIM.i; SIM.state from sim.json's criteria |
| R-4 (output pins) | ≤ 16 mA per pin | baseline | LIM.i (gpio_i_max_a, derating) |
| R-5 (button levels) | above VIH, below VIL | baseline | LVL.threshold |
| R-6 (derating) | 50 % power, 80 % current, 67 % voltage | baseline | LIM.p, LIM.i, LIM.v |
| R-7 (stalled servo) | 0.7 A for ≤ 6 s, no damage | wish N-5 (a jam does no harm), technical | scenario servo-stalled, M-1 |
| R-8 (servo at rest) | ≤ 10 mA from 2 s after the bell | firmware behaviour (detach) of N-5 | acceptance only |
| R-9 (no reset at servo start) | +5V ≥ minimum during the peak | wish (the bell rings, nothing restarts) | transient servo-start (D-33) |
| R-10 (USB only) | no second input, no battery, no mains | non-goal, = N-3 and N-6 and the purpose | M-6 reads the purpose |
| R-11 (base-load resistors) | ≤ 0.25 W, < 60 °C | power part baseline, touch part a wish | LIM.p; LIM.t with touch_c |
| R-12 (firmware pins) | pins as in locks.pins | baseline | STRUCT.lock |
| R-20 (Nano 500 mA) | ≤ 500 mA during the bell | wish (an ordinary power bank), technical | i_max_a in sim.json → LIM.i |
| R-30 (ESP32 1 A) | ≤ 1 A | use condition (a 1 A source) | i_max_a → LIM.i |
| R-31 (3.3 V pins) | no ESP32 pin above 3.4 V | baseline | LIM.v, LIM.declared |
| R-32 (module regulator) | AP2112K ≤ 200 mA, ≤ 125 °C | baseline | LIM.i, LIM.t |
| R-33 (radio band) | 2400–2483.5 MHz, ≤ 20 dBm | law | purpose.radio → LIM.band, LIM.eirp; M-6 |
| R-34 (strapping pins) | IO0, IO2, IO12, IO15 free | baseline | LVL.boot with `strap` in the T-Display's entry |
| R-35 (servo on 3.3 V) | J1's signal 0/3.3 V moves the servo | wish, should | acceptance |
| R-40 (brightness) | the five LEDs look about equally bright | wish, in the maker's words | acceptance – the pattern |

Eight requirements and half of two more restate catalog checks that are errors on every board and block the release
anyway. One restates the law that M-6 (regulatory review) checks from the purpose. The other nine are wishes of the
maker, mostly written as circuit values. R-40 is the only one that reads as the maker would say it, because in item
14 the owner picked "judged by eye" over a number.

## Why

1. **The inventory starts from the design data.** The agent's prompt (agents/requirements-engineer.md, "Sources")
   names sim.json's limits as "often a requirement whose evidence exists already", the protocol's rows as "what a
   rows pattern can match", and `edakit sim --json`. In a project designed before its file, the documents are mostly
   decisions and data, so the candidates became the checks: from evidence to sentence instead of from wish to
   evidence.
2. **edakit has no baseline.** Neither handbook 3.6, nor the skill, nor the agent says that the catalog's checks hold
   without a requirement. "A design choice is no requirement" is written down; "a catalog check is no requirement" is
   not.
3. **The format asks for engineering sentences.** "One testable sentence with quantity, limit and condition"
   (handbook 3.6, 10.4, skill section 2), and the handbook's own example "draws at most 500 mA from J1 at 4.75 to
   5.25 V". So every sentence copies sim.json's supply range, and the maker's words stay in the needs.
4. **The gate rewards restating.** A `must` without passing evidence blocks the release, and the skill says "look for
   existing evidence first – it is often there". The cheapest requirement with evidence is one that matches rows that
   exist already.
5. **The round allowed a bulk yes.** The skill lets "several that need no discussion" go into one item. Nobody asked
   per draft what the gate would miss without it. The second opinion did not run, and its checklist has no item for
   restated checks either.

What it costs: the file counts in the circuit hash. Every change voids M-1 (circuit review) and M-6 (regulatory
review) on all five boards, and their notes must list the IDs they found met. The 20 entries hide the few that
matter. And plan step 4.5 of edakit makes the file required for every project once the bell and the tree have one,
so the bell's file becomes the example that others copy.

## Proposals for edakit

- **A (baseline).** Handbook 3.6, skill requirements ("Only the circuit") and the agent ("What you look for") get
  the rule: what edakit checks on every board is no requirement. That covers ratings and derating, operating ranges,
  logic levels, strapping pins, firmware pins, and a source's and a part's limits. The agent lists such items apart,
  as "already checked by edakit", so the owner sees what edakit covers. Section 11 of the protocol starts with one
  line for the baseline: the catalog checks of stages G and E, passed or failed.
- **B (the maker's words).** A requirement says what the device must do, as its user or builder would say it, and it
  is testable by the gate's evidence or by a person at acceptance. It has a number where the maker has one or must
  choose one ("10 min waiting", "at 1–2 m"). The circuit values that follow from it (100 mA, 0.7 A, 3.8 V) belong to
  the circuit designer: they go into sim.json and the graph's notes with the requirement's ID, and reach the
  requirement as `rows`. The text is the maker's, the evidence can be technical. The example in 10.4 changes with it:
  led-bar's R-1 becomes "runs from a laptop's USB port with all eight LEDs on".
- **C (wish before evidence).** In the agent's sources, sim.json, the parts' limits, the protocol rows and
  `edakit sim --json` are sources of evidence only, never of candidates. A value that stands for a wish leads to the
  wish: i_min_a 0.1 A (D-8) leads to "the power bank stays on". Candidates of a project designed before its file come
  from the reasons in its decisions and from the README, not from its data. More than about ten candidates on a small
  board is a sign of restated checks.
- **D (a check for restating).** DOCS.baseline, a warning that also fires on drafts: a requirement whose evidence is
  only rows of catalog checks whose limits come from parts entries or the default derating adds nothing to the gate.
  A limit the project set itself does count (a source's i_min_a or i_max_a, touch_c, a transient, a criterion). The
  rows would have to carry where their limit came from; whether the simulation keeps that today is not checked.
- **E (the round).** No bulk yes over more than three drafts. Each draft comes in the maker's words, with one line
  "without it the gate would miss: …"; a draft whose line is "nothing" is not proposed. The second opinion runs after
  every first file, and its checklist gets "restates the catalog, M-6 or the firmware contract".
- **F (pilot first).** Plan step 4.5 (the file required for every project) waits for A to E and the bell's rewritten
  file.

## The bell's file under A to E (sketch)

| Requirement | Text | Evidence |
|---|---|---|
| for N-4, Nano (R-2 + R-20) | Runs from an ordinary USB power bank: it does not switch off after 10 min of waiting, and ringing does not overload it. | rows LIM.i keeps the supply on, LIM.i current from the supply; acceptance on the Christmas power bank |
| for N-4, ESP32 (R-2 + R-30) | Runs from a power bank or charger of at least 1 A, and stays on. | the same rows; acceptance |
| for N-2 (R-3) | Every LED lights clearly in its countdown step and is dark otherwise, without a glow. | rows SIM.state LED on and dark; acceptance |
| R-40 (brightness) | as today | acceptance |
| for N-5 (R-7 + R-8) | A jammed bell damages nothing, and after ringing the servo draws no current. | scenario servo-stalled, M-1; acceptance with a USB meter |
| for N-1 (R-9) | Ringing never restarts the board. | transient servo-start; ring now 5 times |
| for N-3, N-6 (R-10) | USB only: no battery, no power supply, no second socket. | M-6 |
| for N-6 (R-11) | Nothing gets too hot to touch. | touch_c in sim.json → LIM.t; 30 min powered |
| ESP32 (R-35) | The servo moves on the ESP32's 3.3 V signal. | acceptance |

Nine entries instead of 20. R-1, R-4 to R-6, R-12 and R-31 to R-34 are dropped with the reason "checked by edakit's
catalog" or "M-6". A changed file before the order means: `cart prepare` compares the release's circuit hash with
today's (docs/edakit-gaps.md, 1), so all five boards would need new gate runs, and M-1 and M-6 would have to be signed
again. The boards themselves do not change.
