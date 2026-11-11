#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.5"]
# ///
"""Bilder und PDF der Bauanleitung docs/aufbau.md, wie pytree's hardware/aufbau.py.

    uv run docs/aufbau.py 2>&1 | cat           # Bilder, dann build/aufbau/aufbau.pdf (Chromium headless)
    uv run docs/aufbau.py bilder 2>&1 | cat    # nur die Bilder → docs/img/ringe_*.svg, docs/img/messen_*.svg

Die Farbringe der Widerstände (5 Ringe, 1 %-Metallschicht) rechnet RINGE aus dem Wert. Die Messbilder legen Punkte und
Schilder über die Ansicht der bestellten Platine (docs/img/aufbau_<platine>_oben.svg bzw. _unten.svg, Kopien der
Ansichten des Releases vom 2026-11-01, rev 1.0); wo ein Punkt liegt, rechnet pad() aus der Bauteilgeometrie
(variants/<platine>/hardware/boards/<platine>.geometry.json) und der Platzierung im Board-File. Das PDF ist erzeugt
und bleibt in build/ (D-22).
"""
import json
import math
import re
import tomllib
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PDF = REPO / "build/aufbau/aufbau.pdf"

CSS = """
@page { size: A4; margin: 15mm 15mm 15mm 15mm; }
body { font-family: "DejaVu Sans", sans-serif; font-size: 10pt; line-height: 1.38; color: #1d1d1d; }
h1 { font-size: 19pt; margin: 0 0 4mm; color: #1f5c3a; }
h2 { font-size: 14pt; margin: 6mm 0 2mm; color: #1f5c3a; break-after: avoid; }
h3 { font-size: 12pt; margin: 4mm 0 2mm; break-after: avoid; }
h2.seite { break-before: page; }
p, li { orphans: 3; widows: 3; }
p:has(+ table) { break-after: avoid; }
table { border-collapse: collapse; margin: 2mm 0 3mm; font-size: 9pt; break-inside: avoid; }
th, td { border: 0.3pt solid #bbb; padding: 1mm 2mm; text-align: left; vertical-align: top; }
th { background: #eceae4; }
td img { width: 84mm; margin: 0; }
td img.ringe { display: inline; width: auto; height: 11mm; margin: 0; vertical-align: middle; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt; }
pre { background: #f3f1ec; padding: 2mm 3mm; font-size: 8.4pt; white-space: pre-wrap; break-inside: avoid; }
img { display: block; margin: 3mm auto; break-inside: avoid; }
a { color: #1f5c3a; text-decoration: none; }
"""

# Farbringe: Wert in Ω → Dateiname; die Ringe aus dem Wert (3 Ziffern, Multiplikator, Toleranz 1 % = braun)
RINGE = {100: ("100", "100 Ω"), 330: ("330", "330 Ω"), 4700: ("4k7", "4,7 kΩ")}
FARBEN = ["#000000", "#7a3e12", "#d42020", "#f07a10", "#f5d000", "#2e9e3e", "#2060d0", "#8a2be2", "#8a8a8a",
          "#ffffff"]  # schwarz, braun, rot, orange, gelb, grün, blau, violett, grau, weiß
KOERPER, BEIN, RAND = "#8fc3e6", "#9a9a9a", "#3d5f78"


def ringe_von(wert):
    """Die fünf Ringe eines 1 %-Widerstands: drei Ziffern, Multiplikator, Toleranz."""
    exp = len(str(int(wert))) - 3
    z = f"{wert:d}"[:3].ljust(3, "0")
    return [int(z[0]), int(z[1]), int(z[2]), exp, 1]


def ringe():
    aus = REPO / "docs/img"
    for wert, (name, text) in RINGE.items():
        r = ringe_von(wert)
        streifen = "".join(f'<rect x="{x}" y="3" width="4" height="18" fill="{FARBEN[f]}" stroke="#555" '
                           f'stroke-width="0.3"/>' for x, f in zip((26, 33, 40, 47, 63), r))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60" viewBox="0 0 100 24">'
               f'<title>{text}</title>'
               f'<rect x="0" y="11" width="100" height="2" fill="{BEIN}"/>'
               f'<rect x="16" y="3" width="68" height="18" rx="7" fill="{KOERPER}" stroke="{RAND}" stroke-width="0.6"/>'
               f"{streifen}</svg>\n")
        (aus / f"ringe_{name}.svg").write_text(svg, encoding="utf-8")
    print(f"Farbringe → docs/img/ringe_{{{','.join(n for n, _ in RINGE.values())}}}.svg")


# ---- Messbilder ---------------------------------------------------------------------------------------------------

BREITE, HOEHE = 85.0, 56.0                       # Platine in mm; die Ansicht zeichnet y nach unten
ROT, SCHWARZ, BLAU = "#e0201b", "#111111", "#1f6fd1"


