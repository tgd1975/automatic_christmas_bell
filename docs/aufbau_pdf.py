#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown>=3.5"]
# ///
"""Farbringe und PDF der Bauanleitung docs/aufbau.md, wie pytree's hardware/aufbau.py.

    uv run docs/aufbau_pdf.py 2>&1 | cat          # Farbringe, dann build/aufbau/aufbau.pdf (Chromium headless)
    uv run docs/aufbau_pdf.py ringe 2>&1 | cat    # nur die Farbringe → docs/img/ringe_*.svg

Die Farbringe der Widerstände (5 Ringe, 1 %-Metallschicht) rechnet RINGE aus dem Wert. Das PDF ist erzeugt und bleibt
in build/ (D-22).
"""
import re
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


# Seitenumbruch vor diesen Abschnitten (h2), damit Tabellen und Schritte nicht zerreißen
NEUE_SEITE = ("Was du lötest", "Reihenfolge", "7 ·", "9 ·")


def main():
    import markdown
    ringe()
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
    {"pdf": main, "ringe": ringe}[sys.argv[1] if len(sys.argv) > 1 else "pdf"]()
