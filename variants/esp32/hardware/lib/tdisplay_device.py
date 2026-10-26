"""LILYGO T-Display V1.1 in EasyEDA: the project's copies of symbol and footprint of the 2x12 female header C18722937
(2541FV-2x12P), rebuilt into the T-Display's (D-13). The T-Display is neither in EasyEDA's library nor at LCSC, and a
device created through the API cannot be placed in the local client ("Device details data does not exist"); a system
part can, and EasyEDA keeps its symbol and footprint as copies in the project, which may be edited – the way the pytree
project builds its RP2350-Zero from the RP2040-Zero.

    uv run --project <edakit> python variants/esp32/hardware/lib/tdisplay_device.py [symbol] [footprint] [check]

The header must be placed once (edakit schematic create) so that the project has the copies; afterwards edakit places
it with the rebuilt symbol, and the PCB gets the rebuilt footprint. Only the board esp32 uses C18722937.

Sources (variants/esp32/hardware/parts/C18722937.json): LILYGO's pin map "ESP32 TTGO T-Display V1.1", the schematic
ESP32-TFT(6-26) (headers P4/P5) and the KiCad and Eagle libraries in the LILYGO repository – all agree on the pin
order. Board 25.09 x 51.49 mm, two rows of 12 pins, pitch 2.54 mm, rows 22.86 mm apart; the first pin of each row sits
15.93 mm from the USB end. The holes are 1.1 mm like the Nano's (D-7): the module plugs into two 1x12 female headers
whose 0.64 mm square tails need them.

Footprint as seen from the top, USB end at -y: right row pins 1-12 (1 = 5V at the USB end), left row pins 13-24
(13 = 3V3 at the USB end). The symbol shows both rows in the same order. Origin: centre of the pin field.
"""

import sys
import time
from pathlib import Path

from edakit import config, eda

HERE = Path(__file__).resolve().parent
CFG = HERE.parents[1] / "edakit.toml"
MIL = 1 / 0.0254

STANDIN = "C18722937"  # 2541FV-2x12P: its symbol has pins 1-24 and the prefix U
PINS = {  # number: name, right row 1-12 from the USB end, left row 13-24 from the USB end
    1: "5V", 2: "GND", 3: "IO27", 4: "IO26", 5: "IO25", 6: "IO33", 7: "IO32", 8: "IO39", 9: "IO38", 10: "IO37",
    11: "IO36", 12: "3V3",
    13: "3V3", 14: "GND", 15: "GND", 16: "IO12", 17: "IO13", 18: "IO15", 19: "IO2", 20: "IO17", 21: "IO22",
    22: "IO21", 23: "GND", 24: "GND",
}
ROW_X = 11.43          # mm from the centre, 22.86 mm between the rows
PITCH = 2.54
PAD, HOLE = 1.7, 1.1   # mm
OUTLINE = (-12.83, -30.2, 12.83, 21.9)  # module 25.09 x 51.49 mm plus 0.15 mm, so the line stays clear of the pads
USB = (-4.6, -29.9, 4.6, -27.9)         # USB-C receptacle at the module end (not past it: board edge, M-5)
SILK = 3                                # top silkscreen
TEXT_MM = 1.5                           # font size: capitals about 1.05 mm (JLCPCB: at least 1 mm)
SHAPE = 48                              # component shape: the outline edakit and EasyEDA take as the part's extent
HEADER_LAYERS = (SILK, SHAPE, 49, 50)   # the header's outline, pin-1 mark and pin marks go; 49/50 are not redrawn


def pin_xy(n):
    """Pad centre in mm, footprint seen from the top, USB end at -y."""
    i = (n - 1) % 12
    return (ROW_X if n <= 12 else -ROW_X), -5.5 * PITCH + i * PITCH


def rect_poly(x0, y0, x1, y1):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    poly = [round(pts[0][0] * MIL, 2), round(pts[0][1] * MIL, 2), "L"]
    for x, y in pts[1:] + pts[:1]:
        poly += [round(x * MIL, 2), round(y * MIL, 2)]
    return {"$polygon": poly}


def api(mcp, path, *args, timeout=130):
    return eda.api(mcp, path, *args, timeout=timeout)


def copies(mcp, cfg):
    """Symbol and footprint copies of the stand-in, from a placed instance on the template of the board."""
    board = cfg.board()
    sch_uuid, pages = eda.find_pages(mcp, board.template)
    eda.focus_page(mcp, sch_uuid, pages[0])
    for c in (eda.state(x) for x in api(mcp, "SCH_PrimitiveComponent.getAll", "part") or []):
        if c.get("SupplierId") == STANDIN:
            return c["Symbol"]["uuid"], c["Footprint"]["uuid"]
    raise SystemExit(f"no {STANDIN} on '{board.template}' – run `edakit schematic create` first")


def open_editor(mcp, cls, uuid, project):
    """Open a library document of the project and wait until it is the active document."""
    try:
        api(mcp, f"{cls}.openInEditor", uuid, project, timeout=30)
    except eda.MCPError as e:
        print(f"  ({cls}.openInEditor: {str(e)[:80]})")
    for _ in range(30):
        cur = api(mcp, "DMT_SelectControl.getCurrentDocumentInfo") or {}
        if cur.get("uuid") == uuid:
            time.sleep(2)
            return cur["tabId"]
        time.sleep(1)
    raise SystemExit(f"{cls} {uuid} did not become the active document")