def pad(platine, ref, nr):
    """Lage von Pad nr des Bauteils ref in Plan-mm (y nach oben) aus Geometrie und Platzierung."""
    v = REPO / "variants" / platine / "hardware/boards"
    geo = json.loads((v / f"{platine}.geometry.json").read_text())
    ort = tomllib.loads((v / f"{platine}.toml").read_text())["place"][ref]
    p = geo[ref]["pads"][str(nr)]
    x, y, r = p["x"] * 0.0254, p["y"] * 0.0254, math.radians(ort["rot"])
    return ort["x"] + x * math.cos(r) - y * math.sin(r), ort["y"] + x * math.sin(r) + y * math.cos(r)


def schild(x, y, text, farbe, fs=2.4):
    b = 0.62 * fs * len(text) + 1.6
    return (f'<rect x="{x - b / 2:.2f}" y="{y - fs * 0.75:.2f}" width="{b:.2f}" height="{fs * 1.5:.2f}" rx="0.6" '
            f'fill="{farbe}" stroke="white" stroke-width="0.25"/>'
            f'<text x="{x:.2f}" y="{y + fs * 0.36:.2f}" font-family="DejaVu Sans, sans-serif" font-weight="bold" '
            f'font-size="{fs}" fill="white" text-anchor="middle">{text}</text>')


def messbild(platine, seite, punkte, paare=(), name=""):
    """punkte: (ref, pad, text, farbe, schild_x, schild_y) in Plan-mm; paare: Paare von Punkt-Indizes, gestrichelt
    verbunden (Durchgang)."""
    grund = (REPO / f"docs/img/aufbau_{platine}_{seite}.svg").read_text(encoding="utf-8")

    def svg(x, y):                               # Plan-mm → Ansicht; unten ist gespiegelt
        return (BREITE - x if seite == "unten" else x), HOEHE - y

    lagen = [(svg(*pad(platine, ref, nr)), text, farbe, svg(sx, sy)) for ref, nr, text, farbe, sx, sy in punkte]
    teile = ['<rect x="-3" y="-3" width="92" height="63" fill="black" opacity="0.35"/>']
    for a, b in paare:
        (x1, y1), (x2, y2) = lagen[a][0], lagen[b][0]
        teile.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="white" '
                     f'stroke-width="0.9" stroke-linecap="round"/>'
                     f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{BLAU}" '
                     f'stroke-width="0.45" stroke-dasharray="1.2 0.8"/>')
    for (px, py), text, farbe, (sx, sy) in lagen:
        teile.append(f'<line x1="{px:.2f}" y1="{py:.2f}" x2="{sx:.2f}" y2="{sy:.2f}" stroke="white" stroke-width="0.7"/>'
                     f'<line x1="{px:.2f}" y1="{py:.2f}" x2="{sx:.2f}" y2="{sy:.2f}" stroke="{farbe}" '
                     f'stroke-width="0.35"/>')
    for (px, py), text, farbe, (sx, sy) in lagen:
        teile.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="1.35" fill="none" stroke="white" stroke-width="0.9"/>'
                     f'<circle cx="{px:.2f}" cy="{py:.2f}" r="1.35" fill="none" stroke="{farbe}" stroke-width="0.5"/>'
                     + schild(sx, sy, text, farbe))
    aus = REPO / f"docs/img/messen_{platine}_{name}.svg"
    aus.write_text(grund.replace("</svg>", f'<g id="messen">{"".join(teile)}</g></svg>'), encoding="utf-8")
    return aus.name


def fächer(platine, refs_nr_text, farbe, y, mitte, abstand):
    """Schilder in einer Reihe auf Höhe y, nach x der Punkte sortiert, um mitte verteilt."""
    reihe = sorted(refs_nr_text, key=lambda t: pad(platine, t[0], t[1])[0])
    x0 = mitte - abstand * (len(reihe) - 1) / 2
    return [(ref, nr, text, farbe, x0 + i * abstand, y) for i, (ref, nr, text) in enumerate(reihe)]


# Die Buchsen des Moduls je Netz (Pad-Nummern aus der Geometrie): THT Nano, ESP32 THT T-Display
BUCHSE = {
    "tht": {"5V": 27, "GND": 29, "SIG": 11, "LED5": 9, "LED4": 8, "LED3": 5, "LED2": 6, "LED1": 7,
            "START": 14, "RESET": 15},
    "esp32tht": {"5V": 1, "GND": 2, "SIG": 17, "LED5": 3, "LED4": 4, "LED3": 5, "LED2": 6, "LED1": 7,
                 "START": 9, "RESET": 10, "3V3": 12},
}
NETZ = {"5V": "+5V", "GND": "GND", "SIG": "SERVO", "LED5": "LED_G1", "LED4": "LED_G2", "LED3": "LED_Y1",
        "LED2": "LED_Y2", "LED1": "LED_R", "START": "BTN_START", "RESET": "BTN_RESET", "3V3": "+3V3"}


def buchsen_prüfen():
    """Jede Buchse in BUCHSE liegt am Netz, das ihr Name sagt – sonst zeigt ein Bild auf das falsche Loch."""
    for platine, buchsen in BUCHSE.items():
        geo = json.loads((REPO / f"variants/{platine}/hardware/boards/{platine}.geometry.json").read_text())
        for text, nr in buchsen.items():
            netz = geo["U1"]["pads"][str(nr)]["net"]
            if netz != NETZ[text]:
                sys.exit(f"{platine}: Buchse {text} = U1.{nr} liegt an {netz}, nicht an {NETZ[text]}")
        for nr, text in ((1, "GND"), (2, "5V"), (3, "SIG")):
            if geo["J1"]["pads"][str(nr)]["net"] != NETZ[text]:
                sys.exit(f"{platine}: J1.{nr} ist nicht {text}")


