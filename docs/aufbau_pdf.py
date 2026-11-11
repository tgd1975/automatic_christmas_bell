#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown>=3.5"]
# ///
"""PDF der Bauanleitung docs/aufbau.md zum Ausdrucken, wie pytree's hardware/aufbau.py.

    uv run docs/aufbau_pdf.py 2>&1 | cat     # → build/aufbau/aufbau.pdf (Chromium headless)

Das PDF ist erzeugt und bleibt in build/ (D-22).
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
table { border-collapse: collapse; margin: 2mm 0 3mm; font-size: 9pt; break-inside: avoid; }
th, td { border: 0.3pt solid #bbb; padding: 1mm 2mm; text-align: left; vertical-align: top; }
th { background: #eceae4; }
td img { width: 84mm; margin: 0; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt; }
pre { background: #f3f1ec; padding: 2mm 3mm; font-size: 8.4pt; white-space: pre-wrap; break-inside: avoid; }
img { display: block; margin: 3mm auto; break-inside: avoid; }
a { color: #1f5c3a; text-decoration: none; }
"""

# Seitenumbruch vor diesen Abschnitten (h2), damit Tabellen und Schritte nicht zerreißen
NEUE_SEITE = ("Was du lötest", "Reihenfolge", "7 ·", "9 ·")


def main():
    import markdown
    text = (REPO / "docs/aufbau.md").read_text(encoding="utf-8")
    # Python-Markdown braucht 4 Leerzeichen für Folgeabsätze in Listen, das Repo schreibt 3 (GitHub-Stil)
    text = re.sub(r"(?m)^   (?=\S)", "    ", text)
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    html = html.replace('src="img/', f'src="{(REPO / "docs/img").as_uri()}/')
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
    main()