def rebuild_symbol(mcp, uuid, project):
    """Pins are deleted and created anew: SCH_PrimitivePin.modify is not saved. Body 120 x 130 (10 mil units), pins
    10 long and 10 apart; the top of each side is the row's far end, as on the module."""
    tab = open_editor(mcp, "LIB_Symbol", uuid, project)
    for cls in ("SCH_PrimitivePin", "SCH_PrimitiveRectangle", "SCH_PrimitivePolygon", "SCH_PrimitiveCircle"):
        old = api(mcp, f"{cls}.getAllPrimitiveId") or []
        if old:
            api(mcp, f"{cls}.delete", old)
    api(mcp, "SCH_PrimitiveRectangle.create", -60, 65, 120, 130, 0, 0, None, None, 1, 0)
    for n, name in PINS.items():
        y = -55 + ((n - 1) % 12) * 10
        x, rot = (70, 0) if n <= 12 else (-70, 180)
        if not api(mcp, "SCH_PrimitivePin.create", x, y, str(n), name, rot, 10):
            raise SystemExit(f"pin {n} not created")
    pins = {p["PinNumber"]: p["PinName"] for p in map(eda.state, api(mcp, "SCH_PrimitivePin.getAll") or [])}
    print(f"  symbol: {len(pins)} pins, saved {api(mcp, 'SCH_Document.save')}")
    api(mcp, "DMT_EditorControl.closeDocument", tab)


def rebuild_footprint(mcp, uuid, project):
    tab = open_editor(mcp, "LIB_Footprint", uuid, project)
    old = api(mcp, "PCB_PrimitivePad.getAllPrimitiveId") or []
    if old:
        api(mcp, "PCB_PrimitivePad.delete", old)
    for cls in ("PCB_PrimitivePolyline", "PCB_PrimitiveLine", "PCB_PrimitiveArc", "PCB_PrimitiveFill",
                "PCB_PrimitiveString"):
        for prim in map(eda.state, api(mcp, f"{cls}.getAll") or []):
            if prim.get("Layer") in HEADER_LAYERS:
                api(mcp, f"{cls}.delete", [prim["PrimitiveId"]])
    d, hole = round(PAD * MIL, 2), ["ROUND", round(HOLE * MIL, 2)]
    for n in sorted(PINS):
        x, y = pin_xy(n)
        shape = ["RECT", d, d, 0] if n in (1, 13) else ["ELLIPSE", d, d]  # square pad: USB end of each row
        if not api(mcp, "PCB_PrimitivePad.create", 12, str(n), round(x * MIL, 2), round(y * MIL, 2), 0, shape, "", hole,
                   0, 0, 0, True):
            raise SystemExit(f"pad {n} not created")
    api(mcp, "PCB_PrimitivePolyline.create", "", SILK, rect_poly(*OUTLINE), 6)
    api(mcp, "PCB_PrimitivePolyline.create", "", SILK, rect_poly(*USB), 6)
    api(mcp, "PCB_PrimitivePolyline.create", "", SHAPE, rect_poly(*OUTLINE), 6)
    api(mcp, "PCB_PrimitiveString.create", SILK, 0, round(-25.8 * MIL, 2), "USB", "default", round(TEXT_MM * MIL, 2), 6,
        5, 0, False, 0, False, False)
    api(mcp, "PCB_PrimitiveString.create", SILK, 0, round(18.3 * MIL, 2), "T-Display", "default", round(TEXT_MM * MIL, 2),
        6, 5, 0, False, 0, False, False)
    pads = list(map(eda.state, api(mcp, "PCB_PrimitivePad.getAll") or []))
    print(f"  footprint: {len(pads)} pads, saved {api(mcp, 'PCB_Document.save')}")
    api(mcp, "DMT_EditorControl.closeDocument", tab)


def check(mcp, cfg, sym, fp, project):
    """Reopen both copies and compare them with PINS and the pad positions."""
    tab = open_editor(mcp, "LIB_Symbol", sym, project)
    pins = {p["PinNumber"]: p["PinName"] for p in map(eda.state, api(mcp, "SCH_PrimitivePin.getAll") or [])}
    api(mcp, "DMT_EditorControl.closeDocument", tab)
    tab = open_editor(mcp, "LIB_Footprint", fp, project)
    pads = {p["PadNumber"]: (p["X"], p["Y"]) for p in map(eda.state, api(mcp, "PCB_PrimitivePad.getAll") or [])}
    api(mcp, "DMT_EditorControl.closeDocument", tab)
    bad = [n for n, name in PINS.items() if pins.get(str(n)) != name]
    bad += [f"pad {n}" for n in PINS if not pads.get(str(n)) or
            max(abs(a - round(b * MIL, 2)) for a, b in zip(pads[str(n)], pin_xy(n))) > 0.5]
    print(f"  check: {len(pins)} pins, {len(pads)} pads" + (f", differ: {bad}" if bad else ", all as drawn"))
    return not bad


def main():
    what = sys.argv[1:] or ["symbol", "footprint", "check"]
    cfg = config.load(CFG)
    mcp = eda.connect(cfg)
    try:
        project = eda.open_project(mcp, cfg)
        sym, fp = copies(mcp, cfg)
        print(f"{STANDIN} in the project: symbol {sym}, footprint {fp}")
        ok = True
        for step in what:
            if step == "symbol":
                rebuild_symbol(mcp, sym, project)
            elif step == "footprint":
                rebuild_footprint(mcp, fp, project)
            elif step == "check":
                ok = check(mcp, cfg, sym, fp, project)
        mcp.call("easyeda_project_save", projectId="current", confirmWrite=True)
        return 0 if ok else 2
    finally:
        mcp.close()


if __name__ == "__main__":
    sys.exit(main())