def messbilder():
    buchsen_prüfen()
    namen = []
    for platine, b in BUCHSE.items():
        oben = platine == "tht"                  # Nano: LED- und Tasterbuchsen in der oberen Reihe
        ry = 28.0 if oben else 21.0              # Schilderreihe im Feld des Moduls
        gnd = ("J1", 1, "GND", SCHWARZ, 73.0, 22.0)
        v5 = ("J1", 2, "5V", ROT, 73.0, 37.0)
        # 1 Versorgung
        punkte = [v5, gnd]
        if platine == "esp32tht":
            punkte.append(("U1", b["3V3"], "3V3", ROT, 44.5, 22.0))
        namen.append(messbild(platine, "oben", punkte, name="versorgung"))
        # 2 LEDs: Diodentest Buchse (rot) gegen GND (schwarz)
        leds = fächer(platine, [("U1", b[t], t) for t in ("LED5", "LED4", "LED3", "LED2", "LED1")], ROT, ry, 24.0,
                      9.5)
        namen.append(messbild(platine, "oben", leds + [gnd], name="leds"))
        # 3 Taster
        taster = fächer(platine, [("U1", b["START"], "START"), ("U1", b["RESET"], "RESET")], ROT, ry,
                        10.0 if oben else 33.0, 11.0)
        gegen = [v5] if oben else [("U1", b["3V3"], "3V3", SCHWARZ, 49.0, ry), gnd]
        namen.append(messbild(platine, "oben", taster + gegen, name="taster"))
        # 4 Durchgang Buchse ↔ J1
        punkte = [("U1", b["5V"], "a", BLAU, *(pad(platine, "U1", b["5V"])[0] + 2.5, ry)),
                  ("U1", b["GND"], "b", BLAU, *(pad(platine, "U1", b["GND"])[0] + 2.5, ry + (4 if oben else -4))),
                  ("U1", b["SIG"], "c", BLAU, *(pad(platine, "U1", b["SIG"])[0] + 1.0, ry + (-4 if oben else 4))),
                  ("J1", 2, "a", BLAU, 85.5, 30.0), ("J1", 1, "b", BLAU, 85.5, 25.5), ("J1", 3, "c", BLAU, 85.5, 34.5)]
        namen.append(messbild(platine, "oben", punkte, paare=((0, 3), (1, 4), (2, 5)), name="durchgang"))
    # 5 Mit Modul: 3V3 des T-Displays von unten
    namen.append(messbild("esp32tht", "unten", [("U1", BUCHSE["esp32tht"]["3V3"], "3V3", ROT, 44.5, 6.0),
                                                ("J1", 1, "GND", SCHWARZ, 74.0, 22.0)], name="3v3_unten"))
    print(f"Messbilder → docs/img/{{{', '.join(namen)}}}")


def bilder():
    ringe()
    messbilder()


# Seitenumbruch vor diesen Abschnitten (h2), damit Tabellen und Schritte nicht zerreißen
NEUE_SEITE = ("Was du lötest", "Reihenfolge", "8 ·", "9 ·")


def main():
    import markdown
    bilder()
    text = (REPO / "docs/aufbau.md").read_text(encoding="utf-8")
    # Python-Markdown braucht 4 Leerzeichen für Folgeabsätze in Listen, das Repo schreibt 3 (GitHub-Stil)
    text = re.sub(r"(?m)^   (?=\S)", "    ", text)
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    html = html.replace('src="img/', f'src="{(REPO / "docs/img").as_uri()}/')
    html = re.sub(r'<img alt="([^"]*)" src="([^"]*ringe_\w+\.svg)"', r'<img class="ringe" alt="\1" src="\2"', html)
    for anfang in NEUE_SEITE:
        html = html.replace(f"<h2>{anfang}", f'<h2 class="seite">{anfang}')
    # Verweise ins Repository führen im Ausdruck nirgendwohin – als Text lassen
    html = re.sub(r'<a href="(?!https?:)[^"]*">([^<]*)</a>', r"\1", html)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    seite = PDF.with_suffix(".html")
    seite.write_text(f'<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><title>Weihnachtsglocke – Aufbau'
                     f"</title><style>{CSS}</style></head><body>{html}</body></html>", encoding="utf-8")
    exe = next((shutil.which(n) for n in ("chromium", "chromium-browser", "google-chrome") if shutil.which(n)), None)
    if not exe:
        sys.exit("Kein Chromium/Chrome gefunden")
    subprocess.run([exe, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    "--virtual-time-budget=10000", f"--print-to-pdf={PDF}", seite.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"PDF → {PDF.relative_to(REPO)}")


if __name__ == "__main__":
    {"pdf": main, "bilder": bilder}[sys.argv[1] if len(sys.argv) > 1 else "pdf"]()
